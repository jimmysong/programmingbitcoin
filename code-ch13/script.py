from io import BytesIO
from logging import getLogger
from unittest import TestCase

from helper import (
    decode_base58,
    encode_varint,
    h160_to_p2pkh_address,
    h160_to_p2sh_address,
    int_to_little_endian,
    little_endian_to_int,
    read_varint,
    sha256,
)
from op import (
    op_equal,
    op_hash160,
    op_verify,
    OP_CODE_FUNCTIONS,
    OP_CODE_NAMES,
)


def p2pkh_script(h160):
    '''Takes a hash160 and returns the p2pkh ScriptPubKey'''
    return Script([0x76, 0xa9, h160, 0x88, 0xac])


def p2sh_script(h160):
    '''Takes a hash160 and returns the p2sh ScriptPubKey'''
    return Script([0xa9, h160, 0x87])


# tag::source1[]
def p2wpkh_script(h160):
    '''Takes a hash160 and returns the p2wpkh ScriptPubKey'''
    return Script([0x00, h160])  # <1>
# end::source1[]


# tag::source4[]
def p2wsh_script(h256):
    '''Takes a hash160 and returns the p2wsh ScriptPubKey'''
    return Script([0x00, h256])  # <1>
# end::source4[]


LOGGER = getLogger(__name__)


