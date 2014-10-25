'''
Created on 24 oct. 2014

@author: karimsayadi
'''

#This module offers some utility functions like for example creating a dynamic file graph.

#The function write_dgs parse the content of a networkx graph to create a dgs file that can be used with graph stream.

import itertools

from networkx.utils.misc import make_str


def write_dgs(G,path):
    """Write G in dgs format to path 
    Examples 
    --------
    >>> G = nx.path_graph(4)
    >>> utilgraph.write_dgs(G,"test.dgs")
    """
    writer = DGSWriter()
    #writer.add_graph(G) In the second version we will add more features of the networks and we will need to implement specific function
    writer.write(path,G) # For now we will use only the write function which will get the list of nodes and the list of the edges and put them in the edges.
    # In the next version G will not be part of the parameter of the function write.
    
    
class DGSWriter ():
#class for writing dgs file
#use writer_dgs function
    def __init__ (self):
                # counters for edge and attribute identifiers
        self.edge_id=itertools.count()
        self.attr_id=itertools.count()
        # default attributes are stored in dictionaries
        self.attr={}
        self.attr['node']={}
        self.attr['edge']={}
        self.attr['node']['dynamic']={}
        self.attr['node']['static']={}
        self.attr['edge']['dynamic']={}
        self.attr['edge']['static']={}
        
    def add_graph(self,G):
        #Add a graph element to the structure of the dgs
        self.add_nodes(G)
        self.add_edges(G)
        
    def add_nodes (self,G):
        for node,data in G.nodes_iter(data=True):
            node_data = data.copy()
            node_id = make_str(node_data.pop('id',node))
            
            print '{0:2s} {1:3s}'.format('an', '"'+node_id+'"')
            
        
    def add_edges(self,G):
        def edge_key_data(G):
            #helper function to unify multigraph and graph edge iterator
            if G.is_multigraph():
                for u,v,key,data in G.edges_iter(data=True, keys=True):
                    edge_data = data.copy()
                    edge_data.update(key=key)
                    edge_id = edge_data.pop('id', None)
                    print(edge_id)
                    if edge_id is None:
                        edge_id=next(self.edge_id)
                    yield u,v,edge_id, edge_data
            else:
                for u,v,data in G.edges_iter(data=True):
                    edge_data = data.copy()
                    edge_id=edge_data.pop('id',None)
                    if edge_id is None:
                        edge_id = next(self.edge_id)
                        print(edge_id)
                    yield u,v,edge_id,edge_data
                    
    def write(self,path, G):
        header = 'DGS004'
        graphName  = 'tweetFromTO 0 0'
        f = open (path,'w')
        f.write(header+'\n')
        f.write(graphName+'\n') 
        for node,data in G.nodes_iter(data=True):
            node_data = data.copy()
            node_id = make_str(node_data.pop('id',node))
            
            f.write ('{0:2s} {1:3s}'.format('an', '"'+node_id+'"')+'\n')
        def edge_key_data(G):
            # helper function to unify multigraph and graph edge iterator
            if G.is_multigraph():
                for u,v,key,data in G.edges_iter(data=True,keys=True):
                    edge_data=data.copy()
                    edge_data.update(key=key)
                    edge_id=edge_data.pop('id',None)
                    if edge_id is None:
                        edge_id=next(self.edge_id)
                    yield u,v,edge_id,edge_data
            else:
                for u,v,data in G.edges_iter(data=True):
                    edge_data=data.copy()
                    edge_id=edge_data.pop('id',None)
                    if edge_id is None:
                        edge_id=next(self.edge_id)
                    yield u,v,edge_id,edge_data
                    
        for u,v,key,edge_data in edge_key_data(G):
            f.write('{0:2s} {1:3s} {2:4s} {3:5s}'.format('ae', '"'+make_str(key)+'"','"'+make_str(u)+'"','"'+make_str(v)+'"')+'\n')
            
        f.close()
