from typing import Any


class Node:
    def __init__(self, value: str):
        self.value = value
        self.left: None | Node = None
        self.right: None | Node = None

    def add_value(self, value: str, children: list[Any]) -> bool:

        if self.left == None:
            node = Node(value)
            children.append(node)
            self.left = node
            return True

        elif self.right == None:
            node = Node(value)
            children.append(node)
            self.right = node
            return True

        else:
            return False
        

    def get_children(self) -> tuple[Any, Any]:
        return self.left, self.right
    
    def set_children(self, children: tuple[Any, Any]):
        self.left = children[0]
        self.right = children[1]
        
        
    def __str__(self):
        return f'value: {self.value}, left: {self.left.value if type(self.left) is Node else None}, right: {self.right.value if type(self.right) is Node else None}'





def construct_tree(data: str) -> Node:
    #the root node is set as the first value in the array data
    top_node = Node(data[0])
    #the program then finds the childeren of the top node
    children: list[Node] = [top_node]
    #a loop that fetches the data from the data array begins 
    for char in data[1:]:
        full_children: list[Node] = []
        for child in children:
            if child.add_value(char, children):
                break
            else:
                full_children.append(child)

        for child in full_children:
            children.remove(child)

    return top_node

def tree_to_string(first_node: Node) -> str:

    chars = [first_node.value]
    nodes: list[Node | None] = [first_node.left, first_node.right]
    children: list[Node | None] = []

    while nodes != []:
        for node in nodes:
            if node != None:
                chars.append(node.value)
                children.append(node.left)
                children.append(node.right)

        nodes = children
        children = []

    return ''.join(chars)
    
    
def swap_nodes(node: Node | None) -> Node | None:

    
#once the tree has been constructed this program then traverses the tree and finds the childeren of the left node and rights node     

    if node == None:
        return None
    
    
    
    if node.left == None or node.right == None:
        left = node.left
        right = node.right
        
        node.left = right
        node.right = left
        return node
    else:
        #this finds the childeren from the left node and the right node if their childeren are not empty
        leftc = node.left.get_children()
        rightc = node.right.get_children()
        #the childeren of the left node are then set as the childeren of the right node and the childeren of the right node are set the the left node
        node.left.set_children(rightc)
        node.right.set_children(leftc)
        #the program then continues down the tree in a level order traversal 
        node.left, node.right = swap_nodes(node.right), swap_nodes(node.left)
        

        return node
    

