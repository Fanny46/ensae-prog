from graph import graph_from_file_route
from spanning_tree import Kruskal, path_spanning_tree3
from time import perf_counter
from random import choice

for n in range (1,10) : # on va chercher le temps total qu'il faut pour trouver un chemin entre toutes les paires de sommets dans les 10 fichiers route
    data_path = "input/"
    file_name = "routes."+str(n)+".in"
    G = graph_from_file_route(data_path + file_name)
    X = Kruskal(G)
    S = X[0]
    time=0
    list=[l for l in S.graph.keys()]
    nb_tests = 8
    for i in range(nb_tests) : # on lance le compteur pour des sommets choisis au hasard dans le graphe
        a=choice(list)
        b=choice(list)
        time_begin=perf_counter()

        path_spanning_tree3(S, a, b)

        time_stop=perf_counter()
        time+=time_stop-time_begin
    
    print("Pour calculer un trajet de", file_name, "il s'est écoulé en moyenne : ", time/nb_tests, "secondes.")
    
    tot_time_sec = (time/nb_tests)*S.nb_edges # à partir du temps moyen obtenu, on calcule le temps qu'il faudrait pour trouver tous les chemins possibles dans le graphe
    tot_time_min = tot_time_sec / 60
    print("Pour calculer l'ensemble des trajets de", file_name, "il faudra : ", tot_time_sec, "s., soit", tot_time_min,"min., soit", tot_time_min/60, "h.")



"""************ Début des résultats d'exécution **************************
Avec la fonction path_spanning_tree :

Pour calculer un trajet de routes.1.in il s'est écoulé en moyenne :  7.075053872540593e-06 secondes.
Pour calculer l'ensemble des trajets de routes.1.in il faudra :  0.00013442602357827127 secondes, soit 2.240433726304521e-06 min.
RecursionError: maximum recursion depth exceeded in comparison

Avec la fonction path_spanning_tree2 :

Pour calculer un trajet de routes.1.in il s'est écoulé en moyenne :  1.4624965842813253e-05 secondes.
Pour calculer l'ensemble des trajets de routes.1.in il faudra :  0.0002778743510134518 s., soit 4.63123918355753e-06 min., soit 7.718731972595883e-08 h.
Pour calculer un trajet de routes.2.in il s'est écoulé en moyenne :  0.27605456253513694 secondes.
Pour calculer l'ensemble des trajets de routes.2.in il faudra :  23160.42568757292 s., soit 386.00709479288196 min., soit 6.433451579881366 h.
Pour calculer un trajet de routes.3.in il s'est écoulé en moyenne :  0.4216748250182718 secondes.
Pour calculer l'ensemble des trajets de routes.3.in il faudra :  42164.95245287707 s., soit 702.7492075479512 min., soit 11.712486792465853 h.

Avec la fonction path_spanning_tree3 :

Pour calculer un trajet de routes.1.in il s'est écoulé en moyenne :  1.0262534487992525e-05 secondes.
Pour calculer l'ensemble des trajets de routes.1.in il faudra :  0.00019498815527185798 s., soit 3.2498025878642997e-06 min., soit 5.416337646440499e-08 h.
Pour calculer un trajet de routes.2.in il s'est écoulé en moyenne :  58.66408922499977 secondes.
Pour calculer l'ensemble des trajets de routes.2.in il faudra :  4921799.757799031 s., soit 82029.99596331718 min., soit 1367.1665993886197 h.
"""