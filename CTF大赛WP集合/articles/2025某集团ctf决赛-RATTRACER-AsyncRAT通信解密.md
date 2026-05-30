# 2025某集团ctf决赛-RATTRACER-AsyncRAT通信解密

> 原文: https://www.ctfiot.com/285924.html
> ID: 285924

小伙伴给了两道ctf说帮忙看看，感觉挺有意思的，这里简单记录一下。附件，https://bohemian.top/images/RATTRACER.zip,有兴趣的小伙伴可以先试一下。

开局给到两个文件

这里一看就是 证书 需要解密

打开wireshark 可以看到是 tlsv1的流量 这里需要解密。回头看p12文件p12 文件其实就是PKCS#12格式的证书文件，通常以.p12或.pfx结尾，用来同时存储证书 (Certificate) + 私钥 (Private Key)，而且可以设置密码保护。

这里知道p12有私钥，会有密码保护openssl pkcs12 -info -in ST.p12敲这个会让我们输入密码，直接回车，显示

说明没有密码，openssl pkcs12 -legacy -in ST.p12 -nocerts -nodes -out key.pem直接命令提私钥即可。让我们输密码，直接回车即可。

此时导入私钥。wireshrak ->编解->首选项–>protocols->tls

ip port 协议 和私钥填写好。

此时你随便选中一个tls流量就可以看到解密后的流量了，

此时看到里面还是 加密的，但是可以看到一点点特征。这个rat的特征呢。

经过对这个特征的搜索，找到一篇大师傅的文章，发现为AsyncRAT，

开源项目https://github.com/NYAN-x-CAT/AsyncRAT-C-Sharp

在https://mp.weixin.qq.com/s/AJUQ8Zd_4Q3Ub9TarQx5Gg文章中 已经给出了详细的解密流程，简单来说就是外层是套了tls的数据，有私钥就能解，内层也就是现在看到的，不涉及加解密，只涉及gunzip和unzip，再就是文件结构了。在仔细看大师傅文章中说的使用到的aes key及HMACSHA256 key，aes key及HMACSHA256 key是对配置信息进行解密，也就是解密样本的，在此题中不涉及，就不讲了。接下来看通信。

这里选择一个数据包，其中从1f 8b 08开始，这是gzip的hex头，然后gunzip即可，解出所有流量了，这里给出python批量脚本。这里需要先将所有的流都保存为bin文件，其实什么文件都行。

