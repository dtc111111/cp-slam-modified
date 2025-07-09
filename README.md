<!--   CP-SLAM-Modified   -->
<p align="center">
  <a href="">
    <img src="https://raw.githubusercontent.com/hjr37/open_access_assets/main/cp-slam/images/logo-1.jpg" alt="Logo" width="75%">
  </a>
</p>
<p align="center">
  <h1 align="center">CP-SLAM: Collaborative Neural Point-based SLAM System[NeurIPS'24] (Unofficial Modified)</h1>
  <div align="center"></div>
</p>

<p align="left">
  <p style="text-align: justify;">This is the unofficial implementation of CP-SLAM: Collaborative Neural Point-based SLAM System. The original CP-SLAM code contained certain issues that hindered its proper functionality. We have addressed and resolved these issues to ensure correct operation.<strong> Additionally, we provided further details on the execution steps and added code for the evaluation section. </strong> CP-SLAM system demonstrates remarkable capabilities in multi-agent deployment and achieves state-of-the-art performance in tracking, map construction, and rendering.</p>
  <a href="">
    <img src="https://raw.githubusercontent.com/hjr37/open_access_assets/main/cp-slam/images/pipeline.jpg" alt="CP-SLAM pipeline" width="100%">
  </a>
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/hjr37/open_access_assets/main/cp-slam/video/single.gif" alt="Single GIF" width="48%">
  <img src="https://raw.githubusercontent.com/hjr37/open_access_assets/main/cp-slam/video/collaboration.gif" alt="Collaboration GIF" width="48%">
</p>

<!-- TABLE OF CONTENTS -->
<details open="open" style='padding: 10px; border-radius:5px 15px 15px 5px; border-style: solid; border-width: 1px;'>
  <summary><strong>Table of Contents</strong></summary>
  <ol>
    <li>
      <a href="#News">News</a>
    </li>
    <li>
      <a href="#Dataset Download Link">Dataset Download Link</a>
    </li>
    <li>
      <a href="#installation">Installation</a>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ol>
        <li><a href="#run">Run</a></li>
        <li><a href="#evaluation">Evaluation</a></li>
      </ol>
    </li>
    <li>
      <a href="#Acknowledgement">Acknowledgement</a>
    </li>
    <li>
      <a href="#Citation">Citation</a>
    </li>
  </ol>
</details>

# Dataset Download Link
<p style="text-align: justify;">
We provide the <a href="https://huggingface.co/datasets/wssy37/CP-SLAM_dataset">Download link</a> to

- Four single-agent trajectories. Each contains 1500 RGB-D frames.
- Four two-agent trajectories. Each  is divided into 2 portions, holding 2500 frames, with the exception of Office-0 which includes 1950 frames per part.
- Two pre-trained NetVLAD models for the loop detection module. 
</p>

# Installation

- ###  Configure the environment in one line
```bash
conda env create -f env.yaml
conda activate cp-slam
```


# Usage

## Run
Create the output directory and modify the corresponding configuration file in multi_config.
```bash
python multi_slam.py --config configs/replica.yaml --config_multi_0 configs/multi_config/room0_0.yaml --config_multi_1 configs/multi_config/room0_1.yaml
```
## Evaluation
```bash
python re_render.py 
python eval.py
python eval_recon.py
```
# Citation
```
@misc{hu2023cpslam,
      title={CP-SLAM: Collaborative Neural Point-based SLAM System}, 
      author={Jiarui Hu and Mao Mao and Hujun Bao and Guofeng Zhang and Zhaopeng Cui},
      year={2023},
      eprint={2311.08013},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}

@article{deng2025mcnslammultiagentcollaborativeneural,
      title={MCN-SLAM: Multi-Agent Collaborative Neural SLAM with Hybrid Implicit Neural Scene Representation}, 
      author={Tianchen Deng and Guole Shen and Xun Chen and Shenghai Yuan and Hongming Shen and Guohao Peng and Zhenyu Wu and Jingchuan Wang and Lihua Xie and Danwei Wang and Hesheng Wang and Weidong Chen},
      journal={arXiv preprint arXiv:2506.18678},
      year={2025},
}

@inproceedings{deng2025mne,
  title={Mne-slam: Multi-agent neural slam for mobile robots},
  author={Deng, Tianchen and Shen, Guole and Xun, Chen and Yuan, Shenghai and Jin, Tongxin and Shen, Hongming and Wang, Yanbo and Wang, Jingchuan and Wang, Hesheng and Wang, Danwei and others},
  booktitle={Proceedings of the Computer Vision and Pattern Recognition Conference},
  pages={1485--1494},
  year={2025}
}
```
