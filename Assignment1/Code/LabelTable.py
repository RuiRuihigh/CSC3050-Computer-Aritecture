from phase1 import fl,dc
import re


#store labels into dict   
def stld(li,o):
    dic = {}
    for i in range(0,len(li)):
        dic[li[i]] = o[i]
    return dic

#store the label and correspomding address
def address(test_file):
    t = 4194304
    o = []
    L = []
    #j=0
    with open(test_file,"r") as file_object:
        test_file_lines=file_object.readlines()
        #print(test_file_lines)
    a = False
    for i in range(0,len(test_file_lines)):
        test_file_lines[i] = test_file_lines[i].replace('\n','')
        if a==True:
            if test_file_lines[i].find(":")>=0:
                L.append(fl(test_file_lines[i]))
                o.append(str(hex(t))[2:])
            else:
                t=t+4
        if test_file_lines[i].find(".text")>=0:
            a = True
    #print(L)
    return stld(L,o)



    #line=expect_lines[i]
    #line=line.replace("\n","").replace(" ","").replace("\t","") #delete "\n","\t" and space
    #expect_lines[i]=line

def itl(la):
    lab=''
    c = bin(int(str(la),16))[2:].zfill(16)
    #for i in range(0,len(c)):
        #if i >13 and i<30:
            #lab = lab + c[i]
    return c

def jtl(la):
    lab=''
    c = bin(int(str(la),16))[2:].zfill(32)
    for i in range(0,len(c)):
        if i >3 and i<30:
            lab = lab + c[i]
    return lab

def branch_table(file):
    old_file=file
    fopen= open(old_file,'r')
    w_str=""
    for line in fopen:
        if re.search(':',line):
            line = re.sub('\n','',line)
            w_str+=line
        else:
            w_str+=line
    wopen=open('tee.txt','w')
    wopen.write(w_str)
    fopen.close()
    wopen.close()
    fi_ob_lines = []
    valid_line=[]
    p=[]
    j=[]
    with open('tee.txt') as fi_ob:
        fi_ob_line=fi_ob.readlines()
        for i in range(0,len(fi_ob_line)):
            fi_ob_line[i] = dc(fi_ob_line[i])
            if len(fi_ob_line[i])>0:
                fi_ob_lines.append(fi_ob_line[i])
        a = False
        for i in range(0,len(fi_ob_lines)):
            if a==True:
                valid_line.append(fi_ob_lines[i])
            if fi_ob_lines[i].find(".text")>=0:
                a = True
    valid_valid_line = []
    for g in range(0,len(valid_line)):
        valid_line[g] = valid_line[g].replace('\n','')
        a= valid_line[g]
        if valid_line[g].find(':')>=0:
            a = a.split(":")
            valid_valid_line.append(a[1])
            p.append(g)
            j.append(a[0].lstrip())
        else:
            valid_valid_line.append(a)
    return j,p,valid_valid_line
    #for g in range(0,len(valid_line)):
        #valid_line[g] = valid_line[g].replace('\n','')
        #specific_instruction = valid_line[g].lstrip().lstrip('\t').split(' ')[0]

