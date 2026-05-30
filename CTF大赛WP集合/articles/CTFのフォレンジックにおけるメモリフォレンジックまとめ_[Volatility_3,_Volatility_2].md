# CTFのフォレンジックにおけるメモリフォレンジックまとめ [Volatility 3, Volatility 2]

> 原文: https://www.ctfiot.com/165189.html
> ID: 165189

竞技编程代码示例补充资料 竞技编程练习题合集 Twitter 竞技安全总结

親記事 → CTFにおけるフォレンジック入門とまとめ – はまやんはまやんはまやん

父文章→CTF中取证介绍及总结-Hamayan Hamayan Hamayan

メモリフォレンジック 记忆取证

メモリダンプが与えられて解析をする問題 给出并分析内存转储的问题。

Volatility Foundation  波动性基础

メモリダンプ解析のスタンダード。これ以外で解析している記事を見たことが無い。（Redlineとか昔はあったぽいが）

内存转储分析的标准。除此之外，我还没有看到任何分析任何内容的文章。 （我认为曾经有类似红线的东西）

Volatility2（無印）とVolatility3があるが、全くの別物。今から学習を始めるなら、絶対にVolatility 3から始めること

有 Volatility2（无品牌）和 Volatility3，但它们完全不同。如果你现在想开始学习，一定要从 Volatility 3 开始。

コマンド実行は結構時間かかるので、プロファイルの特定までは手動でやって、コマンド実行についてはよく使うコマンドを適当なシェルスクリプトで一括で持ってくるといい（その間にご飯）

执行命令需要相当长的时间，因此最好手动指定配置文件，并使用适当的 shell 脚本一次性导入常用命令（并同时执行）来执行命令。

Volatility使わなくてもバイナリ解析でやるようなことをやれば時間はかかるけど、使える情報が抜ける可能性は大いにある

即使您不使用波动性，也将花费更多时间来执行二进制分析所需的操作，但您很有可能获得有用的信息。

例えばFile Carvingを使ってファイルを抜き出したり、stringsでそこそこ有益な情報が得られたりもする

例如，您可以使用文件雕刻来提取文件，并使用字符串来获取一些有用的信息。

解く流れ 求解流程

メモリダンプがどのOSのものかを特定する  识别内存转储属于哪个操作系统

volatilityの解析機能ですぐに特定できるかも

使用波动率分析功能也许可以快速识别它。

できなければ、strings -n 10 mem.bin | grep "ubuntu"みたいに根性で種類とビルドバージョン（カーネルバージョン）を特定する

如果不能，请勇敢地确定类型和构建版本（内核版本），例如 strings -n 10 mem.bin | grep "ubuntu"

シンボルテーブルがなければ作る（メモリのどこに何があるかをまとめたもの…だと思っているが）

如果您没有符号表，请创建一个（我认为它是内存中内容的摘要……）

なければ作るしかないが、想像よりも大変ではない 如果你没有，你就必须制作一个，但这并不像你想象的那么困难。

頑張って解析する  尽力去分析

これは頑張る。メモリ解析は時間がかかるのでよく使うコマンドをシェルスクリプトにまとめて一括実行するのがおすすめ

这件事我会尽力的。内存分析需要时间，因此建议将常用命令编译成shell脚本并一次性执行。

Volatility 3（ちょっと情報薄い。ドキュメント見るといい）

波动性 3（一点点信息。查看文档）

https://qiita.com/ninja400/items/f3dd1e6eb80fd5b39ba9

windows  视窗

python3 /opt/volatility3/vol.py -f image.raw windows.info.Info WindowsInfoが読み取れる

python3 /opt/volatility3/vol.py -f image.raw windows.info.Info 可以读取 WindowsInfo

NTBuildLab 7601.17514.amd64fre.win7sp1_rtm. -> win7sp1が入ってる

NTBuildLab 7601.17514.amd64fre.win7sp1_rtm. -> 包含 win7sp1

Is64Bit True -> 64bits  Is64Bit True -> 64 位

