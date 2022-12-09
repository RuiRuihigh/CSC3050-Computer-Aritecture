from datetime import date


#def low_16(x):
 #   return x & ((1<<16)-1)
#print(bin(low_16(0b11111111111111111111111111111111111111111111110)))
#print(bin((1<<16)-1))

def high_8(x):
    a = (1<<8)-1
    b = a<<24
    c = x&b
    d = c>>24
    return d

def high_mid8(x):
    a = (1<<8)-1
    b = a<<16
    c = x&b
    d = c>>16
    return d

def low_mid8(x):
    a = (1<<8)-1
    b = a<<8
    c = x&b
    d = c>>8
    return d
def low_8(x):
    a = (1<<8)-1
    c = x&a
    return c

def low_16(x):
    return x & ((1<<16)-1)

def high_16(x):
    a = (1<<16)-1
    b = a<<16
    c = x&b
    d = c>>16
    return d










