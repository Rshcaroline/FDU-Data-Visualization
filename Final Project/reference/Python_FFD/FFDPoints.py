#scp manmeetb@guillimin.hpc.mcgill.ca:/sb/project/rck-371-aa/Manmeet/syn3d/cases-controlfiles/inviscid/naca0012wing/planePoints.txt /Users/manmeetbhabra/Desktop



import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import attachffd
import solidBoundaryPoint
import FFDPointElement
import NewtonSolver
import math

CONST_FileName = "planePointsCRM.txt"
CONST_FFD = "FFDPointsCRM.txt"
CONST_DATAFILE = "CRMPointData.txt"
CONST_FFDXMin = 0.00001
CONST_FFDXMax = 1.000001
CONST_FFDYMin = -0.060001
CONST_FFDYMax = 0.060001
CONST_FFDZMin = -0.0001
CONST_FFDZMax = 3.06001

CONST_nXFDD = 10
CONST_nYFDD = 3
CONST_nZFDD = 5

CONST_xEpsilon = 0.025
CONST_yEpsilon = 0.025

GLOBAL_zCrossSectionObjects = {}


class zCrossSectionData(object):

    def __init__(self, xValue, yValue, zValue):
        self.z = zValue
        self.xMax = xValue
        self.xMin = xValue
        self.yMax = yValue
        self.yMin = yValue

    #The getters
    def getXMax(self):
        return self.xMax

    def getXMin(self):
        return self.xMin

    def getYMax(self):
        return self.yMax

    def getYMin(self):
        return self.yMin

    #The setters
    def setXMax(self, xMax):
        self.xMax = xMax

    def setXMin(self, xMin):
        self.xMin = xMin

    def setYMax(self, yMax):
        self.yMax = yMax

    def setYMin(self, yMin):
        self.yMin = yMin



def plotFiguresTemp(xSolid, ySolid, zSolid, xFFDDeform, yFFDDeform, zFFDDeform):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Axes3D.plot_wireframe(ax, z, x, y)
    ax.set_xlabel('Z axis')
    ax.set_ylabel('X axis')
    ax.set_zlabel('Y axis')

    Axes3D.scatter(ax, zSolid, xSolid, ySolid, s=10, c='b')
    Axes3D.scatter(ax, zFFDDeform, xFFDDeform, yFFDDeform, s=30, c='r')

    # Axes3D.set_ylim(ax, [-0.5,4.5])
    # Axes3D.set_xlim(ax, [-0.5,4.5])
    Axes3D.set_zlim(ax, [-0.7, 0.7])

    plt.show(block=True)




def printFFDAndSolidBndData(FFDPointArray, solidBoundaryPointArray):
    print("FFD: ")
    for i in range(CONST_nXFDD):
        for j in range(CONST_nYFDD):
            for k in range(CONST_nZFDD):
                element = FFDPointArray[i][j][k]
                print("i,j,k: " + str(i) + ", " + str(j) + ", " + str(k))
                print("x,y,z: " + str(element.getX()) + ", " + str(element.getY()) + ", " + str(element.getZ()))

    print("solid boundary point data: ")
    printTUVData(solidBoundaryPointArray)

def printTUVData(solidBoundaryPointArray):
    # Iterate through all the solid boundary points and print out the T, U, V and the coordinate data
    for i in range(len(solidBoundaryPointArray)):
        elementi = solidBoundaryPointArray[i]
        print("i + 1: " + str(i + 1))
        print("T, U, V: " + str(elementi.getT()) + "  " + str(elementi.getU()) + "  " + str(elementi.getV()))
        print("x, y ,z: " + str(elementi.getX()) + "  " + str(elementi.getY()) + "  " + str(elementi.getZ()))

