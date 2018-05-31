import nibabel as nib
import vtk
 
fold='./'
img1 = nib.load( fold+'image_lr.nii.gz') # load and save 
img1_data=img1.get_data()           #获取标量场数据
dims=img1.shape # [124,124,73]                  #数据场维度
spacing=(img1.header['pixdim'][1], img1.header['pixdim'][2], img1.header['pixdim'][3] ) 

image=vtk.vtkImageData()              #生成vtkImageData对象
image.SetDimensions( dims[0],dims[1],dims[2] )      #设置vtkImageData对象的维度
#blank  设置间隔
#blank  设置Origin 

if vtk.VTK_MAJOR_VERSION <= 5:
    image.SetNumberOfScalarComponents(1)      #vtkImageData sclalarArray tuple'size
    image.SetScalarTypeToDouble()
else:
    image.AllocateScalars(vtk.VTK_DOUBLE, 1)

# Fill every entry of the image data. 
for z in range(dims[2]):
    for y in range(dims[1]):
        for x in range(dims[0]):
            # blank  将图像标量场数据填入vtkImageData对象的scalar属性中

 
Extractor=vtk.vtkMarchingCubes()         #移动立方体算法对象，得到等值面
#blank  输入数据
#blank  设置value，求value=200的等值面

stripper=vtk.vtkStripper()             #建立三角带对象
stripper.SetInputConnection(Extractor.GetOutputPort())     #输入数据，将生成的三角片连接成三角带
mapper=vtk.vtkPolyDataMapper()                           #下面设置,mapper,actor,renderer等
mapper.SetInputConnection(stripper.GetOutputPort())
actor=vtk.vtkActor()
actor.SetMapper(mapper)  

#blank  设置颜色
actor.GetProperty().SetOpacity(0.9)
actor.GetProperty().SetAmbient(0.25)
actor.GetProperty().SetDiffuse(0.6)
actor.GetProperty().SetSpecular(1.0) 

ren = vtk.vtkRenderer() 
#blank  设置背景颜色
ren.AddActor(actor) 
renWin = vtk.vtkRenderWindow()

renWin.AddRenderer(ren)
renWin.SetSize(250, 250)
iren = vtk.vtkRenderWindowInteractor()

iren.SetRenderWindow(renWin)
iren.Initialize()
renWin.Render()
iren.Start()
