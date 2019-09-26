# coding:utf-8
"""
datetime:2019/09/24
sofeware:PyCharm
description:
"""
import base64
import hashlib
import hmac
import json
import random
import time
import requests
from http import cookiejar
from PIL import Image
import matplotlib.pyplot as plt
import execjs
from urllib.parse import urlencode
from config import *

def getRanduserAgent():
    USER_AGENTS=[
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


class zhihuLogin(object):
    def __init__(self,account:str,password:str):
        self.account = account
        self.password = password
        self.session = requests.session()
        self.session.cookies =cookiejar.LWPCookieJar(filename="./cookies.txt")

        self.session.headers ={
            'accept-encoding': 'gzip, deflate, br',
            'Host': 'www.zhihu.com',
            'Referer': 'https://www.zhihu.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        }

        self.logindata ={
            'username':'',
            'password':'',
            'timestamp':'',
            'client_id':"c3cef7c66a1843f8b3a9e6a1e3160e20",
            'grant_type':"password",
            'source':"com.zhihu.web",
            'signature':'',
            'captcha':'',
            'lang':'en',
            'utm_source':'',
            'ref_source':'homepage',
        }
        self.captcha_api ={
            'cn':"https://www.zhihu.com/api/v3/oauth/captcha?lang=cn",
            'en':"https://www.zhihu.com/api/v3/oauth/captcha?lang=en",
        }

    def loginWithcookies(self):
        """
        加载cookies登录账号
        :return:bool
        """
        try:
            self.session.cookies.load(ignore_discard=True)
            print("成功加载cookies")
            return True
        except FileNotFoundError:
            print("找不到本地cookies文件,需要进行账号和密码登录")
            return False

    def login(self,lang:str="en",load_cookies:bool=True):
        """
        :param captcha:验证码类型 "en" or "cn"
        :param load_cookies:是否加载上次的cookies
        :return:True
        """
        if load_cookies and self.loginWithcookies():
            if self.verifyLogin():
                print("账号{}成功登陆".format(self.account))
                return True
            else :
                print("加载cookies失败,需要重新登录")
        self._verify_user_pass()
        self.logindata['username'] = self.account
        self.logindata['password'] = self.password
        self.logindata['lang'] =lang
        self.logindata['timestamp'] =int(time.time() * 1000)
        self.logindata['captcha'] = self.get_captcha()
        self.logindata['signature'] = self.getSignature()

        headers = self.session.headers.copy()
        headers.update({
            'x-xsrftoken': self.getXcrftoken(),
            'content-type': 'application/x-www-form-urlencoded',
            'x-zse-83': '3_1.1',
        })
        encrypt_token = self.getEncrypt()
        print(encrypt_token)
        login_api = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        response = self.session.post(login_api,data=encrypt_token,headers=headers)
        print("response.text",response.text)
        print("response.json()",response.json())
        if 'error' in response.text:
            print(json.loads(response.text)['error'])
            return False
        if self.verifyLogin():
            print("账号{}密码登录成功".format(self.account))
            return True
        return False

    def getXcrftoken(self):
        """
        访问主页禁止跳转,从cookies获取xsrf
        :return:str
        """
        domain_api = 'https://www.zhihu.com/'
        self.session.get(domain_api,headers=self.session.headers,allow_redirects=False)
        for item in self.session.cookies:
            if "_xsrf" == item.name:
                return item.value
        assert AssertionError("获取_xsrf失败")

    def get_captcha(self):
        """
        第一次get请求为询问服务器是否需要验证码
        第二次put请求为获取验证码
        第三次请求为将验证码post到服务器
        :return: 验证码
        """
        captcha_api =self.captcha_api[self.logindata['lang']]
        response=self.session.get(captcha_api)
        if 'true' in response.text:
            img_response=self.session.put(captcha_api)
            img_base64 = img_response.json()['img_base64']
            with open('./captcha.jpg','wb') as f:
                f.write(base64.b64decode(img_base64))
            img=Image.open('./captcha.jpg')
            if self.logindata['lang'] == 'cn':
                plt.imshow(img)
                print('点击所有倒立的汉字，在命令行中按回车提交')
                points=plt.ginput(7)
                input_text=json.loads({
                    'img_size': [200, 44],
                    'input_points': [[i[0] / 2, i[1] / 2] for i in points]
                })
            else:
                # img_threading=threading.Thread(target=img.show,daemon=True)
                # img_threading.start()
                input_text=input("请输入验证码:")
            data ={"input_text":input_text,}
            captcha_response=self.session.post(captcha_api, data=data)   #这里需要验证是否成功

            if "success" not in captcha_response.text:
                print("验证失败,需要重新请求验证码......")
                self.get_captcha()
            else:
                return input_text
        return ''

    def getSignature(self):
        """
        hmac加密timestamp、client_id、grant_type、source
        除了timestamp之外,其他全部都是固定值
        :return:str
        """
        timestamp=self.logindata['timestamp']
        client_id = self.logindata['client_id']
        grant_type =self.logindata['grant_type']
        source =self.logindata['source']
        ha=hmac.new(b'd1b964811afb40118a12068ff74a12f4',digestmod=hashlib.sha1)
        # ha.update(bytes(( str(timestamp) + client_id + grant_type + source),'utf-8'))
        ha.update(bytes((grant_type + client_id + source + str(timestamp)), 'utf-8'))

        print(timestamp)
        return  ha.hexdigest()

    def getEncrypt(self):
        """
        通过混淆js将self.logindata的参数加密
        :return:密钥
        """
        with open('./encrypt.js','r',encoding='utf-8') as f:
            js_code = f.read()
        cxt=execjs.compile(js_code)
        return cxt.call('Q',urlencode(self.logindata))

    def verifyLogin(self):
        """
        检查账号登录状态,若账号登录成功后访问登录页会自动跳转.
        登录页跳转后保存当前cookies
        :return:bool
        """
        verify_url = "https://www.zhihu.com/signup"
        response = self.session.get(verify_url,headers=self.session.headers,allow_redirects=False) #跳转则表示成功
        if response.status_code == 302:
            self.session.cookies.save()
            return True
        return False

    def _verify_user_pass(self):
        """
        检查账号和密码是否已输入,如果没输入提醒输入
        """
        if not(self.account):
            self.account = input("请输入手机号码:")
        if self.account.isdigit() and "+86" not in self.account:
            self.account = "+86" + self.account
        if not(self.password):
            self.password = input("请输入账号密码:")


if __name__ == '__main__':
    zL=zhihuLogin(account=zhihu_account,password=zhihu_password)
    zL.login(lang="en",load_cookies=True)   #en for 字母验证码,cn for 中文验证码