from random import randint
from collections import deque

uuid = 0
class Node:
    def __init__(self, parent):
        global uuid
        uuid += 1
        self.uuid = uuid

        self.parent = parent
        self.children = {}

    def drop(self):
        if (not self.parent): return

        self.add_child(self.parent)
        if (self in self.parent.children):
            del self.parent.children[self]
        self.parent.drop()

    def add_child(self,child):
        self.children[child] = None

    def __repr__(self):
        return "Node: %d" % (self.uuid)

    def __str__(self):
        return "Node: %d" % (self.uuid)

    def __eq__(self,other):
        return self.uuid == other.uuid

    def __hash__(self):
        return self.uuid

RANDOM_CHILD = 5
RANDOM_HEIGHT_LOW = 8
RANDOM_HEIGHT_HIGH = 10

def make_random_tree():
    root = Node(None)
    queue = deque([root])
    for _ in range(randint(RANDOM_HEIGHT_LOW, RANDOM_HEIGHT_HIGH)):
        if (len(queue) == 0): break
        node = queue.popleft()

        for _ in range(randint(1,RANDOM_CHILD)):
            new_node = Node(node)
            queue.append(new_node)
            node.add_child(new_node)
    return root

def print_tree(base, data):
    for i,node in enumerate(data):

        if (i == len(data)-1):
            print('%s└─%s' % (base, node.uuid))
        else:
            print('%s├─%s' % (base, node.uuid))

        if (not node.children): continue

        if (i == len(data)-1):
            print_tree(base + '  ', node.children)#+[None])
        else:
            print_tree(base + '│ ', node.children)#+[None])

def method_one_helper(node, depth):
    max_depth = depth
    max_node = node

    for child in node.children:
        d,n = method_one_helper(child, depth+1)
        if (d > max_depth):
            max_depth = d
            max_node = n
    return (max_depth, max_node)
        

def method_one(root):
    _,n1 = method_one_helper(root, 0)
    n1.drop()
    d1,_ = method_one_helper(n1, 0)

    return d1+1

def method_two_helper(node, depth):


    max_distance = 0
    max_depths = []

    if (len(node.children) == 0):
        return (0,depth)

    for child in node.children:
        mdi,mde = method_two_helper(child, depth+1)
        if (mdi > max_distance):
            max_distance = mdi
        max_depths.append(mde)

    max1 = 0
    max2 = 0
    for d in max_depths:
        if (d > max1):
            max2 = max1
            max1 = d
        elif (d > max2):
            max2 = d

    #if (max1 != 0 and max2 != 0):
    distance = (max1+max2 - 2*depth)+1
    max_distance = max(max_distance, distance)

    return (max_distance, max(max_depths))

def method_two(root):
    return method_two_helper(root, 0)[0]

def main():
    distance1 = 0
    distance2 = 0
    while (distance1 == distance2):
        global uuid
        uuid = 0
        root = make_random_tree()
        print_tree("", [root])

        distance2 = method_two(root)
        distance1 = method_one(root)

    print("DISCREPANCY FOUND")
    print(distance1, distance2)

main()
