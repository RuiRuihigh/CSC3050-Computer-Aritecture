
from re import L
import re

#deleat comments  
def dc(line):
    line.lstrip()
    if line.find("#")==0:
        return ""
    elif line.find('#')>0:
        return line[:line.find('#')]
    else:
        return line

def no_comment(file):
    old_file=file
    fopen= open(old_file,'r')
    w_str=""
    for line in fopen:
        if re.search('#',line):
            line = line[:line.find('#')]
            if line.find('\n')<0:
                line = line + '\n'
            else:
                pass
            w_str+=line
        else:
            w_str+=line
    #print(w_str)
    wopen=open('nocomment.txt','w')
    wopen.write(w_str)
    fopen.close()
    wopen.close()
    return 'nocomment.txt'



#turn key to list(type of instructions)
def tl(dict_name):
    kl=""
    for key in dict_name.items():
        kl = kl + key + " "
    return kl

# find label
def fl(line):  
    if line.find(":")>=0:
        a = line.split(":")
    return a[0]










