# 固件安全的隐忧：UEFI漏洞的持续威胁与修复之路

> 原文: https://www.ctfiot.com/237369.html
> ID: 237369

UEFI固件漏洞：为何它们反复出现，又该如何守护我们的设备安全？

一、Binarly研究团队协调修补戴尔BIOS代码执行漏洞

一个月前，Binarly的安全研究团队成功披露了惠普设备中16个高影响漏洞和23个影响主要企业供应商的其他安全缺陷。在不到一年的时间里，Binarly披露了困扰UEFI固件生态系统的42个高严重性漏洞，这些漏洞都严重到足以导致在系统管理模式（SMM）中执行任意代码。

这些漏洞的持续发现表明，我们称之为”可重复故障“，这些故障是由于缺乏输入清理或一般而言不安全的编码实践造成的。这些故障是代码库复杂性或对遗留组件的支持的直接后果，这些组件的安全关注较少，但仍在现场广泛部署。在许多情况下，同一个漏洞可以通过多次迭代来修复，但攻击面的复杂性仍为恶意利用留下了漏洞。

这些也证明了大多数可用于源代码分析的企业工具不适合检测固件特定的安全缺陷。原因有很多，其中最明显的一个是内存管理功能的实现与非固件供应链的复杂性导致了几乎无限的漏洞来源。不幸的是，大多数为主要设备供应商开发固件代码的外包公司都没有产品安全团队，有时甚至没有一名专门负责降低安全风险的员工。大多数安全实践都围绕着合规性检查表，使用配置不当的静态分析工具，并在发布前对整个代码库快照运行防病毒扫描。这种对设计缺陷的根本误解导致代码复杂性的扩大，并使设备处于永久的暴露状态。

其中一个最好的例子是已有五年历史的AMI UsbRt漏洞(INTEL-SA-00057)，该漏洞仍然存在于较新的硬件设备中。UsbRt漏洞于2016年首次被发现，名为Aptiocalypsis[2]。然而，由于代码的复杂性，随后发现了该漏洞的多个变体[3]。正如我们在OffensiveCon会议[4]的演讲中所强调的那样，UsbRt漏洞有近六年的成功和可重复利用的历史。快进到今天，Binarly平台继续在企业基础设施中大规模检测AMI UsbRt的易受攻击版本，受影响的设备数量令人担忧。

看到一些供应商向客户提供有关存在漏洞代码的虚假声明[5]，真是令人沮丧。

“…AMI源代码的这一部分已有大约七年历史，并且不再出现在当前的AMI UEFI产品中。”

下图显示了使用UsbRt GUID(04EAAAA1-29A1-11D7-8838-00500473D4EB)进行Linux供应商固件服务（LVFS[6]）搜索查询的结果，其中可能受到影响的供应商列表包括所有主要企业设备制造商，例如联想、戴尔、Star Labs等。

Binarly已与LVFS项目合作，帮助保护企业设备供应链免受已知漏洞的影响。CERT/CC、LVFS（Richard Hughes、Red Hat）和Binarly之间的合作重点是通过应用FwHunt[7]规则检测易受攻击的设备供应商，帮助大规模地确定受影响方的范围。这是AMI UsbRt攻击载体在业界广泛存在并在企业网络上暴露大量攻击面的确凿证据。

这正是我们最新的戴尔漏洞和披露的开始。回顾性扫描发现了可能受影响的设备，这促使我们进一步调查。Binarly团队建议从进一步的UEFI固件更新中删除UsbRt组件，以减少攻击面。由于此组件的代码复杂性，很难维护此代码并吸收可接受的安全风险。与往常一样，我们通过CERT/CC VINCE系统启动披露流程，以通知多个受影响方并在一个集中的地方协调披露流程。

通过这项研究，Binarly发现并向戴尔报告了与其企业设备相关的三种新的UsbRt漏洞变种。

戴尔披露信息可在此处查阅：DSA-2022-053[8]

BRLY ID

Description and Impact

CVSS Score

BRLY-2021-043[9]

CVE-2022-24420

SMM Memory Corruption: Dell BIOS contains an improper input validation vulnerability. A local authenticated malicious user may potentially exploit this vulnerability by using an SMI to gain arbitrary code execution during SMM.

8.2  
(High)

BRLY-2021-045[10]

CVE-2022-24421

SMM Memory Corruption: Dell BIOS contains an improper input validation vulnerability. A local authenticated malicious user may potentially exploit this vulnerability by using an SMI to gain arbitrary code execution during SMM.

8.2  
(High)

BRLY-2022-004[11]

CVE-2022-24419

SMM Callout: Dell BIOS contains an improper input validation vulnerability. A local authenticated malicious user may potentially exploit this vulnerability by using an SMI to gain arbitrary code execution during SMM.

8.2  
(High)

