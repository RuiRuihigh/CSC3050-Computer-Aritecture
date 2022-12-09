from multiprocessing.sharedctypes import Value
import os
import re
import copy
from te import high_8,high_mid8,low_mid8,low_8,low_16,high_16
import sys
from sys import argv
pyth, asm, txt, checkpts, inputfi, outputfi  = argv
def addBinary(a,b):
        a = str(a)
        b = str(b)
        """
        :type a: str
        :type b: str
        :rtype: str
        """
        if len(a) < len(b):    #以长的二进制字符串为遍历起点
            temp = a
            a = b
            b = temp
        a = a[::-1]           #倒序二进制字符串
        b = b[::-1]
        extra = 0             #进位
        new_binary = ""
        for index, num in enumerate(a):     #遍历
            if index > len(b) - 1:          #判断短的二进制字符串是否越界
                b_sum = 0
            else:
                b_sum = int(b[index])
            new_binary = new_binary + str((int(num) + b_sum + extra) % 2)     #二进制加法运算
            if int(num) + b_sum + extra > 1:     #是否进位
                extra = 1
            else:
                extra = 0
        if extra == 1:        #最高位是否进位
            new_binary = new_binary + "1"     
        return new_binary[::-1] 
 #针对二进制的补码
def sign_bin(i):
    i = str(i)
    t =[]
    for j in range(0,len(i)):
        if i[j]=="0":
            t.append("1")
        elif i[j]=="1":
            t.append("0")
    i = ''.join(t)
    i = addBinary(i,1)
    return i
def creat_mem():
    mem_dic = {}
    a = 4194304
    while a<=10485756:
        mem_dic[str(hex(a))]=0
        a = a + 4
    return mem_dic
def creat_reg_dic():
    gg = {}
    reg = {'$zero':'00000','$at':'00001','$v0':'00010','$v1':'00011','$a0':'00100',
        '$a1':'00101','$a2':'00110','$a3':'00111','$t0':'01000','$t1':'01001',
        '$t2':'01010','$t3':'01011','$t4':'01100','$t5':'01101','$t6':'01110',
        '$t7':'01111','$s0':'10000','$s1':'10001','$s2':'10010','$s3':'10011',
        '$s4':'10100','$s5':'10101','$s6':'10110','$s7':'10111','$t8':'11000',
        '$t9':'11001','$k0':'11010','$k1':'11011','$gp':'11100','$sp':'11101',
        '$fp':'11110','$ra':'11111'}
    for key, value in reg.items():
        gg[value] = key
    return gg
def read_mac_code(file,dic):
    mem_dic = dic
    b = 4194304
    with open (file, 'r') as f:
        li=f.readlines()
        for i in range(0,len(li)):
            li[i] = li[i].replace('\n','')
            #mem_dic[str(hex(b+i*4))]=int('0b'+li[i],2)
            mem_dic[str(hex(b+i*4))]=li[i]
    return mem_dic
def read_asm_data(file,dic):
    global bre
    c1 = []
    c2 = []
    c = 5242880
    with open (file, 'r') as f:
        li=f.readlines()
    a = False
    for i in range(0,len(li)):
        if li[i].find(".data")>=0:
            a = True
        elif li[i].find(".text")>=0:
            a = False
        else:
            if len(li[i])>2 and a ==True:
                g = li[i].split(":",1)
                b = g[1].replace("\n","")
                b=b.strip()
                b0=b.split(" ",1)[0]
                b1=b.split(" ",1)[1]
                if b1.find('"')<0:
                    b1 = b1.split(",")
                    #b1 = "".join(b1)
                else:
                    b1 = b1.replace('"','')
                    b1 = b1.replace("\\n","\n")
                c1.append(b0.strip())
                c2.append(b1)
            else:
                pass
    for i in range(len(c1)):
        if c1[i]==".word":
            print(c2[i])
            for j in range(len(c2[i])):
                t = int(c2[i][j])
                print(t)
                #dic[str(hex(c))]=(int(c2[i][j]))<<24
                dic[str(hex(c))]= (high_8(t)) + (high_mid8(t)<<8) + (low_mid8(t)<<16) + (low_8(t)<<24)
                #print(hex(dic[str(hex(c))]))
                #pt = (high_8(t)>>24) + (high_mid8(t)>>8) + (low_mid8(t)<<8) + (low_8(t)<<24)
                c = c + 4
        elif c1[i]==".ascii":
            l=0
            while True:
                if len(c2[i])-4*l>4:
                    j1 = ord(c2[i][0+4*l])
                    j2 = ord(c2[i][1+4*l])
                    j3 = ord(c2[i][2+4*l])
                    j4 = ord(c2[i][3+4*l])
                    dic[str(hex(c))]=(j1<<24)+(j2<<16)+(j3<<8)+j4
                    c = c + 4
                    l = l+1
                else:
                    j=[]
                    to = c2[i][0+4*l:]
                    for i in range(len(to)):
                        j.append(ord(to[i]))
                        dic[str(hex(c))]= dic[str(hex(c))] + (j[i]<<(24-8*i))
                    c = c+4
                    break
        elif c1[i]==".asciiz":
            c2[i] = c2[i]+'\0'
            l=0
            p=True
            while p==True:
                if len(c2[i])-4*l>4:
                    j1 = ord(c2[i][0+4*l])
                    j2 = ord(c2[i][1+4*l])
                    j3 = ord(c2[i][2+4*l])
                    j4 = ord(c2[i][3+4*l])
                    dic[str(hex(c))]=(j1<<24)+(j2<<16)+(j3<<8)+j4
                    c = c + 4
                    l = l+1
                else:
                    j=[]
                    to = c2[i][0+4*l:]
                    for i in range(len(to)):
                        j.append(ord(to[i]))
                        dic[str(hex(c))]= dic[str(hex(c))] + (j[i]<<(24-8*i))
                    c = c+4
                    p=False
        elif c1[i]==".byte":
            l=0
            while True:
                if len(c2[i])-4*l>4:
                    j1 = int(c2[i][0+4*l])
                    j2 = int(c2[i][1+4*l])
                    j3 = int(c2[i][2+4*l])
                    j4 = int(c2[i][3+4*l])
                    dic[str(hex(c))]=(j1<<24)+(j2<<16)+(j3<<8)+j4
                    c = c + 4
                    l = l+1
                else:
                    j=[]
                    to = c2[i][0+4*l:]
                    for i in range(len(to)):
                        j.append(int(to[i]))
                        dic[str(hex(c))]= dic[str(hex(c))] + (j[i]<<(24-8*i))
                    c = c+4
                    break
        elif c1[i]==".half":
            l=0
            while True:
                if len(c2[i])-2*l>2:
                    j1 = int(c2[i][0+2*l])
                    j2 = int(c2[i][1+2*l])
                    dic[str(hex(c))]=(j1<<24)+(j2<<8)
                    c = c + 4
                    l = l+1
                else:
                    j=[]
                    to = c2[i][0+2*l:]
                    for i in range(len(to)):
                        j.append(int(to[i]))
                        dic[str(hex(c))]= dic[str(hex(c))] + (j[i]<<(24-16*i))
                    c = c+4
                    break
    bre = c
    return dic
