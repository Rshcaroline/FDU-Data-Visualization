import nibabel as nib
import vtk
import numpy as np

fold='./'
img1 = nib.load( fold+'image_lr.nii.gz') # load and save 
img1_data=img1.get_data()           #获取标量场数据
dims=img1.shape # [124,124,73]                  #数据场维度
spacing=(img1.header['pixdim'][1], img1.header['pixdim'][2], img1.header['pixdim'][3] )

image=vtk.vtkImageData()              #生成vtkImageData对象
image.SetDimensions( dims[0],dims[1],dims[2] )      #设置vtkImageData对象的维度
image.SetSpacing(spacing[0], spacing[1], spacing[2])        #设置间隔
image.SetOrigin(0,0,0)
image.SetExtent( 0, dims[0]-1, 0, dims[1]-1, 0, dims[2]-1 ) ;

if vtk.VTK_MAJOR_VERSION <= 5:
    image.SetNumberOfScalarComponents(1)      #vtkImageData sclalarArray tuple'size
    image.SetScalarTypeToUnsignedShort()
else:
    image.AllocateScalars(vtk.VTK_UNSIGNED_SHORT , 1)

# Fill every entry of the image data. 
intRange = (-100,900) 
max_u_short = 1000  # 0-100 lung，200-400 enhanced blood, 400-1000 bone
for z in range(dims[2]):
    for y in range(dims[1]):
        for x in range(dims[0]):
            scalardata=img1_data[x][y][z]
            if scalardata<intRange[0]:
                scalardata=intRange[0]
            if scalardata>intRange[1]:
                scalardata=intRange[1]
            scalardata = max_u_short*np.float(scalardata-intRange[0])/np.float(intRange[1]-intRange[0])
            image.SetScalarComponentFromFloat(x, y, z, 0, scalardata)      #将图像标量场数据填入vtkImageData对象的scalar属性中

# Create transfer mapping scalar value to opacity
opacityTransferFunction=vtk.vtkPiecewiseFunction()
#blank     opacityTransferFunction.AddSegment    # 显示肺部
#blank     opacityTransferFunction.AddSegment    # 显示增强 
#blank     opacityTransferFunction.AddSegment    # 骨骼
opacityTransferFunction.ClampingOff()  # 
 
# Create transfer mapping scalar value to color
colorTransferFunction=vtk.vtkColorTransferFunction() 
#blank     colorTransferFunction.AddRGBSegment 
#blank     colorTransferFunction.AddRGBSegment  # intensity between 
#blank     colorTransferFunction.AddRGBSegment  # intensity between  

# grad to opacity transfer
#gradientTransferFunction=vtk.vtkPiecewiseFunction()
#gradientTransferFunction.AddPoint(0,0.0);
#gradientTransferFunction.AddSegment(22, 0.1, 128, 0.3 );

# The property describes how the data will look -- from zxhproj::CardCoronaryRender.cpp
volumeProperty=vtk.vtkVolumeProperty() 
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.SetColor(colorTransferFunction)
#volumeProperty.SetGradientOpacity(gradientTransferFunction)
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()
volumeProperty.SetAmbient(1)
volumeProperty.SetDiffuse(0.9) #漫反射
volumeProperty.SetSpecular(0.8) #镜面反射
volumeProperty.SetSpecularPower(10)  
 
compositeFunction=vtk.vtkVolumeRayCastCompositeFunction()
volumeMapper = vtk.vtkVolumeRayCastMapper() 
volumeMapper.SetVolumeRayCastFunction( compositeFunction )  
volumeMapper.SetInputData(image) 
volumeMapper.SetImageSampleDistance(5.0) 
 
# The volume holds the mapper and the property and
# can be used to position/orient the volume
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