# 一道简单Chacha20_RC4算法CTF题目

> 原文: https://www.ctfiot.com/89178.html
> ID: 89178

本道逆向题涉及的知识点如下：

反调试

花指令

chacha20加密

rc4加密

这是今年12月份帮一朋友做的一道CTF题，看题目描述是某春秋平台的，做这道题也花了2小时，因为以前没遇到过chacha20加密，做题的时在论坛也没有搜到chacha20算法，故而写一篇文章记录一下，供大家参考。

首先我们观察下这道题目，解压后如下，看样子加密后的flag就在flag.enc中：

按照做题惯例，先查个壳，发现就是普通的32位程序，使用VC++编译器编译，没壳：

我们直接拖到IDA中进行静态分析。

进去之后，没什么好说的，直接找main函数按F5开始分析整个程序逻辑；我们先大略的分析一下，见下图注释，函数名都还没有修改，都是IDA自动生成的。

如上注释，通过初步的分析，我们大致了解到，整个程序就是将flag读入，然后经过中间一系列未识别到的函数，最后把文件改名为flag.enc并将加密后的内容覆盖输出到flag.enc。要注意在上图的第23行有一个全局变量的字节序列，这个序列是在函数sub_401610生成的，这里的内容我们最后再分析，接下来先分析最主要的中间那三个函数。

我们看到在22行，有一个名为loc_401450的函数，我们点进去看看为什么该函数没有被IDA正确识别，如下图：

点进去之后，发现左边的地址部分一片红，有经验的逆向人员一看0x401468~0x40146C这部分，就是明显的花指令特征，在地址0x40146A处的跳转无论如何都会跳转到0x40146F处，使得IDA未能识别这种跳转破坏了函数的栈帧，因此IDA没有将该部分正确识别为函数。

看过我另一篇文章的大家应该清楚花指令的还原，也可以用脚本，但是这里的花指令不多，故而我们直接手动来快速还原。将光标定位在地址0x40146E，然后直接按键盘上的D，即可将该部分转换为数据。

弹出如下框，这是在IDA在质问我们人类智慧的一个警告，直接Yes就可以。

然后在正确的代码地址0x40146F处按C键，使得该处的数据转变为正确的代码。

此外，由于0x40146A~0x40146E都是人工添加的无用代码，我们可以直接将该部分数据全部转为空指令nop，即0x90，如下图：

将这5个无用的字节替换为0x90，然后点OK。

至此，上述去花操作完成。

然后，我们选中整个函数的部分0x401450~0x401566，然后按快捷键P，让整个函数能被IDA正确识别。此时我们再次回到main函数的伪代码窗口，看到该部分函数已经被正确识别了，如下图：

剩下的loc_401940和loc_401AA0处的函数还原，和上述处理方法相同，需要注意的是函数的结尾一般是以retn结束。

接下来我们双击点进去sub_401450，开始分析该函数的算法，进去之后也是一脸茫然，看不明白；

继续点进去sub_401380函数看看，我们发现其中有这样一个字符串expand 32-byte k，如下图：

经过一番搜索，才知道这个加密函数是chacha20加密，找到了这个算法的C代码实现，https://github.com/shiffthq/chacha20，算法大致先进行初始化，矩阵置换，然后再是轮函数，最后生成了密钥流，以下是被调用加/解密函数接口：

