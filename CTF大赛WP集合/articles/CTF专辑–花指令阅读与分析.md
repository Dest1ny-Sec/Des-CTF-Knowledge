# CTF专辑–花指令阅读与分析

> 原文: https://www.ctfiot.com/194547.html
> ID: 194547

一、垃圾代码（JunkCode）

对于垃圾代码和花指令的区分，我们一般将没有实际意义的代码称作垃圾代码（Junk Code/Garbage code），而把干扰调试器分析的代码称作花指令。

典型的JunkCode一般是一些操作指令具有相同的操作数，执行一些毫无作用的运算，比如：

mov eax,eax;xchg esp,esp;jmp rva=0;//E9 00 00 00 00xor eax,0;    ；任何一个数异或0等于本身

二、汇编指令的等价替换

（1）算数拆分

add eax,0x5;就可以拆分为add eax,0x2;add eax,0x1;inc eax;inc eax;再如：shl eax,5就可以拆分为：shl eax,3;shl eax,1;shl eax,1;当然，也可以综合其他寄存器进行值的传递，比如：add eax,4;可以改写成：xor ebx,ebx;add ebx,2;mul ebx,2;add eax,ebx;

诸如此类的可以写很多种，不再阐述

下面对几个指令的等价解释进行描述：

（2）等价解释

Ⅰ.push/pop

push 0x11111;在x86程序里就等价于sub esp,0x4;mov [esp],0x11111;

pop eax;在x86程序里面就等价于mov eax,[esp];add esp,0x4;//因此，当某个寄存器没有实际作用的时候，可以用多个Pop,来代替add esp;

Ⅱ.jmp addr

mov eip,addr;

push addr;retn;

push next opcodeAddr;jmp addr;

Ⅳ.retn

比如retn 0x5其等价于：mov eip,[esp];add esp,0x4+0x5;

push ecx;mov ecx,[esp+4];add esp,8;jmp ecx;//这种写法会破坏ecx的值，因此使用的前提是ecx没有正在被程序使用

Ⅴ.enter/leave

ENTER numbytes, nestinglevel

ENTER 有两个操作数：

第一个是常数，定义为局部变量保存的堆栈空间字节数；

第二个定义了过程的词法嵌套级。

它为局部变量保留堆栈空间，把 EBP 入栈。具体来说，它执行三个操作：

把 EBP 入栈 (push ebp)

把 EBP 设置为堆栈帧的基址 (mov ebp, esp)

为局部变量保留空间 (sub esp, numbytes)

下面给出一个实例，ENTER 指令为局部变量保留了 8 个字节的堆栈空间：

enter 8,0

它与下列指令等效：

push ebp;mov ebp,esp;sub esp,8;

而一般情况下，只是简单的enter 后面不接参数，那就没有sub esp的说法了

而leave指令则跟enter相反，一般出现在retn之前:

它等价于：

mov esp, ebp;pop ebp;

等价于 mov A,0;因为异或同一个值的结果必定是0；

Ⅶ.add/sub A,1

等价于inc A;//A+=1dec A;//A-=1

Ⅷ.push/popad

Ⅸ.and

and esp,0xfffffff0

16进制为：E8 00 00 00 00

这种指令常用来获取下一行代码的地址，也可用于获取eip的值。

004710D5 >    E8 00000000   call 11111.004710DA004710DA  |.  68 10B14900   push 11111.0049B110这里执行call后，eip的值为004710DAh，而此时[esp]的值，就是0x4710DAh，因此获取call时的eip就是[esp]-0x5;

mov op1,op2     ---->    push op2 / pop op1

xor A,B==(~A&B)|(A&~B)

（3）间接赋值

我们知道，数学上常有 b=a,c=b就是c=a

那么同样的，在构建花指令的时候也可以这么做。

三、抵消型花指令

抵消型花指令主要的注意点有两个方面，一个是运算的抵消，即逆运算；

另外一个就是栈平衡类型，栈平衡也是考虑堆栈抵消型花指令的注意点。

抵消型花指令一般不会干扰分析引擎分析，但可能会影响栈平衡

（1）运算抵消

常见的运算抵消有这样几种

push-pop（压栈-出栈）

add-sub adc-sbb （加法-减法 进位加法-借位减法）mul-div imul-idiv   （乘法-除法 整数乘法-整数除法）inc-dec （加1-减1）

shl-shr （左移-右移）

xor-xor  (异或)

not-not (取反)

push eax;pop eax;add eax,2;mul eax,2;div eax,2;xor eax,2;xor eax,2;inc eax;dec eax;inc ebx;inc ebx;sub ebx,2;shl ebx,2;shr ebx,2;sub eax,2;

（2）栈平衡实例

Ⅰ.push/pop类

