# encode:utf-8
import re

class mk_2_fc(object):
    def toggle(self,file_path:str):
        compile = r'^#'
        flashCardName = ""
        flash_content = ""
        f=open(file_path,"+r",encoding="utf-8")
        for line in f.readlines():
            if re.match(compile,line):
                print(flashCardName,"\t",flash_content)
                flash_content = ""
                flashCardName=line.strip().replace("#","").replace(" ","")
            elif line !="\n":
                flash_content +=line.replace("\n","")+"</br>"

if __name__ == '__main__':
    file_path=""
    mk_2_fc.toggle(file_path)
