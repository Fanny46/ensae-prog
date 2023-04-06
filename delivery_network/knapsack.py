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
        g = add_power(num_file)
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

    def greedy(self, num_file, B=25*(10**9)) : #complexité en O(E*nb_trucks)
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
        

    def rec_knapsack(self, B, routes, trucks, n) : #complexité en O(2^E), E le nombre de trajets
        """ fonction auxiliaire de naive_knapsack, récursive afin d'explorer toutes les combinaisons de trajets possibles.
            La fonction teste pour chaque route si le sac-à-dos obtenu en la choisissant apporte plus d'utilité que celui obtenu en ne la choisissant pas
            Ainsi, on teste tous les sac-à-dos possibles en les comparant 2 à 2 et en gardant toujours le meilleur des 2 (tout en vérifiant à chaque fois si le budget n'est pas dépassé)
        Args : 
                B (float): budget
                routes (liste de listes) : la liste à partir de laquelle on teste les trajets un par un (chaque sous-liste est du type [sommet1, sommet2, puissance, utilité, camion, coût])
                trucks (liste de listes): la liste qui contient les trajets et camions retenus (chaque sous-liste est du type [camion --> (sommet1, sommet2)])
                n (int) : nombre de trajets
        Output :
                val1 ou val2 (int) : l'utilité totale du sac-à-dos
                trucks1 or trucks2 (liste de listes) : les trajets ajoutés dans le sac-à-dos (chaque sous-liste est du type [camion --> (sommet1, sommet2)]) """
        
        if n == 0 or B <= 0 :     # si on est arrivé au dernier trajet ou si le budget a été dépassé, on n'ajoute aucun profit
            return 0, trucks
        if routes[n-1][5] > B :   # si le coût du trajet est supérieur au budget, on ne prend pas ce trajet et on analyse le trajet suivant
            return self.rec_knapsack(B, routes, trucks, n-1)
        else :                    # si le trajet entre dans le budget, on ne le prend que si le profit en le choisissant est supérieur au profit sans le choisir (ie si val1 > val2)
            node1, node2, _, utility, cam, cost = routes[n-1]
            trucks1 = trucks.copy() + [[str(cam) + " --> " + str((node1, node2))]] #on ajoute le trajet étudié à la liste
            rec = self.rec_knapsack(B-cost, routes, trucks1, n-1)
            val1, trucks1 = utility + rec[0], rec[1]
            val2, trucks2 = self.rec_knapsack(B, routes, trucks, n-1)
            if val1 > val2 :
                return val1, trucks1
            else :
                return val2, trucks2
        

    def naive_knapsack(self, num_file, B = 5*(10**9)) :
        """fonction qui initialise la récursion ci-dessus
        Args : 
                num_file (int) : num d'un fichier routes et de son network associé
                B (float) : le budget, fixé
        Output :
                val1 ou val2 : l'utilité totale obtenue avec la collection de camions optimale, affichée afin de pouvoir la comparer avec celle obtenu par approximation locale (greedy)
                trucks (liste de listes) : la collection de camions à acheter ainsi que les trajets auxquels les affecter (chaque sous-liste est du type [camion --> (sommet1, sommet2)]) """
        routes = self.min_cost(num_file)
        trucks = []
        return self.rec_knapsack(B, routes, trucks, len(routes))

 
 


def catalogue_from_file(filename) : 
    """Completer le dictionnaire avec le fichier
    Args :
            filename (str): nom du fichier trucks
    Output : 
            c (class Catalogue) : le catalogue obtenu à partir du fichier, sous la forme d'une liste de camions et d'un dictionnaire qui associe son coût à chaque camion
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
#print(f.naive_knapsack(1))
#on constate que les 2 algos donnent le même résultat