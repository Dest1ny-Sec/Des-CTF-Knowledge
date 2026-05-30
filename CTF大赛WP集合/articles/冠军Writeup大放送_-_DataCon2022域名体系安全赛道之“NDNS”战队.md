# 冠军Writeup大放送 | DataCon2022域名体系安全赛道之“NDNS”战队

> 原文: https://www.ctfiot.com/92019.html
> ID: 92019

由奇安信集团、清华大学网络研究院、蚂蚁集团、腾讯安全大数据实验室、Coremail论客主办的DataCon2022大数据安全分析竞赛线上赛和决赛已圆满落幕，五大赛道第一名也已各归其主。今天要为大家分享的是域名体系安全赛道排名第一的NDNS战队writeup。

来自国防科技大学DNSLab的NDNS战队组建于2021年，指导老师是许成喜老师。NDNS战队依托国防科技大学网络空间测绘科研团队，主要成员为国防科技大学在读硕博士研究生，关注互联网基础设施安全及测量、网络黑产检测等领域的前沿技术与研究。成员们主要研究方向为DNS安全、黑灰产检测及异常检测、网络空间测绘、机器学习、数据挖掘等。NDNS战队曾获DataCon2021 域名体系安全第二名、2021强网杯人工智能挑战赛口令猜解第二名。

[温馨提示：本文篇幅较长欢迎收藏转发，随时浏览查看]

【赛题要求】

本次比赛域名体系安全中设置了两个题目，域名分类和域名接管。

域名分类：选手需要根据域名的解析规律和访问规律识别并分类出 CDN 及其他种类域名。选手需要了解 DNS 的基础知识和常见域名种类的特点，并能够推断总结出其解析和访问规律，据此实现域名分类识别。

域名接管：选手需要通过在既定靶场中通过域名接管、DNS 污染等攻击方式，在靶场中接管指定的域名从而获取靶场中的 FLAG。

第一部分 域名分类

一、背景知识

域名是网络攻击中必不可少的数字资源，基于域名的安全风险分析研究可以快速的发现和阻断威胁活动。在域名体系安全研究中，针对不同的域名应用场景，安全研究人员对域名进行分类，以便更好的对特定分类域名的行为特征进行分析，也有利于过滤非目标的流量数据。赛题中的分类主要包括：

1. CDN 域名

CDN 全称为内容分发网络，其目的是解决因分布、带宽、服务器性能带来的访问延迟问题，常用于站点加速、点播、直播等场景。可以使用户可就近取得所需内容，解决 Internet 网络拥挤的状况，提高用户访问网站的响应速度和成功率。

CDN 域名指提供 CDN 服务厂商的域名。在实现上，CDN 通常使用域名系统中的 CNAME 记录，将用户的域名 CNAME 到服务商的域名，当用户向源站发起请求时，DNS 服务器解析源站域名时会发现有 CNMAE 记录，这时 DNS 服务器会向 CNAME 域名发起请求，请求会被调度至加速节点的域名。

2. 动态域名

域名的映射关系一般是预先配置好的，但对于一些没有固定 IP 地址场景是无法进行配置。而动态域名可以将任意变换的 IP 地址绑定一个固定的域名，实现了 IP 变换场景下的域名 IP 映射。实现方式通常是利用客户端的软件将本机的 IP 发送至动态域名解析服务器或者某些路由器直接支持动态域名的配置。目前国内支持动态域名的厂商包括花生壳、3322、dnspod、aliyun 以及 huaweicloud 等。

3. 隐藏类型域名

根据提示，我们推断赛题中的隐藏类型域名为 GFW 的监管域名。

4. Sinkhole

当发现恶意软件中所使用的域名后，为了避免后续感染恶意软件的受害者再受到攻击，研究者通常将恶意域名接管至特定的地址，该地址被称为 sinkhole，常见的接管方式是修改恶意软件域名的 NS 记录，将其设置为研究者自己控制的某个 DNS 服务器。

5. Domain Parking

域名停放是将暂时不用的域名或者待出售的域名，托管至域名停放服务商处，由服务商展示统一的广告或者售卖页面，以赚取广告流量费用或者售卖。

6. Webhosting（免费建站）

为方便普通用户部署 web 站点，服务商推出方便 web 托管服务器，可以为用户提供子域名及主机资源，常见的服务商包括 000Webhost、Alwaysdata、freewha、ProFreeHost、FASTLY、Wix.com、SQUARESPACE 等。

7. p2p

对 p2p 不太了解，这里认为是 p2p 网络中所使用的域名。

8. FastFlux

FastFlux 是恶意软件中为了躲避检测而使用的一种技术，最早发现于 2006 年的 storm worm。Flux Fast 最大的特征之一在于频繁改变其域名、IP 地址和名称服务器。

二、域名特性分析及判定指标

根据对每种类型域名的应用场景和使用特性进行分析，总结其解析行为特征，因为比赛中仅找出了 5 种类型的域名，且后动态域名的效果并不好。对于为找出的 3 种类型域名的分析可能有待矫正。下图展示了我们所分析和使用的指标，绿色对号表示我们最终使用的指标。

● CDN 域名
    ○ 具有大量的 CNAME 记录，服务商的 SLD 下具有大量的 FQDN，IP 数量多，地理分布广泛（这个特征再比赛数据中并不明显）
    ○ 判定指标：SLD 的 CNAME 记录数大于 N（100），解析 IP 地理位置数量大于 M（0/2）

● 隐藏类型域名
    ○ 推测为监管域名，根据已有研究[1]，监管域名的响应记录由两个特性
        ■ 响应 IP 的 AS 信息比较集中，常见为 Google，Twitter，Facebook 和 Dropbox
           ■ 响应 IP 的数量有限
    ○ 判定指标：IP ASO 为以上四种，且每个 IP 解析域名数量大于 14W。

