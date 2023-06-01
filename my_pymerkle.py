#!/usr/bin/python3
import hashlib

class MerkleTreeNode:
    leaves = []
    def __init__(self):
        self.left = None
        self.right = None
        self.hashValue = None
        #  self.hashValue = hashlib.sha256(value.encode('utf-8')).hexdigest()
        #  MerkleTreeNode.leaves.append(hashlib.sha256(value.encode('utf-8')).hexdigest())

    def get_leaves(self):
        return MerkleTreeNode.leaves

if __name__ == '__main__':
    print("hello,MerkleTreeNode")
    m = MerkleTreeNode()
    print(m.get_leaves())
