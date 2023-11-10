

class Node:
    def __init__(self, value: str):
        self.value = value
        self.left = None
        self.right = None

    def add_value(self, value: str, children: list) -> bool:
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
        

    def get_children(self) -> tuple:
        return self.left, self.right
    
    def set_children(self, children: tuple):
        self.left = children[0]
        self.right = children[1]
        
        
    def __str__(self):
        return f'value: {self.value}, left: {self.left.value if type(self.left) is Node else None}, right: {self.right.value if type(self.right) is Node else None}'





def construct_tree(data: str) -> Node:

    top_node = Node(data[0])
    
    children = [top_node]

    for char in data[1:]:
        full_children = []
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
    nodes = [first_node.left, first_node.right]
    children = []

    while nodes != []:
        for node in nodes:
            if node != None:
                chars.append(node.value)
                children.append(node.left)
                children.append(node.right)

        nodes = children
        children = []

    return ''.join(chars)
    
    
def swap_nodes(node: Node) -> Node:
    

    if node == None:
        return None
    
    if node.left == None or node.right == None:
        node.left, node.right = node.right, node.left
        return node
    else:

        leftc = node.left.get_children() if node.left != None else (None, None)
        rightc = node.right.get_children() if node.right != None else (None, None)

        node.left.set_children(rightc)
        node.right.set_children(leftc)

        node.left, node.right = swap_nodes(node.right), swap_nodes(node.left)
        

        return node
    




# tree = construct_tree('hello there jiggy')
# tree = swap_nodes(tree)
# tree = swap_nodes(tree)

# print (tree_to_string(tree))

