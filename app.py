
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import pytesseract as tess
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
from datetime import datetime

app = Flask(__name__)


def checkurl(url):
    try:
        http = urllib.request.urlopen("http://"+url)
        https = urllib.request.urlopen("https://"+url)
        try:
            originalUrl = urllib.request.urlopen(url)
            if originalUrl.status == 200:
                return url
        except:
            if http.status == 200:
                return "http://"+url
            elif https.status == 200:
                return "https://"+url

        else:
            return ""
    except:
        return ""


@ app.route('/')
def index():
    img = Image.open('test3.png')

    return render_template('index.html', )


@ app.route('/', methods=['POST'])
def home():
    img = request.files['image_file']
    img = Image.open(img)
    config = ('-l kor+eng --oem 3 --psm 11')
    url = tess.image_to_string(img, config=config)
    url = url.replace(" ", "")
    url = url.replace('\n', "")
    error = ""
    text = checkurl(str(url))
    if text == "":
        error = "다시 시도해 주세요. 분석할 수 없습니다."
    print(text)
    return render_template('index.html', link=text, error=error)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5005)
