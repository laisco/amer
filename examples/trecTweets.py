'''
Created on 9 oct. 2014

@author: karimsayadi
'''

import csv
import re
import networkx as nx
import matplotlib
matplotlib.use('Agg')
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

#Create temporal windows with one day for each window 
def usersFromToDays (u,v,time):
    listtodayu = list()
    listtodayv = list()
    listdayu = list()
    listdayv = list()
    timesplit = time[0].split()
    today = timesplit[2]
    tommorow = int(today) +1
    
    for i in range (len(u)):    
        if int(today)!=tommorow:
            listtodayu.append(u[i])
            listtodayv.append(v[i])
        else:
            tommorow=int(today) +1
            listdayu.append(listtodayu)
            listtodayu = list()
            listdayv.append(listtodayv)
            listtodayv = list()
        if i!=len(u)-1:    
            timesplit = time[i+1].split()
            today = timesplit[2]
        
    return listdayu,listdayv
        
        
            
    

def main():    
    columns = defaultdict(list)
    with open('../data/masterDataSet.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=",")
        reader.next()
        for row in reader:        
            for (i,v) in enumerate(row):
                columns[i].append(v)
                
    #print len(columns)
    
    
    u, v = usersFromToDays(columns[1],columns[2],columns[6])
    #Construct the network with NetworkX library, please note that the index of columns change depending on the edges that you want to create
    G = pwn.pairewiseNetworkDate(u,v,columns[6])
    
    #Analysis of the network

    #print G.number_of_nodes()
    #print G.number_of_edges()
    #print G.degree()
    #print G.nodes(data=True)
    
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