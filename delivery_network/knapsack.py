from graph import add_power, graph_from_file, graph_from_file_route
from spanning_tree import Kruskal
from math import inf
# but : maximiser le profit = la somme des utilités 
# contraintes : puissance camion doit être supérieure à la puissance min sur le trajet ; somme des coûts inférieure au budget, un camion n'effectue qu'un trajet

#problème du sac à dos : le sac est le budget, les objets sont les trajets, poids d'un objet = prix du camion optimal sur le trajet
# On veut maximiser la somme des valeurs des objets ie l'utilité des trajets
# donc on commence par calculer pour chaque trajet quel est le camion idéal (le moins cher) => un trajet est associé à un camion



class Catalogue :
    def __init__(self, cam=[]):
        self.cam = cam #puissance, que l'on suppose suffisante pour identifier un camion
        self.nb_cam = len(cam)
        self.cost = dict([(n, []) for n in cam]) #puissance et coût dans cet ordre

    def min_cost(self, num_file) : #complexité en O(E*nb_trucks)
        """méthode qui détermine pour chaque trajet le modèle de camion le moins cher capable d'effectuer le trajet
        Args : num_file : numéro du fichier route ou network
        Output : g.edges : une liste de listes ou chaque sous-liste est du type : [sommet1, sommet2, puissance minimale, utilité, camion optimal, coût du camion optimal]
        """
        f = graph_from_file_route("input/routes."+str(num_file)+".in")
        K = Kruskal(f) #on utilise un arbre couvrant
        g = add_power(K[0], num_file)
        for i in range(len(g.edges)) : 
            power = g.edges[i][2]
            min_cost = inf
            for cam in self.cam :
                cost = self.cost[cam]
                if cam >= power and cost < min_cost :
                    min_cost = cost
                    min_cam = cam
            g.edges[i] += [min_cam, min_cost] #on ajoute à l'arête le camion dont le coût est minimal ainsi que ce coût
        return g.edges

    def greedy(self, num_file, B=25*(10**9)) : #complexité en O(E*nb_trucks) à cause de l'appel de min_cost
        """ Fonction qui détermine la collection de camions à acheter ainsi que le trajet auquel chaque camion est affecté.
            On demande aussi à l'algo de print le coût total et l'utilité totale des camions achetés.
            On implémente un algorithme glouton.
        Args : 
                num_file : le numéro des fichiers route et network qui sont associés via add_power
                B : le budget
        Output :
                trucks : une liste de listes telle que chaque sous-liste est du type : [camion --> (sommet1, sommet2)] où le modèle de camion est défini par sa puissance"""
        routes = self.min_cost(num_file)    #on utilise la fonction précédente qui associe à chaque trajet un camion avec son coût
        ratios = {}
        choice = {}    #pour l'instant, notre sac-à-dos est vide : on n'a choisi aucun trajet
        for r in routes :                   #tri par ordre décroissant d'un dico des rapports utilité/coût des trajets : le rapport le plus faible correspond au trajet le plus rentable
            ratios[tuple(r)] = r[3]/r[5]
        sorted_ratios = dict(sorted(ratios.items(), key=lambda x: x[1], reverse=True))
        for r in sorted_ratios :       #on sélectionne les trajets par ordre de rentabilité, tant que le budget n'est pas dépassé
            if r[5]<= B :
                choice[tuple(r)] = True
                B = B - r[5]

        #on a obtenu dans choice la liste des trajets les plus rentables dont les coûts restent inférieurs au budget
        #on affiche alors la flotte de camions à acheter, ainsi que les trajets auxquels il faut affecter les camions :

        tot_cost = 0
        tot_utility = 0
        trucks = []
        for route in choice :
            tot_cost +=route[5]
            tot_utility += route[3]
            trucks.append([str(route[4]) + " --> " + str((route[0] , route[1]))])
        print("le coût total est de : " + str(tot_cost))
        print("l'utilité totale est de : " + str(tot_utility))
        return trucks
        
            

def catalogue_from_file(filename) : 
    """Completer le dictionnaire avec le fichier
    Args:
        filename (str): nom du fichier trucks
    """
    with open(filename, "r") as file :
        n = int(file.readline())
        c = Catalogue([])
        c.nb_cam = n
        for i in range(n):
            cam, cost = list(map(int, file.readline().split()))
            c.cam.append(cam)
            c.cost[cam] = cost
    return c


f = catalogue_from_file("input/trucks.0.in")
print(f.greedy(2))