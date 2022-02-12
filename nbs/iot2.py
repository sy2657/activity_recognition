# -*- coding: utf-8 -*-
"""iot2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11LGfscG35AknZvbvU0-zdFZt9ozYSFfW
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install scipy==1.5

import os

PATH = '/content/drive/My Drive/IOT Classification Challenge/Dataset_1/'

os.listdir(PATH)

DATASET = '/content/drive/My Drive/IOT Classification Challenge/Dataset_1/refrigerator/'

os.listdir(DATASET)

from glob import glob
result = [y for x in os.walk(DATASET) for y in glob(os.path.join(x[0], '*.*'))]
result[:10]

result[100]

def initialize_dataset():
  result = [y for x in os.walk(DATASET) for y in glob(os.path.join(x[0], '*.mp4'))]  # extract all the mp4 file.
  labels = [r.split('/')[7] for r in result]   #labels are the interactions with refrigerator.
  return list(zip(labels, result))

initialize_dataset()[:10]

# choose another video
label, path = initialize_dataset()[100]

# visualize
import cv2
from google.colab.patches import cv2_imshow

cap = cv2.VideoCapture(path) #open the video

# keep seeing until person enters
count = 0
while(cap.isOpened()):
  ret, frame = cap.read() # ret is True/False of reading video correctly, frame is pixel matrix.
  if ret == True:
    cv2_imshow(frame) # return the first frame of original picture
    
    count = count+1
    if count >30:
      break

# person enters around frame 29 to 30

import cv2
from google.colab.patches import cv2_imshow

label, path = initialize_dataset()[0] #get first video, label is "put_back_item",path is the ".../...mp4"

cap = cv2.VideoCapture(path) #open the video
while(cap.isOpened()):
  ret, frame = cap.read() # ret is True/False of reading video correctly, frame is pixel matrix.
  if ret == True:
    cv2_imshow(frame) # return the first frame of original picture
    break

import numpy as np
cap = cv2.VideoCapture(path) #open the video

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/

!pip install -U torch==1.5 torchvision==0.6 -f https://download.pytorch.org/whl/cu101/torch_stable.html 
!pip install cython pyyaml==5.1
!pip install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
import torch, torchvision
print(torch.__version__, torch.cuda.is_available())
!gcc --version
!pip install detectron2==0.1.3 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.5/index.html

!pip install pointpats

# try saliency 

import cv2
from google.colab.patches import cv2_imshow

"""static saliency: relies on image features and stats to localize most interesting regions of an image

**motion saliency:** relies on video/frame-by-frame inputs; keep track of objects that move

**objectness**: compute "objectness" and generate "proposals" or bounding boxes of where it thinks an object lies in an image

4 implementations of saliency detectors:
- cv2.saliency.ObjectnessBING_create()
- cv2.saliency.StaticSaliencySpectralResidual_create()
- cv2.saliency.StaticSaliencyFineGrained_create()
- cv2.saliency.MotionSaliencyBinWangApr2014_create()


Each of the above constructors returns an object that implements a compute saliency method called on input image and returning 2 quantities: boolean that indicates if saliency was successful or not, output saliency map used for deriving "interesting" regions of an image

