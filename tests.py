def extended_gcd(a, b):  # Helps us reduce fractions
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1

    return gcd, x, y


findings = []
maxP = 20
q = 3
foundNs = []

for i in range(0, maxP):
    beta = q**i
    for j in range(i, maxP):
        alpha = 2**j
        for Y1 in range(alpha, 1, -1):
            for X1 in range(beta, 1, -1):
                if (X1 - Y1) % (alpha - beta) == 0:
                    b1 = (X1 - Y1) // (alpha - beta)
                    a0 = alpha * b1 + Y1
                    an = beta * b1 + X1
                    gamma = alpha * an - beta * a0
                    gcd, X2, Y2 = extended_gcd(alpha, -beta)
                    X3 = (gcd * X2 * gamma) % beta
                    Y3 = (gcd * Y2 * gamma) % alpha
                    if X3 == X1 and Y3 == Y1:
                        n1 = 6 * (2 * a0 + 1) + 4
                        n2 = 6 * (4 * a0) + 4
                        n3 = 6 * (4 * a0 + 2) + 4
                        if n1 not in foundNs and n2 not in foundNs and n3 not in foundNs:
                            foundNs.append(6 * (2 * a0 + 1) + 4)
                            foundNs.append(6 * (4 * a0) + 4)
                            foundNs.append(6 * (4 * a0 + 2) + 4)
                            print(str(alpha) + " * an = " + str(beta) + " * a0 + " + str(gamma))
                            print("a0 = " + str(alpha) + " * b + " + str(Y1))
                            print("an = " + str(beta) + " * b + " + str(X1))
                            print("b = " + str(b1))
                            print(6 * (2 * a0 + 1) + 4)
                            print(6 * (4 * a0) + 4)
                            print(6 * (4 * a0 + 2) + 4)
