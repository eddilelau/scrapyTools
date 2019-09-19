#coding:utf-8
"""
主题：爬取知乎个人主页中的问答内容

"""
from bs4 import BeautifulSoup
import requests
import random
import re
class zhihuPersonalinfo(object):
    def __init__(self,personalId):
        self.incompleteUrl = "https://www.zhihu.com/people/{}/answers?page=".format(personalId) +"{}"

    def getRandomAgent(self):
        USER_AGENTS = [
         "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
         "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
         "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
         "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
         "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
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

    def getMaxinfoPage(self):
        url=self.incompleteUrl.format(1)
        header={
            'user-agent': self.getRandomAgent()
        }
        response=requests.get(url, headers=header)
        if len(response.text) == 4392:  # 部分UA版本过低,无法浏览知乎网站
            self.getMaxinfoPage()
        else:
            pattern = re.compile('<div class="Pagination">(.*?)</div>')
            for i in response.content.split(sep=b'script'):
                try:
                    for content in pattern.findall(i.decode("utf-8"),re.S):
                        if len(content) > 0:
                            Pagecontent=BeautifulSoup(content,'lxml')
                            return max([int(item.get_text()) for item in Pagecontent.find_all(class_="Button PaginationButton Button--plain")])
                except:
                    print("----------{}-----------\n".format("script"))

    def getAnwser(self):
        pageList=list(range(1, self.getMaxinfoPage()))
        while len(pageList):
            a=pageList.pop()
            url=self.incompleteUrl.format(a)
            header ={
                'user-agent':self.getRandomAgent()
            }
            response=requests.get(url,headers=header)
            if len(response.text) == 4392:    #部分UA版本过低,无法浏览知乎网站
                pageList.append(a)
            else:
                pattern=re.compile('"title":"([\u4e00-\u9fa5].*?)".*?"type":"([a-z]+)","id":(\d+)')
                for i in response.content.split(sep=b'script'):
                    try:
                        for content in pattern.findall(i.decode("utf-8"),re.S) :
                            if len(content)>0:
                                print("title:",content[0],";type:",content[1],";id:",content[2])
                    except:
                        print("部分js脚本用\\x十六进制编码,考虑到实际需求中不需要.该内容直接丢弃")


if __name__ == "__main__":
    personalId ="bai-shi-gang"   #路径
    xmqq = zhihuPersonalinfo(personalId)
    xmqq.getAnwser()
