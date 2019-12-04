from nltk.tree import Tree
import networkx as nx


class SentGraph:
    
    
    def __init__(self, tree1, tree2):
        from nltk.tree import Tree
        import networkx as nx
        self.t1 = Tree.fromstring(tree1)
        self.t2 = Tree.fromstring(tree2)
        
        
    def jaccard(self, prod=True):
        
        if prod:
            sent1 = set([str(i) for i in self.t1.productions()])
            sent2 = set([str(i) for i in self.t2.productions()])
        else:
            sent1 = set([s.pformat() for s in self.t1.subtrees(lambda t: t.height() == 3)])
            sent2 = set([s.pformat() for s in self.t2.subtrees(lambda t: t.height() == 3)])
        
        return len(sent1.intersection(sent2)) / len(sent1.union(sent2))
    
    def cos_sim(self, prod=True):
        
        from numpy import dot
        from numpy.linalg import norm

        if prod:
            sent1 = set([str(i) for i in self.t1.productions()])
            sent2 = set([str(i) for i in self.t2.productions()])
        else:
            sent1 = set([s.pformat() for s in self.t1.subtrees()])
            sent2 = set([s.pformat() for s in self.t2.subtrees()])

        sent1_vect = [0] * len(sent1.union(sent2))
        sent2_vect = [0] * len(sent1.union(sent2))

        for i, j in enumerate(sent1.union(sent2)):
            if j in sent1:
                sent1_vect[i] = 1
            else:
                sent1_vect[i] = 0
            if j in sent2:
                sent2_vect[i] = 1
            else:
                sent2_vect[i] = 0

        return dot(sent1_vect, sent2_vect)/(norm(sent1_vect)*norm(sent2_vect))
    

class Tree2graph:
    '''Takes a parsed NLTK tree object and returns networkx graph and adj matrix in panda df format'''

    def __init__(self, string_tree):
        
        
        self.t1 = Tree.fromstring(string_tree)
        self.graph = self.to_graph()
        self.numpy = nx.to_numpy_matrix(self.graph)
        self.adj = nx.to_pandas_adjacency(self.graph)
        self.adj_col = list(self.adj.columns)
        self.latex = self.t1.pformat_latex_qtree()
        
    def draw(self):
        return nx.draw_networkx(self.graph, node_size=500)
        
    def to_graph(self): 

        d = dict() # temp dictionary to hold relations e.g. {S:(VP, NP)}
        for branch in self.t1.productions():
            leaf = str(branch).split('->')
            if leaf[0].strip() in d:
                d[leaf[0].strip()+'.'] = tuple(leaf[1].strip().strip("'").split(" "))
            else:
                d[leaf[0].strip()] = tuple(leaf[1].strip().strip("'").split(" "))

        list_tuples = list() ## list of tuples compat. w/ nx.graphs
        for key in d:
            for vals in d[key]:
                list_tuples.append((key,vals))

        G = nx.Graph()

        G.add_edges_from(list_tuples)

        return G