def plotFFDandSolidBNDAndInitialFFDandSolidBND(FFDPointArray, solidBoundaryPointArray, xsolidInitial,
                                               ysolidInitial, zsolidInitial, xFFDInitial, yFFDInitial, zFFDInitial):
    # Set up the data structures
    xsolid = []
    ysolid = []
    zsolid = []

    # For the FFD Points
    xFFD = []
    yFFD = []
    zFFD = []

    #filling the object's solid point arrays
    for element in solidBoundaryPointArray:
        xsolid.append(element.getX())
        ysolid.append(element.getY())
        zsolid.append(element.getZ())

    # filling the FFD arrays
    for i in range(CONST_nXFDD):
        for j in range(CONST_nYFDD):
            for k in range(CONST_nZFDD):
                element = FFDPointArray[i][j][k]
                xFFD.append(element.getX())
                yFFD.append(element.getY())
                zFFD.append(element.getZ())

    plotFigures(xsolid, ysolid, zsolid, xFFD, yFFD, zFFD, xsolidInitial,
               ysolidInitial, zsolidInitial, xFFDInitial, yFFDInitial, zFFDInitial)


def plotFigures(xSolid,ySolid,zSolid,xFFDDeform,yFFDDeform,zFFDDeform, xsolidInitial,
               ysolidInitial, zsolidInitial, xFFDInitial, yFFDInitial, zFFDInitial):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    # Axes3D.plot_wireframe(ax, z, x, y)
    ax.set_xlabel('Z axis')
    ax.set_ylabel('X axis')
    ax.set_zlabel('Y axis')

    #Axes3D.scatter(ax, zSolid, xSolid, ySolid, s=10, c='b')
    Axes3D.plot_wireframe(ax, zSolid, xSolid, ySolid, rstride = 1, cstride = 1, color="b")
    Axes3D.scatter(ax, zFFDDeform, xFFDDeform, yFFDDeform, s=30, c='r')

    #Axes3D.scatter(ax, zsolidInitial, xsolidInitial, ysolidInitial, s=10, c='y')
    Axes3D.plot_wireframe(ax, zsolidInitial, xsolidInitial, ysolidInitial,rstride = 1, cstride = 1, color="y")
    Axes3D.scatter(ax, zFFDInitial, xFFDInitial, yFFDInitial, s=30, c='g')

    xZCross = []
    yZCross = []
    zZCross = []

    #plot the points for the limits of each cross section
    for zCrossSect in GLOBAL_zCrossSectionObjects:
        zCrossSectionObject = GLOBAL_zCrossSectionObjects[zCrossSect]

        #add to the arrays, for a fixed z, the following combinations
        # (xmax, ymax) (xmax, ymin) (xmin, ymin) (xmin, ymax)

        # (xmax, ymax)
        xZCross.append(zCrossSectionObject.getXMax())
        yZCross.append(zCrossSectionObject.getYMax())
        zZCross.append(zCrossSect)

        #(xmax, ymin)
        xZCross.append(zCrossSectionObject.getXMax())
        yZCross.append(zCrossSectionObject.getYMin())
        zZCross.append(zCrossSect)

        #(xmin, ymin)
        xZCross.append(zCrossSectionObject.getXMin())
        yZCross.append(zCrossSectionObject.getYMin())
        zZCross.append(zCrossSect)

        #(xmin, ymax)
        xZCross.append(zCrossSectionObject.getXMin())
        yZCross.append(zCrossSectionObject.getYMax())
        zZCross.append(zCrossSect)

    #Axes3D.plot_wireframe(ax, zZCross, xZCross, yZCross)



    #Axes3D.set_ylim(ax, [-0.5,4.5])
    #Axes3D.set_xlim(ax, [-0.5,4.5])
    Axes3D.set_zlim(ax, [-0.7, 0.7])

    plt.show(block=True)

