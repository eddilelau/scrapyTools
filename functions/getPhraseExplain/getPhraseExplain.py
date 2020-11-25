#coding:utf-8
import copy
import json
import re
import time
import urllib.request
import random

import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import make_logging


class make_flashcard(object):
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
        return USER_AGENTS[random.randint(0, 9)]


    def getPage(self,myword:str):
        '''
        :param myword:查询单词
        :return:html
        '''
        basurl='http://dict.cn/'
        searchurl=basurl+myword
        headers={
            "user-agent":self.getRandomAgent()
        }
        try:
            response =requests.get(searchurl,headers=headers)
            html = response.content
            return html
        except:
            make_logging.make_logging().log_info(myword+";{} is a error words,the html repsonse it is invail".format(myword), type="error")
            return False

    def get_wordmeaning(self,html_selector:str):
        '''
        :param html_selector:
        :return:
        '''
        selector=BeautifulSoup(html_selector, "lxml")
        attribute={}
        word={}
        for item in selector.find_all('div', {'class': 'layout dual'}):
            for i in item.find_all('span'):  # 获取单词词性
                i_=i.get_text().replace('\t','').replace('\n','')
                attribute.setdefault('attribute', []).append(i_)

            for i in item.find_all('ol'):  # 获取单词释义
                i_=i.get_text().replace('\t','').replace('\n','')
                word.setdefault('word', []).append(i_)
        if len(word) > 0 and len(attribute):

            return attribute, word  # 返回词性、单词释义
        else:
            return ''

    def get_sentence(self,html_selector:str):
        """
        爬取翻译例句
        :param html_selector:
        :return:sentences
        """
        selector=BeautifulSoup(html_selector, "lxml")
        sentences={}
        for item in selector.find_all('div', {'class': 'layout sort'}):
            for i in item.find_all('li'):  # 获取例句
                i_=i.get_text().replace('\t','').replace('\n','')
                sentences.setdefault('sentences', []).append(i_)

        if len(sentences):

            return sentences  # 返回例句
        else:
            return ''

    def get_phonetic_pronunciation(self,html_selector:str,myword:str):
        """
        :param html_selector:
        :return:
        """
        phonetic={}
        pronunciation={}
        selector=BeautifulSoup(html_selector, "lxml")
        result=selector.find_all('div', {'class': 'phonetic'})
        base_url='http://audio.dict.cn/'
        i=1
        for item in result:
            for i in item.find_all('bdo', {'lang': 'EN-US'}):  # 获取音标,
                i_=i.get_text().replace('\t','').replace('\n','')
                phonetic.setdefault('phonetic', []).append(i_)

            for a in item.find_all('i'):  # 获取读音
                pronunciation.setdefault('pronunciation', []).append(base_url + a['naudio'])

        if len(phonetic) > 0 and len(pronunciation) > 0:
            # return phonetic, pronunciation  # 返回音标、读音
            return phonetic  # 返回读音(不需要音标)
        else:
            with open("./errorWords.txt","a+",encoding="utf-8") as f:
                f.write(myword+";{} has not phonetic".format(myword)+"\n")
            return ""

    def get_explain(self,html_selector:str,myword:str):
        explain={}
        selector=BeautifulSoup(html_selector, "lxml")
        result=selector.find_all('div', {'class': 'basic clearfix'})
        if len(result)>0:
            result=result[0].find_all('ul')
            for item in result:
                for i in item.find_all('li'):  # 获取解析,
                    i_=i.get_text().replace('\t','').replace('\n','')
                    i_='' if 'if' in i_ else i_
                    explain.setdefault('explain', []).append(i_)
            if len(explain) > 0:
                return explain  # 返回解析
            else:
                return " "
        else:return " "

    def get_flashCard(self,pagehtml:str,myword:str):
        if len(BeautifulSoup(pagehtml, "lxml").find_all(text="该词条未找到_海词词典")) == 0:
            # 单词释义
            explain = self.get_explain(pagehtml,myword)
            #单词音标及读音
            phonetic = self.get_phonetic_pronunciation(pagehtml,myword)
            #单词例句
            sentences = self.get_sentence(pagehtml)

            if len(explain)>0 and phonetic !="" :
                explain.update(phonetic)
                explain.update(sentences)
                return explain
            else:
                return ''
        else:
            make_logging.make_logging().log_info("{} is a error words,the html repsonse it can not be found".format(myword),type="error")
            return ''

