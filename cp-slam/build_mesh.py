import torch
import cv2
import numpy as np
import yaml
import open3d as o3d
import camera.camera as camera

device = 'cpu'

scale = 1.0
volume = o3d.pipelines.integration.ScalableTSDFVolume(
    voxel_length=5.0 * scale / 512.0,
    sdf_trunc=0.04 * scale,
    color_type=o3d.pipelines.integration.TSDFVolumeColorType.RGB8)


output_path = 'output_room0'
cfgs = []
trajs = []
prefixs = []
with open('configs/multi_config/room0_0.yaml', 'r') as f:
    cfgs.append(yaml.safe_load(f))
    prefixs.append(output_path + '/imgs_1')
with open('configs/multi_config/room0_1.yaml', 'r') as f:
    cfgs.append(yaml.safe_load(f))
    prefixs.append(output_path + '/imgs_2')

trajs.append(torch.load(output_path + '/pgo_traj_1.pt',map_location=device))
trajs.append(torch.load(output_path + '/pgo_traj_2.pt',map_location=device))

for cfg_id, traj in enumerate(trajs):
    print('processing seq:',cfg_id)
    seq_len = traj.shape[0]
    print(seq_len)
    # camera_now = camera.Camera(cfgs[cfg_id], device)
    cfg_cam = cfgs[cfg_id]['camera']
    intrinsic = o3d.camera.PinholeCameraIntrinsic(cfg_cam['W'], cfg_cam['H'], cfg_cam['fx'], cfg_cam['fy'], cfg_cam['cx'], cfg_cam['cy'])
    print(intrinsic)
    prefix = prefixs[cfg_id]
    for frame_id in range(seq_len):
        print('frame:',frame_id)
        c2w = traj[frame_id].numpy()
        w2c = np.linalg.inv(c2w)
        # print(c2w)
        color_img = np.load(prefix + '/' + str(frame_id) + '_color.npy')[...,::-1].copy()
        depth_img = np.load(prefix + '/' + str(frame_id) + '_depth.npy')
        # print(color_img)
        # print(color_img.shape)
        # print(depth_img.shape)
        # print(depth_img)
        depth_img = depth_img.astype(np.float32) / cfg_cam['png_depth_scale']
        # print(depth_img)
        depth = o3d.geometry.Image(depth_img)
        color = o3d.geometry.Image(color_img)
        # print(color)
        rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
            color,
            depth,
            depth_scale=1.0,
            depth_trunc=30,
            convert_rgb_to_intensity=False)
        volume.integrate(rgbd, intrinsic, w2c)

o3d_mesh = volume.extract_triangle_mesh()
o3d.io.write_triangle_mesh('out_mesh_room0.ply', o3d_mesh)