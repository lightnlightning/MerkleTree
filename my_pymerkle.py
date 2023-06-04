#!/usr/bin/python3
import hashlib

class Node:
    def __init__(self,value=None):
        self.Value = value
        self.parent = None
        self.left = None
        self.right = None
    #  def __repr__(self):
    #      return repr((self.Value, self.parent, self.left,self.right))
    
class MerkleTree:
    def __init__(self):
        self.root = None
        self.queue = []
        self.create_queue = []

    def hash_calculate(self,value):
        return hashlib.sha256(value).digest()

    def show_tree(self,root):
        if not root:
            return 
        self.show_tree(root.left)
        print(root.Value.hex())
        self.show_tree(root.right)

    def get_leaves(self,root):
        leaves_list = []
        def inner(root):
            if not root:
                return 
            inner(root.left)
            inner(root.right)
            if root.left == None and root.right == None:
                leaves_list.append(root)
        inner(root)
        return leaves_list

    def get_proof(self,root=None,string_find=None):
        proof_list = []
        cursor_node = None
        string_hash = self.hash_calculate(string_find.encode('utf-8'))
        leaves_list = self.get_leaves(root)
        for i in leaves_list:
            if i.Value == string_hash:
                cursor_node = i
                break
        if not cursor_node:
            return False
        while cursor_node.parent:
            if cursor_node.parent.left and cursor_node.parent.right:
                if cursor_node.parent.left.Value == cursor_node.Value:
                    proof_list.append(cursor_node.parent.right.Value.hex())
                else:
                    proof_list.append(cursor_node.parent.left.Value.hex())
            cursor_node = cursor_node.parent
        return proof_list
        
    def build_tree(self,list_data,sort_leaves=False, sort_pairs=False):
        for i in list_data :
            new_node = Node(self.hash_calculate(i.encode('utf-8')))
            self.queue.append(new_node)
        if sort_leaves:
            self.queue = sorted(self.queue, key=lambda mt: mt.Value)
        while self.root == None :
            if len(self.queue) == 1:
                self.root = self.queue.pop(0)
                break
            self.create_queue = []
            while self.queue:
                node_left = self.queue.pop(0)
                if self.queue:
                    node_right = self.queue.pop(0)
                    if sort_pairs:
                        if node_left.Value > node_right.Value:
                            temp = node_left
                            node_left = node_right
                            node_right = temp
                    value_parent = self.hash_calculate(node_left.Value + node_right.Value)
                else:
                    node_right = None
                    value_parent = node_left.Value
                node_parent = Node(value_parent)
                node_parent.left = node_left
                node_parent.right = node_right
                node_left.parent = node_parent
                if node_right:
                    node_right.parent = node_parent
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
    tree_root = m.build_tree( list_data,sort_leaves=False,sort_pairs=True)
    #  print(tree_root.Value.hex())
    #  m.show_tree(tree_root)
    print('---------leaves-----------')
    list_leaves = m.get_leaves(tree_root)
    for i in list_leaves:
        print(i.Value.hex())
    print('---------proof-----------')
    proof_list = m.get_proof(tree_root,'e')
    for i in proof_list:
        print(i)


#  def main():
#      print("hello,MerkleTreeNode")
#      m = MerkleTree()
#      #  list_data = [
#      #  "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4", 
#      #  "0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2",
#      #  "0x4B20993Bc481177ec7E8f571ceCaE8A9e22C02db",
#      #  "0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB"
#      #  ]
#      list_data = ['a','b','c','d','e'] 
#      tree_root = m.build_tree( list_data,sort_leaves=True)
#      print(tree_root.Value.hex())
#      #  m.show_tree(tree_root)

