STEPS FOR OPERATION
1. Install DARKNET with cuda and all it´s dependencies
2. Install tesseract 4.0 ocr and it python wrapper along with skimage libraries for python3 and dependencies
3. Place and replace image.c in darknet-master/src directory
4. build darknet
5. copy files detectmin.py and main_script.py in darknet-master
6. create directories resource,result_img and processed_img in darknet-master folder
7. copy files "obj.data", "obj.names", "yolov3-obj.cfg" and "yolov3-obj_final.weights" to the created resource folder
8. run python main_script.py -t [stored/ipcam] (optional :-f [filepath to stored video if stored selected] -i [ipcam stream ip+port]) on terminal

e.g. running on stored video
python main_script.py -t stored -f [path to file]

e.g. running on ipcam
python main_script.py -t ipcam -i [ip:path] 
ip:port e.g.(https://192.168.1.1:8080)


Training with yolov3 Guide
1. install darknet and all it's dependencies then build darknet (if capturing of detected objects is required then follow steps 3 and 6 above or you could tweak image.c in yolov3 to crop and store detected objects)
2. collect training data and prepare using openLabelling tool (https://github.com/Cartucho/OpenLabeling)
3. store path to all images on training folder into a single file called train.txt
4. store and group output frame and texts obtained from openLabelling tool into a single folder.
5. Create file obj.names with all the class labels
6. Create file obj.data with path to train.txt, obj.names
7. Tweak yolov3.cfg for your custom classes and resolution under each yolo layer
8. build darknet
9. download pre-trained model darknet53 from (https://pjreddie.com/darknet/imagenet/#darknet53)
10. Run command darknet.exe detector train (path to obj.data) (path to yolov3.cfg) (path to darknet53.conv.74)


##################################################
based on:
@article{yolov3,
  title={YOLOv3: An Incremental Improvement},
  author={Redmon, Joseph and Farhadi, Ali},
  journal = {arXiv},
  year={2018}
}

tesserat v4.0