void ChaCha20XOR(uint8_t key[32], uint32_t counter, uint8_t nonce[12], uint8_t *in, uint8_t *out, int inlen) { int i, j; uint32_t s[16]; uint8_t block[64]; //static void chacha20_init_state(uint32_t s[16], uint8_t key[32], uint32_t counter, uint8_t nonce[12]) chacha20_init_state(s, key, counter, nonce); for (i = 0; i < inlen; i += 64) { //static void chacha20_block(uint32_t in[16], uint8_t out[64], int num_rounds) chacha20_block(s, block, 20); s[12]++; for (j = i; j < i + 64; j++) { if (j >= inlen) { break; } out[j] = in[j] ^ block[j - i]; } }}

经过对比，我们发现这个函数就是chacha20的加解密算法，对比我们找到的源码，把这个算法拿过来稍微改改，只要把原来函数的in[j]参数直接换作是out[j]即可和题目一样，该参数既当作输入又当作输出。

注：我们使用的话，将github源码下载下来，把cpp和h文件导入即可；ChaCha20是一种流密码，可以将其理解为对称加密算法。

然后剩下的两个函数，如果有一定逆向题目积累的话，就不难猜测出这是RC4流密码。该算法先是对S盒的一个初始化，然后进行加解密操作，对该密码算法的详情可参考文末附带的链接。

加解密算法分析完了，接下来我们呼应一下本题的题目名称Random，看看前边遗留的sub_401610()函数，该函数生成了一个加密密钥，如下图：

我们发现这是一个伪随机生成的，关键是要知道其伪随机生成的种子Seed，v0是根据当前时间的时间戳生成的，所以本题的一个坑点应该是在这里，当前的进程ID我可以猜测他的区间为1~9000。

做题的时候，刚开始我以为时间戳就是flag.enc文件的时间戳，后来发现怎么都出不来，于是从题目的出题时间开始算起（也就是‎ 2022‎年‎9‎月‎11‎日，‏‎23:22:02），写了一个爆破，由于流密码的速度非常快，所以我很快就爆破出来了。

根据以上分析，我们写出其主要的wp代码，完整wp代码我放在了文末的附件，大家打开就能运行。

void get_flag(unsigned char* mykey, int v0, int pid){ unsigned char s[256] = { 0 }; unsigned char key[12] = "Encrypted!!"; char hexData[48] = { 0xFC, 0xD4, 0x19, 0x74, 0x51, 0x67, 0xED, 0x4B, 0x9C, 0x48, 0xC6, 0x5F, 0x9B, 0x5D, 0xB4, 0xF0, 0x44, 0x02, 0xAF, 0xAC, 0x66, 0x01, 0x06, 0xA5, 0xBE, 0xBC, 0xD0, 0x77, 0x29, 0x64, 0x8D, 0x5E, 0x41, 0xD4, 0x77, 0x31, 0x40, 0xB4, 0x92, 0x22, 0xF9, 0x9F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 }; //flag.enc字节序列 int enc_len = strlen(hexData); rc4_init(s, key, strlen((const char *)key)); rc4_crypt(s, (uint8_t *)hexData, enc_len); ChaCha20XOR((uint8_t *)mykey, 1, key, (uint8_t *)hexData, strlen(hexData)); if (hexData[0] == 'f' && hexData[1] == 'l' && hexData[2] == 'a') { //判定前三个字母是fla输出即可 printf("timestamp:%d,pid:%d ", v0, pid); for (int i = 0; i < 48; i++){ printf("%c", hexData[i]); } printf("n"); exit(0); }} int main() { unsigned char mykey[32]; int timestamp; DWORD Seed; timestamp = 1662973302; // time(0); 2022-09-12 17:01:42 for (int pid = 1; pid < 9000; pid++){ for (timestamp = 1662909722; timestamp <= 1662973302; timestamp++) { //最坑的点在这里，时间戳要从出题时间点开始算起 Seed = timestamp ^ pid; srand(Seed); for (int i = 0; i < 32; ++i) mykey[i] = (unsigned __int16)rand() >> 8; get_flag(mykey, timestamp, pid); //传入timestamp和pid纯属好奇 } } printf("endn"); return 0;}

解得flag

为了防止该题目再次出现，flag我就不以文本形式展现了。

另外本文中对另外一个反调试的函数没有进行过多分析，这类文章很多，大家搜一下就知道了，绕过方式也很简单。因为本题目的难度还没有用到动态分析。此外，虽是一道CTF题目，但是其中包含的反调试、ChaCha20、RC4流密码、花指令以及函数的识别，也值得我们多多去学习。

看雪ID：newu

https://bbs.pediy.com/user-home-592531.htm

*本文由看雪论坛 newu 原创，转载请注明来自看雪社区

# 往期推荐

1.CVE-2022-21882提权漏洞学习笔记

2.wibu证书 – 初探

3.win10 1909逆向之APIC中断和实验

4.EMET下EAF机制分析以及模拟实现

5.sql注入学习分享

6.V8 Array.prototype.concat函数出现过的issues和他们的POC们

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
void ChaCha20XOR(uint8_t key[32], uint32_t counter, uint8_t nonce[12], uint8_t *in, uint8_t *out, int inlen) { int i, j; uint32_t s[16]; uint8_t block[64]; //static void chacha20_init_state(uint32_t s[16], uint8_t key[32], uint32_t counter, uint8_t nonce[12]) chacha20_init_state(s, key, counter, nonce); for (i = 0; i < inlen; i += 64) { //static void chacha20_block(uint32_t in[16], uint8_t out[64], int num_rounds) chacha20_block(s, block, 20); s[12]++; for (j = i; j < i + 64; j++) { if (j >= inlen) { break; } out[j] = in[j] ^ block[j - i]; } }}
void get_flag(unsigned char* mykey, int v0, int pid){ unsigned char s[256] = { 0 }; unsigned char key[12] = "Encrypted!!"; char hexData[48] = { 0xFC, 0xD4, 0x19, 0x74, 0x51, 0x67, 0xED, 0x4B, 0x9C, 0x48, 0xC6, 0x5F, 0x9B, 0x5D, 0xB4, 0xF0, 0x44, 0x02, 0xAF, 0xAC, 0x66, 0x01, 0x06, 0xA5, 0xBE, 0xBC, 0xD0, 0x77, 0x29, 0x64, 0x8D, 0x5E, 0x41, 0xD4, 0x77, 0x31, 0x40, 0xB4, 0x92, 0x22, 0xF9, 0x9F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 }; //flag.enc字节序列 int enc_len = strlen(hexData); rc4_init(s, key, strlen((const char *)key)); rc4_crypt(s, (uint8_t *)hexData, enc_len); ChaCha20XOR((uint8_t *)mykey, 1, key, (uint8_t *)hexData, strlen(hexData)); if (hexData[0] == 'f' && hexData[1] == 'l' && hexData[2] == 'a') { //判定前三个字母是fla输出即可 printf("timestamp:%d,pid:%d ", v0, pid); for (int i = 0; i < 48; i++){ printf("%c", hexData[i]); } printf("n"); exit(0); }} int main() { unsigned char mykey[32]; int timestamp; DWORD Seed; timestamp = 1662973302; // time(0); 2022-09-12 17:01:42 for (int pid = 1; pid < 9000; pid++){ for (timestamp = 1662909722; timestamp <= 1662973302; timestamp++) { //最坑的点在这里，时间戳要从出题时间点开始算起 Seed = timestamp ^ pid; srand(Seed); for (int i = 0; i < 32; ++i) mykey[i] = (unsigned __int16)rand() >> 8; get_flag(mykey, timestamp, pid); //传入timestamp和pid纯属好奇 } } printf("endn"); return 0;}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/1-1672413387.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/9-1672413387.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/9-1672413388.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1672413389.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/4-1672413392.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/4-1672413394.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/0-1672413395.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/3-1672413395.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/0-1672413397.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1672413399.png)