● 动态域名
    ○ 具有较多子域名，每个子域名解析的 IP 不固定

● Domain Parking
    ○ parking 服务商较集中，一个 IP 解析大量域名，且统一服务商的对每个域名的解析策略是一致的，如对任何 parked 域名响应 12 个IP
    ○ 判定指标：单个 IP 解析域名大于 N，为特定的 parking 服务商，且解析策略一致

● webhosting
    ○ 服务商较集中，具有大量子域名，单一 IP 解析大量的 FQDN，取决于服务商大小，IP 数量有限
    ○ 判定指标：单个 IP 解析域名大于 N，特定的 hosting 服务商

● sinkhole（未发现）
    ○ sinkhole 的 IP 数量有限，可能一个 IP 解析大量的恶意域名

● p2p（未发现）
    ○ 单一域名解析多个 IP 地址

● fastflux（未发现）
    ○ 单一域名解析大量 IP 地址，同时每个 IP 上解析量分布是均匀的

三、赛题解答

数据处理

1. 遍历所有 CNAME 记录中的 SLD，统计 SLD 对应的 CNAME 解析记录数量。

import csvimport osSLD_Ccount = {}
i=0file_names = os.listdir('./datacon_cdn_basic')for file_name in file_names: i+=1 file_path = os.path.join('./datacon_cdn_basic',file_name) print('Processing with '+ str(i) +' file!') with open(file_path, encoding='utf-8-sig') as f: f_csv = csv.reader(f) #headers = next(f_csv) #headers:['sld_md5', 'all_md5_fqdn', 'request_cnt', 'rtype', 'all_md5_rdata', 'country_code', 'country_name', 'region_name', 'asn_sort'] #['86f066f08908de0c617243cb33081050', '2ddfe6b1ebd12b3d1807eff0274d883c.86f066f08908de0c617243cb33081050', '1', '5', 'ccd4d6df14af7f4215db6b77945fc02a.95074d472f19c7108ee72233cd65f543', 'null', 'null', 'null', '0'] for row in f_csv: if row[3]=='5': if row[4]: sld = row[4].split('.')[-1] if sld in SLD_Ccount: SLD_Ccount[sld] += 1 else: SLD_Ccount[sld] = 1
SLD_Ccount_sorted = dict(sorted(SLD_Ccount.items(), key=lambda x: x[1], reverse=True))
file1 = open('./mydata/SLD_Ccount_sorted.csv', 'w')writer = csv.writer(file1)count_all = 0for k,v in SLD_Ccount_sorted.items(): writer.writerow([k,v]) count_all += vprint(count_all) print('Success!')#共 29581826 条 CNAME 记录

2. 统计 SLD 的所有 FQDN 数量。

import csvimport os
CDN_list1 = []CDN_fqdn_count = {}fqdn_count = {}
with open('./mydata/SLD_Ccount_sorted.csv', encoding='utf-8-sig') as f: f_csv = csv.reader(f) for row in f_csv: #if int(row[1]) >= 397: CDN_list1.append(row[0])
for sld in CDN_list1: CDN_fqdn_count[sld] = 0
i=0file_names = os.listdir('./datacon_cdn_basic')for file_name in file_names: i+=1 file_path = os.path.join('./datacon_cdn_basic',file_name) print('Processing with '+ str(i) +' file!') with open(file_path, encoding='utf-8-sig') as f: f_csv = csv.reader(f) for row in f_csv: sld = row[0] if sld in CDN_list1: fqdn = row[1] if fqdn in fqdn_count: fqdn_count[fqdn] += 1 else: fqdn_count[fqdn] = 1 CDN_fqdn_count[sld] += 1
CDN_fqdn_count_sorted = dict(sorted(CDN_fqdn_count.items(), key=lambda x: x[1], reverse=True))
file1 = open('./mydata/CDN_fqdn_count_sorted.csv', 'w')writer = csv.writer(file1)count_all = 0for k,v in CDN_fqdn_count_sorted.items(): writer.writerow([k,v]) count_all += vprint(count_all) print('Success!')

3. 统计 FQDN 的解析 IP 分布，即：统计 FQDN 对应的 A 记录地区分布及数量。

import csvimport os
CDN_list1 = []fqdn_region_list = {}fqdn_region_count = {}
with open('./mydata/SLD_Ccount_sorted.csv', encoding='utf-8-sig') as f: f_csv = csv.reader(f) for row in f_csv: CDN_list1.append(row[0])#print(CDN_list1)i=0file_names = os.listdir('./datacon_cdn_basic')for file_name in file_names: i+=1 file_path = os.path.join('./datacon_cdn_basic',file_name) print('Processing with '+ str(i) +' file!') with open(file_path, encoding='utf-8-sig') as k: k_csv = csv.reader(k) for row in k_csv: if row[3]=='1': sld = row[0] if sld in CDN_list1: fqdn = row[1] region = row[7] if fqdn in fqdn_region_list: if region in fqdn_region_list[fqdn]: pass else: fqdn_region_list[fqdn].append(region) else: fqdn_region_list[fqdn] = [region]
for k,v in fqdn_region_list.items(): fqdn_region_count[k]=len(v)fqdn_region_count_sorted = dict(sorted(fqdn_region_count.items(), key=lambda x: x[1], reverse=True))
file1 = open('./mydata/fqdn_region_count_sorted.csv', 'w')writer = csv.writer(file1)for k,v in fqdn_region_count_sorted.items(): writer.writerow([k,v]) print('Success!')

4. 将 FQDN 的地区分布情况进行合并，得到 SLD 的地区分布情况及数量。

