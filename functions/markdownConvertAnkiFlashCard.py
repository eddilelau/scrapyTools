#coding:utf-8

import markdown,codecs,re
input_file = codecs.open("C:/Users/ED/Desktop/新建文件夹/note/linux.md", mode="r", encoding="utf-8")
# print("readlines",input_file.readlines(),"\n")

flashCard_name=""
flashCard_content=""
for line in input_file.readlines():
    pattern=r'^#'
    if re.search(pattern,line):
        print(flashCard_name, "\t",flashCard_content)
        flashCard_name = ""
        flashCard_content =""
        flashCard_name = line.replace("\n","").replace("#","").lstrip().rstrip()
    elif flashCard_content !="":
        flashCard_content +="</br>"
        flashCard_content +=line.replace("\n","")
    else:
        flashCard_content +=line.replace("\n","")



