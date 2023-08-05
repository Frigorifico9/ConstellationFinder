from typing import Tuple

from super_awesome_library import (
    NODES,
    Fraction,
    extended_gcd,
    get_each_node,
    threading_gcd,
)


# Give it the coefficients for the constellation and it will find it somewhere
def get_nodes(solutions_a_0, solutions_a_n, constellation: str, b) -> Tuple[Fraction, Fraction]:
    first_node = NODES[3][constellation[0]]
    last_node = NODES[3][constellation[-1]]
    a_0 = solutions_a_0[0] * b + solutions_a_0[1]
    a_n = solutions_a_n[0] * b + solutions_a_n[1]
    n1 = first_node.n1 * a_0 + first_node.n2
    n2 = last_node.s1 * a_n + last_node.s2
    return 6 * n1 + 4, 6 * n2 + 4


def main():
    # I tested with many constellations and many values of b

    # constellation = 'SLS'
    # constellation = 'SLSSSSLLSLSSLSSSLTSSSLSLSSSSSTSSSSTLLLTLTSSSTTSTL'
    # constellation = 'LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL'
    constellation = "SSSLLLTS"
    # constellation = 'SSSLLL'
    # b= Fraction(-7459848397017429,144115188075855872)
    # b=Fraction(-14919696794034863,288230376151711744)
    # b = Fraction(1,29)
    # b=Fraction(6,2**20)
    # constellation = ''
    # constellation = 'SSSLSSTLS'
    # constellation = 'SS'
    b = Fraction(0, 1)
    constant1, constant2, constant3 = threading_gcd(constellation)
    gcd, x, y = extended_gcd(constant3.numerator, -constant1.numerator)

    # We take the modulo to 'slide' the solutions so that if b<0 everything is negative too
    a0_0 = constant3.numerator
    a0_1 = (gcd * y * constant2.numerator) % constant3.numerator
    an = [constant1.numerator, (gcd * x * constant2.numerator) % constant1.numerator]

    print(
        f"The equation for the constellation {constellation} is {int(constant3)}*a_n"
        f" = {int(constant1)} * a_0 + {int(constant2)}"
    )

    print(f"The solutions are: a_0 = {a0_0} * b + {a0_1}, a_n = {an[0]} * b + {an[1]}")

    print(
        f"Finally, using b = {str(b)} we find that one example of this constellation is:"
        f" {get_each_node(a0_0, a0_1, b, constellation)}"
    )


if __name__ == "__main__":
    main()
