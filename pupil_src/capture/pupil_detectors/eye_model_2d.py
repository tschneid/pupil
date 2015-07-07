from pyglui.cygl import utils as cygl
import cv2
import numpy as np
class Eye_Model_2d(object):
    """docstring for Eye_Model_2d"""
    def __init__(self,g_pool):
        super(Eye_Model_2d, self).__init__()
        self.g_pool = g_pool
        self.observations = []
        self.lines = []
        self.center =  Center()

    def add_observation(self,ellipse):
        self.observations.append(ellipse)
        angle = np.pi / 180. * ellipse[2]
        direction =  np.cos(angle),np.sin(angle)
        line = [ellipse[0],direction]
        self.lines.append(line)
        ratio =  min(ellipse[1])/max(ellipse[1])
        weight = 1-ratio
        self.center.add_line(line,weight)

    def fit(self):
        pass
        # if len(self.lines)>10:
        #     self.center = nearest_intersect_2D(self.lines)



    def gl_display(self):
        for e in self.observations:
            ratio =  min(e[1])/max(e[1])
            weight = 1-ratio
            color = cygl.RGBA(0.,1.,0,weight)
            angle = np.pi / 180. * e[2]
            x = 1000* np.cos(angle)
            y = 1000* np.sin(angle)

            # pts = cv2.ellipse2Poly( (int(e[0][0]),int(e[0][1])),
            #                                 (int(e[1][0]/2),int(e[1][1]/2)),
            #                                 int(e[2]),0,360,15)
            # cygl.draw_polyline(pts,1,cygl.RGBA(1.,0,0,.5))
            cygl.draw_polyline( [(e[0][0]-x,e[0][1]-y),(e[0][0]+x,e[0][1]+y)] ,0.5,color)
        cygl.draw_points( [self.center.center],color=cygl.RGBA(0.,0.,1,.3))



def dist_pt_line(pt,line):

    d = norm(np.cross(l2-l1, l1-p))/norm(l2-l1)

def nearest_intersect_2D(lines):
    #finds the learest intersection of many lines (which may not be a real intersection)
    #the original nearest_intersect(const Range& lines) function
    #each element in array lines should be geometry.line2D() class
    A = np.zeros((2,2))
    b = np.zeros((2,1))
    Ivv = [] #vector of matrices
    for line in lines:
        vi = np.asmatrix(line[1])
        vi = np.reshape(vi,(2,1))
        pi = np.asmatrix(line[0])
        pi = np.reshape(pi,(2,1))
        Ivivi = np.identity(2) - vi*vi.T
        Ivv.append(Ivivi)
        A += Ivivi
        b += Ivivi *pi
    return np.linalg.lstsq(A, b)[0]
    return np.linalg.solve(A,b)

class Center(object):
    """docstring for Center"""
    def __init__(self):
        super(Center, self).__init__()
        self.center = 0,0
        self.resd = 0
        self.A = np.zeros((2,2))
        self.b = np.zeros((2,1))

    def add_line(self,line,weight):

        vi = np.asmatrix(line[1])
        vi = np.reshape(vi,(2,1))
        pi = np.asmatrix(line[0])
        pi = np.reshape(pi,(2,1))
        Ivivi = np.identity(2) - vi*vi.T
        self.A += Ivivi *weight
        self.b += Ivivi *pi *weight
        self.center = np.linalg.lstsq(self.A, self.b)[0]
        # print self.center,self.resd,rank,s

