from LabelTable import address,jtl,itl,branch_table
from phase1 import dc, no_comment
import os

R = ['add','addu','and','div','divu','jalr','jr','mfhi','mflo','mthi','mtlo','mult',
     'multu','nor','or','sll','sllv','slt','sltu','sra','srav','srl','srlv','sub',
      'subu','syscall','xor']
I = ['addi','addiu','andi','beq','bgez','bgtz','blez','bltz','bne','lb','lbu','lh',
     'lhu','lui','lw','ori','sb','slti','sltiu','sh','sw','xori','lwl','lwr','swl',
     'swr']
J = ['j','jal']

reg = {'$zero':'00000','$at':'00001','$v0':'00010','$v1':'00011','$a0':'00100',
        '$a1':'00101','$a2':'00110','$a3':'00111','$t0':'01000','$t1':'01001',
        '$t2':'01010','$t3':'01011','$t4':'01100','$t5':'01101','$t6':'01110',
        '$t7':'01111','$s0':'10000','$s1':'10001','$s2':'10010','$s3':'10011',
        '$s4':'10100','$s5':'10101','$s6':'10110','$s7':'10111','$t8':'11000',
        '$t9':'11001','$k0':'11010','$k1':'11011','$gp':'11100','$sp':'11101',
        '$fp':'11110','$ra':'11111'}



def addBinary(a,b = 1):
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


 #针对二进制的操作
def sign_bin(i):
    i = str(i)
    t =[]
    for j in range(0,len(i)):
        if i[j]=="0":
            t.append("1")
        elif i[j]=="1":
            t.append("0")
    i = ''.join(t)
    i = addBinary(i)
    return i

def sp_ad(i):
    con = False
    re = ''
    im = ''
    for j in range(0,len(i)-1):
        if con == True:
            re = re + i[j]
        elif con == False and i[j] != "(":
            im = im + i[j]
        if i[j] == "(":
            con = True
    re.strip()
    im.strip()
    return re,eval(im)




