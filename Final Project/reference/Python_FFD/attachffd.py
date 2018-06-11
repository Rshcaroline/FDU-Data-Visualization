import solidBoundaryPoint

#x, y, z are the solid body points.
#x1, y1, z1 are the FFD points

def computeTUVData(SolidBoundaryPointArray, FFDPointArray, FFDXMax, FFDXMin, FFDYMax, FFDYMin, FFDZMax, FFDZMin):

    for i in range(len(SolidBoundaryPointArray)):
        element = SolidBoundaryPointArray[i]

        t = (element.getX() - FFDXMin)/(FFDXMax - FFDXMin)
        u = (element.getY() - FFDYMin)/(FFDYMax-FFDYMin)
        v = (element.getZ() - FFDZMin)/(FFDZMax-FFDZMin)

        element.setT(t)
        element.setU(u)
        element.setV(v)




