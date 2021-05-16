import cv2
import os
from PIL import Image,ImageGrab
import pytesseract
import re
# char = re.compile('[^0-9a-zA-Z-&ㄱ-ㅣ가-힣 !#?]') 정규식 기억이안남

def OCR_Get_Num(img) :
    height , width , tmp = img.shape
    w = (31*width)/100
    h = (18*height)/100
    x = width*10/40
    # print(w,h,x)
    tmp_img = img[int(h):int(h+x/3),int(w):int(w+x)]
    # gray = img
    gray = cv2.cvtColor(tmp_img,cv2.COLOR_RGB2GRAY)
#    gray = cv2.threshold(gray, 0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename,gray)
    text = pytesseract.image_to_string(Image.open(filename),lang=None)
    num = re.findall("\d+", text)
    s =""
    for i in num:
        s=s+i
    cv2.namedWindow("test")
    cv2.moveWindow("test", 500, 700)
    cv2.imshow("test", gray)
#    cv2.waitKey(0)
    os.remove(filename)
    return s
