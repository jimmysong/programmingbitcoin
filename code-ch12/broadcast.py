import time
from block import Block
from bloomfilter import BloomFilter
from ecc import PrivateKey
from helper import (
    decode_base58,
    encode_varint,
    hash256,
    little_endian_to_int,
    read_varint,
    SIGHASH_ALL,
)
from merkleblock import MerkleBlock
from network import (
    GetDataMessage,
    GetHeadersMessage,
    HeadersMessage,
    NetworkEnvelope,
    SimpleNode,
    TX_DATA_TYPE,
    FILTERED_BLOCK_DATA_TYPE,
)
from script import p2pkh_script, Script
from tx import Tx, TxIn, TxOut, TxFetcher

last_block_hex = '00000000000538d5c2246336644f9a4956551afb44ba47278759ec55ea912e19'

secret = little_endian_to_int(hash256(b''))
private_key = PrivateKey(secret=secret)
addr = private_key.point.address(testnet=True)
h160 = decode_base58(addr)

target_address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'
target_h160 = decode_base58(target_address)
target_script = p2pkh_script(target_h160)
fee = 5000  # fee in satoshis

# connect to tbtc.programmingblockchain.com in testnet mode
node = SimpleNode('tbtc.programmingblockchain.com', testnet=True, logging=True)

# create a bloom filter of size 30 and 5 functions. Add a tweak that you like
bf = BloomFilter(30, 5, 90210)
# add the h160 to the bloom filter
bf.add(h160)

# complete the handshake
node.handshake()
# load the bloom filter with the filterload command
node.send(bf.filterload())

# set start block to last_block from above
start_block = bytes.fromhex(last_block_hex)
# send a getheaders message with the starting block
getheaders = GetHeadersMessage(start_block=start_block)
node.send(getheaders)

# wait for the headers message
headers = node.wait_for(HeadersMessage)
# store the last block as None
last_block = None
# initialize the GetDataMessage
getdata = GetDataMessage()
# loop through the blocks in the headers
for b in headers.blocks:
    # check that the proof of work on the block is valid
    if not b.check_pow():
        raise RuntimeError('proof of work is invalid')
    # check that this block's prev_block is the last block
    if last_block is not None and b.prev_block != last_block:
        raise RuntimeError('chain broken')
    # add a new item to the get_data_message
    # should be FILTERED_BLOCK_DATA_TYPE and block hash
    get_data_message.add_data(FILTERED_BLOCK_DATA_TYPE, b.hash())
    # set the last block to the current hash
    last_block = b.hash()
# send the getdata message
node.send(getdata)

# initialize prev_tx and prev_index to None
prev_tx, prev_index = None, None
# loop while prev_tx is None 
while prev_tx is None:
    # wait for the merkleblock or tx commands
    message = node.wait_for(MerkleBlock, Tx)
    # if we have the merkleblock command
    if message.command == b'merkleblock':
        # check that the MerkleBlock is valid
        if not message.is_valid():
            raise RuntimeError('invalid merkle proof')
    # else we have the tx command
    else:
        # set the tx's testnet to be True
        message.testnet = True
        # loop through the tx outs
        for i, tx_out in enumerate(message.tx_outs):
            # if our output has the same address as our address we found it
            if tx_out.script_pubkey.address(testnet=True) == addr:
                # we found our utxo. set prev_tx, prev_index, and transaction
                prev_tx = message.hash()
                prev_index = i
                print('found: {}:{}'.format(prev_tx.hex(), prev_index))
# create the TxIn
tx_in = TxIn(prev_tx, prev_index)
# calculate the output amount (previous amount minus the fee)
output_amount = prev_amount - fee
# create a new TxOut to the target script with the output amount
tx_outs = TxOut(output_amount, target_script)
# create a new transaction with the one input and one output
tx_obj = Tx(1, [tx_in], [tx_out], 0, testnet=True)
# sign the only input of the transaction
tx_obj.sign_input(0, private_key)
# serialize and hex to see what it looks like
print(tx_obj.serialize().hex())
# send this signed transaction on the network
node.send(tx_obj)
# wait a sec so this message goes through with time.sleep(1)
time.sleep(1)
# now ask for this transaction from the other node
# create a GetDataMessage
getdata = GetDataMessage()
# ask for our transaction by adding it to the message
getdata.add_data(TX_DATA_TYPE, tx_obj.hash())
# send the message
node.send(getdata)
# now wait for a Tx response
received_tx = node.wait_for(Tx)
# if the received tx has the same id as our tx, we are done!
if received_tx.id() == tx_obj.id():
    print('success!')
