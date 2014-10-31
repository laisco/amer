'''
Created on 25 oct. 2014

@author: karimsayadi
'''
import networkx as nx

#import the basic function for creating and manipulating nodes and edges from the pairewiseNet module
from graph import pairwiseNet as pwn
           
#Create a graph that can store multiedges
#Multi-edges are multiple edges between two nodes. Each edge can hold optional data or attributes.
def multiEdgesNetwork (setofnodes1,setofnodes2,setofnodes3):
    g= nx.MultiGraph()
    
    for ind in range(len(setofnodes1)):
        if setofnodes1[ind]:
            g.add_node(setofnodes1[ind])
        if setofnodes2[ind]:
            g.add_node(setofnodes2[ind])
        if setofnodes3[ind]:
            g.add_node(setofnodes3[ind])
        
    g.add_edges_from(pwn.creatEdges(setofnodes1, setofnodes2))
    g.add_edges_from(pwn.creatEdges(setofnodes1, setofnodes3))
    
    
    return g