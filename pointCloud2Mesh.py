#!/usr/bin/python3

import open3d as o3d

print("Loading a point cloud")
pcd = o3d.io.read_point_cloud('data.xyz',format='xyz')

pcd = pcd.voxel_down_sample(voxel_size=20)
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
print(pcd)

alpha = 100000000000000000000
print(f"alpha={alpha:.3f}")
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
mesh.compute_vertex_normals()
print(mesh)
o3d.visualization.draw_geometries([mesh],)
#mesh_show_back_face=True