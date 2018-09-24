import numpy as np
import tensorflow as tf
import tensorflow.contrib.eager as tfe
tf.enable_eager_execution()
import matplotlib
matplotlib.use('tkAgg')
import matplotlib.pyplot as plt
from trajectory.spline.spline_3rd_order import Spline3rdOrder

def test_spline_3rd_order(visualize=False):
    np.random.seed(seed=1)
    n=5
    dt = .01
    k = 100

    target_state = np.random.uniform(-np.pi, np.pi, 3)
    v0 = np.random.uniform(0., 0.5, 1)[0] # Initial speed
    vf = 0.

    start = [0., 0., 0., v0, 0.]
    goal = [target_state[0], target_state[1], target_state[2], 0., 0.]

    start_n5 = np.tile(start, n).reshape((n,5))
    goal_n5 = np.tile(goal, n).reshape((n,5))
    
    start_n5 = tf.constant(start_n5, name='start', dtype=tf.float32)
    goal_n5 = tfe.Variable(goal_n5, name='goal', dtype=tf.float32)

    ts_nk = tf.tile(tf.linspace(0., dt*k, k)[None], [n,1])
    spline_traj = Spline3rdOrder(dt=dt, k=k, n=n, start_n5=start_n5)
    spline_traj.fit(goal_n5=goal_n5, factors_n2=None)
    spline_traj.eval_spline(ts_nk, calculate_speeds=True)
    
    pos_nk3 = spline_traj.position_and_heading_nk3()
    v_nk1 = spline_traj.speed_nk1()
    start_pos_diff = (pos_nk3 - start_n5[:,None,:3])[:,0]
    goal_pos_diff = (pos_nk3 - goal_n5[:,None,:3])[:,-1]
    assert(np.allclose(start_pos_diff, np.zeros((n, 3)), atol=1e-6)) 
    assert(np.allclose(goal_pos_diff, np.zeros((n, 3)), atol=1e-6)) 
   
    start_vel_diff = (v_nk1 - start_n5[:,None,3:4])[:,0]
    goal_vel_diff = (v_nk1 - goal_n5[:,None,3:4])[:,-1]
    assert(np.allclose(start_vel_diff, np.zeros((n,1)), atol=1e-6)) 
    assert(np.allclose(goal_vel_diff, np.zeros((n,1)), atol=1e-6)) 

    if visualize: 
        fig = plt.figure()
        ax = fig.add_subplot(111)
        spline_traj.render(ax, freq=4)
        plt.show()

if __name__ == '__main__':
    test_spline_3rd_order(visualize=True)

