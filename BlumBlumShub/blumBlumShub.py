"""
Adaptado de http://javarng.googlecode.com/svn/trunk/com/modp/random/BlumBlumShub.java
fonte: https://github.com/VSpike/BBS
"""

import sys
import random
import primes
import time

class BlumBlumShub(object):


    def getPrime(self, bits):
        """
        Gera numero primo para uso no algoritmo Blum-Blum-Shub.

        Isso gera um numero primo apropriado (congruentes a 3 (mod 4)) necessarios para
        computador o numero m
        """
        while True:
            p = primes.bigppr(bits)
            if p & 3 == 3:
                return p

    def generateN(self, bits):
        """
        Gera o valor de "n" com base em dois primos gerados
        """
    
        p = self.getPrime(bits/2)
        while 1:
            q = self.getPrime(bits/2)
            #certifica que p eh diferente de q
            if p != q:
                return p * q    

    def __init__(self, bits):
        """
        Construtor, definindo o numero de bits para "n"
        """        
        self.m = self.generateN(bits)
        length = self.bitLen(self.m)
        seed = random.getrandbits(length)
        self.setSeed(seed)  

    def setSeed(self, seed):
        """
        Seta ou reseta o valor da seed e o valor interno
        """
    
        self.state = seed % self.m
    
    def bitLen(self, x):
        "Retorna o tamanho em bits de um inteiro" 
        assert x > 0
        q = 0 
        while x: 
            q += 1 
            x >>= 1 
        return q     

    def next(self, numBits):
        """
        Returno bits aleatorios de tamanho = numBits
        pela formula Xn+1 = Xn^2 modulo M, onde M eh o produto de dois primos grandes
        """
        result = 0
        for i in xrange(numBits):
            self.state = (self.state**2) % self.m
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
    start = time.time()
    while is_Prime(prime) != True:
       prime = bbs.next(4096)
    else:
        print(prime)
        end = time.time()
        print(end-start)
        