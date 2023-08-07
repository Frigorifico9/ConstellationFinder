from super_awesome_library import extended_gcd


def main():
    max_p = 20
    q = 3
    found_ns = set()

    for i in range(0, max_p):
        beta = q**i
        for j in range(i, max_p):
            alpha = 2**j
            for y1 in range(alpha, 1, -1):
                for x1 in range(beta, 1, -1):
                    if (x1 - y1) % (alpha - beta) != 0:
                        continue

                    b1 = (x1 - y1) // (alpha - beta)
                    a0 = alpha * b1 + y1
                    an = beta * b1 + x1
                    gamma = alpha * an - beta * a0
                    gcd, x2, y2 = extended_gcd(alpha, -beta)
                    x3 = (gcd * x2 * gamma) % beta
                    y3 = (gcd * y2 * gamma) % alpha
                    if x3 != x1 or y3 != y1:
                        continue

                    n1 = 6 * (2 * a0 + 1) + 4
                    n2 = 6 * (4 * a0) + 4
                    n3 = 6 * (4 * a0 + 2) + 4
                    if n1 in found_ns or n2 in found_ns or n3 in found_ns:
                        continue

                    found_ns.add(6 * (2 * a0 + 1) + 4)
                    found_ns.add(6 * (4 * a0) + 4)
                    found_ns.add(6 * (4 * a0 + 2) + 4)
                    print(f"{alpha} * an = {beta} * a0 + {gamma}")
                    print(f"a0 = {alpha} * b + {y1}")
                    print(f"an = {beta} * b + {x1}")
                    print(f"b = {b1}")
                    print(6 * (2 * a0 + 1) + 4)
                    print(6 * (4 * a0) + 4)
                    print(6 * (4 * a0 + 2) + 4)


if __name__ == "__main__":
    main()
