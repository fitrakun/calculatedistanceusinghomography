# Fitra Rahmamuliani 1227003 #
#this program made using python3 with some python3 function. Make sure to run it with python3 

import numpy as np
import sys
import math
import cv2

#A4 width
dst_xsize=210
#A4 height
dst_ysize=297

plist = np.array([0,0])

#input paper image point
ppaperimage = np.array([0,0])

def onMouse( event, x, y, flag, params ):
	global plist
	global pnum
	global ppaper
	global ppoint
	wname, img = params

	if event == cv2.EVENT_MOUSEMOVE:
		img2 = np.copy( img )
		h, w = img2.shape[0], img2.shape[1]
		cv2.line( img2, ( x, 0 ), ( x, h - 1 ), ( 255, 0, 0 ) )
		cv2.line( img2, ( 0, y ), ( w - 1, y ), ( 255, 0, 0 ) )
		font = cv2.FONT_HERSHEY_PLAIN
		if pnum==0:
			text="Click TOP LEFT image of A4 paper"
		elif pnum==1:
			text="Click TOP RIGHT image of A4 paper"
		elif pnum==2:
			text="Click BOTTOM RIGHT image of A4 paper"
		elif pnum==3:
			text="Click BOTTOM LEFT image of A4 paper"
		elif pnum==4:
			text='CLICK 1st point'
		elif pnum==5:
			text='CLICK 2nd point'
		else:
			text='type q to END'
		font_size=1
		cv2.putText(img2,text,(0,20),font,font_size,(255,255,0))
		cv2.imshow( wname, img2 )

	if event == cv2.EVENT_LBUTTONDOWN:
		if pnum > 6 :
			return	
		cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
		if pnum < 4:
			ppaperimage[ppaper]=np.array([x,y])
			ppaper +=1
		else:
			plist[ppoint]=np.array([x,y])
			ppoint+=1
		pnum+=1

imageName = input("Please write the image name: ")
print("Opening the file " + str(imageName))
filename = './'
filename +=str(imageName)

#read and show the image
img = cv2.imread(filename)
if img is None:
	print("No image detected, opening sample.jpg")
	imageName = 'sample.jpg'
	img = cv2.imread('sample.jpg')
img_org = img.copy()
cv2.imshow(imageName,img)

# create edge image #
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
edges = cv2.Canny(gray,250,350,apertureSize = 3)
cv2.imshow('image',edges)
cv2.imwrite('edge.jpg',edges)
cv2.destroyAllWindows()

### HoughTransform ###
rho_tics=1.0
theta_tics = np.pi/180.0
th = 200
lines = cv2.HoughLines(edges, rho_tics,theta_tics, th)
wname = "Calculate Distance of 2 points"
plist = np.zeros((2,2))
ppaperimage = np.zeros((4,2))
pnum=0
ppaper=0
ppoint=0
cv2.namedWindow( wname )
cv2.setMouseCallback( wname, onMouse, [ wname, img] )
cv2.imwrite('houghlines3.jpg',img)
cv2.imshow(wname,img)
cv2.waitKey(0)

#set the real world plane of the paper
pts_dst = np.array([[0, dst_ysize],[dst_xsize,dst_ysize],[dst_xsize,0],[0,0]])

#change everything to float32 type for accessing the perspectivetrasform function
ppaperimage2 = np.float32(ppaperimage).reshape(-1,1,2)
pts_dst2 = np.float32(pts_dst).reshape(-1,1,2)
plist2 = np.float32(plist).reshape(-1,1,2)

#compute the relation between the image plane and the real world plane of the paper
h, mask = cv2.findHomography(ppaperimage2, pts_dst2)
pdestination = cv2.perspectiveTransform(plist2,h)

#compute the distance based on the perspective transform result and normalize using euclidean 
distancetext =  str(np.int32(cv2.norm(pdestination[1],pdestination[0], cv2.NORM_L2))) + " mm"
print("Distance: " + distancetext)

#draw the distance number and line 
cv2.line(img,(int(plist[0,0]),int(plist[0,1])),(int(plist[1,0]),int(plist[1,1])),(0,255,0),1)
font = cv2.FONT_HERSHEY_PLAIN
font_size=1
cv2.putText(img,distancetext,(int(plist[0,0])+5,int(plist[0,1])+5),font,font_size,(144, 0, 255),2)

#save the result in distance.png and show the result image
cv2.imwrite('distance.png',img, [cv2.IMWRITE_PNG_COMPRESSION, 9])
cv2.destroyAllWindows()
img_dst = cv2.imread('./distance.png')
cv2.imshow("Distance Result",img_dst)

#window will be close if the user press something
cv2.waitKey(0)
cv2.destroyAllWindows()