python3 /opt/volatility3/vol.py -f image.raw windows.pstree.PsTree プロセスツリーが見られる   python3 /opt/volatility3/vol.py -f image.raw windows.pstree.PsTree 可以看到进程树

cmd.exeが実行されているなら、コマンド系を深堀りしてみる

如果 cmd.exe 正在运行，请尝试深入研究命令系统。

python3 /opt/volatility3/vol.py -f image.raw windows.netscan.NetScan ネットワークコネクションが見られる

python3 /opt/volatility3/vol.py -f image.raw windows.netscan.NetScan 您可以看到网络连接

怪しいIPを見つけたらVirusTotalで確認

如果您发现可疑 IP，请使用 VirusTotal 进行检查

python vol.py -f image.raw windows.cmdline.CmdLine 現在実行中のプロセスがどのような引数で実行されたかが見られる

python vol.py -f image.raw windows.cmdline.CmdLine 您可以查看当前正在运行的进程使用哪些参数执行。

python vol.py -f image.raw windows.dumpfiles --pid="1676" メモリ上にあるpidが1676の関連ファイルをdumpしてくれる

python vol.py -f image.raw windows.dumpfiles --pid="1676" 转储内存中pid为1676的相关文件

python vol.py -f image.raw windows.mutantscan.MutantScan 使用されているミューテックスを出力する

python vol.py -f image.raw windows.mutantscan.MutantScan 输出使用的互斥体

通常、悪意のあるプログラムの作成者は、そのプログラムが二重起動するを避けるためミューテックスを使用する

恶意程序的作者通常使用互斥体来防止其程序启动两次。

python3 /opt/volatility3/vol.py -f image.raw windows.filescan files scanning  python3 /opt/volatility3/vol.py -f image.raw windows.filescan 文件扫描

python3 /opt/volatility3/vol.py -f image.raw windows.dumpfiles --pid="2760" Dump Files  python3 /opt/volatility3/vol.py -f image.raw windows.dumpfiles --pid="2760" 转储文件

python3 /opt/volatility3/vol.py -f physmemraw windows.hashdump.Hashdump hashdump  python3 /opt/volatility3/vol.py -f physmemraw windows.hashdump.Hashdump 哈希转储

Volatility 3のWindows symbolic table

Volatility 3 的 Windows 符号表

JPCERTCC/Windows-Symbol-Tables: Windows symbol tables for Volatility 3

JPCERTCC/Windows-Symbol-Tables：Volatility 3 的 Windows 符号表

Linux

OS特定 python3 /opt/volatility3/vol.py -f dump.mem banner

シンボルテーブルの作成 Volatility 3のシンボルテーブルを手動で作成する – NFLabs. エンジニアブログ

创建符号表 手动为 Volatility 3 创建符号表 – NFLabs. 工程​​师博客

コマンド python3 /opt/volatility3/vol.py -f dump.memの後に 命令 python3 /opt/volatility3/vol.py -f dump.memの後に

linux.bash コマンド履歴を取得  获取linux.bash命令历史记录

linux.psaux ps -aux結果

linux.psaux ps -aux 结果

Volatility2 波动性2

本当は載せるべきではないんだろうけど、こっちじゃないとたまーに動かなくて未だに動かす。

我可能不应该发布它，但除非我在这里发布，否则它仍然不起作用。今から始める人は絶対にVolatility3から始めること。

那些刚刚起步的人绝对应该从 Volatility3 开始。

情報セキュリティ技術のスキルアップ・イベント 仙台CTF 2017

信息安全技术技能提升活动仙台CTF 2017

よい日本語資料 好的日本材料

解析前にprofileを特定、または、用意する必要がある

在分析之前有必要确定或准备概况。

python2 /opt/volatility/vol.py -f memory.raw imageinfoでひたすら待てば可能性のあるprofileが提案されてくる

如果您在 python2 /opt/volatility/vol.py -f memory.raw imageinfo 等待，系统会建议可能的个人资料。

