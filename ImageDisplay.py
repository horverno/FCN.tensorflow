import cv2
import matplotlib
import matplotlib.pyplot as plt
import glob
import os
import numpy as np

fileList = []
fileGlob = os.path.join("Data_zoo\\Shell_Eco01\\", "train", "inp",'*.' + 'png') # jpg / png
fileList.extend(glob.glob(fileGlob))
#print(fileList)
print("%d images found in %s" % (len(fileList), fileGlob))

strInp  = input("Enter a number: ")
if strInp == "":
    numToDisplay = 1
else:
    numToDisplay = int(strInp)

for i in range(numToDisplay):
    iInp = cv2.imread(fileList[i])
    iInp = iInp[:,:,::-1]
    iOut = cv2.imread(fileList[i].replace("inp", "out"))
    iMer = np.zeros(iInp.shape, dtype = "uint8")
    iMer[:, :, 0] = iInp[:, :, 0]
    iMer[:, :, 1] = ((iOut[:, :, 0]-1)*-1) * iInp[:, :, 0]
    iMer[:, :, 2] = iInp[:, :, 0]
    fig, axes = plt.subplots(1, 3, figsize=(16,6))
    axes[0].imshow(iInp, interpolation = 'bicubic')
    axes[1].imshow(iOut[:, :, 1])
    axes[2].imshow(iMer, interpolation = 'bicubic') 
    plt.show()
