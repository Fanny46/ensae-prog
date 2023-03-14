import sys 
sys.path.append("delivery_network")

from graph import Graph, graph_from_file
from spanning_tree import Kruskal, path_spanning_tree, UnionFind
import unittest 

class Test_Kurskal(unittest.TestCase):

    def test_network2(self):
        g = graph_from_file("input/network.02.in")
        S=Kruskal(g)
        self.assertEqual(S.graph[1], [[4, 4, 1]])
        self.assertIn(S.graph[4], [[[1,4,1], [3,4,1]], [[3,4,1], [1,4,1]]])
    
    def test_network4(self):
        g = graph_from_file("input/network.04.in")
        S=Kruskal(g)
        self.assertEqual(S.graph[1], [[2, 4, 1]])
        self.assertIn(S.graph[3], [[[2,4,1], [4,4,1]], [[4,4,1], [2,4,1]]])


if __name__ == '__main__':
    unittest.main()