我们赞扬戴尔PSIRT团队的快速响应和向客户交付补丁。从问题报告到补丁发布大约用了三个月的时间，而其他供应商通常的时间表接近六个月。当我们处理已知的攻击媒介（例如AMI UsbRt）时，缩短披露时间表极其重要。由于可信平台模块(TPM)测量的限制，固件完整性监控系统无法检测到所有已发现漏洞的主动利用。由于固件运行时可见性的设计限制，远程设备健康证明解决方案将无法检测到受影响的系统。

二、AMI UsbRt攻击面的背景

让我们深入研究这些问题的根本原因，以及为什么它们如此频繁地出现在同一段代码中。AMI gUsbData结构非常复杂，无法在一个屏幕上显示，并且包含30多个唯一字段。代码的复杂性在设计上无法保证安全，过去六年报告的多个安全漏洞（8个CVE！）证实了这一点。攻击者可以在操作系统级别的固件之外操纵gUsbData结构。下图显示了攻击面的复杂性：

2017年发现的其中一个问题（CVE-2017-5721）暴露了UsbRt API接口的复杂性问题。来看看过去的这个爆料：

有趣的是这个漏洞是如何被修补的，以及开发人员应用了哪些缓解措施。当输入数据由攻击者控制时，修补此类问题的常见做法是对该输入数据应用清理屏障。下图显示了负责清理gUsbData结构的ValidateUsbData()函数。

正如我们在下面看到的，ValidateUsbData()的实现基于对输入数据的验证，通过计算和验证该数据的CRC32校验和：

由于该实现基于不适当的加密哈希函数，因此它在设计上存在弱点。CRC32哈希可以被欺骗，并且负责清理的验证屏障可以被CRC32欺骗攻击[12]绕过。这导致了几年后发现的另一个漏洞(CVE-2020-12301)。

让我们谈谈CVE-2020-12301漏洞的利用复杂性。攻击媒介没有区别，但基于Intel的缓解措施可能会有一些限制。利用步骤如下：

攻击者控制struct_ptr指针

攻击者控制gUsbData，因为可以绕过基于CRC32的缓解措施

这样就可以调用任意函数并向其传递参数

另一个缓解措施是SMM_Code_Chk_En[13]（有时被开发人员禁用），它由英特尔开发，自Kabylake以来一直用于较新的设备。验证您的设备是否支持此缓解措施的最简单方法是检查MSR_SMM_FEATURE_CONTROL寄存器中的位状态或使用英特尔Chipsec 工具[14]。SMM_Code_Chk_En缓解措施通过应用额外的验证来阻止位于 SMRAM 之外的代码的执行，以防止一类称SMM调用的漏洞。

三、第一个公开披露的基于 ROP 的 SMM 漏洞

Synactiv团队的BrunoPujos在博客“SMM中的代码检查(Mate)[15]”中首次发现了有关SMM_Code_Chk_En绕过的详细信息。作者讨论了绕过此缓解措施的潜在方法，并建议使用ROP链作为最有效的攻击。Binarly团队决定更进一步，通过利用CVE-2020-12301漏洞展示完整的链式ROP漏洞利用演示。与之前介绍的利用步骤有何不同？

攻击者无法控制被调用函数的参数

攻击者需要构建ROP/JOP链来获取其他原语

根据我们的研究，在任何现有的SMM驱动程序中找到ROP小工具非常简单。为了构建有效的攻击，任何SMM驱动程序都包含以下小工具：

SetJump-可用于在任意调用时获取寄存器值

攻击者仍然需要访问RCX指向的内存，并且将利用以下小工具（几乎可以在任何设备上使用）：mov ecx, 0xe8; mov rax, rdx; jmp qword ptr [rcx + 0x48];

我们成功利用的目标是读取SMRAM内存区域，因此我们需要找到几个小工具来设置RCX、RDX、R8寄存器的值以调用CopyMem函数。考虑到UEFI驱动程序的特性，这不是问题。利用Ropper工具[16]可以识别所需的小工具。

ropper -a x86_64 -f UsbRtSmm –search “mov rdx” –detail

现在的最终ROP链如下所示：-设置R8寄存器值（CopyMem的大小）-设置RCX和RDX寄存器值（CopyMem的源和目标缓冲区指针）-在InternalLongJump函数内恢复寄存器值-新的RSP值=泄露的RSP值-8（因为一次POP和两次调用）-跳转到CopyMem函数

以下针对UsbRt的攻击细节适用：-将数据构建到受控内存中-更改gUsbData结构中的指针，使其指向构造的数据-通过设置SwSmiInputValue=0x31触发SWSMI处理程序。

成功利用的结果如下面所示，存储在RCX中的地址的SMRAM中的所需字节被转储到控制台。为了加快PoC的开发，我们利用了IntelChipsec工具PoC源代码[17]可在Binarly的Github仓库中获取。

不幸的是，对于防御者来说，由于UEFI固件规范及其构建过程，ROP攻击在SMM中极易开发。为了实现更稳定和可预测的行为，固件开发人员不使用太多编译器优化或混淆方法。这使得代码流程非常直接，并提供足够的空间来找到可靠的小工具来构建ROP链。那么DellUsbRt漏洞呢？关于AMIUsbRt的具体问题，利用方式与本博客中讨论的先前案例差异不大。让我们来看一下BRLY-2022-004漏洞[18]。

