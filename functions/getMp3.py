# encode:utf-8
import json
import os
import random
import re

import requests
from bs4 import BeautifulSoup


def getRandomAgent():
    USER_AGENTS = [
     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
     "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
     "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
     "Mozilla/5.0 (compatible; MSIE 9.0; W-indows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
     "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
     "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
     "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
     "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
     "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
     "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
     "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    return USER_AGENTS[random.randint(0,9)]

def getMp3(webUrl):
    """
    获取网页中的mp3地址和标题
    webUrl:网页地址
    """
    headers={
        'User-Agent':getRandomAgent()
    }
    req=requests.get(webUrl,headers=headers)
    reqBS=BeautifulSoup(req.text,'lxml')
    title=reqBS.find(attrs={"class":"jm_title mb4"}).get_text()
    mp3Inode=reqBS.find_all(attrs={"id":"mp3"})[0]
    mp3Link=mp3Inode.attrs['value']
    return title,mp3Link

def DownloadFile(mp3_url, save_url,MP3_name):
    try:
        if mp3_url is None or save_url is None or MP3_name is None:
            print('参数错误')
            return None
        # 文件夹不存在，则创建文件夹
        folder = os.path.exists(save_url)
        if not folder:
            os.makedirs(save_url)
        # 读取MP3资源
        res = requests.get(mp3_url,stream=True)
        # 获取文件地址
        file_path = os.path.join(save_url, MP3_name)
        print('开始写入文件：', file_path)
        # 打开本地文件夹路径file_path，以二进制流方式写入，保存到本地
        with open(file_path, 'wb') as fd:
            for chunk in res.iter_content():
                fd.write(chunk)
        print(MP3_name+' 成功下载！')
    except:
        print("程序错误")

def getMp3List(webUrl):
    """
    获取mp3列表
    """
    headers = {
        'User-Agent': getRandomAgent()
    }
    req=requests.get(webUrl,headers=headers)
    print(req.text)
    req_json=json.loads(req.text)
    mp3Info={}
    for item in req_json['result']['dataList']:
        mp3Info[item['audioName']]=item['mp3PlayUrl']
    return  mp3Info

if __name__ == "__main__":
    # MP3源地址url
    webUrls=[
        'http://www.tingban.cn/jm/vpmrSPuy.html',
        'http://www.tingban.cn/jm/lHXNwuOb.html',
    ]
    for webUrl in webUrls:
        title,mp3Link=getMp3(webUrl)
        # MP3保存文件夹
        save_url='C:/Users/ED/Desktop/慢慢走/'
        # MP3文件名
        MP3_name = '{}.mp3'.format(title)
        DownloadFile(mp3Link,save_url, MP3_name)


#     # MP3源地址url
# if __name__ == "__main__":
#     webUrls=[
#         'http://www.tingban.cn/webapi/audios/list?id=1100000129453&pagesize=20&pagenum=2&sorttype=1&_=1589458185765',
#         'http://www.tingban.cn/webapi/audios/list?id=1100000129453&pagesize=20&pagenum=1&sorttype=1&_=1589458185765',
#         'http://www.tingban.cn/webapi/audios/list?id=1100000129453&pagesize=20&pagenum=3&sorttype=1&_=1589458185765',
#         'http://www.tingban.cn/webapi/audios/list?id=1100000129453&pagesize=20&pagenum=4&sorttype=1&_=1589458185765',
#     ]
#     for webUrl in webUrls:
#         mp3Info=getMp3List(webUrl)
#         for title,mp3Link in mp3Info.items() :
#             print(title,mp3Link)
#             # MP3保存文件夹
#             save_url='C:/Users/Administrator/Desktop/慢慢走/'
#             # MP3文件名
#             MP3_name = '{}.mp3'.format(title)
#             DownloadFile(mp3Link,save_url, MP3_name)
