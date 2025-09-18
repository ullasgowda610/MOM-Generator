import google.generativeai as genai
import os   
from PIL import Image
import cv2
import numpy as np  

def extract_text_from_image(image_path):

    #lets load the image
    file_bytes=np.asarray(bytearray(image_path.read()),dtype=np.uint8)
    image1=cv2.imdecode(file_bytes,cv2.IMREAD_COLOR)
    #image1=cv2.imread('image_path')
    image1=cv2.cvtColor(image1,cv2.COLOR_BGR2RGB) # TO CONVERT BGR TO RGB
    image_grey=cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY) 
    _,image_bw=cv2.threshold(image_grey,150,255,cv2.THRESH_BINARY)


    # the image  cv2 gives is in numpy array format so we need to convert it to image object.
    final_image=Image.fromarray(image_bw)
    
    # configure genai model
    key=os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=key)
    model=genai.GenerativeModel('gemini-2.5-flash-lite')
    
    #lets write prompt for OCR
    prompt='''You act as an OCR Application on the given image and extract the text from it.give only the text as output without any other description or punctuation.'''

    # lets extract and return the text
    response=model.generate_content([prompt,final_image])
    output_text=response.text
    return output_text


    