#coding:utf-8
import json
import urllib.request
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


def getPage(myword:str):
    '''
    :param myword:查询单词
    :return:html
    '''
    basurl='http://dict.cn/'
    searchurl=basurl+myword
    try:
        response =  urllib.request.urlopen(searchurl)
        html = response.read()
        return html
    except:
        print("{} is a error words,the html repsonse it is invail".format(myword))
        with open("./errorWords.txt",'a+',encoding="utf-8") as f:
            f.write(myword+";{} is a error words,the html repsonse it is invail".format(myword)+"\n")
        return False

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

def get_phonetic_pronunciation(html_selector:str,myword:str):
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

def get_flashCard(pagehtml:str,myword:str):
    # 单词释义
    explain = get_explain(pagehtml)
    #单词音标及读音
    phonetic = get_phonetic_pronunciation(pagehtml,myword)
    #单词例句
    sentences = get_sentence(pagehtml)

    if len(explain)>0 and phonetic !="" :
        explain.update(phonetic)
        explain.update(sentences)
        return explain
    else:
        return ''

def get_discernterm(glossaryPath:str,essayPath:str):
    """
    :param glossaryPath :存量词汇表地址
    :param essayPath :待识别文章地址
    :return:newWordsList_set_trimStopwordandglossary:新增词汇
    """
    # 加载已有词表
    with open(glossaryPath,'+r') as f2:
        glossary_trim = [ word.replace("\n","") for word in f2.readlines()]
    # 加载停用词表
    stop_words=stopwords.words('english')
    # 识别文章中的英语词汇
    newWordslist_trimBracket = []
    with open(essayPath,'+r') as f:
        newWordslist=[rl.replace("."," ").replace(","," ").split() for rl in f.readlines()]
    for nl in newWordslist:
        newWordslist_trimBracket.extend(nl)
    newWordslist_set=set([word.lower() for word in newWordslist_trimBracket])
    # 去除掉停词和存量词汇表已有词得到新增有效词汇
    newWordsList_set_trimStopwordAndglossary=[word for word in newWordslist_set if word not in glossary_trim and word not in stop_words]
    # 新增词汇追加到glossary
    with open(glossaryPath,'+a') as f3:
        for nt in newWordsList_set_trimStopwordAndglossary:
            f3.write(nt+"\n")
    return newWordsList_set_trimStopwordAndglossary


if __name__ == '__main__':
    objectPatch='./code/'
    glossaryPath=objectPatch+'glossary.txt'
    essayPath=objectPatch+'essay.txt'
    wordlist=get_discernterm(glossaryPath,essayPath)
    for word in wordlist:
        print('crawl {} is starting …………'.format(word))
        result=word.replace('\n','')
        pagehtml=getPage(result)
        if pagehtml:
            flashCard=get_flashCard(pagehtml,result)
            if flashCard != '':
                for key,items in flashCard.items():
                    result+='@'+'<br>'.join(items)
                print(result)
                with open('./wordlist_导入.txt','w+',encoding='utf-8') as w:
                    w.write(result+'\n')
