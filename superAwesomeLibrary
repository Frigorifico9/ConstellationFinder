import itertools
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

def CollatzNodes(start,finish): #You give it the first and last nodes, and it generates all the nodes in between
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

class Node: #I needed to access all of these constants dynamically and this is the best I came up with
    def __init__(self,symbol):
        if symbol == 'S':
            self.n1 = Fraction(2, 1)
            self.n2 = Fraction(1, 1)
            self.s1 = Fraction(3, 1)
            self.s2 = Fraction(2, 1)
        elif symbol == 'L':
            self.n1 = Fraction(4, 1)
            self.n2 = Fraction(0, 1)
            self.s1 = Fraction(3, 1)
            self.s2 = Fraction(0, 1)
        elif symbol == 'T':
            self.n1 = Fraction(4, 1)
            self.n2 = Fraction(2, 1)
            self.s1 = Fraction(1, 1)
            self.s2 = Fraction(0, 1)


def threading(constellation):  # This is the heart and soul of this project, this gets the diophantine equations
    [beta, gamma] = [1, 0]
    for n in range(1, len(constellation)):
        prevNode = Node(constellation[n - 1])
        currentNode = Node(constellation[n])
        factor1 = prevNode.s1 / currentNode.n1
        beta = factor1 * beta
        factor2 = (prevNode.s2 - currentNode.n2) / currentNode.n1
        gamma = factor1 * gamma + factor2
    gcd, x, y = extended_gcd(beta.denominator
                             * gamma.denominator, beta.denominator)
    alpha = Fraction(gcd,1)
    beta = alpha * beta
    gamma = gamma * alpha
    return alpha,beta, gamma #the diophantine equation is: alpha*a_n = beta*a_0 + gamma

def getNodes(Solutions_a_0,Solutions_a_n,constellation,b): #Give it the coefficients for the constellation and it will find it somewhere
    firstNode = Node(constellation[0])
    lastNode = Node(constellation[len(constellation)-1])
    a_0 = Solutions_a_0[0] * b + Solutions_a_0[1]
    a_n = Solutions_a_n[0] * b + Solutions_a_n[1]
    n1 = firstNode.n1 * a_0 + firstNode.n2
    n2 = lastNode.s1 * a_n + lastNode.s2
    return 6*n1+4, 6*n2+4

def getEachNode(a0,b,constellation): #Give the formula for a0, a value of b, and a constellation, and it will find the nodes
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

def Qollatz(q,n): #Generates a sequence in a qn+1 tree
    sequence=[n]
    while True:
        if n%2 == 0:
            n=n//2
            if n in sequence:
                sequence.append(n)
                return sequence
            if n == 1:
                return sequence
            sequence.append(n)
        elif n%2 ==1 :
            n=q*n+1
            if n in sequence:
                sequence.append(n)
                return sequence
            if n == 1:
                return sequence
            sequence.append(n)

def findPossibleCyclicalA0(q,maxP): #attempt to find cycles, currently finds cycles, but also other stuff, \
                                    #probably because they have the same structure as cycles (like being SL)
    findings = []
    for i in range(1, maxP):
        alpha = 2 ** i
        for j in range(1, maxP):
            beta = q ** j
            for Y in range(alpha, 1,-1):
                for X in range(beta, 1, -1):
                    b = (X - Y) / (alpha - beta)
                    bInt = (X - Y) // (alpha - beta)
                    if b == bInt:
                        gcd,X2,Y2 = extended_gcd(alpha,-beta)
                        gamma = Y/(gcd*Y2)
                        gammaInt = Y//(gcd*Y2)
                        if gamma == gammaInt:
                            findings.append([alpha, beta, gammaInt])
    return findings

def generateCyclicalConstellations(length,q): #Generates all the constellations of a given legnth that could be cycles \
                                              #The idea is that you could find the equations of these constellations and \
                                              #see if they fulfill the conditions to be cycles
    tiles = []
    if q==3:
        tiles = 'STL'
    if q==5:
        tiles = 'STLB'
    combinations = list(itertools.product(tiles, repeat=length))
    validConstellations = []
    for constellation in combinations:
        if constellation[0] == constellation[len(constellation)-1]:
            validConstellations.append(''.join(constellation))
    return validConstellations

def QollatzF(q,n,maxStep):
    steps = 0
    sequence = [n]
    while steps<maxStep:
        if n%2 == 0:
            n=n//2
        elif n%2 ==1:
            n=q*n+1
        steps += 1
        if n in sequence:
            return steps
        sequence.append(n)
    return steps
