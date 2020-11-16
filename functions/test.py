import re

line="## fasfadsfsadfsdf"
compile=r'^##[^#]'
if len(re.findall(compile,line,re.S)) >= 1 :
    print("not none")
    print(re.findall(compile,line))