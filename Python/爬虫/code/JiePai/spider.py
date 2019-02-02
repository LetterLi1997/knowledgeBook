import json
import os
import re
import pymongo
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from hashlib import md5
from requests.exceptions import RequestException
from config import *
from multiprocessing import Pool

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_page_index(offset, keyword):
    data = {
        'aid': 24,
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(data)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    try:
        headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        print('请求详情页出错',url)
        return None

def parse_page_detail(content):
    soup = BeautifulSoup(content,'lxml')
    title = soup.select('title')[0].get_text()
    pattern = re.compile('&quot;http://(.*?)&quot;',re.S)
    results = re.findall(pattern,content)
    if results:
        for img_url in results:
            download_image(img_url)
        return {
            'title':title,
            'images': results
        }

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功',result)
        return True
    return False

def download_image(url):
    print('正在下载..',url)
    try:
        headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
        response = requests.get('http://'+url,headers=headers)
        if response.status_code == 200:
            save_image(response.content) # content和text的区别是content返回二进制内容，text返回文本内容
        else:
            return None
    except RequestException:
        print('请求图片出错',url)
        return None

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main(offset):
    html = get_page_index(offset, SEARCH_TYPE)
    for url in parse_page_index(html):
        content = get_page_detail(url)
        if content:
            results = parse_page_detail(content)
            if results:
                save_to_mongo(results)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[offset*20 for offset in range(5)])