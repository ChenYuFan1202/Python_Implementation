#!/usr/bin/env python
# coding: utf-8

# In[1]:

import cv2
import smtplib
from email.mime.image import MIMEImage

def send_gmail(gmail_addr, gmail_pwd, to_addrs, msg):
    smtp_gmail = smtplib.SMTP("smtp.gmail.com", 587)
    print(smtp_gmail.ehlo())
    print(smtp_gmail.starttls())
    print(smtp_gmail.login(gmail_addr, gmail_pwd))
    status = smtp_gmail.sendmail(from_addr = gmail_addr, to_addrs = to_addrs, msg = msg)
    if not status:
        print("寄信成功")
    else:
        print("寄信失敗", status)
    smtp_gmail.quit()

def get_mime_img(subject, fr, to ,img):
    img_encode = cv2.imencode(".jpg", img)[1]
    img_bytes = img_encode.tobytes()
    mime_img = MIMEImage(img_bytes)
    mime_img["Content-type"] = "application/octet-stream"
    mime_img["Content-Disposition"] = "attachment; filename = 'pic.jpg'"
    mime_img["Subject"] = subject
    mime_img["From"] = fr
    mime_img["To"] = to
    return mime_img.as_string()