#creates the lattice of FFD points
def createFFDMesh(FFDPointArray):
    FFDdx = (CONST_FFDXMax-CONST_FFDXMin)/(CONST_nXFDD-1)
    FFDdy = (CONST_FFDYMax - CONST_FFDYMin) / (CONST_nYFDD - 1)
    FFDdz = (CONST_FFDZMax - CONST_FFDZMin) / (CONST_nZFDD - 1)

    for i in range(CONST_nXFDD):
        for j in range(CONST_nYFDD):
            for k in range(CONST_nZFDD):
                #print "CREATE i,j,k: " + str(i) + " " + str(j) + " " + str(k)

                FFDelement = FFDPointElement.FFDPointElement(CONST_FFDXMin+ FFDdx*i, CONST_FFDYMin+ FFDdy*j, CONST_FFDZMin + FFDdz*k)
                FFDPointArray[i][j][k] = FFDelement

                #print str(FFDelement.getX()) + ", " + str(FFDelement.getY()) + ", " + str(FFDelement.getZ())


#reads the points from the solid boundary point file and also creates a rectangular mesh
def initializeData(x,y,z, solidBoundaryPointArray):
    solidBoundaryPointSize, XMax, XMin, YMax, YMin, ZMax, ZMin = readData(x, y, z)

    #print "solidBoundaryPointSize: " + str(solidBoundaryPointSize)
    #print "FFDPointsSize: " + str(FFDPointsSize)

    #create a solidBoundaryPoint element for each point
    for i in range(solidBoundaryPointSize):
        bndelement = solidBoundaryPoint.solidBoundaryPoint(x[i],y[i],z[i])
        solidBoundaryPointArray.append(bndelement)

    return (XMax, XMin, YMax, YMin, ZMax, ZMin)


def isIncludedZCrossSection(z):

    #iterate through all the keys for the zCrossSections dictionary.
    #Then, divide each key by the given z value and if the resulting
    #number is within some epsilon of 1, then we'll say that the number
    #is included in the dictionary

    for key in GLOBAL_zCrossSectionObjects.keys():
        if(key==0 and z ==0):
            return key
        else:
            num = key/z
            if(num<1.05 and num >0.95):
                return key

    return None


# x,y,z are for the solid boundary points
def readData(x,y,z):

    # read from the file
    file = open(CONST_FileName, 'r')
    solidBoundaryPointCounter = 0
    XMax=0
    XMin=0
    YMax=0
    YMin=0
    ZMax=0
    ZMin=0

    for line in file:
        Num1 = 0.0
        Num2 = 0.0
        Num3 = 0.0
        lastComma = 0
        for i in range(3):
            # print "i: " + str(i)
            Comma = line.find(",")
            # print "Comma: " + str(Comma)
            if (Comma == -1):
                # on last number
                Num = line[0: len(line)]
                Num3 = float(Num)
                # print "Num: " + Num
                break

            Num = line[0:Comma]
            # print "Num: " + Num
            line = line[Comma + 1:len(line)]
            # print line

            if (i == 0):
                Num1 = float(Num)
            elif (i == 1):
                Num2 = float(Num)

        if(solidBoundaryPointCounter==0):
            XMax = Num1
            XMin = Num1
            YMax = Num2
            YMin = Num2
            ZMax = Num3
            ZMin = Num3
        else:
            if (Num1 > XMax):
                XMax = Num1
            if (Num1 < XMin):
                XMin = Num1
            if (Num2 > YMax):
                YMax = Num2
            if (Num2 < YMin):
                YMin = Num2
            if (Num3 > ZMax):
                ZMax = Num3
            if (Num3 < ZMin):
                ZMin = Num3
        x.append(Num1)
        y.append(Num2)
        z.append(Num3)

        if(Num3<0.0001):
            zCrossSectionValue = 0
        else:
            zCrossSectionValue = Num3

        keyInDictionary = isIncludedZCrossSection(zCrossSectionValue)
        #add information about constant z cross sections
        if(keyInDictionary != None):
            # if True, then add information about the number
            # to the value that the key points to in the dictionary
            zCrossSectionObject = GLOBAL_zCrossSectionObjects[keyInDictionary]
            if(Num1 > zCrossSectionObject.getXMax()):
                zCrossSectionObject.setXMax(Num1)
            if(Num1 < zCrossSectionObject.getXMin()):
                zCrossSectionObject.setXMin(Num1)
            if(Num2 > zCrossSectionObject.getYMax()):
                zCrossSectionObject.setYMax(Num2)
            if(Num2 < zCrossSectionObject.getYMin()):
                zCrossSectionObject.setYMin(Num2)

        else:
            #if the key isn't in the dictionary, then add it
            newZCrossSectionObject = zCrossSectionData(Num1, Num2, zCrossSectionValue)

            GLOBAL_zCrossSectionObjects[zCrossSectionValue] = newZCrossSectionObject


        solidBoundaryPointCounter+=1



    file.close()
        # Return a tuple containing the number of boundary points and the number of FFD Points
    return (solidBoundaryPointCounter, XMax, XMin, YMax, YMin, ZMax, ZMin)