得られない場合は、デフォルトでないということなので、何とか調べてプロファイルを作って解析する

如果您无法获取它，则意味着它不是默认值，因此请以某种方式查找、创建配置文件并对其进行分析。

CTFtime.org / HTB Business CTF 2021 / Compromised / Writeup

CTFtime.org / HTB Business CTF 2021 / 受损 / 撰写

profileを自分で作るとき  创建自己的个人资料时

module.dwarf（Kernel Data Structures）とSystem.map（Debug Symbols）があれば、profileを自分で作れる

如果您有 module.dwarf （内核数据结构）和 System.map （调试符号），您可以自己创建一个配置文件。

zip _phillip.zip module.dwarf System.mapでzipを作る 使用 zip _phillip.zip module.dwarf System.map 创建 zip

できたzipをvolatility/plugins/overlays/linux/に置く 将创建的 zip 放入 volatility/plugins/overlays/linux/ 中

vol2 --info | grep Profileをすると追加されているので、その名前で使える

如果您执行 vol2 --info | grep Profile ，则会添加该名称，因此您可以使用该名称。

CTFtime.org / HTB Business CTF 2021 / Compromised / Writeup

CTFtime.org / HTB Business CTF 2021 / 受损 / 撰写

GitHub – volatilityfoundation/profiles: Volatility profiles for Linux and Mac OS Xにあるかも

profiles,Linux 和 Mac OS X 的波动率配置文件,下载profiles的源码_GitHub_帮酷

python2 /opt/volatility/vol.py -f memory.raw --profile=Win7SP1x64 [command]みたいにプロファイルをつけてコマンド実行する

使用 python2 /opt/volatility/vol.py -f memory.raw --profile=Win7SP1x64 [command] 等配置文件执行命令

windows 视窗

プロセスを確認してみよう  我们来检查一下流程

pslist -P 実行中のプロセスリストが得られる

pslist -P 可以获得正在运行的进程列表

pstree 実行中のプロセスツリーが得られる

pstree 可以获得正在运行的进程树

cmdline 動いているコマンドを一覧表示できる

cmdline 可以显示正在运行的命令列表

cmdline -p [pid]で実行時のコマンドラインが得られる

cmdline -p [pid] 在运行时为您提供命令行

怪しいプロセスのpidが得られたら…  一旦你获得了可疑进程的 pid…

dumpfiles --pid="[pid]" --dump-dir=./で関連ファイルを抜き出してみる

尝试使用 dumpfiles --pid="[pid]" --dump-dir=./ 提取相关文件

stringsしてから関連キーワードでgrepしてやれば何か出てくるかも

如果您执行字符串操作，然后使用相关关键字进行 grep，您可能会找到一些东西。

procdump -p [pid] -D output pidのプロセスのexeを出力する

procdump -p [pid] -D output 输出带有pid的进程的exe

memdump --pid=[pid] -D . 指定pidのメモリダンプ  memdump --pid=[pid] -D . 指定pid的内存转储

cmdscan cmd.exeで使用したコマンドが見られる（パスワードとか抜けたりするかも）

cmdscan 您可以看到cmd.exe使用的命令（密码可能丢失）

consoles よくわかってないけど、cmdscan使っておけばいいと思う

consoles 我不太明白，但我认为你应该使用cmdscan。

envars 環境変数が見られる  envars 可以看到环境变量

filescan 現在開かれているファイル一覧が得られる

filescan 您可以获得当前打开的文件的列表。

grepをうまく使うといい もろもろ filescan | grep hostsみたいに

很好地使用 grep，例如 もろもろ filescan | grep hosts

dumpfiles -D . --name -Q [offset] offsetのファイルをdumpする

将文件转储到 dumpfiles -D . --name -Q [offset] 偏移量处

offsetはfilescanで得られたオフセットを入れる ex.0x000000004fa23f0

offset 是 filescan ex. 0x000000004fa23f0 获取的偏移量

hashdump ユーザーアカウントのパスワードハッシュを取得する

