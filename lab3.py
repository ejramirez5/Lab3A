"""
CS 2302
Emilio Ramirez
Lab 3 A
Diego Aguirre,  Manoj Saha
Last Date Modified: Novemeber 4th, 2018
Purpose:  Use AVL and RedBlack trees to find the cosine distance between words( similarity) 
"""

import math
from AVL import Node 
from AVL import AVLTree
from RBT import RBTNode
from RBT import RedBlackTree
def Number_of_Nodes(Ctree):
    """
    This method while return the total number of nodes/ elements in the given tree be it a AVl or Red-Black Tree

    Parameters:
        Ctree: root of a tree
    Returns:
        integer that corresponds to the amount of nodes in the given tree
    """ 
    if Ctree is None:
        return 0
    left = Number_of_Nodes(Ctree.left)
    right = Number_of_Nodes(Ctree.right)
    return left + right +1

def Get_Height(Ctree):
    """ 
    This method returns the height for a given node in a tree If the initial Node is the root of a tree
    it will return the height of that tree.

    Parameters:
        Ctree: root/current node of a tree
    Returns:
        integer that corresponds to the height the given node/tree
    """
    if Ctree == None:
        return -1
    L = Get_Height(Ctree.left)
    R = Get_Height(Ctree.right)
    return max(L,R) + 1

def In_Order(Ctree, file):
    """
    This method fills a text file, that has already been opened, with all of the elements in a given tree in ascending order

    Parameters:
        Ctree: root/current node of a tree
        file: file that will be used to write the inforomation from the tree
    Returns:
        Nothing
    """
    if Ctree == None:
        return    
    In_Order(Ctree.left , file)
    file.write(Ctree.key +"\n")
    In_Order(Ctree.right , file)

def At_Depth(Ctree, file, k):
    """
    This method fills a text file, that has already been opened, with all of the elements found
     at depth k of a given tree; in ascending order

    Parameters:
        Ctree: root/current node of a tree
        file: file that will be used to write the information from the tree
        k: integer representing how much deeper must be traversed until reaching the desired level/depth
    Returns:
        Nothing
    """
    if Ctree == None:
        return
    if k != 0:
        At_Depth(Ctree.left, file, k-1)
        At_Depth(Ctree.right, file, k-1)
        return
    file.write(Ctree.key + "\n")
    return
    
def Similarity(filename, Tree):
    """
    This method opens a file with the given name. This file needs to structered in a particular way;
     where there are two words, seperated only by spaces, per line. It then looks for both of these words
     in the given tree. If both of the words are found then the cosine distance between them is solved for 
     and output.
    Parameters:
        filename: name of the file that contains the words that are to be compared
        Tree: root of a tree that contains plenty of words each with their corresponding embedding
    Returns:
        Nothing:
    """

    with open(filename, encoding ="utf8") as file:
        for line in file:
            values = line.split()
            # the two lines below first search for the words in the tree
            Word_1 = Tree.search(values[0])
            Word_2 = Tree.search(values[1])
            
            # if either of the words is not found then there is no need to compare 
            if Word_1 == None or Word_2 == None:
                print("One of the words was not found Similarity = 0")
                continue
            Word_1_Magnitude = 0
            Word_2_Magnitude = 0
            Dot_Product = 0
            
            # the following block of code follows the equation to find the cosine Distance 
            for i in range(len(Word_1.embedding)):
                Word_1_Magnitude += math.pow(float(Word_1.embedding[i]),2)
                Word_2_Magnitude += math.pow(float(Word_2.embedding[i]),2)
                Dot_Product += float(Word_1.embedding[i]) * float(Word_2.embedding[i])
            Word_1_Magnitude = math.sqrt(Word_1_Magnitude)
            Word_2_Magnitude = math.sqrt(Word_2_Magnitude)
            # cosine distance = Dot product/(magnitude of word 1 *magnitude of word 2)
            likeness = Dot_Product/((Word_1_Magnitude)*Word_2_Magnitude)
            
            print(Word_1.key + " and " + Word_2.key + " have a Simliarity of " + str(likeness))



def Get_Words(filename, Tree):
    """
    This method reads a file with the given name and creates a tree, avl or red-black, that will store all of the words
    found in the file that begin with a letter.

    Parameters:
        filename: name of the file that contains a word followed by 50 float point values( each seperated with a space)
                  in each of its lines
        Tree: root of a tree that will serve as the foundation of the dictionary that is to be formed from the words
                found in the given file
    Returns:
        Dictionary: The root of the now populated tree.
    """

    Dictionary = Tree
    with open(filename, encoding ="utf8")as file:
        if(isinstance(Tree, RedBlackTree)):
            for line in file:
                values = line.split()
                if values[0][0] < 'a' or values[0][0] > 'z':
                    continue
                name = values.pop(0)
                Dictionary.insert(name, values)
        else:
            for line in file:
                values = line.split()
                if values[0][0] < 'a' or values[0][0] > 'z':
                    continue
                name = values.pop(0)
                NodeC = Node(name, values)
                Dictionary.insert(NodeC)
        return Dictionary

def main():
    request = input("What kind of Binary Tree Would you like to use? (Enter either AVL or RedBlack) ")
    request = request.lower()
    if request == "avl" :
        Tree = AVLTree()
    else:
        Tree = RedBlackTree()
    Tree = Get_Words("glove.6B.50d.txt", Tree)

    print("There are " + str(Number_of_Nodes(Tree.root)) + " nodes in the tree.")

    print("The tree is of height " + str(Get_Height(Tree.root)))

    f = open("Words_Inorder.txt", "w+", encoding ="utf8")
    In_Order(Tree.root, f)
    f.close()

    f = open("Words_At_Depth", "w+", encoding = "utf8")
    Depth = int(input("Enter Desired Depth "))
    At_Depth(Tree.root,f ,Depth)
    
    Similarity("twofour.txt", Tree)
main()