"""
    # read from the file
    file = open(CONST_FFD, 'r')
    FFDPointCounter = 0
    GLOBAL_FFDXMax = 0
    GLOBAL_FFDXMin = 0
    GLOBAL_FFDYMax = 0
    GLOBAL_FFDYMin = 0
    GLOBAL_FFDZMax = 0
    GLOBAL_FFDZMin = 0
    for line in file:
        Num1 = 0.0
        Num2 = 0.0
        Num3 = 0.0
        lastComma = 0
        for i in range(3):
            # print "i: " + str(i)
            Comma = line.find(",")
            # print "Comma: " + str(Comma)
            if (Comma == -1):
                # on last number
                Num = line[0: len(line)]
                Num3 = float(Num)
                # print "Num: " + Num
                break

            Num = line[0:Comma]
            # print "Num: " + Num
            line = line[Comma + 1:len(line)]
            # print line

            if (i == 0):
                Num1 = float(Num)
            elif (i == 1):
                Num2 = float(Num)

        #Keep track of the FFD Box limits
        if(FFDPointCounter==0):

            GLOBAL_FFDXMax = Num1
            GLOBAL_FFDXMin = Num1
            GLOBAL_FFDYMax = Num2
            GLOBAL_FFDYMin = Num2
            GLOBAL_FFDZMax = Num3
            GLOBAL_FFDZMin = Num3
        else:
            if (Num1>GLOBAL_FFDXMax):
                GLOBAL_FFDXMax = Num1
            if (Num1<GLOBAL_FFDXMin):
                GLOBAL_FFDXMin = Num1
            if (Num2>GLOBAL_FFDYMax):
                GLOBAL_FFDYMax = Num2
            if (Num2<GLOBAL_FFDYMin):
                GLOBAL_FFDYMin = Num2
            if (Num3 > GLOBAL_FFDZMax):
                GLOBAL_FFDZMax = Num3
            if (Num3 < GLOBAL_FFDZMin):
                GLOBAL_FFDZMin = Num3

        x1.append(Num1)
        y1.append(Num2)
        z1.append(Num3)
        FFDPointCounter +=1
"""




def B(i,n,t):
    return (math.factorial(n)/(math.factorial(i)*math.factorial(n-i)))*((1-t)**(n-i))*(t**i)


#Gamma is given by the following expression
#sum(i=0 to n) sum(j=0 to m) sum(k=0 to l) [B(i,n,t)*B(j,m,u)*B(k,l,v)*Pijk]
#the X vector has the following components: X[t,u,v]
def Gamma(X):
    t = X[0]
    u = X[1]
    v = X[2]

    sum = [0,0,0]

    # do a sum from i=0 to n, where n is the number of spaces between FFD points (so if there are n xFFD points then
    # there are n-1 spaces).
    n = CONST_nXFDD-1
    m = CONST_nYFDD-1
    l = CONST_nZFDD-1

    for i in range(CONST_nXFDD):
        for j in range(CONST_nYFDD):
            for k in range(CONST_nZFDD):
                #so now we have the Pijk element (i,j,k are all from 0 to n, (there are n+1 points))
                sum[0] = sum[0] + B(i,n,t)*B(j,m,u)*B(k,l,v)*FFDPointArray[i][j][k].getX()
                sum[1] = sum[1] + B(i, n, t) * B(j, m, u) * B(k, l, v) * FFDPointArray[i][j][k].getY()
                sum[2] = sum[2] + B(i, n, t) * B(j, m, u) * B(k, l, v) * FFDPointArray[i][j][k].getZ()

    return sum

