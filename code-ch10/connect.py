from io import BytesIO

import asyncio

from network import NetworkEnvelope, NETWORK_MAGIC
from helper import (
    double_sha256,
    int_to_little_endian,
    little_endian_to_int,
)

VERSION = bytes.fromhex('f9beb4d976657273696f6e0000000000650000005f1a69d2721101000100000000000000bc8f5e5400000000010000000000000000000000000000000000ffffc61b6409208d010000000000000000000000000000000000ffffcb0071c0208d128035cbc97953f80f2f5361746f7368693a302e392e332fcf05050001')
VERACK = bytes.fromhex('f9beb4d976657261636b000000000000000000005df6e0e2')

class NodeConnection:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.q = asyncio.Queue()
    
    async def connect(self, loop):
        self.reader, self.writer = await asyncio.open_connection(
            host=self.host, port=self.port)
        print('connected')
        self.send(VERSION)
        print('sent version')
        await asyncio.wait([self.receive(), self.process_queue()])

    def send(self, msg):
        self.writer.write(msg)

    async def receive(self):
        print("start receiving")
        while True:
            magic = await self.reader.read(4)
            if magic != NETWORK_MAGIC:
                raise RuntimeError('Network Magic not at beginning of stream')
            command = await self.reader.read(12)
            payload_length = little_endian_to_int(await self.reader.read(4))
            checksum = await self.reader.read(4)
            payload = await self.reader.read(payload_length)
            # check the checksum
            if double_sha256(payload)[:4] != checksum:
                raise RuntimeError('Payload and Checksum do not match')
            await self.q.put(NetworkEnvelope(command, payload))

    async def process_queue(self):
        print("start processing")
        while True:
            envelope = await self.q.get()
            if envelope.command.startswith(b'version'):
                print('sending verack')
                self.send(VERACK)
            else:
                print(envelope)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    node = NodeConnection(host='35.187.200.6', port=8333)
    task = loop.run_until_complete(node.connect(loop))
    loop.close()
