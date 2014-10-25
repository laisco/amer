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
from mpl_toolkits.basemap import Basemap as Basemap#For the drawing on a map
from graph import utilgraph
from graph import pairwiseNet as pwn


from collections import defaultdict

# pull out for who the message is to when we find @ in the begining of message
def toextract(tweet):
    pseudoreg = re.compile("(?<=^@)(?P<pseudostr>.*?)(?=\s)")
    pseudo = pseudoreg.search(tweet)
    if pseudo:
        return pseudo.group(0)
    
# pull out from who the user is retweeting

def RTextract(tweet):
    pseudoreg = re.compile("(?<=RT\s@)(?P<pseudostr>.*?)(?=\s)")
    pseudo = pseudoreg.search(tweet)
    if pseudo:
        return pseudo.group(0)

#Append to the Refdict columns others columns for the to and RT, hour and date 
def toRTcolumns (tweets,columns):
    
    for i in range(len(tweets)):
        
        columns[len(columns)+1].append(toextract(tweets[i])) #Add another column with the corresponding pseudos Col 9
        columns[len(columns)+2].append(RTextract(tweets[i])) #Add another column with the corresponding retweeted columns Col 10
        columns[len(columns)+3].append(hourExtract(columns[6][i])) #Add another column with the corresponding hour of the tweet Col 11
        columns[len(columns)+4].append(dateExtract(columns[6][i])) #Add another column with the corresponding date of the tweet Col 12

#Return two variables : the hour and the data of the tweets
def hourExtract (Times):
    Time = Times.split()
    hourmns = Time[3].split(str=":")
    hour = hourmns[0]
    return hour

    
def dateExtract (Times):
    Time = Times.split()
    dateTweet = Time[0]+Time[1]+Time[2]+Time[5]
    return dateTweet



#Create a pairewise network with the exact date of the tweet as an attribute to the node. This encapsulation of
#the pairwise will allows us to construct some temporal windows. 


            
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

   
            
    

def drawNodesOnMap():
    m = Basemap(
        projection='merc',
        llcrnrlon=-130,
        llcrnrlat=25,
        urcrnrlon=-60,
        urcrnrlat=50,
        lat_ts=0,
        resolution='i',
        suppress_ticks=True)
    # position in decimal lat/lon
    lats=[37.96,42.82]
    lons=[-121.29,-73.95]
    # convert lat and lon to map projection
    mx,my=m(lons,lats)
    
    # The NetworkX part
    # put map projection coordinates in pos dictionary
    G=nx.Graph()
    G.add_edge('a','b')
    pos={}
    pos['a']=(mx[0],my[0])
    pos['b']=(mx[1],my[1])
    # draw
    nx.draw_networkx(G,pos,node_size=200,node_color='blue')
    
    # Now draw the map
    m.drawcountries()
    m.drawstates()
    #m.bluemarble()
    #m.shadedrelief()
    #m.etopo()
    plt.title('How to get from point a to point b')
    plt.show()

   


def main():    
    columns = defaultdict(list)
    with open('../data/masterDataSet.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=",")
        reader.next()
        for row in reader:        
            for (i,v) in enumerate(row):
                columns[i].append(v)
                
    #print len(columns)
    
    
    
    #Construct the network with NetworkX library, please note that the index of columns change depending on the edges that you want to create
    G = pwn.pairewiseNetworkDate(columns[1],columns[2],columns[6])
    
    #Analysis of the network

    #print G.number_of_nodes()
    #print G.number_of_edges()
    #print G.degree()
    print G.nodes(data=True)
    
    #nx.write_gexf(G, '../tweetFromTo.gexf')
    utilgraph.write_dgs(G, '../tweetFromTo.dgs')
    #Draw the graph with the layout parameter
    
    #pos = nx.spring_layout(g)
    #nx.draw(g,pos)
    #plt.show()
    #plt.savefig("pairwisetweetNetwork.png")
    
    # Drawing 
    
    #fig = plt.figure(figsize=(50,50))
    #circular draw
    #nx.draw_circular(G, with_labels = False)
    #spring graph 
    #nx.draw_spring(G, with_labels = False)
    #simple draw 
    #nx.draw(G, with_labels = False)
    #plt.axis("tight")
    #fig.savefig("pairwisetweetNetworkspringFromTo.png")
    
    #Draw nodes on a map, this is not currently operational
    #drawNodesOnMap()      
    
if __name__ == '__main__':
    main()        