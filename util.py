class Node():
    def __init__(self, state: str, parent: str, action):
        self.state = state
        self.parent = parent
        self.action = action
        
    def __repr__(self):
        return f'NODE {self.state}'

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state) -> bool:
        for node in self.frontier:
            if node.state == state:
                return True
        return False
    
    def contains_parent(self, parent) -> bool:
        for node in self.frontier:
            if node.parent == parent:
                return True
        return False

    def empty(self) -> bool:
        return len(self.frontier) == 0

    def remove(self) -> Node:
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
