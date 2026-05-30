# 强网杯2025 Secured Personal Vault 预期解WP

> 原文: https://www.ctfiot.com/282078.html
> ID: 282078

functioninitializeScript(){return[newhost.functionAlias(safeDumpMemory,"MDump")];}asyncfunctionsafeDumpMemory(filePath, startAddress, imageSize){constpageSize =4096;lettotalBytesWritten =0;letlog = host.diagnostics.debugLog;log(`[*] 开始安全转储内存...n`);log(` - 输出文件:${filePath}.pyn`);log(` - 起始地址: 0x${startAddress.toString(16)}n`);log(` - 总大小: 0x${imageSize.toString(16)}bytesn`);try {// 创建或覆盖目标文件letfile = host.namespace.Debugger.Utility.FileSystem.CreateFile(filePath +".py","CreateAlways");vartextWriter = host.namespace.Debugger.Utility.FileSystem.CreateTextWriter(file,'Utf8');// 创建一个4KB的全零缓冲区，用于填充坏页letnullBuffer =newArrayBuffer(pageSize);letnullView =newUint8Array(nullBuffer); textWriter.WriteLine(`# python${filePath}.pybuffer = [ `);// 逐页循环for(letoffset = host.Int64(0); offset.compareTo(imageSize) <0; offset = offset.add(pageSize)) {letcurrentAddress = startAddress.add(offset);letbytesToWrite = (imageSize.subtract(offset).compareTo(pageSize) <0) ? imageSize.subtract(offset) : host.Int64(pageSize);try {// 尝试读取当前内存页letbuffer = host.memory.readMemoryValues(currentAddress,bytesToWrite); textWriter.WriteLine(buffer); textWriter.WriteLine(","); }catch(e) {log(`[!] 错误:${e}n`);// 如果读取失败，就写入零log(`[!] 无法读取地址: 0x${currentAddress.toString(16)}。正在写入0x${bytesToWrite.toString(16)}字节的0... n`); textWriter.WriteLine(nullView); textWriter.WriteLine(","); } totalBytesWritten += bytesToWrite;// 每转储1页打印一次进度if(offset.bitwiseAnd(0xFFFFF) ==0&& offset.compareTo(0) >0) {log(` ... 已写入 0x${offset.toString(16)}bytesn`); } } textWriter.WriteLine(`]f = open('${filePath}','wb')f.write(bytearray(buffer))`); file.Close();log(`n[+] 转储完成! 总共写入 0x${imageSize.toString(16)}字节 请运行${filePath}.pyn`); }catch(e) {log(`[!] 发生严重错误:${e}n`); }}

structCommuStruct{charsign[4];intfunction; __int64 pid; __int64 *processCreateTime;};

0298: Object: ffffe70b7f0673c0 GrantedAccess:
00160089(Protected)En
try:
ffffa687a73fba60Object: ffffe70b7f0673c0 Type:(ffffe70b77835850)FileObjectHeader:
ffffe70b7f067390(newversion)HandleCount: 2 PointerCount:
32768Directory Object: 00000000 Name:
mailslot_1359e83{Mailslot}data:
ffffa687`a8d145d83c5b7d22a862ff7e-89eff96d26e3d3e6<[}".b.~...m&...ffffa687`a8d145e82fc39dff8ac54c0b-e2d1024739459683/.....L....G9E..ffffa687`a8d145f846ce2068f60af065-2b5b85be4fdcf563F.h...e+[..O..cffffa687`a8d14608eee2749f4e077129-03947e5ab0bf6675..t.N.q)..~Z..fuffffa687`a8d146186c4b9cd7c210fd45-4da965368402f98elK.....EM.e6....027c: Object: ffffe70b7f057380 GrantedAccess:
00160089(Protected)(Audit)En
try:
ffffa687a73fb9f0Object: ffffe70b7f057380 Type:(ffffe70b77835850)FileObjectHeader:
ffffe70b7f057350(newversion)HandleCount: 1 PointerCount:
1Directory Object: 00000000 Name:
mailslot_e60a23e2{Mailslot}data:
ffffa687`a5efa7a895c24e064192cf1c-52180132864e385e..N.A...R..2.N8^ffffa687`a5efa7b8e2ee247b680fdcbe-7e143bee47fd2213..${h...~.;.G.".ffffa687`a5efa7c8b3711c1b4008e2b3-ff7834ebe53e7d53.q..@....x4..>}Sffffa687`a5efa7d8485359167446f58b-eb9d961c57135ebbHSY.tF......W.^.ffffa687`a5efa7e82a18fa30982923db-9973d6ac4b0188c5*..0.)#..s..K...ffffa687`a5efa7f87e38b0a58d3e71b0-fec98e7bd8e30c2c~8...>q....{...,ffffa687`a5efa8082707b994946853af-7198843b89ac21de'....hS.q..;..!.ffffa687`a5efa818 56 67 7c c3 e6 cf 43 b8-d6 d5 39 61 5c 76 31 79 Vg|...C...9av1yPROCESS ffffef063fbc1080 ->A(bsod) CreateTime: 0x01dc3fe6f02a77eb SessionId: none Cid: 26f0 Peb: 9216e1a000 ParentCid: 14b0 DirBase: 1296dc000 ObjectTable: ffffa687a6dd3b40 HandleCount: 165. Image: aPersonalVault.exeunsigned char aes_key[] ={ 0x20, 0x51, 0xB5, 0x07, 0x07, 0x70, 0xB8, 0x0E, 0xFC, 0xA3, 0x9C, 0x30, 0x54, 0x92, 0xD6, 0x44, 0x9D, 0x08, 0xE2, 0x02, 0xFE, 0x81, 0xD1, 0xF6, 0x70, 0xB6, 0x86, 0x35, 0x20, 0xB4, 0xA6, 0x6E};
unsigned char iv[] ={ 0xAF, 0x40, 0xDF, 0x21, 0xDA, 0x73, 0x21, 0x01, 0x3A, 0xFA, 0x99, 0x1C, 0xE6, 0x56, 0x69, 0x00};PROCESS ffffef063fbe8080 ->B CreateTime: 0x01dc3fe6ed454439 SessionId: none Cid: 0fa8 Peb: 9f83185000 ParentCid: 14b0 DirBase: 840fe000 ObjectTable: ffffa687a7241740 HandleCount: 161. Image: aPersonalVault.exeunsigned char key[] ={ 0x45, 0x71, 0x9C, 0x96, 0xF3, 0x11, 0x80, 0x2E, 0x9D, 0xAC, 0xF2, 0x94, 0x64, 0x4E, 0xC7, 0xE5, 0x52, 0xA4, 0x46, 0x35, 0x5E, 0x86, 0x72, 0x75, 0xA9, 0xB7, 0xBF, 0x80, 0x52, 0xD0, 0x06, 0xA2};
unsigned char iv[] ={ 0xC9, 0x62, 0xDD, 0x9C, 0xF2, 0xEE, 0x60, 0x5E, 0xA0, 0x6B, 0x4C, 0xCF, 0xB5, 0xEF, 0x0D, 0x82};

