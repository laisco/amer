'''
Created on 25 oct. 2014

@author: karimsayadi


This module will include all the function for creating and manupilating a pairwise network
'''


import networkx as nx


def creatEdges (users, toPseudos):
    edges = list()
    for i in range(len(users)):
        if toPseudos[i]:
            e=(users[i],toPseudos[i])
            edges.append(e)
    return edges       

#Create Edges with a time attributes e.g. When the relation between two husers has been established

def creatEdgesDateStatic (users, toPseudos, date):
    edges = list ()
    for i in range(len(users)):
        if toPseudos[i]:
            edges.append((users[i],toPseudos[i],{'time':''+date[i]}))
    return edges    


#Add attribute for the begining and the end of the relationship
#We begin with a simple condition if a node establish another relation with another node that the current relation that he established 
#at t -1 comes to an end.

#u and v are list of lists each list represent one day of the connection
        
def creatEdgesDateDynamic (u, v, date):
    edges = list ()
    for listtoday in u:
        for i in range(len(listtoday)):
            if v[u.index(listtoday)][i]:
                # I will put the attributes with a start and an and if i find a solution to find when the relation ends in the list
                # For now i will just use a temporal window of one day
                #attributes = {'start':''+date[i],'end':''+date[i],'st':''+str(u.index(listtoday))}
                edges.append((u[u.index(listtoday)][i],
                              v[u.index(listtoday)][i],
                              {'st':''+str(u.index(listtoday))}))     
    return edges 


# Create a pairewise network e.g. from reply messages with @ or with the retweet messages wit RT@    
def pairewiseNetwork (setofnodes1, setofnodes2):
    g = nx.Graph()
    for ind in range(len(setofnodes1)):
        if setofnodes1[ind]:
            g.add_node(setofnodes1[ind])
        if setofnodes2[ind]:
            g.add_node(setofnodes2[ind])
    
    g.add_edges_from(creatEdges(setofnodes1, setofnodes2))
    return g

#Create a pairewise network with the exact date of the tweet as an attribute to the node. This encapsulation of
#the pairwise will allows us to construct some temporal windows. 
def pairewiseNetworkDate (setofnodes1, setofnodes2, date):
    g = nx.Graph()
    """
    for ind in range(len(setofnodes1)):
        if setofnodes1[ind]:
            g.add_node(setofnodes1[ind],time=date[ind])
        if setofnodes2[ind]:
            g.add_node(setofnodes2[ind],time=date[ind])
    """
    g.add_edges_from(creatEdgesDateDynamic(setofnodes1, setofnodes2,date))
    return g


            