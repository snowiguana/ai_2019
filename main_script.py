# -*- coding: utf-8 -*-
"""
Created on Thu May 23 00:39:06 2019

@author: Usuario
"""

import os,sys
import argparse
import subprocess

string="darknet.exe detector demo resource/obj.data resource/yolov3-obj.cfg resource/yolov3-obj_final.weights "

#parse args
def parse_args():
    parser = argparse.ArgumentParser(description='Arguments for running license plate recognition.')
    parser.add_argument('-t','--type', type=str, choices=['ipcam','stored'],required=True, default="stored",
                    help='mode of video playing ipcam or stored')
    parser.add_argument('-f','--filepath', type=str, default=None, 
                    help='file path of video file if using stored')
    parser.add_argument('-i','--ip',type=str, default=None,
                    help='ip address with port in format https://x.x.x.x:x')
    args = parser.parse_args()
    if args.type == "ipcam":
        if args.ip ==None:
            print("error!!! ip:port combination is needed to connect to ipcam")
            print("exiting")
            exit(0)
        else:
            cmd=string + str(args.ip)+"/video?dummy=param.mjpg -i 0 -thresh 0.70"
    elif args.type == "stored":
        if args.filepath ==None:
            print("error!!! need filepath to run detection on stored video")
            print("exiting")
            exit(0)
        else:
            cmd=string+args.filepath+" -thresh 0.70"
    return args,cmd
        
        
if __name__=='__main__':
    cmd2="python detectmin.py"
    args,cmd=parse_args()
    subprocess.call(cmd)
    print("####################finished grabbing detected objects now processing######################\n!\n!\n!")
    subprocess.call(cmd2)
    print("\n!\n!\n########################prediction for the session has completed#######################")