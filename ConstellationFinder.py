import math #just in case you want to have b=pi or other fun stuff like that

def extended_gcd(a, b): #Helps us reduce fractions
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1

    return gcd, x, y

class Fraction: #we need to work with fractions to avoid problems with floating points
    def __init__(self,numerator,denominator):
        if denominator != 0:
            gcd, x, y = extended_gcd(numerator, denominator)
            self.numerator = int(numerator / gcd)
            self.denominator = int(denominator / gcd)
            self.actualValue = self.numerator / self.denominator
            self.print = '(' + str(self.numerator) + '/' + str(self.denominator) + ')'
            self.error = False
        else:
            self.error = True

    def __add__(self, other):
        if type(other) == int:
            fraction2 = Fraction(other,1)
        elif type(other) == type(Fraction(1,1)):
            fraction2 = other
        newNumerator = self.numerator * fraction2.denominator + fraction2.numerator * self.denominator
        return Fraction(newNumerator, self.denominator * fraction2.denominator)

    def __sub__(self, other):
        if type(other) == int:
            fraction2 = Fraction(other,1)
        elif type(other) == type(Fraction(1,1)):
            fraction2 = other
        newNumerator = self.numerator * fraction2.denominator - fraction2.numerator * self.denominator
        return Fraction(newNumerator, self.denominator * fraction2.denominator)

    def __mul__(self, other):
        if type(other) == float:
            fraction2 = Fraction(other,1)
        if type(other) == int:
            fraction2 = Fraction(other,1)
        elif type(other) == type(Fraction(1,1)):
            fraction2 = other
        return Fraction(self.numerator * fraction2.numerator, self.denominator * fraction2.denominator)

    def __truediv__(self, other):
        if type(other) == int:
            fraction2 = Fraction(other,1)
        elif type(other) == type(Fraction(1,1)):
            fraction2 = other
        if fraction2.error:
            print('You are trying to divide by zero idiot')
        return Fraction(self.numerator * fraction2.denominator, self.denominator * fraction2.numerator)

def Collatz(start,finish): #Generates the constellation in one section of the Collatz Tree
    n = start
    sequence=[start]
    while True:
        if n%2 == 0:
            n=n/2
            if (n-4)%6 == 0:
                sequence.append(n)
            if n == finish:
                return sequence
        elif n%2 ==1 :
            n=3*n+1
            if (n-4)%6 == 0:
                sequence.append(n)
            if n == finish:
                return sequence

class Node: #I needed to access all of thee constants dynamically and this is the best I came up with
    def __init__(self,symbol):
        if symbol == 'S':
            self.n1 = Fraction(2,1)
            self.n2 = Fraction(1,1)
            self.s1 = Fraction(3,1)
            self.s2 = Fraction(2,1)
        elif symbol == 'L':
            self.n1 = Fraction(4,1)
            self.n2 = Fraction(0,1)
            self.s1 = Fraction(3,1)
            self.s2 = Fraction(0,1)
        elif symbol == 'T':
            self.n1 = Fraction(4,1)
            self.n2 = Fraction(2,1)
            self.s1 = Fraction(1,1)
            self.s2 = Fraction(0,1)

def Threading(constellation): #This is the heart and soul of this code, this gets the diophantine equations
    [constant1, constant2] = [1, 0]
    for n in range(1, len(constellation)):
        prevNode = Node(constellation[n - 1])
        currentNode = Node(constellation[n])
        factor1 = prevNode.s1 / currentNode.n1
        constant1 = factor1 * constant1
        factor2 = (prevNode.s2 - currentNode.n2) / currentNode.n1
        constant2 = factor1 * constant2 + factor2
    gcd, x, y = extended_gcd(constant1.denominator \
                             * constant2.denominator, constant1.denominator)
    constant3 = Fraction(gcd,1)
    constant1 = constant3 * constant1
    constant2 = constant2 * constant3
    return constant1, constant2, constant3

def getNodes(Solutions_a_0,Solutions_a_n,constellation,b): #Give it the coefficients for the constellation and it will find it somewhere
    firstNode = Node(constellation[0])
    lastNode = Node(constellation[len(constellation)-1])
    a_0 = Solutions_a_0[0] * b + Solutions_a_0[1]
    a_n = Solutions_a_n[0] * b + Solutions_a_n[1]
    n1 = firstNode.n1 * a_0 + firstNode.n2
    n2 = lastNode.s1 * a_n + lastNode.s2
    return 6*n1+4, 6*n2+4

def getEachNode(a0,b,constellation): #Give it a starting point, a value of b, and a constellation, and it will find the nodes
    nodes = []
    a0 = b*a0[0] + a0[1]
    for element in range(0, len(constellation)-1):
        nextNode = Node(constellation[element + 1])
        currentNode = Node(constellation[element])
        n = currentNode.n1 * a0 + currentNode.n2
        nodes.append(n.actualValue*6+4)
        a0 = (currentNode.s1 * a0 + currentNode.s2 - nextNode.n2)/nextNode.n1
    lastNode = Node(constellation[len(constellation)-1])
    n = lastNode.n1 * a0 + lastNode.n2
    nodes.append(n.actualValue*6+4)
    return nodes

#I tested with many constellations and many values of b

#constellation = 'SLS'
#constellation = 'SLSSSSLLSLSSLSSSLTSSSLSLSSSSSTSSSSTLLLTLTSSSTTSTL'
#constellation = 'LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL'
constellation = 'SSSLLLTS'
#constellation = 'SSSLLL'
#b= Fraction(-7459848397017429,144115188075855872)
#b=Fraction(-14919696794034863,288230376151711744)
#b = Fraction(1,29)
#b=Fraction(6,2**20)
#constellation = ''
#constellation = 'SSSLSSTLS'
#constellation = 'SS'
b = Fraction(0,1)
constant1,constant2,constant3 = Threading(constellation)
gcd,x,y = extended_gcd(constant3.numerator,-constant1.numerator)
a0 = [constant3.numerator,(gcd*y*constant2.numerator)%constant3.numerator] #We take the modulo to 'slide' the solutions so that if b<0 everything is negative too
an = [constant1.numerator,(gcd*x*constant2.numerator)%constant1.numerator]

print('The equation for the constellation '+constellation+' is '+str(int(constant3.actualValue))+'*a_n = '+str(int(constant1.actualValue))+' * a_0 + '+str(int(constant2.actualValue)))

print('The solutions are: a_0 = '+str(a0[0])+' * b + '+str(a0[1])+', a_n = '+str(an[0])+' * b + '+str(an[1]))

print('Finally, using b = '+str(b.print)+' we find that one example of this constellation is: '+str(getEachNode(a0,b,constellation)))
