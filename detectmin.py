# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:01:57 2019

@author: Usuario
"""

from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage import measure
from skimage.measure import regionprops
from PIL import Image
import os,sys
import pytesseract
import glob
import concurrent.futures
import cv2


os.environ['OMP_THREAD_LIMIT'] = '1'   
path = "result_img/"
processed_img_path = "processed_img/"

#process image for better character recognition mainly crop based on the detected bounding box the scale
def processImage(filename,count):
    image = imread(path+filename, as_gray=True)
    
    # the next line is not compulsory however, a grey scale pixel
    # in skimage ranges between 0 & 1. multiplying it with 255
    # will make it range between 0 & 255 (something we can relate better with
    
    gray_image = image * 255
    threshold_value = threshold_otsu(gray_image)
    binary_image = gray_image > threshold_value
    plate_objects_cordinates = []
    # CCA (finding connected regions) of binary image
    
    # this gets all the connected regions and groups them together
    label_image = measure.label(binary_image)
    plate_dimensions = (0.30*label_image.shape[0], 1*label_image.shape[0], 0.50*label_image.shape[1], 1*label_image.shape[1])
    min_height, max_height, min_width, max_width = plate_dimensions
    # regionprops creates a list of properties of all the labelled regions
    for region in regionprops(label_image):
        # print(region)
        if region.area < 50:
            #if the region is so small then it's likely not a license plate
            continue
            # the bounding box coordinates
        min_row, min_col, max_row, max_col = region.bbox
        plate_objects_cordinates.append((min_row, min_col,
                                     max_row, max_col))
        
    #assuming that licence plates area in the must be at least 30% of original image´s height and 50% of original image´s width
    for item in plate_objects_cordinates:
        mi_r,mi_c,mx_r,mx_c =item
        region_height=mx_r-mi_r
        region_width=mx_c-mi_c
        if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
            min_row, min_col, max_row, max_col = item
            
    double=2
    imgobj=Image.open(path+filename)
    cropped =imgobj.crop((min_col,min_row,min_col+(max_col-min_col),min_row+(max_row-min_row)))
    scaled_image=cropped.resize( [int(double * s) for s in cropped.size] )
    scaled_image.save(processed_img_path+str(count)+'.jpg', 'JPEG', quality=90)

#cleanup prossed_img folder at start of session
def cleanup():    
    dirs=os.listdir( processed_img_path )
    for item in dirs:
        if os.path.isfile(processed_img_path+item):
            os.remove(processed_img_path+item)

#pass each image for processing then
def processing():    
    dirs=os.listdir( path )
    count=0
    for item in dirs:
        if os.path.isfile(path+item):
            processImage(item,count)
            #os.remove(path+item)
            count=count+1
            
def ocr(img_path):
    img = cv2.imread(img_path)
    text = pytesseract.image_to_string(img,lang='eng',config='--psm 7')
    return text
#divide work among multiple workers for running parallel instances of tesseract         
def predict():            
    path = "processed_img"
    output_text=[]
    if os.path.isdir(path) == 1:
        #divide work among multiple workers for running parallel instances of tesseract     
        with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
            image_list = glob.glob(path+"\\*.jpg")
            for img_path,out in zip(image_list,executor.map(ocr,image_list)):
                print(img_path.split("\\")[-1],',',out,', processed')
                output_text.append(out)
    count_plate=[]
    for item in output_text:
        #if nothing has been predicted for the image we do not need to keep record of it the image may be too noisy
        if item == '':
            continue
        x=output_text.count(item)
        #assume that the license plates must be detected at least 8 frames i.e. same character prediction for 8 frames
        if x>=8:
            count_plate.append((x,item))
    #removing duplicates
    final_result= list(dict.fromkeys(count_plate))
    for item in final_result:
        print("\n[no of counts:predicted plate] == "+str(item))
    
    
if __name__=='__main__':
    cleanup()    
    processing()
    predict()