importosimportstructimportbinasciiimportglobimportgzipimporthashlibfromcommonimportreverse_data, bytes_to_int, gzip_uncompress, hash_data_sha256, write_filedefgetbuflen(buf, isreverse=False): """获取缓冲区长度""" tmp = buf[:] ifisreverse: tmp = reverse_data(tmp) returnbytes_to_int(tmp)defparseMsgPack(data): """解析MsgPack数据""" output = [] # 键值对数量 output.append(str(data[0] -0x80)) off =1 whileoff <len(data): # 解析载荷数据 buf, num = readstring(data[off:]) ifnum !=0: output.append(buf) off += num else: break ifbuf =="Msgpack": msgbuf, num = readbinary(data[off:]) ifnum !=0: output.append(msgbuf) off += num iflen(output) >=2andoutput[-1] =="Dll"andoutput[-2] =="savePlugin": msgbuf, num = readbinary(data[off:]) ifnum !=0: output.append(msgbuf) off += num return"->".join(output), offdefreadstring(data): """读取字符串""" ifnotdata: return"",0 byteflag = data[0] if160<= byteflag <=191: num = byteflag -160 iflen(data) < num +1: return"",0 output = data[1:num+1].decode('utf-8', errors='ignore') returnoutput, num +1 elifbyteflag ==217: iflen(data) <2: return"",0 num = data[1] iflen(data) < num +2: return"",0 output = data[2:num+2].decode('utf-8', errors='ignore') returnoutput, num +2 return"",0defreadbinary(buf): """读取二进制数据""" ifnotbuf: return"",0 byteflag = buf[0] ifbyteflag ==0xc4: iflen(buf) <2: return"",0 len_zipdata = buf[1] iflen(buf) <6+ len_zipdata -4: return"",0 len_data = getbuflen(buf[2:6],True) zipdata = buf[6:6+len_zipdata-4] data = gzip_uncompress(zipdata) ifdataisNoneorlen_data !=len(data): return"",0 output, off = parseMsgPack(data) ifoff !=len(data): return"",0 returnoutput,2+ len_zipdata elifbyteflag ==0xc6: iflen(buf) <9: return"",0 len_zipdata = getbuflen(buf[1:5],False) len_data = getbuflen(buf[5:9],True) iflen(buf) <9+ len_zipdata -4: return"",0 zipdata = buf[9:9+len_zipdata-4] data = gzip_uncompress(zipdata) ifdataisNoneorlen_data !=len(data): return"",0 ifdata.startswith(b'MZ'): filename ="dll_"+ hash_data_sha256(data) write_file(filename, data) output ="保存DLL，文件名为-"+ filename returnoutput,1+4+ len_zipdata else: output, off = parseMsgPack(data) if"wallpaper"inoutput: ifoff +5<len(data): len_image = getbuflen(data[off+1:off+5],False) ifoff +5+ len_image <=len(data): imagedata = data[off+5:off+5+len_image] filename ="image_"+ hash_data_sha256(imagedata) write_file(filename, imagedata) output ="保存图片，文件名为-"+ filename returnoutput,1+4+ len_zipdata return"",0defprocess_bin_file(filename, output_file): """处理单个bin文件""" try: withopen(filename,'rb')asf: data = f.read() exceptExceptionase: print(f"读取文件失败{filename}:{e}") return print(f"处理文件:{filename}") base_name = os.path.splitext(os.path.basename(filename))[0] withopen(output_file,'a', encoding='utf-8')asf: f.write(f"n=== 处理文件:{filename}===nn") num =0 pkt_num =0 whilenum <len(data): ifnum +4>len(data): break len_encodedata = getbuflen(data[num:num+4],True) ifnum + len_encodedata +4>len(data): break encodedata = data[num+4:num+4+len_encodedata] iflen(encodedata) <4: num += len_encodedata +4 continue len_decodedata = getbuflen(encodedata[:4],True) zipdata = encodedata[4:] decodedata = gzip_uncompress(zipdata) ifdecodedataandlen(decodedata) == len_decodedata: # 保存解密数据到统一文件 withopen(output_file,'a', encoding='utf-8')asf: f.write(f"--- 数据包{pkt_num}---n") iflen_encodedata >0x200: f.write(f"加密数据：{binascii.hexlify(data[num:num+0x200+4]).decode()}n") f.write(f"解密数据_hex：{binascii.hexlify(decodedata[:0x200]).decode()}n") else: f.write(f"加密数据：{binascii.hexlify(data[num:num+len_encodedata+4]).decode()}n") f.write(f"解密数据_hex：{binascii.hexlify(decodedata).decode()}n") output, off = parseMsgPack(decodedata) ifoff !=len(decodedata): if"2->Packet->pong->Message"notinoutput: f.write("Errorn") f.write(f"解密通信指令：{output}nn") print(f"已处理数据包{pkt_num}") pkt_num +=1 else: print("!!!解压失败!!!") num += len_encodedata +4defmain(): """主函数""" # 获取所有bin文件 bin_files = glob.glob("*.bin") print(f"找到{len(bin_files)}个bin文件") # 创建统一的输出文件 output_file ="decrypted_output.txt" # 清空文件 withopen(output_file,'w', encoding='utf-8')asf: f.write("解密报告 - 所有bin文件数据n") f.write("="*50+"nn") forfilenameinbin_files: process_bin_file(filename, output_file) print(f"解密完成，结果保存到{output_file}") main()if__name__ =="__main__": main()

然后就可以解出所有相关信息了。这里小伙伴又说忘记题目是啥了，根据已知的信息，并没有flag关键字，那我们就将所有的流量提出来，这里你会问，不是已经把所有的流量都解出来了么，是的，但是有一个没有解出来，就是>remoteDesktop-，这是远程桌面的流量，可能出题人只是远程cat flag，

2流就是所有的数据，想办法提出来，首先找到

