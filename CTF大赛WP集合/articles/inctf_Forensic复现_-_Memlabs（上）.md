# inctf Forensic复现 | Memlabs（上）

> 原文: https://www.ctfiot.com/71847.html
> ID: 71847


```
a = "335d366f5d6031767631707f".decode("hex")
for i in range(0,255):
 b = ""
 for j in a:
 b = b + chr(ord(j) ^ i)
 print b
```



```
┌──(root㉿SanDieg0)-[/mnt/d/volatility_2.6_win64_standalone]
└─# ./volatility.exe -f "F:\Memlabs\lab1\Lab1.raw" --profile=Win7SP1x64 hashdump
Volatility Foundation Volatility Framework 2.6
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SmartNet:1001:aad3b435b51404eeaad3b435b51404ee:4943abb39473a6f32c11301f4987e7e0:::
HomeGroupUser$:1002:aad3b435b51404eeaad3b435b51404ee:f0fc3d257814e08fea06e63c5762ebd5:::
Alissa Simpson:1003:aad3b435b51404eeaad3b435b51404ee:f4ff64c8baac57d22f22edc681055ba6:::
```



```
┌──(root㉿SanDieg0)-[/mnt/d/volatility-master]
└─# python2 vol.py --plugins=./volatility/plugins/ -f "/mnt/f/Memlabs/lab2/Lab2.raw" --profile=Win7SP1x64 chromehistory
```



```
sudo apt install steghide
```



```
import sys
import string

def xor(s):

 a = ''.join(chr(ord(i)^3) for i in s)
 return a

def encoder(x):

 return x.encode("base64")

if __name__ == "__main__":

 f = open("C:\\Users\\hello\\Desktop\\vip.txt", "w")

 arr = sys.argv[1]

 arr = encoder(xor(arr))

 f.write(arr)

 f.close()
```



```
s = 'am1gd2V4M20wXGs3b2U='
d = s.decode('base64')
a = ''.join(chr(ord(i)^3) for i in d)

print a
```
