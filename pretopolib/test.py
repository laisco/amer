'''
Created on 6 oct. 2014

@author: karimsayadi
'''

from sets import Set

def main():
    aA = Set() #Interior of A
    E = ['s','t','u','v','w','x','y','z']
    gamma = [['s','t'],['t'],['u','v','x','z'],['v'],['s','v','w','x','z'],['t','v','x'],['v','y','z'],['z']] # Gamma is a binary relation representing a graph
    A = Set(['x','y','z']) # A is a subset of E
     
    for i in gamma:
        
        if Set(i).issubset(A):
            
            aA.add(E[gamma.index(i)]) # index of Gamma is the same as E
      
    print aA
    
    
if __name__ == '__main__':
    main()