def AttachFFDNewton(SolidBoundaryPointArray):
    for i in range(len(solidBoundaryPointArray)):
        print("Attach FFD i: " + str(i))
        element = SolidBoundaryPointArray[i]

        xElem = element.getX()
        yElem = element.getY()
        zElem = element.getZ()

        #capture the xElem, yElem and zElem values (these change in the loop so capture these
        #values for what they are when the lambda function is created)
        testFunction_1 = (lambda X, xElem = xElem: xElem - Gamma(X)[0])
        testFunction_2 = (lambda X, yElem = yElem: yElem - Gamma(X)[1])
        testFunction_3 = (lambda X, zElem = zElem: zElem - Gamma(X)[2])

        testFunctionArray = [testFunction_1, testFunction_2, testFunction_3]
        AnswerArray = NewtonSolver.NewtonSolve(3, [0.5, 0.5, 0.5], testFunctionArray)
        element.setT(AnswerArray[0])
        element.setU(AnswerArray[1])
        element.setV(AnswerArray[2])


def createFFDPointsFixedCrossSections(FFDPointArray, zvalue, k):
    zCrossSectionObject = GLOBAL_zCrossSectionObjects[zvalue]
    xMax = zCrossSectionObject.getXMax()
    xMin = zCrossSectionObject.getXMin()
    yMax = zCrossSectionObject.getYMax()
    yMin = zCrossSectionObject.getYMin()

    FFDdx = (xMax + 2*CONST_xEpsilon- xMin) / (CONST_nXFDD - 1)
    FFDdy = (yMax + 2*CONST_yEpsilon - yMin) / (CONST_nYFDD - 1)

    for i in range(CONST_nXFDD):
        for j in range(CONST_nYFDD):
            # print "CREATE i,j,k: " + str(i) + " " + str(j) + " " + str(k)

            FFDelement = FFDPointElement.FFDPointElement(xMin - CONST_xEpsilon + FFDdx * i, yMin - CONST_yEpsilon + FFDdy * j,
                                                         zvalue)
            FFDPointArray[i][j][k] = FFDelement

            # print str(FFDelement.getX()) + ", " + str(FFDelement.getY()) + ", " + str(FFDelement.getZ())


#The method used to attach the FFD points onto the CRM wing.
def createFFDMeshCRM(FFDPointArray, solidBoundaryPointArray, solidXMax, solidXMin, solidYMax, solidYMin, solidZMax, solidZMin):

    #sort the keys in the z cross section dictionary
    zCrossSectionList = GLOBAL_zCrossSectionObjects.keys()
    zCrossSectionList.sort()

    print(zCrossSectionList)

    dz = (zCrossSectionList[len(zCrossSectionList)-1] - zCrossSectionList[0])/(CONST_nZFDD-1)

    numCrossSections = len(zCrossSectionList)-1

    print("length: " + str(len(zCrossSectionList)))

    # points will be put at index =0 and index = numCrossSections-1
    # That leaves CONST_nZFDD-2 cross sections left to put.

    #The index seperation between cross sections with FFD points
    dCrossSections = float(numCrossSections)/float((CONST_nZFDD-1))

    print("d cross: " + str(dCrossSections))

    tolerance = 0.1
    for k in range(CONST_nZFDD):
        print("z section exact: " + str(zCrossSectionList[0] + k * dz))
        zCrossSectionSearch = 0
        #The z cross section to search for in the dictionary
        for key in zCrossSectionList:
            if (key == 0 and (zCrossSectionList[0] + k * dz) == 0):
                zCrossSectionSearch = key
                break
            else:
                num = key / (zCrossSectionList[0] + k * dz)
                print("     num: " + str(num))
                if (num < (1 + tolerance) and num > (1-tolerance)):
                    zCrossSectionSearch = key
                    break

        if(k==CONST_nZFDD-1):
            zCrossSectionSearch = zCrossSectionList[len(zCrossSectionList)-1]

        print("z cross section search: " + str(zCrossSectionSearch))

        #index = int(k*dCrossSections)
        #print "index: " + str(index)

        createFFDPointsFixedCrossSections(FFDPointArray, zCrossSectionSearch, k)


