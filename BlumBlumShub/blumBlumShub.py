"""
Adapted from http://javarng.googlecode.com/svn/trunk/com/modp/random/BlumBlumShub.java
"""

# fonte https://github.com/VSpike/BBS

import sys
import random
import primes

class BlumBlumShub(object):


    def getPrime(self, bits):
        """
        Generate appropriate prime number for use in Blum-Blum-Shub.
         
        This generates the appropriate primes (p = 3 mod 4) needed to compute the
        "n-value" for Blum-Blum-Shub.
         
        bits - Number of bits in prime
        """
        while True:
            p = primes.bigppr(bits)
            if p & 3 == 3:
                return p

    def generateN(self, bits):
        """
        This generates the "n value" for use in the Blum-Blum-Shub algorithm.
       
        bits - The number of bits of security
        """
    
        p = self.getPrime(bits/2)
        while 1:
            q = self.getPrime(bits/2)
            # make sure p != q (almost always true, but just in case, check)
            if p != q:
                return p * q    

    def __init__(self, bits):
        """
        Constructor, specifing bits for n.
         
        bits - number of bits
        """        
        self.n = self.generateN(bits)
        # print "n set to " + repr(self.n)
        length = self.bitLen(self.n)
        seed = random.getrandbits(length)
        self.setSeed(seed)  

    def setSeed(self, seed):
        """
        Sets or resets the seed value and internal state.
         
        seed -The new seed
        """
    
        self.state = seed % self.n
    
    def bitLen(self, x):
        " Get the bit lengh of a positive number" 
        assert x > 0
        q = 0 
        while x: 
            q += 1 
            x >>= 1 
        return q     

    def next(self, numBits):
        "Returns up to numBit random bits"
        
        result = 0
        for i in xrange(numBits):
            self.state = (self.state**2) % self.n
            result = (result << 1) | (self.state&1)
        
        return result    
 
def is_Prime(n):
    """
    O teste Miller-Rabin eh um teste probabilistico da primitividade de um dado numero n
    Se o numero passar no teste, ele eh primo, com uma probabilidade de 75 dependendo de quantas vezes eh testado
    nesse caso, oito vezes
 
    Se retornar False, com certeza nao eh primo
    Se retornar True, muito provavelmente eh um primo
    """

    # se nao for inteiro nao eh primo
    if n!=int(n): 
        return False
    n=int(n)

    # elimina os nao primos menor que 10
    if n==0 or n==1 or n==4 or n==6 or n==8 or n==9: 
        return False
    # elmina os primos menor que 10
    if n==2 or n==3 or n==5 or n==7: 
        return True
    s = 0
    d = n-1
    while d%2==0:
        d>>=1
        s+=1
    assert(2**s * d == n-1)
 
    def trial_composite(a): 
        """
        se n eh numero primo e a nao tiver divisor em comum com d nao eh primo 
        """
        if pow(a, d, n) == 1:
            return False
        """
        Ou se exitir um r E {0,1,...s-1} tal que a ^2^^i*d equivalente a -1 mod n, tambem nao eh primo
        """
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True  
        
    #Oito tentativas para testar se o numero eh primo
    for i in range(8):
        #pega um numero ramdomicamente num range [2,n-1]
        a = random.randrange(2, n)
        #se eh composto, nao eh primo 
        if trial_composite(a): 
            return False
    
    # se chegar aqui, provavelmente eh primo
    return True  

if __name__ == "__main__":
     # seed inicial
    bbs = BlumBlumShub(128)
    prime = 0
    while is_Prime(prime) != True:
       prime = bbs.next(32)
    else:
        print(prime)
        
    #print "Generating 10 numbers"