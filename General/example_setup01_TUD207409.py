"""
Example for PC in right corner

Setup right corner:
    Camera 1: Regular camera
    Camera 2: SH sensor
"""

from camera.ueye_camera import uEyeCamera
from pyueye import ueye
import time
import numpy as np
import matplotlib.pyplot as plt

SH_Sensor_Index = 3
Camera_Index = 1

def grabframes(nframes, cameraIndex=1):
    with uEyeCamera(device_id=cameraIndex) as cam:
        cam.set_colormode(ueye.IS_CM_SENSOR_RAW8)#IS_CM_MONO8)
        #w=1280
        #h=1024
        #cam.set_aoi(0,0, w, h)
        w=600
        h=600
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

if __name__ == "__main__":
    from dm.thorlabs.dm import ThorlabsDM
    a=np.linspace(-0.9,0.9, 43)
    with ThorlabsDM() as dm:
    
        act=np.zeros([len(dm)])
        while False:
            for k in range(len(dm)):
                act[k]=1
                for i in range(len(dm)):
                    act_dis=act*a[i]
                    dm.setActuators(act_dis)
                    time.sleep(0.01)
                for i in range(len(dm)):
                    act_dis=act*a[i]*-1
                    dm.setActuators(act_dis)
                    time.sleep(0.01)
                act[k]=0
                dm.setActuators(act)
                time.sleep(0.01)
                
        
        act=np.ones([len(dm)])
        act[-3:] = 0
        while True:
            for k in np.linspace(-0.8, 0.8, 101):
                dm.setActuators(act * k)
                time.sleep(0.01)
            for k in np.linspace(+0.8, -0.8, 101):
                dm.setActuators(act * k)
                time.sleep(0.01)
            
        if False:
            print(f"Deformable mirror with {len(dm)} actuators")
            #dm.setActuators(np.random.uniform(-1,1,size=len(dm)))
            act=np.zeros([len(dm)])
            dm.setActuators(act)
     
            
            plt.figure()    
            img1=grabframes(1, Camera_Index)
            plt.imshow(img1[-1],cmap='gray', vmin=0, vmax=255)
            

            plt.figure()
            img2=grabframes(4, SH_Sensor_Index)
            plt.imshow(img2[-1])