import csvsld_region_list = {}sld_region_count = {}for k,v in fqdn_region_list.items(): sld = k.split('.')[-1] if sld in sld_region_list: for _ in v: if _ in sld_region_list[sld]: pass else: sld_region_list[sld].append(_) else: sld_region_list[sld] = vfor k,v in sld_region_list.items(): sld_region_count[k]=len(v) sld_region_count_sorted = dict(sorted(sld_region_count.items(), key=lambda x: x[1], reverse=True)) 
file1 = open('./mydata/sld_region_count_sorted.csv', 'w')writer = csv.writer(file1)for k,v in sld_region_count_sorted.items(): writer.writerow([k,v]) print('Success!')

5. 提取非 CNAME 记录相关的 FQDN 的 IP 统计信息。

cdn_name_path = "./mydata_level2/SLD_CNAME_count_sorted.csv"fp = open(cdn_name_path,"r")cdns = fp.readlines()cdns = [ci.split(",")[0] for ci in cdns][:200]fp.close()
file_names = os.listdir('./cdn_level2/datacon_cdn_ad')# fo = open("./mydata_level2/level2_sld_geo_data.txt","w")sld_dict = {}for file_name in tqdm(file_names): file_path = os.path.join('./cdn_level2/datacon_cdn_ad',file_name) with open(file_path,"r") as fp: for line in fp: if line.startswith("sld,md5_fqdn"): continue line = line.strip().split(",") try: if line[3]=="5" and (line[0] in cdns or ".".join(line[4].split(".")[1:]) in cdns): continue except Exception as e: print(e) pass
 if line[0] not in sld_dict: sld_dict[line[0]] = [0,0,0,0,set(),set(),set()]# FQDN, A,CNAME, 被 CNAME, geo，IP,ASO if line[3]=="5": sld_dict[line[0]][2] += 1 if ".".join(line[4].split(".")[1:]) not in sld_dict: sld_dict[".".join(line[4].split(".")[1:])] = [0,0,0,0,set(),set(),set()] sld_dict[".".join(line[4].split(".")[1:])][3] += 1
 if line[3]=="1" and line[0] != line[1]: sld_dict[line[0]][0] += 1 sld_dict[line[0]][4].update([line[10]]) sld_dict[line[0]][5].update([line[4]]) sld_dict[line[0]][6].update([line[6]]) if line[3]=="1" and line[0] ==line[1]: sld_dict[line[0]][1] += 1 sld_dict[line[0]][4].update([line[10]]) sld_dict[line[0]][5].update([line[4]]) sld_dict[line[0]][6].update([line[6]])

sld_dict_sorted = dict(sorted(sld_dict.items(), key=lambda x: x[1], reverse=True)) 
fo = open("./mydata_level2/sld_fqdn_a_canme_r_ip_aso.txt","w")
for key in tqdm(sld_dict_sorted): fo.write(",".join([key]+list(map(str,sld_dict_sorted[key][:4]+[len(sld_dict_sorted[key][4])]+[len(sld_dict_sorted[key][5])]+[len(sld_dict_sorted[key][6])])))+"n")fo.close()

6. 统计每个 IP 解析的域名数量，并标记判定类别。

# step 统计每个 IP 的解析域名的数量，并标记已知的类别fp = open("./mydata_level2/level2_sld_geo_data.txt","r")cdn_ips = {}hidden_ips = {}other_ips = {}for line in tqdm(fp): line = line.split(",") if line[0] in bloom_cdn: if line[1] not in cdn_ips: cdn_ips[line[1]] = 1 else: cdn_ips[line[1]] += 1 elif line[0] in bloom_hidden: if line[1] not in hidden_ips: hidden_ips[line[1]] = 1 else: hidden_ips[line[1]] += 1 else: if line[1] not in other_ips: other_ips[line[1]] = 1 else: other_ips[line[1]] += 1
fo = open("./mydata_level2/all_ip_count.txt","w")
cdn_ips_sorted = dict(sorted(cdn_ips.items(), key=lambda x: x[1], reverse=True)) hidden_ips_sorted = dict(sorted(hidden_ips.items(), key=lambda x: x[1], reverse=True)) other_ips_sorted = dict(sorted(other_ips.items(), key=lambda x: x[1], reverse=True))
for key in cdn_ips_sorted: fo.write(key+","+str(cdn_ips_sorted[key])+","+"1"+"n")for key in hidden_ips_sorted: fo.write(key+","+str(hidden_ips_sorted[key])+","+"2"+"n")for key in other_ips_sorted: fo.write(key+","+str(other_ips_sorted[key])+","+"0"+"n")fo.close()

域名类型判定

● CDN
○ 取SLD的CNAME 记录数大于 100，解析IP地理位置数量大于 0，level 1 得分：100
○ 取SLD的CNAME 记录数大于 100，解析IP地理位置数量大于 2，level 2 得分：22

● 隐藏类型
○ IP ASO 为以上四种，且每个 IP 解析域名数量大于 14W， 得分：24

import osfrom tqdm import tqdmfrom pybloom_live import ScalableBloomFilter, BloomFilter# step 0 提取特定 ASO 信息的 IP 地址# step 1 统计每个 IP 解析的 FQDN 数fp = open("./answer/cdn_level2/result.txt","r")hdomains = fp.readlines()hdomains = [hi.strip().split("t")[1] for hi in hdomains]print(hdomains[9])file_names = os.listdir('./cdn_level2/datacon_cdn_ad')
ip_dict = {}
for file_name in tqdm(file_names): file_path = os.path.join('./cdn_level2/datacon_cdn_ad',file_name) with open(file_path,"r") as fp: for line in tqdm(fp): if line.startswith("sld,md5_fqdn"): continue line = line.strip().split(",") if line[3]=="5": continue if line[3] == "1" and line[0] in hdomains: if line[4] not in ip_dict: ip_dict[line[4]] = 0 ip_dict[line[4]] += 1