看雪ID：moshuiD

https://bbs.kanxue.com/user-home-932553.htm

*本文为看雪论坛精华文章，由moshuiD原创，转载请注明来自看雪社区

# 往期推荐

KernelSU检测之“时间侧信道攻击”

记录工作中解决bug用到的逆向知识

写一个简单的ollvm混淆还原

VmProtect.3.0.0beta分析之虚拟机流程

AI辅助逆向APP白盒AES分析

球分享

球点赞

球在看

点击阅读原文查看更多


```
functioninitializeScript(){return[newhost.functionAlias(safeDumpMemory,"MDump")];}asyncfunctionsafeDumpMemory(filePath, startAddress, imageSize){constpageSize =4096;lettotalBytesWritten =0;letlog = host.diagnostics.debugLog;log(`[*] 开始安全转储内存...n`);log(` - 输出文件:${filePath}.pyn`);log(` - 起始地址: 0x${startAddress.toString(16)}n`);log(` - 总大小: 0x${imageSize.toString(16)}bytesn`);try {// 创建或覆盖目标文件letfile = host.namespace.Debugger.Utility.FileSystem.CreateFile(filePath +".py","CreateAlways");vartextWriter = host.namespace.Debugger.Utility.FileSystem.CreateTextWriter(file,'Utf8');// 创建一个4KB的全零缓冲区，用于填充坏页letnullBuffer =newArrayBuffer(pageSize);letnullView =newUint8Array(nullBuffer); textWriter.WriteLine(`# python${filePath}.pybuffer = [ `);// 逐页循环for(letoffset = host.Int64(0); offset.compareTo(imageSize) <0; offset = offset.add(pageSize)) {letcurrentAddress = startAddress.add(offset);letbytesToWrite = (imageSize.subtract(offset).compareTo(pageSize) <0) ? imageSize.subtract(offset) : host.Int64(pageSize);try {// 尝试读取当前内存页letbuffer = host.memory.readMemoryValues(currentAddress,bytesToWrite); textWriter.WriteLine(buffer); textWriter.WriteLine(","); }catch(e) {log(`[!] 错误:${e}n`);// 如果读取失败，就写入零log(`[!] 无法读取地址: 0x${currentAddress.toString(16)}。正在写入0x${bytesToWrite.toString(16)}字节的0... n`); textWriter.WriteLine(nullView); textWriter.WriteLine(","); } totalBytesWritten += bytesToWrite;// 每转储1页打印一次进度if(offset.bitwiseAnd(0xFFFFF) ==0&& offset.compareTo(0) >0) {log(` ... 已写入 0x${offset.toString(16)}bytesn`); } } textWriter.WriteLine(`]f = open('${filePath}','wb')f.write(bytearray(buffer))`); file.Close();log(`n[+] 转储完成! 总共写入 0x${imageSize.toString(16)}字节 请运行${filePath}.pyn`); }catch(e) {log(`[!] 发生严重错误:${e}n`); }}
structCommuStruct{charsign[4];intfunction; __int64 pid; __int64 *processCreateTime;};
0298: Object: ffffe70b7f0673c0 GrantedAccess:
00160089(Protected)En
try:
ffffa687a73fba60Object: ffffe70b7f0673c0 Type:(ffffe70b77835850)FileObjectHeader:
ffffe70b7f067390(newversion)HandleCount: 2 PointerCount:
32768Directory Object: 00000000 Name:
mailslot_1359e83{Mailslot}data:
ffffa687`a8d145d83c5b7d22a862ff7e-89eff96d26e3d3e6<[}".b.~...m&...ffffa687`a8d145e82fc39dff8ac54c0b-e2d1024739459683/.....L....G9E..ffffa687`a8d145f846ce2068f60af065-2b5b85be4fdcf563F.h...e+[..O..cffffa687`a8d14608eee2749f4e077129-03947e5ab0bf6675..t.N.q)..~Z..fuffffa687`a8d146186c4b9cd7c210fd45-4da965368402f98elK.....EM.e6....027c: Object: ffffe70b7f057380 GrantedAccess:
00160089(Protected)(Audit)En
try:
ffffa687a73fb9f0Object: ffffe70b7f057380 Type:(ffffe70b77835850)FileObjectHeader:
ffffe70b7f057350(newversion)HandleCount: 1 PointerCount:
1Directory Object: 00000000 Name:
mailslot_e60a23e2{Mailslot}data:
ffffa687`a5efa7a895c24e064192cf1c-52180132864e385e..N.A...R..2.N8^ffffa687`a5efa7b8e2ee247b680fdcbe-7e143bee47fd2213..${h...~.;.G.".ffffa687`a5efa7c8b3711c1b4008e2b3-ff7834ebe53e7d53.q..@....x4..>}Sffffa687`a5efa7d8485359167446f58b-eb9d961c57135ebbHSY.tF......W.^.ffffa687`a5efa7e82a18fa30982923db-9973d6ac4b0188c5*..0.)#..s..K...ffffa687`a5efa7f87e38b0a58d3e71b0-fec98e7bd8e30c2c~8...>q....{...,ffffa687`a5efa8082707b994946853af-7198843b89ac21de'....hS.q..;..!.ffffa687`a5efa818 56 67 7c c3 e6 cf 43 b8-d6 d5 39 61 5c 76 31 79 Vg|...C...9av1yPROCESS ffffef063fbc1080 ->A(bsod) CreateTime: 0x01dc3fe6f02a77eb SessionId: none Cid: 26f0 Peb: 9216e1a000 ParentCid: 14b0 DirBase: 1296dc000 ObjectTable: ffffa687a6dd3b40 HandleCount: 165. Image: aPersonalVault.exeunsigned char aes_key[] ={ 0x20, 0x51, 0xB5, 0x07, 0x07, 0x70, 0xB8, 0x0E, 0xFC, 0xA3, 0x9C, 0x30, 0x54, 0x92, 0xD6, 0x44, 0x9D, 0x08, 0xE2, 0x02, 0xFE, 0x81, 0xD1, 0xF6, 0x70, 0xB6, 0x86, 0x35, 0x20, 0xB4, 0xA6, 0x6E};
unsigned char iv[] ={ 0xAF, 0x40, 0xDF, 0x21, 0xDA, 0x73, 0x21, 0x01, 0x3A, 0xFA, 0x99, 0x1C, 0xE6, 0x56, 0x69, 0x00};PROCESS ffffef063fbe8080 ->B CreateTime: 0x01dc3fe6ed454439 SessionId: none Cid: 0fa8 Peb: 9f83185000 ParentCid: 14b0 DirBase: 840fe000 ObjectTable: ffffa687a7241740 HandleCount: 161. Image: aPersonalVault.exeunsigned char key[] ={ 0x45, 0x71, 0x9C, 0x96, 0xF3, 0x11, 0x80, 0x2E, 0x9D, 0xAC, 0xF2, 0x94, 0x64, 0x4E, 0xC7, 0xE5, 0x52, 0xA4, 0x46, 0x35, 0x5E, 0x86, 0x72, 0x75, 0xA9, 0xB7, 0xBF, 0x80, 0x52, 0xD0, 0x06, 0xA2};
unsigned char iv[] ={ 0xC9, 0x62, 0xDD, 0x9C, 0xF2, 0xEE, 0x60, 0x5E, 0xA0, 0x6B, 0x4C, 0xCF, 0xB5, 0xEF, 0x0D, 0x82};
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121641-wxsync-2025-11-a136d22308f26694b692feb6225e32e8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121644-wxsync-2025-11-6c09fe2075d99ab7838f07e814d62898.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121647-wxsync-2025-11-790b7b49be92e0417a0807a5298fb421.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121649-wxsync-2025-11-7bf06122b073e638114fa2e8bef1dd13.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121650-wxsync-2025-11-a959896ab724099e11c47ab979dc97b3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121652-wxsync-2025-11-4cfa8c638684d4de7d589eb88fd47374.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121654-wxsync-2025-11-7de6e46f3473b8c03a70689d498a9be4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121656-wxsync-2025-11-31e411974663809cd1ffab41fadcccb1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121658-wxsync-2025-11-7e39ee97edee048ae50a5c89346067b7.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121659-wxsync-2025-11-3f3f375c922ca6222a0894c8ef3444be.png)