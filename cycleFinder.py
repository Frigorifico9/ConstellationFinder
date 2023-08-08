import superAwesomeLibrary as SAL

q=3
maxP = 8
findings = SAL.findPossibleCyclicalA0(q,maxP)
possibleCycles =[]
for i in range(1,8):
    print("possibleCycles")
    print(possibleCycles)
    print("SAL.generateCyclicalConstellations(i, q)")
    print(SAL.generateCyclicalConstellations(i, q))
    possibleCycles += SAL.generateCyclicalConstellations(i, q)
print("possibleCycles")
print(possibleCycles)

findcount=0
for constellation in possibleCycles:
    equation=SAL.Threading(constellation,q)
    if equation in findings:
        findcount+=1
        print("constellation")
        print(constellation)
        print("equation")
        print(equation)
        print("findings")
        print(findings)

print("findcount %i" %findcount)

