#!/usr/bin/python3

import open3d as o3d
import numpy as np

print("Loading a point cloud")
pcd = o3d.io.read_point_cloud('dataFilter.xyz',format='xyz')

pcd = pcd.voxel_down_sample(voxel_size=10)
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
print(pcd)

with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as mm:
    labels = np.array(
        pcd.cluster_dbscan(eps=100, min_points=5, print_progress=True))

radii = [70, 20, 40, 80]
rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
    pcd, o3d.utility.DoubleVector(radii))
o3d.visualization.draw_geometries([rec_mesh])