import super_awesome_library as SAL

q = 3
maxP = 8
findings = SAL.findPossibleCyclicalA0(q, maxP)
possibleCycles = []
for i in range(1, 8):
    print(possibleCycles)
    print(SAL.generateCyclicalConstellations(i, q))
    possibleCycles.append(SAL.generateCyclicalConstellations(i, q))
    print(possibleCycles)

for constellation in possibleCycles:
    equation = SAL.Threading(constellation, q)
    if equation in findings:
        print(constellation)
        print(equation)
        print(findings)
