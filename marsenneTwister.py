# Prime Number Sieve
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
# fonte https://inventwithpython.com/cracking/chapter22.html
import math, random
import time

def primeSieve(sieveSize):
    # Retorna uma lista de numeros primos calculados usando
    # o algoritmo peneira de Eratosthenes

    sieve = [True] * sieveSize
    sieve[0] = False # 0 e 1 nao sao primos
    sieve[1] = False

    # cria a peneira:
    for i in range(2, int(math.sqrt(sieveSize)) + 1):
        pointer = i * 2
        while pointer < sieveSize:
            sieve[pointer] = False
            pointer += i

    # compila a lista de primos:
    primes = []
    for i in range(sieveSize):
        if sieve[i] == True:
            primes.append(i)

    return primes

def rabinMiller(num):
    #Retorna True se o numero eh primo
    if num % 2 == 0 or num < 2:
        return False # Miller-Rabin nao funciona para inteiros pares.
    if num == 3:
        return True
    s = num - 1
    t = 0
    while s % 2 == 0:
        # continua reduzindo pela metade ate que seja impar
        # e usa t para contar quantas vezes dividimos pela metade
        s = s // 2
        t += 1
    for trials in range(5): # Tenta negar a primalidade 5 vezes.
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1: # esse teste nao se aplica se v igual a 1
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True

 # Most of the time we can quickly determine if num is not prime
 # by dividing by the first few dozen prime numbers. This is quicker
 # than rabinMiller() but does not detect all composites.

#Na maioria das vezes podemos determinar rapidamente se um numero nao eh primo
# dividindo pelos primeiras dezenas de numeros primos. Isso eh mais rapido
# do que o rabinMiller() mas nao funciona para todas as composicoes
LOW_PRIMES = primeSieve(100)


def isPrime(num):
    # Retorna True se o numero eh primo. Essa funcao 
    # usa os metodos mais rapidos antes de apelar para o ranbinMiller()
    if (num < 2):
        return False # 0, 1, e numeros negativos nao sao primos.
    # Verifica se algum dos primos baixos pode dividir o numero:
    for prime in LOW_PRIMES:
        if (num == prime):
            return True
        if (num % prime == 0):
            return False
    # Se todo o resto falhar, chama o rabinMiller para determinar se numero eh primo:
    return rabinMiller(num)


def generateLargePrime(keysize=1024):
    #Retorna um numero primo de tamanho keysize de bits:
    while True:
        #Usa o pacote random do phyton (MarsenneTwistter)
        # para gerar um numero aleatorio de keysize bits
        num = random.randrange(2**(keysize-1), 2**(keysize)) 
        if isPrime(num):
            return num

if __name__ == '__main__':
    start = time.time()
    prime = generateLargePrime(4096)
    print(prime)
    print(time.time()-start)
