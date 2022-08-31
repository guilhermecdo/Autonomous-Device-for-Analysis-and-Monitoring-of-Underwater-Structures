#!/usr/bin/python3

import open3d as o3d

print("Loading a point cloud")
pcd = o3d.io.read_point_cloud('data.xyz',format='xyz')
print(pcd)
#o3d.visualization.draw_geometries([pcd])

downpcd = pcd.voxel_down_sample(voxel_size=25)
print(downpcd)
o3d.visualization.draw_geometries([downpcd])