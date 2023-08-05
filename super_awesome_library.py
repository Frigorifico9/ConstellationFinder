import itertools
from dataclasses import dataclass
from typing import Iterable, List, Tuple, Union


def extended_gcd(a: Union[float, int], b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean algorithm to find the greatest common divisor (gcd)
    and the coefficients x, y that satisfy ax + by = gcd(a, b).

    :param a: an integer or float value representing the first number
    :param b: an integer value representing the second number
    :return: a tuple containing the gcd, x, and y values

    Example Usage:
    >>> extended_gcd(10, 6)
    (2, -1, 2)
    >>> extended_gcd(21, 14)
    (7, 1, -1)
    """
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1

    return gcd, x, y


class Fraction:  # we need to work with fractions to avoid problems with floating points
    def __init__(self, numerator: Union[int, float], denominator: int):
        if denominator == 0:
            raise ArithmeticError

        gcd, x, y = extended_gcd(numerator, denominator)
        self.numerator = numerator / gcd if type(numerator) != int else numerator // gcd
        self.denominator = denominator // gcd

    def __str__(self):
        return f"({str(self.numerator)}/{str(self.denominator)})"

    def __float__(self) -> float:
        """
        Convert a fraction to a floating-point number.

        :return: The floating-point representation of the fraction.
        :rtype: float
        """
        return self.numerator / self.denominator

    def __int__(self) -> int:
        """
        Converts the fraction to an integer by performing integer division of the numerator by the denominator.

        :return: The integer value of the fraction.
        """
        return int(self.numerator // self.denominator)

    def __add__(self, other: Union[int, "Fraction"]) -> "Fraction":
        if type(other) == int or type(other) == float:
            fraction2 = Fraction(other, 1)
        elif isinstance(other, Fraction):
            fraction2 = other
        new_numerator = self.numerator * fraction2.denominator + fraction2.numerator * self.denominator
        return Fraction(new_numerator, self.denominator * fraction2.denominator)

    def __sub__(self, other: Union[int, "Fraction"]) -> "Fraction":
        if type(other) == int:
            fraction2 = Fraction(other, 1)
        elif isinstance(other, Fraction):
            fraction2 = other
        new_numerator = self.numerator * fraction2.denominator - fraction2.numerator * self.denominator
        return Fraction(new_numerator, self.denominator * fraction2.denominator)

    def __mul__(self, other: Union[float, int, "Fraction"]) -> "Fraction":
        if type(other) == float or type(other) == int:
            fraction2 = Fraction(other, 1)
        elif isinstance(other, Fraction):
            fraction2 = other
        return Fraction(
            self.numerator * fraction2.numerator,
            self.denominator * fraction2.denominator,
        )

    def __truediv__(self, other: Union[int, "Fraction"]) -> "Fraction":
        if type(other) == int:
            fraction2 = Fraction(other, 1)
        elif isinstance(other, Fraction):
            fraction2 = other
        return Fraction(
            self.numerator * fraction2.denominator,
            self.denominator * fraction2.numerator,
        )


def collatz(start: int, finish: int) -> Iterable[int]:
    """
    :param start: The starting number of the Collatz sequence.
    :param finish: The number at which the Collatz sequence should finish.
    :return: An iterable of numbers in the Collatz sequence.

    This method generates the Collatz sequence starting from the given start number and continuing until the specified finish number is reached. The Collatz sequence is generated based on the following rules:

    - If the current number is even, divide it by 2.
    - If the current number is odd, multiply it by 3 and add 1.

    The sequence stops when the specified finish number is reached. Numbers in the sequence are yielded one by one as they are generated.

    Example usage:
    >>> for num in collatz(1, 10):
    >>>    print(num)
    Output:
    ```
    1
    4
    2
    ```
    """
    n = start
    yield start
    while n != finish:
        if n % 2 == 0:
            n //= 2
            if n % 6 == 2:
                yield n
        else:  # n % 2 == 1
            n = 3 * n + 1
            if n % 6 == 2:
                yield n


def qollatz(q: int, n: int):  # Generates the constellation in one section of the Collatz Tree
    sequence = [n]
    while True:
        if n % 2 == 0:
            n //= 2
            if n in sequence:
                sequence.append(n)
                return sequence
            if n == 1:
                return sequence
            sequence.append(n)
        else:  # n % 2 == 1
            n = q * n + 1
            if n in sequence:
                sequence.append(n)
                return sequence
            if n == 1:
                return sequence
            sequence.append(n)


@dataclass(kw_only=True, frozen=True)
class Node:
    n1: Fraction
    n2: Fraction
    s1: Fraction
    s2: Fraction


NODES = {
    3: {
        "S": Node(
            n1=Fraction(2, 1),
            n2=Fraction(1, 1),
            s1=Fraction(3, 1),
            s2=Fraction(2, 1),
        ),
        "L": Node(
            n1=Fraction(4, 1),
            n2=Fraction(0, 1),
            s1=Fraction(3, 1),
            s2=Fraction(0, 1),
        ),
        "T": Node(
            n1=Fraction(4, 1),
            n2=Fraction(2, 1),
            s1=Fraction(1, 1),
            s2=Fraction(0, 1),
        ),
    },
    5: {
        "S": Node(
            n1=Fraction(2, 1),
            n2=Fraction(0, 1),
            s1=Fraction(5, 1),
            s2=Fraction(1, 1),
        ),
        "L": Node(
            n1=Fraction(4, 1),
            n2=Fraction(3, 1),
            s1=Fraction(5, 1),
            s2=Fraction(4, 1),
        ),
        "T": Node(
            n1=Fraction(8, 1),
            n2=Fraction(5, 1),
            s1=Fraction(5, 1),
            s2=Fraction(3, 1),
        ),
        "B": Node(
            n1=Fraction(16, 1),
            n2=Fraction(9, 1),
            s1=Fraction(1, 1),
            s2=Fraction(0, 1),
        ),
    },
}


# This is the heart and soul of this code, this gets the diophantine equations
def threading(constellation: str, q: int = 3) -> Tuple[Fraction, Fraction]:
    constant1 = Fraction(1, 1)
    constant2 = Fraction(0, 1)
    nodes = NODES[q]
    for c0, c1 in zip(constellation, constellation[1:]):
        prev_node = nodes[c0]
        current_node = nodes[c1]
        factor1 = prev_node.s1 / current_node.n1
        constant1 = factor1 * constant1
        factor2 = (prev_node.s2 - current_node.n2) / current_node.n1
        constant2 = factor1 * constant2 + factor2
    return constant1, constant2


def threading_gcd(constellation: str, q: int = 3) -> Tuple[Fraction, Fraction, int]:
    constant1, constant2 = threading(constellation, q)
    gcd, x, y = extended_gcd(constant1.denominator * constant2.denominator, constant1.denominator)
    constant1 *= gcd
    constant2 *= gcd
    return constant1, constant2, gcd


# Give it a starting point, a value of b, and a constellation, and it will find the nodes
def get_each_node(
    solution_a0_0: Union[Fraction, int, float],
    solution_a0_1: Union[Fraction, int, float],
    b: Fraction,
    constellation: str,
) -> List[float]:
    nodes = []
    a0 = b * solution_a0_0 + solution_a0_1
    for c0, c1 in zip(constellation, constellation[1:]):
        current_node = NODES[3][c0]
        next_node = NODES[3][c1]
        n = current_node.n1 * a0 + current_node.n2
        nodes.append(float(n) * 6 + 4)
        a0 = (current_node.s1 * a0 + current_node.s2 - next_node.n2) / next_node.n1
    last_node = NODES[3][constellation[-1]]
    n = last_node.n1 * a0 + last_node.n2
    nodes.append(float(n) * 6 + 4)
    return nodes


def find_possible_cyclical_a0(q: int, max_p: int) -> Iterable[Tuple[int, int, int]]:
    for i in range(1, max_p):
        alpha = 2**i
        for j in range(1, max_p):
            beta = q**j
            for y in range(alpha, 1, -1):
                for x in range(beta, 1, -1):
                    b = (x - y) / (alpha - beta)
                    b_int = (x - y) // (alpha - beta)
                    if b != b_int:
                        continue

                    gcd, x2, y2 = extended_gcd(alpha, -beta)
                    gamma = y / (gcd * y2)
                    gamma_int = y // (gcd * y2)
                    if gamma == gamma_int:
                        yield alpha, beta, gamma_int


def generate_cyclical_constellations(length: int, q: int) -> Iterable[str]:
    tiles = {
        3: "STL",
        5: "STLB",
    }[q]
    return (
        "".join(constellation)
        for constellation in itertools.product(tiles, repeat=length)
        if constellation[0] == constellation[-1]
    )
