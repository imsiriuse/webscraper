from typing import Tuple, TypeVar, Generator, List
from tree_iter import TreeIter

T = TypeVar("T")

class Tree:
    @property
    def parent(self) -> T:
        try:
            return self._parent
        except AttributeError:
            return None
    
    @property
    def children(self) :
        try:
            return tuple(self._children)
        except AttributeError:
            self._children = []
            return tuple(self._children)
    
    @children.setter
    def _set_children(self, children: List[T]):
        del self.children
        self._children = children
        
    @children.deleter
    def _del_children(self):
        del _children
    
    @property
    def path_to_root(self) -> Generator[T, None, None]:
        cur = self
        while cur is not None:
            yield cur
            cur = cur.parent        
    
    @property
    def path_from_root(self) -> Tuple[T]:
        return tuple(reversed(list(self.path_to_root())))
    
    @property
    def siblings(self) -> Tuple[T]:
        if self.parent is None:
            return tuple()
        else:
            return tuple(node for node in self.parent.children if node is not self)
    
    
    @property
    def depth(self) -> int:
        for (i, _) in enumerate(self.path_to_root):
            continue
        return i
    
    @property
    def is_leaf(self):
        return self.children and len(self.children) == 0
    
    @property
    def leaves(self) -> Tuple[T]:
        return tuple(node for node in TreeIter(self, lambda x: x.is_leaf))


"""TODO: refactor and properly integrate into Tree"""
def print_tree(current_node, indent="", last='updown'):
    nb_children = lambda node: sum(nb_children(child) for child in node.children) + 1
    size_branch = {child: nb_children(child) for child in current_node.children}

    """ Creation of balanced lists for "up" branch and "down" branch. """
    up = sorted(current_node.children, key=lambda node: nb_children(node))
    down = []
    while up and sum(size_branch[node] for node in down) < sum(size_branch[node] for node in up):
        down.append(up.pop())

    """ Printing of "up" branch. """
    for child in up:     
        next_last = 'up' if up.index(child) == 0 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " * len(repr(current_node)))
        print_tree(child, indent=next_indent, last=next_last)

    """ Printing of current node. """
    if last == 'up': start_shape = '┌'
    elif last == 'down': start_shape = '└'
    elif last == 'updown': start_shape = ' '
    else: start_shape = '├'

    if up: end_shape = '┤'
    elif down: end_shape = '┐'
    else: end_shape = ''

    print('{0}{1}{2}{3}'.format(indent, start_shape, repr(current_node), end_shape))

    """ Printing of "down" branch. """
    for child in down:
        next_last = 'down' if down.index(child) is len(down) - 1 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " * len(repr(current_node)))
        print_tree(child, indent=next_indent, last=next_last)    