这种长的流，很长，

先解hex 在解gunzip 在进行tohex，这里就有图片的前缀了，

然后在解码就好了。

就可以解密所有rdp的流量了，一个一个提确实有点小慢，这里简单写个脚本

importosimportstructimportgzipimportbinasciifromcommonimportreverse_data, bytes_to_int, gzip_uncompressdefgetbuflen(buf, isreverse=False): """获取缓冲区长度""" tmp = buf[:] ifisreverse: tmp = reverse_data(tmp) returnbytes_to_int(tmp)defextract_jpeg_from_bin(bin_file, output_dir): """从 bin 文件中提取 JPEG 图像""" ifnotos.path.exists(output_dir): os.makedirs(output_dir) try: withopen(bin_file,'rb')asf: data = f.read() exceptExceptionase: print(f"读取文件失败{bin_file}:{e}") return print(f"处理文件:{bin_file}") num =0 pkt_num =0 jpeg_count =0 whilenum <len(data): ifnum +4>len(data): break len_encodedata = getbuflen(data[num:num+4],True) ifnum + len_encodedata +4>len(data): break encodedata = data[num+4:num+4+len_encodedata] iflen(encodedata) <4: num += len_encodedata +4 continue len_decodedata = getbuflen(encodedata[:4],True) zipdata = encodedata[4:] decodedata = gzip_uncompress(zipdata) ifdecodedataandlen(decodedata) == len_decodedata: # 查找 JPEG 数据 soi_index = decodedata.find(b'xffxd8xffxe0') ifsoi_index != -1: jpeg_data = decodedata[soi_index:] # 查找 EOI 标记 eoi_index = jpeg_data.find(b'xffxd9') ifeoi_index != -1: jpeg_data = jpeg_data[:eoi_index +2] # 包含 EOI # 保存 JPEG 文件 filename =f"{output_dir}/packet_{pkt_num}.jpg" withopen(filename,'wb')asimg_file: img_file.write(jpeg_data) print(f"提取 JPEG:{filename}") jpeg_count +=1 else: print(f"数据包{pkt_num}: 未找到 JPEG EOI 标记") else: print(f"数据包{pkt_num}: 未找到 JPEG SOI 标记") pkt_num +=1 else: print(f"数据包{pkt_num}: 解压失败") num += len_encodedata +4 print(f"n提取完成，共提取{jpeg_count}个 JPEG 图像到{output_dir}目录")if__name__ =="__main__": extract_jpeg_from_bin("bb.bin","extracted_images")

这样就会生成一个目录，

可以看到攻击者rdp了主机，看了一个程序 up.exe

在解析中也可以看到相关程序。

总的来说就是先解tls，在进行去除不需要的数据，在进行gunzip。

这里小伙伴也是不知道问题是啥了，看所有数据应该是这个了，有小伙伴知道的话，麻烦告知一下，咱们在研究。做这道题花费了一下午的时间，并且在一直查资料问gpt，小伙伴说比赛环境是不出网的，啊这。

致谢

最后感谢您读到现在，这篇文章匆忙构成肯定有不周到或描述不正确的地方，期待业界师傅们用各种方式指正勘误。如果您感觉文章写的不错，帮笔者点给公众号点点关注，先谢谢大家了。

emmm 太菜了一直在路上

参考

https://mp.weixin.qq.com/s/AJUQ8Zd_4Q3Ub9TarQx5Gg AsyncRAT通信模型剖析https://xz.aliyun.com/news/12945AsyncRAT通信模型剖析及自动化解密脚本实现


