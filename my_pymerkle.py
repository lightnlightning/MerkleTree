#!/usr/bin/python3
import hashlib

class Node:
    def __init__(self,value=None):
        self.Value = value
        self.left = None
        self.right = None

class MerkleTree:
    def __init__(self):
        self.root = None
        self.queue = [] #用来存放正在操作的三个树节点，分别是root,left和right
        self.create_queue = [] #用来存放先序序列来创建二叉树

    def hash_calculate(self,value):
        return hashlib.sha256(value).digest()

    def build_tree(self,list_data):
        for i in list_data :
            new_node = Node(self.hash_calculate(i.encode('utf-8')))
            self.queue.append(new_node)
        while self.root == None :
            if len(self.queue) == 1:
                self.root = self.queue.pop(0)
                break
            self.create_queue = []
            while self.queue:
                node_left = self.queue.pop(0)
                if self.queue:
                    node_right = self.queue.pop(0)
                    value_parent = self.hash_calculate(node_left.Value + node_right.Value)
                else:
                    node_right = None
                    value_parent = node_left.Value
                node_parent = Node(value_parent)
                node_parent.left = node_left
                node_parent.right = node_right
                self.create_queue.append(node_parent)
            self.queue = self.create_queue
        return self.root

if __name__ == '__main__':
    print("hello,MerkleTreeNode")
    m = MerkleTree()
    #  list_data = [
    #  "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4", 
    #  "0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2",
    #  "0x4B20993Bc481177ec7E8f571ceCaE8A9e22C02db",
    #  "0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB"
    #  ]
    list_data = ['a','b','c','d','e'] 
    print(m.build_tree( list_data ).Value.hex())
