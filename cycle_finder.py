from super_awesome_library import (
    find_possible_cyclical_a0,
    generate_cyclical_constellations,
    threading_gcd,
)


def main():
    q = 3
    max_p = 8
    findings = list(find_possible_cyclical_a0(q, max_p))
    possible_cycles = []
    for i in range(1, 8):
        print(possible_cycles)
        constellations = list(generate_cyclical_constellations(i, q))
        print(constellations)
        possible_cycles.extend(constellations)
        print(possible_cycles)

    for constellation in possible_cycles:
        equation = threading_gcd(constellation, q)
        if equation in findings:
            print(constellation)
            print(equation)
            print(findings)


if __name__ == "__main__":
    main()