class get_item(object):

    def add_2_glossary(self,glossaryPath:str,added_terms:list):
        """
        :param glossaryPath :存量词汇表地址
        return none
        """
        with open(glossaryPath,'a') as gp:
            for term in added_terms:
                gp.write(term+"\n")

    def trim_glosssary(self,glossaryPath:str,added_terms:list):
        """
        :param glossaryPath :存量词汇表地址
        :return 新增词汇列表
        """
        with open(glossaryPath,'r') as gp:
            term_stock=set([term.split("\n")[0].lower() for term in gp])
        return [term for term in added_terms if term not in term_stock],len(term_stock)

    def get_term(self,glossaryPath:str,filePath:str):
        """
        :param glossaryPath :存量词汇表文件
        :param filePath :新增词汇表文件
        :return:新增词汇列表
        """
        # added_term
        with open(filePath,'+r',encoding="utf-8") as f2:
            added_terms = [ word.replace("\n","").lower() for word in f2.readlines()]
        terms,stock_term_count=self.trim_glosssary(glossaryPath, added_terms)
        return terms,stock_term_count,len(added_terms)

    def get_term_from_essay(self,glossaryPath:str,essayPath:str):
        """
        params:essayPath 等待分词文章
        params:glossaryPath 存量词汇表
        return
        """
        # stop_words
        stop_words=stopwords.words('english')
        newWordslist_trimBracket = []

        # 识别文章中的英语词汇
        with open(essayPath,'+r',encoding="utf-8") as f:
            newWordslist=[rl.replace("……","").replace("|","").replace("\\","").replace(":","").replace("."," ").replace(","," ").replace("*","").replace("?","").replace(".","").replace("!","").replace("(","").replace(")","").split() for rl in f.readlines()]
        for nl in newWordslist:
            newWordslist_trimBracket.extend(nl)
        newWordslist_set=set([word.lower() for word in newWordslist_trimBracket if len(re.findall(r'[^a-zA-Z]',word))==0])
        # 去除掉停词和存量词汇表已有词得到新增有效词汇
        added_terms=[word for word in newWordslist_set if word not in stop_words]
        # 新增词汇追加到glossary
        terms,stock_term_count=self.trim_glosssary(glossaryPath, added_terms)
        return terms,stock_term_count,len(added_terms)


if __name__ == '__main__':

    # extract from general or code
    glossaryPath='./glossary.txt'
    filePath='./soda_opera_terms.txt'
    gt=get_item()
    terms,stock_term_count,newly_term_count=gt.get_term(glossaryPath,filePath)
    mfd=make_flashcard()
    terms_2_fd=copy.deepcopy(terms)
    fail_count=0
    while len(terms_2_fd):
        result=terms_2_fd.pop()
        pagehtml=mfd.getPage(result)       # extra page context
        if pagehtml:
            flashCard=mfd.get_flashCard(pagehtml,result)    # make a anki flashcard
            if flashCard != '':
                make_logging.make_logging().log_info("{}'s anki flashcard has done!".format(result))
                for key,items in flashCard.items():
                    result+='@'+'<br>'.join(items)
                with open('./wordlist_导入.txt','a+',encoding='utf-8') as w:
                    w.write(result+'\n')
            else:
                fail_count +=1
    gt.add_2_glossary(glossaryPath,terms)
    make_logging.make_logging().log_info("summary:{} newly terms,{} stock terms, {} added terms, {} failure being flash card ,{} success being flash card ".format(newly_term_count,stock_term_count,len(terms),fail_count,len(terms)-fail_count))

    # extract from soup opera essay
    # glossaryPath = './glossary.txt'
    # essayPath = './soda opera essay.txt'
    # gt = get_item()
    # terms,stock_term_count,newly_term_count = gt.get_term_from_essay(glossaryPath, essayPath)
    # mfd=make_flashcard()
    # terms_2_fd=copy.deepcopy(terms)
    # fail_count=0
    # while len(terms_2_fd):
    #     result=terms_2_fd.pop()
    #     pagehtml=mfd.getPage(result)       # extra page context
    #     if pagehtml:
    #         flashCard=mfd.get_flashCard(pagehtml,result)    # make a anki flashcard
    #         if flashCard != '':
    #             make_logging.make_logging().log_info("{}'s anki flashcard has done!".format(result))
    #             for key,items in flashCard.items():
    #                 result+='@'+'<br>'.join(items)
    #             with open('./wordlist_导入.txt','a+',encoding='utf-8') as w:
    #                 w.write(result+'\n')
    #         else:
    #             fail_count +=1
    # gt.add_2_glossary(glossaryPath,terms)
    # make_logging.make_logging().log_info("summary:{} newly terms,{} stock terms, {} added terms, {} files has made".format(newly_term_count,stock_term_count,len(terms),files_num))