"""

# objectness
saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
(success, saliencyMap) = saliency.computeSaliency(image)
saliencyMap = (saliencyMap * 255).astype("uint8")
cv2.imshow("Image", image)
cv2.imshow("Output", saliencyMap)
cv2.waitKey(0)

import imutils

# try to visualize the frame

cap = cv2.VideoCapture(path) #open the video

cnt = 0

while(cap.isOpened()):
  ret, frame = cap.read()
  if ret == True:
    resized = imutils.resize(frame, width=500) # pyimagesearch.com article
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    #gray = cv2.GaussianBlur(gray, (21,21), 0)
    
    #cv2_imshow(gray) # frame

    if cnt == 0:
      firstFrame = gray
      cnt = cnt+1
      continue

    frame_delta = cv2.absdiff(firstFrame, gray)

    cv2_imshow(frame_delta)

    thres = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]


    cnt = cnt+1

    if cnt>30:
      break

frame_delta

cnt

# feb 4 from Mengjie function
import numpy as np
def get_frames(path, frameskip = 1, greyscale = False):

  cap = cv2.VideoCapture(path) #open the video

  cnt = 0
  framelist = []

  #extracts frames according to frameskip
  while(cap.isOpened()):
    ret, frame = cap.read()

    #print("length of frame is ", len(frame))

    if ret == True:
      if cnt%frameskip == 0:
        framelist.append(frame)
    else:
      break

    cnt += 1

  #greyscaling video
  if greyscale:
    greyer = lambda t: cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)
    framelist = np.array([greyer(x) for x in framelist])
  
  return framelist

grey_frames = get_frames(path, frameskip=2, greyscale=True)

len(grey_frames[0][0]) # dimension is 720 rows by 1280 columns

import matplotlib

matplotlib.pyplot.matshow(grey_frames[0])

grey_frames[0]

grey_frames[1]

frame30 = grey_frames[30] - grey_frames[29]

cv2_imshow(frame30)

a1 = np.array([[1,1,1], [2,2,2]])

a2 = np.array([[0,0,0], [0,0,1]])

a1 - a2

a3 = a1 - a2

boola3 = a3 > 1 # boolean

boola3

np.where(boola3)

where_a3 = np.where(boola3)

for el in where_a3:
  print(el)

where_a3[0].tolist()

coords = []
for (x, y) in zip(where_a3[0], where_a3[1]):
    print((x, y))
    coords.append((x,y))

coords

ind = 0

thres = 150

frame_coords = {}

frame_coords_x = {}
frame_coords_y = {}

firstFrame = grey_frames[0]

for frame in grey_frames:

  if ind==0:
    prev_frame = frame
    ind = ind+1
    continue

  diff = prev_frame - frame
  diff_abs = abs(diff)

  #cv2_imshow(diff_abs)

  frame_delta = cv2.absdiff(firstFrame, frame)

  if 20 <ind < 25:
    cv2_imshow(frame_delta)

  # boolean greater than threshold
  boolean_diff = frame_delta > thres #diff_abs > thres

  where_diff = np.where(boolean_diff)
  coords = []
  coords_x = []
  coords_y= []
  for (x, y) in zip(where_diff[0], where_diff[1]):
      #print((x, y))
      coords_x.append(x)
      coords_y.append(y)
      coords.append((x,y))

      # compare distance with average?


  # analyze coordinates
  frame_coords[ind] = coords
  frame_coords_x[ind] = coords_x
  frame_coords_y[ind] = coords_y

  ind = ind+1
  prev_frame=frame

# analyze coordinates

coords = frame_coords[20] # choose a frame # 

# fall within bin of 10 from eachother? 

# create bins within area of 0 to 1280 columns and 0 to 720 rows: divide by 20 
bin_limits = []
bin_map = {}
bin_orig_map = {}
ind=0

for i in range(64): # 1280 total
  for j in range(36): # 720 total
    i_lim_low = i*(20)
    i_lim_high = (i+1)*(20)
    j_lim_low = j*(20)
    j_lim_high = (j+1)*(20)
    ij_low = (i_lim_low, j_lim_low)
    bin_limits.append(ij_low)
    bin_map[ij_low] = ind
    bin_orig_map[(i,j)] = ind

    ind = ind+1

coords[2]

!pip install scipy==1.5

from scipy import stats
import numpy as np

ax = [0.1, 2.1, 0.1, 2.6]
ay = [2.1, 2.6, 2.1, 2.1]

ax= np.array(ax, dtype=float)
ay= np.array(ay, dtype=float)

binx = [0 , 2, 3]
biny = [0,2, 3]

binx= np.array(binx, dtype=float)
biny= np.array(biny, dtype=float)

#binx = [0.0, 0.5, 1.0]
#biny = [2.0, 2.5, 3.0]

stats.binned_statistic_2d(ax, ay, None, 'count', bins=[binx, biny], expand_binnumbers=True)

import numpy as np 
20*np.arange(37)

"""for c in coords:
  # bins 
  cx = c[0]
  cy = c[1]

  # find which bin it falls into
  x_low_div_20 = np.floor(cx/20)
  y_low_div_20 = np.floor(cy/20)



  c_ind = bin_map[(x_low, y_low)]"""

binx = 20*np.arange(66)
biny = 20*np.arange(38)


sb = stats.binned_statistic_2d(coords_x, coords_y, None, 'count', bins=[binx, biny], expand_binnumbers=True)

bin_arrs = sb[3]

bin_x = bin_arrs[0]
bin_y = bin_arrs[1]

bin_histogram = {}

for ind in range(len(bin_x)):
  pair = (bin_x[ind], bin_y[ind])
  #print("pair is ", pair)
  orig_index = bin_orig_map[pair]
  if bin_histogram.get(orig_index) ==None:
    bin_histogram[orig_index]=1
  else:
    bin_histogram[orig_index]= bin_histogram[orig_index]+1

# choose starting frame based on where the bins are well concentrated

bin_x

bin_y

bin_histogram

# geographic data methods

import numpy
#import pandas
#import geopandas
#import pysal
#import seaborn
#import contextily
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

from pointpats import centrography

coordinates = [[1,1], [0,0],[2,2]]

centrography.std_distance([[1,1], [0,0],[2,2]]) # dispersion


# standard deviational ellipse

#major, minor, rotation = centrography.ellipse()

qstat = QStatistic(coordinates) # whether points are spread out, or if they are clustered into a few cells

def euclid_dist(x1, x2):
  return np.linalg.norm(x1 - x2)



# from binary change

# abs(grey_frames[:(len(grey_frames)-1)] - grey_frames[1:])

frames_diff = np.where((abs(grey_frames[:(len(grey_frames)-1)] - grey_frames[1:]))<150,0,1)

# idea: measure if the change occurs within the same area / neighborhood  ; or if it appears from the side first?

#frames_diff
frames_diff_sum = np.sum(frames_diff,axis=(1,2))

segments = []
for i in np.arange(len(frames_diff_sum)/10):
    segments.append(sum(frames_diff_sum[(int(i)*10):(int(i)*10+100)]))
best_segment = segments.index(max(segments))

# best segment is 1st entry but does this correspond to which frame?

# feb 6: change detection matrices

# select similarity measure and threshold

# detect any differences between the arrays ?

saliency = cv2.saliency.StaticSaliencySpectralResidual_create()

#visualize with saliency
cap = cv2.VideoCapture(path) #open the video
while(cap.isOpened()):
  ret, frame = cap.read()
  if ret == True:
    (success, saliencyMap) = saliency.computeSaliency(frame)
    saliencyMap = (saliencyMap * 255).astype("uint8")
    cv2_imshow(frame)
    cv2_imshow(saliencyMap)
    
    break

# static saliency : static spectral saliency

cap = cv2.VideoCapture(path) #open the video

count= 0

saliency = cv2.saliency.StaticSaliencySpectralResidual_create()

while(cap.isOpened()):
  ret, frame = cap.read()
  if ret == True:
    (success, saliencyMap) = saliency.computeSaliency(frame)
    saliencyMap = (saliencyMap * 255).astype("uint8")
    cv2_imshow(frame)
    cv2_imshow(saliencyMap)
    
    count= count+1

    if count>2:
      break

# fine grained saliency

saliency = cv2.saliency.StaticSaliencyFineGrained_create()

count=0

while(cap.isOpened()):
  ret, frame = cap.read()
  if ret == True:
    (success, saliencyMap) = saliency.computeSaliency(frame)
    saliencyMap = (saliencyMap * 255).astype("uint8")
    cv2_imshow(frame)
    cv2_imshow(saliencyMap)
    
    count= count+1

    if count>2:
      break

threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255,	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

cv2_imshow(threshMap)

frame_delta = cv2.absdiff(firstFrame, gray)

firstFrame = gray

saliency = cv2.saliency.ObjectnessBING_create()
# set path as first frame?

# difference btwn saliency maps

saliency = cv2.saliency.ObjectnessBING_create()

# try other saliency maps

count=0

while(cap.isOpened()):
  ret, frame = cap.read()
  if ret == True:

    if count == 0:
      firstFrame = frame # gray
      saliencyMap = saliency.computeSaliency(frame)
      firstSaliency = (saliencyMap * 255).astype("uint8")
      cnt = cnt+1
      continue    
    # basic detection and tracking of motion
    frame_delta = cv2.absdiff(firstFrame, frame ) # gray

    

    (success, saliencyMap) = saliency.computeSaliency(frame)
    saliencyMap = (saliencyMap * 255).astype("uint8")
    
    #cv2_imshow(frame)
    #cv2_imshow(saliencyMap)

    frame_delta_saliency = cv2.absdiff(firstSaliency, saliencyMap)

    cv2_imshow(frame_delta_saliency)

    count= count+1

    if count>2:
      break

# objectness, detections

# loop over the detections
for i in range(0, min(numDetections, args["max_detections"])):
	# extract the bounding box coordinates
	(startX, startY, endX, endY) = saliencyMap[i].flatten()
	
	# randomly generate a color for the object and draw it on the image
	output = image.copy()
	color = np.random.randint(0, 255, size=(3,))
	color = [int(c) for c in color]
	cv2.rectangle(output, (startX, startY), (endX, endY), color, 2)
	# show the output image
	cv2_imshow(output)

# motion saliency from Wang, Dudek 2014

if saliency is None:
		saliency = cv2.saliency.MotionSaliencyBinWangApr2014_create()
		saliency.setImagesize(frame.shape[1], frame.shape[0])
		saliency.init()
  
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
(success, saliencyMap) = saliency.computeSaliency(gray)
saliencyMap = (saliencyMap * 255).astype("uint8")
# display the image to our screen
cv2.imshow("Frame", frame)
cv2.imshow("Map", saliencyMap)