def r(si,vl):
    op = '000000'
    if si=='add':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rs = reg.get(vll[1])
        rt = reg.get(vll[2])
        return op+rs+rt+rd+'00000'+'100000'
    elif si=='addu':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rs = reg.get(vll[1])
        rt = reg.get(vll[2])
        return op+rs+rt+rd+'00000'+'100001'
    elif si=='and':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rs = reg.get(vll[1])
        rt = reg.get(vll[2])
        return op+rs+rt+rd+'00000'+'100100'
    elif si=='div':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rs = reg.get(vll[0])
        rt = reg.get(vll[1])
        return op+rs+rt+'00000'+'00000'+'011010'
    elif si=='divu':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rs = reg.get(vll[0])
        rt = reg.get(vll[1])
        return op+rs+rt+'00000'+'00000'+'011011'
    elif si=='jalr':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rs = reg.get(vll[1])
        return op+rs+'00000'+rd+'00000'+'001001'
    elif si=='jr':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rs = reg.get(vll[0])
        return op+rs+'00000'+'00000'+'00000'+'001000'
    elif si=='mfhi':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        return op+'00000'+'00000'+rd+'00000'+'010000'
    elif si=='mflo':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        return op+'00000'+'00000'+rd+'00000'+'010010'
    elif si=='mthi':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rs = reg.get(vll[0])
        return op+rs+'00000'+'00000'+'00000'+'010001'
    elif si=='mtlo':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rs = reg.get(vll[0])
        return op+rs+'00000'+'00000'+'00000'+'010011'
    elif si=='mult':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rs = reg.get(vll[0])
        rt = reg.get(vll[1])
        return op+rs+rt+'00000'+'00000'+'011000'
    elif si=='multu':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rs = reg.get(vll[0])
        rt = reg.get(vll[1])
        return op+rs+rt+'00000'+'00000'+'011001'
    elif si=='nor':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rs = reg.get(vll[1])
        rt = reg.get(vll[2])
        return op+rs+rt+rd+'00000'+'100111'
    elif si=='or':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rs = reg.get(vll[1])
        rt = reg.get(vll[2])
        return op+rs+rt+rd+'00000'+'100101'
    elif si=='sll':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rt = reg.get(vll[1])
        sa = reg.get(vll[2])
        return op+'00000'+rt+rd+sa+'000000'
    elif si=='sllv':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rt = reg.get(vll[1])
        rs = reg.get(vll[2])
        return op+rs+rt+rd+'00000'+'000100'
    elif si=='slt':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rs = reg.get(vll[1])
        rt = reg.get(vll[2])
        return op+rs+rt+rd+'00000'+'101010'
    elif si=='sltu':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rs = reg.get(vll[1])
        rt = reg.get(vll[2])
        return op+rs+rt+rd+'00000'+'101011'
    elif si=='sra':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rt = reg.get(vll[1])
        sa = reg.get(vll[2])
        return op+'00000'+rt+rd+sa+'000011'
    elif si=='srav':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rt = reg.get(vll[1])
        rs = reg.get(vll[2])
        return op+rs+rt+rd+'00000'+'000111'
    elif si=='srl':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rt = reg.get(vll[1])
        sa = reg.get(vll[2])
        return op+'00000'+rt+rd+sa+'000010'
    elif si=='srlv':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rt = reg.get(vll[1])
        rs = reg.get(vll[2])
        return op+rs+rt+rd+'00000'+'000110'
    elif si=='sub':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rs = reg.get(vll[1])
        rt = reg.get(vll[2])
        return op+rs+rt+rd+'00000'+'100010'
    elif si=='subu':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rs = reg.get(vll[1])
        rt = reg.get(vll[2])
        return op+rs+rt+rd+'00000'+'100011'
    elif si=='sub':
        return op+'00000'+'00000'+'00000'+'00000'+'001100'
    elif si=='xor':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rd = reg.get(vll[0])
        rs = reg.get(vll[1])
        rt = reg.get(vll[2])
        return op+rs+rt+rd+'00000'+'100110'
