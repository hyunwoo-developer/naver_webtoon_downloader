import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbwebtoon

# 외부 크롤링 -> database
# comicId, title, author, relWeekday, recentPageNum, thumbnailImgUrl, pageUrl,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://comic.naver.com/webtoon/weekday', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

lis = soup.select('#content > div.list_area.daily_all > div > div > ul > li')

base_url = "https://comic.naver.com"

for li in lis:
    title = li.select_one('div > a > img')['title']
    thumbnailImgUrl = li.select_one('a > img')['src']
    pageUrl = base_url + li.select_one('a')['href']
    weekday = pageUrl[-3:]
    id = pageUrl[45:51]

    detail_data = requests.get(pageUrl, headers=headers)
    detail_soup = BeautifulSoup(detail_data.text, 'html.parser')

    author = detail_soup.select_one('#content > div.comicinfo > div.detail > h2 > span:nth-child(1)').text
    category_1 = detail_soup.select_one('#content > div.comicinfo > div.detail > p.detail_info > span.genre').text.strip().split(',')[0]
    category_2 = detail_soup.select_one('#content > div.comicinfo > div.detail > p.detail_info > span.genre').text.strip().split(',')[1]
    desc = detail_soup.select_one('#content > div.comicinfo > div.detail > p:nth-child(2)').text
    recentPageNum = detail_soup.select_one('td.title > a')['href'].split('&')[1].split('=')[1]

    doc = {
        'id' : id,
        'title' : title,
        'category_1' : category_1,
        'category_2' : category_2,
        'author' : author,
        'desc' : desc,
        'recent_page_num' : recentPageNum
    }
    db.mywebtoon.insert_one(doc)