# Printing to the file. The data will be written to the file in the following format
    # FFD Point
        # I,J,K
        # X,Y,Z
    # Solid Boundary Point
        # X,Y,Z
        # T,U,V

def preprocessingCRM(xsolid,ysolid,zsolid, solidBoundaryPointArray, FFDPointArray):
    solidXMax, solidXMin, solidYMax, solidYMin, solidZMax, \
    solidZMin = initializeData(xsolid, ysolid, zsolid, solidBoundaryPointArray)

    createFFDMeshCRM(FFDPointArray, solidBoundaryPointArray, solidXMax, solidXMin, solidYMax, solidYMin, solidZMax, solidZMin)

    #AttachFFDNewton(solidBoundaryPointArray)

    f = open(CONST_DATAFILE, "w")
    # first write out the FFD Points
    f.write("FFD Points: X, Y, Z" + "\n")

    for i in range(CONST_nXFDD):
        for j in range(CONST_nYFDD):
            for k in range(CONST_nZFDD):
                FFDElement = FFDPointArray[i][j][k]
                f.write(str(i) + ", " + str(j) + ", " + str(k) + "\n")
                f.write(str(FFDElement.getX()) + ", " + str(FFDElement.getY()) + ", " + str(FFDElement.getZ()) + "\n")

    f.write("Solid Boundary Point Data" + "\n")
    for i in range(len(solidBoundaryPointArray)):
        element = solidBoundaryPointArray[i]
        f.write(str(element.getX()) + ", " + str(element.getY()) + ", " + str(element.getZ()) + "\n")
        f.write(str(element.getT()) + ", " + str(element.getU()) + ", " + str(element.getV()) + "\n")

    f.close()


def preprocessing(xsolid,ysolid,zsolid, solidBoundaryPointArray, FFDPointArray):
    solidXMax, solidXMin, solidYMax, solidYMin, solidZMax, \
    solidZMin = initializeData(xsolid, ysolid, zsolid, solidBoundaryPointArray)

    createFFDMesh(FFDPointArray)
    AttachFFDNewton(solidBoundaryPointArray)

    # Printing to the file. The data will be written to the file in the following format
    # FFD Point
        # I,J,K
        # X,Y,Z
    #Solid Boundary Point
        #X,Y,Z
        #T,U,V

    f = open(CONST_DATAFILE, "w")
    # first write out the FFD Points
    f.write("FFD Points: X, Y, Z" + "\n")

    for i in range(CONST_nXFDD):
        for j in range(CONST_nYFDD):
            for k in range(CONST_nZFDD):
                FFDElement = FFDPointArray[i][j][k]
                f.write(str(i) + ", " + str(j) + ", " + str(k) + "\n")
                f.write(str(FFDElement.getX()) + ", " + str(FFDElement.getY()) + ", " + str(FFDElement.getZ()) + "\n")

    f.write("Solid Boundary Point Data" + "\n")
    for i in range(len(solidBoundaryPointArray)):
        element = solidBoundaryPointArray[i]
        f.write(str(element.getX()) + ", " + str(element.getY()) + ", " + str(element.getZ()) + "\n")
        f.write(str(element.getT()) + ", " + str(element.getU()) + ", " + str(element.getV()) + "\n")

    f.close()

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

