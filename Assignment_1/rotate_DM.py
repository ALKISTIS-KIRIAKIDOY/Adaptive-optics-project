from camera.ueye_camera import uEyeCamera
from pyueye import ueye
import time
import numpy as np
import matplotlib.pyplot as plt
import imageio


SH_Sensor_Index = 3
Camera_Index = 1

def grabframes(nframes, cameraIndex=1):
    with uEyeCamera(device_id=cameraIndex) as cam:
        cam.set_colormode(ueye.IS_CM_SENSOR_RAW8)#IS_CM_MONO8)
        #w=1280
        #h=1024
        #cam.set_aoi(0,0, w, h)
        w=1000
        h=1000
        cam.set_aoi(0,0, w, h)
        
        cam.alloc(buffer_count=10)
        cam.set_exposure(0.1)
        cam.capture_video(True)
    
        imgs = np.zeros((nframes, h ,w),dtype = np.uint8)
        acquired = 0
        # For some reason, the IDS cameras seem to be overexposed on the first frames (ignoring exposure time?). 
        # So best to discard some frames and then use the last one
        while acquired<nframes:
            frame = cam.grab_frame()
            if frame is not None:
                imgs[acquired] = frame
                acquired+=1
            
    
        cam.stop_video()
    
    return imgs




from dm.thorlabs.dm import ThorlabsDM
a=np.linspace(-0.9,0.9, 43)
with ThorlabsDM() as dm:
    writer = imageio.get_writer('camera_movie.mp4', fps=10)
    act=np.ones([len(dm)])
    Running = True
    t = 0
    while t<1:
        dm.setActuators(act * 0)
        for i in range(len(act)):
            for j in np.linspace(-0.8,0.8,5):
                act[i] = act[i]*j
                dm.setActuators(act)
                time.sleep(0.01)
                img1=grabframes(1, Camera_Index)
                writer.append_data(img1[-1])
        act[-3:] = 0
        dm.setActuators(act)
        t+=1
    writer.close()
    
    
    