import gmpy2
from Crypto.Util.number import *
from binascii import a2b_hex,b2a_hex
import binascii

e = 65537

c = 28767758880940662779934612526152562406674613203406706867456395986985664083182
#1.将n分解为p和q
p = 189239861511125143212536989589123569301
q = 386123125371923651191219869811293586459
n = p*q

phi = (p-1)*(q-1)
#2.求d
d = gmpy2.invert(e,phi)
#3.m=pow(c,d,n)
m = gmpy2.powmod(c,d,n)
print(binascii.unhexlify(hex(m)[2:]))
#binascii.unhexlify(hexstr):从十六进制字符串hexstr返回二进制数据