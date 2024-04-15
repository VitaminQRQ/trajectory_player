#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import pandas as pd
import numpy as np

from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp

from geometry_msgs.msg import Pose as ROSPose  # 重命名避免冲突
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState


class CustomPose:  # 改名避免冲突
    def __init__(self, position, orientation):
        self.position = np.array(position)
        self.orientation = R.from_quat(orientation)

    def interpolate_pose(self, other, t):
        # 线性插值位置
        interp_pos = (1 - t) * self.position + t * other.position
        
        # 创建一个包含两个旋转的Rotation对象
        rotations = R.from_quat([
            self.orientation.as_quat(), 
            other.orientation.as_quat()
        ])
        
        # 假设pose1对应时间0，pose2对应时间1
        times = [0, 1]  
        
        # 创建Slerp插值器
        slerp = Slerp(times, rotations)
        
        # 使用slerp进行插值
        interp_orient = slerp([t])
        
        return CustomPose(interp_pos, interp_orient.as_quat()[0])
    
    def to_ros_pose(self):
        pose = ROSPose()
        pose.position.x, pose.position.y, pose.position.z = self.position
        quat = self.orientation.as_quat()
        pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w = quat
        return pose

class TrajectoryDisplay:
    def __init__(self):
        rospy.init_node('trajectory_display')

        data_path = rospy.get_param('~data_path')
        model_name = rospy.get_param('~model_name', 'hmmwv')  
        data_interval = rospy.get_param('~data_interval', 0.1)
        discrete_num = rospy.get_param('~discrete_num', 10)
        loop_flag = rospy.get_param('~loop_flag', True)  
          
        self.df = pd.read_csv(data_path)
        self.model_state_pub = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        self.data_interval = data_interval
        self.discrete_num = discrete_num
        self.model_name = model_name
        self.loop_flag = loop_flag
        
    def play(self):
        frequency = 1 * self.discrete_num / self.data_interval
        print('frequency = ', frequency, ' Hz')
        
        rate = rospy.Rate(frequency)
        while not rospy.is_shutdown():
            for i in range(len(self.df) - 1):
                pose1_df = self.df.iloc[i]
                pose2_df = self.df.iloc[i + 1]
                
                pose1 = CustomPose(
                    [pose1_df['x'], pose1_df['y'], pose1_df['z']], 
                    [pose1_df['qx'], pose1_df['qy'], pose1_df['qz'], pose1_df['qw']]
                )
                
                pose2 = CustomPose(
                    [pose2_df['x'], pose2_df['y'], pose2_df['z']], 
                    [pose2_df['qx'], pose2_df['qy'], pose2_df['qz'], pose2_df['qw']]
                )
                
                # for t in np.arange(0, 1, 0.1):
                for t in np.linspace(0, 1, self.discrete_num):
                    interpolated_pose = pose1.interpolate_pose(pose2, t)
                    model_state = ModelState()
                    model_state.model_name = self.model_name
                    model_state.pose = interpolated_pose.to_ros_pose()
                    
                    try:
                        self.model_state_pub(model_state)
                    except rospy.ServiceException as e:
                        rospy.logerr("Service call failed: %s" % e)
                    
                    rate.sleep()
                    
            if not self.loop_flag:
                break
            
            rospy.loginfo("Restarting trajectory")
        
        rospy.loginfo("Bye.")

if __name__ == '__main__':
    player = TrajectoryDisplay()
    player.play()