hashdump 获取用户帐户的密码哈希

clipboard クリップボードを取得する  clipboard 获取剪贴板

notepad ノートパッドにある文字列を抜き出してくる

notepad 从记事本中提取字符串

screenshot -D screens/ スクリーンショットを持ってくることができる？

screenshot -D screens/ 你能截图吗？

通信系

まずはこれ 👉 netscan ネット通信関連のアーティファクト収集

首先，就是这个了👉 netscan 收集与网络通讯相关的神器

sockets 確立しているTCP/UDPのソケット一覧取得（だけど--profile=Win7SP1x86_23418でやってみたら動かなかった

sockets 获取已建立的 TCP/UDP 套接字列表（但是当我尝试使用 --profile=Win7SP1x86_23418 时它不起作用）

connections 通信の一覧を取得（だけど--profile=Win7SP1x86_23418でやってみたら動かなかった

connections 获取通信列表（但是当我尝试使用 --profile=Win7SP1x86_23418 时它不起作用

connscan 通信の一覧を取得（だけど--profile=Win7SP1x86_23418でやってみたら動かなかった

connscan 获取通信列表（但是当我尝试使用 --profile=Win7SP1x86_23418 时它不起作用

iehistory IEの履歴を取得する  iehistory 获取 IE 历史记录

yarascan -Y "[keyword]" yaraを使ってキーワードスキャンする

yarascan -Y "[keyword]" 使用 yara 扫描关键字

レジストリ系   登记系统

hivelist レジストリハイブ一覧を取得する

hivelist 获取注册表配置单元列表

dumpregistry -o [offset] -D output hivelistからoffset（0xXXXXXX)を持ってきて、これで出力する。Registry Explorerで中身を見ればいい。

dumpregistry -o [offset] -D output 从 hivelist 获取偏移量 (0xXXXXXX) 并以此输出。您可以使用注册表资源管理器查看内容。

userassist レジストリのUserAssis情報を見て、起動履歴などを確認する

userassist 查看注册表中的UserAssis信息，查看启动历史记录等。

printkey -K "Software\Microsoft\Windows\CurrentVersion\UnreadMail\[email protected]" レジストリを直接参照したいとき

printkey -K "Software\Microsoft\Windows\CurrentVersion\UnreadMail\[email protected]" 当你想直接引用注册表时

lsadump LSAメモリをダンプしてくる  lsadump 转储 LSA 内存

linux Linux Command Reference · volatilityfoundation/volatility Wiki

linux Linux 命令参考 ·volatilityfoundation/volatility Wiki

linux_bash bashの実行履歴を確認する  linux_bash 检查bash执行历史记录

linux_enumerate_files ファイル列挙ができる   linux_enumerate_files 可以枚举文件

ここでメモリアドレスも一緒に得られるのでlinux_find_file -i [address] -O [output filename]で取り出せる

您还可以在这里获取内存地址，因此您可以使用 linux_find_file -i [address] -O [output filename] 检索它

linuxのバージョンを把握するとき grep -a "Linux version" mem.limeのように関連ワードで直接grep

确定linux版本时，直接grep相关词，如 grep -a "Linux version" mem.lime

Welcome to Ubuntu 20.04.1 LTS

TAMU CTF 2021だと、ISOダウンロードしてきてvolatilityツールでdwarfとmapを取得してきて使っている。

对于 TAMU CTF 2021，我下载了 ISO 并使用波动性工具获取矮人和地图。

linux_lsof lsofコマンドと同等の結果が得られる

linux_lsof 获得与 lsof 命令等效的结果

すべてのプロセスがオープンしているディスク上のファイル、名前付きパイプ、ネットワークソケット、デバイスが含まれる

包含磁盘上的文件、命名管道、网络套接字以及所有进程打开的设备。

オープンしているものとしては  既然是开放的

/dev/pts/0 ファイルか名前付きパイプ（？）

/dev/pts/0 文件或命名管道 (?)

