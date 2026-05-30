# Wireshark

Wireshark 是一个网络封包分析软件。网络封包分析软件的功能是提取网络封包，并尽可能显示出最为详细的网络封包资料。

Wireshark 的主界面包含 6 个部分：

1. 菜单栏：用于调试、配置
2. 工具栏：常用功能的快捷方式
3. 过滤栏：指定过滤条件，过滤数据包
4. 数据包列表：核心区域，每一行就是一个数据包
5. 数据包详情：数据包的详细数据
6. 数据包字节：数据包对应的字节流，二进制

![](https://files.mdnice.com/user/88172/f9fa3cc7-9ab5-4c86-a926-e64eda9e968b.png)

注意，数据包详情面板中展示的信息是经过 Wireshark 解析并”格式化”过的，方便阅读。最下面的数据包字节面板里才是这个包的真实数据。

# 常见功能使用

### 过滤器

过滤器是 Wireshark 的核心功能，也是我们平时使用最多的一个功能。

Wireshark 提供了两个过滤器：抓包过滤器 和 显示过滤器。两个过滤器的过滤思路不同。

抓包过滤器：重点在动作，需要的包我才抓，不需要的我就不抓。

显示过滤器：重点在数据的展示，包已经抓了，只是不显示出来。

抓包过滤器在抓包前使用，它的过滤有一个基本的语法格式：BPF 语法格式。

BPF（全称 Berkeley Packet Filter），中文叫伯克利封包过滤器，它有四个核心元素：类型、方向、协议 和 逻辑运算符。

#### 抓包过滤器

1. 类型 Type：主机（host）、网段（net）、端口（port）
2. 方向 Dir：源地址（src）、目标地址（dst）
3. 协议 Proto：各种网络协议，比如：tcp、udp、http
4. 逻辑运算符：与（ && ）、或（ || ）、非（ ！）

四个元素可以自由组合，比如：

- src host 192.168.31.1：抓取源 IP 为 192.168.31.1 的数据包
- tcp || udp：抓取 TCP 或者 UDP 协议的数据包

#### 显示过滤器

1. IP 地址：ip.addr、ip.src、ip.dst
2. 端口：tcp.port、tcp.srcport、tcp.dstport
3. 协议：tcp、udp、http
4. 比较运算符：> < == >= <= !=
5. 逻辑运算符：and、or、not、xor（有且仅有一个条件被满足）

5 个核心元素可以自由组合，比如：

- ip.addr == 192.168.32.121：显示 IP 地址为 192.168.32.121 的数据包
- tcp.port == 80 ：显示端口为 80 的数据包

在过滤栏输入过滤语句，修改后立即生效。

![](https://files.mdnice.com/user/88172/8ef86c76-70bf-4ae8-8ec7-28b5e0d94c59.png)


#### 过滤器比较符号

![](https://files.mdnice.com/user/88172/17d660d8-640a-4e81-ade0-0016f3e4393a.png)

#### 常见过滤语法

- 对目的地址进行过滤

```bash
ip.dst == 192.168.0.1
```

- 如果想排除以上的数据包，只需要将其用括号囊括，然后使用 "!" 即可

```bash
!(ip.addr == 192.168.0.1)
```

- 对源地址进行过滤

```bash
ip.src == 192.168.0.1
```

- 请求的 uri 中包含"user"关键字的

```bash
http.request.uri matches "user"
```

- 过滤 http 请求方法

```bash
http.request.method=="POST"
```

- 过滤 http 响应状态码

```bash
http.response.code==302
```

- 过滤含有指定 cookie 的 http 数据包

```bash
http.cookie contains "userid"
```

### 数据包搜索

在 wireshark 界面按“Ctrl+F”，可以进行关键字搜索：

![](https://files.mdnice.com/user/88172/570a0518-a471-4bb1-82ca-5e7e5cf566b9.png)


Wireshark 的搜索功能支持正则表达式、字符串、十六进制等方式进行搜索，通常情况下直接使用字符串方式进行搜索。

![](https://files.mdnice.com/user/88172/463871a2-2fe6-4cca-88a3-90ba5ecf792e.png)


搜索栏的左边下拉，有分组列表、分组详情、分组字节流三个选项，分别对应 wireshark 界面的三个部分，搜索时选择不同的选项以指定搜索区域：


![](https://files.mdnice.com/user/88172/4ff78dce-31e0-4ec0-905c-a2a9d78a2d32.png)

![](https://files.mdnice.com/user/88172/746fcd72-1ce6-42fb-8876-839c5b1624fb.png)


### 数据包追踪

在 Wireshark 中，数据流追踪功能可以帮助我们将一个 TCP 或 UDP 连接中传输的数据按照时间顺序重新组合起来，从而让我们更清晰地看到数据的传输过程。通过 Wireshark 的数据包列表区，我们可以发现 Wireshark 捕获的流量是一个个的数据包片段，如果单独拿出每一个数据包进行分析，里边的字节流等信息是很难读懂的，这个时候我们就需要数据流追踪功能，将数据包进行重组，并完整的展现出来。

例如，在上传文件时，文件会被分割成多个数据包进行传输。通过数据流追踪，我们可以将这些分散的数据包重新组合起来，从而得到完整的文件内容。

目前这五种流可以被跟踪。他们分别是 TCP、UDP、SSL、HTTP、QUIC。

- TCP 流

重组使用 TCP 协议的数据，比如 HTTP 和 FTP。

- UDP 流

重组使用 UDP 协议的数据，比如 DNS。

- SSL 流

重组加密的协议，比如 HTTPS。你必须提供秘钥来解密流量。

- HTTP 流

从 HTTP 协议中重组和解压数据，当使用 TCP 流跟踪但又没有完全解码出的 HTTP 数据时，这个功能就派上用场了。

以一个简单的 HTTP 交互举例来说，在报文中单击一个 TCP 或者 HTTP 数据包:

![](https://files.mdnice.com/user/88172/2fdaaa5c-6ca7-4bad-af0a-bee862a39e3f.png)

右键单击这个文件并选择跟踪流。这时候 TCP 流就会在一个单独的窗口中显示出来。


![](https://files.mdnice.com/user/88172/b746e48a-8fa1-4bfa-b549-2ef79a94b3b4.png)

红色用来标明从源地址前往目标地址的流量。蓝色用来区分出相反方向，也就是从目标地址到源地址的流量。

例如:

以网站向服务器发送请求为例，首先浏览器会与服务器建立 TCP 连接。通过 TCP 三次握手进行连接。连接后通过 http 协议开始发送操作请求。首先浏览器所在的客户机向服务器发送请求报文 SYN，服务器接收到报文后，向客户机发送确认报文 SYN+ACK。客户机接收到确认报文后，再次向服务器发出 ACK 报文，确认已接收到确认报文，此时客户机与服务器之间的 TCP 连接建立完成，开始通信。发送 http 请求，如下图：

![](https://files.mdnice.com/user/88172/766b7b2f-4c00-42f4-b58a-27ede40007fd.png)


Wireshark 中数据流追踪的操作步骤

首先我们点击选择一条数据包，可以选择数据流，点击右键中的快捷键，追踪流-TCP 流。

![](https://files.mdnice.com/user/88172/46b1f699-d549-4043-a0ac-3cf170634c58.png)


在追踪数据流页面，红色代表请求信息（request）蓝色代表响应信息（response）。是将三个 TCP 数据包拼装成的可视化的展示。

![](https://files.mdnice.com/user/88172/42ddce75-ad83-4051-b5f5-8aee02ac40c3.png)


当然，对于 http 协议，也可以点击追踪流进行可视化的展示。点击 http 协议数据包，选择追踪流-http 流。

![](https://files.mdnice.com/user/88172/bcba8065-fd8d-4a0b-9200-135d8e9a38be.png)


最后总结一下数据流追踪功能，那就是将 TCP、UDP、SSL 等数据流进行重组并完整呈现出来。

![](https://files.mdnice.com/user/88172/c7649440-2e60-4df5-a635-8b115f72bd21.jpg)


上行流为红色，下行流为蓝色。可以在下拉菜单中选择同时显示上下行，或只选择单向流。支持以 ASCII 码、原始 16 进制、Hex 转储等编码方式显示数据。可以使用**查找栏**查找关键的值，选择显示原始数据时可查找 16 进制值，显示 ASCII 码时可查找字符串类型值。

### 数据包提取

Wireshark 支持提取通过 http 传输（上传/下载）、ftp、tcp 等协议传输的文件内容，方法如下：

自动提取通过 http 传输的文件内容

文件-> 导出对象->HTTP

![](https://files.mdnice.com/user/88172/786e05ad-b49d-4d97-b146-13632d3e6188.png)


在打开的对象列表中找到有价值的文件，如压缩文件、文本文件、音频文件、图片等，点击 `Save` 进行保存，或者 `Save All` 保存所有对象再进入文件夹进行分析。

![](https://files.mdnice.com/user/88172/1eefb814-b748-4bc0-90f7-ff85c02f6f30.png)


将所有 http 请求和响应体的数据进行导出。

### **分组字节显示**

右键特定字段，选择导出分组字节，可调出分组字节窗口。《显示为》 选项可选择编码方式，可以根据需求选择，然后导出该字段的所有字节。明文数据可以导出 ASCII 码。部分压缩文件可导出原始数据。 开始和结束也可以控制字节的大小。

![](https://files.mdnice.com/user/88172/91c3c88f-70ea-47d9-8ce0-e8918fb967ad.jpg)


# Tshark

wireshark 是一个伟大的网络问题分析工具，当然它也是有终端命令行工具的。tshark 就是 wireshark 的命令行之一。WireShark 的功能基本都有，还能组合 grep/awk 等编程处理分析抓包文件。

## 常用命令

```bash
-r 提取如wireshark表格中显示的封包摘要信息
```

![](https://files.mdnice.com/user/88172/7fc6f720-2908-4940-b6da-4a641aa5f97b.png)


```bash
-Y 使用filter过滤器
```

![](https://files.mdnice.com/user/88172/f8bde136-3b3e-44dc-85ff-9309f0942ccd.png)

```bash
-T 指出解析时输出的格式 
     默认text 
     fields (需要增加-e参数)
     其他选项 ek|json|jsonraw|pdml|ps|psml|tabs
-e 指定一个字段
```

![](https://files.mdnice.com/user/88172/c50123c6-4c96-4794-b741-de768a8a2673.png)


字段名可以通过 apply as column 应用为列

![](https://files.mdnice.com/user/88172/d267d2c9-0583-419d-9ee0-fb40ce73a673.png)


然后在列中右击，此时就可以看到我们想提取的字段对应的字段表达式
![](https://files.mdnice.com/user/88172/b9b58c54-7a3e-4451-9daf-ed95781fda29.png)


例如：我要提取 http 协议中每个请求的 uri。首先，找到 uri 的位置。

![](https://files.mdnice.com/user/88172/23f35007-409d-489d-a04f-12d3e3d33b71.png)


右击应用为列

![](https://files.mdnice.com/user/88172/2b61cf28-81d0-4637-adcf-c52a3165e98c.png)


在分组列表右键，可以看到 request uri 对应的表达式字典为 http.request.uri

![](https://files.mdnice.com/user/88172/6a270e12-a96e-428e-a5ec-60b687c26cb6.png)