import numpy as np
from matplotlib import pyplot as plt
import superAwesomeLibrary as sa

maxQ = 1000
maxN = 100
maxStep = 100
img = []
for i in range(0,maxQ):
    q = 2 * i + 1
    steps = []
    for n in range(-100,maxN):
        step = sa.QollatzF(q,n,maxStep)
        #if step < maxStep and n > 0:
            #print('q = ' + str(q))
            #print('n = ' + str(n))
            #print('step = '+str(step))
        steps.append(step)
    img.append(steps)

imgNP = np.array(img,int)

plt.imshow(imgNP,interpolation='none')
plt.xlabel('N')
plt.ylabel('Q')
plt.show()