def Ii(l1,l2,c,si,vl):
    if si=='addi':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        rs = reg.get(vll[1])
        imm = eval(vll[2])
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            imm = sign_bin(imm)
        return '001000'+rs+rt+imm
    elif si=='addiu':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        rs = reg.get(vll[1])
        imm = eval(vll[2])
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            imm = sign_bin(imm)
        return '001001'+rs+rt+imm
    elif si=='andi':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        rs = reg.get(vll[1])
        imm = eval(vll[2])
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            imm = sign_bin(imm)
        return '001100'+rs+rt+imm
    elif si=='beq':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        rs = reg.get(vll[1])
        lab = vll[2]
        kk = l1.index(lab)
        jj = l2[kk]
        jj=int(jj)
        if g>jj:
            qq = -g+jj-1
        elif g<jj:
            qq=jj-g-1
        if qq >=0:
            qq = bin(qq)[2:].zfill(16)
        elif qq <0:
            qq = -qq
            qq = bin(qq)[2:].zfill(16)
            #print(imm)
            qq = sign_bin(qq)
        lab = qq
        return '000100'+rt+rs+lab
    elif si=='bgez':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rs = reg.get(vll[0])
        lab = vll[1]
        kk = l1.index(lab)
        jj = l2[kk]
        jj=int(jj)
        if g>jj:
            qq = -g+jj-1
        elif g<jj:
            qq=jj-g-1
        if qq >=0:
            qq = bin(qq)[2:].zfill(16)
        elif qq <0:
            qq = -qq
            qq = bin(qq)[2:].zfill(16)
            #print(imm)
            qq = sign_bin(qq)
        lab = qq
        return '000001'+rs+'00001'+lab
    elif si=='bgtz':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rs = reg.get(vll[0])
        lab = vll[1]
        kk = l1.index(lab)
        jj = l2[kk]
        jj=int(jj)
        if g>jj:
            qq = -g+jj-1
        elif g<jj:
            qq=jj-g-1
        if qq >=0:
            qq = bin(qq)[2:].zfill(16)
        elif qq <0:
            qq = -qq
            qq = bin(qq)[2:].zfill(16)
            #print(imm)
            qq = sign_bin(qq)
        lab = qq
        return '000111'+rs+'00000'+lab
    elif si=='blez':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        #print(vll)
        rs = reg.get(vll[0])
        lab = vll[1]
        kk = l1.index(lab)
        jj = l2[kk]
        jj=int(jj)
        if g>jj:
            qq = -g+jj-1
        elif g<jj:
            qq=jj-g-1
        if qq >=0:
            qq = bin(qq)[2:].zfill(16)
        elif qq <0:
            qq = -qq
            qq = bin(qq)[2:].zfill(16)
            #print(imm)
            qq = sign_bin(qq)
        lab = qq
        return '000110'+rs+'00000'+lab
    elif si=='bltz':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rs = reg.get(vll[0])
        lab = vll[1]
        kk = l1.index(lab)
        jj = l2[kk]
        jj=int(jj)
        if g>jj:
            qq = -g+jj-1
        elif g<jj:
            qq=jj-g-1
        if qq >=0:
            qq = bin(qq)[2:].zfill(16)
        elif qq <0:
            qq = -qq
            qq = bin(qq)[2:].zfill(16)
            #print(imm)
            qq = sign_bin(qq)
        lab = qq
        return '000001'+rs+'00000'+lab
    elif si=='bne':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rs = reg.get(vll[0])
        rt = reg.get(vll[1])
        lab = vll[2]
        kk = l1.index(lab)
        jj = l2[kk]
        jj=int(jj)
        if g>jj:
            qq = -g+jj-1
        elif g<jj:
            qq=jj-g-1
        if qq >=0:
            qq = bin(qq)[2:].zfill(16)
        elif qq <0:
            qq = -qq
            qq = bin(qq)[2:].zfill(16)
            #print(imm)
            qq = sign_bin(qq)
        lab = qq
        return '000101'+rs+rt+lab
    elif si=='lb':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        r = vll[1]
        rs,imm = sp_ad(r)
        rs = reg.get(rs)
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            #print(imm)
            imm = sign_bin(imm)
            #print(imm)
        return '100000'+rs+rt+imm
    elif si=='lbu':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        r = vll[1]
        rs,imm = sp_ad(r)
        rs = reg.get(rs)
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            #print(imm)
            imm = sign_bin(imm)
            #print(imm)
        return '100100'+rs+rt+imm
    elif si=='lh':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        r = vll[1]
        rs,imm = sp_ad(r)
        rs = reg.get(rs)
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            #print(imm)
            imm = sign_bin(imm)
            #print(imm)
        return '100001'+rs+rt+imm
    elif si=='lhu':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        r = vll[1]
        rs,imm = sp_ad(r)
        rs = reg.get(rs)
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            #print(imm)
            imm = sign_bin(imm)
            #print(imm)
        return '100101'+rs+rt+imm
    elif si=='lui':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        imm = eval(vll[1])
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            imm = sign_bin(imm)
        return '001111'+'00000'+rt+imm
    elif si=='lw':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        r = vll[1]
        rs,imm = sp_ad(r)
        rs = reg.get(rs)
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            #print(imm)
            imm = sign_bin(imm)
            #print(imm)
        return '100011'+rs+rt+imm
    elif si=='ori':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        rs = reg.get(vll[1])
        imm = eval(vll[2])
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            imm = sign_bin(imm)
        return '001101'+rs+rt+imm
    elif si=='sb':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        r = vll[1]
        rs,imm = sp_ad(r)
        rs = reg.get(rs)
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            #print(imm)
            imm = sign_bin(imm)
            #print(imm)
        return '101000'+rs+rt+imm
    elif si=='slti':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        rs = reg.get(vll[1])
        imm = eval(vll[2])
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            imm = sign_bin(imm)
        return '001010'+rs+rt+imm
    elif si=='sltiu':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        rs = reg.get(vll[1])
        imm = eval(vll[2])
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            imm = sign_bin(imm)
        return '001011'+rs+rt+imm
    elif si=='sh':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        r = vll[1]
        rs,imm = sp_ad(r)
        rs = reg.get(rs)
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            #print(imm)
            imm = sign_bin(imm)
            #print(imm)
        return '101001'+rs+rt+imm
    elif si=='sw':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        r = vll[1]
        rs,imm = sp_ad(r)
        rs = reg.get(rs)
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            #print(imm)
            imm = sign_bin(imm)
            #print(imm)
        return '101011'+rs+rt+imm
    elif si=='xori':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        rs = reg.get(vll[1])
        imm = eval(vll[2])
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            imm = sign_bin(imm)
        return '001110'+rs+rt+imm
    elif si=='lwl':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        r = vll[1]
        rs,imm = sp_ad(r)
        rs = reg.get(rs)
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            #print(imm)
            imm = sign_bin(imm)
            #print(imm)
        return '100010'+rs+rt+imm
    elif si=='lwr':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        r = vll[1]
        rs,imm = sp_ad(r)
        rs = reg.get(rs)
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            #print(imm)
            imm = sign_bin(imm)
            #print(imm)
        return '100110'+rs+rt+imm
    elif si=='swl':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        r = vll[1]
        rs,imm = sp_ad(r)
        rs = reg.get(rs)
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            #print(imm)
            imm = sign_bin(imm)
            #print(imm)
        return '101010'+rs+rt+imm
    elif si=='swr':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        rt = reg.get(vll[0])
        r = vll[1]
        rs,imm = sp_ad(r)
        rs = reg.get(rs)
        if imm >=0:
            imm = bin(imm)[2:].zfill(16)
        elif imm <0:
            imm = -imm
            imm = bin(imm)[2:].zfill(16)
            #print(imm)
            imm = sign_bin(imm)
            #print(imm)
        return '101110'+rs+rt+imm