pushad;pushfd;push eax;push ecx;push ebx;push esi;pop esi;pop ebx;pop ecx;pop eax;popfd;popad;

Ⅱ.动态使栈平衡

动态使栈平衡的主要思路就是保存原来的栈指针,后面再恢复；下面给出一个实例：

push ebp;mov ebp,esp;sub esp,1000h;push 0h;push esi;push eax;mov esp,ebp;pop ebp;

四、jmp db型花指令

这类花指令主要是干扰分析工具分析：

其中IDA　使用的反汇编算法是Recursive Traversal

Olldbg     使用的反汇编算法是LinearSweep/Recursive Traversal(按ctrl+A组合键时)

其中线性扫描（LinearSweep）算法的技术含量不高，反汇编工具将整个模块中的每一条指令都反汇编成汇编指令，将遇到的机器码都作为代码处理，没有对所反汇编的内容进行任何判断。因此，该种算法不能有效的将代码和数据区分开，从而导致反汇编出现错误。这种错误会影响对下一条指令的正确识别，会使整个反汇编都出现错误。

而递归行进法（Recursive Traversal）按照代码可能执行的顺序来反汇编程序，对每条可能的路径进行扫描。当解码出分支指令后，反汇编工具就将这个地址记录下来，并分别反汇编各个分支中的指令，因此该算法灵活度高。

（1）无条件跳转的jmp db型

最基本的Jmp db型就是跳转接上了一个干扰的db opcode：

例如

004710D5 > $ /EB 03         jmp short 11111.004710DA004710D7     |55            db 55                                    ;  CHAR 'U'004710D8     |E8            db E8                                    ;  注意这里004710D9   . |AA            db AA004710DA   > 83C0 02       add eax,0x2

004710D5 > /EB 03           jmp short 11111.004710DA004710D7   |55              push ebp                                 ; kernel32.768E00C9004710D8   |E8 AA83C002     call 03079487

说明：Linear Sweep型反汇编引擎是逐行反汇编的，该花指令中的垃圾数据db EBh 干扰了其工作，因此错误地确定了指令的起始位置，导致反汇编的一些跳转指令的地址无效

而OD使用递归引擎分析就会正常，变成：

004710D5 > $ /EB 03         jmp short 11111.004710DA004710D7     |55            db 55                                    ;  CHAR 'U'004710D8     |E8            db E8004710D9   . |AA            stos byte ptr es:[edi]004710DA   > 83C0 02       add eax,0x2

（2）条件跳转的jmp db型

条件跳转跟无条件跳转其实差不多，主要的是用条件跳转代替了原来的jmp

下面给出一个CTF中常出现的实例：

start:  xor eax,eax;  test eax,eax;  jz label1;  jnz label1;  db E8h;label 1:  xor eax,3;  add eax,3;  ...........

（3）jmp to db干扰分析型(jx+jnx)

注：这里的jmp to db指的是一类，控制转移指令到的地址是无效的数据(db)的情况

这里的jx,jnx一般指两个相对的条件跳转，上面常接

来设置位，让条件跳转成立。

在递归算法中一个十分重要的假设是：对任意一条控制转移指令（jmp/retn/call等）都能确定其后继（即转移）的目的地址，要想要迷惑这类反汇编工具，只要让其难以确定跳转的目的地址即可；

一个实例如下：

start:  xor eax,eax;  test eax,eax;  jz label0;  jnz label1;label 0:  db 0E8hlabel 1:  xor eax,3;  add eax,3;  ...........

与上面的实例2作对比，可以看见是两个跳转实际上是跳到了不同的地方，一个是混淆的代码，一个是真正的控制流，而上面只是直接跳到了真正的控制流，只不过是控制流上面接了脏字节。

OD中反编译的结果如下

004710D5 >  33C0            xor eax,eax004710D7    85C0            test eax,eax004710D9    74 03           je short 11111.004710DE004710DB    75 00           jnz short 11111.004710DD004710DD    E8 83F00383     call 834B0165004710E2    c003 90         rol byte ptr ds:[ebx],0x90

这里具体解释下原因，首先是有两个跳转

 je跳转到的是xor eax,3而jnz是跳转到db E8，而E8是call的opcode 后面需要4个字节作为地址，所以这边就会将xor等的opcode 作为地址，从而导致识别错误。

因此这种写法，在CTF中非常常见，因为两种引擎都不能将他分析出来，需要手动去除。

注：(这里的db，也可以换成一些干扰堆栈平衡的指令，不过一定不会被执行，比如add esp,0x1)

五、call 0h型

（1）call +db+平衡

call loc+1;db C8;pop eax;//add esp,0x4;

（2）call + add [esp], n + retn

004010BF   .  E8 00000000   call 1111.004010C4004010C4  /$  830424 06     add dword ptr ss:[esp],0x6004010C8  .  C3            retn004010C9      B9            db B9

