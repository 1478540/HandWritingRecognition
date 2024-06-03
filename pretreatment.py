from PIL import Image
import numpy as np
import cv2
import os


def auto_crop_and_save(input_image_path, output_image_path):

    image = cv2.imread(input_image_path)
    
   
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    max_contour = max(contours, key=cv2.contourArea)
    
    x, y, w, h = cv2.boundingRect(max_contour)
    
    cropped_image = image[y:y+h, x:x+w]
    
    resized_image = cv2.resize(cropped_image, (image.shape[1], image.shape[0]))
    
    cv2.imwrite(output_image_path, resized_image)
    

def preprocess_image(image_path, output_path):

    image = Image.open(image_path)
    image = image.resize((32, 32))
    image = image.convert('L')
    image_array = np.array(image)
    threshold = 128
    image_array = np.where(image_array < threshold, 1, 0)
    np.savetxt(output_path, image_array, fmt='%d', delimiter='')


def pretreatment_image(input_image_path,output_text_path):
    
   
    auto_crop_and_save(input_image_path,"temp231.jpg")

    preprocess_image("temp231.jpg",output_text_path)

    os.remove("temp231.jpg")


