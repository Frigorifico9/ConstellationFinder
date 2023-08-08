import itertools


def extended_gcd(a, b):  # Helps us reduce fractions
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1

    return gcd, x, y


class Fraction:  # we need to work with fractions to avoid problems with floating points
    def __init__(self, numerator, denominator):
        if denominator != 0:
            gcd, x, y = extended_gcd(numerator, denominator)
            self.numerator = int(numerator / gcd)
            self.denominator = int(denominator / gcd)
            self.actual_value = self.numerator / self.denominator
            self.print = "(" + str(self.numerator) + "/" + str(self.denominator) + ")"
            self.error = False
        else:
            self.error = True

    def __add__(self, other):
        if type(other) == int:
            fraction2 = Fraction(other, 1)
        elif isinstance(other, Fraction):
            fraction2 = other
        new_numerator = self.numerator * fraction2.denominator + fraction2.numerator * self.denominator
        return Fraction(new_numerator, self.denominator * fraction2.denominator)

    def __sub__(self, other):
        if type(other) == int:
            fraction2 = Fraction(other, 1)
        elif isinstance(other, Fraction):
            fraction2 = other
        new_numerator = self.numerator * fraction2.denominator - fraction2.numerator * self.denominator
        return Fraction(new_numerator, self.denominator * fraction2.denominator)

    def __mul__(self, other):
        if type(other) == float:
            fraction2 = Fraction(other, 1)
        if type(other) == int:
            fraction2 = Fraction(other, 1)
        elif isinstance(other, Fraction):
            fraction2 = other
        return Fraction(self.numerator * fraction2.numerator, self.denominator * fraction2.denominator)

    def __truediv__(self, other):
        if type(other) == int:
            fraction2 = Fraction(other, 1)
        elif isinstance(other, Fraction):
            fraction2 = other
        if fraction2.error:
            print("You are trying to divide by zero idiot")
        return Fraction(self.numerator * fraction2.denominator, self.denominator * fraction2.numerator)


def collatz(start, finish):  # Generates the constellation in one section of the Collatz Tree
    n = start
    sequence = [start]
    while True:
        if n % 2 == 0:
            n = n / 2
            if (n - 4) % 6 == 0:
                sequence.append(n)
            if n == finish:
                return sequence
        elif n % 2 == 1:
            n = 3 * n + 1
            if (n - 4) % 6 == 0:
                sequence.append(n)
            if n == finish:
                return sequence


class Node:  # I needed to access all of thee constants dynamically and this is the best I came up with
    def __init__(self, symbol, q):
        if q == 3:
            if symbol == "S":
                self.n1 = Fraction(2, 1)
                self.n2 = Fraction(1, 1)
                self.s1 = Fraction(3, 1)
                self.s2 = Fraction(2, 1)
            elif symbol == "L":
                self.n1 = Fraction(4, 1)
                self.n2 = Fraction(0, 1)
                self.s1 = Fraction(3, 1)
                self.s2 = Fraction(0, 1)
            elif symbol == "T":
                self.n1 = Fraction(4, 1)
                self.n2 = Fraction(2, 1)
                self.s1 = Fraction(1, 1)
                self.s2 = Fraction(0, 1)
        elif q == 5:
            if symbol == "S":
                self.n1 = Fraction(2, 1)
                self.n2 = Fraction(0, 1)
                self.s1 = Fraction(5, 1)
                self.s2 = Fraction(1, 1)
            elif symbol == "L":
                self.n1 = Fraction(4, 1)
                self.n2 = Fraction(3, 1)
                self.s1 = Fraction(5, 1)
                self.s2 = Fraction(4, 1)
            elif symbol == "T":
                self.n1 = Fraction(8, 1)
                self.n2 = Fraction(5, 1)
                self.s1 = Fraction(5, 1)
                self.s2 = Fraction(3, 1)
            elif symbol == "B":
                self.n1 = Fraction(16, 1)
                self.n2 = Fraction(9, 1)
                self.s1 = Fraction(1, 1)
                self.s2 = Fraction(0, 1)


def threading(constellation, q):  # This is the heart and soul of this code, this gets the diophantine equations
    [beta, gamma] = [1, 0]
    for n in range(1, len(constellation)):
        print(constellation)
        prev_node = Node(constellation[n - 1], q)
        current_node = Node(constellation[n], q)
        factor1 = prev_node.s1 / current_node.n1
        beta = factor1 * beta
        factor2 = (prev_node.s2 - current_node.n2) / current_node.n1
        gamma = factor1 * gamma + factor2
    gcd, x, y = extended_gcd(beta.denominator * gamma.denominator, beta.denominator)
    alpha = Fraction(gcd, 1)
    beta = alpha * beta
    gamma = gamma * alpha
    return alpha, beta, gamma


def get_nodes(
    solutions_a_0, solutions_a_n, constellation, b, q
):  # Give it the coefficients for the constellation and it will find it somewhere
    first_node = Node(constellation[0], q)
    last_node = Node(constellation[len(constellation) - 1], q)
    a_0 = solutions_a_0[0] * b + solutions_a_0[1]
    a_n = solutions_a_n[0] * b + solutions_a_n[1]
    n1 = first_node.n1 * a_0 + first_node.n2
    n2 = last_node.s1 * a_n + last_node.s2
    return 6 * n1 + 4, 6 * n2 + 4


def get_each_node(
    a0, b, constellation, q
):  # Give it a starting point, a value of b, and a constellation, and it will find the nodes
    nodes = []
    a0 = b * a0[0] + a0[1]
    for element in range(0, len(constellation) - 1):
        next_node = Node(constellation[element + 1], q)
        current_node = Node(constellation[element], q)
        n = current_node.n1 * a0 + current_node.n2
        nodes.append(n.actual_value * 6 + 4)
        a0 = (current_node.s1 * a0 + current_node.s2 - next_node.n2) / next_node.n1
    last_node = Node(constellation[len(constellation) - 1])
    n = last_node.n1 * a0 + last_node.n2
    nodes.append(n.actual_value * 6 + 4)
    return nodes


def qollatz(q, n):  # Generates the constellation in one section of the Collatz Tree
    sequence = [n]
    while True:
        if n % 2 == 0:
            n = n // 2
            if n in sequence:
                sequence.append(n)
                return sequence
            if n == 1:
                return sequence
            sequence.append(n)
        elif n % 2 == 1:
            n = q * n + 1
            if n in sequence:
                sequence.append(n)
                return sequence
            if n == 1:
                return sequence
            sequence.append(n)


def find_possible_cyclical_a0(q, maxP):
    findings = []
    for i in range(1, maxP):
        alpha = 2**i
        for j in range(1, maxP):
            beta = q**j
            for Y in range(alpha, 1, -1):
                for X in range(beta, 1, -1):
                    b = (X - Y) / (alpha - beta)
                    b_int = (X - Y) // (alpha - beta)
                    if b == b_int:
                        gcd, x2, y2 = extended_gcd(alpha, -beta)
                        gamma = Y / (gcd * y2)
                        gamma_int = Y // (gcd * y2)
                        if gamma == gamma_int:
                            findings.append([alpha, beta, gamma_int])
    return findings


def generate_cyclical_constellations(length, q):
    tiles = []
    if q == 3:
        tiles = "STL"
    if q == 5:
        tiles = "STLB"
    combinations = list(itertools.product(tiles, repeat=length))
    valid_constellations = []
    for constellation in combinations:
        if constellation[0] == constellation[len(constellation) - 1]:
            valid_constellations.append("".join(constellation))
    return valid_constellations