可以看到这里的add，是将call 00h的返回的地址，也就是[esp]+0x6（add 的四个字节+C3 B9）

来实现一个跳转，到004010CA，对于这种，只需要将下面的特征码patch掉就可以了：

E80000000083042406C3??

六、去除脚本

import ida_bytesimport ida_ida
def patch(ea,num=1):    for i in range(num):        ida_bytes.patch_byte(ea+i,0x90)    return
def f(begin_addr,end_addr,hexStr)  xx=(len(hexStr)-1)//2    bMask = bytes.fromhex(hexStr.replace('00', '01').replace('??', '00'))    bPattern = bytes.fromhex(hexStr.replace('??', '00'))    signs=ida_bytes.BIN_SEARCH_FORWARD| ida_bytes.BIN_SEARCH_NOBREAK| ida_bytes.BIN_SEARCH_NOSHOW    while begin_addr<end_addr:        ea=ida_bytes.bin_search(begin_addr,end_addr,bPattern,bMask,1,signs)        if ea == ida_idaapi.BADADDR:            break        else:            print(hex(ea))            patch(ea,xx)            begin_addr=ea+xx f(0x0,0x1000,"?? ?? 00 00 00 ??")

在上述脚本中：

定义了一个名为f的函数，用于执行二进制搜索并对匹配的位置进行nop。

begin_addr是搜索开始的地址。

end_addr是搜索结束的地址。

hexStr是用于搜索的十六进制模式字符串（用空格分开，其中??表示通配符，注意不可以使用诸如2?这样的情况）

接着，将hexStr转换为两个字节数组：bMask和bPattern。bMask是用于表示可变字节的，其中00表示需要匹配的字节，01表示不需要匹配的字节；bPattern则是用于搜索的固定字节序列。

定义了一个signs变量，用于指定搜索的标志位，其中BIN_SEARCH_FORWARD表示向前搜索，BIN_SEARCH_NOBREAK表示不允许搜索中途中断，BIN_SEARCH_NOSHOW表示不显示搜索结果。

接着使用ida_bytes.bin_search函数进行二进制搜索，从begin_addr到end_addr之间搜索bPattern，其中可变字节由bMask指定。搜索到匹配的位置后，将其打印出来，并调用patch函数对其进行补丁操作。

最后更新begin_addr为下一个搜索的起始地址，通常为当前匹配位置加上一个偏移量。

七、例题

[GFCTF 2021]wordy

花指令-jmp db型IDA脚本编写动态调试

一、基本分析

分析main()函数可以看到是杂乱的字节，观察0x1144可以发现，存在着jmp db1这种类型的花指令，因此可以写一个idapython脚本来解决

代码如下：

import ida_bytesimport ida_ida
def patch(ea,num=1):  for i in range(num):    ida_bytes.patch_byte(ea+i,0x90)  returnprint("-----")hexStr="EB FF C0 BF ?? 00 00 00 E8"bMask = bytes.fromhex(hexStr.replace('00', '01').replace('??', '00'))bPattern = bytes.fromhex(hexStr.replace('??', '00'))signs=ida_bytes.BIN_SEARCH_FORWARD| ida_bytes.BIN_SEARCH_NOBREAK| ida_bytes.BIN_SEARCH_NOSHOWprint(bMask,bPattern)begin_addr=0x1135end_addr=0x3100while begin_addr<end_addr:  ea=ida_bytes.bin_search(begin_addr,end_addr,bPattern,bMask,1,signs)  if ea == ida_idaapi.BADADDR:    break  else:    print(hex(ea))    patch(ea,3)    begin_addr=ea+8

二、自动化逆向

既然我们已经去除了花指令，且代码都是重复的，为什么我们不能直接获取putchar()的内容呢，为此，我们在上面代码的基础下，写下如下

idapython代码:

import idcimport ida_bytesimport ida_idaprint("-----")hexStr="EB FF C0 BF ?? 00 00 00 E8"bMask = bytes.fromhex(hexStr.replace('00', '01').replace('??', '00'))bPattern = bytes.fromhex(hexStr.replace('??', '00'))signs=ida_bytes.BIN_SEARCH_FORWARD| ida_bytes.BIN_SEARCH_NOBREAK| ida_bytes.BIN_SEARCH_NOSHOWprint(bMask,bPattern)begin_addr=0x1135end_addr=0x3100s=""while begin_addr<end_addr:  ea=ida_bytes.bin_search(begin_addr,end_addr,bPattern,bMask,1,signs)  if ea == ida_idaapi.BADADDR:    break  else:    s+=chr(idc.get_wide_byte(ea+4))    begin_addr=ea+8 print(s)

#GFCTF{u_are2wordy}

[NCTF 2022]cccha

