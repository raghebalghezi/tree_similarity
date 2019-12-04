
from main import SentGraph, Tree2graph

s1 = "(S (NP (D a) (JJ bad) (N researcher)) (VP (V shred) (NP (D the) (N paper))))"
s2 = "(S (NP (D the) (JJ angry) (N dog)) (VP (V ate) (NP (D the) (N steak))))"

score = SentGraph(s1, s2)

entity = Tree2graph(s1)
