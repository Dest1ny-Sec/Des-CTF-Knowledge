# Buuctf解题思路

> 原文: https://www.ctfiot.com/64553.html
> ID: 64553

声明

[buuctf]刮开有奖

逻辑分析

这道题是无壳32位的程序，利用ida打开，找到main函数。

int __stdcall WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd){ DialogBoxParamA(hInstance, (LPCSTR)0x67, 0, (DLGPROC)DialogFunc, 0); return 0;}

BOOL __userpurge DialogFunc@(int a1@, int a2@, HWND hDlg, UINT a4, WPARAM a5, LPARAM a6){ const char *v6; // esi const char *v7; // edi int v9; // [esp+4h] [ebp-20030h] int v10; // [esp+8h] [ebp-2002Ch] int v11; // [esp+Ch] [ebp-20028h] int v12; // [esp+10h] [ebp-20024h] int v13; // [esp+14h] [ebp-20020h] int v14; // [esp+18h] [ebp-2001Ch] int v15; // [esp+1Ch] [ebp-20018h] int v16; // [esp+20h] [ebp-20014h] int v17; // [esp+24h] [ebp-20010h] int v18; // [esp+28h] [ebp-2000Ch] int v19; // [esp+2Ch] [ebp-20008h] CHAR String; // [esp+30h] [ebp-20004h] char v21; // [esp+31h] [ebp-20003h] char v22; // [esp+32h] [ebp-20002h] char v23; // [esp+33h] [ebp-20001h] char v24; // [esp+34h] [ebp-20000h] char v25; // [esp+10030h] [ebp-10004h] char v26; // [esp+10031h] [ebp-10003h] char v27; // [esp+10032h] [ebp-10002h] int v28; // [esp+20028h] [ebp-Ch]  int v29; // [esp+2002Ch] [ebp-8h] __alloca_probe(); if ( a4 == 272 ) return 1; v29 = a2; v28 = a1; if ( a4 != 273 ) return 0; if ( (_WORD)a5 == 1001 ) { memset(&String, 0, 0xFFFFu); GetDlgItemTextA(hDlg, 1000, &String, 0xFFFF); if ( strlen(&String) == 8 ) { v9 = 90; v10 = 74; v11 = 83; v12 = 69; v13 = 67; v14 = 97; v15 = 78; v16 = 72; v17 = 51; v18 = 110; v19 = 103; sub_4010F0(&v9, 0, 10); memset(&v25, 0, 0xFFFFu); v6 = (const char *)sub_401000(&v25, strlen(&v25)); memset(&v25, 0, 0xFFFFu); v26 = v23; v25 = v22; v27 = v24; v7 = (const char *)sub_401000(&v25, strlen(&v25)); if ( String == v9 + 34 && v21 == v13 && 4 * v22 - 141 == 3 * v11 && v23 / 4 == 2 * (v16 / 9) && !strcmp(v6, "ak1w") && !strcmp(v7, "V1Ax") ) { MessageBoxA(hDlg, "U g3t 1T!", "@_@", 0); } } return 0; } if ( (_WORD)a5 != 1 && (_WORD)a5 != 2 ) return 0; EndDialog(hDlg, (unsigned __int16)a5); return 1;}

int __cdecl sub_4010F0(int a1, int a2, int a3){ int result; // eax int i; // esi int v5; // ecx  int v6; // edx result = a3; for ( i = a2; i <= a3; a2 = i ) { v5 = 4 * i; v6 = *(_DWORD *)(4 * i + a1); if ( a2 < result && i < result ) { do { if ( v6 > *(_DWORD *)(a1 + 4 * result) ) { if ( i >= result ) break; ++i; *(_DWORD *)(v5 + a1) = *(_DWORD *)(a1 + 4 * result); if ( i >= result ) break; while ( *(_DWORD *)(a1 + 4 * i) <= v6 ) { if ( ++i >= result ) goto LABEL_13; } if ( i >= result ) break; v5 = 4 * i; *(_DWORD *)(a1 + 4 * result) = *(_DWORD *)(4 * i + a1); } --result; } while ( i < result ); }LABEL_13: *(_DWORD *)(a1 + 4 * result) = v6; sub_4010F0(a1, a2, i - 1); result = a3; ++i; } return result;}

#include#includeint __cdecl sub_4010F0(char* a1, int a2, int a3){ int result; // eax int i; // esi int v5; // ecx    int v6; // edx result = a3; for (i = a2; i <= a3; a2 = i) { v5 =i; v6 = a1[i]; if (a2 < result && i < result) { do { if (v6 > a1[result]) { if (i >= result) break; ++i; a1[v5] = a1[result]; if (i >= result) break; while (a1[i] <= v6) { if (++i >= result) goto LABEL_13; } if (i >= result) break; v5 =i; a1[result] = a1[i]; } --result; } while (i < result); } LABEL_13: a1[result] = v6; sub_4010F0(a1, a2, i - 1); result = a3; ++i; } return result;}int main() { char str[] = "ZJSECaNH3ng"; sub_4010F0(str, 0, 10); printf("%s", str); return 0;}

_BYTE *__cdecl sub_401000(int a1, int a2){ int v2; // eax int v3; // esi size_t v4; // ebx _BYTE *v5; // eax _BYTE *v6; // edi int v7; // eax _BYTE *v8; // ebx int v9; // edi signed int v10; // edx int v11; // edi signed int v12; // eax signed int v13; // esi _BYTE *result; // eax _BYTE *v15; // [esp+Ch] [ebp-10h] _BYTE *v16; // [esp+10h] [ebp-Ch] int v17; // [esp+14h] [ebp-8h]  int v18; // [esp+18h] [ebp-4h] v2 = a2 / 3; v3 = 0; if ( a2 % 3 > 0 ) ++v2; v4 = 4 * v2 + 1; v5 = malloc(v4); v6 = v5; v15 = v5; if ( !v5 ) exit(0); memset(v5, 0, v4); v7 = a2; v8 = v6; v16 = v6; if ( a2 > 0 ) { while ( 1 ) { v9 = 0; v10 = 0; v18 = 0; do { if ( v3 >= v7 ) break; ++v10; v9 = *(unsigned __int8 *)(v3++ + a1) | (v9 << 8); } while ( v10 < 3 ); v11 = v9 << 8 * (3 - v10); v12 = 0; v17 = v3; v13 = 18; do { if ( v10 >= v12 ) { *((_BYTE *)&v18 + v12) = (v11 >> v13) & 0x3F; v8 = v16; } else { *((_BYTE *)&v18 + v12) = 64; } *v8++ = byte_407830[*((char *)&v18 + v12)]; v13 -= 6; ++v12; v16 = v8; } while ( v13 > -6 ); v3 = v17; if ( v17 >= a2 ) break; v7 = a2; } v6 = v15; } result = v6; *v8 = 0; return result;}

.rdata:
00407830 byte_407830 db 41h ; DATA XREF: sub_401000+C0↑r.rdata:
00407831 aBcdefghijklmno db 'BCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=',0

[buuctf]简单注册器

分析

这是一个apk文件，所以我用jadx来解题，把apk拖入到其中。

进入主函数MainActivity中

package com.example.flag;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v7.app.ActionBarActivity;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;/* loaded from: classes.dex */public class MainActivity extends ActionBarActivity { /* JADX INFO: Access modifiers changed from: protected */ @Override // android.support.v7.app.ActionBarActivity, android.support.v4.app.FragmentActivity, android.app.Activity public void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main); if (savedInstanceState == null) { getSupportFragmentManager().beginTransaction().add(R.id.container, new PlaceholderFragment()).commit(); } Button button = (Button) findViewById(R.id.button1); final TextView textview = (TextView) findViewById(R.id.textView1); final EditText editview = (EditText) findViewById(R.id.editText1); button.setOnClickListener(new View.OnClickListener() { // from class: com.example.flag.MainActivity.1 @Override // android.view.View.OnClickListener public void onClick(View v) { int flag = 1; String xx = editview.getText().toString(); if (xx.length() != 32 || xx.charAt(31) != 'a' || xx.charAt(1) != 'b' || (xx.charAt(0) + xx.charAt(2)) - 48 != 56) { flag = 0; } if (flag == 1) { char[] x = "dd2940c04462b4dd7c450528835cca15".toCharArray(); x[2] = (char) ((x[2] + x[3]) - 50); x[4] = (char) ((x[2] + x[5]) - 48); x[30] = (char) ((x[31] + x[9]) - 48); x[14] = (char) ((x[27] + x[28]) - 97); for (int i = 0; i < 16; i++) { char a = x[31 - i]; x[31 - i] = x[i]; x[i] = a; } String bbb = String.valueOf(x); textview.setText("flag{" + bbb + "}"); return; } textview.setText("输入注册码错误"); } });    } @Override // android.app.Activity public boolean onCreateOptionsMenu(Menu menu) { getMenuInflater().inflate(R.menu.main, menu); return true;    } @Override // android.app.Activity public boolean onOptionsItemSelected(MenuItem item) { int id = item.getItemId(); if (id == R.id.action_settings) { return true; } return super.onOptionsItemSelected(item);    } /* loaded from: classes.dex */ public static class PlaceholderFragment extends Fragment { @Override // android.support.v4.app.Fragment public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) { View rootView = inflater.inflate(R.layout.fragment_main, container, false); return rootView; } }}

if (flag == 1) { char[] x = "dd2940c04462b4dd7c450528835cca15".toCharArray(); x[2] = (char) ((x[2] + x[3]) - 50); x[4] = (char) ((x[2] + x[5]) - 48); x[30] = (char) ((x[31] + x[9]) - 48); x[14] = (char) ((x[27] + x[28]) - 97); for (int i = 0; i < 16; i++) { char a = x[31 - i]; x[31 - i] = x[i]; x[i] = a;                    }之后针对这里进行改写，flag即可出来#include#includeint main() {char x[]= "dd2940c04462b4dd7c450528835cca15";x[2] = ((x[2] + x[3]) - 50);x[4] = ((x[2] + x[5]) - 48);x[30] = (char)((x[31] + x[9]) - 48);x[14] = (char)((x[27] + x[28]) - 97);for (int i = 0; i < 16; i++) {char a = x[31 - i];x[31 - i] = x[i];x[i] = a;}printf("flag{%s}", x);
return 0;}

[buuctf][Zer0pts2020]easy strcmp

思路

第一步还是先查壳

放在linux中运行一下，发现竟然没有任何输入的位置。

放入ida64中查看，因为这个是一个64位的可执行文件，有main函数，直接进入main函数查看

__int64 __fastcall main(signed int a1, char **a2, char **a3){ if ( a1 > 1 ) { if ( !strcmp(a2[1], "zer0pts{********CENSORED********}") ) puts("Correct!"); else puts("Wrong!"); } else { printf("Usage: %sn", *a2, a3, a2); } return 0LL;}

__int64 __fastcall sub_6EA(__int64 a1, __int64 a2){ int i; // [rsp+18h] [rbp-8h] int v4; // [rsp+18h] [rbp-8h]  int j; // [rsp+1Ch] [rbp-4h] for ( i = 0; *(_BYTE *)(i + a1); ++i ) ; v4 = (i >> 3) + 1; for ( j = 0; j < v4; ++j ) *(_QWORD *)(8 * j + a1) -= qword_201060[j]; return qword_201090(a1, a2);}

qword_201060 dq 0, 410A4335494A0942h, 0B0EF2F50BE619F0h, 4F0A3A064A35282Bh

import binasciistr_1 = "********"str_2 = "CENSORED"str_3 = "********"word_1 = [0x410A4335494A0942]word_2 = [0x0B0EF2F50BE619F0]word_3 = [0x4F0A3A064A35282B]bin_1 = binascii.b2a_hex(str_1.encode('ascii')[::-1])bin_2 = binascii.b2a_hex(str_2.encode('ascii')[::-1])bin_3 = binascii.b2a_hex(str_3.encode('ascii')[::-1])j_1 = binascii.a2b_hex(hex(int(bin_1, 16) + word_1[0])[2:])[::-1]j_2 = binascii.a2b_hex(hex(int(bin_2, 16) + word_2[0])[2:])[::-1]j_3 = binascii.a2b_hex(hex(int(bin_3, 16) + word_3[0])[2:])[::-1]print(j_1 + j_2 + j_3)

▇ 扫码关注我们 ▇

长白山攻防实验室

学习最新技术知识


```
int __stdcall WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd){ DialogBoxParamA(hInstance, (LPCSTR)0x67, 0, (DLGPROC)DialogFunc, 0); return 0;}
BOOL __userpurge DialogFunc@(int a1@, int a2@, HWND hDlg, UINT a4, WPARAM a5, LPARAM a6){ const char *v6; // esi const char *v7; // edi int v9; // [esp+4h] [ebp-20030h] int v10; // [esp+8h] [ebp-2002Ch] int v11; // [esp+Ch] [ebp-20028h] int v12; // [esp+10h] [ebp-20024h] int v13; // [esp+14h] [ebp-20020h] int v14; // [esp+18h] [ebp-2001Ch] int v15; // [esp+1Ch] [ebp-20018h] int v16; // [esp+20h] [ebp-20014h] int v17; // [esp+24h] [ebp-20010h] int v18; // [esp+28h] [ebp-2000Ch] int v19; // [esp+2Ch] [ebp-20008h] CHAR String; // [esp+30h] [ebp-20004h] char v21; // [esp+31h] [ebp-20003h] char v22; // [esp+32h] [ebp-20002h] char v23; // [esp+33h] [ebp-20001h] char v24; // [esp+34h] [ebp-20000h] char v25; // [esp+10030h] [ebp-10004h] char v26; // [esp+10031h] [ebp-10003h] char v27; // [esp+10032h] [ebp-10002h] int v28; // [esp+20028h] [ebp-Ch]  int v29; // [esp+2002Ch] [ebp-8h] __alloca_probe(); if ( a4 == 272 ) return 1; v29 = a2; v28 = a1; if ( a4 != 273 ) return 0; if ( (_WORD)a5 == 1001 ) { memset(&String, 0, 0xFFFFu); GetDlgItemTextA(hDlg, 1000, &String, 0xFFFF); if ( strlen(&String) == 8 ) { v9 = 90; v10 = 74; v11 = 83; v12 = 69; v13 = 67; v14 = 97; v15 = 78; v16 = 72; v17 = 51; v18 = 110; v19 = 103; sub_4010F0(&v9, 0, 10); memset(&v25, 0, 0xFFFFu); v6 = (const char *)sub_401000(&v25, strlen(&v25)); memset(&v25, 0, 0xFFFFu); v26 = v23; v25 = v22; v27 = v24; v7 = (const char *)sub_401000(&v25, strlen(&v25)); if ( String == v9 + 34 && v21 == v13 && 4 * v22 - 141 == 3 * v11 && v23 / 4 == 2 * (v16 / 9) && !strcmp(v6, "ak1w") && !strcmp(v7, "V1Ax") ) { MessageBoxA(hDlg, "U g3t 1T!", "@_@", 0); } } return 0; } if ( (_WORD)a5 != 1 && (_WORD)a5 != 2 ) return 0; EndDialog(hDlg, (unsigned __int16)a5); return 1;}
int __cdecl sub_4010F0(int a1, int a2, int a3){ int result; // eax int i; // esi int v5; // ecx  int v6; // edx result = a3; for ( i = a2; i <= a3; a2 = i ) { v5 = 4 * i; v6 = *(_DWORD *)(4 * i + a1); if ( a2 < result && i < result ) { do { if ( v6 > *(_DWORD *)(a1 + 4 * result) ) { if ( i >= result ) break; ++i; *(_DWORD *)(v5 + a1) = *(_DWORD *)(a1 + 4 * result); if ( i >= result ) break; while ( *(_DWORD *)(a1 + 4 * i) <= v6 ) { if ( ++i >= result ) goto LABEL_13; } if ( i >= result ) break; v5 = 4 * i; *(_DWORD *)(a1 + 4 * result) = *(_DWORD *)(4 * i + a1); } --result; } while ( i < result ); }LABEL_13: *(_DWORD *)(a1 + 4 * result) = v6; sub_4010F0(a1, a2, i - 1); result = a3; ++i; } return result;}
    #include#includeint __cdecl sub_4010F0(char* a1, int a2, int a3){ int result; // eax int i; // esi int v5; // ecx    int v6; // edx result = a3; for (i = a2; i <= a3; a2 = i) { v5 =i; v6 = a1[i]; if (a2 < result && i < result) { do { if (v6 > a1[result]) { if (i >= result) break; ++i; a1[v5] = a1[result]; if (i >= result) break; while (a1[i] <= v6) { if (++i >= result) goto LABEL_13; } if (i >= result) break; v5 =i; a1[result] = a1[i]; } --result; } while (i < result); } LABEL_13: a1[result] = v6; sub_4010F0(a1, a2, i - 1); result = a3; ++i; } return result;}int main() { char str[] = "ZJSECaNH3ng"; sub_4010F0(str, 0, 10); printf("%s", str); return 0;}
_BYTE *__cdecl sub_401000(int a1, int a2){ int v2; // eax int v3; // esi size_t v4; // ebx _BYTE *v5; // eax _BYTE *v6; // edi int v7; // eax _BYTE *v8; // ebx int v9; // edi signed int v10; // edx int v11; // edi signed int v12; // eax signed int v13; // esi _BYTE *result; // eax _BYTE *v15; // [esp+Ch] [ebp-10h] _BYTE *v16; // [esp+10h] [ebp-Ch] int v17; // [esp+14h] [ebp-8h]  int v18; // [esp+18h] [ebp-4h] v2 = a2 / 3; v3 = 0; if ( a2 % 3 > 0 ) ++v2; v4 = 4 * v2 + 1; v5 = malloc(v4); v6 = v5; v15 = v5; if ( !v5 ) exit(0); memset(v5, 0, v4); v7 = a2; v8 = v6; v16 = v6; if ( a2 > 0 ) { while ( 1 ) { v9 = 0; v10 = 0; v18 = 0; do { if ( v3 >= v7 ) break; ++v10; v9 = *(unsigned __int8 *)(v3++ + a1) | (v9 << 8); } while ( v10 < 3 ); v11 = v9 << 8 * (3 - v10); v12 = 0; v17 = v3; v13 = 18; do { if ( v10 >= v12 ) { *((_BYTE *)&v18 + v12) = (v11 >> v13) & 0x3F; v8 = v16; } else { *((_BYTE *)&v18 + v12) = 64; } *v8++ = byte_407830[*((char *)&v18 + v12)]; v13 -= 6; ++v12; v16 = v8; } while ( v13 > -6 ); v3 = v17; if ( v17 >= a2 ) break; v7 = a2; } v6 = v15; } result = v6; *v8 = 0; return result;}
.rdata:
00407830 byte_407830 db 41h ; DATA XREF: sub_401000+C0↑r.rdata:
00407831 aBcdefghijklmno db 'BCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=',0
package com.example.flag;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v7.app.ActionBarActivity;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;/* loaded from: classes.dex */public class MainActivity extends ActionBarActivity { /* JADX INFO: Access modifiers changed from: protected */ @Override // android.support.v7.app.ActionBarActivity, android.support.v4.app.FragmentActivity, android.app.Activity public void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main); if (savedInstanceState == null) { getSupportFragmentManager().beginTransaction().add(R.id.container, new PlaceholderFragment()).commit(); } Button button = (Button) findViewById(R.id.button1); final TextView textview = (TextView) findViewById(R.id.textView1); final EditText editview = (EditText) findViewById(R.id.editText1); button.setOnClickListener(new View.OnClickListener() { // from class: com.example.flag.MainActivity.1 @Override // android.view.View.OnClickListener public void onClick(View v) { int flag = 1; String xx = editview.getText().toString(); if (xx.length() != 32 || xx.charAt(31) != 'a' || xx.charAt(1) != 'b' || (xx.charAt(0) + xx.charAt(2)) - 48 != 56) { flag = 0; } if (flag == 1) { char[] x = "dd2940c04462b4dd7c450528835cca15".toCharArray(); x[2] = (char) ((x[2] + x[3]) - 50); x[4] = (char) ((x[2] + x[5]) - 48); x[30] = (char) ((x[31] + x[9]) - 48); x[14] = (char) ((x[27] + x[28]) - 97); for (int i = 0; i < 16; i++) { char a = x[31 - i]; x[31 - i] = x[i]; x[i] = a; } String bbb = String.valueOf(x); textview.setText("flag{" + bbb + "}"); return; } textview.setText("输入注册码错误"); } });    } @Override // android.app.Activity public boolean onCreateOptionsMenu(Menu menu) { getMenuInflater().inflate(R.menu.main, menu); return true;    } @Override // android.app.Activity public boolean onOptionsItemSelected(MenuItem item) { int id = item.getItemId(); if (id == R.id.action_settings) { return true; } return super.onOptionsItemSelected(item);    } /* loaded from: classes.dex */ public static class PlaceholderFragment extends Fragment { @Override // android.support.v4.app.Fragment public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) { View rootView = inflater.inflate(R.layout.fragment_main, container, false); return rootView; } }}
if (flag == 1) { char[] x = "dd2940c04462b4dd7c450528835cca15".toCharArray(); x[2] = (char) ((x[2] + x[3]) - 50); x[4] = (char) ((x[2] + x[5]) - 48); x[30] = (char) ((x[31] + x[9]) - 48); x[14] = (char) ((x[27] + x[28]) - 97); for (int i = 0; i < 16; i++) { char a = x[31 - i]; x[31 - i] = x[i]; x[i] = a;                    }之后针对这里进行改写，flag即可出来#include#includeint main() {char x[]= "dd2940c04462b4dd7c450528835cca15";x[2] = ((x[2] + x[3]) - 50);x[4] = ((x[2] + x[5]) - 48);x[30] = (char)((x[31] + x[9]) - 48);x[14] = (char)((x[27] + x[28]) - 97);for (int i = 0; i < 16; i++) {char a = x[31 - i];x[31 - i] = x[i];x[i] = a;}printf("flag{%s}", x);
return 0;}
__int64 __fastcall main(signed int a1, char **a2, char **a3){ if ( a1 > 1 ) { if ( !strcmp(a2[1], "zer0pts{********CENSORED********}") ) puts("Correct!"); else puts("Wrong!"); } else { printf("Usage: %sn", *a2, a3, a2); } return 0LL;}
__int64 __fastcall sub_6EA(__int64 a1, __int64 a2){ int i; // [rsp+18h] [rbp-8h] int v4; // [rsp+18h] [rbp-8h]  int j; // [rsp+1Ch] [rbp-4h] for ( i = 0; *(_BYTE *)(i + a1); ++i ) ; v4 = (i >> 3) + 1; for ( j = 0; j < v4; ++j ) *(_QWORD *)(8 * j + a1) -= qword_201060[j]; return qword_201090(a1, a2);}
qword_201060 dq 0, 410A4335494A0942h, 0B0EF2F50BE619F0h, 4F0A3A064A35282Bh
import binasciistr_1 = "********"str_2 = "CENSORED"str_3 = "********"word_1 = [0x410A4335494A0942]word_2 = [0x0B0EF2F50BE619F0]word_3 = [0x4F0A3A064A35282B]bin_1 = binascii.b2a_hex(str_1.encode('ascii')[::-1])bin_2 = binascii.b2a_hex(str_2.encode('ascii')[::-1])bin_3 = binascii.b2a_hex(str_3.encode('ascii')[::-1])j_1 = binascii.a2b_hex(hex(int(bin_1, 16) + word_1[0])[2:])[::-1]j_2 = binascii.a2b_hex(hex(int(bin_2, 16) + word_2[0])[2:])[::-1]j_3 = binascii.a2b_hex(hex(int(bin_3, 16) + word_3[0])[2:])[::-1]print(j_1 + j_2 + j_3)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/0-1666229937.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1666229937.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/7-1666229938.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1666229938.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1666229938.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/7-1666229938.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/4-1666229939.png)