
import re
import requests

class dp(object):
    def download_from_url(self,pic_url:str):
        r = requests.get(pic_url, stream=True)
        pic_name=re.split(r'/',pic_url)
        if "mmbiz_gif" in pic_name:
            open('E:/SynologyDrive/笔记/100 - 项目管理/pics/{}.{}'.format(pic_name[4],"gif"), 'wb').write(r.content)  # 将内容写入图片
        else:
            open('E:/SynologyDrive/笔记/100 - 项目管理/pics/{}.{}'.format(pic_name[4] ,"jpg"), 'wb').write(r.content)  # 将内容写入图片


