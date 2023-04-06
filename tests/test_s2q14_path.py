import sys 
sys.path.append("delivery_network")

from graph import Graph, graph_from_file
from spanning_tree import Kruskal, path_spanning_tree, path_spanning_tree3, UnionFind
import unittest 

class Test_path_spanning_tree(unittest.TestCase):

    def test_network2(self):
        g = graph_from_file("input/network.02.in")
        S=Kruskal(g)
        self.assertEqual(path_spanning_tree3(S, 1, 2), (4, [1,4,3,2]))
        self.assertEqual(path_spanning_tree3(S, 1, 4), (4, [1,4]))

    def test_network3(self):
        g = graph_from_file("input/network.03.in")
        S=Kruskal(g)
        self.assertEqual(path_spanning_tree3(S, 1, 3), (10, [1,2,3]))
        self.assertEqual(path_spanning_tree3(S, 1, 4), (10, [1,2,3,4]))

    def test_network4(self):
        g = graph_from_file("input/network.04.in")
        S=Kruskal(g)
        self.assertEqual(path_spanning_tree3(S, 1, 2), (4, [1,2]))
        self.assertEqual(path_spanning_tree3(S, 1, 4), (4, [1,2,3,4]))

if __name__ == '__main__':
    unittest.main()