```
importosimportstructimportbinasciiimportglobimportgzipimporthashlibfromcommonimportreverse_data, bytes_to_int, gzip_uncompress, hash_data_sha256, write_filedefgetbuflen(buf, isreverse=False): """获取缓冲区长度""" tmp = buf[:] ifisreverse: tmp = reverse_data(tmp) returnbytes_to_int(tmp)defparseMsgPack(data): """解析MsgPack数据""" output = [] # 键值对数量 output.append(str(data[0] -0x80)) off =1 whileoff <len(data): # 解析载荷数据 buf, num = readstring(data[off:]) ifnum !=0: output.append(buf) off += num else: break ifbuf =="Msgpack": msgbuf, num = readbinary(data[off:]) ifnum !=0: output.append(msgbuf) off += num iflen(output) >=2andoutput[-1] =="Dll"andoutput[-2] =="savePlugin": msgbuf, num = readbinary(data[off:]) ifnum !=0: output.append(msgbuf) off += num return"->".join(output), offdefreadstring(data): """读取字符串""" ifnotdata: return"",0 byteflag = data[0] if160<= byteflag <=191: num = byteflag -160 iflen(data) < num +1: return"",0 output = data[1:num+1].decode('utf-8', errors='ignore') returnoutput, num +1 elifbyteflag ==217: iflen(data) <2: return"",0 num = data[1] iflen(data) < num +2: return"",0 output = data[2:num+2].decode('utf-8', errors='ignore') returnoutput, num +2 return"",0defreadbinary(buf): """读取二进制数据""" ifnotbuf: return"",0 byteflag = buf[0] ifbyteflag ==0xc4: iflen(buf) <2: return"",0 len_zipdata = buf[1] iflen(buf) <6+ len_zipdata -4: return"",0 len_data = getbuflen(buf[2:6],True) zipdata = buf[6:6+len_zipdata-4] data = gzip_uncompress(zipdata) ifdataisNoneorlen_data !=len(data): return"",0 output, off = parseMsgPack(data) ifoff !=len(data): return"",0 returnoutput,2+ len_zipdata elifbyteflag ==0xc6: iflen(buf) <9: return"",0 len_zipdata = getbuflen(buf[1:5],False) len_data = getbuflen(buf[5:9],True) iflen(buf) <9+ len_zipdata -4: return"",0 zipdata = buf[9:9+len_zipdata-4] data = gzip_uncompress(zipdata) ifdataisNoneorlen_data !=len(data): return"",0 ifdata.startswith(b'MZ'): filename ="dll_"+ hash_data_sha256(data) write_file(filename, data) output ="保存DLL，文件名为-"+ filename returnoutput,1+4+ len_zipdata else: output, off = parseMsgPack(data) if"wallpaper"inoutput: ifoff +5<len(data): len_image = getbuflen(data[off+1:off+5],False) ifoff +5+ len_image <=len(data): imagedata = data[off+5:off+5+len_image] filename ="image_"+ hash_data_sha256(imagedata) write_file(filename, imagedata) output ="保存图片，文件名为-"+ filename returnoutput,1+4+ len_zipdata return"",0defprocess_bin_file(filename, output_file): """处理单个bin文件""" try: withopen(filename,'rb')asf: data = f.read() exceptExceptionase: print(f"读取文件失败{filename}:{e}") return print(f"处理文件:{filename}") base_name = os.path.splitext(os.path.basename(filename))[0] withopen(output_file,'a', encoding='utf-8')asf: f.write(f"n=== 处理文件:{filename}===nn") num =0 pkt_num =0 whilenum <len(data): ifnum +4>len(data): break len_encodedata = getbuflen(data[num:num+4],True) ifnum + len_encodedata +4>len(data): break encodedata = data[num+4:num+4+len_encodedata] iflen(encodedata) <4: num += len_encodedata +4 continue len_decodedata = getbuflen(encodedata[:4],True) zipdata = encodedata[4:] decodedata = gzip_uncompress(zipdata) ifdecodedataandlen(decodedata) == len_decodedata: # 保存解密数据到统一文件 withopen(output_file,'a', encoding='utf-8')asf: f.write(f"--- 数据包{pkt_num}---n") iflen_encodedata >0x200: f.write(f"加密数据：{binascii.hexlify(data[num:num+0x200+4]).decode()}n") f.write(f"解密数据_hex：{binascii.hexlify(decodedata[:0x200]).decode()}n") else: f.write(f"加密数据：{binascii.hexlify(data[num:num+len_encodedata+4]).decode()}n") f.write(f"解密数据_hex：{binascii.hexlify(decodedata).decode()}n") output, off = parseMsgPack(decodedata) ifoff !=len(decodedata): if"2->Packet->pong->Message"notinoutput: f.write("Errorn") f.write(f"解密通信指令：{output}nn") print(f"已处理数据包{pkt_num}") pkt_num +=1 else: print("!!!解压失败!!!") num += len_encodedata +4defmain(): """主函数""" # 获取所有bin文件 bin_files = glob.glob("*.bin") print(f"找到{len(bin_files)}个bin文件") # 创建统一的输出文件 output_file ="decrypted_output.txt" # 清空文件 withopen(output_file,'w', encoding='utf-8')asf: f.write("解密报告 - 所有bin文件数据n") f.write("="*50+"nn") forfilenameinbin_files: process_bin_file(filename, output_file) print(f"解密完成，结果保存到{output_file}") main()if__name__ =="__main__": main()
```



