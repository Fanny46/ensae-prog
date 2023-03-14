#******************** Ce fichier nous sert à la conception des programmes ********************

from graph import graph_from_file, graph_from_file_route
from spanning_tree import Kruskal
from random import randrange, choice
from time import perf_counter
from spanning_tree import output_routes, Kruskal, path_spanning_tree

"""
g = graph_from_file_route("input/"+"routes.1.in")
kruskal = Kruskal(g)
f = open("input/routes.1.in", "r")
h = open("delivery_network/route.test.out", "w")
nb_route = f.readline()
for i in range(int(nb_route) - 1):
    line = f.readline().split()
    src = int(line[0])
    dest = int(line[1])
    h.write(str(src)+" " + str(dest) + " "+ str(path_spanning_tree(kruskal, src, dest)[0]) + "\n")
f.close()
h.close()"""

output_routes(1)