socket:[xxx] ネットワークソケット xxxにある数字はなんだろう

socket:[xxx] 网络套接字 xxx 中的数字是多少？

anon_inode:[xxx] わからん  anon_inode:[xxx] 我不知道

pipe:[xxx] pipe？  pipe:[xxx] 管道？

:[xxx] anonymous file createdらしい

:[xxx] 似乎已创建匿名文件

ctf-writeups/2022-HTB-Business at master · Zarkrosh/ctf-writeups

ctf-writeups/2022-HTB-业务大师 · Zarkrosh/ctf-writeups

何かが書き込まれた可能性があるので、プロセスが使っていたinodeを検索して、片っ端からダンプしてみる

有可能向其中写入了某些内容，因此请搜索该进程使用的 inode 并从一端转储它。

pidからメモリマップを取得 linux_proc_maps -p [pid] 从pid linux_proc_maps -p [pid] 获取内存映射

0xffff911935415b00 9260 bash 0x00005574f0196000 0x00005574f02a2000 rw- 0x0 0 0 0 [heap]

0xffff911935415b00 9260 bash 0x00007ffc9446d000 0x00007ffc9448e000 rw- 0x0 0 0 0 [stack]

こんな感じでheap領域やらstack領域やらも表示してくれるので持ってきてstringsとかすると面白いデータが転がってるかも

它将像这样显示堆区域和堆栈区域，因此如果您将其带入和字符串，您可能会发现一些有趣的数据。

linux_dump_map -p [pid] -s 0x00007ffc9446d000 -D .のような感じでstack領域をダンプしてこれる

您可以使用 linux_dump_map -p [pid] -s 0x00007ffc9446d000 -D . 之类的内容转储堆栈区域

指定しているのは仮想アドレスみたいで物理アドレスに変換する必要があるが、Volatilityがうまくやってくれる

看起来您指定的是虚拟地址，因此您需要将其转换为物理地址，但 Volatility 做得很好。

理論は19: Intro to Memory Forensics | COMPSCI 590F | Advanced Digital Forensics (Spring 2019)

理论は 19：内存取证简介 | COMPSCI 590F |高级数字取证（2019 年春季）

メモリマップから使っているライブラリを推定して、そこで使われている構造体が分かれば、stack領域とかから構造体を引っ張ってこれるかも

如果您可以从内存映射中估计正在使用的库并找出那里使用的结构，您也许可以从堆栈区域中提取该结构。

linux_volshell pythonコンソールを起動して、色々やる

linux_volshell 启动python控制台并执行各种操作

cc(pid=[pid])でコンテキストを指定pidに移す（色々やる前にやる）

使用 cc(pid=[pid]) 将上下文移动到指定的 pid（在执行其他操作之前执行此操作）

使用されている（いた？）inodeを抜き出す  提取使用过的（曾经？）inode

for filp, fd in self._proc.lsof():として print("{}: {} (INODE: {})".format(fd, filp, filp.f_inode))として更に改行

for filp, fd in self._proc.lsof(): 然后 print("{}: {} (INODE: {})".format(fd, filp, filp.f_inode)) 然后另一个换行符

0: 18446622369272764928 (INODE: 18446622369302465544)という感じで色々出てくる。先頭の0:部分はファイルディスクリプタでlsofした結果と紐づく

0: 18446622369272764928 (INODE: 18446622369302465544) 类似这样的事情有很多。第一个 0: 部分与使用文件描述符的 lsof 结果相关联。

linux_find_file -i [inode] -O out.binとしてファイルをダンプしてくる

将文件转储为 linux_find_file -i [inode] -O out.bin

OpenSSHのカギを取得するためのプラグインがある

有一个插件可以获取 OpenSSH 密钥。

https://github.com/fox-it/OpenSSH-Session-Key-Recovery/blob/main/volatility2/openssh_sessionkeys.py

原文始发于hamayanhamayan：CTFのフォレンジックにおけるメモリフォレンジックまとめ [Volatility 3, Volatility 2]