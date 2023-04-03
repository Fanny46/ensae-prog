from graph import add_power, graph_from_file, graph_from_file_route
from spanning_tree import Kruskal
from math import inf
# but : maximiser le profit = la somme des utilités 
# contraintes : puissance camion doit être supérieure à la puissance min sur le trajet ; somme des coûts inférieure au budget, un camion n'effectue qu'un trajet

#problème du sac à dos : le sac est le budget, les poids des objets = les prix des camions.
# On veut maximiser la somme des valeurs des objets ie l'utilité des trajets
# donc on commence par calculer pour chaque trajet quel est le camion idéal (le moins cher) => un trajet est associé à un camion



class Catalogue :
    def __init__(self, cam=[]):
        self.cam = cam #puissance, que l'on suppose suffisante pour identifier un camion
        self.nb_cam = len(cam)
        self.cost = dict([(n, []) for n in cam]) #puissance et coût dans cet ordre

    def min_cost(self, num_file) :
        """méthode qui détermine pour chaque trajet le modèle de camion le moins cher capable d'effectuer le trajet
        Args : num_file : numéro du fichier route ou network
        Output : rien
        """
        f = graph_from_file_route("input/routes."+str(num_file)+".in")
        #K = Kruskal(f) #on utilise un arbre couvrant
        g = add_power(f, num_file)
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


f = catalogue_from_file("input/trucks.1.in")
print(f.min_cost(1))



#à partir de là, les fonctions servent à un algo de programmation dynamique mais on voit que ça sera trop long même sur des petits fichiers à cause de la taille du budget
"""def value(self, n, B = 25*(10^9)) :
        value = {}
        for i in range (n) :
            for j in range (B) :
                value[i,j] = -1
        return value


    def m(self, i, j) :      # Define function m so that it represents the maximum value we can get under the condition: use first i trucks, total cost limit is j
        cost = self.cost[i]
        utility = self.route[i][2]
        if i == 0 or j <= 0 :
            self.value[i, j] = 0
            return
        if self.value[i-1, j] == -1 :     # m[i-1, j] has not been calculated, we have to call function m
            return self.m(i-1, j)
        if cost > j :                      # item cannot fit in the budget
            self.value[i, j] = self.value[i-1, j]
        elif self.value[i-1, j-cost] == -1 :     # m[i-1,j-w[i]] has not been calculated, we have to call function m
            return self.m(i-1, j-cost)
        self.value[i, j] = max(self.value[i-1,j], self.value[i-1, j-cost] + utility)
        return self.value[i, j]

    def knapsack(self, i, j):
        if i == 0 :
            return set()
        if self.m[i, j] > self.m[i-1, j] :
            return {i} | self.knapsack(i-1, j-self.cost[i])
        else:
            return self.knapsack(i-1, j)"""