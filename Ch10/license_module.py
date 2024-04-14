#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import cv2
import time
import re

recog_url = "https://vike.cognitiveservices.azure.com/vision/v3.2/read/analyze"
key = "4f4167ec50fe45b2a4636f903def1a40"
headers = {"Ocp-Apim-Subscription-Key" : key}
headers_stream = {"Ocp-Apim-Subscription-Key" : key, "Content-Type" : "application/octet-stream"}

def get_license(img):
    img_encode = cv2.imencode(".jpg", img)[1]
    img_bytes = img_encode.tobytes()
    r1 = requests.post(recog_url, headers = headers_stream, data = img_bytes)
    if r1.status_code != 202:
        print(r1.json())
        return "請求失敗"
    result_url = r1.headers["Operation-Location"]
    r2 = requests.get(result_url, headers = headers)
    while r2.status_code == 200 and r2.json()["status"] != "succeeded":
        r2 = requests.get(result_url, headers = headers)
        time.sleep(0.5)
        print("status: ", r2.json()["status"])
    carcard = ""
    lines = r2.json()["analyzeResult"]["readResults"][0]["lines"]
    for i in range(len(lines)):
        text = lines[i]["text"]
        m = re.match(r"^[\w]{2,4}[-. ][\w]{2,4}$", text)
        if m != None:
            carcard = m.group()
            return carcard
    if carcard == "":
        return "找不到車牌"
 

def main():
    try:
        img = cv2.imread("car.jpg")
        print("status: Start")
        text = get_license(img)
        print("車牌:　", text)
        cv2.imshow("Frame", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        print("讀取圖片失敗")
        
if __name__ == "__main__":
    main()