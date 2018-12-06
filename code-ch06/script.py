from io import BytesIO
from logging import getLogger
from unittest import TestCase

from helper import (
    encode_varint,
    int_to_little_endian,
    little_endian_to_int,
    read_varint,
)
from op import (
    OP_CODE_FUNCTIONS,
    OP_CODE_NAMES,
)


LOGGER = getLogger(__name__)


# tag::source1[]
class Script:

    def __init__(self, instructions=None):
        if instructions is None:
            self.instructions = []
        else:
            self.instructions = instructions  # <1>
    # end::source1[]

    def __repr__(self):
        result = ''
        for instruction in self.instructions:
            if type(instruction) == int:
                if OP_CODE_NAMES.get(instruction):
                    name = OP_CODE_NAMES.get(instruction)
                else:
                    name = 'OP_[{}]'.format(instruction)
                result += '{} '.format(name)
            else:
                result += '{} '.format(instruction.hex())
        return result

    # tag::source4[]
    def __add__(self, other):
        return Script(self.instructions + other.instructions)  # <1>
    # end::source4[]

    # tag::source2[]
    @classmethod
    def parse(cls, s):
        length = read_varint(s)  # <2>
        instructions = []
        count = 0
        while count < length:  # <3>
            current = s.read(1)  # <4>
            count += 1
            current_byte = current[0]  # <5>
            if current_byte >= 1 and current_byte <= 75:  # <6>
                n = current_byte
                instructions.append(s.read(n))
                count += n
            elif current_byte == 76:  # <7>
                data_length = little_endian_to_int(s.read(1))
                instructions.append(s.read(data_length))
                count += data_length + 1
            elif current_byte == 77:  # <8>
                data_length = little_endian_to_int(s.read(2))
                instructions.append(s.read(data_length))
                count += data_length + 2
            else:  # <9>
                op_code = current_byte
                instructions.append(op_code)
        if count != length:  # <10>
            raise SyntaxError('parsing script failed')
        return cls(instructions)
    # end::source2[]

    # tag::source3[]
    def raw_serialize(self):
        result = b''
        for instruction in self.instructions:
            if type(instruction) == int:  # <1>
                result += int_to_little_endian(instruction, 1)
            else:
                length = len(instruction)
                if length < 75:  # <2>
                    result += int_to_little_endian(length, 1)
                elif length > 75 and length < 0x100:  # <3>
                    result += int_to_little_endian(76, 1)
                    result += int_to_little_endian(length, 1)
                elif length >= 0x100 and length <= 520:  # <4>
                    result += int_to_little_endian(77, 1)
                    result += int_to_little_endian(length, 2)
                else:  # <5>
                    raise ValueError('too long an instruction')
                result += instruction
        return result

    def serialize(self):
        result = self.raw_serialize()
        total = len(result)
        return encode_varint(total) + result  # <6>
    # end::source3[]

    # tag::source5[]
    def evaluate(self, z):
        instructions = self.instructions[:]  # <1>
        stack = []
        altstack = []
        while len(instructions) > 0:  # <2>
            instruction = instructions.pop(0)
            if type(instruction) == int:
                operation = OP_CODE_FUNCTIONS[instruction]  # <3>
                if instruction in (99, 100):  # <4>
                    if not operation(stack, instructions):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[instruction]))
                        return False
                elif instruction in (107, 108):  # <5>
                    if not operation(stack, altstack):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[instruction]))
                        return False
                elif instruction in (172, 173, 174, 175):  # <6>
                    if not operation(stack, z):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[instruction]))
                        return False
                else:
                    if not operation(stack):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[instruction]))
                        return False
            else:
                stack.append(instruction)  # <7>
        if len(stack) == 0:
            return False  # <8>
        if stack.pop() == b'':
            return False  # <9>
        return True  # <10>
    # end::source5[]

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
