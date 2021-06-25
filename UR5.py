from simulation import sim
from simulation import simConst as vrep
import numpy as np
import matplotlib.pyplot as plt
import os
import time

class Robot(object):
    def __init__(self, is_sim, num_obj):
        # 是否是模拟环境
        self.is_sim = is_sim

        if self.is_sim:
            # Define colors for object meshes (Tableau palette)
            self.color_space = np.asarray([[78.0, 121.0, 167.0],  # blue
                                           [89.0, 161.0, 79.0],  # green
                                           [156, 117, 95],  # brown
                                           [242, 142, 43],  # orange
                                           [237.0, 201.0, 72.0],  # yellow
                                           [186, 176, 172],  # gray
                                           [255.0, 87.0, 89.0],  # red
                                           [176, 122, 161],  # purple
                                           [118, 183, 178],  # cyan
                                           [255, 157, 167]]) / 255.0  #pink

            # Read files in object mesh directory
            self.num_obj = num_obj

            # 随机选取物体加入场景
            self.obj_mesh_color = self.color_space[np.asarray(range(self.num_obj)) % 10, :]

            # Remote in vrep
            sim.simxFinish(-1)  # 关闭连接
            self.sim_client = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)  # Connect to V-REP on port 19997
            if self.sim_client == -1:
                print('Failed to connect to simulation (V-REP remote API server). Exiting.')
                exit()
            # else:
            #     print('Connected to simulation.')
            #     self.restart_sim()

            # self.add_objects()

    def add_object(self, shapetype, position, sizes, orientation, color, name):
        # position = [0.1, 0.1, 1]
        # sizes = [0.15, 0.3, 0.2]
        # orientation = [0, 0, 0]
        # color = self.color_space[1].tolist()
        # 添加单个物体
        res, resInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(self.sim_client, "remoteApiCommandServer",
                                                                                    vrep.sim_scripttype_childscript,
                                                                                    'createPureshape_function', [shapetype],
                                                                                    position + sizes + orientation + color,
                                                                                    [name], bytearray(),
                                                                                    vrep.simx_opmode_blocking)

        return res, resInts, retFloats, retStrings, retBuffer


    def OMPL2position(self):
        res, resInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(self.sim_client,
                                                                                    "remoteApiCommandServer",
                                                                                    vrep.sim_scripttype_childscript,
                                                                                    'OMPL2Position',
                                                                                    [],
                                                                                    [],
                                                                                    [], bytearray(),
                                                                                    vrep.simx_opmode_blocking)
        return res, resInts, retFloats, retStrings, retBuffer

    def move2position(self, position):
        """
        将机械臂移动到指定的xyz坐标
        由于关节限制，如果移动不到会移动到最大关节处
        :param position:
        :return:
        """
        res, resInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(self.sim_client,
                                                                                    "remoteApiCommandServer",
                                                                                    vrep.sim_scripttype_childscript,
                                                                                    'MovetoPosition',
                                                                                    [],
                                                                                    position,
                                                                                    [], bytearray(),
                                                                                    vrep.simx_opmode_blocking)

        return res, resInts, retFloats, retStrings, retBuffer

    def suction_open(self):
        """
        打开吸盘
        :return:
        """
        res, resInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(self.sim_client,
                                                                                    "remoteApiCommandServer",
                                                                                    vrep.sim_scripttype_childscript,
                                                                                    'suction_cup_open',
                                                                                    [],
                                                                                    [],
                                                                                    [], bytearray(),
                                                                                    vrep.simx_opmode_blocking)


    def suction_close(self):
        """
        关闭吸盘
        :return:
        """
        res, resInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(self.sim_client,
                                                                                    "remoteApiCommandServer",
                                                                                    vrep.sim_scripttype_childscript,
                                                                                    'suction_cup_close',
                                                                                    [],
                                                                                    [],
                                                                                    [], bytearray(),
                                                                                    vrep.simx_opmode_blocking)

    def get_object(self, name):
        """
        获取指定物体的位姿和大小
            [position,
             oritation,
             size]
        :param name:
        :return:
        """
        res, resInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(self.sim_client,
                                                                                    "remoteApiCommandServer",
                                                                                    vrep.sim_scripttype_childscript,
                                                                                    'GetObject',
                                                                                    [],
                                                                                    [],
                                                                                    [name], bytearray(),
                                                                                    vrep.simx_opmode_blocking)

        return res, resInts, retFloats, retStrings, retBuffer

    def set_object(self, name, PosAndOrt):
        res, resInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(self.sim_client,
                                                                                    "remoteApiCommandServer",
                                                                                    vrep.sim_scripttype_childscript,
                                                                                    'SetObject',
                                                                                    [],
                                                                                    PosAndOrt,
                                                                                    [name], bytearray(),
                                                                                    vrep.simx_opmode_blocking)

        return res, resInts, retFloats, retStrings, retBuffer

    def MoveToJoints(self, joints):
        print(joints)
        res, resInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(self.sim_client,
                                                                                    "remoteApiCommandServer",
                                                                                    vrep.sim_scripttype_childscript,
                                                                                    'MoveToJoints',
                                                                                    [],
                                                                                    joints,
                                                                                    [], bytearray(),
                                                                                    vrep.simx_opmode_blocking)

        return res, resInts, retFloats, retStrings, retBuffer

    def AddToJoints(self, joints):
        res, resInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(self.sim_client,
                                                                                    "remoteApiCommandServer",
                                                                                    vrep.sim_scripttype_childscript,
                                                                                    'AddToJoints',
                                                                                    [],
                                                                                    joints,
                                                                                    [], bytearray(),
                                                                                    vrep.simx_opmode_blocking)

        return res, resInts, retFloats, retStrings, retBuffer

    def GetRGBD(self):
        """
        获取RGBD信息
        :return:
        """
        sim_ret, cam_handle = sim.simxGetObjectHandle(self.sim_client, "Vision_sensor", vrep.simx_opmode_blocking)

        # 获取 RGB Info
        sim_ret, resolution, raw_image = sim.simxGetVisionSensorImage(self.sim_client, cam_handle, 0,
                                                                      vrep.simx_opmode_blocking)
        color_img = np.asarray(raw_image)
        color_img.shape = (resolution[1], resolution[0], 3)
        color_img = color_img.astype(np.float)
        color_img[color_img < 0] += 255
        color_img = np.fliplr(color_img)
        color_img = color_img.astype(np.uint8)

        # 获取 Depth Info
        sim_ret, resolution, depth_buffer = sim.simxGetVisionSensorDepthBuffer(self.sim_client, cam_handle,
                                                                               vrep.simx_opmode_blocking)
        depth_img = np.asarray(depth_buffer)
        depth_img.shape = (resolution[1], resolution[0])
        depth_img = np.fliplr(depth_img)
        zNear = 0.01
        zFar = 2
        # plt.imshow(depth_img)
        # plt.show()
        depth_img = depth_img * (zFar - zNear) + zNear

        return color_img, depth_img

    def add_objects(self):

        # Add each object to robot workspace at x,y location and orientation (random or pre-loaded)
        self.object_handles = []
        sim_obj_handles = []
        for object_idx in range(self.num_obj):
            # curr_mesh_file = os.path.join(self.obj_mesh_dir, self.mesh_list[self.obj_mesh_ind[object_idx]])
            # if self.is_testing and self.test_preset_cases:
            #    curr_mesh_file = self.test_obj_mesh_files[object_idx]
            curr_shape_name = 'shape_%02d' % object_idx
            # drop_x = (self.workspace_limits[0][1] - self.workspace_limits[0][0] - 0.2) * np.random.random_sample() + \
            #          self.workspace_limits[0][0] + 0.1
            # drop_y = (self.workspace_limits[1][1] - self.workspace_limits[1][0] - 0.2) * np.random.random_sample() + \
            #          self.workspace_limits[1][0] + 0.1
            drop_x = 0.2*np.random.random_sample()
            drop_y = 0.2*np.random.random_sample()
            object_position = [drop_x, drop_y, 0.15]
            object_orientation = [2 * np.pi * np.random.random_sample(), 2 * np.pi * np.random.random_sample(),
                                  2 * np.pi * np.random.random_sample()]
            object_sizes = [0.2*np.random.random_sample(), 0.2*np.random.random_sample(), 0.2*np.random.random_sample()]
            # if self.is_testing and self.test_preset_cases:
            #     object_position = [self.test_obj_positions[object_idx][0], self.test_obj_positions[object_idx][1],
            #                        self.test_obj_positions[object_idx][2]]
            #     object_orientation = [self.test_obj_orientations[object_idx][0],
            #                           self.test_obj_orientations[object_idx][1],
            #                           self.test_obj_orientations[object_idx][2]]
            object_color = self.obj_mesh_color[object_idx].tolist()
            res, resInts, retFloats, retStrings, retBuffer = self.add_object(0, object_position, object_sizes, object_orientation, object_color, "obj" + str(object_idx))
            if res == 8:
                print('Failed to add new objects to simulation. Please restart.')
                exit()
            curr_shape_handle = resInts[0]
            self.object_handles.append(curr_shape_handle)
            # if not (self.is_testing and self.test_preset_cases):
            #     time.sleep(2)
        self.prev_obj_positions = []
        self.obj_positions = []

    def set_object_position(self, position, orientation, name, parent):
        # position = [0.1, 0.1, 1]
        # orientation = [0, 0, 0]
        # 物体
        res, resInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(self.sim_client, "remoteApiCommandServer",
                                                                                    vrep.sim_scripttype_childscript,
                                                                                    'setObjectPosition_function', [],
                                                                                    position + orientation,
                                                                                    [name, parent], bytearray(),
                                                                                    vrep.simx_opmode_blocking)



if __name__ == "__main__":

    robot = Robot(True, 10)

    # robot.set_object_position([0.0, 0.4, 0.2], [np.deg2rad(-90), np.deg2rad(-90), 0], 'Dummy', "UR5")
    # robot.set_object_position([-0.2, 0.3, 0.1], [np.deg2rad(-90), 0, np.deg2rad(-90)], 'Dummy', "UR5")
    robot.set_object_position([0, 0, 0.18], [np.deg2rad(-90), 0, np.deg2rad(-90)], 'Dummy', "test_cube")
    robot.OMPL2position()
    robot.suction_close()

    # robot.set_object_position([0.35, -0.675, 0.35], [np.deg2rad(-90), 0, np.deg2rad(-90)], 'Dummy', "UR5")
    # robot.OMPL2position()
    # robot.suction_open()