def j(si,vl):
    if si=='j':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        lab = jtl(my_dic.get(vll[0]))
        return '000010' + lab
    elif si=='jal':
        vl=vl.replace(si,' ')
        vl=vl.lstrip()
        vll=vl.split(',')
        #print(vll)
        for i in range(0,len(vll)):
            vll[i]=vll[i].strip()
        lab = jtl(my_dic.get(vll[0]))
        return '000011' + lab



def ex(my_file):
    global my_dic
    global g
    my_file = no_comment(my_file)
    my_dic = address(my_file)
    #print(my_dic)
    valid_line=[]
    finnal_result = []
    fi_ob_lines = []
    la_na,la_po,valid_line = branch_table(my_file)
    for g in range(0,len(valid_line)):
        specific_instruction = valid_line[g].lstrip().lstrip('\t').split(' ')[0]
        if specific_instruction in R:
            finnal_result.append(r(specific_instruction,valid_line[g].lstrip().lstrip('\t')))
        elif specific_instruction in I:
            finnal_result.append(Ii(la_na,la_po,g,specific_instruction,valid_line[g].lstrip().lstrip('\t')))
        elif specific_instruction in J:
            finnal_result.append(j(specific_instruction,valid_line[g].lstrip().lstrip('\t')))
    if os.path.exists("nocomment.txt"):
        os.remove("nocomment.txt")
    if os.path.exists("tee.txt"):
        os.remove("tee.txt")
    with open ('output.txt', 'w') as f:
        for i in range(len(finnal_result)):
            f.write(finnal_result[i])     
