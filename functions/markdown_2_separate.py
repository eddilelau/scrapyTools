# coding:utf-8
import os
import re


class mk_2_s(object):
    def __init__(self,file_dir:str,compile:str,sep_compile:str,file_sep:str):
        self.file_dir=file_dir
        self.compile=compile
        self.sep_compile=sep_compile
        self.file_sep=file_sep
        self.filename=""

    def file_exist(self):
        if not(os.path.exists(self.file_dir)):
            os.mkdir(self.file_dir)

    def separate(self):
        with open(self.file_sep, encoding="utf-8") as f:
            for line in f.readlines():
                if len(re.findall(compile,line,re.S)) >= 1 :
                    self.filename=line.split(self.sep_compile)[1].replace("\n","")
                    print(self.filename,"is beginning separate.......")
                else:
                    with open("{}{}.md".format(self.file_dir, self.filename), mode="a", encoding="utf-8") as f2:
                        f2.write(line)


if __name__ == '__main__':
    compile=r'^###[^#]'  # regular compile
    sep_compile="###"   # separate pattern
    file_dir='E:/SynologyDrive/笔记/200 - 个人知识库/202 - 编程/编程语言/Python/PYPI/'
    file_sep='E:/SynologyDrive/笔记/200 - 个人知识库/202 - 编程/编程语言/Python/PYPI/PyPI.md'
    mk=mk_2_s(compile=compile,sep_compile=sep_compile,file_dir=file_dir,file_sep=file_sep)
    mk.separate()
