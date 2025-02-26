import os
from multiprocessing import Process
from multiprocessing import Manager
from multiprocessing import Lock
import multiprocessing
from multiprocessing import Event
from multiprocessing.managers import BaseManager
from src.sharedata import Sharedata, ShareDataProxy
from src.explorer import Explorer
import yaml
import torch
from src.fusion import Fusion
from src.FedAVG import FedAVG
from ctypes import c_bool
import argparse
import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s %(name)s %(filename)s [line:%(lineno)d] - %(message)s"
logging.basicConfig(filename='multi_slam.log',format=LOG_FORMAT,level=logging.DEBUG)


class Explorer_single():
    '''
    entry class for different agents, shared data, federated center and fusion center
    '''
    def __init__(self, configer, configer_0, configer_1, conf) -> None:
        BaseManager.register('ShareData', Sharedata, ShareDataProxy)
        manager = BaseManager()
        manager.start()
        self.share_data_one = manager.ShareData()
        self.share_data_two = manager.ShareData()

        self.event_one = Event()  # default False after instance
        self.event_one.set()
        self.event_two = Event()
        self.event_two.set()
        
        
        self.fed_average = Manager().Value(c_bool, False)
        self.end_one = Manager().Value(c_bool, False)
        self.end_two = Manager().Value(c_bool, False)

        self.explorer_one = Explorer(configer_0, device='cuda:0', conf=conf, name='Agent_0', agent_id=0)
        self.explorer_two = Explorer(configer_1, device='cuda:1', conf=conf, name='Agent_1', agent_id=1)
        self.fusion = Fusion(configer, configer_0, configer_1, device='cuda:2')

        self.feder = FedAVG(device='cuda:2') 
    def run(self):
        '''
        define local and central Locks to avoid process conflicts.
        '''
        print('Parent process %s.' % os.getpid())
        l_des = Lock()
        l_map_one = Lock()
        l_map_two = Lock()
        
        p_one = Process(target=self.explorer_one.slam, args=(l_des,l_map_one, self.share_data_one, self.fed_average, self.end_one,  self.event_one))
        p_two = Process(target=self.explorer_two.slam, args=(l_des, l_map_two, self.share_data_two, self.fed_average, self.end_two, self.event_two))
        p_fusion = Process(target=self.fusion.multi_fusion, args=(l_des, l_map_one, l_map_two, self.share_data_one, self.share_data_two, self.end_one, self.end_two))
        p_fed = Process(target=self.feder.federate, args=(self.share_data_one, self.share_data_two, self.event_one, self.event_two))
        
        p_one.start()
        p_two.start()
        p_fusion.start()
        p_fed.start()
        p_one.join()
        p_two.join()
        p_fusion.join()
        p_fed.join()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default='configs/replica.yaml', help="overall config")
    parser.add_argument("--config_multi_0", default='configs/multi_config/room0_0.yaml', help="multi config 0")
    parser.add_argument("--config_multi_1", default='configs/multi_config/room0_1.yaml', help="multi config 1")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    
    assert os.path.exists(args.config), 'Cannot find config files!!!'

    with open(args.config, 'r') as f:
        configer = yaml.safe_load(f)
        print('\033[1;32m Load configer successfully \033[0m')

    with open(args.config_multi_0, 'r') as f:
        configer_0 = yaml.safe_load(f)
        print('\033[1;32m Load configer successfully \033[0m')

    with open(args.config_multi_1, 'r') as f:
        configer_1 = yaml.safe_load(f)
        print('\033[1;32m Load configer successfully \033[0m')
 

    conf = {
        'checkpoint_path': './checkpoint/TokyoTM_struct.mat',
        'whiten': True
    }
    torch.multiprocessing.set_start_method('spawn')
    explorer_single = Explorer_single(configer, configer_0, configer_1, conf)
    explorer_single.run()