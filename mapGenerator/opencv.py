import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def Detect(template, img):
 w, h = template.shape[::-1]
 res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
 threshold = 0.8
 loc = np.where( res >= threshold)
 for pt in zip(*loc[::-1]):
  cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)


templates=[]
adrs=[]
while True:
 adr = input()
 if adr == "":
  break
 else:
  adrs.append(adr)

for img in adrs:
 template=cv.imread(img, cv.IMREAD_GRAYSCALE)
 assert template is not None, "file could not be read, check with os.path.exists()"
 templates.append(template)


img_rgb = cv.imread('shapes.png')
assert img_rgb is not None, "file could not be read, check with os.path.exists()"

img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)


for n in templates :
 Detect(n,img_rgb)

cv.imwrite('res.png',img_rgb)