def reg_con():
    reg = {'$zero':'00000','$at':'00001','$v0':'00010','$v1':'00011','$a0':'00100',
        '$a1':'00101','$a2':'00110','$a3':'00111','$t0':'01000','$t1':'01001',
        '$t2':'01010','$t3':'01011','$t4':'01100','$t5':'01101','$t6':'01110',
        '$t7':'01111','$s0':'10000','$s1':'10001','$s2':'10010','$s3':'10011',
        '$s4':'10100','$s5':'10101','$s6':'10110','$s7':'10111','$t8':'11000',
        '$t9':'11001','$k0':'11010','$k1':'11011','$gp':'11100','$sp':'11101',
        '$fp':'11110','$ra':'11111'}
    for key,Value in reg.items():
        reg[key]=0
    reg['$fp']=10485760
    reg['$sp']=10485760
    reg['$gp']=0x508000
    reg["PC"]="0x400000"
    reg["HI"]=0
    reg["LO"]=0
    return reg
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
def operation(mc,dic1,dic2,dic3): #dic1:map of reg and code  dic2:reg_mem #dic3:mem_dic
    global bre
    #print(mc)
    fun = mc[26:]
    op = mc[:6]
    if fun=="100000"and op=="000000": #add 
        rs = mc[6:11]
        rt = mc[11:16]
        rd = mc[16:21]
        rs = dic1[rs]
        rt = dic1[rt]
        rd = dic1[rd]
        dic2[rd] = dic2[rs] + dic2[rt]
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="100001"and op=="000000":#addu
        rs = mc[6:11]
        rt = mc[11:16]
        rd = mc[16:21]
        rs = dic1[rs]
        rt = dic1[rt]
        rd = dic1[rd]
        dic2[rd] = dic2[rs] + dic2[rt]
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="100100"and op=="000000": #and
        rs = mc[6:11]
        rt = mc[11:16]
        rd = mc[16:21]
        rs = dic1[rs]
        rt = dic1[rt]
        rd = dic1[rd]
        s = dic2[rs]
        t = dic2[rt]
        dic2[rd] = s&t
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="011010"and op=="000000": #div 
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        dic2["LO"]=dic2[rs]//dic2[rt]
        dic2["HI"]=dic2[rs]%dic2[rt]
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="011011"and op=="000000": #divu 
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        dic2["LO"]=dic2[rs]//dic2[rt]
        dic2["HI"]=dic2[rs]%dic2[rt]
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="001001"and op=="000000": #jalr
        rs = mc[6:11]
        rd = mc[16:21]
        rs = dic1[rs]
        if rd in dic1.keys():
            rd = dic1[rd]
        else:
            rd = "$ra"
        dic2[rd] = int((hex(int(dic2["PC"],16)+4)),16)
        dic2["PC"] = hex(dic2[rs])
    elif fun=="001000"and op=="000000": #jr
        rs = mc[6:11]
        rs = dic1[rs]
        dic2["PC"] = hex(dic2[rs])
    elif fun=="010000"and op=="000000": #mfhi
        rd = mc[16:21]
        rd = dic1[rd]
        dic2[rd]=dic2["HI"]
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="010010"and op=="000000": #mflo
        rd = mc[16:21]
        rd = dic1[rd]
        dic2[rd]=dic2["LO"]
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="010001"and op=="000000": #mthi
        rs = mc[6:11]
        rs = dic1[rs]
        dic2["HI"]=dic2[rs]
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="010011"and op=="000000": #mtlo
        rs = mc[6:11]
        rs = dic1[rs]
        dic2["LO"]=dic2[rs]
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="011000"and op=="000000": #mult
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        res = dic2[rs]*dic2[rt]
        res = bin(res)[2:].zfill(64)
        dic2["LO"]=int("0b"+res[32:64],2)
        dic2["HI"]=int("0b"+res[0:32],2)
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="011001"and op=="000000": #multu
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        res = dic2[rs]*dic2[rt]
        res = bin(res)[2:].zfill(64)
        dic2["LO"]=int("0b"+res[32:64],2)
        dic2["HI"]=int("0b"+res[0:32],2)
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="100111"and op=="000000": #nor
        rs = mc[6:11]
        rt = mc[11:16]
        rd = mc[16:21]
        rs = dic1[rs]
        rt = dic1[rt]
        rd = dic1[rd]
        s = dic2[rs]
        t = dic2[rt]
        dic2[rd] = ~(s&t)
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="100101"and op=="000000": #or
        rs = mc[6:11]
        rt = mc[11:16]
        rd = mc[16:21]
        rs = dic1[rs]
        rt = dic1[rt]
        rd = dic1[rd]
        s = dic2[rs]
        t = dic2[rt]
        dic2[rd] = s|t
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="000000"and op=="000000": #sll
        rt = mc[11:16]
        rd = mc[16:21]
        shamt = mc[21:26]
        shamt = int("0b"+shamt,2)
        rt = dic1[rt]
        rd = dic1[rd]
        t = dic2[rt]
        dic2[rd] = t<<shamt
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="000100"and op=="000000": #sllv
        rs = mc[6:11]
        rt = mc[11:16]
        rd = mc[16:21]
        rs = dic1[rs]
        rt = dic1[rt]
        rd = dic1[rd]
        s = dic2[rs]
        t = dic2[rt]
        dic2[rd] = t<<s
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="101010"and op=="000000": #slt
        rs = mc[6:11]
        rt = mc[11:16]
        rd = mc[16:21]
        rs = dic1[rs]
        rt = dic1[rt]
        rd = dic1[rd]
        s = dic2[rs]
        t = dic2[rt]
        if s<t:
            dic2[rd] = 1
        else:
            dic2[rd] = 0
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="101011"and op=="000000": #sltu
        rs = mc[6:11]
        rt = mc[11:16]
        rd = mc[16:21]
        rs = dic1[rs]
        rt = dic1[rt]
        rd = dic1[rd]
        s = dic2[rs]
        t = dic2[rt]
        if s<t:
            dic2[rd] = 1
        else:
            dic2[rd] = 0
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="000011"and op=="000000": #sra
        rt = mc[11:16]
        rd = mc[16:21]
        shamt = mc[21:26]
        shamt = int("0b"+shamt,2)
        rt = dic1[rt]
        rd = dic1[rd]
        t = dic2[rt]
        dic2[rd] = t>>shamt
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="000111"and op=="000000": #srav
        rs = mc[6:11]
        rt = mc[11:16]
        rd = mc[16:21]
        rs = dic1[rs]
        rt = dic1[rt]
        rd = dic1[rd]
        s = dic2[rs]
        t = dic2[rt]
        dic2[rd] = t>>s
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="000010"and op=="000000": #srl
        rt = mc[11:16]
        rd = mc[16:21]
        shamt = mc[21:26]
        shamt = int("0b"+shamt,2)
        rt = dic1[rt]
        rd = dic1[rd]
        t = dic2[rt]
        if t<0:
            t=-t
            t = bin(t)[2:].zfill(32)
            t = sign_bin(t)
        else:
            t = bin(t)[2:].zfill(32)
        t =shamt*"0"+t
        j = t[:32]
        if j[0]=="0":
            dic2[rd] = int("0b"+j,2)
        else:
            t = sign_bin(t)
            dic2[rd] = -int("0b"+j,2)
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="000110"and op=="000000": #srlv
        rs = mc[6:11]
        rt = mc[11:16]
        rd = mc[16:21]
        rs = dic1[rs]
        rt = dic1[rt]
        rd = dic1[rd]
        s = dic2[rs]
        t = dic2[rt]
        if t<0:
            t=-t
            t = bin(t)[2:].zfill(32)
            t = sign_bin(t)
        else:
            t = bin(t)[2:].zfill(32)
        t = s*"0"+t
        j = t[:32]
        if j[0]=="0":
            dic2[rd] = int("0b"+j,2)
        else:
            t = sign_bin(t)
            dic2[rd] = -int("0b"+j,2)
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="100010"and op=="000000": #sub
        rs = mc[6:11]
        rt = mc[11:16]
        rd = mc[16:21]
        rs = dic1[rs]
        rt = dic1[rt]
        rd = dic1[rd]
        dic2[rd] = dic2[rs] - dic2[rt]
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="100011"and op=="000000": #subu
        rs = mc[6:11]
        rt = mc[11:16]
        rd = mc[16:21]
        rs = dic1[rs]
        rt = dic1[rt]
        rd = dic1[rd]
        dic2[rd] = dic2[rs] - dic2[rt]
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))  
    elif fun=="001100"and op=="000000": #syscall
        global f 
        global read_index
        global print_index
        print(111111111111111111111111111111)
        if dic2["$v0"]==1:
            if print_index==0:
                fi = open(outputfi,"w")
                imm = bin(dic2["$a0"])[2:].zfill(32)
                if imm[0]=="1":
                    sao = sign_bin(imm)
                    imm = -int("0b"+sao,2)
                else:
                    imm = dic2["$a0"]
                fi.write(str(imm))
                fi.close()
                print_index = print_index +1
            else:
                fi = open(outputfi,"a")
                imm = bin(dic2["$a0"])[2:].zfill(32)
                if imm[0]=="1":
                    sao = sign_bin(imm)
                    imm = -int("0b"+sao,2)
                else:
                    imm = dic2["$a0"]
                fi.write(str(dic2["$a0"]))
                fi.close()
                print_index = print_index +1
        elif dic2["$v0"]==4:
            if print_index==0:
                fi = open(outputfi,"w")
                #start_content = dic3[hex(dic2["$a0"])]
                ind =0
                cont = ""
                bo = True
                while bo==True:
                    print(hex(dic2["$a0"]+4*ind))
                    k1 = dic3[hex(dic2["$a0"]+4*ind)]
                    k11 = high_8(k1)
                    k12 = high_mid8(k1)
                    k13 = low_mid8(k1)
                    k14 = low_8(k1)
                    k11 = chr(k11)
                    k12 = chr(k12)
                    k13 = chr(k13)
                    k14 = chr(k14)
                    k111 = [k11,k12,k13,k14]
                    #print(k111)
                    for i in range(len(k111)):
                        if k111[i] != "\0":
                            cont = cont + k111[i]
                        else:
                            bo = False                           
                    ind = ind + 1
                print_index = print_index + 1
                print(cont)
                fi.write(cont)
                fi.close()            
            else:
                fi = open(outputfi,"a")
                a0 = dic2["$a0"]
                q = a0//4
                r = a0%4
                if r==0:
                    ind =0
                    cont = ""
                    bo = True
                    while bo==True:
                        k1 = dic3[hex(dic2["$a0"]+4*ind)]
                        k11 = high_8(k1)
                        k12 = high_mid8(k1)
                        k13 = low_mid8(k1)
                        k14 = low_8(k1)
                        k11 = chr(k11)
                        k12 = chr(k12)
                        k13 = chr(k13)
                        k14 = chr(k14)
                        k111 = [k11,k12,k13,k14]
                        #print(k111)
                        for i in range(len(k111)):
                            if k111[i] != "\0":
                                cont = cont + k111[i]
                            else:
                                bo = False                           
                        ind = ind + 1
                elif r==2:
                    ind =0
                    cont = ""
                    bo = True
                    while bo==True:
                        k1 = dic3[hex(4*q)]
                        k11 = low_mid8(k1)
                        k12 = low_8(k1)
                        k1 = dic3[hex(4*(q+1))]
                        k13 = high_8(k1)
                        k14 = high_mid8(k1)
                        k11 = chr(k11)
                        k12 = chr(k12)
                        k13 = chr(k13)
                        k14 = chr(k14)
                        k111 = [k11,k12,k13,k14]
                        for i in range(len(k111)):
                            if k111[i] != "\0":
                                cont = cont + k111[i]
                            else:
                                bo = False 
                        q = q+1
                print_index = print_index + 1
                fi.write(cont)
                fi.close()
        elif dic2["$v0"]==5:
            fi = open(in_file,"r")
            fii = fi.readlines()
            fi.close()
            for i in range(len(fii)):
                fii[i] = fii[i].replace("\n","")
            dic2["$v0"] = int(fii[read_index])
            read_index = read_index+1
        elif dic2["$v0"]==8:
            a0 = dic2["$a0"]
            q = a0//4
            r = a0%4
            print(hex(a0))
            a1 = dic2["$a1"]
            fi = open(in_file,"r")
            fii = fi.readlines()
            fi.close()
            #for i in range(len(fii)):
                #fii[i] = fii[i].replace("\n","")
            kk1 = fii[read_index]
            if len(kk1)>=a1:
                kk2 = kk1[:a1]
            else:
                kk2 = kk1
            #for i in range(len(kk2)):
            print(kk2)
            if r ==0:
                l=0
                p=True
                while p==True:
                    if len(kk2)-4*l>4:
                        print(1)
                        print(hex(a0))
                        j1 = ord(kk2[0+4*l])
                        j2 = ord(kk2[1+4*l])
                        j3 = ord(kk2[2+4*l])
                        j4 = ord(kk2[3+4*l])
                        dic3[str(hex(a0))]=dic3[str(hex(a0))] + (j1<<24)+(j2<<16)+(j3<<8)+j4
                        a0 = a0 + 4
                        l = l+1
                    else:
                        j=[]
                        to = kk2[0+4*l:]
                        for i in range(len(to)):
                            j.append(ord(to[i]))
                            dic3[str(hex(a0))]= dic3[str(hex(a0))] + (j[i]<<(24-8*i))
                        a0 = a0+4
                        p=False
            elif r ==2:
                l=0
                p=True
                while p==True:
                    if len(kk2)-4*l>4:
                        j1 = ord(kk2[0+4*l])
                        j2 = ord(kk2[1+4*l]) 
                        j3 = ord(kk2[2+4*l])
                        j4 = ord(kk2[3+4*l])
                        dic3[str(hex(4*q))]=dic3[str(hex(4*q))] + (j1<<8)+j2
                        dic3[str(hex(4*(q+1)))]=dic3[str(hex(4*(q+1)))] + (j3<<24)+(j4<<16)
                        q = q+1
                        a0 = 4*q+r
                        l = l+1
                    elif len(kk2)-4*l==4:
                        j1 = ord(kk2[0+4*l])
                        j2 = ord(kk2[1+4*l]) 
                        j3 = ord(kk2[2+4*l])
                        j4 = ord(kk2[3+4*l])
                        dic3[str(hex(4*q))]=dic3[str(hex(4*q))] + (j1<<8)+j2
                        dic3[str(hex(4*(q+1)))]=dic3[str(hex(4*(q+1)))] + (j3<<24)+(j4<<16)
                        q = q+1
                        a0 = 4*q+r
                        break
                    elif len(kk2)-4*l==3:
                        j1 = ord(kk2[0+4*l])
                        j2 = ord(kk2[1+4*l]) 
                        j3 = ord(kk2[2+4*l])
                        dic3[str(hex(4*q))]=dic3[str(hex(4*q))] + (j1<<8)+j2
                        dic3[str(hex(4*(q+1)))]=dic3[str(hex(4*(q+1)))] + (j3<<24)
                        q = q+1
                        a0 = 4*q+r
                        break
                    elif len(kk2)-4*l==2:
                        j1 = ord(kk2[0+4*l])
                        j2 = ord(kk2[1+4*l]) 
                        dic3[str(hex(4*q))]=dic3[str(hex(4*q))] + (j1<<8)+j2
                        q = q+1
                        a0 = 4*q+r
                        break
                    elif len(kk2)-4*l==1:
                        j1 = ord(kk2[0+4*l])
                        dic3[str(hex(4*q))]=dic3[str(hex(4*q))] + (j1<<8)
                        q = q+1
                        a0 = 4*q+r
                        break
            read_index = read_index+1
        elif dic2["$v0"]==9:
            a0 = dic2["$a0"]
            #print(a0)
            print(a0)
            print(hex(bre))
            #print(dic2["$gp"])
            dic2["$v0"] = bre
            bre = bre + a0
            #print(hex(bre))
        elif dic2["$v0"]==11:
            a0 = dic2["$a0"]
            a0 = chr(a0)
            if print_index ==0:
                fi = open(outputfi,"w")
                fi.write(a0)
            else:
                fi = open(outputfi,"a")
                fi.write(a0)
            fi.close()
            print_index = print_index +1
        elif dic2["$v0"]==12:
            fi = open(in_file,"r")
            fii = fi.readlines()
            fi.close()
            for i in range(len(fii)):
                fii[i] = fii[i].replace("\n","")
            kk1 = fii[read_index]
            j = ord(kk1)
            #print(j)
            dic2["$v0"] = j
            read_index = read_index+1
        elif dic2["$v0"]==13:
            a1 = dic2["$a1"]
            ind =0
            cont = ""
            bo = True
            while bo==True:
                print(hex(dic2["$a0"]+4*ind))
                k1 = dic3[hex(dic2["$a0"]+4*ind)]
                k11 = high_8(k1)
                k12 = high_mid8(k1)
                k13 = low_mid8(k1)
                k14 = low_8(k1)
                k11 = chr(k11)
                k12 = chr(k12)
                k13 = chr(k13)
                k14 = chr(k14)
                k111 = [k11,k12,k13,k14]
                    #print(k111)
                for i in range(len(k111)):
                    if k111[i] != "\0":
                        cont = cont + k111[i]
                    else:
                        bo = False                           
                ind = ind + 1
            a0 = cont
            print(a1)
            #if a1==2:
                #f = open(a0,"r")
                #print("#########################")
                #f = open("file.txt","r")
            #elif a1 ==1:
                #f = open(a0,"w")
            #elif a1==66:
                #f = open(a0,"w")
                #f.close()
                #f = open(a0,"a")
                #f = open("file.txt","a")
            f = os.open(a0,a1)
            #f = os.open( "file.txt",a1)
            #f = os.open( "file.txt", os.O_RDWR|os.O_CREAT )
            dic2["$a0"] = ord("f")
        elif dic2["$v0"]==14:
            a0 = eval(chr(dic2["$a0"]))
            a1 = dic2["$a1"]
            a2 = dic2["$a2"]
            fii = os.read(a0,a2)
            #for i in range(len(fii)):
                #fii[i] = fii[i].replace("\n","")
            print(fii)
            kk1 = fii
            kk2 = kk1
            kk2 = kk2.decode()
            le = len(kk2)
            print(kk2)
            l=0
            p=True
            while p==True:
                if len(kk2)-4*l>4:
                    print(ord(kk2[0+4*l]))
                    j1 = ord(kk2[0+4*l])
                    j2 = ord(kk2[1+4*l])
                    j3 = ord(kk2[2+4*l])
                    j4 = ord(kk2[3+4*l])
                    dic3[str(hex(a1))]=(j1<<24)+(j2<<16)+(j3<<8)+j4
                    a1 = a1 + 4
                    l = l+1
                else:
                    j=[]
                    to = kk2[0+4*l:]
                    print("0000000000")
                    print(len(to))
                    for i in range(len(to)):
                        j.append(ord(to[i]))
                        print(j)
                        dic3[str(hex(a1))]= dic3[str(hex(a1))] + (j[i]<<(24-8*i))
                    a1 = a1+4
                    p=False
            dic2["$a0"]  = le
        elif dic2["$v0"]==15:
            a0 = eval(chr(dic2["$a0"]))
            a1 = dic2["$a1"]
            a2 = dic2["$a2"]
            ind =0
            cont = ""
            bo = True
            while bo==True:
                #print(hex(dic2["$a0"]+4*ind))
                if a2-4*ind==0:
                    k1 = dic3[hex(dic2["$a1"]+4*ind)]
                    k11 = high_8(k1)
                    k12 = high_mid8(k1)
                    k13 = low_mid8(k1)
                    k14 = low_8(k1)
                    k11 = chr(k11)
                    k12 = chr(k12)
                    k13 = chr(k13)
                    k14 = chr(k14)
                    k111 = [k11,k12,k13,k14]
                    for i in range(len(k111)):
                        if k111[i] != "\0":
                            cont = cont + k111[i]
                        else:
                            cont = cont + k111[i]
                            bo = False
                    bo = False
                elif a2-4*ind==1:
                    k1 = dic3[hex(dic2["$a1"]+4*ind)]
                    k11 = high_8(k1)
                    k11 = chr(k11)
                    k111 = [k11]
                    for i in range(len(k111)):
                        if k111[i] != "\0":
                            cont = cont + k111[i]
                        else:
                            cont = cont + k111[i]
                            bo = False
                    bo = False
                elif a2-4*ind==2:
                    k1 = dic3[hex(dic2["$a1"]+4*ind)]
                    k11 = high_8(k1)
                    k12 = high_mid8(k1)
                    k11 = chr(k11)
                    k12 = chr(k12)
                    k111 = [k11,k12]
                    for i in range(len(k111)):
                        if k111[i] != "\0":
                            cont = cont + k111[i]
                        else:
                            cont = cont + k111[i]
                            bo = False
                    bo = False
                elif a2-4*ind==3:
                    k1 = dic3[hex(dic2["$a1"]+4*ind)]
                    k11 = high_8(k1)
                    k12 = high_mid8(k1)
                    k13 = low_mid8(k1)
                    k11 = chr(k11)
                    k12 = chr(k12)
                    k13 = chr(k13)
                    k111 = [k11,k12,k13]
                    for i in range(len(k111)):
                        if k111[i] != "\0":
                            cont = cont + k111[i]
                        else:
                            cont = cont + k111[i]
                            bo = False
                    bo = False
                elif a2-4*ind>=4:
                    k1 = dic3[hex(dic2["$a1"]+4*ind)]
                    k11 = high_8(k1)
                    k12 = high_mid8(k1)
                    k13 = low_mid8(k1)
                    k14 = low_8(k1)
                    k11 = chr(k11)
                    k12 = chr(k12)
                    k13 = chr(k13)
                    k14 = chr(k14)
                    k111 = [k11,k12,k13,k14]
                    for i in range(len(k111)):
                        if k111[i] != "\0":
                            cont = cont + k111[i]
                        else:
                            cont = cont + k111[i]
                            bo = False                 
                ind = ind + 1
            lee = len(cont)
            os.write(a0,cont.encode())
            dic2["$a0"] = lee
        elif dic2["$v0"]==16:
            a0 = eval(chr(dic2["$a0"]))
            os.close(a0)
        elif dic2["$v0"]==10 or 17:
                sys.exit()
                print("done")
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif fun=="100110"and op=="000000": #xor
        rs = mc[6:11]
        rt = mc[11:16]
        rd = mc[16:21]
        rs = dic1[rs]
        rt = dic1[rt]
        rd = dic1[rd]
        s = dic2[rs]
        t = dic2[rt]
        dic2[rd] = s^t
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="001000": #addi
        rs = mc[6:11]
        rt = mc[11:16]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        rs = dic1[rs]
        rt = dic1[rt]
        dic2[rt] = dic2[rs] + imm
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="001001": #addiu
        rs = mc[6:11]
        rt = mc[11:16]
        imm = mc[16:]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = int("0b"+imm,2)
        dic2[rt] = dic2[rs] + imm
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="001100": #andi
        rs = mc[6:11]
        rt = mc[11:16]
        imm = mc[16:]
        rs = dic1[rs]
        rt = dic1[rt]
        s = dic2[rs]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        dic2[rt] = s&imm
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
        print("__________________")
    elif op=="000100": #beq
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        if dic2[rs]==dic2[rt]:
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4+4*imm))
        else:
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="000001"and mc[11:16]=="00001": #bgez
        rs = mc[6:11]
        rs = dic1[rs]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        if dic2[rs]>=0:
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4+4*imm))
        else:
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="000111": #bgtz
        rs = mc[6:11]
        rs = dic1[rs]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        if dic2[rs]>0:
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4+4*imm))
        else:
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="000110": #blez
        rs = mc[6:11]
        rs = dic1[rs]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        if dic2[rs]<=0:
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4+4*imm))
        else:
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="000001"and mc[11:16]=="00000": #bltz
        rs = mc[6:11]
        rs = dic1[rs]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        if dic2[rs]<0:
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4+4*imm))
        else:
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="000101": #bne
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        if dic2[rs]!=dic2[rt]:
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4+4*imm))
        else:
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="100000": #lb
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        q = imm//4
        r = imm%4
        if imm>=0:
            p = dic3[str(hex(dic2[rs]+4*q))]
            #print("****************")
            #print(p)
            if r == 0:
                x = high_8(p)
                dic2[rt] = x
                #print(x)
            elif r==1 :
                x = high_mid8(p)
                dic2[rt] = x
            elif r==2:
                x = low_mid8(p)
                dic2[rt] = x
            elif r==3:
                x = low_8(p)
                dic2[rt] = x
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
        elif imm<0:
            if r == 0:
                p = dic3[str(hex(dic2[rs]+4*q))]
                x = high_8(p)
                dic2[rt] = x
            elif r==-3:
                p = dic3[str(hex(dic2[rs]+4*(q-1)))]
                x = high_mid8(p)
                dic2[rt] = x
            elif r==-2:
                p = dic3[str(hex(dic2[rs]+4*(q-1)))]
                x = low_mid8(p)
                dic2[rt] = x
            elif r==-1:
                p = dic3[str(hex(dic2[rs]+4*(q-1)))]
                x = low_8(p)
                dic2[rt] = x
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="100100": #lbu
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        q = imm//4
        r = imm%4
        if imm>=0:
            p = dic3[str(hex(dic2[rs]+4*q))]
            #print("****************")
            #print(p)
            if r == 0:
                x = high_8(p)
                dic2[rt] = x
                #print(x)
            elif r==1 :
                x = high_mid8(p)
                dic2[rt] = x
            elif r==2:
                x = low_mid8(p)
                dic2[rt] = x
            elif r==3:
                x = low_8(p)
                dic2[rt] = x
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
        elif imm<0:
            if r == 0:
                p = dic3[str(hex(dic2[rs]+4*q))]
                x = high_8(p)
                dic2[rt] = x
            elif r==-3:
                p = dic3[str(hex(dic2[rs]+4*(q-1)))]
                x = high_mid8(p)
                dic2[rt] = x
            elif r==-2:
                p = dic3[str(hex(dic2[rs]+4*(q-1)))]
                x = low_mid8(p)
                dic2[rt] = x
            elif r==-1:
                p = dic3[str(hex(dic2[rs]+4*(q-1)))]
                x = low_8(p)
                dic2[rt] = x
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="100001": #lh
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        #print(hex(dic2[rs]))
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        q = imm//4
        r = imm%4
        #print(q)
        #print("2222222222222222")
        if imm>=0:
            p = dic3[str(hex(dic2[rs]+4*q))]
            if r == 0:
                x = high_16(p)
                x = (low_mid8(x)) + (low_8(x)<<8)
                print("xxxxxxxxxxxxxxx")
                print(hex(x))
                dic2[rt] = x
            elif r==2:
                x = low_16(p)
                x = (low_mid8(x)) + (low_8(x)<<8)
                print("xxxxxxxxxxxxxxx")
                print(hex(x))
                dic2[rt] = x
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
        elif imm<0:
            if r == 0:
                p = dic3[str(hex(dic2[rs]+4*q))]
                x = high_16(p)
                x = (low_mid8(x)) + (low_8(x)<<8)
                dic2[rt] = x
            elif r==-2:
                p = dic3[str(hex(dic2[rs]+4*(q-1)))]
                x = low_16(p)
                x = (low_mid8(x)) + (low_8(x)<<8)
                dic2[rt] = x
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="100101": #lhu
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        #print(hex(dic2[rs]))
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        q = imm//4
        r = imm%4
        #print(q)
        #print("2222222222222222")
        if imm>=0:
            p = dic3[str(hex(dic2[rs]+4*q))]
            if r == 0:
                x = high_16(p)
                x = (low_mid8(x)) + (low_8(x))
                print("xxxxxxxxxxxxxxx")
                print(hex(x))
                dic2[rt] = x
            elif r==2:
                x = low_16(p)
                x = (low_mid8(x)) + (low_8(x))
                print("xxxxxxxxxxxxxxx")
                print(hex(x))
                dic2[rt] = x
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
        elif imm<0:
            if r == 0:
                p = dic3[str(hex(dic2[rs]+4*q))]
                x = high_16(p)
                x = (low_mid8(x)) + (low_8(x))
                dic2[rt] = x
            elif r==-2:
                p = dic3[str(hex(dic2[rs]+4*(q-1)))]
                x = low_16(p)
                x = (low_mid8(x)) + (low_8(x))
                dic2[rt] = x
            dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="001111": #lui
        rt = mc[11:16]
        imm = mc[21:]
        rt = dic1[rt]
        
        dic2[rt] = imm + 16*"0"
        if dic2[rt][0]=="1":
            dic2[rt] = sign_bin(dic2[rt])
            dic2[rt] = -int("0b"+dic2[rt],2)
        else:
            dic2[rt] = int("0b"+dic2[rt],2)
        #print(dic2[rt])
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="100011": #lw
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        p = dic3[str(hex(dic2[rs]+imm))]
        pk = (high_8(p)) + (high_mid8(p)<<8) + (low_mid8(p)<<16) +(low_8(p)<<24)
        #pk = high_8(p) + high_mid8(p) +low_mid8(p) + low_8(p)
        #print(chr(high_8(p)),chr(high_mid8(p)),chr(low_mid8(p)),chr(low_8(p)))
        #print(hex(pk))
        dic2[rt] = pk
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="001101": #ori
        rs = mc[6:11]
        rs = dic1[rs]
        rt = mc[11:16]
        rt = dic1[rt]
        d=""
        imm = mc[16:]
        imm = 16*"0"+imm
        s = dic2[rs]
        if s<0:
            s=-s
            s = bin(s)[2:].zfill(32)
            s = sign_bin(s)
        else:
            s = bin(s)[2:].zfill(32)
        #print(s)
        for i in range(len(s)):
            if s[i]=="1" or imm[i]=="1":
                d = d+"1"
            else:
                d = d+'0'
        #print(d)
        d = int("0b"+d,2)
        dic2[rt] = d
        #print(dic2[rt])
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="101000": #sb
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        q=(dic2[rs]+imm)//4
        r=(dic2[rs]+imm)%4
        if r==0:
            p = low_8(dic2[rt])
            dic3[str(hex(4*q))] = p<<24 
        elif r== 1:
            p = low_8(dic2[rt])
            dic3[str(hex(4*q))] = p<<16
        elif r== 2:
            p = low_8(dic2[rt])
            dic3[str(hex(4*q))] = p<<8
        elif r== 3:
            p = low_8(dic2[rt])
            dic3[str(hex(4*q))] = p
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="101001": #sh
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        q=(dic2[rs]+imm)//4
        r=(dic2[rs]+imm)%4
        if r==0:
            p = low_16(dic2[rt])
            dic3[str(hex(4*q))] = (low_8(p)<<24) + (low_mid8(p)<<16)
        elif r==2:
            p = low_16(dic2[rt])
            dic3[str(hex(4*q))] = (low_8(p)<<8) + (low_mid8(p))
        dic3[str(hex(dic2[rs]+4*q))] = p
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="101011": #sw
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        t = dic2[rt]
        #print(hex(t<<24))
        #print(hex(dic2[rs]+imm))
        pt = high_8(t) + (high_mid8(t)<<8) + (low_mid8(t)<<16) + (low_8(t)<<24)
        #print(chr(low_8(t)))
        #print(hex(pt))
        #print(hex(dic2[rs]+imm))
        dic3[str(hex(dic2[rs]+imm))]=pt
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="001010": #slti
        rs = mc[6:11]
        rt = mc[11:16]
        imm = mc[16:]
        rs = dic1[rs]
        rt = dic1[rt]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        if dic2[rs]<imm:
            dic2[rt]=1
        else:
            dic2[rt]=0
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="001011": #sltiu
        rs = mc[6:11]
        rt = mc[11:16]
        imm = mc[16:]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = int("0b"+imm,2)
        if dic2[rs]<imm:
            dic2[rt]=1
        else:
            dic2[rt]=0
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="001110": #xori
        rs = mc[6:11]
        rt = mc[11:16]
        imm = mc[16:]
        rs = dic1[rs]
        rt = dic1[rt]
        im = mc[16:].zfill(32)
        d=""
        if s<0:
            s=-s
            s = bin(s)[2:].zfill(32)
            s = sign_bin(s)
        else:
            s = bin(s)[2:].zfill(32)
        for i in range(len(s)):
            if s[i]==im[i]:
                d = d+"0"
            else:
                d = d+'1'
        d = int("0b"+d,2)
        dic2[rd] = d
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="100010":  #lwl
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        #p = dic3[str(hex(dic2[rs]+imm))]
        p = dic2[rs]+imm
        print(hex(p))
        q = p//4
        r = p%4
        if r == 0:
            pp2 = dic3[str(hex(4*q))]
            pk = (high_8(pp2)<<24) 
            dic2[rt] = pk + (high_mid8(dic2[rt])<<16) + (low_mid8(dic2[rt])<<8) + (low_8(dic2[rt]))
        elif r == 1:
            pp2 = dic3[str(hex(4*q))]
            pk = (high_8(pp2)<<16) + (high_mid8(pp2)<<24) 
            dic2[rt] = pk + (low_mid8(dic2[rt])<<8) + (low_8(dic2[rt]))
        elif r== 2:
            pp2 = dic3[str(hex(4*q))]
            pk = (high_8(pp2)<<8) + (high_mid8(pp2)<<16) + (low_mid8(pp2)<<24) 
            dic2[rt] = pk + (low_8(dic2[rt]))
        elif r== 3:
            #pp1 = dic3[str(hex(4*q-4))]
            pp2 = dic3[str(hex(4*q))]
            pk = (high_8(pp2)) + (high_mid8(pp2)<<8) + (low_mid8(pp2)<<16) + (low_8(pp2)<<24) 
            dic2[rt] = pk
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="100110": #lwr
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        #p = dic3[str(hex(dic2[rs]+imm))]
        p = dic2[rs]+imm
        q = p//4
        r = p%4
        print(r)
        if r == 0:
            pp = dic3[str(hex(4*q))]
            #print(hex(pp))
            pk = (high_8(pp)) + (high_mid8(pp)<<8) + (low_mid8(pp)<<16) + (low_8(pp)<<24) 
            dic2[rt] = pk
        elif r == 1:
            pp1 = dic3[str(hex(4*q))]
            #print(hex(4*q))
            #print(hex(pp))
            pk = (high_mid8(pp1)) + (low_mid8(pp1)<<8) + (low_8(pp1)<<16)
            #print(hex(pk))
            dic2[rt] = pk + (high_8(dic2[rt])<<24)
        elif r == 2:
            pp = dic3[str(hex(4*q))]
            pk =  low_mid8(pp)+(low_8(pp)<<8)
            dic2[rt] = pk+(high_8(dic2[rt])<<24)+(high_mid8(dic2[rt])<<16)
        elif r == 3:
            pp = dic3[str(hex(4*q))]
            pk =  low_8(pp)
            dic2[rt] = pk +(high_8(dic2[rt])<<24)+(high_mid8(dic2[rt])<<16) + (low_mid8(dic2[rt])<<8)
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op == "101010": #swl
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        t = dic2[rt]
        q = (dic2[rs]+imm)//4
        r = (dic2[rs]+imm)%4
        if r==0:
            pt = (high_8(t)<<24)  
            dic3[str(hex(4*q))]=pt + (high_mid8(dic3[str(hex(4*q))])<<16) +(low_mid8(dic3[str(hex(4*q))])<<8) +(low_8(dic3[str(hex(4*q))]))
        elif r==1:
            pt = (high_8(t)<<16) + (high_mid8(t)<<24)
            dic3[str(hex(4*q))]=pt+(low_mid8(dic3[str(hex(4*q))])<<8) +(low_8(dic3[str(hex(4*q))]))
            print(hex(dic3[str(hex(4*q))]))
        elif r==2:
            pt = (high_8(t)<<8) + (high_mid8(t)<<16) + (low_mid8(t)<<24) 
            dic3[str(hex(4*q))]=pt +(low_8(dic3[str(hex(4*q))]))
        elif r==3:
            pt = (high_8(t))+ (high_mid8(t)<<8) + (low_mid8(t)<<16)+(low_8(t)<<24) 
            dic3[str(hex(4*q))]=pt
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="101110": #swr
        rs = mc[6:11]
        rt = mc[11:16]
        rs = dic1[rs]
        rt = dic1[rt]
        imm = mc[16:]
        if imm[0]=="1":
            imm = sign_bin(imm)
            imm = -int("0b"+imm,2)
        else:
            imm = int("0b"+imm,2)
        t = dic2[rt]
        q = (dic2[rs]+imm)//4
        r = (dic2[rs]+imm)%4
        if r==0:
            pt = (high_8(t)) +(high_mid8(t)<<8)+(low_mid8(t)<<16) + (low_8(t)<<24) 
            dic3[str(hex(4*q))]=pt
        elif r==1:
            pt = (high_mid8(t))+(low_mid8(t)<<8) + (low_8(t)<<16)  
            dic3[str(hex(4*q))]=pt+ (high_8(dic3[str(hex(4*q))])<<24)
        elif r==2:
            pt = (low_mid8(t)) + (low_8(t)<<8)  
            dic3[str(hex(4*q))]=pt + (high_8(dic3[str(hex(4*q))])<<24) + (high_mid8(dic3[str(hex(4*q))])<<16)
            print(hex(dic3[str(hex(4*q))]))
        elif r==3:
            pt = (low_8(t))  
            dic3[str(hex(4*q))]=pt+ (high_8(dic3[str(hex(4*q))])<<24) + (high_mid8(dic3[str(hex(4*q))])<<16)+(low_mid8(dic3[str(hex(4*q))])<<8)
        dic2["PC"] = str(hex(int(dic2["PC"],16)+4))
    elif op=="000010": #j
        imm = mc[6:]
        rp = dic2["PC"]
        rp = int(rp,16)
        rp = bin(rp)[2:]
        rp = rp.zfill(32)
        dic2["PC"] = rp[:4]+imm+"00"
        dic2["PC"] = int("0b"+dic2["PC"],2)
        dic2["PC"] = str(hex(dic2["PC"]))
    elif op=="000011": #jal
        dic2["$ra"] = int((hex(int(dic2["PC"],16)+4)),16)
        imm = mc[6:]
        rp = dic2["PC"]
        #print(rp)
        rp = int(rp,16)
        rp = bin(rp)[2:]
        rp = rp.zfill(32)
        dic2["PC"] = rp[:4]+imm+"00"
        dic2["PC"] = int("0b"+dic2["PC"],2)
        dic2["PC"] = str(hex(dic2["PC"]))
        #print(dic2["PC"])
    return dic2
