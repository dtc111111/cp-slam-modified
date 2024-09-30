import torch
import yaml
from src.optimizer import Optimizer
from data.dataloader import *
from torch.utils.data import DataLoader
from src.frame import Frame
import camera.camera as camera
import matplotlib

def dataloader_choice(cfg, device):
        if cfg['name'] == 'replica':
            dataset = ReplicaDataset(cfg, device)
            dataloader = DataLoader(dataset)
        elif cfg['name'] == 'scannet':
            dataset = ScannetDataset(cfg, device)
            dataloader = DataLoader(dataset)
        elif cfg['name'] == 'apartment':
            dataset = ApartmentDataset(cfg, device)
            dataloader = DataLoader(dataset)
        else:
            dataset = SelfmakeDataset(cfg, device)
            dataloader = DataLoader(dataset)
        return dataloader



cmap = matplotlib.colormaps.get_cmap('Spectral')

device = 'cuda:0'
output_path = 'output_room0'
optimizer = torch.load(output_path + '/optimizer.pt',map_location=device)
optimizer.device = device
feature_map = torch.load(output_path + '/pgo_feature_map.pt',map_location=device)
total_map = torch.load(output_path + '/pgo_map.pt',map_location=device)
source_table = torch.load(output_path + '/pgo_source_table.pt',map_location=device)

trajs = []
cfgs = []
save_paths = []
trajs.append(torch.load(output_path + '/pgo_traj_1.pt',map_location=device))
trajs.append(torch.load(output_path + '/pgo_traj_2.pt',map_location=device))
save_paths.append(output_path + '/imgs_1')
save_paths.append(output_path + '/imgs_2')

with open('configs/multi_config/room0_0.yaml', 'r') as f:
    cfgs.append(yaml.safe_load(f))
    print('\033[1;32m Load configer successfully \033[0m')
with open('configs/multi_config/room0_1.yaml', 'r') as f:
    cfgs.append(yaml.safe_load(f))
    print('\033[1;32m Load configer successfully \033[0m')
optimizer.net_to_eval()

for cfg_id, cfg in enumerate(cfgs):
    traj = trajs[cfg_id]
    dataloader = dataloader_choice(cfg, device)
    camera_rgbd = camera.Camera(cfg, device)
    save_path = save_paths[cfg_id]
    for iter, data in enumerate(dataloader):
        color_img = data['color_img'].to(device).squeeze().clone().detach().float()
        depth_img = data['depth_img'].to(device).squeeze().clone().detach().float() / cfg['camera']['png_depth_scale']

        frame = Frame(cfg, color_img, depth_img)
        frame.pose = traj[iter]
        depth_value_non_zero = frame.depth[frame.depth!=0]
        depth_max, depth_min = torch.max(depth_value_non_zero), torch.min(depth_value_non_zero)
        frame.near, frame.far = depth_min, depth_max

        depth, color = optimizer.viz(frame, camera_rgbd, total_map, feature_map, device)
        # print(color.shape)
        # print(depth_.shape)
        depth_show = (depth - depth.min()) / (depth.max() - depth.min()) * 255.0
        depth_show = depth_show.astype(np.uint8)
        depth_show = (cmap(depth_show)[:, :, :3] * 255)[:, :, ::-1].astype(np.uint8)
        cv2.imwrite('depth_show.png', depth_show)
        cv2.imwrite('color_show.png', color)
        np.save('{}/{:d}_depth.npy'.format(save_path,iter), depth)
        np.save('{}/{:d}_color.npy'.format(save_path,iter), color)
        # exit(0)
        print('finish:',iter)
    