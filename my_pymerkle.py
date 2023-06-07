#!/usr/bin/python3
import hashlib
from web3 import Web3

class Node:
    def __init__(self,value=None):
        self.Value = value
        self.parent = None
        self.left = None
        self.right = None
     # def __repr__(self):
         # return repr((self.Value, self.parent, self.left,self.right))
    
class MerkleTree:
    def __init__(self,method='keccak'):
        self.root = None
        self.queue = []
        self.create_queue = []
        self.hash_method = method

    def hash_calculate(self,hexstring=None,string=None):
        if bool(hexstring) ^ bool(string):
            match self.hash_method:
                case 'sha256':
                    if hexstring:
                        if hexstring[:2] == '0x':
                            return hashlib.sha256(bytes.fromhex(hexstring[2:])).hexdigest()
                        else:
                            return hashlib.sha256(bytes.fromhex(hexstring)).hexdigest()
                    else:
                        return hashlib.sha256(string.encode('utf-8')).hexdigest()
                case 'keccak':
                    if hexstring:
                        return Web3.keccak(hexstr=hexstring).hex()[2:]
                    else:
                        return Web3.keccak(text=string).hex()[2:]
                case _:
                    return False
        else:
            return False
                
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

    def get_proof(self,root=None,string_find=None,ishex=False):
        proof_list = []
        cursor_node = None
        if ishex:
            string_hash = self.hash_calculate(hexstring=string_find)
        else:
            string_hash = self.hash_calculate(string=string_find)
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
                    proof_list.append(cursor_node.parent.right.Value)
                else:
                    proof_list.append(cursor_node.parent.left.Value)
            cursor_node = cursor_node.parent
        return proof_list
        
    def verify_proof(self, root, proof, leaf, ishex=False):
        # cursor_hash = self.hash_calculate(string=leaf)
        if ishex:
            cursor_hash = self.hash_calculate(hexstring=leaf)
        else:
            cursor_hash = self.hash_calculate(string=leaf)
        for i_hash in proof:
            if cursor_hash < i_hash:
                cursor_hash = self.hash_calculate(hexstring=(cursor_hash + i_hash)) 
            else:
                cursor_hash = self.hash_calculate(hexstring=(i_hash + cursor_hash))
        if cursor_hash == root.Value:
            return True
        else:
            return False

    def build_tree(self,list_data,sort_leaves=False,ishex=False):
        if ishex:
            for i_str in list_data :
                new_node = Node(self.hash_calculate(hexstring=i_str))
                self.queue.append(new_node)
        else:
            for i_str in list_data :
                new_node = Node(self.hash_calculate(string=i_str))
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
                    if node_left.Value > node_right.Value:
                        value_parent = self.hash_calculate(hexstring=(node_right.Value + node_left.Value))
                    else:
                        value_parent = self.hash_calculate(hexstring=(node_left.Value + node_right.Value))
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
    m = MerkleTree('sha256')
    list_data = [
         "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4", 
         "0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2",
         "0x4B20993Bc481177ec7E8f571ceCaE8A9e22C02db",
         "0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB"
         ]
    # list_data = ['a','b','c','d','e'] 
    tree_root = m.build_tree(list_data,sort_leaves=True,ishex=False)
    print('---------root-----------')
    print(tree_root.Value)
    #  m.show_tree(tree_root)
    print('---------leaves-----------')
    list_leaves = m.get_leaves(tree_root)
    for i in list_leaves:
        print(i.Value)
    print('---------proof-----------')
    print('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2')
    proof_list = m.get_proof(tree_root,'0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2',ishex=False)
    print(proof_list)
    print('---------verify-----------')
    print('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2')
    print(m.verify_proof(tree_root,proof_list,'0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2',ishex=False))
    assert m.verify_proof(tree_root,proof_list,'0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2',ishex=False) == True

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
