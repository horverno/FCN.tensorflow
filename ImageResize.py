'''
This script resizes (optinally tresholds and fixes broken files) and saves images
source path is defined in sourcePath and destination path is defined in whereToSave

The directory formats are:
* v1
  - test  - inp (20%)
          - out
          - oux
  - train - inp (60%)
          - out
          - oux         
  - val   - inp (20%)
          - out
          - oux

* v2
  - annotations - training   (60%)
                - validation (20%)
  - images      - training   (60%)
                - validation (20%)

'''

#import cv2 # scipy.misc instead
import glob
import os
import inspect
import numpy as np
import scipy.misc as misc
from scipy.ndimage.interpolation import zoom
from scipy.misc import imsave
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.widgets import Button
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from random import shuffle

errorCount = 0 # nuber of errors
ii = 0 # iteration variable
whereToSave = "E:\\DatasetW\\"
sourcePath = os.path.join("Data_zoo\\Shell_Eco03\\test\\inp", "*.png") # jpg / png || test train val
fileList = []
fileDirs = sourcePath.split("\\")[0:-1] # file directories list # "\\".join(fileDirs)
fileList.extend(glob.glob(sourcePath))
#print(fileList)
print("%d images found in %s\\%s" % (len(fileList), os.path.dirname(os.path.abspath(inspect.stack()[0][1])), sourcePath))
iInp = misc.imread(fileList[0])
iOut = misc.imread(fileList[0].replace("inp", "out"))
# create the directory structure format v1
#directories = [whereToSave, whereToSave + "\\test\\inp", whereToSave + "\\test\\out", whereToSave + "\\test\\oux", whereToSave + "\\train\\inp", whereToSave + "\\train\\out", whereToSave + "\\train\\oux", whereToSave + "\\val\\inp", whereToSave + "\\val\\out", whereToSave + "\\val\\oux"]
# create the directory structure format v2
directories = [whereToSave, whereToSave + "\\annotations\\training", whereToSave + "\\annotations\\validation", whereToSave + "\\images\\training", whereToSave + "\\images\\validation"]
for d in directories:
    if not os.path.exists(d):
        os.makedirs(d)
        print(d + " >> created.")
    else:
        print(d + " >> already exists.")
'''
# format v1
tvt = ["train\\" for i in range(len(fileList) + 1)] # tvt - train, validation, test directories to save
for i in range(int(len(fileList) * 0.2)): tvt[i] = "test\\" # 20% is test
tvt = tvt[::-1] # reverse list
for i in range(int(len(fileList) * 0.2)): tvt[i] = "val\\" # 20% is validatiton
shuffle(tvt) # shuffle list
'''
# format v2
tvt = ["training\\" for i in range(len(fileList) + 1)] # tvt - train, validation, test directories to save
for i in range(int(len(fileList) * 0.2)): tvt[i] = "validation\\" # 20% is validatiton
shuffle(tvt) # shuffle list


for i in fileList:
    ii += 1
    iInp = misc.imread(i)
    iInp
    try:
        iOut = misc.imread(i.replace("inp", "out"))
    except:
        errorCount += 1
        print("Error: " + i)
    if np.amax(iOut[:, :, 0]) > 3: # we have 4 categories 0-3, so pixelvalue normally cannot be higher than 3, but there were some broken images
        print(iInp.shape + iOut.shape, end=" - ")
        print("max: %3d" % np.amax(iOut[:, :, 0]), end = " - ")
        #plt.imshow(iOut[:, :, 0]); plt.colorbar(); plt.show()
        iO = iOut[:, :, 0]
        iO[iO > 3] = 0 # optinal treshold if pixelvalue is higher than 3
        #plt.imshow(A); plt.colorbar(); plt.show()
        iOut[:, :, 0] = iO
    else:
        iO = iOut[:, :, 0]
    '''
    # format v1
    imsave(whereToSave + tvt[ii] + "out\\" + os.path.split(i)[1], misc.imresize(iOut, (290, 512))) #zoom(iOut[:, :, 0], 0.5)
    imsave(whereToSave + tvt[ii] + "oux\\" + os.path.split(i)[1], misc.imresize(iO*80, (290, 512))) #zoom(iOut[:, :, 0], 0.5)
    imsave(whereToSave + tvt[ii] + "inp\\" + os.path.split(i)[1], misc.imresize(iInp[:, :, 0:3], (290, 512))) #zoom(iOut[:, :, 0], 0.5)
    # iInp[:, :, 0:3] >> means cutting the alpha from RGBA so only RGB channels
    '''

    # format v2
    imsave(whereToSave + "annotations\\" + tvt[ii] + os.path.split(i)[1], misc.imresize(iO, (290, 512))) #zoom(iOut[:, :, 0], 0.5)
    imsave(whereToSave + "images\\" + tvt[ii] + os.path.split(i)[1], misc.imresize(iInp[:, :, 0:3], (290, 512))) #zoom(iOut[:, :, 0], 0.5)
    # iInp[:, :, 0:3] >> means cutting the alpha from RGBA so only RGB channels
    print("%s\\%s" % (os.path.dirname(os.path.abspath(inspect.stack()[0][1])), i.replace("inp", "out")))
    #print(iOut.shape[2], end = " - ")
    #print(np.amax(iOut[:, :, 0]), end = " - ")

if errorCount > 0:
    print("Error: " + errorCount)
else:
    print("No file was missing")