在下图中展示了一段Hex-Rays反编译器的伪代码片段，其中Struct指针可能被攻击者控制，并且没有检查其是否与SMRAM内存重叠。这意味着潜在的攻击者可以进行写操作。

另一个案例是BRLY-2021-045漏洞[19]披露，其中Struct值可能被潜在攻击者控制。如果FuncIndex==15，那么位于偏移0x30D8的函数将被调用，如下图所示：

Invoke()函数的第一个参数是一个指针，该指针将从gUsbData指向的结构中检索。攻击者可以控制指针，执行任意函数并向其传递最多7个参数。由于没有检查Struct->SubfuncIndex的值，如果Struct->SubfuncIndex的值等于9或10或11，则会导致在SMM中执行任意代码，因为gCoreProcTable[9]=gCoreProcTable[10]=gCoreProcTable[11]=0。

正如笔者在本博客中所展示的，缺乏对不受信任的输入的验证，这些输入可能会被攻击者操纵，而且代码库的复杂性会导致同一代码中一再出现可重复的漏洞。

博客的目的是提高人们对这些可重复问题的认识，展示众所周知的攻击媒介如何仍然能够进入较新设备的固件供应链。对于本博客中提到的与FwHunt对本博客中与AMIUsbRt漏洞相关的所有问题的检测结果如下所示：

Binarly团队一直致力于保护固件供应链，并通过向市场提供创新技术来减少整个行业客户的攻击面。根据我们的经验，我们明白修复单个供应商的漏洞是不够的。由于固件供应链的复杂性，制造端存在难以弥补的漏洞，因为这涉及到设备供应商无法控制的问题。

四、相关链接

[1]https://www.binarly.io/blog/ami-usbrt-repeatable-failures-a-6-year-old-attack-vector-still-affecting-millions-of-enterprise-devices

[2]https://github.com/Cr4sh/Aptiocalypsis

[3]https://github.com/Cr4sh/Aptiocalypsis

[4]https://github.com/binarlyio/Research_Publications/tree/main/OffensiveCon_2022

[5]https://www.ami.com/ami-clarification-on-uefi-firmware-vulnerabilities-presentation-at-offensivecon-2022/

[6]https://fwupd.org/

[7]https://github.com/binarly-io/FwHunt

[8]https://www.dell.com/support/kbdoc/en-us/000197057/dsa-2022-053

[9]https://www.binarly.io/advisories/BRLY-2021-043

[10]https://www.binarly.io/advisories/BRLY-2021-045

[11]https://www.binarly.io/advisories/BRLY-2022-004

[12]https://www.nayuki.io/page/forcing-a-files-crc-to-any-value

[13]https://www.synacktiv.com/en/publications/code-checkmate-in-smm.html

[14]https://github.com/chipsec/chipsec/blob/0be5bed8ac68707e9a22a037b26fc4b06f300751/chipsec/modules/common/smm_code_chk.py

[15]https://www.synacktiv.com/en/publications/code-checkmate-in-smm.html

[16]https://github.com/sashs/Ropper

[17]https://github.com/binarly-io/Research_Publications/tree/main/OffensiveCon_2022

[18]https://binarly.io/advisories/BRLY-2022-004

[19]https://binarly.io/advisories/BRLY-2021-045

山石网科是中国网络安全行业的技术创新领导厂商，由一批知名网络安全技术骨干于2007年创立，并以首批网络安全企业的身份，于2019年9月登陆科创板（股票简称：山石网科，股票代码：688030）。

现阶段，山石网科掌握30项自主研发核心技术，申请560多项国内外专利。山石网科于2019年起，积极布局信创领域，致力于推动国内信息技术创新，并于2021年正式启动安全芯片战略。2023年进行自研ASIC安全芯片的技术研发，旨在通过自主创新，为用户提供更高效、更安全的网络安全保障。目前，山石网科已形成了具备“全息、量化、智能、协同”四大技术特点的涉及基础设施安全、云安全、数据安全、应用安全、安全运营、工业互联网安全、信息技术应用创新、安全服务、安全教育等九大类产品服务，50余个行业和场景的完整解决方案。

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-f4054b1978be7f8b3008c6d9e0a8d800.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-69e77e8800f6486a2faeb2080447b24b.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-4cbfc61ec1e3281bc716000eeea722ad.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-993f28de1a006b0ddd12c014cb47fae6.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-94eb8e81dbb2c6480abbf45b9614acd4-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-6a51af6becf07bd9a515d613a3adcf9a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-51bbcc0ff4969412c50d4323a9277d99.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-8a1a73cf8d4409d7f5e0f74063719058.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-991a049440419dbf0f0b640697d0c8b0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-993f28de1a006b0ddd12c014cb47fae6.webp)