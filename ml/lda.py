'''
Created on 8 oct. 2014

@author: karimsayadi
'''
import numpy

class lda:
    '''
    Latent Dirichlet Allocation + collapsed Gibbs sampling
    '''


    def __init__(self, K, alpha, beta, docs, V, samrinit=True):
        '''
        Constructor
        '''
        self.K = K 
        self.alpha = alpha #parameter of topics prior 
        self.beta = beta #parameter of words prior 
        self.docs = docs
        self.V = V
        
        self.z_m_n = [] # topics of words of documents
        self.n_m_z = numpy.zeros((len(self.docs),K)) + alpha #word count of each document and topic
        self.n_z_t = numpy.zeros((K,V)) + beta # word count of each topic and vocabulary 
        self.n_z = numpy.zeros(K) + V * beta  #word count of each topic
        
        self.N = 0 
        
        for m, doc in enumerate(docs):
            self.N += len(doc)
            z_n = []
            for t in doc:
                if samrinit:
                    p_z = self.n_z_t[:,t] * self.n_m_z[m] / self.n_z
                    z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()
                else:
                    z = numpy.random.randint(0, K)
                z_n.append(z)
                self.n_m_z[m, z] += 1
                self.n_z_t[z, t] += 1
                self.n_z[z] += 1
            self.z_m_n.append(numpy.array(z_n))
            
                    
            