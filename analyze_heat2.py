import cv2
import numpy as np
import pandas as pd


img = cv2.imread("sample2.jpg", 0)
img[img<10] = 0
xs,ys = np.nonzero(img)
print(xs)
print(ys)

data = pd.DataFrame(columns=["x","y","z"])

for x,y in zip(xs, ys):
    data.loc[len(data)] = {'x' : x , 'y' : y, 'z' : img[x,y]}
print(data)
data.to_csv("231126" + '_' + "test" + '.csv', index=False, encoding='utf8')