花指令-call 0h型花指令-抵消式花指令-jmp db型IDA脚本编写chacha20

一、去花

分析main()函数，乱七八糟，看不了伪代码，观察汇编

（1）花指令-jmp变型(call 0h型)

这边的call 0h(E8 00 00 00 00)实际上目的是获取eip的地址，即call下面一行指令的地址，pop rbx的作用就是将取到的eip值放到rbx里面，然后给rbx加上一个值，赋值给call函数的返回地址，所以这段代码的本质实际上是实现了一个跳转的作用（jmp指令的变型），跳转的地址就是计算后的rbx.

除了这一种jmp变型之外，还有一种类似的，不同的是add所占用的字节数不同，

import ida_bytesimport ida_idaimport idcsigns=ida_bytes.BIN_SEARCH_FORWARD| ida_bytes.BIN_SEARCH_NOBREAK| ida_bytes.BIN_SEARCH_NOSHOWbegin_addr=0x1090end_addr=0xa1e7lth=lambda code:
int((len(code)+1)/3)
def patch(ea,code):    cd=list(code)    for i in range(len(cd)):        ida_bytes.patch_byte(ea+i,cd[i])    return
def patch_jmp_1(hexStr):    print("------patch_jmp_1-----------")    bMask = bytes.fromhex(hexStr.replace('00', '01').replace('??', '00'))    bPattern = bytes.fromhex(hexStr.replace('??', '00'))    iaddr=begin_addr    length=lth(hexStr)    while iaddr<end_addr:        ea=ida_bytes.bin_search(iaddr,end_addr,bPattern,bMask,1,signs)        print(hex(ea))        if ea == ida_idaapi.BADADDR:            break        else:            offset=idc.get_wide_dword(ea+12)+3            code=b'xe9'+offset.to_bytes(4, 'little')            patch(ea,b'x90'*length)            patch(ea,code)            iaddr=ea+length    return
def patch_jmp_2(hexStr):    print("-----------patch_jmp_2---------")    bMask = bytes.fromhex(hexStr.replace('00', '01').replace('??', '00'))    bPattern = bytes.fromhex(hexStr.replace('??', '00'))    iaddr=begin_addr    length=lth(hexStr)    while iaddr<end_addr:        ea=ida_bytes.bin_search(iaddr,end_addr,bPattern,bMask,1,signs)        print(hex(ea))        if ea == ida_idaapi.BADADDR:            break        else:            offset=idc.get_wide_byte(ea+12)+6            code=b'xeb'+offset.to_bytes(1, 'little')            patch(ea,b'x90'*length)            patch(ea,code)            iaddr=ea+length    return
def patch_directly(code):    print("------花指令:",code,"-----")    bMask = bytes.fromhex(code.replace('00', '01').replace('??', '00'))    bPattern = bytes.fromhex(code.replace('??', '00'))    iaddr=begin_addr    length=lth(code)    while iaddr<end_addr:        ea=ida_bytes.bin_search(iaddr,end_addr,bPattern,bMask,1,signs)        print(hex(ea))        if ea == ida_idaapi.BADADDR:            break        else:            patch(ea,b'x90'*length)            iaddr=ea+length-1    return
patch_jmp_1("53 53 9C E8 00 00 00 00 5B 48 81 C3 ?? ?? ?? ?? 48 89 5C 24 10 9D 5B C3")p=["50 53 52 5A 5B 58", "52 50 58 5A","53 52 5A 5B","50 52 5A 58","50 53 5B 58","53 5B","50 58","52 5A","9C 50 48 3D 22 20 00 00 77 04 7E 02 E8 E8 58 9D"]#抵消式花指令 如push rbx&pop rbx;  jmp db;
for i in p:    patch_directly(i)patch_jmp_2("53 53 9C E8 00 00 00 00 5B 48 83 C3 ?? 48 89 5C 24 10 9D 5B C3")
'''junk_jmp_change_1.text:
0000000000008838 53                            push    rbx.text:
0000000000008839 53                            push    rbx.text:
000000000000883A 9C                            pushfq.text:
000000000000883B E8 00 00 00 00                call    $+5.text:
0000000000008840 5B                            pop     rbx.text:
0000000000008841 48 81 C3 3F 00 00 00          add     rbx, (offset byte_887F - offset loc_8840).text:
0000000000008848 48 89 5C 24 10                mov     [rsp+18h+var_8], rbx.text:
000000000000884D 9D                            popfq.text:
000000000000884E 5B                            pop     rbx.text:
000000000000884F C3                            retn''''''junk_jmp_change_2.text:
000000000000892C 53                            push    rbx.text:
000000000000892D 53                            push    rbx.text:
000000000000892E 9C                            pushfq.text:
000000000000892F E8 00 00 00 00                call    $+5.text:
0000000000008934 5B                            pop     rbx.text:
0000000000008935 48 83 C3 C4                   add     rbx, (offset qword_88F8 - offset loc_8934).text:
0000000000008939 48 89 5C 24 10                mov     [rsp+20h+var_10], rbx.text:
000000000000893E 9D                            popfq.text:
000000000000893F 5B                            pop     rbx.text:
0000000000008940 C3                            retn'''
'''junk_jmp_db.text:
0000000000008883 9C                            pushfq.text:
0000000000008884 50                            push    rax.text:
0000000000008885 48 3D 22 20 00 00             cmp     rax, 2022h.text:
000000000000888B 77 04                         ja      short loc_8891.text:
000000000000888D 7E 02                         jle     short loc_8891.text:
000000000000888F E8                            db 0E8h.text:
0000000000008890 E8                            db 0E8h.text:
0000000000008891 58                            pop     rax.text:
0000000000008892 9D                            popfq'''

