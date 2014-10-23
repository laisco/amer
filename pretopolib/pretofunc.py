'''
Created on 6 oct. 2014

@author: karimsayadi
'''
from sets import Set
from .spaces import rel


class pretofunc(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    def pseudoClosure (self, E, A):
        aA = A
        relations = rel() 
        for i in relations:
            if A.intersection(i):
                aA.add(E[relations.index(i)])
        return aA  
    
    def interior(self, E, A):
        iA = Set()
        relations = rel()
        for i in relations:
            #if every element of the set relations of the element e is in A then add to the set of interior
            if Set(i).issubset(A):
                iA.add(E[relations.index(i)])
        return iA