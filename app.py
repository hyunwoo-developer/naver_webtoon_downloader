from flask import Flask, send_file
from bs4 import BeautifulSoup
import requests
import os
import shutil
from urllib.request import Request, urlopen
import zipfile

app = Flask(__name__)

@app.route('/')
def download():

    url = "https://comic.naver.com/webtoon/detail?titleId=780506&no=42&weekday=tue" # 화수 링크
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    images = list(soup.select('img[alt="comic content"]'))

    path = "./static/temp"
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    cnt = 1
    for image in images:
        req = Request(image['src'], headers=headers)
        image_read = urlopen(req).read()

        image_open = open(path + "/" + str(cnt) + ".jpg", 'wb')
        image_open.write(image_read)
        image_open.close()
        cnt += 1

    zip_file = zipfile.ZipFile("./static/webtoon.zip", "w")
    for file in os.listdir(path):
        if file.endswith(".jpg"):
            zip_file.write(os.path.join(path, file), compress_type=zipfile.ZIP_DEFLATED)

    zip_file.close()

    file_name = f"static/webtoon.zip"
    return send_file(file_name,
                     mimetype='application/zip',
                     attachment_filename='./static/webtoon.zip',
                     as_attachment=True)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)