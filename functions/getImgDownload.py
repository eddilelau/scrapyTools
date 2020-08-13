
import re
import requests

with open('E:/SynologyDrive/笔记/100 - 项目管理/archive/archive 20200625 广州好玩好吃/江南西篇.md',encoding='utf-8') as f:
    pattern=re.compile(r'img\]\((.*)\)')
    pics=[]
    for line in f.readlines():
        if len(re.findall(pattern,line)):
            pics.append(re.findall(pattern,line)[0])

print(pics)
for pic in pics:
    r = requests.get(pic, stream=True)
    pic_name=re.split(r'/',pic)[-1]
    print(pic_name)
    open('E:/SynologyDrive/笔记/100 - 项目管理/pics/{}'.format(pic_name), 'wb').write(r.content)  # 将内容写入图片


