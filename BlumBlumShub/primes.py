"""
From http://www.4dsolutions.net/cgi-bin/py2html.cgi?script=/ocn/python/primes.py
"""

import random

def bigppr(bits=256):
    """
    Ramdomicamente gera um provavel numero primo data um numero de digitos em hexadecimal
    """
     
    candidate = random.getrandbits(bits) | 1  # certificar que eh impar

    prob = 0
    while 1:
        prob=pptest(candidate)
        if prob>0:
            return candidate
        candidate += 2
        
def pptest(n):
    """
    simples implementacao do miller-rabin para deste de provavel primo
    """
    
    if n<=1: 
        return 0

    # se qualquer um dos primos eh um fator, ja era
    bases  = [random.randrange(2,50000) for x in xrange(90)]

    
    for b in bases:
        if n%b==0: 
            return 0
        
    tests,s  = 0L,0
    m        = n-1

    # transformando (n-1) em (2**s) * m

    while not m&1:  #enquanto m eh impar
        m >>= 1
        s += 1

    for b in bases:
        tests += 1
        isprob = algP(m,s,b,n)
        if not isprob: 
            break
            
    if isprob: 
        return (1-(1./(4**tests)))
    
    return 0

def algP(m,s,b,n):
    """
    baseado no algoritmo P no Donald Knuth's ' Arte de programacao computacional
    v.2 pg. 395 
    """
    y = pow(b,m,n)    
    
    for j in xrange(s):
        if (y==1 and j==0) or (y==n-1):
            return 1
        y = pow(y,2,n)       
       
        return 0