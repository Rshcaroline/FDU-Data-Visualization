# visualize vector using glyph

import nibabel as nib
import vtk
import numpy as np

fold='./'
img1 = nib.load( fold+'image_lr.nii.gz') # load and save 

img1_data=img1.get_data() 
#获取标量场数据

dims=img1.shape             #数据场维度
spacing=(img1.header['pixdim'][1], img1.header['pixdim'][2], img1.header['pixdim'][3] )

image=vtk.vtkImageData()              #生成vtkImageData对象
image.SetDimensions( dims[0],dims[1],dims[2] )      #设置vtkImageData对象的维度
image.SetSpacing(spacing[0], spacing[1], spacing[2])        #设置间隔
image.SetOrigin(0,0,0)
image.SetExtent( 0, dims[0]-1, 0, dims[1]-1, 0, dims[2]-1 ) ;
if vtk.VTK_MAJOR_VERSION <= 5:
    image.SetNumberOfScalarComponents(1)      #vtkImageData sclalarArray tuple'size
    image.SetScalarTypeToShort()
else:
    image.AllocateScalars(vtk.VTK_SHORT, 1)

#  
intRange = (-100,900)
max_u_short = 1000
for z in range(dims[2]):
    for y in range(dims[1]):
        for x in range(dims[0]):
            scalardata=img1_data[x][y][z]
            if scalardata<intRange[0]:
                scalardata=intRange[0]
            if scalardata>intRange[1]:
                scalardata=intRange[1]
            scalardata = max_u_short*np.float(scalardata-intRange[0])/np.float(intRange[1]-intRange[0])
            image.SetScalarComponentFromFloat(x, y, z, 0, scalardata)       

gradientFilter=vtk.vtkImageGradient()           #生成梯度图 
gradientFilter.SetInputData(image)
gradientFilter.SetDimensionality(3)
gradientFilter.Update() 

#################################################
magnitude=vtk.vtkImageMagnitude()           #生成梯度模值图
magnitude.SetInputConnection(gradientFilter.GetOutputPort())
magnitude.Update()
imageCast = vtk.vtkImageCast()
imageCast.SetInputConnection( magnitude.GetOutputPort() )
imageCast.SetOutputScalarTypeToUnsignedShort()
imageCast.Update()
magimage = imageCast.GetOutput()


# Create transfer mapping scalar value to opacity
opacityTransferFunction=vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(100,0.0)
opacityTransferFunction.AddSegment(101,0.3,400,0.5)  
opacityTransferFunction.AddPoint(500,0.0)
opacityTransferFunction.ClampingOff();   
 
# Create transfer mapping scalar value to color
colorTransferFunction=vtk.vtkColorTransferFunction() 
colorTransferFunction.AddRGBSegment( 0, 1, 0.0, 0.0, 200, 1, 0, 0 ) 
colorTransferFunction.AddRGBSegment( 251, 0.1,1,0 , 1000, 0.1,1,0 ) # intensity between 0 
 

# The property describes how the data will look -- from zxhproj::CardCoronaryRender.cpp
volumeProperty=vtk.vtkVolumeProperty() 
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.SetColor(colorTransferFunction) 
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()
volumeProperty.SetAmbient(0.25)
volumeProperty.SetDiffuse(0.6) #漫反射
volumeProperty.SetSpecular(0.4) #镜面反射 
 
compositeFunction=vtk.vtkVolumeRayCastCompositeFunction()
volumeMapper = vtk.vtkVolumeRayCastMapper() 
volumeMapper.SetVolumeRayCastFunction( compositeFunction )  
volumeMapper.SetInputData(magimage) 
volumeMapper.SetImageSampleDistance(5.0)  

volume=vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

ren = vtk.vtkRenderer()
ren.SetBackground( 1, 1, 1 )
ren.AddVolume(volume)
renWin=vtk.vtkRenderWindow()  

light=vtk.vtkLight()
light.SetColor(1,1,1) #光的颜色

ren.AddLight( light ) 

renWin.AddRenderer(ren)
renWin.SetSize(500, 500)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

renWin.Render()
iren.Initialize()
iren.Start()