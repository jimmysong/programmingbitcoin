import math

from unittest import TestCase

import helper
import merkleblock

from block import Block
from helper import (
    bytes_to_bit_field,
    hash256,
    little_endian_to_int,
    read_varint,
)
from merkleblock import (
    MerkleBlock,
    MerkleTree,
)


def merkle_parent(hash1, hash2):
    return hash256(hash1 + hash2)


def merkle_parent_level(hashes):
    if len(hashes) == 1:
        raise RuntimeError('Cannot take a parent level with only 1 item')
    if len(hashes) % 2 == 1:
        hashes.append(hashes[-1])
    parent_level = []
    for i in range(0, len(hashes), 2):
        parent = merkle_parent(hashes[i], hashes[i + 1])
        parent_level.append(parent)
    return parent_level


def merkle_root(hashes):
    current_level = hashes
    while len(current_level) > 1:
        current_level = merkle_parent_level(current_level)
    return current_level[0]


class Chapter11Test(TestCase):

    def test_apply(self):

        def validate_merkle_root(self):
            hashes = [h[::-1] for h in self.tx_hashes]
            root = merkle_root(hashes)
            return root[::-1] == self.merkle_root

        @classmethod
        def parse(cls, s):
            version = little_endian_to_int(s.read(4))
            prev_block = s.read(32)[::-1]
            merkle_root = s.read(32)[::-1]
            timestamp = little_endian_to_int(s.read(4))
            bits = s.read(4)
            nonce = s.read(4)
            total = little_endian_to_int(s.read(4))
            num_txs = read_varint(s)
            hashes = []
            for _ in range(num_txs):
                hashes.append(s.read(32)[::-1])
            flags_length = read_varint(s)
            flags = s.read(flags_length)
            return cls(version, prev_block, merkle_root, timestamp, bits,
                       nonce, total, hashes, flags)

        def is_valid(self):
            flag_bits = bytes_to_bit_field(self.flags)
            hashes = [h[::-1] for h in self.hashes]
            merkle_tree = MerkleTree(self.total)
            merkle_tree.populate_tree(flag_bits, hashes)
            return merkle_tree.root()[::-1] == self.merkle_root

        helper.merkle_parent = merkle_parent
        merkleblock.merkle_parent = merkle_parent
        helper.merkle_parent_level = merkle_parent_level
        helper.merkle_root = merkle_root
        Block.validate_merkle_root = validate_merkle_root
        MerkleBlock.parse = parse
        MerkleBlock.is_valid = is_valid

    def test_example_1(self):
        hash0 = bytes.fromhex('c117ea8ec828342f4dfb0ad6bd140e03a50720ece40169ee38bdc15d9eb64cf5')
        hash1 = bytes.fromhex('c131474164b412e3406696da1ee20ab0fc9bf41c8f05fa8ceea7a08d672d7cc5')
        parent = hash256(hash0 + hash1)
        self.assertEqual(parent.hex(), '8b30c5ba100f6f2e5ad1e2a742e5020491240f8eb514fe97c713c31718ad7ecd')

    def test_example_2(self):
        hex_hashes = [
            'c117ea8ec828342f4dfb0ad6bd140e03a50720ece40169ee38bdc15d9eb64cf5',
            'c131474164b412e3406696da1ee20ab0fc9bf41c8f05fa8ceea7a08d672d7cc5',
            'f391da6ecfeed1814efae39e7fcb3838ae0b02c02ae7d0a5848a66947c0727b0',
            '3d238a92a94532b946c90e19c49351c763696cff3db400485b813aecb8a13181',
            '10092f2633be5f3ce349bf9ddbde36caa3dd10dfa0ec8106bce23acbff637dae',
        ]
        hashes = [bytes.fromhex(x) for x in hex_hashes]
        if len(hashes) % 2 == 1:
            hashes.append(hashes[-1])
        parent_level = []
        for i in range(0, len(hex_hashes), 2):
            parent = merkle_parent(hashes[i], hashes[i + 1])
            parent_level.append(parent)
        want = [
            '8b30c5ba100f6f2e5ad1e2a742e5020491240f8eb514fe97c713c31718ad7ecd',
            '7f4e6f9e224e20fda0ae4c44114237f97cd35aca38d83081c9bfd41feb907800',
            '3ecf6115380c77e8aae56660f5634982ee897351ba906a6837d15ebc3a225df0',
        ]
        self.assertEqual([x.hex() for x in parent_level], want)

    def test_example_3(self):
        hex_hashes = [
            'c117ea8ec828342f4dfb0ad6bd140e03a50720ece40169ee38bdc15d9eb64cf5',
            'c131474164b412e3406696da1ee20ab0fc9bf41c8f05fa8ceea7a08d672d7cc5',
            'f391da6ecfeed1814efae39e7fcb3838ae0b02c02ae7d0a5848a66947c0727b0',
            '3d238a92a94532b946c90e19c49351c763696cff3db400485b813aecb8a13181',
            '10092f2633be5f3ce349bf9ddbde36caa3dd10dfa0ec8106bce23acbff637dae',
            '7d37b3d54fa6a64869084bfd2e831309118b9e833610e6228adacdbd1b4ba161',
            '8118a77e542892fe15ae3fc771a4abfd2f5d5d5997544c3487ac36b5c85170fc',
            'dff6879848c2c9b62fe652720b8df5272093acfaa45a43cdb3696fe2466a3877',
            'b825c0745f46ac58f7d3759e6dc535a1fec7820377f24d4c2c6ad2cc55c0cb59',
            '95513952a04bd8992721e9b7e2937f1c04ba31e0469fbe615a78197f68f52b7c',
            '2e6d722e5e4dbdf2447ddecc9f7dabb8e299bae921c99ad5b0184cd9eb8e5908',
            'b13a750047bc0bdceb2473e5fe488c2596d7a7124b4e716fdd29b046ef99bbf0',
        ]
        hashes = [bytes.fromhex(x) for x in hex_hashes]
        current_level = hashes
        while len(current_level) > 1:
            current_level = merkle_parent_level(current_level)
        self.assertEqual(current_level[0].hex(), 'acbcab8bcc1af95d8d563b77d24c3d19b18f1486383d75a5085c4e86c86beed6')

    def test_example_4(self):
        tx_hex_hashes = [
            '42f6f52f17620653dcc909e58bb352e0bd4bd1381e2955d19c00959a22122b2e',
            '94c3af34b9667bf787e1c6a0a009201589755d01d02fe2877cc69b929d2418d4',
            '959428d7c48113cb9149d0566bde3d46e98cf028053c522b8fa8f735241aa953',
            'a9f27b99d5d108dede755710d4a1ffa2c74af70b4ca71726fa57d68454e609a2',
            '62af110031e29de1efcad103b3ad4bec7bdcf6cb9c9f4afdd586981795516577',
            '766900590ece194667e9da2984018057512887110bf54fe0aa800157aec796ba',
            'e8270fb475763bc8d855cfe45ed98060988c1bdcad2ffc8364f783c98999a208',
        ]
        tx_hashes = [bytes.fromhex(x) for x in tx_hex_hashes]
        hashes = [h[::-1] for h in tx_hashes]
        self.assertEqual(
            merkle_root(hashes)[::-1].hex(),
            '654d6181e18e4ac4368383fdc5eead11bf138f9b7ac1e15334e4411b3c4797d9')

    def test_exercise_5(self):
        total = 27
        max_depth = math.ceil(math.log(total, 2))
        merkle_tree = []
        for depth in range(max_depth + 1):
            num_items = math.ceil(total / 2**(max_depth - depth))
            level_hashes = [None] * num_items
            merkle_tree.append(level_hashes)
        expected = [1, 2, 4, 7, 14, 27]
        for want, level in zip(expected, merkle_tree):
            self.assertEqual(level, [None] * want)

    def test_example_5(self):
        hex_hashes = [
            "9745f7173ef14ee4155722d1cbf13304339fd00d900b759c6f9d58579b5765fb",
            "5573c8ede34936c29cdfdfe743f7f5fdfbd4f54ba0705259e62f39917065cb9b",
            "82a02ecbb6623b4274dfcab82b336dc017a27136e08521091e443e62582e8f05",
            "507ccae5ed9b340363a0e6d765af148be9cb1c8766ccc922f83e4ae681658308",
            "a7a4aec28e7162e1e9ef33dfa30f0bc0526e6cf4b11a576f6c5de58593898330",
            "bb6267664bd833fd9fc82582853ab144fece26b7a8a5bf328f8a059445b59add",
            "ea6d7ac1ee77fbacee58fc717b990c4fcccf1b19af43103c090f601677fd8836",
            "457743861de496c429912558a106b810b0507975a49773228aa788df40730d41",
            "7688029288efc9e9a0011c960a6ed9e5466581abf3e3a6c26ee317461add619a",
            "b1ae7f15836cb2286cdd4e2c37bf9bb7da0a2846d06867a429f654b2e7f383c9",
            "9b74f89fa3f93e71ff2c241f32945d877281a6a50a6bf94adac002980aafe5ab",
            "b3a92b5b255019bdaf754875633c2de9fec2ab03e6b8ce669d07cb5b18804638",
            "b5c0b915312b9bdaedd2b86aa2d0f8feffc73a2d37668fd9010179261e25e263",
            "c9d52c5cb1e557b92c84c52e7c4bfbce859408bedffc8a5560fd6e35e10b8800",
            "c555bc5fc3bc096df0a0c9532f07640bfb76bfe4fc1ace214b8b228a1297a4c2",
            "f9dbfafc3af3400954975da24eb325e326960a25b87fffe23eef3e7ed2fb610e",
        ]
        tree = MerkleTree(len(hex_hashes))
        tree.nodes[4] = [bytes.fromhex(h) for h in hex_hashes]
        tree.nodes[3] = merkle_parent_level(tree.nodes[4])
        tree.nodes[2] = merkle_parent_level(tree.nodes[3])
        tree.nodes[1] = merkle_parent_level(tree.nodes[2])
        tree.nodes[0] = merkle_parent_level(tree.nodes[1])
        self.assertEqual(tree.nodes[0][0].hex(), '597c4bafe3832b17cbbabe56f878f4fc2ad0f6a402cee7fa851a9cb205f87ed1')

    def test_example_6(self):
        hex_hashes = [
            "9745f7173ef14ee4155722d1cbf13304339fd00d900b759c6f9d58579b5765fb",
            "5573c8ede34936c29cdfdfe743f7f5fdfbd4f54ba0705259e62f39917065cb9b",
            "82a02ecbb6623b4274dfcab82b336dc017a27136e08521091e443e62582e8f05",
            "507ccae5ed9b340363a0e6d765af148be9cb1c8766ccc922f83e4ae681658308",
            "a7a4aec28e7162e1e9ef33dfa30f0bc0526e6cf4b11a576f6c5de58593898330",
            "bb6267664bd833fd9fc82582853ab144fece26b7a8a5bf328f8a059445b59add",
            "ea6d7ac1ee77fbacee58fc717b990c4fcccf1b19af43103c090f601677fd8836",
            "457743861de496c429912558a106b810b0507975a49773228aa788df40730d41",
            "7688029288efc9e9a0011c960a6ed9e5466581abf3e3a6c26ee317461add619a",
            "b1ae7f15836cb2286cdd4e2c37bf9bb7da0a2846d06867a429f654b2e7f383c9",
            "9b74f89fa3f93e71ff2c241f32945d877281a6a50a6bf94adac002980aafe5ab",
            "b3a92b5b255019bdaf754875633c2de9fec2ab03e6b8ce669d07cb5b18804638",
            "b5c0b915312b9bdaedd2b86aa2d0f8feffc73a2d37668fd9010179261e25e263",
            "c9d52c5cb1e557b92c84c52e7c4bfbce859408bedffc8a5560fd6e35e10b8800",
            "c555bc5fc3bc096df0a0c9532f07640bfb76bfe4fc1ace214b8b228a1297a4c2",
            "f9dbfafc3af3400954975da24eb325e326960a25b87fffe23eef3e7ed2fb610e",
        ]
        tree = MerkleTree(len(hex_hashes))
        tree.nodes[4] = [bytes.fromhex(h) for h in hex_hashes]
        while tree.root() is None:
            if tree.is_leaf():
                tree.up()
            else:
                left_hash = tree.get_left_node()
                right_hash = tree.get_right_node()
                if left_hash is None:
                    tree.left()
                elif right_hash is None:
                    tree.right()
                else:
                    tree.set_current_node(merkle_parent(left_hash, right_hash))
                    tree.up()
        self.assertEqual(tree.nodes[0][0].hex(), '597c4bafe3832b17cbbabe56f878f4fc2ad0f6a402cee7fa851a9cb205f87ed1')

    def test_example_7(self):
        hex_hashes = [
            "9745f7173ef14ee4155722d1cbf13304339fd00d900b759c6f9d58579b5765fb",
            "5573c8ede34936c29cdfdfe743f7f5fdfbd4f54ba0705259e62f39917065cb9b",
            "82a02ecbb6623b4274dfcab82b336dc017a27136e08521091e443e62582e8f05",
            "507ccae5ed9b340363a0e6d765af148be9cb1c8766ccc922f83e4ae681658308",
            "a7a4aec28e7162e1e9ef33dfa30f0bc0526e6cf4b11a576f6c5de58593898330",
            "bb6267664bd833fd9fc82582853ab144fece26b7a8a5bf328f8a059445b59add",
            "ea6d7ac1ee77fbacee58fc717b990c4fcccf1b19af43103c090f601677fd8836",
            "457743861de496c429912558a106b810b0507975a49773228aa788df40730d41",
            "7688029288efc9e9a0011c960a6ed9e5466581abf3e3a6c26ee317461add619a",
            "b1ae7f15836cb2286cdd4e2c37bf9bb7da0a2846d06867a429f654b2e7f383c9",
            "9b74f89fa3f93e71ff2c241f32945d877281a6a50a6bf94adac002980aafe5ab",
            "b3a92b5b255019bdaf754875633c2de9fec2ab03e6b8ce669d07cb5b18804638",
            "b5c0b915312b9bdaedd2b86aa2d0f8feffc73a2d37668fd9010179261e25e263",
            "c9d52c5cb1e557b92c84c52e7c4bfbce859408bedffc8a5560fd6e35e10b8800",
            "c555bc5fc3bc096df0a0c9532f07640bfb76bfe4fc1ace214b8b228a1297a4c2",
            "f9dbfafc3af3400954975da24eb325e326960a25b87fffe23eef3e7ed2fb610e",
            "38faf8c811988dff0a7e6080b1771c97bcc0801c64d9068cffb85e6e7aacaf51",
        ]
        tree = MerkleTree(len(hex_hashes))
        tree.nodes[5] = [bytes.fromhex(h) for h in hex_hashes]
        while tree.root() is None:
            if tree.is_leaf():
                tree.up()
            else:
                left_hash = tree.get_left_node()
                if left_hash is None:
                    tree.left()
                elif tree.right_exists():
                    right_hash = tree.get_right_node()
                    if right_hash is None:
                        tree.right()
                    else:
                        tree.set_current_node(merkle_parent(left_hash, right_hash))
                        tree.up()
                else:
                    tree.set_current_node(merkle_parent(left_hash, left_hash))
                    tree.up()
        self.assertEqual(tree.nodes[0][0].hex(), '0a313864f84b284ad13f7f93940d43459808c3c300ed274a90f265802ab10f91')