ip_dict_sorted = dict(sorted(ip_dict.items(), key=lambda x: x[1], reverse=True))
fo = open("./mydata_level2/hidden_ip_fqdn_count_sorted.txt","w")
for key in ip_dict_sorted: fo.write(key+","+str(ip_dict_sorted[key])+"n")fo.close()

# step 2 取前 591 个 IP，这些 IP 每个平均解析了 14 万的域名，找出其解析过的 SLDfp = open("./mydata_level2/hidden_591.ip","r")hips = fp.readlines()hips = [hi.strip() for hi in hips]
file_names = os.listdir('./cdn_level2/datacon_cdn_ad')
sld_dict = set()
for file_name in tqdm(file_names): file_path = os.path.join('./cdn_level2/datacon_cdn_ad',file_name) with open(file_path,"r") as fp: for line in tqdm(fp): if line.startswith("sld,md5_fqdn"): continue line = line.strip().split(",") if line[3]=="5": continue if line[3] == "1" and line[4] in hips: sld_dict.update([line[0]])
fo = open("./mydata_level2/hidden_ip_591_to_sld.txt","w")for si in list(sld_dict):    fo.write(si+"n")

● domain parking，webhosting 和动态域名
○ 统计每个 IP 解析的域名数量，及 SLD 的 QFDN 数量，之后进行服务商的判定
○ domain parking 和 webhosting 设定每个 IP 解析域名数量大于 1000
○ 动态域名设定每个 IP 的解析域名小于 3 个，且对应 SLD 的 FQDN 数量大于 20，同时收集动态域名列表进行匹配[2]
○ 得分：9

# webhosting provider["Dreamscape Networks Limited", "BIZLAND-SD", "Cizgi Telekomunikasyon Anonim Sirketi","Marcin Waligorski Greener", "Namesco Limited","Register S.p.A.","Host Europe GmbH", "AUTOMATTIC","InterNetX GmbH", "WEBAIR-INTERNET","Strato AG","FASTLY","LIQUIDWEB","WEEBLY","BIZLAND-SD","Wix.com","SQUARESPACE","Trellian Pty. Limited"]# domain parking["Linode","SEDO GmbH","BODIS-NJ","CONFLUENCE-NETWORK-INC","CENTURYLINK-LEGACY-SAVVIS","IONOS SE","UK-2 Limited"]

第二部分 域名接管

一、背景知识

子域名接管漏洞

子域名接管漏洞是指注册一个不存在或已被注销的域名，来获得另一个目标域名控制权的过程。以最常见的 CNAME 子域名接管为例：

1. 域名A有一个子域名（sub.abc.com ）的 CNAME 记录解析到另一个域的域名B（secrank.net ）.

2. 后来，域名 B 由于未及时续费等原因到期，此时任何人可以公开注册。

3. 而A的 CNAME 记录没有被从 域名A的区域中删除，导致攻击者注册 B 的域名，即可完成对域名 A 子域名的劫持，控制域名 A子域名 的内容，直到该记录被删除掉。

子域名接管造成的危害十分广泛:

1. 从合法域名发起鱼叉式网络钓鱼攻击

2. 利用被接管域名流量投放广告

3. 执行跨站脚本攻击

4. 破坏域内其他网站内容的声誉和形象

5. 攻击者窃取他人的知识产权

子域名接管漏洞还可能存在于 NS/MX/A 记录下，会产生更多安全隐患，因此子域名接管攻击方法的研究是十分值得重视的。

其他相关知识

DNS 缓存投毒

DNS缓存投毒是指通过恶意篡改DNS解析服务器中的缓存记录，使得用户解析到错误的IP地址。域名解析流程中为避免一个域名的重复查询，通过域名的TTL控制域名的缓存到期时间，未到期前，DNS 解析器使用缓存的记录响应解析请求。

攻击者通过发起针对特定域名的请求，并正确的响应返回之前，发送大量的伪造响应，服务器端将有可能将伪造的结果缓存下来，导致错误的解析。比较著名的攻击方式是 Kaminsky 攻击。不过攻击的难易程度和方法也与服务器的具体实现逻辑有关系。目前常见的防范缓存投毒的方法是部署TXID和源端口随机化，还有其他方案，如0x20。

DNS 缓存中毒的长期解决方案是 DNSSEC。DNSSEC 允许组织使用公钥加密签署他们的 DNS 记录，但DNSSEC的部署推进仍不理想。

缓存投毒攻击[3]

域名归属权验证机制

本次比赛中主要的问题是CDN在进行域名托管时的域名归属权验证问题。在用户配置域名时应验证其是否是域名的所有者，赛题正是不同场景下不合理的域名归属权验证机制的复现。

通过 DNS 解析验证来验证域名归属权是较为常用的一种方法，通过设置特定的TXT记录证明域名为本人所有。

此外，还有不同服务商还提供文件验证(服务商亲自访问目录下验证文件)[4]和 API 验证方法。

DMARC 邮件安全协议

DMARC，全称为Domain-based Message Authentication，Reporting and Conformance，是一类电子邮件安全协议，一般和 DKIM 和 SPF 一同使用。用于确认当前邮件来源是否合法，需要使用者在 _dmarc 或 dmarc 子域名  TXT 记录下设置如下内容:

v=DMARC1; p=none; fo=1; ruf=mailto:xxx@xxxxxx.com; rua=mailto:xxx@xxxxxx.com

其中和本题目相关的，rua：用于接收收件方对该来源邮件检测完毕后，生成的汇总报告。因此可以通过探测该类的子域名解析记录，找到疑似的 CDN 平台管理员账户.

工具

● 一台公网 HTTP 服务器
● 一台公网 DNS 服务器

基本思路

域名接管的五道题，容器都连通外网，因此在适当条件下，外部的 DNS 可以参与解析，但本地解析均在容器内进行，经测试存在 DNS 缓存、CDN 服务平台、本地 DNS，和题目相关的网站记录均在本地 DNS 内。

