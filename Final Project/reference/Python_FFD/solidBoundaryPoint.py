

#A class that will hold all the data for each boundary point.
class solidBoundaryPoint(object):

    def __init__(self, xInitial, yInitial, zInitial):
        self.x = xInitial
        self.y = yInitial
        self.z = zInitial

        self.t = 0
        self.u = 0
        self.v = 0

    #The getters
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def getT(self):
        return self.t

    def getU(self):
        return self.u

    def getV(self):
        return self.v

    #The setters
    def setT(self, t):
        self.t = t

    def setU(self, u):
        self.u = u

    def setV(self, v):
        self.v = v

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setZ(self, z):
        self.z = z

