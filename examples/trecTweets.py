'''
Created on 9 oct. 2014

@author: karimsayadi
'''

import csv
import re
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



from collections import defaultdict

def trimat (tweets):
    return re.sub('@', '', tweets)

# pull out for who the message is to when we find @ in the begining of message
def toextract(tweet):
    pseudoreg = re.compile("(?<=^@)(?P<pseudostr>.*?)(?=\s)")
    pseudo = pseudoreg.search(tweet)
    if pseudo:
        return pseudo.group(0)

# Create a pairewise network e.g. from reply messages with @ or with the retweet messages wit RT@    
def pairewiseNetwork (users, toPseudos):
    g = nx.Graph()
    for ind in range(len(users)):
        if users[ind]:
            g.add_node(users[ind])
        if toPseudos[ind]:
            g.add_node(toPseudos[ind])    
    g.add_edges_from(creatEdges(users, toPseudos))
    return g

def creatEdges (users, toPseudos):
    edges = list()
    for i in range(len(users)):
        if toPseudos[i]:
            e=(users[i],toPseudos[i])
            edges.append(e)
    return edges       

def main():    
    columns = defaultdict(list)
    with open('../data/tweets.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=",")
        reader.next()
        for row in reader:        
            for (i,v) in enumerate(row):
                columns[i].append(v)
    
    tweets = columns[4]
    # pull out for who the message is to when we find @ 
    
    
    for i in range(len(tweets)):
        columns[5].append(toextract(tweets[i])) #Add another column with the corresponding pseudos 
    
    #Construct the network with NetworkX library
    G = pairewiseNetwork(columns[1],columns[5])
    #print G.number_of_nodes()
    #print G.number_of_edges()
    #print G.degree()
    
    #pos = nx.spring_layout(g)
    #nx.draw(g,pos)
    #plt.show()
    #plt.savefig("pairwisetweetNetwork.png")
    fig = plt.figure(figsize=(50,50))
    nx.draw(G, with_labels = False)
    plt.axis("tight")
    fig.savefig("pairwisetweetNetwork.png")
    
    
    
   

        
    
if __name__ == '__main__':
    main()        