题目基础解题模式相同，主要分为以下步骤：

1. 注册 CDN 平台账号（主要包含邮箱和用户名）

2. 使用平台登记 CNAME 和 A 记录，使得 datacon2022.secrank.cn间接指向有HTTP服务的攻击者个人IP，本文关于这里的设置全部统一，因此不再重复此图。

3. 使用某种方式（这是五道题的差异化考点），使得归属权验证成功（题目通过查询被接管网站 TXT 记录验证归属权），获得在该 CDN 下域名的归属权，使得被接管网站借由 CDN 服务，在平台服务范围（本题为该容器内）被解析到攻击者 IP。

4. 在/flag下验证 Key 值，它将访问 datacon2022.secrank.cn，接管成功后，则实际访问位于外网的攻击者 IP 下的 HTTP 服务，将 80 端口主页面内容修改为其指定KEY值，完成对接管情况的验证。

5. 成功则获得 flag。

【level1】

分析

第一题较为简单，CDN 平台对网站接管，没有任何验证逻辑，将 datacon2022.secrank.cn 作为自定义域名，攻击者 IP 作为目的 IP，即可直接接管。

解题过程

注册账号，邮箱、用户名不受限制，试着查询 datacon2022.secrank.cn. 的 A 记录，CNAME 记录未注销，存在接管风险。

;; QUESTION SECTION: ;datacon2022.secrank.cn. IN A
 ;; ANSWER SECTION: datacon2022.secrank.cn. 30  IN  CNAME   admin.datacon.cdn.

登记 CDN 记录，直接设置 CDN 记录，即可接管。

最后修改并验证 HTTP 页面的指定KEY值，获得 flag。

【level2】

分析

增加了 TXT 记录的验证，需要在目标域名的区域文件中设置特定的 TXT ，但目标域名下的 TXT 记录在注销后未被删除，存在利用风险。

且对 datacon2022.secrank.cn 生成的验证码固定（经测试与用户名、邮箱均无关，只与顶级、二级域名相关），形成了验证漏洞。

解题过程

注册账号，邮箱、用户名不受限制，试着查询 datacon2022.secrank.cn. 的 A、TXT 记录，发现 CNAME 记录未注销，且 TXT 记录也未注销（且与归属权验证所需验证码相同），存在接管风险。

;; ANSWER SECTION: datacon2022.secrank.cn. 30 IN CNAME admin.datacon.cdn. ;; ANSWER SECTION: secrank.cn.     60  IN  TXT "5ca162f89d93a4e7e5661a4b290b6d33"

要接管的子域名的 CNAME 解析为 admin.datacon.cdn.，直接设置 CDN 记录，即可完成验证。

最后修改并验证 HTTP 页面的指定KEY值，获得 flag。

【level3】

分析

本题提示：admin 的用户为 admin@secrank.cn，且已被注销。

在 CDN 服务登记 CDN 的 CNAME 和 A 记录时会产生一个归属权验证码，用于验证用户的归属权，将该验证码登记在被服务的二级域名的TXT中即可生效。本题中 secrank.cn 未删除原来的 TXT 记录。

经对照测试，该验证码的生成不随次数改变而随机产生，且与用户名和邮箱高度相关，猜测为拼接后 MD5 求取散列，根据实验结果猜测格式为 md5(‘固定值+邮箱+用户名+自定义域名的etld+固定值’) ，因此直接按照提示注册 admin@secrank.cn 账号即可。

解题过程

注册账号，有限制，邮箱和用户名必须为 admin@secrank.cn 和 admin。
查询 datacon2022.secrank.cn 的 A 记录、secrank.cn 的 TXT 记录，情况如下：

;; ANSWER SECTION: datacon2022.secrank.cn. 30 IN CNAME admin.datacon.cdn. ;; ANSWER SECTION: secrank.cn.     60  IN  TXT "fdf82d037bff4fbb42495e6232c1d7f3"

重置环境不变，说明 md5 是使用了固定的加盐值（也可能没有加盐），和某些固定参数计算出来的。

域名归属权验证码生成规则的猜测（以下为部分对照）

secrank.cn TXT e1f6c5df7297f459d2eae4783361613a

secrank.cn TXT 982a0de018edf5bf12d042284629106a

secrank.cn TXT fdf82d037bff4fbb42495e6232c1d7f3

secrank.cn TXT fdf82d037bff4fbb42495e6232c1d7f3

secrank.cn TXT fdf82d037bff4fbb42495e6232c1d7f3

上述及其他测试结果，表明生成 归属权验证码 MD5值的原字符串至少包含了：

● CDN 服务 注册用户名
● CDN 服务 注册邮箱
● CND 服务 自定义域名的etld
可能存在
● 固定盐值（可能每道题不同）
● 且该值和以下值无关
● 自定义域名的三级域名
● 提供 CDN 服务的子域名
● 生成时间等变化参数

第三题中原用户注册的 CDN 账户为 admin admin@secrank.cn ，因此只有使用该用户名才能产生正确的 md5（且不随机），原来的网站的 TXT 未被注销，造成验证漏洞，使用特定账户即可产生特定的验证码。

建立用户成功后

datacon2022.secrank.cn. 30 IN CNAME admin.datacon.cdn. admin.datacon.cdn.  3600    IN  A   xxx.xxx.xxx.xxx(IP)

将目标网站主页面编辑为对应的 Key 值，即可验证接管，获得 flag。

【level4】

分析

解题过程

首先注册任意账号，查询 secrank.cn 域 的验证码 TXT 记录，且存在 DMARC 协议 TXT 记录，经测试该记录的 rua 参数下的邮箱被注册为 CDN 用户，猜测为管理员账号。

_verify.secrank.cn. 86400 IN TXT "f3c5e853dbd3c50b66d1545aaa074b86" _dmarc.secrank.cn.  86400   IN  TXT "v=DMARC1; p=quarantine; rua=mailto:da1ef3b3@secrank.cn"

