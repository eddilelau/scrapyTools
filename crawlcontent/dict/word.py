#coding:utf-8
import json
import urllib.request
from bs4 import BeautifulSoup



def getPage(myword:str):
    '''
    :param myword:查询单词
    :return:html
    '''
    basurl='http://dict.cn/'
    searchurl=basurl+myword
    response =  urllib.request.urlopen(searchurl)
    html = response.read()
    return html

def get_wordmeaning(html_selector:str):
    '''
    :param html_selector:
    :return:
    '''
    selector=BeautifulSoup(html_selector, "lxml")
    # print(selector)
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

def get_sentence(html_selector:str):
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

def get_phonetic_pronunciation(html_selector:str):
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
        return " "

def get_explain(html_selector:str):
    explain={}
    selector=BeautifulSoup(html_selector, "lxml")
    result=selector.find_all('div', {'class': 'basic clearfix'})[0]
    result=result.find_all('ul')
    base_url='http://audio.dict.cn/'
    i=1
    for item in result:
        for i in item.find_all('li'):  # 获取解析,
            i_=i.get_text().replace('\t','').replace('\n','')
            i_='' if 'if' in i_ else i_
            explain.setdefault('explain', []).append(i_)
    # print(explain)
    if len(explain) > 0:
        return explain  # 返回解析
    else:
        return " "

def get_word(word:str):
    #获得页面
    pagehtml=getPage(word)
    attribute = []
    explain = []
    word = []
    phonetic = []
    pronunciation = []
    sentences = []
    #单词释义
    explain = get_explain(pagehtml)
    #单词音标及读音
    phonetic = get_phonetic_pronunciation(pagehtml)
    #单词例句
    sentences = get_sentence(pagehtml)

    if len(explain)>0:
        explain.update(phonetic)
        explain.update(sentences)
        return explain
    else:
        return ''

if __name__ == '__main__':
    wordlist=[]
    with open('./wordlist.txt','r') as f:
        for word in f.readlines():
            wordlist.append(word)
    for word in wordlist:
        print(word)
        result=word.replace('\n','')
        if get_word(word) != '':
            for key,items in get_word(word).items():
                result+='@'+'<br>'.join(items)
            print(result)
            with open('./wordlist_导入.txt','a+',encoding='utf-8') as w:
                w.write(result+'\n')