```
importosimportstructimportgzipimportbinasciifromcommonimportreverse_data, bytes_to_int, gzip_uncompressdefgetbuflen(buf, isreverse=False): """获取缓冲区长度""" tmp = buf[:] ifisreverse: tmp = reverse_data(tmp) returnbytes_to_int(tmp)defextract_jpeg_from_bin(bin_file, output_dir): """从 bin 文件中提取 JPEG 图像""" ifnotos.path.exists(output_dir): os.makedirs(output_dir) try: withopen(bin_file,'rb')asf: data = f.read() exceptExceptionase: print(f"读取文件失败{bin_file}:{e}") return print(f"处理文件:{bin_file}") num =0 pkt_num =0 jpeg_count =0 whilenum <len(data): ifnum +4>len(data): break len_encodedata = getbuflen(data[num:num+4],True) ifnum + len_encodedata +4>len(data): break encodedata = data[num+4:num+4+len_encodedata] iflen(encodedata) <4: num += len_encodedata +4 continue len_decodedata = getbuflen(encodedata[:4],True) zipdata = encodedata[4:] decodedata = gzip_uncompress(zipdata) ifdecodedataandlen(decodedata) == len_decodedata: # 查找 JPEG 数据 soi_index = decodedata.find(b'xffxd8xffxe0') ifsoi_index != -1: jpeg_data = decodedata[soi_index:] # 查找 EOI 标记 eoi_index = jpeg_data.find(b'xffxd9') ifeoi_index != -1: jpeg_data = jpeg_data[:eoi_index +2] # 包含 EOI # 保存 JPEG 文件 filename =f"{output_dir}/packet_{pkt_num}.jpg" withopen(filename,'wb')asimg_file: img_file.write(jpeg_data) print(f"提取 JPEG:{filename}") jpeg_count +=1 else: print(f"数据包{pkt_num}: 未找到 JPEG EOI 标记") else: print(f"数据包{pkt_num}: 未找到 JPEG SOI 标记") pkt_num +=1 else: print(f"数据包{pkt_num}: 解压失败") num += len_encodedata +4 print(f"n提取完成，共提取{jpeg_count}个 JPEG 图像到{output_dir}目录")if__name__ =="__main__": extract_jpeg_from_bin("bb.bin","extracted_images")
```



```
https://mp.weixin.qq.com/s/AJUQ8Zd_4Q3Ub9TarQx5Gg AsyncRAT通信模型剖析https://xz.aliyun.com/news/12945AsyncRAT通信模型剖析及自动化解密脚本实现
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765249926-wxsync-2025-12-462ee47772940d92eafc3428a95aa1fc.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765249929-wxsync-2025-12-358677a9b4c81b11f295be3ab1adc138.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765249931-wxsync-2025-12-433c57bb71afe111721bda2773dfb497.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765249933-wxsync-2025-12-5afd2553f12a8547ab7ab6129039aadb.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765249935-wxsync-2025-12-32d0a12ea730878ef9aac02e3367c948.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765249936-wxsync-2025-12-5826c6f837569157e115c2a862d37e86.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765249938-wxsync-2025-12-d2f0271a5ef1db7390bca5a35810eac8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765249940-wxsync-2025-12-f06615f509e2617af3e75ed47f86b7d2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765249942-wxsync-2025-12-5a0727c0d5de5c888d2e882435d351cf.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765249943-wxsync-2025-12-247853954395f8edb1139abdf071bd1e.png)