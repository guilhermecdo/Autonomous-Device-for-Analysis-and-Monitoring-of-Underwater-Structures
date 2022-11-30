#!/usr/bin/python3

import open3d as o3d
import numpy as np

print("Loading a point cloud")
pcd = o3d.io.read_point_cloud('dataFilter.xyz',format='xyz')

pcd = pcd.voxel_down_sample(voxel_size=5)
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
print(pcd)

with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as mm:
    labels = np.array(
        pcd.cluster_dbscan(eps=100, min_points=5, print_progress=True))

alpha = 25
print(f"alpha={alpha:.3f}")
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
mesh.compute_vertex_normals()
print(mesh)
o3d.visualization.draw_geometries([mesh])