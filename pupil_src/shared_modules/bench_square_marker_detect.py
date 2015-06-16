
from pyx_compiler import build_extensions
build_extensions()
import cv2
import square_marker_detect
import cy_square_marker_detect
from timeit import Timer



def bench():
    cap = cv2.VideoCapture('/Users/mkassner/recordings/2015_06_16/000/world.mkv')
    status,img = cap.read()
    markers = []
    while status:
        markers = cy_square_marker_detect.detect_markers_robust( cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),5,markers,true_detect_every_frame=1)
        status,img = cap.read()
        if markers:
            return



if __name__ == '__main__':

    import cProfile,subprocess,os
    cProfile.runctx("bench()",{},locals(),"world.pstats")
    loc = os.path.abspath(__file__).rsplit('pupil_src', 1)
    gprof2dot_loc = os.path.join(loc[0], 'pupil_src', 'shared_modules','gprof2dot.py')
    subprocess.call("python "+gprof2dot_loc+" -f pstats world.pstats | dot -Tpng -o world_cpu_time.png", shell=True)
    print "created  time graph for  process. Please check out the png next to this file"
    exit()



    cap = cv2.VideoCapture('/Users/mkassner/recordings/2015_06_16/000/world.mkv')
    status,img = cap.read()

    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    t = Timer(lambda: cy_square_marker_detect.detect_markers_robust(gray_img,5,[],true_detect_every_frame=1))
    print "Time required for cython"
    print t.timeit(number=100)

    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    t = Timer(lambda: square_marker_detect.detect_markers_robust(gray_img,5,[],true_detect_every_frame=1))
    print "Time required for python"
    print t.timeit(number=100)