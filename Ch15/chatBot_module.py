#!/usr/bin/env python
# coding: utf-8

# In[17]:


#  1-2-2  機器人的耳朵函式
import speech_recognition as sr

def bot_listen():
    recong = sr.Recognizer()
    with sr.Microphone() as source:
        audioData = recong.listen(source)
    try:
        text = recong.recognize_google(audioData, language = "zh-tw")
        return text
    except:
        return "聽不懂"
    
# 1-4-3 機器人的說話函式
from gtts import gTTS
from pygame import mixer
import os

mixer.init()
if not os.path.isfile("tmp.mp3"):
    tts = gTTS(text = "不重要的語音檔", lang = "zh-tw")
    tts.save("tmp.mp3")
    print("已產生不重要的語音檔 tmp.mp3")
#-----------------#
def bot_speak(text, lang):
    try:
        mixer.music.load("tmp.mp3")
        tts = gTTS(text = text, lang = lang)
        tts.save("speak.mp3")
        mixer.music.load("speak.mp3")
        mixer.music.play()
        while (mixer.music.get_busy()):
            continue
    except:
        print("播放音效失敗")
# 	1-6-3  抓取維基百科愛因斯坦網頁內的文章第一段

from bs4 import BeautifulSoup as bs
import requests

def bot_get_wiki(keyword):
    response = requests.get("https://zh.wikipedia.org/zh-tw/" + keyword)
    soup = bs(response.text, features = "lxml")
    p_list = soup.find_all("p")
    for p in p_list:
        if keyword in p.text: # 怕10個字搜不到
            return p.text
            
# 1-7-3 唸出常規表達式處理後的字串
import re

def bot_speak_re(sentence):
    s1 = re.sub(r"\[[^\]]*\]", "", sentence)
    s1 = re.sub(r"／.*?ⓘ", "", s1)
    print(s1)
    en_list = re.findall(r"[a-zA-Z ]+", s1)
    s2 = re.sub(r"[a-zA-Z \-]+", "@English@", s1)
    all_list = s2.split("@")
    index = 0
    for text in all_list:
        if text != "English":
            bot_speak(text, "zh-tw")
        else:
            bot_speak(en_list[index], "en")
            index += 1
            
# 1-8-3 對 Google 搜尋結果進行網路爬蟲
from hanziconv import HanziConv

def bot_get_google(question):
    url = f"https://www.google.com/search?q={question}+維基百科"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        soup = bs(response.text, features = "lxml")
        title = soup.find("h3", attrs = {"class": "LC20lb MBeuO DKV0Md"}).text # 日向雛田- 維基百科，自由的百科全書</h3>
        end = title.index("-")
        kwd = title[: end].strip()
        # wiki_url = soup.find("cite")
        # kwd = wiki_url.text.split("›")[-1].strip() # .replace(" ","")也可以
        # kwd_tra = HanziConv.toTraditional(kwd)
        return kwd# kwd_tra
    else:
        print("請求失敗")