二、分析

IDA状态栏右键，重新分析程序。

重新分析，伪代码如下：

可以分析出，这里是一个典型的chacha20的字符串，且这个函数是用来初始化状态的

__int64 __fastcall sub_55FC9CAF9DED(){  __int64 v0; // rbp  int i; // [rsp-140h] [rbp-140h]  _DWORD v3[44]; // [rsp-138h] [rbp-138h] BYREF  __int64 v4; // [rsp-85h] [rbp-85h] BYREF  int v5; // [rsp-7Dh] [rbp-7Dh]  char v6; // [rsp-79h] [rbp-79h]  _QWORD v7[4]; // [rsp-78h] [rbp-78h] BYREF  char v8; // [rsp-58h] [rbp-58h]  _QWORD v9[5]; // [rsp-48h] [rbp-48h] BYREF  __int16 v10; // [rsp-20h] [rbp-20h]  unsigned __int64 v11; // [rsp-10h] [rbp-10h]  __int64 v12; // [rsp-8h] [rbp-8h]
  v12 = v0;  v11 = __readfsqword(0x28u);  v7[0] = 7639691014887960151LL;  v7[1] = 0x12CFEBEC73124005LL;  v7[2] = 0xF060C3D29ED918C4LL;  v7[3] = 0x45613036DB175B72LL;  v4 = 0x143D83BD8A1337E6LL;  v5 = -1868846699;  v9[0] = 0x23CE4B73757CC05ELL;  v9[1] = 0x708F01F3AC89BBA4LL;  v9[2] = 0x62D45B4183317FC8LL;  v9[3] = 0x4B50FC9DDC27A7A6LL;  v9[4] = 0x385117386B2F9806LL;  v10 = 0xEF2F;  v8 = 0;  v6 = 0;  puts("input:");  gets(s1);  if ( strlen(s1) != 42 )  {    printf("Wrong!");    exit(0);  }  expand_key(v3, v7, &v4, -1640531527);  Gen_KeyStream(v3);  for ( i = 0; i <= 41; ++i ){    s1[i] ^= *(v3 + i);    s1[i] += i;  }  if ( !memcmp(s1, v9, 0x2AuLL) )    printf("Right!");  else    printf("Wrong!");  return 0LL;}

v9_g=[0x23CE4B73757CC05E,0x708F01F3AC89BBA4,0x62D45B4183317FC8,0x4B50FC9DDC27A7A6,0x385117386B2F9806,0xEF2F]s_g=[0x24aa2514342efc10,0x57b9d9d0924bd6aa,0x668a271f44325f8f ,0x1900ecaca269bcb6,0x774ec7717c3840df,0xd878e3846e0ebb32]def f(x):    s=[]    for i in x:        t=hex(i)[2:]        for j in range(len(t),0, -2):            s.append(int(t[j-2:j],16))    return sv9=f(v9_g)s=f(s_g)flg=""for i in range(42):    flg+=chr(((v9[i]-i)^s[i]+256)%256)print(flg)

NCTF{cb86d437-8671-42a4-82dc-3259754e5ef5}

八、总结

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:
222328705

星盟安全团队纳新群2:
346014666

有兴趣的师傅欢迎一起来讨论!

PS:
团队纳新简历投递邮箱：

xmcve@qq.com

责任编辑：@LYK0r4师傅


