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

            if 0.85<ratio<.86:
                cygl.draw_points( [e[0]],color=cygl.RGBA(1.,0.,1,.3),size=3)


            if 0.75<ratio<.76:
                cygl.draw_points( [e[0]],color=cygl.RGBA(1.,0.,0,.3),size=3)

            if 0.65<ratio<.66:
                cygl.draw_points( [e[0]],color=cygl.RGBA(0.,1.,1,.3),size=3)

            if 0.55<ratio<.56:
                cygl.draw_points( [e[0]],color=cygl.RGBA(1.,0.,1,.3),size=3)

            if 0.45<ratio<.46:
                cygl.draw_points( [e[0]],color=cygl.RGBA(0.,0.,1,.3),size=3)

            # pts = cv2.ellipse2Poly( (int(e[0][0]),int(e[0][1])),
            #                                 (int(e[1][0]/2),int(e[1][1]/2)),
            #                                 int(e[2]),0,360,15)
            # cygl.draw_polyline(pts,1,cygl.RGBA(1.,0,0,.5))
            # cygl.draw_polyline( [(e[0][0]-x,e[0][1]-y),(e[0][0]+x,e[0][1]+y)] ,0.5,color)
        cygl.draw_points( [self.center.center],color=cygl.RGBA(0.,0.,1,.3))



def dist_pt_lines(p, line):
    x3,y3 = p
    org ,direction = line[:,0],line[:,1]
    x1,y1 = org[:,0],org[:,1]
    dx21,dy21 = direction[:,0],direction[:,1]
    # (y1,x1),(dy21,dx21) = line

    lensq21 = dx21*dx21 + dy21*dy21

    u = (x3-x1)*dx21 + (y3-y1)*dy21

    u = u / lensq21
    x = x1+ u * dx21
    y = y1+ u * dy21
    dx30 = x3-x
    dy30 = y3-y
    return np.sqrt( dx30**2 + dy30**2 )

def dist_pt_line(p, line):
    x3,y3 = p
    org ,direction = line
    x1,y1 = org
    dx21,dy21 = direction
    # (y1,x1),(dy21,dx21) = line

    lensq21 = dx21*dx21 + dy21*dy21

    u = (x3-x1)*dx21 + (y3-y1)*dy21

    u = u / lensq21
    x = x1+ u * dx21
    y = y1+ u * dy21
    dx30 = x3-x
    dy30 = y3-y
    return np.sqrt( dx30**2 + dy30**2 )

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
        self.lines = []
        self.weights = []

    def add_line(self,line,weight):
        self.lines.append(line)
        self.weights.append(weight)
        vi = np.asmatrix(line[1]).reshape((2,1))
        pi = np.asmatrix(line[0]).reshape((2,1))
        Ivivi = np.identity(2) - vi*vi.T
        self.A += Ivivi *weight
        self.b += Ivivi *pi *weight
        self.center = np.linalg.lstsq(self.A, self.b)[0]
        # print self.center,self.resd,rank,s
        print np.mean(dist_pt_lines(self.center,np.array(self.lines))*np.array(self.weights))


if __name__ == '__main__':
    line = ((100.,100.),(np.sin(np.pi/2),np.cos(np.pi/2)))

    # line = np.array((line,)*1)
    print line
    pt = (0.,0.)
    print dist_pt_line(pt,line)