class Script:

    def __init__(self, instructions=None):
        if instructions is None:
            self.instructions = []
        else:
            self.instructions = instructions

    def __repr__(self):
        result = []
        for instruction in self.instructions:
            if type(instruction) == int:
                if OP_CODE_NAMES.get(instruction):
                    name = OP_CODE_NAMES.get(instruction)
                else:
                    name = 'OP_[{}]'.format(instruction)
                result.append(name)
            else:
                result.append(instruction.hex())
        return ' '.join(result)

    def __add__(self, other):
        return Script(self.instructions + other.instructions)

    @classmethod
    def parse(cls, s):
        # get the length of the entire field
        length = read_varint(s)
        # initialize the instructions array
        instructions = []
        # initialize the number of bytes we've read to 0
        count = 0
        # loop until we've read length bytes
        while count < length:
            # get the current byte
            current = s.read(1)
            # increment the bytes we've read
            count += 1
            # convert the current byte to an integer
            current_byte = current[0]
            # if the current byte is between 1 and 75 inclusive
            if current_byte >= 1 and current_byte <= 75:
                # we have an instruction set n to be the current byte
                n = current_byte
                # add the next n bytes as an instruction
                instructions.append(s.read(n))
                # increase the count by n
                count += n
            elif current_byte == 76:
                # op_pushdata1
                data_length = little_endian_to_int(s.read(1))
                instructions.append(s.read(data_length))
                count += data_length + 1
            elif current_byte == 77:
                # op_pushdata2
                data_length = little_endian_to_int(s.read(2))
                instructions.append(s.read(data_length))
                count += data_length + 2
            else:
                # we have an opcode. set the current byte to op_code
                op_code = current_byte
                # add the op_code to the list of instructions
                instructions.append(op_code)
        if count != length:
            raise SyntaxError('parsing script failed')
        return cls(instructions)

    def raw_serialize(self):
        # initialize what we'll send back
        result = b''
        # go through each instruction
        for instruction in self.instructions:
            # if the instruction is an integer, it's an opcode
            if type(instruction) == int:
                # turn the instruction into a single byte integer using int_to_little_endian
                result += int_to_little_endian(instruction, 1)
            else:
                # otherwise, this is an element
                # get the length in bytes
                length = len(instruction)
                # for large lengths, we have to use a pushdata opcode
                if length < 75:
                    # turn the length into a single byte integer
                    result += int_to_little_endian(length, 1)
                elif length > 75 and length < 0x100:
                    # 76 is pushdata1
                    result += int_to_little_endian(76, 1)
                    result += int_to_little_endian(length, 1)
                elif length >= 0x100 and length <= 520:
                    # 77 is pushdata2
                    result += int_to_little_endian(77, 1)
                    result += int_to_little_endian(length, 2)
                else:
                    raise ValueError('too long an instruction')
                result += instruction
        return result

    def serialize(self):
        # get the raw serialization (no prepended length)
        result = self.raw_serialize()
        # get the length of the whole thing
        total = len(result)
        # encode_varint the total length of the result and prepend
        return encode_varint(total) + result

    def evaluate(self, z, witness):
        # create a copy as we may need to add to this list if we have a
        # RedeemScript
        instructions = self.instructions[:]
        stack = []
        altstack = []
        while len(instructions) > 0:
            instruction = instructions.pop(0)
            if type(instruction) == int:
                # do what the opcode says
                operation = OP_CODE_FUNCTIONS[instruction]
                if instruction in (99, 100):
                    # op_if/op_notif require the instructions array
                    if not operation(stack, instructions):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[instruction]))
                        return False
                elif instruction in (107, 108):
                    # op_toaltstack/op_fromaltstack require the altstack
                    if not operation(stack, altstack):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[instruction]))
                        return False
                elif instruction in (172, 173, 174, 175):
                    # these are signing operations, they need a sig_hash
                    # to check against
                    if not operation(stack, z):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[instruction]))
                        return False
                else:
                    if not operation(stack):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[instruction]))
                        return False
            else:
                # add the instruction to the stack
                stack.append(instruction)
                # p2sh rule. if the next three instructions are:
                # OP_HASH160 <20 byte hash> OP_EQUAL this is the RedeemScript
                # OP_HASH160 == 0xa9 and OP_EQUAL == 0x87
                if len(instructions) == 3 and instructions[0] == 0xa9 \
                    and type(instructions[1]) == bytes and len(instructions[1]) == 20 \
                    and instructions[2] == 0x87:
                    redeem_script = encode_varint(len(instruction)) + instruction
                    # we execute the next three opcodes
                    instructions.pop()
                    h160 = instructions.pop()
                    instructions.pop()
                    if not op_hash160(stack):
                        return False
                    stack.append(h160)
                    if not op_equal(stack):
                        return False
                    # final result should be a 1
                    if not op_verify(stack):
                        LOGGER.info('bad p2sh h160')
                        return False
                    # hashes match! now add the RedeemScript
                    redeem_script = encode_varint(len(instruction)) + instruction
                    stream = BytesIO(redeem_script)
                    instructions.extend(Script.parse(stream).instructions)
                # witness program version 0 rule. if stack instructions are:
                # 0 <20 byte hash> this is p2wpkh
                # tag::source3[]
                if len(stack) == 2 and stack[0] == b'' and len(stack[1]) == 20:  # <1>
                    h160 = stack.pop()
                    stack.pop()
                    instructions.extend(witness)
                    instructions.extend(p2pkh_script(h160).instructions)
                # end::source3[]
                # witness program version 0 rule. if stack instructions are:
                # 0 <32 byte hash> this is p2wsh
                # tag::source6[]
                if len(stack) == 2 and stack[0] == b'' and len(stack[1]) == 32:
                    s256 = stack.pop()  # <1>
                    stack.pop()  # <2>
                    instructions.extend(witness[:-1])  # <3>
                    witness_script = witness[-1]  # <4>
                    if s256 != sha256(witness_script):  # <5>
                        print('bad sha256 {} vs {}'.format
                            (s256.hex(), sha256(witness_script).hex()))
                        return False
                    stream = BytesIO(encode_varint(len(witness_script)) 
                        + witness_script)
                    witness_script_instructions = Script.parse(stream).instructions  # <6>
                    instructions.extend(witness_script_instructions)
                # end::source6[]
        if len(stack) == 0:
            return False
        if stack.pop() == b'':
            return False
        return True

    def is_p2pkh_script_pubkey(self):
        '''Returns whether this follows the
        OP_DUP OP_HASH160 <20 byte hash> OP_EQUALVERIFY OP_CHECKSIG pattern.'''
        # there should be exactly 5 instructions
        # OP_DUP (0x76), OP_HASH160 (0xa9), 20-byte hash, OP_EQUALVERIFY (0x88),
        # OP_CHECKSIG (0xac)
        return len(self.instructions) == 5 and self.instructions[0] == 0x76 \
            and self.instructions[1] == 0xa9 \
            and type(self.instructions[2]) == bytes and len(self.instructions[2]) == 20 \
            and self.instructions[3] == 0x88 and self.instructions[4] == 0xac

    def is_p2sh_script_pubkey(self):
        '''Returns whether this follows the
        OP_HASH160 <20 byte hash> OP_EQUAL pattern.'''
        # there should be exactly 3 instructions
        # OP_HASH160 (0xa9), 20-byte hash, OP_EQUAL (0x87)
        return len(self.instructions) == 3 and self.instructions[0] == 0xa9 \
            and type(self.instructions[1]) == bytes and len(self.instructions[1]) == 20 \
            and self.instructions[2] == 0x87

    # tag::source2[]
    def is_p2wpkh_script_pubkey(self):  # <2>
        return len(self.instructions) == 2 and self.instructions[0] == 0x00 \
            and type(self.instructions[1]) == bytes and len(self.instructions[1]) == 20
    # end::source2[]

    # tag::source5[]
    def is_p2wsh_script_pubkey(self):
        return len(self.instructions) == 2 and self.instructions[0] == 0x00 \
            and type(self.instructions[1]) == bytes and len(self.instructions[1]) == 32
    # end::source5[]

    def address(self, testnet=False):
        '''Returns the address corresponding to the script'''
        if self.is_p2pkh_script_pubkey():  # p2pkh
            # hash160 is the 3rd instruction
            h160 = self.instructions[2]
            # convert to p2pkh address using h160_to_p2pkh_address (remember testnet)
            return h160_to_p2pkh_address(h160, testnet)
        elif self.is_p2sh_script_pubkey():  # p2sh
            # hash160 is the 2nd instruction
            h160 = self.instructions[1]
            # convert to p2sh address using h160_to_p2sh_address (remember testnet)
            return h160_to_p2sh_address(h160, testnet)
        raise ValueError('Unknown ScriptPubKey')


