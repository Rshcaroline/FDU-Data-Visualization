import nibabel as nib
fold='./'
img1 = nib.load( fold+'image_lr.nii.gz') # load and save
#nib.save( img1, 'new_image.nii.gz' )

# header
img1_header=img1.header
#print( img1_header)
print( img1.header['dim'] ) # image size [dimension, xsize, ysize, zsize, tsize, asize, bsize, csize]
print( img1.header['pixdim'] ) # pixel size [pixeldim, spacing[0], spacing[1], spacing[2], spacing[3], spacing[4], spacing[5], spacing[6]]
# data
img1_data = img1.get_data()
print(img1_data.shape) # (124, 124, 73)
 
# access data
#img1_data(i, j, k)

import matplotlib.pyplot as plt
plt.figure( 'one slice of a volumetric image!' )
plt.imshow( img1_data[:,:,30] ,cmap='gray' )
plt.show()