# 2026解题领红包基本完成(少MCP和Win高级, 但很有梗)

> 原文: https://www.ctfiot.com/302505.html
> ID: 302505

作者论坛账号：Command

环境检测,如果异常则影响下一步解密的结果

使用AES(大概是)解密输入文件,解密后得到文字点阵图(图片内容就是Flag)

将用户输入进行渲染, 并与(2)中的点阵图比较

变量

含义

干净环境值

JNI 环境异常标志（FindClass/GetMethodID/NewStringUTF/GetObjectRefType 检测）

（JNI 全部正常）

（即v152）

/proc/self/maps 首次读取相关异常

（即v161）

可执行库 hook 检测（Frida/Xposed inline hook）

（无 hook）

readlink + readlinkat 路径一致性 + maps/status 模拟器特征检测

maps 中是否存在黑名单字符串（frida/magisk 等）

设备指纹命中模拟器列表（v263 == 1）

不触发

、/sys/cpu等路径 access 失败超限

不触发（真机均可访问）

首次 maps 解析：检测[vdso]/[vsyscall]/ 调试器路径 / frida-agent 路径等 → 干净环境无命中，v114 = 0

后续各阶段（maps hash 校验、emulator 文件系统检测、可执行文件符号链接校验等） → 全部通过，无加分

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码隐藏代码int__cdeclsub_D5D130(chara1){__time32_tv1;// eaxcharv2;// alcharv3;// alcharv4;// dlcharv5;// clintv6;// eaxunsigned__int8 v8;// alintv9;// edxintv10;// edxintv11;// eax__time32_t*Time;// [esp+0h] [ebp-78h] BYREFstd::
string_0 *v13;// [esp+14h] [ebp-64h]char*Str;// [esp+18h] [ebp-60h]charv15[4];// [esp+1Ch] [ebp-5Ch] BYREFintv16;// [esp+20h] [ebp-58h]int(__cdecl *v17)(int,int,int,int,int,int);// [esp+34h] [ebp-44h]int*v18;// [esp+38h] [ebp-40h]int*v19;// [esp+3Ch] [ebp-3Ch]void(__noreturn *v20)();// [esp+40h] [ebp-38h]__time32_t**p_Time;// [esp+44h] [ebp-34h]char*v22;// [esp+58h] [ebp-20h] BYREFintv23;// [esp+5Ch] [ebp-1Ch]charv24;// [esp+60h] [ebp-18h] BYREFchar*v25;// [esp+70h] [ebp-8h]intsavedregs;// [esp+78h] [ebp+0h] BYREF v25 = &a1; v17 = sub_D5C800; p_Time = &Time; v18 = dword_D5E3D4; v19 = &savedregs; v20 = sub_D5D4EA; sub_C9C330(v15); sub_C9A650(); v16 =-1; v1 = time(0); srand(v1); SetConsoleOutputCP(0xFDE9u); sub_D57E50((int)&dword_D627C0,"========================================"); sub_C915B0(Time); sub_D57E50((int)&dword_D627C0," CrackMe Challenge v2.5 - 2026 "); sub_C915B0(Time); sub_D57E50((int)&dword_D627C0,"========================================"); sub_C915B0(Time); sub_D57E50((int)&dword_D627C0,"Keywords: 52pojie, 2026, Happy new year"); sub_C915B0(Time); sub_D57E50((int)&dword_D627C0,"Hint: Fake flag; length is key"); sub_C915B0(Time); sub_D57E50((int)&dword_D627C0,"----------------------------------------"); sub_C915B0(Time); v22 = &v24; v23 =0; v24 =0; v16 =1; v13 = (std::
string_0 *)&v22; sub_D57E50((int)&dword_D627C0,"n[?] Enter the password: "); v13 = (std::
string_0 *)&v22; v2 = sub_C91560(); v13 = (std::
string_0 *)&v22; sub_D55840(&dword_D625E0, &v22, v2); Str = v22; v3 = sub_C91740(v22); v4 =53; v5 = v3; v6 =0;if( !v5 ) { while( Str[v6] == v4 ) { if( ++v6 ==16)// 长度16的假码 { v16 =1; sub_D57E50((int)&dword_D627C0,"n[!] You're getting closer..."); v16 =1; gotoLABEL_9; } v4 = byte_D63032[v6]; } if(strlen(Str) !=31)// 真码长度为31 { v16 =1; sub_D57E50((int)&dword_D627C0,"n[!] Hint: The length is your first real challenge."); gotoLABEL_9; } v16 =1; if( sub_C916D0((int)Str,31) )// 在这里面进行校验 { Str =0; v8 = *v22; if( !*v22 ) gotoLABEL_16; v9 =0; do { Str += ++v9 * v8; v8 = v22[v9]; } while( v8 ); if( Str != (char*)44709)// 其实这里不需要管的, 直接去上面的函数就行 {LABEL_16: v16 =1; sub_D57E50((int)&dword_D627C0,"n[!] Checksum failed! Something is wrong..."); sub_C915B0(Time); sub_D57E50((int)&dword_D627C0,"[!] Expected: 44709, Got: "); sub_D0DE70(Str); sub_C915B0(v10);LABEL_17: v16 =1; gotoLABEL_10; } v16 =1; sub_D57E50((int)&dword_D627C0,"n========================================"); sub_C915B0(Time); sub_D57E50((int)&dword_D627C0," *** SUCCESS! *** "); sub_C915B0(Time); sub_D57E50((int)&dword_D627C0,"========================================"); sub_C915B0(Time); sub_D57E50((int)&dword_D627C0,"[+] Congratulations! You cracked it!"); sub_C915B0(Time); v11 = sub_D57E50((int)&dword_D627C0,"[+] Correct flag: "); sub_D54330(v11, v22, v23); } else { v16 =1; sub_D57E50((int)&dword_D627C0,"n[X] Access Denied!"); sub_C915B0(Time); sub_D57E50((int)&dword_D627C0,"[X] Wrong password. Keep trying!"); } sub_C915B0(Time); gotoLABEL_17; } sub_D57E50((int)&dword_D627C0,"n[!] Nice try, but not quite right...");LABEL_9: sub_C915B0(Time);LABEL_10: sub_C917C0();std::
string::
_M_dispose(v13); sub_C9C600(v15);return0;}
复制代码隐藏代码bool__cdeclsub_C916D0(inta1,inta2){unsigned__int8 *Block;// ebpintv3;// eaxintv4;// ebxboolv5;// dl Block = (unsigned__int8 *)sub_D5B710(0x64u); sub_C91620(Block);// 在这里动态生成Flagif( a2 <=0)// 此处下断点断下后直接查看Block的值即可 { v4 =0; }else { v3 =0; v4 =0; do { v5 = *(char*)(a1 + v3) == Block[v3]; ++v3; v4 += v5; } while( a2 != v3 ); } j_j_free(Block);returna2 == v4;}
复制代码隐藏代码packageu1;publicfinalclassmextendsK1.limplementsJ1.f { /* 伪代码经过删减 */ publicm(InterfaceC0772V interfaceC0772V, InterfaceC0772V interfaceC0772V2, InterfaceC0772V interfaceC0772V3, InterfaceC0772V interfaceC0772V4, InterfaceC0772V interfaceC0772V5, InterfaceC0772V interfaceC0772V6, C0826g c0826g, InterfaceC0772V interfaceC0772V7, InterfaceC0772V interfaceC0772V8, InterfaceC0772V interfaceC0772V9, Context context, View view, InterfaceC0097w interfaceC0097w){ super(3); /* ... */ this.f7612q = interfaceC0772V7;// Flag从这里读, 不过其实我不知道这是个啥结构 } @Override// J1.f publicfinalObjectd0(Object obj, Object obj2, Object obj3){ C0810uc0810u=(C0810u) obj2; intintValue=((Number) obj3).intValue(); if((intValue &14) ==0) { intValue |= c0810u.f(cVar) ?4:2; } if((intValue &91) ==18&& c0810u.A()) { c0810u.T(); }else{ /* ... */ J0j04=this.f7612q; Stringstr=(String) j04.getValue();// this.q.getValue() 为flag字符串 InterfaceC0772VinterfaceC0772V5=this.f7608m; if(str !=null) {// 如果没拼好的话就是空字符串 H.mf6=androidx.compose.foundation.layout.d.f(androidx.compose.foundation.layout.a.e(bVar3.a(H.a.f351j), z8 ?6:10, z8 ? -16: a(g4) -20), z8 ?42:48); c0810u.Y(1157296644); booleanf7=c0810u.f(interfaceC0772V5); ObjectD3=c0810u.D(); if(f7 || D3 == obj4) { z6 =false; D3 =newf(interfaceC0772V5,0); c0810u.j0(D3); }else{ z6 =false; } c0810u.t(z6); /* 代码经过删减 */ c0810u.t(false); H.ma4=androidx.compose.ui.graphics.a.a(b4, (J1.c) D4); c0286i3 = c0286i10; c0286i4 = c0286i9; interfaceC0772V = interfaceC0772V5; j02 = j04; M1.a.b(Q2,"查看FLAG", a4,null, g6,0.0f,null, c0810u,24632,104); z2 =true; z3 =false; K1.i.y(c0810u,false,true,false,false); }else{ c0286i2 = c0286i14; c0286i3 = c0286i11; interfaceC0772V = interfaceC0772V5; j02 = j04; c0286i4 = c0286i13; z2 =true; z3 =false; } /* ... */ } returnC0847j.f8294a; }}
复制代码隐藏代码Java.perform(function() { varLog=Java.use("android.util.Log"); varThrowable=Java.use("java.lang.Throwable"); functionprintStack(tag) { varstack =Log.getStackTraceString(Throwable.$new()); console.log("==== "+ tag +" ===="); console.log(stack); } letm =Java.use("u1.m"); m["$init"].implementation=function(interfaceC0772V, interfaceC0772V2, interfaceC0772V3, interfaceC0772V4, interfaceC0772V5, interfaceC0772V6, c0826g, interfaceC0772V7, interfaceC0772V8, interfaceC0772V9, context, view, interfaceC0097w) { printStack() console.log(`m.$init is called: interfaceC0772V=${interfaceC0772V}, interfaceC0772V2=${interfaceC0772V2}, interfaceC0772V3=${interfaceC0772V3}, interfaceC0772V4=${interfaceC0772V4}, interfaceC0772V5=${interfaceC0772V5}, interfaceC0772V6=${interfaceC0772V6}, c0826g=${c0826g}, interfaceC0772V7=${interfaceC0772V7}, interfaceC0772V8=${interfaceC0772V8}, interfaceC0772V9=${interfaceC0772V9}, context=${context}, view=${view}, interfaceC0097w=${interfaceC0097w}`); this["$init"](interfaceC0772V, interfaceC0772V2, interfaceC0772V3, interfaceC0772V4, interfaceC0772V5, interfaceC0772V6, c0826g, interfaceC0772V7, interfaceC0772V8, interfaceC0772V9, context, view, interfaceC0097w); };})
复制代码隐藏代码java.lang.Throwable at u1.m.(Native Method)// 构造函数 at t1.k.d(SourceFile:89) at p1.a.g0(SourceFile:59) at D.e.g0(SourceFile:57) at K1.i.s(SourceFile:5) at w.v.a(SourceFile:
177) at androidx.compose.material3.E0.a(SourceFile:90)
复制代码隐藏代码publicstaticfinalvoidd(g p0,u p1,intp2,intp3);
复制代码隐藏代码packagew1.g;publicfinalclassgextendsa{ publicfinalB e; publicA f; publicb g; publicbooleanh; publicfinalQ i; publicfinalz j; publicfinalQ k;/* 这个是存储Flag的 Property */ publicfinalz l; publicfinalQ m; publicfinalz n; publicA o; publicvoidg(Application p0){ k.e(p0,"application"); super(p0); ContextapplicationC=p0.getApplicationContext(); k.d(applicationC,"getApplicationContext(...)"); this.e =newB(applicationC); this.g = b.i; Qq=D.b(c.a()); this.i = q; this.j =newz(q); q = D.b(null); this.k = q; this.l =newz(q); q = D.b(Boolean.FALSE); this.m = q; this.n =newz(q); } /* 省略了 */}
复制代码隐藏代码packagew1.d;publicfinalclassdextendsjimplementse // class@000c40 from classes.dex{ publicintm; publicfinalg n; publicfinalString o; publicvoidd(g p0,String p1,d p2){// o又是p1, 在F.C被初始化 this.n = p0; this.o = p1; super(2, p2); } publicfinaldf(d p0,Object p1){ returnnewd(this.n,this.o, p0); } publicfinalObjectg0(Object p0,Object p1){ returnthis.f(p1, p0).i(j.a); } publicfinalObjecti(Object p0){ ai=a.i; dtm=this.m; dtn=this.n; booleanb=true; if(tm !=null) { if(tm == b) { v.l(p0); }else{ thrownewIllegalStateException("call to 'resume' before 'invoke' with coroutine"); } }else{ /* 播放声音, 不过我并没有听到, 其实如果直接从声音下手更好 */ v.l(p0); p0 = tn.e; Stringstr="mdx.aac"; try{ p0.getClass(); p0.v(); MediaPlayermediaPlayer=newMediaPlayer(); AssetFileDescriptoruAssetFileDe=p0.j.getAssets().openFd(str); k.d(uAssetFileDe,"openFd(...)"); mediaPlayer.setDataSource(uAssetFileDe.getFileDescriptor(), uAssetFileDe.getStartOffset(), uAssetFileDe.getLength()); uAssetFileDe.close(); mediaPlayer.setLooping(b); mediaPlayer.prepare(); mediaPlayer.start(); p0.k = mediaPlayer; label_005f : this.m = b; if(x.f(2000,this) == i) { returni; } }catch(java.io.IOException e12){ }catch(java.lang.IllegalStateException e12){ } e12.printStackTrace(); gotolabel_005f ; } tn.k.k(this.o);/* 这里将k设置为this.o */ returnj.a; }}
复制代码隐藏代码packageF.C;publicfinalclassCextendslimplementsc // class@000072 from classes.dex{ publicfinalintj; publicfinalObject k; publicvoidC(intp0,Object p1){ this.j = p0; this.k = p1; super(1); } publicfinalObjectq0(Object p0){ switch(c.j){ /* 没用的case全删了 */ case25: k.e(uoa,"part"); StringBuilderstr=""; i = uoa.length; for(; i3 < i; i3 = i3 + i4) { e = c.k; c1 = i3 % e.length; d = e[c1] &0x00ff; b = uoa[i3] ^ d; str = str.append((char)b); } Stringstr1=str; k.d(str1,"toString(...)"); returnstr1; case28:// 判断 r = uoa.intValue(); k = c.k; gi8=k.i; bvalue=i8.getValue(); if(value.c ==null&& (uob = a.a0(value, r)) !=null) { /* ... */ bc2=j.c; if(r && c2 ==null) { if((f8 = k.f) !=null) { f8.a(uoe); } k.f = x.r(H.q(k), uoe, i3,newe(k, uoe),3); } if(c2 !=null) { if(c2 !=null) { c2 = j.a; if(k.a(c2, b.h)) {// 检查是否完成拼图 Iteratoriterator1=c2.iterator(); longl5=0; d = i3; while(true) { if(iterator1.hasNext()) { obj = iterator1.next(); i10 = d +1; if(d >=0) { l5 = l5 * (long)31; d = obj.intValue() * i10; l5 = l5 + (long)d; d = i10; }else{ l.k(); throwuoe; } }elseif((l5 ^0x12345678) -0xe30fe54d0){// 校验拼图的HASH? byte[] uobyteArray =newbyte[i1];// 解密密钥 uobyteArray[i3] = (byte)54; uobyteArray[i4] = (byte)i4; uobyteArray[i2] =22; uobyteArray[3] =28; int[][] a2 = a.a;// 这是flag密文 uC =newC(25, uobyteArray);// 跳转到case 25进行解密 AppendableuAppendable=""; c1 = i3; i1 = c1; for(; c1 <6; c1 = c1 + i4) { objectoobject=a2[c1]; if((i1 = i1 + i4) > i4) { uAppendable = uAppendable.append(""); } c.g(uAppendable, oobject, uC); } uoe2 = uAppendable+""; k.d(uoe2,"joinTo(StringBuilder(), …ed, transform).toString()"); label_020b : if(uoe2 !=null) { x.r(H.q(k), uoe, i3,newd(k, uoe2, uoe),3); } } } } } uoe2 = uoe; gotolabel_020b ; } } returnj.a; break; } }}
复制代码隐藏代码key = [54,1,22,28]cipher_blocks = [ [80,109,119,123,77], [97,116,34,45,105], [ord('f'),ord('1'),ord('|'),ord('-'),5,ord('^')], [4,49,36,42,105], [ord('e'),ord('q'),ord('d'),ord('-'),ord('X'),ord('f'),ord('I')], [ord('p'),ord('2'),ord('e'),ord('h'),7,ord('w'),ord('"'),ord('p'),ord('K')]]flag =""forblockincipher_blocks: foriinrange(len(block)): # 原代码：c1 = i3 % e.length; d = e[c1] & 0x00ff; current_key = key[i %len(key)] # 原代码：b = uoa[i3] ^ d; char_code = block[i] ^ current_key # 拼接字符串 flag +=chr(char_code)print(flag)
复制代码隐藏代码importhashlibimportbase64importsysdefxor_decrypt(data, key): """XOR解密""" result =bytearray() fori, byteinenumerate(data): result.append(byte ^ key ^ i &255) returnresult.decode('utf-8', errors='ignore')defget_encrypted_flag(): """获取加密的flag""" enc_data ='e3w+fiRvfW18fnx4ZAZ6Pj43YwB9OWMXfXo8Dg4O' returnbase64.b64decode(enc_data)defgenerate_flag(): """动态生成flag""" encrypted = get_encrypted_flag() key =78 result =bytearray() fori, byteinenumerate(encrypted): result.append(byte ^ key) returnresult.decode('utf-8')defcalculate_checksum(s): """计算校验和""" total =0 fori, cinenumerate(s): total +=ord(c) * (i +1) returntotaldefhash_string(s): """计算字符串哈希""" returnhashlib.sha256(s.encode()).hexdigest()defverify_flag(user_input): """验证flag""" correct_flag = generate_flag() iflen(user_input)!=len(correct_flag): returnFalse else: foriinrange(len(correct_flag)): ifuser_input[i]!= correct_flag[i]: returnFalse returnTruedeffake_check_1(user_input): """假检查1""" fake_hash ='a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890' returnhash_string(user_input) == fake_hashdeffake_check_2(user_input): """假检查2""" fake_hash ='1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef' returnhash_string(user_input) == fake_hashdefmain(): """主函数""" print('==================================================') print(' CrackMe Challenge - Python Edition') print('==================================================') print('Keywords: 52pojie, 2026, Happy New Year') print('Hint: Decompile me if you can!') print('--------------------------------------------------') user_input =input('n[?] Enter the password: ').strip() iffake_check_1(user_input): print('n[!] Nice try, but not quite right...') input('nPress Enter to exit...') returnNone else: iffake_check_2(user_input): print('n[!] You're getting closer...') input('nPress Enter to exit...') else: ifverify_flag(user_input): checksum = calculate_checksum(user_input) expected_checksum = calculate_checksum(generate_flag()) ifchecksum == expected_checksum: print('n==================================================') print(' *** SUCCESS! ***') print('==================================================') print('[+] Congratulations! You cracked it!') print(f'[+] Correct flag:{user_input}') else: print('n[!] Checksum failed!') else: print('n[X] Access Denied!') print('[X] Wrong password. Keep trying!') input('nPress Enter to exit...')if__name__ =='__main__': try: main() exceptKeyboardInterrupt: print('nn[!] Interrupted by user') sys.exit(0)
复制代码隐藏代码操作系统:
Windows(Server2003)[AMD64, 64 位, 控制台](Heur)语言:
C打包工具:
Nuitka[OneFile](Heur)打包工具:
Compressedorpackeddata[High entropy + Section 10 (".rsrc") compressed]
复制代码隐藏代码
# 这个代码在吾爱另一位佬的文章里importioimportstructdefread_uint32(bio): returnstruct.unpack(" '{decrypted_part}'") flag += decrypted_part print("-"*50) print(f"[+] 最终解密出的 Flag:{flag}") print(f"[+] 字符总长度:{len(flag)}(符合常量池中的 _total_len: 30)")if__name__ =='__main__': decrypt_flag()
复制代码隐藏代码localfunctiongetWinMessage() localcontent =nil iflove.filesystem.getInfo("assets/flag.dat")then content = love.filesystem.read("assets/flag.dat") end ifnotcontentorcurrentDifficulty ~="hard"then return"You WIN!" end localkey ="52pojie" localkeyLen =#key localresult = {} localbit =require("bit") fori =1,#contentdo localb =string.byte(content, i) localk =string.byte(key, ((i -1) % keyLen) +1) table.insert(result,string.char(bit.bxor(b, k))) end returntable.concat(result)end
复制代码隐藏代码INT_PTR __fastcallDialogFunc(HWND a1,inta2, __int16 a3){// 类型定义被我吃了if( a2 ==272) { /* 这个分支是初始化, 我省略了 */ }elseif( a2 ==273) { if( a3 ==10) { MessageBoxW(a1, &::
Text, &word_14000A152,0x40u); } elseif( a3 ==11) { *(_QWORD *)Str =0; memset(String,0,0x200u); GetDlgItemTextW(a1,2, String,255); v5 = _wfopen(String, aR); if( v5 ) { GetDlgItemTextW(a1,3, String,255); v6 = _wfopen(String,L"wb");// 打开文件 if( v6 ) { GetDlgItemTextA(a1,4, Str,79); v7 = sub_140008720(Str, v5, v6);// 解密函数, 传入Flag, 输入文件, 输出文件 fclose(v5); fclose(v6); memset(Text,0,sizeof(Text)); sub_140008D70((__int64)Text); if( v7 ) MessageBoxW(a1, Text, &word_14000A078,0x10u); else MessageBoxW(a1, Text, &Caption,0x40u); } else { fclose(v5); MessageBoxW(a1, &word_14000A0B0, &word_14000A078,0x10u); } } else { MessageBoxW(a1, &word_14000A080, &word_14000A078,0x10u); } } }else { result =0; if( a2 !=16) returnresult; EndDialog(a1,0); }return1;}
复制代码隐藏代码__int64 __fastcallsub_140008720(char*Str, FILE *Stream, FILE *a3){size_tv6;// rax __int64 v7;// rdicharv8;// dl __int64 result;// rax __int64 v10;// rdiunsigned__int64 v11;// r13char*v12;// raxchar*v13;// r12 __int64 v14;// rdxunsignedintv15;// r8dunsigned__int64 v16;// rax _DWORD Buffer[4];// [rsp+20h] [rbp-858h] BYREFunsigned__int64 v18[265];// [rsp+30h] [rbp-848h] BYREF CRC32_Init((__int64)v18);// 打开之后有一个很经典的CRC常数, 那很显然了吧? CRC32_Update(v18,"52pojie_2026_",14); v6 =strlen(Str); CRC32_Update(v18, Str, v6); v7 = CRC32_Final(v18);// 将"52pojie_2026_"和输入的Flag进行CRC, 然后存入v18 fread(Buffer,0x10u,1u, Stream);// 此处读取了输入文件的前0x10(16)个字节 v8 = sub_140008310((__int64)v18, v7, Buffer);// 这里是密钥派生部分吧 (具体跟进去看) result =1;if( v8 ) { fseek(Stream,0,2); v10 = ftell(Stream); result =2; v11 = v10 -16; if( (v10 &7) ==0) { fseek(Stream,16,0); v12 = (char*)malloc(v10 -16); v13 = v12; if( v12 ) { fread(v12,1u, v10 -16, Stream); sub_1400081E0((__int64)v18, (__int64)v13, v10 -16);// v18: 大数组, v13: 输入, v10-16: payload长度(?) if( (unsigned__int8)sub_1400082E0(v18, v14, v15) )// 这里是一个校验 { v16 = (unsigned__int8)v13[v10 -17];// PKCS#7填充 if( v11 < v16 ) { free(v13); return5; } else { fwrite(v13,1u, v11 - v16, a3); free(v13); return0; } } else { free(v13); return4; } } else { return3; } } }returnresult;}
复制代码隐藏代码__int64 __fastcallsub_140008310(__int64 a1, __int64 a2, _DWORD *a3){ __int64 result;// raxintv6;// eax result =0;if( a3 ) { if( *a3 ==909266243)// a3是输入文件, 比较开头前四字节是否为CM26 { sub_140008360((_QWORD *)a1, a2, (__int64)(a3 +2));// 后八字节作为IV v6 = a3[1];// 再之后四字节被存储到v6, 这里反编译应该是错了, 这是实际上是个CRC校验和 *(_DWORD *)(a1 +288) =-1; *(_DWORD *)(a1 +292) = v6; return1; } }returnresult;}void*__fastcallsub_140008360(_QWORD *a1, __int64 a2, __int64 a3)// a1: Key, a3: IV{ __int64 v3;// rax v3 =0; *a1 = a2;do { *((_BYTE *)a1 + v3 +16) = *(_BYTE *)(a3 + v3); ++v3; }while( v3 !=16);returnmemcpy(a1 +4, &unk_14000A270,0x100u);// unk_14000A270其实就是AES S-BOX...}
复制代码隐藏代码CM26 (前4) CRC校验和(中间4)IV(后4)
复制代码隐藏代码// 哇哦, 这是什么东西// a1, 大数组, a2输入, a3长度__int64 __fastcallsub_1400081E0(unsigned__int64 *a1, __int64 a2, __int64 a3){unsigned__int64 v3;// rbxunsigned__int64 v5;// rdi _DWORD *v6;// r12 __int64 result;// rax v3 = a2 -24627; v5 = a2 -24627+ (a3 &0xFFFFFFFFFFFFFFF8uLL);if( a2 -24627< v5 ) { v6 = a1 +36; do { v3 +=8LL;// 从这里我们可以发现, 他是8个字节为一组进行解密的 sub_140008080(a1, (__int64 *)(v3 +24619)); result = sub_140008480(v6, v3 +24619,8); } while( v3 < v5 ); }returnresult;}char__fastcallsub_140008080(unsigned__int64 *a1, __int64 *a2){intv2;// r8dunsigned__int64 v3;// r11 __int64 v5;// raxchar*v6;// rcxunsigned__int64 v7;// rax __int64 *v8;// rdxcharv9;// alcharresult;// al v2 =8; v3 = *a2; v5 = *a1; v6 = (char*)a1 -21569; v7 = __ROL8__(v5,3);do { v7 = (v7 <<8) | *((unsigned__int8 *)a1 + (HIBYTE(v7) |0x221300) -2233056); --v2; }while( v2 ); *a1 = v7; v8 = a2 +4711;do { v9 = *((_BYTE *)v8 -37688); ++v6; v8 = (__int64 *)((char*)v8 +1); result = v6[21568] ^ v6[21584] ^ v9;// 偏移相差 16 字节. 回到初始化那边看的话其实就是密钥流和IV, v9是密文 *((_BYTE *)v8 -37689) = result; }while( v6 != (char*)a1 -21561); a1[2] = v3;// 这里是解密之前的密文块returnresult;}
复制代码隐藏代码importstructimportzlibimportos
# 标准 AES S-BoxAES_SBOX = [ 0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76, 0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0, 0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15, 0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75, 0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84, 0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF, 0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8, 0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2, 0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73, 0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB, 0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79, 0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08, 0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A, 0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E, 0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF, 0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16]# 生成 AES 逆 S-Box (用于倒推密钥)AES_INV_SBOX = [0] *256fori, valinenumerate(AES_SBOX): AES_INV_SBOX[val] = idefrotl64(x, y): """64位循环左移""" return((x << y) | (x >> (64- y))) &0xFFFFFFFFFFFFFFFFdefrotr64(x, y): """64位循环右移""" return((x >> y) | (x << (64- y))) &0xFFFFFFFFFFFFFFFFdefrecover_key_from_png(iv_bytes, ciphertext_block0): """ 已知明文攻击 (KPA)：通过 PNG 文件头逆推 64位主密钥 """ # 所有的 PNG 文件必然以这 8 个字节开头，刚好满足一个加密块大小 (8 bytes) png_magic =b'x89x50x4Ex47x0Dx0Ax1Ax0A' # 1. 因为 Plaintext = Keystream ^ IV ^ Ciphertext # 所以 Keystream = Plaintext ^ IV ^ Ciphertext k_bytes =bytearray(8) foriinrange(8): k_bytes[i] = png_magic[i] ^ iv_bytes[i] ^ ciphertext_block0[i] # 2. 逆推 Key 生成算法 # 在原算法中，rotl64 是在 8 次 S-Box 循环的外部执行的。 # 所以最终生成的 Keystream 实际上就是 rotl64(Key, 3) 的每一个独立字节经过 SBox 的结果。 t0_bytes =bytearray(8) foriinrange(8): # 通过逆向 S-Box 还原出 rotl64(Key, 3) 时的原始字节 t0_bytes[i] = AES_INV_SBOX[k_bytes[i]] # 组合成 64 位整数 T0 t0 = struct.unpack('<Q', t0_bytes)[0] # 逆向循环左移 3 位 (即循环右移 3 位) 恢复出完全准确的初始 Key64 k_current = rotr64(t0,3) returnk_currentdefdecrypt_cm26_file_kpa(input_path, output_path): """基于已知明文攻击的无密码解密主逻辑""" withopen(input_path,'rb')asf: file_data = f.read() iflen(file_data) <16: raiseValueError("文件太小，不是有效的 CM26 文件") # 1. 解析头部 magic, expected_crc, iv = struct.unpack('<4sI8s', file_data[:16]) ifmagic !=b'CM26': raiseValueError(f"文件特征码不匹配，预期为 CM26，实际为:{magic}") iv_array =bytearray(iv) ciphertext = file_data[16:] iflen(ciphertext) %8!=0: raiseValueError("加密数据大小不是 8 的倍数，文件可能已损坏") # 2. 实施已知明文攻击，直接从加密文件中逆推初始密钥 print(" 正在执行已知明文攻击 (PNG Magic KPA)...") key64 = recover_key_from_png(iv_array, ciphertext[:8]) print(f"[+] 攻击成功！恢复出原始 64 位 Key: 0x{key64:
016X}") plaintext_padded =bytearray() # 3. 逐块解密循环 foroffsetinrange(0,len(ciphertext),8): block = ciphertext[offset:
offset+8] # 3.1 生成当前块的 64 位 Keystream # 修复：循环左移 3 位是在 8 次 S-Box 替换循环的 *外部* 发生的 k = rotl64(key64,3) for_inrange(8): idx = (k >>56) &0xFF sbox_val = AES_SBOX[idx] k = ((k <<8) &0xFFFFFFFFFFFFFFFF) | sbox_val key64 = k # 3.2 异或解密 k_bytes = struct.pack('<Q', k) pt_block =bytearray(8) foriinrange(8): pt_block[i] = k_bytes[i] ^ iv_array[i] ^ block[i] plaintext_padded.extend(pt_block) # 3.3 更新 IV iv_array =bytearray(block) # 校验 CRC32 actual_crc = zlib.crc32(plaintext_padded) &0xFFFFFFFF ifactual_crc != expected_crc: print(f"警告: CRC32 校验失败! (预期:{hex(expected_crc)}, 实际:{hex(actual_crc)})") # PKCS#7 ifplaintext_padded: padding_len = plaintext_padded[-1] ifpadding_len >0andpadding_len <=8: plaintext = plaintext_padded[:-padding_len] else: plaintext = plaintext_padded else: plaintext = plaintext_padded withopen(output_path,'wb')asf: f.write(plaintext)if__name__ =="__main__": in_file ="flag.png.encrypted" out_file ="flag.png" decrypt_cm26_file_kpa(in_file, out_file)
复制代码隐藏代码packagecom.zj.wuaipojie2026_2;importf1.h;importjava.nio.ByteBuffer;importjava.nio.ByteOrder;/* loaded from: classes.dex */publicfinalclassNativeBridge{ publicstaticfinalint$stable=0; publicstaticfinalintERR_CHEAT=-7; publicstaticfinalNativeBridgeINSTANCE=newNativeBridge(); publicstaticfinalintSCORE_GOOD=1; publicstaticfinalintSCORE_MISS=0; publicstaticfinalintSCORE_PERFECT=2; static{ System.loadLibrary("hajimi"); } privateNativeBridge(){ } privatefinalnativevoidstartSessionBytes(longj2,byte[] bArr,inti2); publicfinalnativeintcheckRhythm(longj2,inti2,longj3,inti3); publicfinalnativebyte[] decryptFrames(byte[] bArr,longj2); publicfinalnativevoidsetDebugBypass(booleanz2);// 设置调试模式(?) 反正这玩意必须得自己设置 publicfinalvoidstartSession(longj2,int[] iArr,inti2){ h.e(iArr,"beatMapMs"); ByteBufferorder=ByteBuffer.allocate(iArr.length *4).order(ByteOrder.LITTLE_ENDIAN); for(inti3 : iArr) { order.putInt(i3); } byte[] array = order.array(); h.d(array,"array(...)"); startSessionBytes(j2, array, i2); } publicfinalnativelongupdateExp(inti2,inti3,longj2); publicfinalnativebyte[] verifyAndDecrypt(byte[] bArr, String str);// 需要逆向的是这个函数, bArr是hjm_pack.bin文件内容, Str是用户输入的Flag}
复制代码隐藏代码jintJNI_OnLoad(JavaVM *vm,void*reserved){ JavaVM v2;// x8 __int64 v4;// x0 _QWORD v5[2];// [xsp+0h] [xbp-10h] BYREF v5[1] = *(_QWORD *)(_ReadStatusReg(TPIDR_EL0) +40); v2 = *vm; v5[0] =0;if( v2->GetEnv(vm, (void**)v5,65542) ) return-1; v4 = (*(__int64 (__fastcall **)(_QWORD, constchar*))(*(_QWORD *)v5[0] + 48LL))( v5[0], "com/zj/wuaipojie2026_2/NativeBridge");if( !v4 ) return-1;if( (*(unsignedint(__fastcall **)(_QWORD, __int64,char**, __int64))(*(_QWORD *)v5[0] + 1720LL))( v5[0], v4, off_5E6F8, 6) )// 此处动态注册, off_5E6F8是表 { return-1; }return65542;}
复制代码隐藏代码名称 (字符串)签名 (字符串)函数
复制代码隐藏代码void__fastcallsub_25C90(JNIEnv *a1,void*a2, jboolean a3){ DebugFlag = a3 ==1;// 先给他改个名, 不然逆向verifyAndDecrypt的时候得晕}
复制代码隐藏代码jbyteArray __fastcallverifyAndDecrypt(JNIEnv *vm,void*reserved, jbyteArray *bArr, jstring *Str){ JNIEnv v5;// x8intv8;// w0size_tv9;// x23unsignedintv10;// w21char*v11;// x0char*v12;// x25char*v13;// x19 JNIEnv v14;// x8 jbyteArray v15;// x0 jbyteArray v16;// x22unsigned__int64 v18;// x0intv19;// w10 __int64 v20;// x9 __int64 v21;// x8unsigned__int64 v22;// x9unsigned__int64 v23;// x9unsigned__int64 v24;// x10 __int128 v25;// t2intv26;// w26intv27;// w10intv28;// w24intv29;// w25intv30;// w8 __int64 v31;// x0doublev32;// d0doublev33;// d1longdoublev34;// q2int8x16_tv35;// q3int8x16_tv36;// q4int8x8_tv37;// d5constchar*InpStr;// x26intv39;// w28charv40;// w24size_tv41;// x2unsigned__int64 v42;// x0unsigned__int64 v43;// x1 __int64 a1;// [xsp+8h] [xbp-38h] BYREFintv45[2];// [xsp+10h] [xbp-30h]intv46[2];// [xsp+18h] [xbp-28h]void*s2[4];// [xsp+20h] [xbp-20h] BYREF s2[3] = *(void**)(_ReadStatusReg(TPIDR_EL0) +40); v5 = *vm;if( bArr && Str ) { v8 = v5->GetArrayLength(vm, bArr); if( v8 >0) { v9 = (unsignedint)v8; v10 = v8; v11 = (char*)operator new((unsignedint)v8); v12 = &v11[v9]; v13 = v11; a1 = (__int64)v11; *(_QWORD *)v46 = &v11[v9]; memset(v11,0, v9); v14 = *vm; *(_QWORD *)v45 = v12; v14->GetByteArrayRegion(vm, bArr,0, v10, v13); if( v10 <=0x33|| *(_DWORD *)v13 !=827148872)// 长度检测&文件头检测 gotofail; v18 = env_check(vm); // 就这个环境检测, 老长了... v19 = dword_5EA50 + HIDWORD(v18); v20 = dword_5EA4C | (unsignedint)v18; if( dword_5EA50 + HIDWORD(v18) >=12) v19 =12; dword_5EA4C |= v18; dword_5EA50 = v19; if( v19 <4) { v21 = qword_5EA28; if( byte_5EA54 !=1) { v26 =0; gotoLABEL_20; } } else { v21 = qword_5EA28; byte_5EA54 =1; } v22 = (v19 ^ (unsigned__int64)(v20 <<32) ^0x1A8CBC5B802E097CLL) -0x61C8864680B583EBLL; v23 =0x94D049BB133111EBLL * ((0xBF58476D1CE4E5B9LL * (v22 ^ (v22 >>30))) ^ ((0xBF58476D1CE4E5B9LL * (v22 ^ (v22 >>30))) >>27)); v24 = v23 ^ (v23 >>31); if( v24 ) { *((_QWORD *)&v25 +1) = v23 ^ (v23 >>31); *(_QWORD *)&v25 = v23; v21 ^= (v25 >>35) ^ v24; } v26 =1;LABEL_20: v27 = *((_DWORD *)v13 +2); qword_5EA30 = v21; if( v27 ) { v28 = *((_DWORD *)v13 +3); if( v28 ) { v29 = *((_DWORD *)v13 +4); if( v29 ) { v30 = *((_DWORD *)v13 +1); if( v30 ==2) { if( (v26 | (unsigned__int8)byte_5EA40) &1| (DebugFlag !=0) )// 启用调试之后可以在直接把环境监测数值改为0的情况下, 走正常分支 { if( DebugFlag ) v42 = sub_2DCDC(); else v42 = qword_5EA38; if( v26 ) v43 = v42 ^0xA5A5A5A5A5A5A5A5LL; else v43 = v42; if( (sub_2DDF8(&a1, v43) &1) ==0) {LABEL_47: v15 = (*vm)->NewByteArray(vm,0); gotoLABEL_7; }LABEL_29: InpStr = (*vm)->GetStringUTFChars(vm, Str,0); if( InpStr ) { v39 = v29 * v28; sub_2D46C(s2, (unsignedint)(v29 * v28) >>3); v40 = sub_2E5FC(InpStr, v28, v29, s2[0], (char*)s2[1] - (char*)s2[0]);// 将输入的字符串"渲染"成点阵图, 后续直接将其与解密得到的位图进行比较) (*vm)->ReleaseStringUTFChars(vm, Str, InpStr); if( (v40 &1) !=0 && (unsignedint)v39 >=8 && (v41 = (unsigned__int64)v39 >>3, v41 +52<= v9) && !memcmp(v13 +52, s2[0], v41) )// 此处为比较代码, v13 + 52是FLAG的内容的地址, s2[0]是输入的字符串渲染成的点阵图, 比较长度(v41)为512 { v16 = (*vm)->NewByteArray(vm, v10); (*vm)->SetByteArrayRegion(vm, v16,0, v10, v13); } else { v16 = (*vm)->NewByteArray(vm,0); } if( s2[0] ) { s2[1] = s2[0]; operatordelete(s2[0]); } gotoLABEL_8; } gotoLABEL_47; } } elseif( v30 ==1) { if( v26 ) v31 =1515870653; else v31 =999; sub_2D4F0(v31, (_QWORD *)v13 +3, (__int64 *)v13 +5, (unsigned__int64 *)s2); sub_2D678((__int64)(v13 +52), v9 -52, s2, v13 +40, v32, v33, v34, v35, v36, v37);// AES-128? gotoLABEL_29; } } } }fail: v15 = (*vm)->NewByteArray(vm,0);LABEL_7: v16 = v15;LABEL_8: operatordelete(v13); returnv16; } v5 = *vm; }returnv5->NewByteArray(vm,0);}
复制代码隐藏代码returnv332 | (unsignedint)v340 | (unsigned__int64)(v324 <<32);
复制代码隐藏代码干净环境返回值 = 0x0000000000000000
复制代码隐藏代码constTARGET_LIB="libhajimi.so";constANTI_DEBUG_OFFSET=0x25ef8; // 此处填入从IDA中找到的环境检测函数的偏移地址Interceptor.attach(Module.findExportByName(null,"android_dlopen_ext"), { onEnter:
function(args) { this.libName= args[0].readCString(); }, onLeave:
function(retval) { if(this.libName&&this.libName.indexOf(TARGET_LIB) !== -1) { letbaseAddr =Module.getBaseAddress(TARGET_LIB); letantiDebugPtr = baseAddr.add(ANTI_DEBUG_OFFSET); Interceptor.replace(antiDebugPtr,newNativeCallback(function(a) { returnptr(0); },'pointer', ['pointer'])); } }});Java.perform(function() { letNativeBridge=Java.use("com.zj.wuaipojie2026_2.NativeBridge"); NativeBridge.INSTANCE.value["setDebugBypass"](true)// 启用Debug})
复制代码隐藏代码__int64sub_2E5FC( constchar*text, // a1: 输入的源字符串 (例如: Flag) intwidth, // a2: 画布总像素宽度 intheight, // a3: 画布总像素高度 void*out_buffer, // s: 输出位图缓冲区 (每 bit 代表一像素) size_tbuffer_n // n: 缓冲区字节大小);
复制代码隐藏代码do{ v58 = v56[v55];// 获取字模的一行数据// ... 检查 v58 的每一位 (0x10, 0x08, 0x04, 0x02, 0x01)// ... 如果位被点亮，计算全局坐标并写入缓冲区}while( v55 !=7);
复制代码隐藏代码/*...*/InpStr = (*vm)->GetStringUTFChars(vm, Str,0);if( InpStr ){ v39 = v29 * v28; sub_2D46C(s2, (unsignedint)(v29 * v28) >>3); v40 = sub_2E5FC(InpStr, v28, v29, s2[0], (char*)s2[1] - (char*)s2[0]);// 这里根据输入绘制 (*vm)->ReleaseStringUTFChars(vm, Str, InpStr);if( (v40 &1) !=0 && (unsignedint)v39 >=8 && (v41 = (unsigned__int64)v39 >>3, v41 +52<= v9) && !memcmp(v13 +52, s2[0], v41) )// 这里将两个图进行比较, 如果相同就返回FLAG图 { v16 = (*vm)->NewByteArray(vm, v10); (*vm)->SetByteArrayRegion(vm, v16,0, v10, v13); }else { v16 = (*vm)->NewByteArray(vm,0); }if( s2[0] ) { s2[1] = s2[0]; operatordelete(s2[0]); }gotoLABEL_8;}gotoLABEL_47;/*...*/
复制代码隐藏代码/* 注意, 此处代码需要配合上面移除环境检测的代码一起使用, 如果hook不上可以和上面的代码在同一时机hook */constTARGET_LIB="libhajimi.so";constMEMCMP_OFFSET=0x25b24; // 此处填入调用MEMCMP的地址letbaseAddr =Module.findBaseAddress(TARGET_LIB);letmemcmpPtr = baseAddr.add(MEMCMP_OFFSET);Interceptor.attach(memcmpPtr.add(4)/* +4 是因为在下一条指令处修改寄存器 (MEMCMP返回值寄存器为x0) */, { onEnter:
function(args) { console.log(this.context.w0) console.log(this.context.x0) this.context.w0=0 this.context.x0=0 }})
复制代码隐藏代码wasm-decompile FileName.wasm -o Result .dcmp
复制代码隐藏代码asyncfunctioninit() { leti =false, w =document.createTreeWalker(document,128), n try{ awaitwasm_bindgen('f.wasm')/* 这里被我改过 */ constaudio =document.getElementById('audioPlayer') audio.volume=0.3 checkboxText.addEventListener('click',async() => { constuidInput =document.getElementById('uid') if(!uidInput.value) { uidInput.focus() return } constuid =parseInt(uidInput.value) ||0 constvoice =document.getElementById('voice').value try{ // 将uid和音色传入wasm导出的gen函数中 constchallenge = wasm_bindgen.gen(uid, voice) /* ... */ } }) /* ... */ } /* ... */}
复制代码隐藏代码// a: 传入的UID// b: voice字符串指针// c: voice字符串长度(?)// return: 一堆指针(音频, Hash)exportfunctiongen(a:
int,b:
int,c:
int): (int, int, int)
复制代码隐藏代码exportfunctiongen(a:
int,b:
int,c:
int):(int, int, int) {// func50/* 省略定义 */wbg_wbg_getRandomValues_1c61fac11405ffdc(d +80,17);// 获取随机字节, 储存在地址d[80]到d[97] c =5412468[0]:
int;vare:
int =5412472[0]:
int;5412468[0]:
long@4= 0L;varg:
int = d +72; g[1]:
int = e; g[0]:
int = c ==1; j =f_zb(37,1);// malloc申请内存, 这里存了Payloadif(j) { // ---- j[3]:
byte = (b = d[83]:
ubyte ^ a >>24); j[2]:
byte = (c = d[82]:
ubyte ^ a >>16); j[1]:
byte = (e = d[81]:
ubyte ^ a >>8); j[0]:
byte = (a = d[80]:
ubyte ^ a); // ---- 上方将UID的4字节与获取的前四个随机字节进行逐字节异或, 并且放入j中前四个字节 // 下方将剩余随机字节复制到j中 j[4]:
long@1= d[10]:
long;// 这里的long是8字节, 所以其实还是复制 (j +12)[0]:
long@1= (d +88)[0]:
long; (j +20)[0]:
byte = (d +96)[0]:
ubyte; /*...*/ }}
复制代码隐藏代码+----------------+------------------+| UID(j[0..3]) | 随机字节(j[4..20])|| 4字节, 小端序 | 17字节 |+----- -----------++----------------+
复制代码隐藏代码exportfunctiongen(a:
int,b:
int,c:
int):(int, int, int) {// func50/* 省略定义 */wbg_wbg_getRandomValues_1c61fac11405ffdc(d +80,17);// 获取随机字节, 储存在地址d[80]到d[97] c =5412468[0]:
int;vare:
int =5412472[0]:
int;5412468[0]:
long@4= 0L;varg:
int = d +72; g[1]:
int = e; g[0]:
int = c ==1; j =f_zb(37,1);// malloc申请内存, 这里存了Payloadif(j) { /*...*/ memory_copy(a,1295967,14);// 从1295967复制14字节Key b = d +416; b[0]:
long@1= a[0]:
long; (b +56)[0]:
long@1= c[0]:
long; (b +48)[0]:
long@1= e[0]:
long; (b +40)[0]:
long@1= f[0]:
long; (b +32)[0]:
long@1= g[0]:
long; (b +24)[0]:
long@1= l[0]:
long; (b +16)[0]:
long@1= i[0]:
long; (b +8)[0]:
long@1= k[0]; g_a = a +352; a =0; /* 0x36 HMAC标准中的ipad */ loop L_w { c = d +416; b = c + a; b[0]:
byte = b[0]:
ubyte ^54; e = b +1; e[0]:
byte = e[0]:
ubyte ^54; e = b +2; e[0]:
byte = e[0]:
ubyte ^54; b = b +3; b[0]:
byte = b[0]:
ubyte ^54; a = a +4; if(a !=64)continueL_w; } a =0; // 下方加载了SHA-256的常量 (d +504)[0]:
long = d_Cahabcdefghijklmnopqrstuvwxy[113@8]:
long; (d +496)[0]:
long = d_Cahabcdefghijklmnopqrstuvwxy[105@8]:
long; (d +488)[0]:
long = d_Cahabcdefghijklmnopqrstuvwxy[97@8]:
long; d[64]:
long = 1L; d[60]:
long = d_Cahabcdefghijklmnopqrstuvwxy[89@8]:
long; f_j(d +480, c,1); /* 再次异或正好得到0x5c, HMAC标准中的opad */ loop L_x { c = d +416; b = c + a; b[0]:
byte = b[0]:
ubyte ^106; e = b +1; e[0]:
byte = e[0]:
ubyte ^106; e = b +2; e[0]:
byte = e[0]:
ubyte ^106; b = b +3; b[0]:
byte = b[0]:
ubyte ^106; a = a +4; if(a !=64)continueL_x; } /* ... 省略很长的代码... 下方将结果大端序的后16字节转为小端序, 组装到Payload */ j[33]:
int@1= ((e = d[77]:
int) <<24| (e &65280) <<8) | ((e >>8&65280) | e >>24); j[29]:
int@1= (c <<24| (c &65280) <<8) | ((c >>8&65280) | c >>24); j[25]:
int@1= (b <<24| (b &65280) <<8) | ((b >>8&65280) | b >>24); j[21]:
int@1= (a <<24| (a &65280) <<8) | ((a >>8&65280) | a >>24); }}
复制代码隐藏代码+----------------+------------------+----------------------+| UID(j[0..3]) | 随机字节(j[4..20])| HMAC-SHA256(j[21..36])|| 4字节, 小端序 | 17字节 | 16字节, 强调是小端序 |+----------------+-----------------+-----------------------+
复制代码隐藏代码exportfunctiongen(a:
int,b:
int,c:
int):(int, int, int) {// func50/* 省略定义 */wbg_wbg_getRandomValues_1c61fac11405ffdc(d +80,17);// 获取随机字节, 储存在地址d[80]到d[97] c =5412468[0]:
int;vare:
int =5412472[0]:
int;5412468[0]:
long@4= 0L;varg:
int = d +72; g[1]:
int = e; g[0]:
int = c ==1; j =f_zb(37,1);// 这里存了Payloadif(j) { /* 上方代码省略 */ if(b) { a =0; d[106]:
int =0; d[105]:
int = b; d[104]:
int =50; f =1; b =0; e = j; loop L_ga { lett0 = e; g = a <<2; e = f + j; l = t0[0]:
ubyte; h = l | h <<8; c = b; loop L_ha { i = (h >> (b = c +2) &63)[1295903]:
ubyte;// base64查表, 经典操作了属于是 if(d[104]:
int == a) {f_na(d +416) } (d[105]:
int + g)[0]:
int = i; d[106]:
int = (a = a +1); c = c -6; g = g +4; if(b >5)continueL_ha; } b = c +8; f = f + (i = f !=37); if(i)continueL_ga; } if(c == -8) goto B_u; b = (l << -2- c &63)[1295903]:
ubyte;// base64结束 if(a == d[104]:
int) {f_na(d +416) } (d[105]:
int + g)[0]:
int = b; d[106]:
int = (a = a +1); goto B_u; } f_nb(4,200); }}
复制代码隐藏代码importosimporthmacimporthashlibimportbase64TRANS =str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/','abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!')KEY =b'x00x01x01x01x01x01x01x00x01x00x01x00x05x02'defMyFlag(UID:
int) ->str: RandomBytes = os.urandom(17) j =bytearray(37) UIDBytes = UID.to_bytes(4,'little') # j[0..3] foriinrange(4): j[i] = UIDBytes[i] ^ RandomBytes[i] j[4:21] = RandomBytes h = hmac.new(KEY, j[:21], hashlib.sha256).digest() j[21:37] = h[:16]# 小端序, 所以前16 returnbase64.b64encode(j).decode().translate(TRANS).replace('=','')
# 魔改print('flag{'+ MyFlag(1354181) +'}')
# 这写自己UID
复制代码隐藏代码if (q !=1) goto B_eb;br_table[...](r[0] -99)// 命中 'c' (99) -> 指向 1048577, 长度 76762// 命中 'e' (101) -> 指向 1125339, 长度 86076// ...
复制代码隐藏代码(a + f)[0]:
int@1=1179011410;//'RIFF'(d[65]:
int+ a)[0]:
int@1=1163280727;//'WAVE'(d[65]:
int+ a)[0]:
int@1=544501094; //'fmt '(d[65]:
int+ a)[0]:
int@1=16; //Subchunk1Size(d[65]:
int+ a)[0]:
short@1=1; //AudioFormat(PCM)(d[65]:
int+ a)[0]:
short@1=1; //NumChannels(单声道)(d[65]:
int+ a)[0]:
int@1=24000; //SampleRate(d[65]:
int+ a)[0]:
int@1=48000; //ByteRate(24000*1*16/8)(d[65]:
int+ a)[0]:
short@1=2; //BlockAlign(d[65]:
int+ a)[0]:
short@1=16; //BitsPerSample(d[65]:
int+ a)[0]:
int@1=1635017060;//'data'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773910845-wxsync-2026-03-f58330fd0eb05c4a28fcf169b472129c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773910847-wxsync-2026-03-7bc04836762861d7162d2cb0e4d90ef1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773910850-wxsync-2026-03-2571e49cb05f166510f2b4fc7cbd50a5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773910851-wxsync-2026-03-487759504b83c964516984ffc2c94184.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773910853-wxsync-2026-03-bfa025429cbf60949c658018aef8a8ad.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773910854-wxsync-2026-03-deaf80fbab5cef15eec0b82d010a9ec9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773910856-wxsync-2026-03-0f03d081adc810d51fd68c66fa5940ae.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773910857-wxsync-2026-03-61638d9c234ef055f414925ead4960a4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773910858-wxsync-2026-03-b7931e29726f4d4c7e84993123bb969a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773910859-wxsync-2026-03-2bf3663f4ee099b36a7b0e2ebc228750.jpeg)