# -*- coding: utf-8 -*-
"""
Created on Thu May 25 11:55:29 2017

@author: Administrator
"""

'''
import vtk
import time
cone=vtk.vtkConeSource()
cone.SetHeight(10)
cone.SetRadius(1)
cone.SetResolution(20)
coneMapper = vtk.vtkPolyDataMapper()
coneMapper.SetInputConnection( cone.GetOutputPort() )
coneActor = vtk.vtkActor()
coneActor.SetMapper( coneMapper )
ren1= vtk.vtkRenderer()
ren1.AddActor( coneActor )
ren1.SetBackground( 0.1, 0.2, 0.4 )
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer( ren1 )
renWin.SetSize( 300, 300 )
for i in range(0,360):
    time.sleep(0.08)
    renWin.Render()
    ren1.GetActiveCamera().Azimuth(1)
'''

import nibabel as nib
import vtk

fold = ''
img1 = nib.load(fold+'img_lr.nii.gz')
img1_data = img1.get_data()
dims = img1.shape
spacing = (img1.header['pixdim'][1],)