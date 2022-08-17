#!/usr/bin/python3

import open3d as o3d
import numpy as np

def cartesian2Polar(x,y):
    rho=np.sqrt(x**2 + y**2)
    theta=np.arctan2(y,x)
    return (float("{:.2f}".format(rho)), float("{:.2f}".format(theta*180)))

data=np.load('/home/guilherme/Documents/Autonomous-Device-for-Analysis-and-Monitoring-of-Underwater-Structures/datasPiscina/matrixSample.npy')


rangeSonar=1500 #1.5m
numOfpoints=len(data[0][0])
#print(numOfpoints)
factorCorretion=rangeSonar/numOfpoints

lines=(data.shape[0]*data.shape[1]*data.shape[2])

f=np.zeros((lines,6))
 
file=open('/home/guilherme/Documents/data.txt','w+')

aux=0
for z in range(len(data)):
    for y in range(len(data[z])):
        for x in range(len(data[z][y])):
            if data[z][y][x]>230 and  data[z][y][x]<250:
                #a=np.max(data[z][y])
                #x=np.median(a)
                rho,theta=cartesian2Polar(int(x)*factorCorretion,int(y)*0.9)
                f[aux][0]=rho
                f[aux][1]=theta
                f[aux][2]=int(z)*20
                f[aux][3]=0.0
                f[aux][4]=float("{:.2f}".format(data[z][y][x]/254))
                f[aux][5]=0.0
                content=str(f[aux][0])+' '+str(f[aux][1])+' '+str(f[aux][2])+' '+str(f[aux][3])+' '+str(f[aux][4])+' '+str(f[aux][5])
                file.write(content)
                file.write('\n')
                aux+=1

file.close()
print("Loading a point cloud")
pcd = o3d.io.read_point_cloud('/home/guilherme/Documents/data.txt',format='xyzrgb')
print(pcd)
print(np.asarray(pcd.points))
o3d.visualization.draw_geometries([pcd],
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])