def write_binary_mc(fd,value):
    bin_data = int(value).to_bytes(length=4, byteorder='big', signed=False)
    fd.write(bin_data)

def write_binary(fd,value):
    bin_data = int(value).to_bytes(length=4, byteorder='big', signed=True)
    fd.write(bin_data)

def ex():
    global asm_file
    global in_file
    global txt_file
    global read_index
    global print_index
    global bre
    read_index = 0
    print_index =0 
    mem_dic = creat_mem()
    reg_dic=creat_reg_dic()
    reg_mem = reg_con()
    asm_file =asm #input("asm file name:")
    check_point_file =checkpts #input("checkpoints file name:")
    txt_file = txt #input("machine_code file name:")
    in_file = inputfi  #input(".in file name:")
    check_points_list = []
    with open (check_point_file,"r") as fil:
        li = fil.readlines()
        for i in range(0,len(li)):
            li[i] = li[i].replace('\n','')
            check_points_list.append(int(li[i]))
    #input_file = "fib" #"lwlr_swlr_2"   #"many"  #"memcpy-hello-world"
    no_comment(asm_file)
    mem_dic = read_mac_code(txt_file,mem_dic)
    mem_dic = read_asm_data("nocomment.txt",mem_dic)
    print(mem_dic)
    #print(mem_dic["0x400000"])
    #print(mem_dic["0x400004"])
    #打出memory的0x500000
    #kk = 5242880
    #while kk<5243408:
        #print(str(hex(kk)),":")
        #print(hex(mem_dic[str(hex(kk))]))
        #kk =kk+4
    ####
    os.remove("nocomment.txt")
    #运行程序
    jj=0
    while True:
        if jj in check_points_list:
            mem_di = copy.deepcopy(mem_dic)
            kl = 0x400000
            print("The memory is dumping..............")
            with open("memory_"+ str(jj) + ".bin","wb") as fi:
                #print(mem_dic)
                #mem_di = mem_dic
                jjj = 0x400000
                while jjj<=(0x500000-4):
                    a = mem_di[hex(jjj)]
                    if type(a) == str:
                        a1 = a[0:8]
                        a2 = a[8:16]
                        a3 = a[16:24]
                        a4 = a[24:32]
                        mem_di[hex(jjj)] = int("0b"+a4+a3+a2+a1,2)
                    jjj = jjj +4
                #print(mem_di)
                while kl<=(0xa00000-4):   
                    if mem_di[hex(kl)]>=0:             
                        write_binary_mc(fi,mem_di[hex(kl)])
                        kl = kl+4
                    else:
                        write_binary(fi,mem_di[hex(kl)])
                        kl = kl+4
            with open("register_"+ str(jj) + ".bin","wb") as fi:
                for key in reg_mem:
                    #print(key,":")
                    p = reg_mem[key]
                    if key == "PC":
                        p = int(p,16) 
                    p1 = low_8(p)<<24
                    p2 = low_mid8(p)<<16
                    p3 = high_mid8(p)<<8
                    p4 = high_8(p)
                    pall = p1+p2+p3+p4
                    if pall>=0:
                        write_binary_mc(fi,pall)
                    else:
                        write_binary(fi,pall)
        mc = mem_dic[reg_mem["PC"]]
        #print(mem_dic)
        #print(reg_mem)
        print("jj:",jj)
        print(reg_mem["PC"])
        print(reg_mem)
        print("-----------------------------")
        print("\n")
        reg_mem = operation(mc,reg_dic,reg_mem,mem_dic)
        jj=jj+1
ex()




