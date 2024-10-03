import torch
import yaml
import numpy as np


def align(model, data):
    """Align two trajectories using the method of Horn (closed-form).

    Args:
        model -- first trajectory (3xn)
        data -- second trajectory (3xn)

    Returns:
        rot -- rotation matrix (3x3)
        trans -- translation vector (3x1)
        trans_error -- translational error per point (1xn)

    """
    np.set_printoptions(precision=3, suppress=True)
    model_zerocentered = model - model.mean(1)
    data_zerocentered = data - data.mean(1)

    W = np.zeros((3, 3))
    for column in range(model.shape[1]):
        W += np.outer(model_zerocentered[:,
                         column], data_zerocentered[:, column])
    U, d, Vh = np.linalg.linalg.svd(W.transpose())
    S = np.matrix(np.identity(3))
    if (np.linalg.det(U) * np.linalg.det(Vh) < 0):
        S[2, 2] = -1
    rot = U*S*Vh
    trans = data.mean(1) - rot * model.mean(1)

    model_aligned = rot * model + trans
    np.savetxt('rot_tmp.txt', rot)
    np.savetxt('trans_tmp.txt',trans)
    alignment_error = model_aligned - data

    trans_error = np.sqrt(np.sum(np.multiply(
        alignment_error, alignment_error), 0)).A[0]

    return rot, trans, trans_error

def calc_eval(gt, pred):
    gt_trans = np.matrix(gt[:, :3, 3]).transpose()
    pred_trans = np.matrix(pred[:, :3, 3]).transpose()
    rot, trans, trans_error = align(gt_trans, pred_trans)
    
    # print(trans_error.shape)
    # print(trans_error)
    rmse = np.sqrt(np.dot(trans_error, trans_error) / len(trans_error))
    mean = np.mean(trans_error)
    median = np.median(trans_error)
    print('rmse_seq:',rmse)
    print('mean_seq:',mean)
    print('median_seq:',median)

    return rmse, mean, median



output_path = 'output_room0'
gt_pose_all = np.loadtxt('eval_room0/traj.txt').reshape(-1, 4, 4)
print(gt_pose_all.shape)

segs = [(0,1100),(900,2000)]
gt_poses = []
for seg in segs:
    poses_mat = gt_pose_all[seg[0]:seg[1]]
    # print(poses_mat.shape)
    # print(poses_mat.shape)
    gt_poses.append(poses_mat)

# exit(0)
gt_poses = np.concatenate(gt_poses,axis=0)
print(gt_poses.shape)

out_trajs_1 = torch.load(output_path + '/pgo_traj_1.pt', map_location='cpu').numpy()
out_trajs_2 = torch.load(output_path + '/pgo_traj_2.pt', map_location='cpu').numpy()
pred_poses = np.concatenate([out_trajs_1,out_trajs_2],axis=0)
# print(gt_poses.shape)

# print(out_trajs_1.shape)
# print(out_trajs_2.shape)
# pred_poses = [out_trajs_1,out_trajs_2]

# results_1 = calc_eval(gt_poses[0], pred_poses[0])
# results_2 = calc_eval(gt_poses[1], pred_poses[1])

# result_final = (np.array(results_1) + np.array(results_2)) / 2.0

result_final = calc_eval(gt_poses, pred_poses)

print('rmse(cm):',result_final[0] * 100)
print('mean(cm):',result_final[1] * 100)
print('median(cm):',result_final[2] * 100)