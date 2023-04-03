from graph import Graph, graph_from_file_route, graph_from_file
from random import choice

#******************** Question 12 ********************
class UnionFind:
    def __init__ (self, G = Graph()) :
        self.root = {k : k for k in G.nodes} # la racine va permettre d'associer aux sommets d'un sous-ensemble un unique sommet qui sera leur "racine" car on veut construire un arbre
        self.rank = {k : 0 for k in G.nodes} # nombre de fils par sommet

    def find(self, k) : # on trouve la racine d'un sommet au sein d'un sous-arbre
        """_summary_
        On trouve la racine d'un sommet au sein d'un sous-arbre.
        Args:
            k (int): sommet dont on veut trouver la racine
        """
        if self.root[k] != k :
            return self.find(self.root[k])
        else : return k

    def union(self, x, y) : # pour construire l'arbre, on relie deux sous-arbres par leur racine : l'une devient la racine de l'autre
        """Permet de relier deux sous-arbres par leurs racines (nécessaire à la construction du graph)
        Args:
            x : sous-arbre de racine x
            y : sous-arbre de racine y
        Returns:
            Ne retourne rien
        """
        rx = self.find(x)
        ry = self.find(y)
        if self.rank[rx] > self.rank[ry]:
            self.root[ry] = rx
        else :
            self.root[rx] = ry
            if self.rank[rx] == self.rank[ry] :
                self.rank[ry] += 1
        return None

 
    
def Kruskal(G) : # prend un graph G en entrée. Complexité en O(Elog(E))
    """Implémentation de l'Algorithme de Kurskal : contruit un abre couvrant de poids minimal.
    Args:
        G (Graph): Graph dont on veut obtenir l'arbre couvrant de poids minimal.
    Returns:
        Graph, root : retourne l'arbre couvrant de poids minimal et la racine de l'arbre (utile dans une autre fonction)
    """
    U = UnionFind(G)
    nodes = []
    X = Graph(nodes)
    s_edges = sorted(G.edges, key=lambda x:x[2]) # on trie les arêtes par ordre de poids
    for edge in s_edges : # pour chaque arête, si les sommets u et v ne sont pas dans le même sous-arbre, on va les relier jusqu'à avoir un arbre unique
        u = edge[0]
        v = edge[1]
        power = edge[2]
        if U.find(u) != U.find(v): # si les deux points ne sont pas dans le même sous-abre (i.e. ils n'ont pas la même racine)
            X.add_edge(u,v,power) # on ajoute l'arête (u,v) à l'arbre couvrant
            U.union(u,v) # on unit les sous-arbres des sommets u et v pour qu'ils aient la même racine (on crée un arbre, sans cycle)
    root = U.find(s_edges[0][0])
    return X, root



#******************** Question 14 ******************** 
# Complexité en O(V)
def aux_parcours(S, node, path, src, dest, nodes_v, powers) :
    """fonction auxiliaire de path_spanning_tree qui renvoie le chemin allant d'une source à une destination et la puissance minimale pour couvrir le trajet
    """
    if node == dest:
        return max(powers), path
    for i in S.graph[node] :
        k=i[0]
        k_power = i[1]
        if not nodes_v[k] :
            nodes_v[k]=True
            powers.append(k_power)
            return aux_parcours(S, k, path+[k], src, dest, nodes_v, powers)
        elif i == S.graph[node][-1] and path[-1] != src : # en cas de cul-de-sac, on repart en arrière
            nodes_v[i[0]]=True
            powers.pop()
            path.pop()
            k = path[-1]
            return aux_parcours(S, k, path, src, dest, nodes_v, powers)
    return None

def path_spanning_tree (S, src, dest) : # prend un arbre couvrant en entrée
    """Should return power_min, path"""
    nodes_v = {node : False for node in S.nodes}  # dictionnaire qui permet de savoir si l'on est déjà passé par un sommet
    nodes_v [src] = True
    powers = [0]  # on crée une liste qui contient toutes les puissances, dont on gardera le max
    
    return aux_parcours(S, src, [src], src, dest, nodes_v, powers)


#******************** Autre méthode question 14 ********************
def depth (S, root) :
    """fonction qui renvoie la profondeur (par rapport à la racine) à laquelle se situent tous les sommets d'un arbre couvrant et leur père (associé à la puissance du trajet pour y aller)
    """
    parent = {k : [-1, -1 ]for k in S.nodes}
    depth = {k : 0 for k in S.nodes}
    parent[root] = [root, 0]
    return aux_depth(S, root, 1, parent, depth)

def aux_depth(S, node, depth_node, parent, depth) : # complexité en O(V + E)
    """fonction récursive qui renvoie la profondeur (par rapport à la racine) à laquelle se situe un sommet d'un arbre couvrant et son parent (associé à la puissance du trajet jusqu'au parent)
    """
    for edge in S.graph[node] :
        node_v = edge[0]
        power = edge[1]
        if parent[node_v] == [-1,-1] :
            parent[node_v] = [node, power]
            depth[node_v] = depth_node
            aux_depth(S, node_v, depth_node+1, parent, depth)
    return parent, depth

#l'initialisation, en comptant Kruskal, a une complexité en O(Elog(E))

def path_spanning_tree2 (X, src, dest) : # complexité sans tenir compte de l'initialisation : O(V)
    """Should return power_min, path"""
    S, root = X
    dico_parent, dico_depth = depth(S, root)
    path_src = [src]
    path_dest =[dest]
    powers = [0]

    p, p_power = dico_parent[src] # si la source est plus profonde que la destination, on ajoute à path_src la portion de chemin comprise entre la source et un sommet de même profondeur que la destination
    while dico_depth[p] > dico_depth[dest] :
        powers += [p_power]
        path_src += [p]
        p, p_power = dico_parent[p]
    q, q_power = dico_parent[dest]
    while dico_depth[q] > dico_depth[src] : # même chose si la destination est plus profonde que la source
        powers += [q_power]
        path_dest.insert(0, q)
        q, q_power = dico_parent[q]
    while p not in path_dest and q not in path_src : # dès qu'un des parents de la source est ajouté dans path_dest, les 2 chemins montant depuis src et dest se rejoignent : on a donc trouvé l'unique chemin entre src et dest
        powers += [p_power] + [q_power]
        path_src += [p]
        path_dest.insert(0, q)
        p, p_power = dico_parent[p]
        q, q_power = dico_parent[q]
    path = path_src + path_dest # on obtient le chemin de src vers dest en joignant les remontées respectives
    return max(powers), path


#******************** Question 15 ********************
def output_routes(num_fichier):
    g = graph_from_file_route("input/routes."+str(num_fichier)+".in")
    kruskal = Kruskal(g)[0]
    f = open("input/routes."+str(num_fichier)+".in", "r")
    h = open("delivery_network/route."+str(num_fichier)+".out", "w")
    nb_route = f.readline()
    for i in range(int(nb_route) - 1):
        line = f.readline().split()
        src = int(line[0])
        dest = int(line[1])
        h.write(str(path_spanning_tree(kruskal, src, dest)[0]) + "\n")
    f.close()
    h.close()

#output_routes(1)
#Le code a déjà été exécuté sur le fichier routes.1.in et peut être consulté dans le delivery_network.





            