以第三题对MD5 的归属权验证码生成规则的对照测试结果为标准，在被攻击域名 datacon2022.secrank.cn 不变的条件下，猜测 MD5 生成规则为固定数据+邮箱+用户名+固定数据的形式，顺此思路，针对 da1ef3b3@secrank.cn + da1ef3b3 的组合注册如下账号：

邮箱：da1ef3b3@secrank.c用户名：nda1ef3b3

发现生成的归属权验证码，与 DIG 查询 _verify.secrank.cn 的TXT结果一致，因此MD5生成方法 假设基本正确。修改攻击机的 DNS 主页面 KEY，对网站进行接管验证，得到 flag。

【level5】

分析

本题目与前面题目的不同在于，可以指定解析用 DNS 服务器，且在对服务器的具体实现逻辑的测试中，发现缓存服务器会将该解析（对指定 DNS 服务器）的结果直接缓存，存在缓存污染风险。

解题过程

首先，使用任意帐号登记 datacon2022.secrank.cn 的 CDN 服务，获得一个待验证的归属权验证码 b6406817af968a444aa934fc2e0c6f3f ，使用它在攻击者 DNS 服务器设置伪造 _verify.secrank.cn TXT 记录，指定CDN平台提供的 DIG 工具(指定攻击者 DNS 服务器IP)查询_verify.secrank.cn 的 TXT 记录，使其缓存伪造的TXT记录。

$TTL 1D @ IN SOA _verify.secrank.cn. rname.invalid. ( 0 ; serial 1D ; refresh 1H ; retry 1W ; expire 3H ) ; minimum NS _verify.secrank.cn. A xxx.xxx.xxx.xxx(攻击者 DNS IP 地址) AAAA ::1     TXT "b6406817af968a444aa934fc2e0c6f3f"

使用本地DNS服务器再次查询TXT记录，确认缓存污染完毕，完成归属权验证。

修改攻击机的 DNS 主页面 KEY，对网站进行接管验证，得到 flag。

总结反思

域名分类题目展示了为维护域名系统的安全，研究人员将域名划分为不同的类型，扩展了我们对域名的认识，同时也展示了Passive DNS数据在域名体系安全中的威胁挖掘能力。域名接管则展示了域名系统对现代互联网应用的支撑，同时展示了在应用时可能存在的安全风险。我们认为风险主要包括：

● CDN或者域名托管验证的必要性，用户体验与安全性的平衡
● 服务过期后，历史记录如何处理的问题
● 验证逻辑的完善性
● 验证码的强度问题，与用户信息相关，但也应该加入随机因素
● DNS服务器解析流程的缓存策略问题

参考文献

[1] Hoang N P, Niaki A A, Dalek J, et al. How Great is the Great Firewall? Measuring China’s {DNS} Censorship[C]//30th USENIX Security Symposium (USENIX Security 21). 2021: 3381-3398.

[2]https://gist.githubusercontent.com/neu5ron/8dd695d4cb26b6dcd997/raw/5c31ae47887abbff76461e11a3733f26bddd5d44/dynamic-dns.txt

[3] https://blog.csdn.net/weixin_44604541/article/details/115916484

[4] https://help.aliyun.com/document_detail/169377.html

【往期回顾】

添加DataCon小助手微信微信号：DataConofficial获取更多大数据安全知识进群还有超多活动、福利DataCon定制服饰、背包等精彩好礼等你来拿！


```
import csvimport osSLD_Ccount = {}
i=0file_names = os.listdir('./datacon_cdn_basic')for file_name in file_names: i+=1 file_path = os.path.join('./datacon_cdn_basic',file_name) print('Processing with '+ str(i) +' file!') with open(file_path, encoding='utf-8-sig') as f: f_csv = csv.reader(f) #headers = next(f_csv) #headers:['sld_md5', 'all_md5_fqdn', 'request_cnt', 'rtype', 'all_md5_rdata', 'country_code', 'country_name', 'region_name', 'asn_sort'] #['86f066f08908de0c617243cb33081050', '2ddfe6b1ebd12b3d1807eff0274d883c.86f066f08908de0c617243cb33081050', '1', '5', 'ccd4d6df14af7f4215db6b77945fc02a.95074d472f19c7108ee72233cd65f543', 'null', 'null', 'null', '0'] for row in f_csv: if row[3]=='5': if row[4]: sld = row[4].split('.')[-1] if sld in SLD_Ccount: SLD_Ccount[sld] += 1 else: SLD_Ccount[sld] = 1
SLD_Ccount_sorted = dict(sorted(SLD_Ccount.items(), key=lambda x: x[1], reverse=True))
file1 = open('./mydata/SLD_Ccount_sorted.csv', 'w')writer = csv.writer(file1)count_all = 0for k,v in SLD_Ccount_sorted.items(): writer.writerow([k,v]) count_all += vprint(count_all) print('Success!')#共 29581826 条 CNAME 记录
```



```
import csvimport os
CDN_list1 = []CDN_fqdn_count = {}fqdn_count = {}
with open('./mydata/SLD_Ccount_sorted.csv', encoding='utf-8-sig') as f: f_csv = csv.reader(f) for row in f_csv: #if int(row[1]) >= 397: CDN_list1.append(row[0])
for sld in CDN_list1: CDN_fqdn_count[sld] = 0
i=0file_names = os.listdir('./datacon_cdn_basic')for file_name in file_names: i+=1 file_path = os.path.join('./datacon_cdn_basic',file_name) print('Processing with '+ str(i) +' file!') with open(file_path, encoding='utf-8-sig') as f: f_csv = csv.reader(f) for row in f_csv: sld = row[0] if sld in CDN_list1: fqdn = row[1] if fqdn in fqdn_count: fqdn_count[fqdn] += 1 else: fqdn_count[fqdn] = 1 CDN_fqdn_count[sld] += 1
CDN_fqdn_count_sorted = dict(sorted(CDN_fqdn_count.items(), key=lambda x: x[1], reverse=True))
file1 = open('./mydata/CDN_fqdn_count_sorted.csv', 'w')writer = csv.writer(file1)count_all = 0for k,v in CDN_fqdn_count_sorted.items(): writer.writerow([k,v]) count_all += vprint(count_all) print('Success!')
```



