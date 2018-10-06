import math

from io import BytesIO
from unittest import TestCase

from helper import (
    bytes_to_bit_field,
    little_endian_to_int,
    merkle_parent,
    read_varint,
)


class MerkleTree:

    def __init__(self, total):
        self.total = total
        # compute max depth math.ceil(math.log(self.total, 2))
        self.max_depth = math.ceil(math.log(self.total, 2))
        # initialize the nodes property to hold the actual tree
        self.nodes = []
        # loop over the number of levels (max_depth+1)
        for depth in range(self.max_depth + 1):
            # the number of items at this depth is
            # math.ceil(self.total / 2**(self.max_depth - depth))
            num_items = math.ceil(self.total / 2**(self.max_depth - depth))
            # create this level's hashes list with the right number of items
            level_hashes = [None] * num_items
            # append this level's hashes to the merkle tree
            self.nodes.append(level_hashes)
        # set the pointer to the root (depth=0, index=0)
        self.current_depth = 0
        self.current_index = 0

    def __repr__(self):
        result = ''
        for depth, level in enumerate(self.nodes):
            for index, h in enumerate(level):
                short = '{}...'.format(h.hex()[:8])
                if depth == self.current_depth and index == self.current_index:
                    result += '*{}*, '.format(short[:-2])
                else:
                    result += '{}, '.format(short)
            result += '\n'
        return result

    def up(self):
        # reduce depth by 1 and halve the index
        self.current_depth -= 1
        self.current_index //= 2

    def left(self):
        # increase depth by 1 and double the index
        self.current_depth += 1
        self.current_index *= 2

    def right(self):
        # increase depth by 1 and double the index + 1
        self.current_depth += 1
        self.current_index = self.current_index * 2 + 1

    def root(self):
        return self.nodes[0][0]

    def set_current_node(self, value):
        self.nodes[self.current_depth][self.current_index] = value

    def get_current_node(self):
        return self.nodes[self.current_depth][self.current_index]

    def get_left_node(self):
        return self.nodes[self.current_depth + 1][self.current_index * 2]

    def get_right_node(self):
        return self.nodes[self.current_depth + 1][self.current_index * 2 + 1]

    def is_leaf(self):
        return self.current_depth == self.max_depth

    def right_exists(self):
        return len(self.nodes[self.current_depth + 1]) > self.current_index * 2 + 1

    def populate_tree(self, flag_bits, hashes):
        # populate until we have the root
        while self.root() is None:
            # if we are a leaf, we know this position's hash
            if self.is_leaf():
                # get the next bit from flag_bits: flag_bits.pop(0)
                flag_bits.pop(0)
                # set the current node in the merkle tree to the next hash: hashes.pop(0)
                self.set_current_node(hashes.pop(0))
                # go up a level
                self.up()
            # else
            else:
                # get the left hash
                left_hash = self.get_left_node()
                # Exercise 6.2: get the right hash
                # if we don't have the left hash
                if left_hash is None:
                    # if the next flag bit is 0, the next hash is our current node
                    if flag_bits.pop(0) == 0:
                        # set the current node to be the next hash
                        self.set_current_node(hashes.pop(0))
                        # sub-tree doesn't need calculation, go up
                        self.up()
                    # else
                    else:
                        # go to the left node
                        self.left()
                # Exercise 6.2: if we don't have the right hash
                    # go to the right node
                # Exercise 6.2: else
                    # combine the left and right hashes
                    # we've completed this subtree, go up
                # Exercise 7.2: if the right hash exists
                elif self.right_exists():
                    # get the right hash
                    right_hash = self.get_right_node()
                    # if we don't have the right hash
                    if right_hash is None:
                        # go to the right node
                        self.right()
                    # else
                    else:
                        # combine the left and right hashes
                        self.set_current_node(merkle_parent(left_hash, right_hash))
                        # we've completed this sub-tree, go up
                        self.up()
                # else
                else:
                    # combine the left hash twice
                    self.set_current_node(merkle_parent(left_hash, left_hash))
                    # we've completed this sub-tree, go up
                    self.up()
        if len(hashes) != 0:
            raise RuntimeError('hashes not all consumed {}'.format(len(hashes)))
        for flag_bit in flag_bits:
            if flag_bit != 0:
                raise RuntimeError('flag bits not all consumed')


class MerkleTreeTest(TestCase):

    def test_init(self):
        tree = MerkleTree(9)
        self.assertEqual(len(tree.nodes[0]), 1)
        self.assertEqual(len(tree.nodes[1]), 2)
        self.assertEqual(len(tree.nodes[2]), 3)
        self.assertEqual(len(tree.nodes[3]), 5)
        self.assertEqual(len(tree.nodes[4]), 9)

    def test_populate_tree_1(self):
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
        hashes = [bytes.fromhex(h) for h in hex_hashes]
        tree.populate_tree([1] * 31, hashes)
        root = '597c4bafe3832b17cbbabe56f878f4fc2ad0f6a402cee7fa851a9cb205f87ed1'
        self.assertEqual(tree.root().hex(), root)

    def test_populate_tree_2(self):
        hex_hashes = [
            '42f6f52f17620653dcc909e58bb352e0bd4bd1381e2955d19c00959a22122b2e',
            '94c3af34b9667bf787e1c6a0a009201589755d01d02fe2877cc69b929d2418d4',
            '959428d7c48113cb9149d0566bde3d46e98cf028053c522b8fa8f735241aa953',
            'a9f27b99d5d108dede755710d4a1ffa2c74af70b4ca71726fa57d68454e609a2',
            '62af110031e29de1efcad103b3ad4bec7bdcf6cb9c9f4afdd586981795516577',
        ]
        tree = MerkleTree(len(hex_hashes))
        hashes = [bytes.fromhex(h) for h in hex_hashes]
        tree.populate_tree([1] * 11, hashes)
        root = 'a8e8bd023169b81bc56854137a135b97ef47a6a7237f4c6e037baed16285a5ab'
        self.assertEqual(tree.root().hex(), root)
