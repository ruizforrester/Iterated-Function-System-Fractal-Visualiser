from matplotlib.figure import Figure
import numpy as np
import random as random

def algDeterminista(sfi, num_iter, color, firstPoints):
    finalPoints = firstPoints
    fig = Figure()
    ax = fig.add_subplot()
    for i in range(num_iter):
        tempPoints = np.array([])
        for j in sfi:
            for k in finalPoints:
                newPoints = np.array([j[0]*k[0]+j[1]*k[1]+j[4], j[2]*k[0]+j[3]*k[1]+j[5]])
                tempPoints = np.append(tempPoints, newPoints)
        finalPoints = tempPoints.reshape(-1,2)

    x = finalPoints[:,0].reshape(-1,len(firstPoints))
    y = finalPoints[:,1].reshape(-1,len(firstPoints))
    for i in range(len(x)):
        ax.fill(x[i], y[i], color)
    ax.set_aspect('equal', adjustable='box')
    return fig

def algAleatorio(probSfi, sfi, num_iter, color):
    x = np.array([1,1])
    finalPoints = np.array([])
    if len(sfi) != 0: #Si se ha dado una lista de funciones no vacia
        if probSfi is None: #Calculamos las probabilidades si no se han dado
            probSfi = np.zeros(len(sfi))
            sumatorio = abs(sfi[:,0]*sfi[:,3]-sfi[:,1]*sfi[:,2]).sum()
            if sumatorio != 0:
                hayCero = False
                for i in range(len(sfi)):
                    probSfi[i] = abs(sfi[i][0]*sfi[i][3]-sfi[i][1]*sfi[i][2])/abs(sumatorio)
                    if probSfi[i] == 0:
                        probSfi[i] = 0.001
                        hayCero = True
                if hayCero:
                    probSfi[np.argmax(probSfi)] = probSfi[np.argmax(probSfi)] - 0.001
            else:
                probSfi = np.ones(len(sfi))/len(sfi)
        
        for i in range(num_iter):
            #Esta linea escoge una función aleatoria del sfi según las probabilidades dadas
            randFunc = sfi[np.random.choice(len(sfi), p=probSfi)]
            y = np.array([randFunc[0]*x[0]+randFunc[1]*x[1]+randFunc[4], 
                                    randFunc[2]*x[0]+randFunc[3]*x[1]+randFunc[5]])
            x = y
            if i > 50:
                finalPoints = np.append(finalPoints, x)
        finalPoints = finalPoints.reshape(-1,2)
    else:
        finalPoints = np.array([x])
    fig = Figure()
    ax = fig.add_subplot()
    x_values = finalPoints[:,0]
    y_values = finalPoints[:,1]
    x_min = x_values.min()
    x_max = x_values.max()
    y_min = y_values.min()
    y_max = y_values.max()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    ax.plot(x_values, y_values, marker=',', markerfacecolor=color, 
             markeredgecolor=color, linestyle='None', scalex=False, scaley=False)
    ax.set_aspect('equal', adjustable='box')
    return fig