```
mov eax,eax;xchg esp,esp;jmp rva=0;//E9 00 00 00 00xor eax,0;    ；任何一个数异或0等于本身
add eax,0x5;就可以拆分为add eax,0x2;add eax,0x1;inc eax;inc eax;再如：shl eax,5就可以拆分为：shl eax,3;shl eax,1;shl eax,1;当然，也可以综合其他寄存器进行值的传递，比如：add eax,4;可以改写成：xor ebx,ebx;add ebx,2;mul ebx,2;add eax,ebx;
push 0x11111;在x86程序里就等价于sub esp,0x4;mov [esp],0x11111;
pop eax;在x86程序里面就等价于mov eax,[esp];add esp,0x4;//因此，当某个寄存器没有实际作用的时候，可以用多个Pop,来代替add esp;
mov eip,addr;
push addr;retn;
push next opcodeAddr;jmp addr;
比如retn 0x5其等价于：mov eip,[esp];add esp,0x4+0x5;
push ecx;mov ecx,[esp+4];add esp,8;jmp ecx;//这种写法会破坏ecx的值，因此使用的前提是ecx没有正在被程序使用
push ebp;mov ebp,esp;sub esp,8;
mov esp, ebp;pop ebp;
等价于 mov A,0;因为异或同一个值的结果必定是0；
等价于inc A;//A+=1dec A;//A-=1
and esp,0xfffffff0
004710D5 >    E8 00000000   call 11111.004710DA004710DA  |.  68 10B14900   push 11111.0049B110这里执行call后，eip的值为004710DAh，而此时[esp]的值，就是0x4710DAh，因此获取call时的eip就是[esp]-0x5;
mov op1,op2     ---->    push op2 / pop op1
xor A,B==(~A&B)|(A&~B)
push eax;pop eax;add eax,2;mul eax,2;div eax,2;xor eax,2;xor eax,2;inc eax;dec eax;inc ebx;inc ebx;sub ebx,2;shl ebx,2;shr ebx,2;sub eax,2;
pushad;pushfd;push eax;push ecx;push ebx;push esi;pop esi;pop ebx;pop ecx;pop eax;popfd;popad;
push ebp;mov ebp,esp;sub esp,1000h;push 0h;push esi;push eax;mov esp,ebp;pop ebp;
004710D5 > $ /EB 03         jmp short 11111.004710DA004710D7     |55            db 55                                    ;  CHAR 'U'004710D8     |E8            db E8                                    ;  注意这里004710D9   . |AA            db AA004710DA   > 83C0 02       add eax,0x2
004710D5 > /EB 03           jmp short 11111.004710DA004710D7   |55              push ebp                                 ; kernel32.768E00C9004710D8   |E8 AA83C002     call 03079487
004710D5 > $ /EB 03         jmp short 11111.004710DA004710D7     |55            db 55                                    ;  CHAR 'U'004710D8     |E8            db E8004710D9   . |AA            stos byte ptr es:[edi]004710DA   > 83C0 02       add eax,0x2
start:  xor eax,eax;  test eax,eax;  jz label1;  jnz label1;  db E8h;label 1:  xor eax,3;  add eax,3;  ...........
start:  xor eax,eax;  test eax,eax;  jz label0;  jnz label1;label 0:  db 0E8hlabel 1:  xor eax,3;  add eax,3;  ...........
004710D5 >  33C0            xor eax,eax004710D7    85C0            test eax,eax004710D9    74 03           je short 11111.004710DE004710DB    75 00           jnz short 11111.004710DD004710DD    E8 83F00383     call 834B0165004710E2    c003 90         rol byte ptr ds:[ebx],0x90
call loc+1;db C8;pop eax;//add esp,0x4;
004010BF   .  E8 00000000   call 1111.004010C4004010C4  /$  830424 06     add dword ptr ss:[esp],0x6004010C8  .  C3            retn004010C9      B9            db B9
E80000000083042406C3??
import ida_bytesimport ida_ida
def patch(ea,num=1):    for i in range(num):        ida_bytes.patch_byte(ea+i,0x90)    return
def f(begin_addr,end_addr,hexStr)  xx=(len(hexStr)-1)//2    bMask = bytes.fromhex(hexStr.replace('00', '01').replace('??', '00'))    bPattern = bytes.fromhex(hexStr.replace('??', '00'))    signs=ida_bytes.BIN_SEARCH_FORWARD| ida_bytes.BIN_SEARCH_NOBREAK| ida_bytes.BIN_SEARCH_NOSHOW    while begin_addr<end_addr:        ea=ida_bytes.bin_search(begin_addr,end_addr,bPattern,bMask,1,signs)        if ea == ida_idaapi.BADADDR:            break        else:            print(hex(ea))            patch(ea,xx)            begin_addr=ea+xx f(0x0,0x1000,"?? ?? 00 00 00 ??")
import ida_bytesimport ida_ida
def patch(ea,num=1):  for i in range(num):    ida_bytes.patch_byte(ea+i,0x90)  returnprint("-----")hexStr="EB FF C0 BF ?? 00 00 00 E8"bMask = bytes.fromhex(hexStr.replace('00', '01').replace('??', '00'))bPattern = bytes.fromhex(hexStr.replace('??', '00'))signs=ida_bytes.BIN_SEARCH_FORWARD| ida_bytes.BIN_SEARCH_NOBREAK| ida_bytes.BIN_SEARCH_NOSHOWprint(bMask,bPattern)begin_addr=0x1135end_addr=0x3100while begin_addr<end_addr:  ea=ida_bytes.bin_search(begin_addr,end_addr,bPattern,bMask,1,signs)  if ea == ida_idaapi.BADADDR:    break  else:    print(hex(ea))    patch(ea,3)    begin_addr=ea+8
import idcimport ida_bytesimport ida_idaprint("-----")hexStr="EB FF C0 BF ?? 00 00 00 E8"bMask = bytes.fromhex(hexStr.replace('00', '01').replace('??', '00'))bPattern = bytes.fromhex(hexStr.replace('??', '00'))signs=ida_bytes.BIN_SEARCH_FORWARD| ida_bytes.BIN_SEARCH_NOBREAK| ida_bytes.BIN_SEARCH_NOSHOWprint(bMask,bPattern)begin_addr=0x1135end_addr=0x3100s=""while begin_addr<end_addr:  ea=ida_bytes.bin_search(begin_addr,end_addr,bPattern,bMask,1,signs)  if ea == ida_idaapi.BADADDR:    break  else:    s+=chr(idc.get_wide_byte(ea+4))    begin_addr=ea+8 print(s)
#GFCTF{u_are2wordy}
import ida_bytesimport ida_idaimport idcsigns=ida_bytes.BIN_SEARCH_FORWARD| ida_bytes.BIN_SEARCH_NOBREAK| ida_bytes.BIN_SEARCH_NOSHOWbegin_addr=0x1090end_addr=0xa1e7lth=lambda code:
int((len(code)+1)/3)
def patch(ea,code):    cd=list(code)    for i in range(len(cd)):        ida_bytes.patch_byte(ea+i,cd[i])    return
def patch_jmp_1(hexStr):    print("------patch_jmp_1-----------")    bMask = bytes.fromhex(hexStr.replace('00', '01').replace('??', '00'))    bPattern = bytes.fromhex(hexStr.replace('??', '00'))    iaddr=begin_addr    length=lth(hexStr)    while iaddr<end_addr:        ea=ida_bytes.bin_search(iaddr,end_addr,bPattern,bMask,1,signs)        print(hex(ea))        if ea == ida_idaapi.BADADDR:            break        else:            offset=idc.get_wide_dword(ea+12)+3            code=b'xe9'+offset.to_bytes(4, 'little')            patch(ea,b'x90'*length)            patch(ea,code)            iaddr=ea+length    return
def patch_jmp_2(hexStr):    print("-----------patch_jmp_2---------")    bMask = bytes.fromhex(hexStr.replace('00', '01').replace('??', '00'))    bPattern = bytes.fromhex(hexStr.replace('??', '00'))    iaddr=begin_addr    length=lth(hexStr)    while iaddr<end_addr:        ea=ida_bytes.bin_search(iaddr,end_addr,bPattern,bMask,1,signs)        print(hex(ea))        if ea == ida_idaapi.BADADDR:            break        else:            offset=idc.get_wide_byte(ea+12)+6            code=b'xeb'+offset.to_bytes(1, 'little')            patch(ea,b'x90'*length)            patch(ea,code)            iaddr=ea+length    return
def patch_directly(code):    print("------花指令:",code,"-----")    bMask = bytes.fromhex(code.replace('00', '01').replace('??', '00'))    bPattern = bytes.fromhex(code.replace('??', '00'))    iaddr=begin_addr    length=lth(code)    while iaddr<end_addr:        ea=ida_bytes.bin_search(iaddr,end_addr,bPattern,bMask,1,signs)        print(hex(ea))        if ea == ida_idaapi.BADADDR:            break        else:            patch(ea,b'x90'*length)            iaddr=ea+length-1    return
patch_jmp_1("53 53 9C E8 00 00 00 00 5B 48 81 C3 ?? ?? ?? ?? 48 89 5C 24 10 9D 5B C3")p=["50 53 52 5A 5B 58", "52 50 58 5A","53 52 5A 5B","50 52 5A 58","50 53 5B 58","53 5B","50 58","52 5A","9C 50 48 3D 22 20 00 00 77 04 7E 02 E8 E8 58 9D"]#抵消式花指令 如push rbx&pop rbx;  jmp db;
for i in p:    patch_directly(i)patch_jmp_2("53 53 9C E8 00 00 00 00 5B 48 83 C3 ?? 48 89 5C 24 10 9D 5B C3")
'''junk_jmp_change_1.text:
0000000000008838 53                            push    rbx.text:
0000000000008839 53                            push    rbx.text:
000000000000883A 9C                            pushfq.text:
000000000000883B E8 00 00 00 00                call    $+5.text:
0000000000008840 5B                            pop     rbx.text:
0000000000008841 48 81 C3 3F 00 00 00          add     rbx, (offset byte_887F - offset loc_8840).text:
0000000000008848 48 89 5C 24 10                mov     [rsp+18h+var_8], rbx.text:
000000000000884D 9D                            popfq.text:
000000000000884E 5B                            pop     rbx.text:
000000000000884F C3                            retn''''''junk_jmp_change_2.text:
000000000000892C 53                            push    rbx.text:
000000000000892D 53                            push    rbx.text:
000000000000892E 9C                            pushfq.text:
000000000000892F E8 00 00 00 00                call    $+5.text:
0000000000008934 5B                            pop     rbx.text:
0000000000008935 48 83 C3 C4                   add     rbx, (offset qword_88F8 - offset loc_8934).text:
0000000000008939 48 89 5C 24 10                mov     [rsp+20h+var_10], rbx.text:
000000000000893E 9D                            popfq.text:
000000000000893F 5B                            pop     rbx.text:
0000000000008940 C3                            retn'''
'''junk_jmp_db.text:
0000000000008883 9C                            pushfq.text:
0000000000008884 50                            push    rax.text:
0000000000008885 48 3D 22 20 00 00             cmp     rax, 2022h.text:
000000000000888B 77 04                         ja      short loc_8891.text:
000000000000888D 7E 02                         jle     short loc_8891.text:
000000000000888F E8                            db 0E8h.text:
0000000000008890 E8                            db 0E8h.text:
0000000000008891 58                            pop     rax.text:
0000000000008892 9D                            popfq'''
__int64 __fastcall sub_55FC9CAF9DED(){  __int64 v0; // rbp  int i; // [rsp-140h] [rbp-140h]  _DWORD v3[44]; // [rsp-138h] [rbp-138h] BYREF  __int64 v4; // [rsp-85h] [rbp-85h] BYREF  int v5; // [rsp-7Dh] [rbp-7Dh]  char v6; // [rsp-79h] [rbp-79h]  _QWORD v7[4]; // [rsp-78h] [rbp-78h] BYREF  char v8; // [rsp-58h] [rbp-58h]  _QWORD v9[5]; // [rsp-48h] [rbp-48h] BYREF  __int16 v10; // [rsp-20h] [rbp-20h]  unsigned __int64 v11; // [rsp-10h] [rbp-10h]  __int64 v12; // [rsp-8h] [rbp-8h]
  v12 = v0;  v11 = __readfsqword(0x28u);  v7[0] = 7639691014887960151LL;  v7[1] = 0x12CFEBEC73124005LL;  v7[2] = 0xF060C3D29ED918C4LL;  v7[3] = 0x45613036DB175B72LL;  v4 = 0x143D83BD8A1337E6LL;  v5 = -1868846699;  v9[0] = 0x23CE4B73757CC05ELL;  v9[1] = 0x708F01F3AC89BBA4LL;  v9[2] = 0x62D45B4183317FC8LL;  v9[3] = 0x4B50FC9DDC27A7A6LL;  v9[4] = 0x385117386B2F9806LL;  v10 = 0xEF2F;  v8 = 0;  v6 = 0;  puts("input:");  gets(s1);  if ( strlen(s1) != 42 )  {    printf("Wrong!");    exit(0);  }  expand_key(v3, v7, &v4, -1640531527);  Gen_KeyStream(v3);  for ( i = 0; i <= 41; ++i ){    s1[i] ^= *(v3 + i);    s1[i] += i;  }  if ( !memcmp(s1, v9, 0x2AuLL) )    printf("Right!");  else    printf("Wrong!");  return 0LL;}
v9_g=[0x23CE4B73757CC05E,0x708F01F3AC89BBA4,0x62D45B4183317FC8,0x4B50FC9DDC27A7A6,0x385117386B2F9806,0xEF2F]s_g=[0x24aa2514342efc10,0x57b9d9d0924bd6aa,0x668a271f44325f8f ,0x1900ecaca269bcb6,0x774ec7717c3840df,0xd878e3846e0ebb32]def f(x):    s=[]    for i in x:        t=hex(i)[2:]        for j in range(len(t),0, -2):            s.append(int(t[j-2:j],16))    return sv9=f(v9_g)s=f(s_g)flg=""for i in range(42):    flg+=chr(((v9[i]-i)^s[i]+256)%256)print(flg)
NCTF{cb86d437-8671-42a4-82dc-3259754e5ef5}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/0-1721435281.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/2-1721435282.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/0-1721435283.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1721435283.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1721435284.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/1-1721435284.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/9-1721435285.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/10-1721435285.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1721435285.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1721435286.png)