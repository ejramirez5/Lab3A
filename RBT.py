#Zybooks implementation of Red-Black Trees class along with corresponding Node class

# RBTNode class - represents a node in a red-black tree
class RBTNode:
    def __init__(self, key, parent, embedding, is_red = False, left = None, right = None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent
        self.embedding = embedding
        
        if is_red:
            self.color = "red"
        else:
            self.color = "black"

    # Returns true if both child nodes are black. A child set to None is considered
    # to be black.
    def are_both_children_black(self):
        if self.left != None and self.left.is_red():
            return False
        if self.right != None and self.right.is_red():
            return False
        return True

    def count(self):
        count = 1
        if self.left != None:
            count = count + self.left.count()
        if self.right != None:
            count = count + self.right.count()
        return count
    
    # Returns the grandparent of this node
    def get_grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    # Gets this node's predecessor from the left child subtree
    # Precondition: This node's left child is not None
    def get_predecessor(self):
        node = self.left
        while node.right is not None:
            node = node.right
        return node

    # Returns this node's sibling, or None if this node does not have a sibling
    def get_sibling(self):
        if self.parent is not None:
            if self is self.parent.left:
                return self.parent.right
            return self.parent.left
        return None

    # Returns the uncle of this node
    def get_uncle(self):
        grandparent = self.get_grandparent()
        if grandparent is None:
            return None
        if grandparent.left is self.parent:
            return grandparent.right
        return grandparent.left

    # Returns True if this node is black, False otherwise
    def is_black(self):
        return self.color == "black"

    # Returns True if this node is red, False otherwise
    def is_red(self):
        return self.color == "red"

    # Replaces one of this node's children with a new child
    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)
        return False

    # Sets either the left or right child of this node
    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False
            
        if which_child == "left":
            self.left = child
        else:
            self.right = child

        if child != None:
            child.parent = self

        return True


class RedBlackTree:
    def __init__(self):
        self.root = None
    
    def __len__(self):
        if self.root is None:
            return 0
        return self.root.count()
    
    def insert(self, key, embedding):
        new_node = RBTNode(key, None, embedding, True, None, None)
        self.insert_node(new_node)
        
    def insert_node(self, node):
        # Begin with normal BST insertion
        if self.root is None:
            # Special case for root
            self.root = node
        else:
            current_node = self.root
            while current_node is not None:
                if node.key < current_node.key:
                    if current_node.left is None:
                        current_node.set_child("left", node)
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.set_child("right", node)
                        break
                    else:
                        current_node = current_node.right
        
        # Color the node red
        node.color = "red"
            
        # Balance
        self.insertion_balance(node)

    def insertion_balance(self, node):
        # If node is the tree's root, then color node black and return
        if node.parent is None:
            node.color = "black"
            return
        
        # If parent is black, then return without any alterations
        if node.parent.is_black():
            return
    
        # References to parent, grandparent, and uncle are needed for remaining operations
        parent = node.parent
        grandparent = node.get_grandparent()
        uncle = node.get_uncle()
        
        # If parent and uncle are both red, then color parent and uncle black, color grandparent
        # red, recursively balance  grandparent, then return
        if uncle is not None and uncle.is_red():
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.insertion_balance(grandparent)
            return

        # If node is parent's right child and parent is grandparent's left child, then rotate left
        # at parent, update node and parent to point to parent and grandparent, respectively
        if node is parent.right and parent is grandparent.left:
            self.rotate_left(parent)
            node = parent
            parent = node.parent
        # Else if node is parent's left child and parent is grandparent's right child, then rotate
        # right at parent, update node and parent to point to parent and grandparent, respectively
        elif node is parent.left and parent is grandparent.right:
            self.rotate_right(parent)
            node = parent
            parent = node.parent

        # Color parent black and grandparent red
        parent.color = "black"
        grandparent.color = "red"
                
        # If node is parent's left child, then rotate right at grandparent, otherwise rotate left
        # at grandparent
        if node is parent.left:
            self.rotate_right(grandparent)
        else:
            self.rotate_left(grandparent)

    def rotate_left(self, node):
        right_left_child = node.right.left
        if node.parent != None:
            node.parent.replace_child(node, node.right)
        else: # node is root
            self.root = node.right
            self.root.parent = None
        node.right.set_child("left", node)
        node.set_child("right", right_left_child)

    def rotate_right(self, node):
        left_right_child = node.left.right
        if node.parent != None:
            node.parent.replace_child(node, node.left)
        else: # node is root
            self.root = node.left
            self.root.parent = None
        node.left.set_child("right", node)
        node.set_child("left", left_right_child)

    def search(self, key):
        current_node = self.root
        while current_node is not None:
            # Return the node if the key matches.
            if current_node.key == key:
                return current_node
        
            # Navigate to the left if the search key is
            # less than the node's key.
            elif key < current_node.key:
                current_node = current_node.left

            # Navigate to the right if the search key is
            # greater than the node's key.
            else:
                current_node = current_node.right  