```
import csvimport os
CDN_list1 = []fqdn_region_list = {}fqdn_region_count = {}
with open('./mydata/SLD_Ccount_sorted.csv', encoding='utf-8-sig') as f: f_csv = csv.reader(f) for row in f_csv: CDN_list1.append(row[0])#print(CDN_list1)i=0file_names = os.listdir('./datacon_cdn_basic')for file_name in file_names: i+=1 file_path = os.path.join('./datacon_cdn_basic',file_name) print('Processing with '+ str(i) +' file!') with open(file_path, encoding='utf-8-sig') as k: k_csv = csv.reader(k) for row in k_csv: if row[3]=='1': sld = row[0] if sld in CDN_list1: fqdn = row[1] region = row[7] if fqdn in fqdn_region_list: if region in fqdn_region_list[fqdn]: pass else: fqdn_region_list[fqdn].append(region) else: fqdn_region_list[fqdn] = [region]
for k,v in fqdn_region_list.items(): fqdn_region_count[k]=len(v)fqdn_region_count_sorted = dict(sorted(fqdn_region_count.items(), key=lambda x: x[1], reverse=True))
file1 = open('./mydata/fqdn_region_count_sorted.csv', 'w')writer = csv.writer(file1)for k,v in fqdn_region_count_sorted.items(): writer.writerow([k,v]) print('Success!')
```



```
import csvsld_region_list = {}sld_region_count = {}for k,v in fqdn_region_list.items(): sld = k.split('.')[-1] if sld in sld_region_list: for _ in v: if _ in sld_region_list[sld]: pass else: sld_region_list[sld].append(_) else: sld_region_list[sld] = vfor k,v in sld_region_list.items(): sld_region_count[k]=len(v) sld_region_count_sorted = dict(sorted(sld_region_count.items(), key=lambda x: x[1], reverse=True)) 
file1 = open('./mydata/sld_region_count_sorted.csv', 'w')writer = csv.writer(file1)for k,v in sld_region_count_sorted.items(): writer.writerow([k,v]) print('Success!')
```



```
cdn_name_path = "./mydata_level2/SLD_CNAME_count_sorted.csv"fp = open(cdn_name_path,"r")cdns = fp.readlines()cdns = [ci.split(",")[0] for ci in cdns][:200]fp.close()
file_names = os.listdir('./cdn_level2/datacon_cdn_ad')# fo = open("./mydata_level2/level2_sld_geo_data.txt","w")sld_dict = {}for file_name in tqdm(file_names): file_path = os.path.join('./cdn_level2/datacon_cdn_ad',file_name) with open(file_path,"r") as fp: for line in fp: if line.startswith("sld,md5_fqdn"): continue line = line.strip().split(",") try: if line[3]=="5" and (line[0] in cdns or ".".join(line[4].split(".")[1:]) in cdns): continue except Exception as e: print(e) pass
 if line[0] not in sld_dict: sld_dict[line[0]] = [0,0,0,0,set(),set(),set()]# FQDN, A,CNAME, 被 CNAME, geo，IP,ASO if line[3]=="5": sld_dict[line[0]][2] += 1 if ".".join(line[4].split(".")[1:]) not in sld_dict: sld_dict[".".join(line[4].split(".")[1:])] = [0,0,0,0,set(),set(),set()] sld_dict[".".join(line[4].split(".")[1:])][3] += 1
 if line[3]=="1" and line[0] != line[1]: sld_dict[line[0]][0] += 1 sld_dict[line[0]][4].update([line[10]]) sld_dict[line[0]][5].update([line[4]]) sld_dict[line[0]][6].update([line[6]]) if line[3]=="1" and line[0] ==line[1]: sld_dict[line[0]][1] += 1 sld_dict[line[0]][4].update([line[10]]) sld_dict[line[0]][5].update([line[4]]) sld_dict[line[0]][6].update([line[6]])

sld_dict_sorted = dict(sorted(sld_dict.items(), key=lambda x: x[1], reverse=True)) 
fo = open("./mydata_level2/sld_fqdn_a_canme_r_ip_aso.txt","w")
for key in tqdm(sld_dict_sorted): fo.write(",".join([key]+list(map(str,sld_dict_sorted[key][:4]+[len(sld_dict_sorted[key][4])]+[len(sld_dict_sorted[key][5])]+[len(sld_dict_sorted[key][6])])))+"n")fo.close()
```



```
# step 统计每个 IP 的解析域名的数量，并标记已知的类别fp = open("./mydata_level2/level2_sld_geo_data.txt","r")cdn_ips = {}hidden_ips = {}other_ips = {}for line in tqdm(fp): line = line.split(",") if line[0] in bloom_cdn: if line[1] not in cdn_ips: cdn_ips[line[1]] = 1 else: cdn_ips[line[1]] += 1 elif line[0] in bloom_hidden: if line[1] not in hidden_ips: hidden_ips[line[1]] = 1 else: hidden_ips[line[1]] += 1 else: if line[1] not in other_ips: other_ips[line[1]] = 1 else: other_ips[line[1]] += 1
fo = open("./mydata_level2/all_ip_count.txt","w")
cdn_ips_sorted = dict(sorted(cdn_ips.items(), key=lambda x: x[1], reverse=True)) hidden_ips_sorted = dict(sorted(hidden_ips.items(), key=lambda x: x[1], reverse=True)) other_ips_sorted = dict(sorted(other_ips.items(), key=lambda x: x[1], reverse=True))
for key in cdn_ips_sorted: fo.write(key+","+str(cdn_ips_sorted[key])+","+"1"+"n")for key in hidden_ips_sorted: fo.write(key+","+str(hidden_ips_sorted[key])+","+"2"+"n")for key in other_ips_sorted: fo.write(key+","+str(other_ips_sorted[key])+","+"0"+"n")fo.close()
```



