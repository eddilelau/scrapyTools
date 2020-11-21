# --coding:utf-8 ---
import re
import requests

def UPFM(filename,regular_pattern,upload_dir,replace_dir):
    with open(filename,mode='r',encoding='utf-8') as fn:
        content=''
        for line in fn.readlines():
            img_urls=re.findall(regular_pattern, line, re.S)
            if len(img_urls)>0:
                for img_url in img_urls:
                    img_name=img_url.split('/')[-1].split('?')[0]
                    upload_dir_imgname=upload_dir+img_name
                    replace_pattern=replace_dir+img_name
                    with open(upload_dir_imgname,mode='wb') as upload_img:
                        upload_img.write(requests.get(img_url, stream=True).content)
                        print(img_name,'下载成功')
                    content +=line.replace(img_url,replace_pattern)
            else:
                content +=line
    with open(filename,mode='w',encoding='utf-8') as fn:
        fn.write(content)



if __name__ == '__main__':
    filename='E:/SynologyDrive/笔记/100 - 项目管理/on_going/on_going 20200809 法律维权/维权 淘宝消费.md'
    upload_dir='E:/SynologyDrive/笔记/100 - 项目管理/pics/'
    replace_dir='../../pics/'
    regular_pattern='\[img\]\((.*)\)'
    UPFM(filename,regular_pattern,upload_dir,replace_dir)
