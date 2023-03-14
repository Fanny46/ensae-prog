import sys 
sys.path.append("delivery_network")

from graph import Graph, graph_from_file
from spanning_tree import Kruskal, path_spanning_tree, UnionFind
import unittest 

class Test_path_spanning_tree(unittest.TestCase):

    def test_network2(self):
        g = graph_from_file("input/network.02.in")
        S=Kruskal(g)
        self.assertEqual(path_spanning_tree(S,1,2), (4, [1,4,3,2]))
        self.assertEqual(path_spanning_tree(S, 1, 4), (4, [1,4]))

    def test_network4(self):
        g = graph_from_file("input/network.04.in")
        S=Kruskal(g)
        self.assertEqual(path_spanning_tree(S,1,2), (4, [1,2]))
        self.assertEqual(path_spanning_tree(S, 1, 4), (4, [1,2,3,4]))

if __name__ == '__main__':
    unittest.main()
