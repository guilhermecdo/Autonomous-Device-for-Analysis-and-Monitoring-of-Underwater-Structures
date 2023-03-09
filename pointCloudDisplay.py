#!/usr/bin/python3

import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

print("Loading a point cloud")
pcd = o3d.io.read_point_cloud('dataNoFilter.xyz',format='xyz')
print('No filtering pcd')
print(pcd)
o3d.visualization.draw_geometries([pcd])

pcd = o3d.io.read_point_cloud('dataFilter.xyz',format='xyz')
print('Filtering pcd')
print(pcd)
o3d.visualization.draw_geometries([pcd])

pcd = pcd.voxel_down_sample(voxel_size=5)
print('Voxel filtering pcd')
print(pcd)
o3d.visualization.draw_geometries([pcd])

with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as mm:
    labels = np.array(
        pcd.cluster_dbscan(eps=100, min_points=5, print_progress=True))

max_label = labels.max()
print(f"point cloud has {max_label + 1} clusters")
colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
colors[labels < 0] = 0
pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
print('CLUSTER')
print(pcd)
o3d.visualization.draw_geometries([pcd])