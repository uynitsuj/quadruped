
import math

import numpy as np

class Leg:
    def __init__(self, origin):
        self.init_origin = origin
        self.origin = origin
        self.h_rad = None
        self.s_rad = None
        self.w_rad = None
        #local (relative to leg origin - hip rotator joint)
        self.x = None
        self.y = None
        self.z = None
        #global (relative to Quadruped origin)
        self.g_x = None
        self.g_y = None
        self.g_z = None
    def __str__(self):
        return f'origin: {self.origin}, angles: [hip: {math.degrees(self.h_rad)}, shoulder: {math.degrees(self.s_rad)}, wrist: {math.degrees(self.w_rad)}], endpoint: {(self.x, self.y, self.z)}'

class InverseKinematics:
    def __init__(self, wrist, shoulder, body_dim, hip_offset):
        '''
        body_dim: (length, width, thickness) in mm
        '''
        self.wrist = wrist
        self.shoulder = shoulder
        self.body_dim = body_dim
        self.hip_offset = hip_offset  # z, y
        self.joint_angles = []
    def engine(self, legs_xyz):
        '''
        IK engine
        '''
        try:
            joint_angles = []
            for i, (x, y, z) in enumerate(legs_xyz):
                h1 = math.sqrt(self.hip_offset[0]**2 + self.hip_offset[1]**2)
                h2 = math.sqrt(z**2 + y**2)
                alpha_0 = math.atan(y / z)
                alpha_1 = math.atan(self.hip_offset[1] / self.hip_offset[0])
                alpha_2 = math.atan(self.hip_offset[0] / self.hip_offset[1])
                alpha_3 = math.asin(
                    h1 * math.sin(alpha_2 + math.radians(90)) / h2)
                alpha_4 = math.radians(90) - alpha_3 - alpha_2
                alpha_5 = alpha_1 - alpha_4
                theta_h = alpha_0 - alpha_5

                r0 = h1 * math.sin(alpha_4) / math.sin(alpha_3)
                h = math.sqrt(r0**2 + x**2)
                phi = math.asin(x / h)
                theta_s = math.acos(
                    (h**2 + self.shoulder**2 - self.wrist**2) / (2 * h * self.shoulder)) - phi
                theta_w = math.acos((self.wrist**2 + self.shoulder **
                                     2 - h**2) / (2 * self.wrist * self.shoulder))

                if i < 2:
                    joint_angles.append((theta_h, theta_s, theta_w))
                else:
                    joint_angles.append((-theta_h, theta_s, theta_w))
            self.joint_angles = joint_angles
        except:
            print("Out of bounds.")
        return self.joint_angles
