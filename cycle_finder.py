import super_awesome_library as sal

q = 3
maxP = 8
findings = sal.find_possible_cyclical_a0(q, maxP)
possible_cycles = []
for i in range(1, 8):
    print(possible_cycles)
    print(sal.generate_cyclical_constellations(i, q))
    possible_cycles.append(sal.generate_cyclical_constellations(i, q))
    print(possible_cycles)

for constellation in possible_cycles:
    equation = sal.threading(constellation, q)
    if equation in findings:
        print(constellation)
        print(equation)
        print(findings)
