import numpy as np
import matplotlib.pyplot as plt

def payloadrange_diagram(points,x):

    section_AB = [points[0][0],points[1][0],points[0][1],points[1][1]]
    section_BC = [points[1][0],points[2][0],points[1][1],points[2][1]]
    section_CD = [points[2][0],points[3][0],points[2][1],points[3][1]]
    
    if x >= points[0][0] and x <= points[1][0]:
        payload = points[0][1]
    elif x >= points[1][0] and x <= points[2][0]:
        m = (section_BC[3]-section_BC[2])/(section_BC[1]-section_BC[0])
        y = m*(x-section_BC[0])+section_BC[2]
        payload = y
    elif x >= points[2][0] and x <= points[3][0]:
        m = (section_CD[3]-section_CD[2])/(section_CD[1]-section_CD[0])
        y = m*(x-section_CD[0])+section_CD[2]
        payload = y

    return payload


# range = np.linspace(0,800,10000)
# points = [(0,36000),(200,36000),(600,25000),(800,0)]
# payload = [payloadrange_diagram(points, x) for x in range]
# plt.plot(range,payload)
# plt.grid()
# plt.show()

