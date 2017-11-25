import sys
import numpy as np
from numpy import cumsum
from PIL import Image

def addpadding(source,pad):
    imarr = np.array(source)
    padimarr = np.zeros((imarr.shape[0]+2*pad,imarr.shape[1]+2*pad),dtype=np.uint8)
    padimarr[pad:padimarr.shape[0]-pad,pad:padimarr.shape[1]-pad]=imarr
    return padimarr

def part(local): #local hist. eq. function
    possibility = [0 for i in range (256)] # need for local hist. eq.
    for v in range (3):
        for h in  range (3):
            P= local [v] [h]
            possibility[P] = possibility[P] +1

    for o in range (256):
        possibility[o] = float(float ( float ( possibility[o]) / 9 ) * 255 )
        possibility[o] = int (round( possibility[o]))

    
    S = local [1][1]
    
    return possibility[S]

orj_img = Image.open(sys.argv[1])
sizex = orj_img.size[0] 
sizey = orj_img.size[1] 
img = addpadding(orj_img,1)

Matrix = [[0 for x in range(sizex+2)] for y in range(sizey+2)] 

for i in range(sizex ): 
    for y in range(sizey):
        temp1 = np.array([img[i, y], img[i+1, y], img[i+2, y]])
        local = np.vstack([temp1])
        temp2 = np.array([img[i, y+1], img[i+1, y+1], img[i+2, y+1]])
        local = np.vstack([local, temp2])
        temp3 = np.array([img[i, y + 2], img[i + 1, y + 2], img[i + 2, y + 2]])
        local = np.vstack([local, temp3])
        Matrix[i+1][y+1]=part(local)


MatrixFinish = [[0 for x in range(sizex)] for y in range(sizey)]  # again convert orjinal  size"example 512 x 512 image"
for k in range (sizex):
    for t in range(sizey):
        MatrixFinish[t][k] =  Matrix[t+1][k+1]


        
#finish part
Image = np.asarray(MatrixFinish)
Image.fromarray(Image,'L').save('NewImage.png','PNG')
                