```
import osfrom tqdm import tqdmfrom pybloom_live import ScalableBloomFilter, BloomFilter# step 0 提取特定 ASO 信息的 IP 地址# step 1 统计每个 IP 解析的 FQDN 数fp = open("./answer/cdn_level2/result.txt","r")hdomains = fp.readlines()hdomains = [hi.strip().split("t")[1] for hi in hdomains]print(hdomains[9])file_names = os.listdir('./cdn_level2/datacon_cdn_ad')
ip_dict = {}
for file_name in tqdm(file_names): file_path = os.path.join('./cdn_level2/datacon_cdn_ad',file_name) with open(file_path,"r") as fp: for line in tqdm(fp): if line.startswith("sld,md5_fqdn"): continue line = line.strip().split(",") if line[3]=="5": continue if line[3] == "1" and line[0] in hdomains: if line[4] not in ip_dict: ip_dict[line[4]] = 0 ip_dict[line[4]] += 1

ip_dict_sorted = dict(sorted(ip_dict.items(), key=lambda x: x[1], reverse=True))
fo = open("./mydata_level2/hidden_ip_fqdn_count_sorted.txt","w")
for key in ip_dict_sorted: fo.write(key+","+str(ip_dict_sorted[key])+"n")fo.close()

# step 2 取前 591 个 IP，这些 IP 每个平均解析了 14 万的域名，找出其解析过的 SLDfp = open("./mydata_level2/hidden_591.ip","r")hips = fp.readlines()hips = [hi.strip() for hi in hips]
file_names = os.listdir('./cdn_level2/datacon_cdn_ad')
sld_dict = set()
for file_name in tqdm(file_names): file_path = os.path.join('./cdn_level2/datacon_cdn_ad',file_name) with open(file_path,"r") as fp: for line in tqdm(fp): if line.startswith("sld,md5_fqdn"): continue line = line.strip().split(",") if line[3]=="5": continue if line[3] == "1" and line[4] in hips: sld_dict.update([line[0]])
fo = open("./mydata_level2/hidden_ip_591_to_sld.txt","w")for si in list(sld_dict):    fo.write(si+"n")
```



```
# webhosting provider["Dreamscape Networks Limited", "BIZLAND-SD", "Cizgi Telekomunikasyon Anonim Sirketi","Marcin Waligorski Greener", "Namesco Limited","Register S.p.A.","Host Europe GmbH", "AUTOMATTIC","InterNetX GmbH", "WEBAIR-INTERNET","Strato AG","FASTLY","LIQUIDWEB","WEEBLY","BIZLAND-SD","Wix.com","SQUARESPACE","Trellian Pty. Limited"]# domain parking["Linode","SEDO GmbH","BODIS-NJ","CONFLUENCE-NETWORK-INC","CENTURYLINK-LEGACY-SAVVIS","IONOS SE","UK-2 Limited"]
```



```
v=DMARC1; p=none; fo=1; ruf=mailto:xxx@xxxxxx.com; rua=mailto:xxx@xxxxxx.com
```



```
;; QUESTION SECTION: ;datacon2022.secrank.cn. IN A
 ;; ANSWER SECTION: datacon2022.secrank.cn. 30  IN  CNAME   admin.datacon.cdn.
```



```
;; ANSWER SECTION: datacon2022.secrank.cn. 30 IN CNAME admin.datacon.cdn. ;; ANSWER SECTION: secrank.cn.     60  IN  TXT "5ca162f89d93a4e7e5661a4b290b6d33"
```



```
;; ANSWER SECTION: datacon2022.secrank.cn. 30 IN CNAME admin.datacon.cdn. ;; ANSWER SECTION: secrank.cn.     60  IN  TXT "fdf82d037bff4fbb42495e6232c1d7f3"
```



```
secrank.cn TXT e1f6c5df7297f459d2eae4783361613a
```



```
secrank.cn TXT 982a0de018edf5bf12d042284629106a
```



```
secrank.cn TXT fdf82d037bff4fbb42495e6232c1d7f3
```



```
secrank.cn TXT fdf82d037bff4fbb42495e6232c1d7f3
```



```
secrank.cn TXT fdf82d037bff4fbb42495e6232c1d7f3
```



```
datacon2022.secrank.cn. 30 IN CNAME admin.datacon.cdn. admin.datacon.cdn.  3600    IN  A   xxx.xxx.xxx.xxx(IP)
```



```
_verify.secrank.cn. 86400 IN TXT "f3c5e853dbd3c50b66d1545aaa074b86" _dmarc.secrank.cn.  86400   IN  TXT "v=DMARC1; p=quarantine; rua=mailto:da1ef3b3@secrank.cn"
```



```
邮箱：da1ef3b3@secrank.c用户名：nda1ef3b3
```



```
$TTL 1D @ IN SOA _verify.secrank.cn. rname.invalid. ( 0 ; serial 1D ; refresh 1H ; retry 1W ; expire 3H ) ; minimum NS _verify.secrank.cn. A xxx.xxx.xxx.xxx(攻击者 DNS IP 地址) AAAA ::1     TXT "b6406817af968a444aa934fc2e0c6f3f"
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1673593129.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/6-1673593130.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1673593131.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/8-1673593132.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/4-1673593133.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/4-1673593134.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1673593134.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1673593135.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/6-1673593135.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1673593136.png)