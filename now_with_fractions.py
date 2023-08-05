from super_awesome_library import Fraction, get_each_node, threading


# We find the first solution by brute force, I'm sorry
def find_first_solution(constant1: Fraction, constant2: Fraction):
    for n in range(2**63):
        k = constant1 * n + constant2
        if int(k) == float(k):
            return int(k), n


def main():
    constellation = "SSSLSSTTTT"
    b = Fraction(0, 1)
    constant1, constant2 = threading(constellation)
    # gcd, x0, y0 = extended_gcd(constant1.denominator, -constant1.numerator)
    # Solutions_a0 = [Fraction(-constant1.denominator/gcd,1),(constant2*y0*gcdSign)]
    # Solutions_an = [Fraction(-constant1.numerator/gcd,1),(constant2*x0*gcdSign)]
    k, n = find_first_solution(constant1, constant2)
    solution_a0_0 = Fraction(constant1.denominator, 1)
    solution_a0_1 = Fraction(n, 1)
    solutions_an = [Fraction(constant1.numerator, 1), Fraction(k, 1)]

    print(f"The equation for the constellation {constellation} is a_n = {constant1} * a_0 + {constant2}")

    print(
        f"The solutions are: a_0 = {solution_a0_0} * b + {solution_a0_1},"
        f" a_n = {solutions_an[0]} * b + {solutions_an[1]}"
    )

    print(
        f"Finally, using b = {b} we find that one example of this constellation is:"
        f" {get_each_node(solution_a0_0, solution_a0_1, b, constellation)}"
    )


if __name__ == "__main__":
    main()
