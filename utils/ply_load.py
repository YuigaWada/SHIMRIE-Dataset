import open3d as o3d
import numpy as np
import json
from tqdm import tqdm


def load(ply_path, colors, sem_seg_path, f_segs_path, out_path):
    mesh = o3d.io.read_triangle_mesh(ply_path)
    pcd = o3d.io.read_point_cloud(ply_path)
    zeros = np.zeros_like(np.asarray(pcd.points))

    # json load
    with open(sem_seg_path) as f_1:
        data = json.load(f_1)

    all_seg_ids = []
    for i in range(len(data['segGroups'])):
        d = data['segGroups'][i]
        all_seg_ids.append((d['segments'], d['label']))

    # seg_ids = data['segGroups'][0]['segments']

    with open(f_segs_path) as f_2:
        mesh_data = json.load(f_2)

    mesh_ids = mesh_data['segIndices']

    mesh_seg_ids = []

    color_map = {}
    cp = 0
    for j, (seg_ids, label) in enumerate(tqdm(all_seg_ids)):
        if label not in color_map:
            color_map[label] = cp
            cp += 1
        for seg_id in seg_ids:
            for i, mesh_id in enumerate(mesh_ids):
                if seg_id == mesh_id:
                    mesh_seg_ids.append(i)

        for mesh_seg_id in mesh_seg_ids:
            point_ids = np.asarray(mesh.triangles)[mesh_seg_id]
            for point_id in point_ids:
                zeros[point_id] = colors[color_map[label]]
        mesh_seg_ids = []

    # colorize
    pcd.colors = o3d.utility.Vector3dVector(zeros)
    mesh.vertex_colors = o3d.utility.Vector3dVector(zeros)

    # save mesh
    o3d.io.write_triangle_mesh(out_path, mesh)
    # color_mesh = o3d.io.read_triangle_mesh(out_path)
    # o3d.visualization.draw_geometries([color_mesh])

    return pcd, mesh

