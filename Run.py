#!/usr/bin/python3
#! coding: utf-8
from bs4 import BeautifulSoup
import requests
import urllib3
from captchasolver import *
import pytesseract
import os
import argparse
urllib3.disable_warnings() #cerficate Warnings Disable Algeria .... Old Certicates Not Secure ...

try:
    import Image, ImageOps, ImageEnhance, imread
except ImportError:
    from PIL import Image, ImageOps, ImageEnhance
def get_captcha():
    file_name =  "image.png"
    i = requests.get("http://ec.algerietelecom.dz/captcha/captcha.php")
    if i.status_code == requests.codes.ok:
        with open(file_name, 'wb') as file:
                file.write(i.content)
    else:
        print("Error Getting Captcha")
    pass
def clean_trash():
    dir = os.system("cd trash")
    os.system("rm *.png")
    pass
http_proxy  = "http://127.0.0.1:8080" #used For Debug Http requests Burp Suit Proxy
proxyDict = {"http":http_proxy}
phone_number = "032546423"
cookies = {
    'TS01276d82': '0107c3cab6a2e9ef9673e157813a665072f15c2fa1ad145627693c0e8f63169e846826d3b4a5733f4b7d0bb2d050807e77844c036b612269398a64f353fa0b5b2fb3695308',
    'PHPSESSID': '3skvci46tjb9rgd3l7181dhhi2',
}
headers = {
    'Host': 'ec.algerietelecom.dz',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '46',
    'Connection': 'close',
    'Referer': 'https://ec.algerietelecom.dz/index.php?p=internet_recharge',
    'Upgrade-Insecure-Requests': '1',
}
params = (
    ('p', 'internet_recharge'),
)
while True:
    get_captcha()
    capthatext = solve_captcha("image.png") #Utf-8 Encode In Case Of Bad Characters 
    print("Captcha:{}".format(capthatext))
    data = 'nd=%s&userCode=%s&validerADSL=Confirmer'% (phone_number, str(capthatext))
    print(data)
    req2 = requests.post('https://ec.algerietelecom.dz/index.php', headers=headers, params=params, cookies=cookies, data=data,verify=False)#proxies=proxyDict You Can Add Proxies Heree For Debug Like Burp ..
    req_code = req2.status_code
    print(req_code)
    os.system("ls | grep *.png")
    soup = BeautifulSoup(req2.text, 'html.parser') #Hot Soup "Chourba :)"
    if soup.center == None:
        if soup.title.text == "Request Rejected":
            print("rejected................................")
            print(soup.title.text)
            pass
        else:
            print("succes")
            print(req2.text)
            exit()
        pass
    if soup.center!=None:
        print(soup.center.text)
        pass
    #print(req2.text)
    clean_trash() # Clean Algerie Telecom Captcha Trash
    pass
