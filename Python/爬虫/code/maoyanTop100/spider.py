# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 14:22:42 2019

@author: LiXinfeng
"""
import json
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
import re

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            return content
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?'
                         +'data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?'
                         +'star">(.*?)</p>.*?releasetime">(.*?)</p>'+
                         '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    results = re.findall(pattern,html)
    for result in results:
        yield {
            'index': result[0],
            'url': result[1],
            'name': result[2],
            'star': result[3],
            'releasetime': result[4],
            'score': result[5]+result[6]
        }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')
        f.close()

def main(offset):
    url = 'https://maoyan.com/board/4?'
    new_url = url + 'offset='+ str(offset*10)
    html = get_one_page(new_url)
    # print(html)
    # parse_one_page(html)
    for result in parse_one_page(html):
        print(result)
        write_to_file(result)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i for i in range(10)])