#deform the FFD points arbitrarily
def deformFFDPoints(FFDPointArray):
    for i in range(CONST_nXFDD):
        for j in range(CONST_nYFDD):
            for k in range(CONST_nZFDD):
                #shift on row of ffd points by 0.3 in the y direction
                if(k==CONST_nZFDD-1):
                    element = FFDPointArray[i][j][k]
                    newYValue = element.getY()+0.3
                    element.setY(newYValue)




def modifyShape(solidBoundaryPointArray, FFDPointArray):

    #compute the new coordinates of all the solid boundary points using the FFD points

    # do a sum from i=0 to n, where n is the number of spaces between FFD points (so if there are n xFFD points then
    # there are n-1 spaces).
    n = CONST_nXFDD - 1
    m = CONST_nYFDD - 1
    l = CONST_nZFDD - 1

    for solidElement in solidBoundaryPointArray:

        xNew = 0
        yNew = 0
        zNew = 0

        t = solidElement.getT()
        u = solidElement.getU()
        v = solidElement.getV()

        for i in range(CONST_nXFDD):
            for j in range(CONST_nYFDD):
                for k in range(CONST_nZFDD):
                    xNew = xNew + B(i, n, t) * B(j, m, u) * B(k, l, v) * FFDPointArray[i][j][k].getX()
                    yNew = yNew + B(i, n, t) * B(j, m, u) * B(k, l, v) * FFDPointArray[i][j][k].getY()
                    zNew = zNew + B(i, n, t) * B(j, m, u) * B(k, l, v) * FFDPointArray[i][j][k].getZ()

        solidElement.setX(xNew)
        solidElement.setY(yNew)
        solidElement.setZ(zNew)


def FFDSolve():
    # read the data from the file and fill the data structures
    initializeDataFromFile(solidBoundaryPointArray, FFDPointArray)
    solidBoundaryPointArray.sort(key=lambda x: x.getZ(), reverse=True)
    fillInitialArrays(solidBoundaryPointArray, FFDPointArray, xsolidInitial,
                      ysolidInitial, zsolidInitial, xFFDInitial, yFFDInitial, zFFDInitial)

    # printFFDAndSolidBndData(FFDPointArray, solidBoundaryPointArray)

    deformFFDPoints(FFDPointArray)
    modifyShape(solidBoundaryPointArray, FFDPointArray)

    plotFFDandSolidBNDAndInitialFFDandSolidBND(FFDPointArray, solidBoundaryPointArray, xsolidInitial,
                                               ysolidInitial, zsolidInitial, xFFDInitial, yFFDInitial, zFFDInitial)


#Main Method

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


#The preprocessor. Needs to only be run once to initialize all the data and write it
#into the file.


#preprocessing(xsolidInitial,ysolidInitial,zsolidInitial, solidBoundaryPointArray, FFDPointArray)

#preprocessingCRM(xsolidInitial,ysolidInitial,zsolidInitial, solidBoundaryPointArray, FFDPointArray)


# filling the FFD arrays
for i in range(CONST_nXFDD):
    for j in range(CONST_nYFDD):
        for k in range(CONST_nZFDD):
            element = FFDPointArray[i][j][k]
            xFFDInitial.append(element.getX())
            yFFDInitial.append(element.getY())
            zFFDInitial.append(element.getZ())

#plotFiguresTemp(xsolidInitial, ysolidInitial, zsolidInitial, xFFDInitial, yFFDInitial, zFFDInitial)

for element in solidBoundaryPointArray:
    if(element.getT()>1 or element.getU()>1 or element.getV()>1):
        print("T, U, V: " + str(element.getT()) + "  " + str(element.getU()) + "  " + str(element.getV()))
        print("x, y ,z: " + str(element.getX()) + "  " + str(element.getY()) + "  " + str(element.getZ()))

FFDSolve()




