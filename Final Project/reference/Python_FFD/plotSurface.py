from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

import solidBoundaryPoint
import FFDPointElement

CONST_DATAFILE = "CRMPointData.txt"
CONST_nXFDD = 10
CONST_nYFDD = 3
CONST_nZFDD = 5


def plotFiguresTemp(xSolid, ySolid, zSolid, xFFDDeform, yFFDDeform, zFFDDeform):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #fig = plt.figure()
    #ax = fig.gca(projection='3d')

    # Axes3D.plot_wireframe(ax, z, x, y)
    ax.set_xlabel('Z axis')
    ax.set_ylabel('X axis')
    ax.set_zlabel('Y axis')

    #ax.plot_trisurf(zSolid, xSolid, ySolid, cmap=cm.jet, linewidth=0.2)
    ax.plot_wireframe(zSolid, xSolid, ySolid, rstride = 1, cstride = 1, color="y")

    #Axes3D.scatter(ax, zSolid, xSolid, ySolid, s=10, c='b')
    Axes3D.scatter(ax, zFFDDeform, xFFDDeform, yFFDDeform, s=30, c='r')

    # Axes3D.set_ylim(ax, [-0.5,4.5])
    # Axes3D.set_xlim(ax, [-0.5,4.5])
    Axes3D.set_zlim(ax, [-0.7, 0.7])




    plt.show(block=True)


#For reading the data into the data structures from the file
def initializeDataFromFile(solidBoundaryPointArray, FFDPointArray):
    fileData = open(CONST_DATAFILE, "r")

    # first read the FFD point data
    lineFFD = fileData.readline()
    while(True):

        #read the IJK data line
        lineIJK = fileData.readline()

        #if all the FFD point data has been read already
        if(lineIJK == "Solid Boundary Point Data\n"):
            break

            #otherwise, there are now two lines of FFD data to read. Read the second line too
        lineXYZ = fileData.readline()

        #parse the IJK data line
        I = 0
        J = 0
        K = 0
        for i in range(3):
            Comma = lineIJK.find(",")
            if (Comma == -1):
                # on last number
                Num = lineIJK[0: len(lineIJK)]
                K = int(Num)
                break

            Num = lineIJK[0:Comma]
            lineIJK = lineIJK[Comma + 1:len(lineIJK)]

            if (i == 0):
                I = int(Num)
            elif (i == 1):
                J = int(Num)

        #parse the XYZ line
        X = 0.0
        Y = 0.0
        Z = 0.0
        for i in range(3):
            Comma = lineXYZ.find(",")
            if (Comma == -1):
                # on last number
                Num = lineXYZ[0: len(lineXYZ)]
                Z = float(Num)
                break

            Num = lineXYZ[0:Comma]
            lineXYZ = lineXYZ[Comma + 1:len(lineXYZ)]

            if (i == 0):
                X = float(Num)
            elif (i == 1):
                Y = float(Num)

        #create an FFD point element and store the data in the object. place the object in the FFD Point list
        FFDElement = FFDPointElement.FFDPointElement(X,Y,Z)
        FFDPointArray[I][J][K] = FFDElement


    #Now read the solid boundary point data
    while(True):
        lineXYZSolid = fileData.readline()
        #the end of the solid boundary point data, and the file, has been reached
        if(lineXYZSolid == ""):
            break

        #Loop didn't break so there is more data to read
            #read the T,U,V line
        lineTUVSolid = fileData.readline()

        # parse the XYZ line
        Xsolid = 0.0
        Ysolid = 0.0
        Zsolid = 0.0
        for i in range(3):
            Comma = lineXYZSolid.find(",")
            if (Comma == -1):
                # on last number
                Num = lineXYZSolid[0: len(lineXYZSolid)]
                Zsolid = float(Num)
                break

            Num = lineXYZSolid[0:Comma]
            lineXYZSolid = lineXYZSolid[Comma + 1:len(lineXYZSolid)]

            if (i == 0):
                Xsolid = float(Num)
            elif (i == 1):
                Ysolid = float(Num)

        #parse the TUV line
        T = 0.0
        U = 0.0
        V = 0.0
        for i in range(3):
            Comma = lineTUVSolid.find(",")
            if (Comma == -1):
                # on last number
                Num = lineTUVSolid[0: len(lineTUVSolid)]
                V = float(Num)
                break

            Num = lineTUVSolid[0:Comma]
            lineTUVSolid = lineTUVSolid[Comma + 1:len(lineTUVSolid)]

            if (i == 0):
                T = float(Num)
            elif (i == 1):
                U = float(Num)

        #create the solidBoundaryPoint element and store the data into the object. Then add the object to the
        # solidBoundaryPoint array
        solidBndElement = solidBoundaryPoint.solidBoundaryPoint(Xsolid,Ysolid,Zsolid)
        solidBndElement.setT(T)
        solidBndElement.setU(U)
        solidBndElement.setV(V)

        solidBoundaryPointArray.append(solidBndElement)

    fileData.close()

def fillInitialArrays(solidBoundaryPointArray, FFDPointArray, xsolidInitial,
                      ysolidInitial, zsolidInitial, xFFDInitial, yFFDInitial, zFFDInitial):
    # filling the object's solid point arrays
    for element in solidBoundaryPointArray:
        xsolidInitial.append(element.getX())
        ysolidInitial.append(element.getY())
        zsolidInitial.append(element.getZ())

    # filling the FFD arrays
    for i in range(CONST_nXFDD):
        for j in range(CONST_nYFDD):
            for k in range(CONST_nZFDD):
                element = FFDPointArray[i][j][k]
                xFFDInitial.append(element.getX())
                yFFDInitial.append(element.getY())
                zFFDInitial.append(element.getZ())




#Main:

#The lists that will hold the solid boundary point and FFD point objects
solidBoundaryPointArray = []
FFDPointArray = []
for i in range(CONST_nXFDD):
    rowj = []
    for j in range(CONST_nYFDD):
        rowk = []
        for k in range(CONST_nZFDD):
            rowk.append(FFDPointElement.FFDPointElement(0,0,0))
        rowj.append(rowk)
    FFDPointArray.append(rowj)

#create arrays that will hold the initial object's solid points and the initial FFD points
# For the initial solid boundary points
xsolidInitial = []
ysolidInitial = []
zsolidInitial = []

# For the initial FFD Points
xFFDInitial = []
yFFDInitial = []
zFFDInitial = []

initializeDataFromFile(solidBoundaryPointArray, FFDPointArray)

solidBoundaryPointArray.sort(key=lambda x: x.getZ(), reverse=True)

fillInitialArrays(solidBoundaryPointArray, FFDPointArray, xsolidInitial,
                  ysolidInitial, zsolidInitial, xFFDInitial, yFFDInitial, zFFDInitial)

print xsolidInitial
print ysolidInitial
print zsolidInitial




plotFiguresTemp(xsolidInitial, ysolidInitial, zsolidInitial, xFFDInitial, yFFDInitial, zFFDInitial)