class ScriptTest(TestCase):

    def test_parse(self):
        script_pubkey = BytesIO(bytes.fromhex('6a47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937'))
        script = Script.parse(script_pubkey)
        want = bytes.fromhex('304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a71601')
        self.assertEqual(script.instructions[0].hex(), want.hex())
        want = bytes.fromhex('035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937')
        self.assertEqual(script.instructions[1], want)

    def test_serialize(self):
        want = '6a47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937'
        script_pubkey = BytesIO(bytes.fromhex(want))
        script = Script.parse(script_pubkey)
        self.assertEqual(script.serialize().hex(), want)

    def test_address(self):
        address_1 = '1BenRpVUFK65JFWcQSuHnJKzc4M8ZP8Eqa'
        h160 = decode_base58(address_1)
        p2pkh_script_pubkey = p2pkh_script(h160)
        self.assertEqual(p2pkh_script_pubkey.address(), address_1)
        address_2 = 'mrAjisaT4LXL5MzE81sfcDYKU3wqWSvf9q'
        self.assertEqual(p2pkh_script_pubkey.address(testnet=True), address_2)
        address_3 = '3CLoMMyuoDQTPRD3XYZtCvgvkadrAdvdXh'
        h160 = decode_base58(address_3)
        p2sh_script_pubkey = p2sh_script(h160)
        self.assertEqual(p2sh_script_pubkey.address(), address_3)
        address_4 = '2N3u1R6uwQfuobCqbCgBkpsgBxvr1tZpe7B'
        self.assertEqual(p2sh_script_pubkey.address(testnet=True), address_4)
