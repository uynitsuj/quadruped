from numpy import *  # imports all function so we don't have to use np.function()
import math
import pyqtgraph.opengl as gl
import pyqtgraph as pg
# class defines robot joint vertices and stores & plots vertex definition
# in cartesian space relative to the origin of the base frame
# those vertices get plotted within MPL's 3d visualization plotter using their plot function.


class Quadruped:

    def __init__(self, ax=0, origin=(0, 0, 100), body_dim=(230, 110), limb_lengths=(107, 130), offsets=(10, 30), height=170):
        '''
        body_dim: (length, width,thickness) in mm
        limb_lengths: (upper_arm, bottom_arm) in mm
        offsets: (z_offset, y_offset) in mm
        '''
        self.ax = ax
        self.body_dim = body_dim
        self.limb_lengths = limb_lengths
        self.offsets = offsets
        self.init_origin = origin
        self.origin = origin
        self.yaw = 0
        self.pitch = 0
        self.roll = 0
        self.del_x = 0
        self.del_y = 0
        self.del_z = 0
        self.height = height

        #list of tuples of body frame coordinates in R3 cartesian
        #Order: 0-Front Right, 1-Back Right, 2-Back Left, 3-Front Left
        self.body = [

                     (origin[0] - self.body_dim[0] / 2,
                      origin[1] - self.body_dim[1] / 2, origin[2]),
                     (origin[0] + self.body_dim[0] / 2,
                      origin[1] - self.body_dim[1] / 2, origin[2]),
                     (origin[0] + self.body_dim[0] / 2,
                      origin[1] + self.body_dim[1] / 2, origin[2]),
                     (origin[0] - self.body_dim[0] / 2,
                      origin[1] + self.body_dim[1] / 2, origin[2]),
                     (origin[0] - self.body_dim[0] / 2,
                      origin[1] - self.body_dim[1] / 2, origin[2])

                      ]

        self.body_reset = [

                     (origin[0] - self.body_dim[0] / 2,
                      origin[1] - self.body_dim[1] / 2, origin[2]),
                     (origin[0] + self.body_dim[0] / 2,
                      origin[1] - self.body_dim[1] / 2, origin[2]),
                     (origin[0] + self.body_dim[0] / 2,
                      origin[1] + self.body_dim[1] / 2, origin[2]),
                     (origin[0] - self.body_dim[0] / 2,
                      origin[1] + self.body_dim[1] / 2, origin[2]),
                     (origin[0] - self.body_dim[0] / 2,
                      origin[1] - self.body_dim[1] / 2, origin[2])

                      ]

    def IK(self, leg, xyz_wf):
        try:
            x = xyz_wf[0]-self.body[leg][0]
            if leg < 2:
                y = xyz_wf[1]-self.body[leg][1]
            else:
                y = self.body[leg][1]-xyz_wf[1]
            z = xyz_wf[2]-self.body[leg][2]
            off0 = self.offsets[0]
            off1 = self.offsets[1]
            s = self.limb_lengths[0]
            w = self.limb_lengths[1]
            h1 = sqrt(off0**2+off1**2)
            h2 = sqrt(z**2+y**2)
            a0 = arctan(y/z)
            a1 = arctan(off1/off0)
            a2 = arctan(off0/off1)
            a3 = arcsin(h1*sin(a2+pi/2)/h2)
            a4 = pi/2-(a3+a2)
            a5 = a1-a4
            r0=h1*sin(a4)/sin(a3)
            h3 = sqrt(r0**2+x**2)
            phi = arcsin(x / h3)
            t_h = a0-a5
            t_w = arccos((s**2+w**2-h3**2)/(2*s*w))
            t_s = arccos((s**2+h3**2-w**2)/(2*s*h3)) - phi
            if leg < 2:
                return t_h, t_s, t_w
            else:
                return -t_h, t_s, t_w
        except:
            print("Out of bounds.")
        return 0,0,0


    def draw_body(self):
        x_data = [vector[0] for vector in self.body]
        y_data = [vector[1] for vector in self.body]
        z_data = [vector[2] for vector in self.body]
        pts = vstack([x_data, y_data, z_data]).transpose()
        self.ax.w.addItem(gl.GLLinePlotItem(pos=pts, color=pg.glColor((4, 50)), width=1, antialias=True))

    @staticmethod
    def translate(delx, dely, delz):
        return [[1,0,0,delx],
                [0,1,0,dely],
                [0,0,1,delz],
                [0,0,0,1]]

    @staticmethod
    def rotate(yaw, pitch, roll):
        return [[cos(yaw)*cos(pitch),
        cos(yaw)*sin(pitch)*sin(roll)-sin(yaw)*cos(roll),
        cos(yaw)*sin(pitch)*cos(roll)+sin(yaw)*sin(roll),0],


        [sin(yaw)*cos(pitch),
        sin(yaw)*sin(pitch)*sin(roll)+cos(yaw)*cos(roll),
        sin(yaw)*sin(pitch)*cos(roll)-cos(yaw)*sin(roll),0],


        [-sin(pitch),
        cos(pitch)*sin(roll),
        cos(pitch)*cos(roll),0],
        [0,0,0,1]]

    def draw_legs(self, f_c):
        for i in range(0,4):
            pol1=1
            pol2=1
            if i < 2:
                pol1=-1
                pol2 = 0
            xyz = (f_c[i][0],f_c[i][1],f_c[i][2])
            t_h, t_s, t_w = Quadruped.IK(self, i,xyz)
            M1F = dot(Quadruped.translate(self.body[i][0],self.body[i][1],self.body[i][2]),
            Quadruped.rotate(self.yaw, self.pitch, -t_h))
            p1 = dot(M1F, Quadruped.translate(0,0,-self.offsets[0]))
            p2 = dot(p1, Quadruped.translate(0,pol1*self.offsets[1],0))
            M2F = dot(p2, dot(Quadruped.rotate(0,t_s+pi*pol2,0),
            Quadruped.translate(0,0,pol1*self.limb_lengths[0])))
            leg_pts = array([

            [M1F[0][3],M1F[1][3],M1F[2][3]],
            [p1[0][3], p1[1][3], p1[2][3]],
            [p2[0][3], p2[1][3], p2[2][3]],
            [M2F[0][3],M2F[1][3],M2F[2][3]],
            [f_c[i][0],f_c[i][1],f_c[i][2]]

            ])
            self.ax.w.addItem(gl.GLLinePlotItem(pos=leg_pts, color=pg.glColor((4, 100)), width=3, antialias=True))
            self.ax.w.addItem(gl.GLScatterPlotItem(pos=leg_pts, color=pg.glColor((4, 5)), size=7))


    def shift_body_rotation(self, yaw, pitch, roll):
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        for i, vector in enumerate(self.body):
            P = dot(Quadruped.translate(0, 0, self.body_reset[i][2]),
            dot(Quadruped.rotate(self.yaw, self.pitch, self.roll),
            Quadruped.translate(self.body_reset[i][0],self.body_reset[i][1],0)))
            self.body[i] = (P[0][3], P[1][3], P[2][3])

    def shift_body_translation(self, dx, dy, dz):
        self.del_x = dx
        self.del_y = dy
        self.del_z = dz
        for i, vector in enumerate(self.body):
            P = dot(Quadruped.translate(self.del_x, self.del_y, self.del_z),
            Quadruped.translate(self.body[i][0],self.body[i][1],self.body[i][2]))

            self.body[i] = (P[0][3], P[1][3], P[2][3])

    def reset(self, reset):
        if reset == 1:
            print("reset")
            for i, vector in enumerate(self.body):
                self.body[i] = (self.body_reset[i][0],self.body_reset[i][1],self.body_reset[i][2])
