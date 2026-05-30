# 2024年羊城杯粤港澳大湾区网络安全大赛WP-Reverse篇

> 原文: https://www.ctfiot.com/203459.html
> ID: 203459

chal（赛后出flag的零解题）

cython的逆向万变不离其宗，用Cython 二进制库逆向分析全面指南里的方法能逆出个大概。赛后又去再看了一下，（以为只是用来防多解的）self._tips才发现它才是真正的check。真正的密文竟然不是已知数组，而是……

先看题目给的main.py的调用，是直接用chal.chal(flag)对flag进行检查：

import chal

flag = input("flag: ")
chal.chal(flag)

>>> import chal
>>> dir(chal)
['__builtins__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '__test__', 'chal', 'os', 'random']
>>> dir(chal.chal)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_p1', '_p2', '_p3']
>>> chal.chal._p1
<cyfunction chal._p1 at 0x4000fa0450>
>>> chal.chal._p2
<cyfunction chal._p2 at 0x4000fa0520>
>>> chal.chal._p3
<cyfunction chal._p3 at 0x4000fa05f0>
>>> dir(chal.chal("a"))
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_p1', '_p2', '_p3', '_tips', '_var1', '_var2', '_var3']
>>> chal.chal("a")._tips
"Don't peek!!!"
>>> chal.chal("a")._var1
'a'
>>> chal.chal("a")._var2
[121, 73, 141, 146, 115, 230, 181, 65, 238, 17, 146, 73, 228, 82, 188, 66, 12, 148, 225, 66, 255, 254, 47, 22, 163, 250, 222, 133, 35, 232, 106, 176]
>>> chal.chal("a")._var3
[12, 243, 133, 147, 7, 36, 29, 49, 226, 211, 156, 56, 142, 78, 254, 12]

typedef struct {
    PyObject **p;
    const char *s;
    const Py_ssize_t n;
    const char* encoding;
    const char is_unicode;
    const char is_str;
    const char intern;
} __Pyx_StringTabEntry;

__m128i v8;
__int64 v9;
__int64 v10;
__int16 v11;
char v12;

v8 = _mm_unpacklo_epi64(&qword_28A98, "AttributeError");
v9 = 15LL;
v10 = 0LL;
v11 = 0x100;
v12 = 1;

qword_29170 = PyLong_FromLong(113LL, v9, v244, v245);
if ( qword_29170 )

qword_29600 = PyLong_FromString("2654435769", 0LL, 0LL);
if ( qword_29600 )

qword_296B8 = _Pyx_GetBuiltinName(qword_28A98);
if ( !qword_296B8 )
  return 0xFFFFFFFFLL;

qword_29630 = PyTuple_Pack(2LL, qword_29600, qword_29618);
if ( !qword_29630 )
  return 0xFFFFFFFFLL;

// *** _Pyx_InitCachedConstants ***
// 元组赋值
v1 = PyTuple_Pack(7LL, self, x1, x2, tmp, low, high, ans);
if ( !v1 )
  return 0xFFFFFFFFLL;
// 函数定义
qword_29688 = _Pyx_PyCode_New_constprop_0(
  3, 7, qword_28A80, qword_28A78, qword_28A78, v1, qword_28A78, 
  qword_28A78, chal_py, p1, 19, qword_28A80
);
if ( !qword_29688 )
  return 0xFFFFFFFFLL;

// *** _pyx_pymod_exec_chal ***
v559 = _Pyx_CyFunction_New_constprop_0(&_pyx_mdef_4chal_4chal_3_p1, chal__p1, chal, _pyx_mstate_global_static, qword_29688);                                
v560 = PyObject_SetItem(v6, p1, v559) >> 31; // self._p1 = v559

ctypedef struct PyMethodDef:
    const char* ml_name
    PyCFunction ml_meth
    int ml_flags
    const char* ml_doc

.data:00000000000289C0 AD 41 02 00 00 00 00 00           __pyx_mdef_4chal_4chal_3_p1 dq offset aChalChalP1+0Ah
.data:00000000000289C0                                                                 ; DATA XREF: __pyx_pymod_exec_chal+236B↑o
.data:00000000000289C0                                                                 ; "_p1"
.data:00000000000289C8 70 F7 00 00 00 00 00 00           dq offset __pyx_pw_4chal_4chal_3_p1
.data:00000000000289D0 82 00 00 00                       dd 82h
.data:00000000000289D4 00                                db 0

v539 = _Pyx_ImportDottedModule_constprop_0(random);
if ( PyDict_SetItem(_pyx_mstate_global_static, random, v539) < 0 )
{

v22 = PyObject_SetAttr(self, var1, s);

v23 = PyList_New(32LL); // 1. 创建新的列表对象
v24 = pyx_int_121; // 2. v24 = 121
if ( *pyx_int_121 != -1 ) // 3. 错误处理
  ++*pyx_int_121;
v25 = v23[3]; // 4. 列表对象（v23）的[3]是数据部分
*v25 = v24; // 5. 列表第一个元素为v24即121
// ... 重复以上2、3、5步处理对列表赋值
v58 = PyObject_SetAttr(self, var2, v23);

v150 = *(*(self + 8) + 144LL);
// v2 = self._p3
    if ( v150 )
      v2 = v150(self, p3);
    else
      v2 = PyObject_GetAttr(self, p3);
    if ( !v2 )
    {
      v101 = 0LL;
      v1 = 0LL;
      v23 = 0LL;
      v122 = 4493LL;
      v123 = 10LL;
      goto LABEL_211;
    }
    if ( *(v2 + 8) == &PyMethod_Type && (v151 = *(v2 + 24)) != 0LL )
    {
      v1 = *(v2 + 16);
      if ( *v151 != -1 )
        ++*v151;
      if ( *v1 != -1 )
        ++*v1;
      if ( *v2 >= 0 )
      {
        v152 = *v2 - 1LL;
        *v2 = v152;
        if ( !v152 )
          _Py_Dealloc(v2);
      }
// 参数是("Don't hook!!!")
      v192 = _mm_loadh_ps(&Don_thook___);
// 函数调用，执行self._p3("Don't hook!!!")，返回值给v23
      v23 = _Pyx_PyObject_FastCallDict_constprop_0(v1, &v192, 2LL);
      if ( *v151 >= 0 )
      {
        v153 = *v151 - 1LL;
        *v151 = v153;
        if ( !v153 )
          _Py_Dealloc(v151);
      }
    }
// 不同的调用方式，和上面的if同层
    else
    {
      v1 = v2;
      v192.m128_u64[0] = 0LL;
      v192.m128_u64[1] = Don_thook___;
      v23 = _Pyx_PyObject_FastCallDict_constprop_0(v2, v187, 1LL);
    }
    if ( !v23 )
    {
      v101 = 0LL;
      v2 = 0LL;
      v122 = 4513LL;
      v123 = 10LL;
      goto LABEL_211;
    }
    if ( *v1 >= 0 )
    {
      v154 = *v1 - 1LL;
      *v1 = v154;
      if ( !v154 )
        _Py_Dealloc(v1);
    }

v404 = _Pyx_PyObject_GetAttrStr(v403, to_bytes);
v406 = _Pyx_PyObject_Call_constprop_0(v404, t_2_big); // t_2_big是元组(2, 'big')，在_Pyx_InitCachedConstants中有初始化

v406 = v403.to_bytes(2, 'big')

// v2 = self._var2
    v155 = *(*(self + 8) + 144LL);
    if ( v155 )
      v2 = v155(self, var2);
    else
      v2 = PyObject_GetAttr(self, var2);
/* 上文返回值v23和v2对比，对比常量：
https://github.com/python/cpython/blob/3.12/Include/object.h#L862
#define Py_LT 0
#define Py_LE 1
#define Py_EQ 2
#define Py_NE 3
#define Py_GT 4
#define Py_GE 5
*/
    v1 = PyObject_RichCompare(v23, v2, 2LL);
// 确定是否IsTrue
    LOBYTE(IsTrue) = v1 == &Py_TrueStruct;
    if ( v1 == &Py_TrueStruct || v1 == &Py_FalseStruct || v1 == &Py_NoneStruct )
    {
      IsTrue = IsTrue;
    }
    else
    {
      IsTrue = PyObject_IsTrue(v1);
    }
// 如果not IsTrue，即 v23 != self._var2
    if ( !IsTrue )

取数组长度

（手动删除了框架代码和错误处理）

v2 = PyObject_GetAttr(self, var1);
v91 = PyObject_Size(v2);
v93 = PyLong_FromSsize_t(v91);

v93 = len(self._var1)

运算

// v3 = 2654435769 - v93
v3 = PyNumber_Subtract(pyx_int_2654435769, v93);
// v294 = v293 ^ v91
v294 = (__m128 *)PyNumber_Xor(v293, v91);
// v367 = v1229 + v365
v367 = (__int64 *)PyNumber_Add(v1229, v365);
// InPlace字样，这里等同于v1213 = (v483 &= 4294967295)
v1213 = (__int64 *)PyNumber_InPlaceAnd(v483, pyx_int_4294967295);
// m128_u64 = v1213 >> 4
m128_u64 = (_QWORD *)_Pyx_PyInt_RshiftObjC_constprop_0(v1213, pyx_int_4, 4LL);
// v537 = v1225 & 3
v537 = (_QWORD *)_Pyx_PyInt_AndObjC_constprop_0(v1225, pyx_int_3, 3LL, 0LL);
// ItemInt_List_Fast_constprop_0 = v537 + 4
ItemInt_List_Fast_constprop_0 = (__m128 *)_Pyx_PyInt_AddObjC_constprop_0(v537, pyx_int_4, 4LL, 0LL);
// ...

hook辅助

使用x86_64机器上的Python 3.12导入chal，即可对其函数进行hook。如我们需要hookself._p1：

>>> import chal
>>> setattr(chal.chal, "ori_p1", chal.chal.__dict__["_p1"]) # 保存原来的_p1
>>> def hook_p1(self, a, b): # 写hook函数，打印参数和返回值
...     print(a, b)
...     ret = self.ori_p1(a, b)
...     print(ret)
...     return ret
... 
>>> setattr(chal.chal, "_p1", hook_p1) # 挂上去
>>> chal.chal("a") # 调用后即可看到每次调用self._p1时的参数和返回值，且不影响函数原来的功能
52232 48895
-27712
52883 49898
-25833
64660 29775
-28948
# ... 数据省略

import os
import random

class chal():
    def __init__(self, s):
        # 变量的开头下划线都没写，懒（
        self.var1 = s
        self.var2 = [121, 73, 141, 146, 115, 230, 181, 65, 238, 17, 146, 73, 228, 82, 188, 66, 12, 148, 225, 66, 255, 254, 47, 22, 163, 250, 222, 133, 35, 232, 106, 176]
        self.var3 = [12, 243, 133, 147, 7, 36, 29, 49, 226, 211, 156, 56, 142, 78, 254, 12]
        random.seed(sum([2654435769-len(s)] + [ord(x) for x in str(len(s))]))
        if self._p3("Don't hook!!!") == self.var2: # 假的check，别信
            print("yes")
        elif self.tips == 0: # 真的check！
            # 有个self._var2 + self._var3，但没有使用
            print("yes")
        self.tips = "Don't peek!!!"

    def _p1(self, a, b): # a * b % 65537
        # print(a, b)
        c = a * b
        cl = c & 0xFFFF
        ch = (c >> 16) & 0xFFFF
        if cl - ch < 0:
            ret = cl - ch + 1
        else:
            ret = cl - ch
        # print(ret)
        return ret

    def _p2(self, i): # sm4 subbytes
        # print(i)
        l = [214, 144, 233, 254, 204, 225, 61, 183, 22, 182, 20, 194, 40, 251, 44, 5, 43, 103, 154, 118, 42, 190, 4, 195, 170, 68, 19, 38, 73, 134, 6, 153, 156, 66, 80, 244, 145, 239, 152, 122, 51, 84, 11, 67, 237, 207, 172, 98, 228, 179, 28, 169, 201, 8, 232, 149, 128, 223, 148, 250, 117, 143, 63, 166, 71, 7, 167, 252, 243, 115, 23, 186, 131, 89, 60, 25, 230, 133, 79, 168, 104, 107, 129, 178, 113, 100, 218, 139, 248, 235, 15, 75, 112, 86, 157, 53, 30, 36, 14, 94, 99, 88, 209, 162, 37, 34, 124, 59, 1, 33, 120, 135, 212, 0, 70, 87, 159, 211, 39, 82, 76, 54, 2, 231, 160, 196, 200, 158, 234, 191, 138, 210, 64, 199, 56, 181, 163, 247, 242, 206, 249, 97, 21, 161, 224, 174, 93, 164, 155, 52, 26, 85, 173, 147, 50, 48, 245, 140, 177, 227, 29, 246, 226, 46, 130, 102, 202, 96, 192, 41, 35, 171, 13, 83, 78, 111, 213, 219, 55, 69, 222, 253, 142, 47, 3, 255, 106, 114, 109, 108, 91, 81, 141, 27, 175, 146, 187, 221, 188, 127, 17, 217, 92, 65, 31, 16, 90, 216, 10, 193, 49, 136, 165, 205, 123, 189, 45, 116, 208, 18, 184, 229, 180, 176, 137, 105, 151, 74, 12, 150, 119, 126, 101, 185, 241, 9, 197, 110, 198, 132, 24, 240, 125, 236, 58, 220, 77, 32, 121, 238, 95, 62, 215, 203, 57, 72]
        ret = int.from_bytes(bytes(map(lambda x: l[x], i.to_bytes(4, 'little'))), 'little')
        # print(ret)
        return ret

    def _p3(self):
        # 开头的lambda是个pkcs5padding，但是输入整块的数据就不重要了（块长度是16
        # s = pkcs5padding(self.var1).encode()
        s = self.var1.encode()
        L = [173, 7, 131, 63, 141, 180, 193, 156, 21, 198, 65, 218, 13, 216, 148, 105, 165, 96, 250, 121, 168, 23, 94, 49, 79, 120, 101, 211, 167, 240, 75, 136, 43, 70, 115, 203, 220, 34, 160, 188, 222, 61, 169, 117, 95, 134, 174, 167]
        tmpl = []
        self.tips = 0
        for i in range(len(s)):
            tmpl.append(L[i%len(L)] ^ s[i])
        rslt = b''
        for i in range(0, len(tmpl), 8):
            longs = tmpl[i:i+8]
            randl = []
            # IDEA的轮密钥
            for _ in range(52):
                randl.append(random.getrandbits(16))
            ll = [] # v141
            for j in range(0, len(longs), 2):
                ll.append(int.from_bytes(longs[j:j+2]))
            assert len(ll) == 4
            v1227, v1229, v1230, v1222 = ll
            for v1232 in range(8):
                v1225 = random.randint(0x9e3779b9, 0xc6ef3720)
                # TEA 密钥
                rilv1224 = []
                for _ in range(8):
                    rilv1224.append(random.randint(0x56AA3350, 0xa3b1bac6))
                # XTEA 密钥
                rilv1228 = []
                for _ in range(8):
                    rilv1228.append(random.randint(0x677D9197, 0xb27022dc))
                # 半轮魔改IDEA
                lv1233 = []
                lv1233.append(self._p1(v1227, randl[6 * v1232 + 0]) & 0xFFFF)
                lv1233.append((v1229 + randl[6 * v1232 + 1]) & 0xFFFF)
                lv1233.append((v1230 + randl[6 * v1232 + 2]) & 0xFFFF)
                lv1233.append(self._p1(v1222, randl[6 * v1232 + 3]) & 0xFFFF)
                lv395 = []
                for j in range(4):
                    lv395.append(lv1233[j].to_bytes(2, 'big'))
                tmps = b''.join(lv395)
                lv424 = []
                for j in range(0, len(tmps), 4):
                    lv424.append(int.from_bytes(tmps[j:j+4], 'little'))
                assert len(lv424) == 2
                # 魔改TEA
                l, r = lv424 # v1213, v1215
                l += ((r << 4) + self._p2(rilv1224[0])) ^ (r + v1225) ^ ((r >> 5) + self._p2(rilv1224[1]))
                l &= 4294967295
                r += ((l << 5) + self._p2(rilv1224[2])) ^ (l + v1225) ^ ((l >> 4) + self._p2(rilv1224[3]))
                r &= 4294967295
                # 魔改XTEA
                l += (((r << 5) ^ (r >> 4)) + r) ^ (v1225 + self._p2(rilv1228[4 + (v1225 & 3)]))
                l &= 4294967295
                r += (((l << 4) ^ (l >> 5)) + l) ^ (v1225 + self._p2(rilv1228[4 + ((v1225 >> 11) & 3)]))
                r &= 4294967295
                # 奇数轮更改v1225（TEA/XTEA中的sum）
                if v1232 & 1 == 1:
                    v1225 = random.getrandbits(32)
                # 魔改TEA
                l += (((r << 3) ^ (r >> 6)) + r) ^ (v1225 + self._p2(rilv1228[v1225 & 3]))
                l &= 4294967295
                r += (((l << 4) ^ (l >> 5)) + l) ^ (v1225 + self._p2(rilv1228[(v1225 >> 11) & 3]))
                r &= 4294967295
                # 魔改XTEA
                l += ((r << 4) + self._p2(rilv1224[4])) ^ (r + v1225) ^ ((r >> 5) + self._p2(rilv1224[5]))
                l &= 4294967295
                r += ((l << 2) + self._p2(rilv1224[6])) ^ (l + v1225) ^ ((l >> 7) + self._p2(rilv1224[7]))
                r &= 4294967295
                tmps = b''.join([x.to_bytes(4, 'little') for x in [l, r]])
                lv770 = []
                for j in range(0, len(tmps), 2):
                    lv770.append(int.from_bytes(tmps[j:j+2], 'big'))
                assert len(lv770) == 4
                # 另外半轮魔改IDEA
                a, b, c, d = lv770 # v1242, v1241, v1240, v1239
                v1196 = self._p1((a ^ c) & 0xFFFF, randl[v1232 * 6 + 4])
                v835 = self._p1(((b ^ d) + v1196) & 0xFFFF, randl[v1232 * 6 + 5]) & 0xFFFF
                v1198 = (v1196 + v835) & 0xFFFF
                v840 = a ^ v835
                v841 = d ^ v1198
                v842 = b ^ v1198
                v91 = c ^ v835
                # 奇数轮和偶数轮交接给下一轮的变量不同
                if v1232 & 1 != 0:
                    v1230 = v91
                    v1229 = v842
                else:
                    v1230 = v842
                    v1229 = v91
                v1222 = v841
                v1227 = v840
            # 最后半轮魔改IDEA
            v1227 = self._p1(v1227 & 0xFFFF, randl[48]) & 0xFFFF
            v1229 = (v1229 + randl[49]) & 0xFFFF
            v1230 = (v1230 + randl[50]) & 0xFFFF
            v1222 = self._p1(v1222 & 0xFFFF, randl[51]) & 0xFFFF
            ll = [v1227, v1229, v1230, v1222]
            lv918 = []
            for j in range(len(ll)):
                lv918.append(ll[j].to_bytes(2, 'big'))
            tmps = b''.join(lv918)
            print(list(tmps))
            rslt += tmps
            # 真正的比对在这里（
            self.tips += sum([tmps[j] ^ random.getrandbits(8) for j in range(len(tmps))])
        print(self.tips, list(rslt))
        # 没用的返回值，真随机
        return [x ^ y for x, y in zip(os.urandom(len(rslt)), rslt)]

if __name__ == '__main__':
    c = chal("a"*48) # 测试

import random

# 假密文！！！
dst = [121, 73, 141, 146, 115, 230, 181, 65, 238, 17, 146, 73, 228, 82, 188, 66, 12, 148, 225, 66, 255, 254, 47, 22, 163, 250, 222, 133, 35, 232, 106, 176]
dst += [12, 243, 133, 147, 7, 36, 29, 49, 226, 211, 156, 56, 142, 78, 254, 12]
random.seed(sum([2654435769-len(dst)] + [ord(x) for x in str(len(dst))]))

r_randl = []
r8_v1225 = []
r8_rilv1224 = []
r8_rilv1228 = []
r8_rand8b = []
for _ in range(0, len(dst), 8):
    r_randl.append([random.getrandbits(16) for _ in range(52)])
    tmpl = []
    for i in range(8):
        tmpl.append(random.randint(0x9e3779b9, 0xc6ef3720))
        r8_rilv1224.append([random.randint(0x56AA3350, 0xa3b1bac6) for _ in range(8)])
        r8_rilv1228.append([random.randint(0x677D9197, 0xb27022dc) for _ in range(8)])
        if i & 1 == 1:
            tmpl.append(random.getrandbits(32))
    r8_v1225 += tmpl[::-1]
    r8_rand8b.append([random.getrandbits(8) for _ in range(8)])
v1225_iter = iter(r8_v1225)
# 真密文
dst = sum(r8_rand8b, [])

def _p1(a, b):
    c = a * b
    cl = c & 0xFFFF
    ch = (c >> 16) & 0xFFFF
    if cl - ch < 0:
        return cl - ch + 1
    else:
        return cl - ch

def _p2(i):
    l = [214, 144, 233, 254, 204, 225, 61, 183, 22, 182, 20, 194, 40, 251, 44, 5, 43, 103, 154, 118, 42, 190, 4, 195, 170, 68, 19, 38, 73, 134, 6, 153, 156, 66, 80, 244, 145, 239, 152, 122, 51, 84, 11, 67, 237, 207, 172, 98, 228, 179, 28, 169, 201, 8, 232, 149, 128, 223, 148, 250, 117, 143, 63, 166, 71, 7, 167, 252, 243, 115, 23, 186, 131, 89, 60, 25, 230, 133, 79, 168, 104, 107, 129, 178, 113, 100, 218, 139, 248, 235, 15, 75, 112, 86, 157, 53, 30, 36, 14, 94, 99, 88, 209, 162, 37, 34, 124, 59, 1, 33, 120, 135, 212, 0, 70, 87, 159, 211, 39, 82, 76, 54, 2, 231, 160, 196, 200, 158, 234, 191, 138, 210, 64, 199, 56, 181, 163, 247, 242, 206, 249, 97, 21, 161, 224, 174, 93, 164, 155, 52, 26, 85, 173, 147, 50, 48, 245, 140, 177, 227, 29, 246, 226, 46, 130, 102, 202, 96, 192, 41, 35, 171, 13, 83, 78, 111, 213, 219, 55, 69, 222, 253, 142, 47, 3, 255, 106, 114, 109, 108, 91, 81, 141, 27, 175, 146, 187, 221, 188, 127, 17, 217, 92, 65, 31, 16, 90, 216, 10, 193, 49, 136, 165, 205, 123, 189, 45, 116, 208, 18, 184, 229, 180, 176, 137, 105, 151, 74, 12, 150, 119, 126, 101, 185, 241, 9, 197, 110, 198, 132, 24, 240, 125, 236, 58, 220, 77, 32, 121, 238, 95, 62, 215, 203, 57, 72]
    return int.from_bytes(bytes(map(lambda x: l[x], i.to_bytes(4, 'little'))), 'little')

def p1_rev(ret, b):
    for i in range(0x10000):
        if ret == (_p1(i, b) & 0xFFFF):
            return i

res = b''
for xi in range(0, len(dst), 8):
    randl = r_randl[xi//8]
    l8 = dst[xi:xi+8]
    l4 = [int.from_bytes(bytes(l8[i:i+2]), 'big') for i in range(0, len(l8), 2)]
    v1227, v1229, v1230, v1222 = l4
    v1227 = p1_rev(v1227, randl[48]) & 0xFFFF
    v1229 = (v1229 - randl[49]) & 0xFFFF
    v1230 = (v1230 - randl[50]) & 0xFFFF
    v1222 = p1_rev(v1222, randl[51]) & 0xFFFF
    for i in range(8)[::-1]:
        rilv1224 = r8_rilv1224[xi + i]
        rilv1228 = r8_rilv1228[xi + i]
        v841 = v1222
        v840 = v1227
        if i & 1 != 0:
            v91 = v1230
            v842 = v1229
        else:
            v842 = v1230
            v91 = v1229
        a_xor_c = v840 ^ v91
        b_xor_d = v841 ^ v842
        v1196 = _p1(a_xor_c, randl[i * 6 + 4]) & 0xFFFF
        v835 = _p1((b_xor_d + v1196) & 0xFFFF, randl[i * 6 + 5]) & 0xFFFF
        v1198 = (v1196 + v835) & 0xFFFF
        a = v840 ^ v835
        b = v842 ^ v1198
        c = v91 ^ v835
        d = v841 ^ v1198
        l4 = [a, b, c, d]
        s = b''.join([x.to_bytes(2, 'big') for x in l4])
        l, r = [int.from_bytes(s[j:j+4], 'little') for j in range(0, len(s), 4)]
        v1225 = next(v1225_iter)
        r -= ((l << 2) + _p2(rilv1224[6])) ^ (l + v1225) ^ ((l >> 7) + _p2(rilv1224[7]))
        r &= 4294967295
        l -= ((r << 4) + _p2(rilv1224[4])) ^ (r + v1225) ^ ((r >> 5) + _p2(rilv1224[5]))
        l &= 4294967295
        r -= (((l << 4) ^ (l >> 5)) + l) ^ (v1225 + _p2(rilv1228[(v1225 >> 11) & 3]))
        r &= 4294967295
        l -= (((r << 3) ^ (r >> 6)) + r) ^ (v1225 + _p2(rilv1228[v1225 & 3]))
        l &= 4294967295
        if i & 1 == 1:
            v1225 = next(v1225_iter)
        r -= (((l << 4) ^ (l >> 5)) + l) ^ (v1225 + _p2(rilv1228[4 + ((v1225 >> 11) & 3)]))
        r &= 4294967295
        l -= (((r << 5) ^ (r >> 4)) + r) ^ (v1225 + _p2(rilv1228[4 + (v1225 & 3)]))
        l &= 4294967295
        r -= ((l << 5) + _p2(rilv1224[2])) ^ (l + v1225) ^ ((l >> 4) + _p2(rilv1224[3]))
        r &= 4294967295
        l -= ((r << 4) + _p2(rilv1224[0])) ^ (r + v1225) ^ ((r >> 5) + _p2(rilv1224[1]))
        l &= 4294967295
        s = b''.join([x.to_bytes(4, 'little') for x in [l, r]])
        v1227, v1229, v1230, v1222 = [int.from_bytes(s[j:j+2], 'big') for j in range(0, len(s), 2)]
        v1227 = p1_rev(v1227, randl[6 * i + 0]) & 0xFFFF
        v1229 = (v1229 - randl[6 * i + 1]) & 0xFFFF
        v1230 = (v1230 - randl[6 * i + 2]) & 0xFFFF
        v1222 = p1_rev(v1222, randl[6 * i + 3]) & 0xFFFF
    res += b''.join([x.to_bytes(2, 'big') for x in [v1227, v1229, v1230, v1222]])

L = [173, 7, 131, 63, 141, 180, 193, 156, 21, 198, 65, 218, 13, 216, 148, 105, 165, 96, 250, 121, 168, 23, 94, 49, 79, 120, 101, 211, 167, 240, 75, 136, 43, 70, 115, 203, 220, 34, 160, 188, 222, 61, 169, 117, 95, 134, 174, 167]
flag = []
for i in range(len(res)):
    flag.append(res[i] ^ L[i%len(L)])
print(bytes(flag))
# b'DASCTF{c6090fd29eaf2ae1d111289e3f3c0c7a3819dcc1}'

# ... 从vb脚本搬过来，省略
yyjskEVAnLNVYXPjnqeGNhKNvXlbSIslOoqViLKkb = BumFQkMgMUNykMNviBlfdZHOyVThmijmcNTUNaXSNHYdNzXKRqhYiKlaRzCfBlcoN + dWPtWzWvKrZRFrsAWZMGNjZQbCrgAImKXVUkOykXWeRltpUU + AMaKeZzlhAtdNANKAKwMNbKEKUWuQVZQbbCJIUog + BvEKpalonhsRIgbPkYPYbsbQGzIzvPitapncgtGKIo + yBILPYnXCUApVHExOtpKlnfTkVfexwgrFQOFIveA + pqdgalQAZJKIDySPundFqdITahrgAYveJXfZCOUHWnUDKXZwZU + pErQJcjFIvYQeIehtTPMaOgEwFvvjnaTkabtJDvpHbWG

import base64
# 测试套了两层base64
res = base64.b64decode(yyjskEVAnLNVYXPjnqeGNhKNvXlbSIslOoqViLKkb)
res = base64.b64decode(res)
with open("temp.exe", "wb") as f:
    f.write(res)

v9[0] = 4288;
// ... v9赋值，省略
  v9[53] = 7808;
  if ( a1 == 2 )
  {
    for ( j = 0; j < (int)j_strlen(*(const char **)(a2 + 8)) && (unsigned __int64)j < 0x36; ++j )
      v9[j + 64] = *(char *)(*(_QWORD *)(a2 + 8) + j) << 6;
    for ( j = 0; (unsigned __int64)j < 0x36; ++j )
    {
      if ( v9[j] != v9[j + 64] )
      {
        printf("bad");
        v4 = 0i64;
        goto LABEL_16;
      }
    }
    printf("good");
    v4 = 0i64;

# v9
dst = [4288, 4480, 5376, 4352, 5312, 4160, 7936, 5184, 6464, 6528, 5632, 3456, 7424, 5632, 6336, 6528, 6720, 6144, 6272, 7488, 6656, 7296, 7424, 2432, 2432, 2432, 5632, 4416, 3456, 7168, 6528, 7488, 6272, 5632, 3520, 6208, 5632, 4736, 6528, 6400, 7488, 3520, 5632, 5184, 3456, 7488, 7296, 3200, 6272, 7424, 2432, 2432, 2432, 7808]
for i in range(len(dst)):
    dst[i] = (dst[i] >> 6) ^ 7
print(bytes(dst))
# b'DASCTF{Vba_1s_dangerous!!!_B1ware_0f_Macr0_V1ru5es!!!}'

// input
puts("Please input your flag~");
scanf("%s", flag);
len = strlen(flag);
if ( len != 33 )
{
  puts("Len error!");
  exit(0);
}
// check
for ( i = 0; i <= 32; ++i )
{
  if ( std::abs(check[i] - in[i]) > (long double)(double)0.0001 )
  {
    puts("Wrong!!");
    exit(0);
  }
}
puts("Right!!");

rot13_encrypt(flag);

for ( i = 0; strlen(flag) > i; ++i )
{
  v2 = flag[i];
  *std::vector<int>::operator[]((std::vector<int> *const)i, v11) = v2;
}
encrypt((std::vector<double> *)((char *)__n + 1), &input);

std::vector<double> *__cdecl encrypt(std::vector<double> *retstr, const std::vector<int> *input)
{
  // ...
  for ( i = 0; i < size; ++i )
  {
    for ( j = 0; j < size; ++j )
    {
      v5 = (double)*std::vector<int>::operator[]((const std::vector<int> *const)j, v10);
      v2 = cos(((long double)j + 0.5) * ((long double)i * 3.141592653589793) / (long double)size);
      v6 = v2 * v5;
      v3 = std::vector<double>::operator[]((std::vector<double> *const)i, v11);
      *v3 = *v3 + v6;
    }
    if ( i )
      v4 = sqrt(2.0 / (long double)size);
    else
      v4 = sqrt(1.0 / (long double)size);
    v7 = v4;
    eax9 = std::vector<double>::operator[]((std::vector<double> *const)i, v12);
    *eax9 = *eax9 * v7;
  }
}

from math import sqrt, cos, pi

l = [513.355, -37.7986, 8.7316, -10.7832, -1.3097, -20.5779, 6.98641, -29.2989, 15.9422, 21.4138, 29.4754, -2.77161, -6.58794, -4.22332, -7.20771, 8.83506, -4.38138, -19.3898, 18.3453, 6.88259, -14.7652, 14.6102, 24.7414, -11.6222, -9.754759999999999, 12.2424, 13.4343, -34.9307, -35.735, -20.0848, 39.689, 21.879, 26.8296]
n = len(l)

# IDCT from https://github.com/lquatrin/CGT1-1D_DCT_IDCT/blob/master/CG_T1/src/MyDCTS.cpp
flag = []
for i in range(n):
    x = 0
    for j in range(n):
        if j != 0:
            x += l[j] * cos(((((2.0*i)+1.0)*j)*pi)/(2.0*n))
        else:
            x += l[j] * (1.0 / sqrt(2)) * cos(((((2.0*i)+1.0)*j)*pi)/(2.0*n))
    flag.append(round(sqrt(2.0 / n) * x))

# rot13
for i in range(n):
    if flag[i] in range(ord('A'), ord('Z')+1):
        base = ord('A')
    elif flag[i] in range(ord('a'), ord('z')+1):
        base = ord('a')
    else:
        continue
    flag[i] = (flag[i]-base+13) % 26 + base
print(bytes(flag))
# b'DASCTF{Wh0_1s_Ma1n_@nd_FunnY_Dct}'

.text:000000000049DB31
.text:000000000049DB31 loc_49DB31:
.text:000000000049DB31 movzx   r9d, byte ptr [rsi+rbx]
.text:000000000049DB36 xor     r9d, edx
.text:000000000049DB39 mov     [rax+rbx], r9b
.text:000000000049DB3D inc     rbx

.text:000000000049DB5F movzx   r11d, byte ptr [rbx+rax]
.text:000000000049DB64 inc     r9d             ; int
.text:000000000049DB67 movzx   r12d, r9b
.text:000000000049DB6B mov     r13d, [rdx+r12*4]
.text:000000000049DB6F add     r10d, r13d      ; int
.text:000000000049DB72 movzx   r15d, r10b
.text:000000000049DB76 mov     esi, r11d
.text:000000000049DB79 mov     r11d, [rdx+r15*4]
.text:000000000049DB7D mov     [rdx+r12*4], r11d
.text:000000000049DB81 mov     [rdx+r15*4], r13d
.text:000000000049DB85 mov     r11d, [rdx+r12*4]
.text:000000000049DB89 add     r11d, r13d
.text:000000000049DB8C movzx   r11d, r11b      ; int
.text:000000000049DB90 xor     esi, [rdx+r11*4]
.text:000000000049DB94 xor     esi, 11h
.text:000000000049DB97 mov     [rax+rbx], sil
.text:000000000049DB9B inc     rbx
.text:000000000049DB9E xchg    ax, ax

#include <stdio.h>
#include <string.h>

unsigned char S_Box[256] = {0};
// RC4 initial
void Init(unsigned char * key, int keyLen) {
    unsigned char T[256] = {0};
    for (int i = 0; i < 256; i++) {
        S_Box[i] = i;
        T[i] = key[i%keyLen];
    }
    int j = 0;
    for (int i = 0; i < 256; i++) {
        j = (j+S_Box[i]+T[i]) % 256;
        unsigned char tmp = S_Box[i];
        S_Box[i] = S_Box[j];
        S_Box[j] = tmp;
    }
    return;
}

void RC4(unsigned char * key, int keyLen, unsigned char * data, int dataLen) {
    Init(key, keyLen);
    int i = 0, j = 0;
    for (int k = 0; k < dataLen; k++) {
        i = (i+1) % 256;
        j = (j+S_Box[i]) % 256;
        unsigned char tmp = S_Box[i];
        S_Box[i] = S_Box[j];
        S_Box[j] = tmp;
        data[k] ^= S_Box[(S_Box[i]+S_Box[j])%256] ^ key[1] ^ 0x11;
    }
}

unsigned char magic[8] = {137, 80, 78, 71, 13, 10, 26, 10}; // png文件头
int isFind(unsigned char * data) {
    for (int i = 0; i < 8; i++) {
        if (data[i] != magic[i]) {
            return 0;
        }
    }
    return 1;
}

int main() {
    int png_size = 552205;
    unsigned char png[552205+1] = {0};
    FILE * fp = fopen("flag.png", "rb");
    fread(png, sizeof(char), png_size, fp);
    fclose(fp);
    unsigned char key[5+1] = {0};
    unsigned char data[552205+1] = {0};
    unsigned char charset[] = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    int charset_size = 62;
    unsigned char find = 0;
    for (int i0 = 0; i0 < charset_size; i0++) {
        for (int i1 = 0; i1 < charset_size; i1++) {
            for (int i2 = 0; i2 < charset_size; i2++) {
                for (int i3 = 0; i3 < charset_size; i3++) {
                    for (int i4 = 0; i4 < charset_size; i4++) {
                        key[0] = charset[i0];
                        key[1] = charset[i1];
                        key[2] = charset[i2];
                        key[3] = charset[i3];
                        key[4] = charset[i4];
                        memcpy(data, png, png_size);
                        RC4(key, 5, data, png_size);
                        if (isFind(data)) {
                            find = 1;
                            printf("find key: %sn", key);
                            fp = fopen("res.png", "wb");
                            fwrite(data, sizeof(char), png_size, fp);
                            fclose(fp);
                            break;
                        }
                    }
                    if (find) break;
                }
                if (find) break;
            }
            if (find) break;
        }
        if (find) break;
    }
    return 0;
}

00000000 vm struc ; (sizeof=0x420, align=0x8, mappedto_64)
00000000   l1 db 1024 dup(?)
00000400   l2 dw 8 dup(?)
00000410   l3 db 8 dup(?)
00000418   r1 db ?
00000419   r2 db ?
0000041A   r3 db ?
0000041B   r4 db ?
0000041C   check_flag db ?
0000041D   db ? ; undefined
0000041E   db ? ; undefined
0000041F   db ? ; undefined
00000420 vm ends

if ( *(input + 39) != 125 )
    goto LABEL_251;

do                                            // 3*8 -> 4*6
  {
    i0 = i_add_2 - 2;
    if ( i_add_2 - 2 >= v97 )
    {
      v189 = &off_443350;
      goto LABEL_261;
    }
    i0 = i_add_2 - 1;
    if ( i_add_2 - 1 >= v97 )
    {
      v189 = &off_443368;
      goto LABEL_261;
    }
    if ( i_add_2 >= v97 )
    {
      i0 = i_add_2;
      v189 = &off_443380;
LABEL_261:
      panic(i0, v97, v189);
    }
    inp_i_0 = *(input_inner_32 + i_add_2 - 2);
    inp_i_1 = *(input_inner_32 + i_add_2 - 1);
    inp_i_2 = *(input_inner_32 + i_add_2);
    if ( v102 == v101 )
    {
      sub_40A440(lpMem);
      v102 = lpMem[3];
      v101 = lpMem[0];
      v98 = lpMem[1];
      v100 = lpMem[2];
    }
    v109 = &v100[v102];
    v110 = 0i64;
    if ( v109 >= v101 )
      v110 = v101;
    *(v98 + v109 - v110) = inp_i_0 >> 2;
    v111 = (v102 + 1);
    lpMem[3] = v111;
    v101 = lpMem[0];
    if ( v111 == lpMem[0] )
    {
      sub_40A440(lpMem);
      v101 = lpMem[0];
      v111 = lpMem[3];
    }
    v112 = ((inp_i_1 >> 4) | (16 * inp_i_0)) & 0x3F;
    v98 = lpMem[1];
    v100 = lpMem[2];
    v113 = 0i64;
    if ( lpMem[2] + v111 >= v101 )
      v113 = v101;
    *(lpMem[1] + lpMem[2] + v111 - v113) = v112;
    v114 = v111 + 1;
    lpMem[3] = v114;
    if ( v114 == v101 )
    {
      sub_40A440(lpMem);
      v114 = lpMem[3];
      v101 = lpMem[0];
      v98 = lpMem[1];
      v100 = lpMem[2];
    }
    v115 = ((inp_i_2 >> 6) | (4 * inp_i_1)) & 0x3F;
    v116 = 0i64;
    if ( &v100[v114] >= v101 )
      v116 = v101;
    *(v98 + &v100[v114] - v116) = v115;
    v117 = v114 + 1;
    lpMem[3] = v117;
    if ( v117 == v101 )
    {
      sub_40A440(lpMem);
      v117 = lpMem[3];
      v101 = lpMem[0];
      v98 = lpMem[1];
      v100 = lpMem[2];
    }
    v103 = inp_i_2 & 0x3F;
    v104 = 0i64;
    if ( &v100[v117] >= v101 )
      v104 = v101;
    *(v98 + &v100[v117] - v104) = v103;
    v102 = (v117 + 1);
    lpMem[3] = v102;
    i_add_2 += 3i64;
  }
  while ( i_add_2 != 35 );

enc(&Src, (v124 << 8) + (inp_32to44[v120 - v122 + 1] << 16) - 0x4EFFFFE8, 0x3000201u);

# 提取出的22次enc的参数，用0000暂代被校验的两字节
l = [(0xb1000018, 0x03000201), (0xa4090000, 0x03020100), (0x002aa600, 0x02010003), (0x001b009e, 0x02000103), (0x00570096, 0x02000103), (0x00ad005d, 0x02000103), (0xae750000, 0x02030100), (0x0065ac00, 0x01020300), (0x00008c09, 0x01000203), (0x000076a0, 0x01000203), (0x472c0000, 0x02030100), (0x10000001, 0x00030201), (0x007c000f, 0x00020301), (0x00ba0047, 0x00020301), (0x00953000, 0x01020003), (0x74009b00, 0x03010200), (0x2d00003f, 0x03000102), (0x00009a2d, 0x01000203), (0x00003187, 0x01000302), (0x0000ba43, 0x00010302), (0x00002c70, 0x01000302), (0x56004c00, 0x03010200)]
for t in l:
    rslt = 0
    for i in range(4):
        x = (t[1] >> (i * 8)) & 0xFF
        rslt |= ((t[0] >> (x * 8)) & 0xFF) << (i * 8)
    print(hex(rslt))

if ( !Src.check_flag )
  {
    lpMem[0] = &off_443340; // "You Get FLAG!n"
    lpMem[1] = 1;
    lpMem[2] = &off_442D60;
    *&lpMem[3] = 0i64;
    result = sub_42E480(lpMem);
  }

if ( vm->r1 )
          ++vm->check_flag;

LOBYTE(v3) = vm->r2;
        vm->r1 ^= v3;
        return v3;

'''
movzx   eax, byte ptr [rsi+419h]
xor     [rsi+418h], al
'''
with open("vm_r", "w") as f:
    f.write("")
while True:
    wait_for_next_event(WFNE_CONT, 3)
    rsi = get_reg_value("rsi")
    with open("vm_r", "a") as f:
        s = get_bytes(rsi+0x418, 2)
        get = "0x" + hex(s[0])[2:].rjust(2, "0") + " ^ 0x" + hex(s[1])[2:].rjust(2, "0") + "n"
        f.write(get)

无论输入是什么（以测试第3个字节时的第5-6行数据为例），红框位置和黄框位置的数据是不变的，其中黄框数据为前面构造函数enc的第二个参数时的常量中的其中一个字节（如这里的0x09来自0xa4090000）。

蓝框位置数据恒为输入数据经过前面“3字节变4字节”转换后的结果。

绿框位置数据是红框位置数据和蓝框位置数据xor的结果。

r1 = f(x)
r1 ^= y
r1 ^= C

l = []
for i in range(44*2):
    wait_for_next_event(WFNE_CONT, 3)
    if i & 1 == 0:
        rsi = get_reg_value("rsi")
        s = get_wide_byte(rsi+0x418)
        l.append(s)
print(l)
# [0, 130, 17, 146, 168, 57, 130, 40, 154, 97, 88, 139, 162, 67, 104, 137, 4, 143, 176, 67, 73, 58, 24, 57, 114, 12, 186, 118, 152, 19, 139, 70, 51, 43, 37, 162, 139, 39, 183, 97, 124, 63, 88, 86]

# from debugging
key1 = [0, 130, 17, 146, 168, 57, 130, 40, 154, 97, 88, 139, 162, 67, 104, 137, 4, 143, 176, 67, 73, 58, 24, 57, 114, 12, 186, 118, 152, 19, 139, 70, 51, 43, 37, 162, 139, 39, 183, 97, 124, 63, 88, 86]
# enc's args
key2 = []
l = [(0xb1000018, 0x03000201), (0xa4090000, 0x03020100), (0x002aa600, 0x02010003), (0x001b009e, 0x02000103), (0x00570096, 0x02000103), (0x00ad005d, 0x02000103), (0xae750000, 0x02030100), (0x0065ac00, 0x01020300), (0x00008c09, 0x01000203), (0x000076a0, 0x01000203), (0x472c0000, 0x02030100), (0x10000001, 0x00030201), (0x007c000f, 0x00020301), (0x00ba0047, 0x00020301), (0x00953000, 0x01020003), (0x74009b00, 0x03010200), (0x2d00003f, 0x03000102), (0x00009a2d, 0x01000203), (0x00003187, 0x01000302), (0x0000ba43, 0x00010302), (0x00002c70, 0x01000302), (0x56004c00, 0x03010200)]
for t in l:
    for i in range(4):
        x = (t[1] >> (i * 8)) & 0xFF
        if i in [2, 3]:
            key2.append((t[0] >> (x * 8)) & 0xFF)
# get flag's data
flag_data = []
for i in range(len(key1)):
    flag_data.append(key1[i] ^ key2[i])
flag = []
for i in range(0, len(flag_data), 4):
    b = ""
    for j in range(4):
        b += bin(flag_data[i+j])[2:].rjust(6, '0')
    flag += [int(b[i:i+8], 2) for i in range(0, 24, 8)]
print(b"DASCTF{" + bytes(flag)[:-1] + b"}")
# b'DASCTF{c669733af3ce4459b88016420b81cb15}'


```
import chal

flag = input("flag: ")
chal.chal(flag)
```



```
>>> import chal
>>> dir(chal)
['__builtins__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '__test__', 'chal', 'os', 'random']
>>> dir(chal.chal)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_p1', '_p2', '_p3']
>>> chal.chal._p1
<cyfunction chal._p1 at 0x4000fa0450>
>>> chal.chal._p2
<cyfunction chal._p2 at 0x4000fa0520>
>>> chal.chal._p3
<cyfunction chal._p3 at 0x4000fa05f0>
>>> dir(chal.chal("a"))
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_p1', '_p2', '_p3', '_tips', '_var1', '_var2', '_var3']
>>> chal.chal("a")._tips
"Don't peek!!!"
>>> chal.chal("a")._var1
'a'
>>> chal.chal("a")._var2
[121, 73, 141, 146, 115, 230, 181, 65, 238, 17, 146, 73, 228, 82, 188, 66, 12, 148, 225, 66, 255, 254, 47, 22, 163, 250, 222, 133, 35, 232, 106, 176]
>>> chal.chal("a")._var3
[12, 243, 133, 147, 7, 36, 29, 49, 226, 211, 156, 56, 142, 78, 254, 12]
```



```
typedef struct {
    PyObject **p;
    const char *s;
    const Py_ssize_t n;
    const char* encoding;
    const char is_unicode;
    const char is_str;
    const char intern;
} __Pyx_StringTabEntry;
```



```
__m128i v8;
__int64 v9;
__int64 v10;
__int16 v11;
char v12;

v8 = _mm_unpacklo_epi64(&qword_28A98, "AttributeError");
v9 = 15LL;
v10 = 0LL;
v11 = 0x100;
v12 = 1;
```



```
qword_29170 = PyLong_FromLong(113LL, v9, v244, v245);
if ( qword_29170 )
```



```
qword_29600 = PyLong_FromString("2654435769", 0LL, 0LL);
if ( qword_29600 )
```



```
qword_296B8 = _Pyx_GetBuiltinName(qword_28A98);
if ( !qword_296B8 )
  return 0xFFFFFFFFLL;
```



```
qword_29630 = PyTuple_Pack(2LL, qword_29600, qword_29618);
if ( !qword_29630 )
  return 0xFFFFFFFFLL;
```



```
// *** _Pyx_InitCachedConstants ***
// 元组赋值
v1 = PyTuple_Pack(7LL, self, x1, x2, tmp, low, high, ans);
if ( !v1 )
  return 0xFFFFFFFFLL;
// 函数定义
qword_29688 = _Pyx_PyCode_New_constprop_0(
  3, 7, qword_28A80, qword_28A78, qword_28A78, v1, qword_28A78, 
  qword_28A78, chal_py, p1, 19, qword_28A80
);
if ( !qword_29688 )
  return 0xFFFFFFFFLL;
```



```
// *** _pyx_pymod_exec_chal ***
v559 = _Pyx_CyFunction_New_constprop_0(&_pyx_mdef_4chal_4chal_3_p1, chal__p1, chal, _pyx_mstate_global_static, qword_29688);                                
v560 = PyObject_SetItem(v6, p1, v559) >> 31; // self._p1 = v559
```



```
ctypedef struct PyMethodDef:
    const char* ml_name
    PyCFunction ml_meth
    int ml_flags
    const char* ml_doc
```



```
.data:00000000000289C0 AD 41 02 00 00 00 00 00           __pyx_mdef_4chal_4chal_3_p1 dq offset aChalChalP1+0Ah
.data:00000000000289C0                                                                 ; DATA XREF: __pyx_pymod_exec_chal+236B↑o
.data:00000000000289C0                                                                 ; "_p1"
.data:00000000000289C8 70 F7 00 00 00 00 00 00           dq offset __pyx_pw_4chal_4chal_3_p1
.data:00000000000289D0 82 00 00 00                       dd 82h
.data:00000000000289D4 00                                db 0
```



```
v539 = _Pyx_ImportDottedModule_constprop_0(random);
if ( PyDict_SetItem(_pyx_mstate_global_static, random, v539) < 0 )
{
```



```
v22 = PyObject_SetAttr(self, var1, s);
```



```
v23 = PyList_New(32LL); // 1. 创建新的列表对象
v24 = pyx_int_121; // 2. v24 = 121
if ( *pyx_int_121 != -1 ) // 3. 错误处理
  ++*pyx_int_121;
v25 = v23[3]; // 4. 列表对象（v23）的[3]是数据部分
*v25 = v24; // 5. 列表第一个元素为v24即121
// ... 重复以上2、3、5步处理对列表赋值
v58 = PyObject_SetAttr(self, var2, v23);
```



```
v150 = *(*(self + 8) + 144LL);
// v2 = self._p3
    if ( v150 )
      v2 = v150(self, p3);
    else
      v2 = PyObject_GetAttr(self, p3);
    if ( !v2 )
    {
      v101 = 0LL;
      v1 = 0LL;
      v23 = 0LL;
      v122 = 4493LL;
      v123 = 10LL;
      goto LABEL_211;
    }
    if ( *(v2 + 8) == &PyMethod_Type && (v151 = *(v2 + 24)) != 0LL )
    {
      v1 = *(v2 + 16);
      if ( *v151 != -1 )
        ++*v151;
      if ( *v1 != -1 )
        ++*v1;
      if ( *v2 >= 0 )
      {
        v152 = *v2 - 1LL;
        *v2 = v152;
        if ( !v152 )
          _Py_Dealloc(v2);
      }
// 参数是("Don't hook!!!")
      v192 = _mm_loadh_ps(&Don_thook___);
// 函数调用，执行self._p3("Don't hook!!!")，返回值给v23
      v23 = _Pyx_PyObject_FastCallDict_constprop_0(v1, &v192, 2LL);
      if ( *v151 >= 0 )
      {
        v153 = *v151 - 1LL;
        *v151 = v153;
        if ( !v153 )
          _Py_Dealloc(v151);
      }
    }
// 不同的调用方式，和上面的if同层
    else
    {
      v1 = v2;
      v192.m128_u64[0] = 0LL;
      v192.m128_u64[1] = Don_thook___;
      v23 = _Pyx_PyObject_FastCallDict_constprop_0(v2, v187, 1LL);
    }
    if ( !v23 )
    {
      v101 = 0LL;
      v2 = 0LL;
      v122 = 4513LL;
      v123 = 10LL;
      goto LABEL_211;
    }
    if ( *v1 >= 0 )
    {
      v154 = *v1 - 1LL;
      *v1 = v154;
      if ( !v154 )
        _Py_Dealloc(v1);
    }
```



```
v404 = _Pyx_PyObject_GetAttrStr(v403, to_bytes);
v406 = _Pyx_PyObject_Call_constprop_0(v404, t_2_big); // t_2_big是元组(2, 'big')，在_Pyx_InitCachedConstants中有初始化
```



```
v406 = v403.to_bytes(2, 'big')
```



```
// v2 = self._var2
    v155 = *(*(self + 8) + 144LL);
    if ( v155 )
      v2 = v155(self, var2);
    else
      v2 = PyObject_GetAttr(self, var2);
/* 上文返回值v23和v2对比，对比常量：
https://github.com/python/cpython/blob/3.12/Include/object.h#L862
#define Py_LT 0
#define Py_LE 1
#define Py_EQ 2
#define Py_NE 3
#define Py_GT 4
#define Py_GE 5
*/
    v1 = PyObject_RichCompare(v23, v2, 2LL);
// 确定是否IsTrue
    LOBYTE(IsTrue) = v1 == &Py_TrueStruct;
    if ( v1 == &Py_TrueStruct || v1 == &Py_FalseStruct || v1 == &Py_NoneStruct )
    {
      IsTrue = IsTrue;
    }
    else
    {
      IsTrue = PyObject_IsTrue(v1);
    }
// 如果not IsTrue，即 v23 != self._var2
    if ( !IsTrue )
```



```
v2 = PyObject_GetAttr(self, var1);
v91 = PyObject_Size(v2);
v93 = PyLong_FromSsize_t(v91);
```



```
v93 = len(self._var1)
```



```
// v3 = 2654435769 - v93
v3 = PyNumber_Subtract(pyx_int_2654435769, v93);
// v294 = v293 ^ v91
v294 = (__m128 *)PyNumber_Xor(v293, v91);
// v367 = v1229 + v365
v367 = (__int64 *)PyNumber_Add(v1229, v365);
// InPlace字样，这里等同于v1213 = (v483 &= 4294967295)
v1213 = (__int64 *)PyNumber_InPlaceAnd(v483, pyx_int_4294967295);
// m128_u64 = v1213 >> 4
m128_u64 = (_QWORD *)_Pyx_PyInt_RshiftObjC_constprop_0(v1213, pyx_int_4, 4LL);
// v537 = v1225 & 3
v537 = (_QWORD *)_Pyx_PyInt_AndObjC_constprop_0(v1225, pyx_int_3, 3LL, 0LL);
// ItemInt_List_Fast_constprop_0 = v537 + 4
ItemInt_List_Fast_constprop_0 = (__m128 *)_Pyx_PyInt_AddObjC_constprop_0(v537, pyx_int_4, 4LL, 0LL);
// ...
```



```
>>> import chal
>>> setattr(chal.chal, "ori_p1", chal.chal.__dict__["_p1"]) # 保存原来的_p1
>>> def hook_p1(self, a, b): # 写hook函数，打印参数和返回值
...     print(a, b)
...     ret = self.ori_p1(a, b)
...     print(ret)
...     return ret
... 
>>> setattr(chal.chal, "_p1", hook_p1) # 挂上去
>>> chal.chal("a") # 调用后即可看到每次调用self._p1时的参数和返回值，且不影响函数原来的功能
52232 48895
-27712
52883 49898
-25833
64660 29775
-28948
# ... 数据省略
```



```
import os
import random

class chal():
    def __init__(self, s):
        # 变量的开头下划线都没写，懒（
        self.var1 = s
        self.var2 = [121, 73, 141, 146, 115, 230, 181, 65, 238, 17, 146, 73, 228, 82, 188, 66, 12, 148, 225, 66, 255, 254, 47, 22, 163, 250, 222, 133, 35, 232, 106, 176]
        self.var3 = [12, 243, 133, 147, 7, 36, 29, 49, 226, 211, 156, 56, 142, 78, 254, 12]
        random.seed(sum([2654435769-len(s)] + [ord(x) for x in str(len(s))]))
        if self._p3("Don't hook!!!") == self.var2: # 假的check，别信
            print("yes")
        elif self.tips == 0: # 真的check！
            # 有个self._var2 + self._var3，但没有使用
            print("yes")
        self.tips = "Don't peek!!!"

    def _p1(self, a, b): # a * b % 65537
        # print(a, b)
        c = a * b
        cl = c & 0xFFFF
        ch = (c >> 16) & 0xFFFF
        if cl - ch < 0:
            ret = cl - ch + 1
        else:
            ret = cl - ch
        # print(ret)
        return ret

    def _p2(self, i): # sm4 subbytes
        # print(i)
        l = [214, 144, 233, 254, 204, 225, 61, 183, 22, 182, 20, 194, 40, 251, 44, 5, 43, 103, 154, 118, 42, 190, 4, 195, 170, 68, 19, 38, 73, 134, 6, 153, 156, 66, 80, 244, 145, 239, 152, 122, 51, 84, 11, 67, 237, 207, 172, 98, 228, 179, 28, 169, 201, 8, 232, 149, 128, 223, 148, 250, 117, 143, 63, 166, 71, 7, 167, 252, 243, 115, 23, 186, 131, 89, 60, 25, 230, 133, 79, 168, 104, 107, 129, 178, 113, 100, 218, 139, 248, 235, 15, 75, 112, 86, 157, 53, 30, 36, 14, 94, 99, 88, 209, 162, 37, 34, 124, 59, 1, 33, 120, 135, 212, 0, 70, 87, 159, 211, 39, 82, 76, 54, 2, 231, 160, 196, 200, 158, 234, 191, 138, 210, 64, 199, 56, 181, 163, 247, 242, 206, 249, 97, 21, 161, 224, 174, 93, 164, 155, 52, 26, 85, 173, 147, 50, 48, 245, 140, 177, 227, 29, 246, 226, 46, 130, 102, 202, 96, 192, 41, 35, 171, 13, 83, 78, 111, 213, 219, 55, 69, 222, 253, 142, 47, 3, 255, 106, 114, 109, 108, 91, 81, 141, 27, 175, 146, 187, 221, 188, 127, 17, 217, 92, 65, 31, 16, 90, 216, 10, 193, 49, 136, 165, 205, 123, 189, 45, 116, 208, 18, 184, 229, 180, 176, 137, 105, 151, 74, 12, 150, 119, 126, 101, 185, 241, 9, 197, 110, 198, 132, 24, 240, 125, 236, 58, 220, 77, 32, 121, 238, 95, 62, 215, 203, 57, 72]
        ret = int.from_bytes(bytes(map(lambda x: l[x], i.to_bytes(4, 'little'))), 'little')
        # print(ret)
        return ret

    def _p3(self):
        # 开头的lambda是个pkcs5padding，但是输入整块的数据就不重要了（块长度是16
        # s = pkcs5padding(self.var1).encode()
        s = self.var1.encode()
        L = [173, 7, 131, 63, 141, 180, 193, 156, 21, 198, 65, 218, 13, 216, 148, 105, 165, 96, 250, 121, 168, 23, 94, 49, 79, 120, 101, 211, 167, 240, 75, 136, 43, 70, 115, 203, 220, 34, 160, 188, 222, 61, 169, 117, 95, 134, 174, 167]
        tmpl = []
        self.tips = 0
        for i in range(len(s)):
            tmpl.append(L[i%len(L)] ^ s[i])
        rslt = b''
        for i in range(0, len(tmpl), 8):
            longs = tmpl[i:i+8]
            randl = []
            # IDEA的轮密钥
            for _ in range(52):
                randl.append(random.getrandbits(16))
            ll = [] # v141
            for j in range(0, len(longs), 2):
                ll.append(int.from_bytes(longs[j:j+2]))
            assert len(ll) == 4
            v1227, v1229, v1230, v1222 = ll
            for v1232 in range(8):
                v1225 = random.randint(0x9e3779b9, 0xc6ef3720)
                # TEA 密钥
                rilv1224 = []
                for _ in range(8):
                    rilv1224.append(random.randint(0x56AA3350, 0xa3b1bac6))
                # XTEA 密钥
                rilv1228 = []
                for _ in range(8):
                    rilv1228.append(random.randint(0x677D9197, 0xb27022dc))
                # 半轮魔改IDEA
                lv1233 = []
                lv1233.append(self._p1(v1227, randl[6 * v1232 + 0]) & 0xFFFF)
                lv1233.append((v1229 + randl[6 * v1232 + 1]) & 0xFFFF)
                lv1233.append((v1230 + randl[6 * v1232 + 2]) & 0xFFFF)
                lv1233.append(self._p1(v1222, randl[6 * v1232 + 3]) & 0xFFFF)
                lv395 = []
                for j in range(4):
                    lv395.append(lv1233[j].to_bytes(2, 'big'))
                tmps = b''.join(lv395)
                lv424 = []
                for j in range(0, len(tmps), 4):
                    lv424.append(int.from_bytes(tmps[j:j+4], 'little'))
                assert len(lv424) == 2
                # 魔改TEA
                l, r = lv424 # v1213, v1215
                l += ((r << 4) + self._p2(rilv1224[0])) ^ (r + v1225) ^ ((r >> 5) + self._p2(rilv1224[1]))
                l &= 4294967295
                r += ((l << 5) + self._p2(rilv1224[2])) ^ (l + v1225) ^ ((l >> 4) + self._p2(rilv1224[3]))
                r &= 4294967295
                # 魔改XTEA
                l += (((r << 5) ^ (r >> 4)) + r) ^ (v1225 + self._p2(rilv1228[4 + (v1225 & 3)]))
                l &= 4294967295
                r += (((l << 4) ^ (l >> 5)) + l) ^ (v1225 + self._p2(rilv1228[4 + ((v1225 >> 11) & 3)]))
                r &= 4294967295
                # 奇数轮更改v1225（TEA/XTEA中的sum）
                if v1232 & 1 == 1:
                    v1225 = random.getrandbits(32)
                # 魔改TEA
                l += (((r << 3) ^ (r >> 6)) + r) ^ (v1225 + self._p2(rilv1228[v1225 & 3]))
                l &= 4294967295
                r += (((l << 4) ^ (l >> 5)) + l) ^ (v1225 + self._p2(rilv1228[(v1225 >> 11) & 3]))
                r &= 4294967295
                # 魔改XTEA
                l += ((r << 4) + self._p2(rilv1224[4])) ^ (r + v1225) ^ ((r >> 5) + self._p2(rilv1224[5]))
                l &= 4294967295
                r += ((l << 2) + self._p2(rilv1224[6])) ^ (l + v1225) ^ ((l >> 7) + self._p2(rilv1224[7]))
                r &= 4294967295
                tmps = b''.join([x.to_bytes(4, 'little') for x in [l, r]])
                lv770 = []
                for j in range(0, len(tmps), 2):
                    lv770.append(int.from_bytes(tmps[j:j+2], 'big'))
                assert len(lv770) == 4
                # 另外半轮魔改IDEA
                a, b, c, d = lv770 # v1242, v1241, v1240, v1239
                v1196 = self._p1((a ^ c) & 0xFFFF, randl[v1232 * 6 + 4])
                v835 = self._p1(((b ^ d) + v1196) & 0xFFFF, randl[v1232 * 6 + 5]) & 0xFFFF
                v1198 = (v1196 + v835) & 0xFFFF
                v840 = a ^ v835
                v841 = d ^ v1198
                v842 = b ^ v1198
                v91 = c ^ v835
                # 奇数轮和偶数轮交接给下一轮的变量不同
                if v1232 & 1 != 0:
                    v1230 = v91
                    v1229 = v842
                else:
                    v1230 = v842
                    v1229 = v91
                v1222 = v841
                v1227 = v840
            # 最后半轮魔改IDEA
            v1227 = self._p1(v1227 & 0xFFFF, randl[48]) & 0xFFFF
            v1229 = (v1229 + randl[49]) & 0xFFFF
            v1230 = (v1230 + randl[50]) & 0xFFFF
            v1222 = self._p1(v1222 & 0xFFFF, randl[51]) & 0xFFFF
            ll = [v1227, v1229, v1230, v1222]
            lv918 = []
            for j in range(len(ll)):
                lv918.append(ll[j].to_bytes(2, 'big'))
            tmps = b''.join(lv918)
            print(list(tmps))
            rslt += tmps
            # 真正的比对在这里（
            self.tips += sum([tmps[j] ^ random.getrandbits(8) for j in range(len(tmps))])
        print(self.tips, list(rslt))
        # 没用的返回值，真随机
        return [x ^ y for x, y in zip(os.urandom(len(rslt)), rslt)]

if __name__ == '__main__':
    c = chal("a"*48) # 测试
```



```
import random

# 假密文！！！
dst = [121, 73, 141, 146, 115, 230, 181, 65, 238, 17, 146, 73, 228, 82, 188, 66, 12, 148, 225, 66, 255, 254, 47, 22, 163, 250, 222, 133, 35, 232, 106, 176]
dst += [12, 243, 133, 147, 7, 36, 29, 49, 226, 211, 156, 56, 142, 78, 254, 12]
random.seed(sum([2654435769-len(dst)] + [ord(x) for x in str(len(dst))]))

r_randl = []
r8_v1225 = []
r8_rilv1224 = []
r8_rilv1228 = []
r8_rand8b = []
for _ in range(0, len(dst), 8):
    r_randl.append([random.getrandbits(16) for _ in range(52)])
    tmpl = []
    for i in range(8):
        tmpl.append(random.randint(0x9e3779b9, 0xc6ef3720))
        r8_rilv1224.append([random.randint(0x56AA3350, 0xa3b1bac6) for _ in range(8)])
        r8_rilv1228.append([random.randint(0x677D9197, 0xb27022dc) for _ in range(8)])
        if i & 1 == 1:
            tmpl.append(random.getrandbits(32))
    r8_v1225 += tmpl[::-1]
    r8_rand8b.append([random.getrandbits(8) for _ in range(8)])
v1225_iter = iter(r8_v1225)
# 真密文
dst = sum(r8_rand8b, [])

def _p1(a, b):
    c = a * b
    cl = c & 0xFFFF
    ch = (c >> 16) & 0xFFFF
    if cl - ch < 0:
        return cl - ch + 1
    else:
        return cl - ch

def _p2(i):
    l = [214, 144, 233, 254, 204, 225, 61, 183, 22, 182, 20, 194, 40, 251, 44, 5, 43, 103, 154, 118, 42, 190, 4, 195, 170, 68, 19, 38, 73, 134, 6, 153, 156, 66, 80, 244, 145, 239, 152, 122, 51, 84, 11, 67, 237, 207, 172, 98, 228, 179, 28, 169, 201, 8, 232, 149, 128, 223, 148, 250, 117, 143, 63, 166, 71, 7, 167, 252, 243, 115, 23, 186, 131, 89, 60, 25, 230, 133, 79, 168, 104, 107, 129, 178, 113, 100, 218, 139, 248, 235, 15, 75, 112, 86, 157, 53, 30, 36, 14, 94, 99, 88, 209, 162, 37, 34, 124, 59, 1, 33, 120, 135, 212, 0, 70, 87, 159, 211, 39, 82, 76, 54, 2, 231, 160, 196, 200, 158, 234, 191, 138, 210, 64, 199, 56, 181, 163, 247, 242, 206, 249, 97, 21, 161, 224, 174, 93, 164, 155, 52, 26, 85, 173, 147, 50, 48, 245, 140, 177, 227, 29, 246, 226, 46, 130, 102, 202, 96, 192, 41, 35, 171, 13, 83, 78, 111, 213, 219, 55, 69, 222, 253, 142, 47, 3, 255, 106, 114, 109, 108, 91, 81, 141, 27, 175, 146, 187, 221, 188, 127, 17, 217, 92, 65, 31, 16, 90, 216, 10, 193, 49, 136, 165, 205, 123, 189, 45, 116, 208, 18, 184, 229, 180, 176, 137, 105, 151, 74, 12, 150, 119, 126, 101, 185, 241, 9, 197, 110, 198, 132, 24, 240, 125, 236, 58, 220, 77, 32, 121, 238, 95, 62, 215, 203, 57, 72]
    return int.from_bytes(bytes(map(lambda x: l[x], i.to_bytes(4, 'little'))), 'little')

def p1_rev(ret, b):
    for i in range(0x10000):
        if ret == (_p1(i, b) & 0xFFFF):
            return i

res = b''
for xi in range(0, len(dst), 8):
    randl = r_randl[xi//8]
    l8 = dst[xi:xi+8]
    l4 = [int.from_bytes(bytes(l8[i:i+2]), 'big') for i in range(0, len(l8), 2)]
    v1227, v1229, v1230, v1222 = l4
    v1227 = p1_rev(v1227, randl[48]) & 0xFFFF
    v1229 = (v1229 - randl[49]) & 0xFFFF
    v1230 = (v1230 - randl[50]) & 0xFFFF
    v1222 = p1_rev(v1222, randl[51]) & 0xFFFF
    for i in range(8)[::-1]:
        rilv1224 = r8_rilv1224[xi + i]
        rilv1228 = r8_rilv1228[xi + i]
        v841 = v1222
        v840 = v1227
        if i & 1 != 0:
            v91 = v1230
            v842 = v1229
        else:
            v842 = v1230
            v91 = v1229
        a_xor_c = v840 ^ v91
        b_xor_d = v841 ^ v842
        v1196 = _p1(a_xor_c, randl[i * 6 + 4]) & 0xFFFF
        v835 = _p1((b_xor_d + v1196) & 0xFFFF, randl[i * 6 + 5]) & 0xFFFF
        v1198 = (v1196 + v835) & 0xFFFF
        a = v840 ^ v835
        b = v842 ^ v1198
        c = v91 ^ v835
        d = v841 ^ v1198
        l4 = [a, b, c, d]
        s = b''.join([x.to_bytes(2, 'big') for x in l4])
        l, r = [int.from_bytes(s[j:j+4], 'little') for j in range(0, len(s), 4)]
        v1225 = next(v1225_iter)
        r -= ((l << 2) + _p2(rilv1224[6])) ^ (l + v1225) ^ ((l >> 7) + _p2(rilv1224[7]))
        r &= 4294967295
        l -= ((r << 4) + _p2(rilv1224[4])) ^ (r + v1225) ^ ((r >> 5) + _p2(rilv1224[5]))
        l &= 4294967295
        r -= (((l << 4) ^ (l >> 5)) + l) ^ (v1225 + _p2(rilv1228[(v1225 >> 11) & 3]))
        r &= 4294967295
        l -= (((r << 3) ^ (r >> 6)) + r) ^ (v1225 + _p2(rilv1228[v1225 & 3]))
        l &= 4294967295
        if i & 1 == 1:
            v1225 = next(v1225_iter)
        r -= (((l << 4) ^ (l >> 5)) + l) ^ (v1225 + _p2(rilv1228[4 + ((v1225 >> 11) & 3)]))
        r &= 4294967295
        l -= (((r << 5) ^ (r >> 4)) + r) ^ (v1225 + _p2(rilv1228[4 + (v1225 & 3)]))
        l &= 4294967295
        r -= ((l << 5) + _p2(rilv1224[2])) ^ (l + v1225) ^ ((l >> 4) + _p2(rilv1224[3]))
        r &= 4294967295
        l -= ((r << 4) + _p2(rilv1224[0])) ^ (r + v1225) ^ ((r >> 5) + _p2(rilv1224[1]))
        l &= 4294967295
        s = b''.join([x.to_bytes(4, 'little') for x in [l, r]])
        v1227, v1229, v1230, v1222 = [int.from_bytes(s[j:j+2], 'big') for j in range(0, len(s), 2)]
        v1227 = p1_rev(v1227, randl[6 * i + 0]) & 0xFFFF
        v1229 = (v1229 - randl[6 * i + 1]) & 0xFFFF
        v1230 = (v1230 - randl[6 * i + 2]) & 0xFFFF
        v1222 = p1_rev(v1222, randl[6 * i + 3]) & 0xFFFF
    res += b''.join([x.to_bytes(2, 'big') for x in [v1227, v1229, v1230, v1222]])

L = [173, 7, 131, 63, 141, 180, 193, 156, 21, 198, 65, 218, 13, 216, 148, 105, 165, 96, 250, 121, 168, 23, 94, 49, 79, 120, 101, 211, 167, 240, 75, 136, 43, 70, 115, 203, 220, 34, 160, 188, 222, 61, 169, 117, 95, 134, 174, 167]
flag = []
for i in range(len(res)):
    flag.append(res[i] ^ L[i%len(L)])
print(bytes(flag))
# b'DASCTF{c6090fd29eaf2ae1d111289e3f3c0c7a3819dcc1}'
```



```
# ... 从vb脚本搬过来，省略
yyjskEVAnLNVYXPjnqeGNhKNvXlbSIslOoqViLKkb = BumFQkMgMUNykMNviBlfdZHOyVThmijmcNTUNaXSNHYdNzXKRqhYiKlaRzCfBlcoN + dWPtWzWvKrZRFrsAWZMGNjZQbCrgAImKXVUkOykXWeRltpUU + AMaKeZzlhAtdNANKAKwMNbKEKUWuQVZQbbCJIUog + BvEKpalonhsRIgbPkYPYbsbQGzIzvPitapncgtGKIo + yBILPYnXCUApVHExOtpKlnfTkVfexwgrFQOFIveA + pqdgalQAZJKIDySPundFqdITahrgAYveJXfZCOUHWnUDKXZwZU + pErQJcjFIvYQeIehtTPMaOgEwFvvjnaTkabtJDvpHbWG

import base64
# 测试套了两层base64
res = base64.b64decode(yyjskEVAnLNVYXPjnqeGNhKNvXlbSIslOoqViLKkb)
res = base64.b64decode(res)
with open("temp.exe", "wb") as f:
    f.write(res)
```



```
v9[0] = 4288;
// ... v9赋值，省略
  v9[53] = 7808;
  if ( a1 == 2 )
  {
    for ( j = 0; j < (int)j_strlen(*(const char **)(a2 + 8)) && (unsigned __int64)j < 0x36; ++j )
      v9[j + 64] = *(char *)(*(_QWORD *)(a2 + 8) + j) << 6;
    for ( j = 0; (unsigned __int64)j < 0x36; ++j )
    {
      if ( v9[j] != v9[j + 64] )
      {
        printf("bad");
        v4 = 0i64;
        goto LABEL_16;
      }
    }
    printf("good");
    v4 = 0i64;
```



```
# v9
dst = [4288, 4480, 5376, 4352, 5312, 4160, 7936, 5184, 6464, 6528, 5632, 3456, 7424, 5632, 6336, 6528, 6720, 6144, 6272, 7488, 6656, 7296, 7424, 2432, 2432, 2432, 5632, 4416, 3456, 7168, 6528, 7488, 6272, 5632, 3520, 6208, 5632, 4736, 6528, 6400, 7488, 3520, 5632, 5184, 3456, 7488, 7296, 3200, 6272, 7424, 2432, 2432, 2432, 7808]
for i in range(len(dst)):
    dst[i] = (dst[i] >> 6) ^ 7
print(bytes(dst))
# b'DASCTF{Vba_1s_dangerous!!!_B1ware_0f_Macr0_V1ru5es!!!}'
```



```
// input
puts("Please input your flag~");
scanf("%s", flag);
len = strlen(flag);
if ( len != 33 )
{
  puts("Len error!");
  exit(0);
}
// check
for ( i = 0; i <= 32; ++i )
{
  if ( std::abs(check[i] - in[i]) > (long double)(double)0.0001 )
  {
    puts("Wrong!!");
    exit(0);
  }
}
puts("Right!!");
```



```
rot13_encrypt(flag);
```



```
for ( i = 0; strlen(flag) > i; ++i )
{
  v2 = flag[i];
  *std::vector<int>::operator[]((std::vector<int> *const)i, v11) = v2;
}
encrypt((std::vector<double> *)((char *)__n + 1), &input);
```



```
std::vector<double> *__cdecl encrypt(std::vector<double> *retstr, const std::vector<int> *input)
{
  // ...
  for ( i = 0; i < size; ++i )
  {
    for ( j = 0; j < size; ++j )
    {
      v5 = (double)*std::vector<int>::operator[]((const std::vector<int> *const)j, v10);
      v2 = cos(((long double)j + 0.5) * ((long double)i * 3.141592653589793) / (long double)size);
      v6 = v2 * v5;
      v3 = std::vector<double>::operator[]((std::vector<double> *const)i, v11);
      *v3 = *v3 + v6;
    }
    if ( i )
      v4 = sqrt(2.0 / (long double)size);
    else
      v4 = sqrt(1.0 / (long double)size);
    v7 = v4;
    eax9 = std::vector<double>::operator[]((std::vector<double> *const)i, v12);
    *eax9 = *eax9 * v7;
  }
}
```



```
from math import sqrt, cos, pi

l = [513.355, -37.7986, 8.7316, -10.7832, -1.3097, -20.5779, 6.98641, -29.2989, 15.9422, 21.4138, 29.4754, -2.77161, -6.58794, -4.22332, -7.20771, 8.83506, -4.38138, -19.3898, 18.3453, 6.88259, -14.7652, 14.6102, 24.7414, -11.6222, -9.754759999999999, 12.2424, 13.4343, -34.9307, -35.735, -20.0848, 39.689, 21.879, 26.8296]
n = len(l)

# IDCT from https://github.com/lquatrin/CGT1-1D_DCT_IDCT/blob/master/CG_T1/src/MyDCTS.cpp
flag = []
for i in range(n):
    x = 0
    for j in range(n):
        if j != 0:
            x += l[j] * cos(((((2.0*i)+1.0)*j)*pi)/(2.0*n))
        else:
            x += l[j] * (1.0 / sqrt(2)) * cos(((((2.0*i)+1.0)*j)*pi)/(2.0*n))
    flag.append(round(sqrt(2.0 / n) * x))

# rot13
for i in range(n):
    if flag[i] in range(ord('A'), ord('Z')+1):
        base = ord('A')
    elif flag[i] in range(ord('a'), ord('z')+1):
        base = ord('a')
    else:
        continue
    flag[i] = (flag[i]-base+13) % 26 + base
print(bytes(flag))
# b'DASCTF{Wh0_1s_Ma1n_@nd_FunnY_Dct}'
```



```
.text:000000000049DB31
.text:000000000049DB31 loc_49DB31:
.text:000000000049DB31 movzx   r9d, byte ptr [rsi+rbx]
.text:000000000049DB36 xor     r9d, edx
.text:000000000049DB39 mov     [rax+rbx], r9b
.text:000000000049DB3D inc     rbx
```



```
.text:000000000049DB5F movzx   r11d, byte ptr [rbx+rax]
.text:000000000049DB64 inc     r9d             ; int
.text:000000000049DB67 movzx   r12d, r9b
.text:000000000049DB6B mov     r13d, [rdx+r12*4]
.text:000000000049DB6F add     r10d, r13d      ; int
.text:000000000049DB72 movzx   r15d, r10b
.text:000000000049DB76 mov     esi, r11d
.text:000000000049DB79 mov     r11d, [rdx+r15*4]
.text:000000000049DB7D mov     [rdx+r12*4], r11d
.text:000000000049DB81 mov     [rdx+r15*4], r13d
.text:000000000049DB85 mov     r11d, [rdx+r12*4]
.text:000000000049DB89 add     r11d, r13d
.text:000000000049DB8C movzx   r11d, r11b      ; int
.text:000000000049DB90 xor     esi, [rdx+r11*4]
.text:000000000049DB94 xor     esi, 11h
.text:000000000049DB97 mov     [rax+rbx], sil
.text:000000000049DB9B inc     rbx
.text:000000000049DB9E xchg    ax, ax
```



```
#include <stdio.h>
#include <string.h>

unsigned char S_Box[256] = {0};
// RC4 initial
void Init(unsigned char * key, int keyLen) {
    unsigned char T[256] = {0};
    for (int i = 0; i < 256; i++) {
        S_Box[i] = i;
        T[i] = key[i%keyLen];
    }
    int j = 0;
    for (int i = 0; i < 256; i++) {
        j = (j+S_Box[i]+T[i]) % 256;
        unsigned char tmp = S_Box[i];
        S_Box[i] = S_Box[j];
        S_Box[j] = tmp;
    }
    return;
}

void RC4(unsigned char * key, int keyLen, unsigned char * data, int dataLen) {
    Init(key, keyLen);
    int i = 0, j = 0;
    for (int k = 0; k < dataLen; k++) {
        i = (i+1) % 256;
        j = (j+S_Box[i]) % 256;
        unsigned char tmp = S_Box[i];
        S_Box[i] = S_Box[j];
        S_Box[j] = tmp;
        data[k] ^= S_Box[(S_Box[i]+S_Box[j])%256] ^ key[1] ^ 0x11;
    }
}

unsigned char magic[8] = {137, 80, 78, 71, 13, 10, 26, 10}; // png文件头
int isFind(unsigned char * data) {
    for (int i = 0; i < 8; i++) {
        if (data[i] != magic[i]) {
            return 0;
        }
    }
    return 1;
}

int main() {
    int png_size = 552205;
    unsigned char png[552205+1] = {0};
    FILE * fp = fopen("flag.png", "rb");
    fread(png, sizeof(char), png_size, fp);
    fclose(fp);
    unsigned char key[5+1] = {0};
    unsigned char data[552205+1] = {0};
    unsigned char charset[] = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    int charset_size = 62;
    unsigned char find = 0;
    for (int i0 = 0; i0 < charset_size; i0++) {
        for (int i1 = 0; i1 < charset_size; i1++) {
            for (int i2 = 0; i2 < charset_size; i2++) {
                for (int i3 = 0; i3 < charset_size; i3++) {
                    for (int i4 = 0; i4 < charset_size; i4++) {
                        key[0] = charset[i0];
                        key[1] = charset[i1];
                        key[2] = charset[i2];
                        key[3] = charset[i3];
                        key[4] = charset[i4];
                        memcpy(data, png, png_size);
                        RC4(key, 5, data, png_size);
                        if (isFind(data)) {
                            find = 1;
                            printf("find key: %sn", key);
                            fp = fopen("res.png", "wb");
                            fwrite(data, sizeof(char), png_size, fp);
                            fclose(fp);
                            break;
                        }
                    }
                    if (find) break;
                }
                if (find) break;
            }
            if (find) break;
        }
        if (find) break;
    }
    return 0;
}
```



```
00000000 vm struc ; (sizeof=0x420, align=0x8, mappedto_64)
00000000   l1 db 1024 dup(?)
00000400   l2 dw 8 dup(?)
00000410   l3 db 8 dup(?)
00000418   r1 db ?
00000419   r2 db ?
0000041A   r3 db ?
0000041B   r4 db ?
0000041C   check_flag db ?
0000041D   db ? ; undefined
0000041E   db ? ; undefined
0000041F   db ? ; undefined
00000420 vm ends
```



```
if ( *(input + 39) != 125 )
    goto LABEL_251;
```



```
do                                            // 3*8 -> 4*6
  {
    i0 = i_add_2 - 2;
    if ( i_add_2 - 2 >= v97 )
    {
      v189 = &off_443350;
      goto LABEL_261;
    }
    i0 = i_add_2 - 1;
    if ( i_add_2 - 1 >= v97 )
    {
      v189 = &off_443368;
      goto LABEL_261;
    }
    if ( i_add_2 >= v97 )
    {
      i0 = i_add_2;
      v189 = &off_443380;
LABEL_261:
      panic(i0, v97, v189);
    }
    inp_i_0 = *(input_inner_32 + i_add_2 - 2);
    inp_i_1 = *(input_inner_32 + i_add_2 - 1);
    inp_i_2 = *(input_inner_32 + i_add_2);
    if ( v102 == v101 )
    {
      sub_40A440(lpMem);
      v102 = lpMem[3];
      v101 = lpMem[0];
      v98 = lpMem[1];
      v100 = lpMem[2];
    }
    v109 = &v100[v102];
    v110 = 0i64;
    if ( v109 >= v101 )
      v110 = v101;
    *(v98 + v109 - v110) = inp_i_0 >> 2;
    v111 = (v102 + 1);
    lpMem[3] = v111;
    v101 = lpMem[0];
    if ( v111 == lpMem[0] )
    {
      sub_40A440(lpMem);
      v101 = lpMem[0];
      v111 = lpMem[3];
    }
    v112 = ((inp_i_1 >> 4) | (16 * inp_i_0)) & 0x3F;
    v98 = lpMem[1];
    v100 = lpMem[2];
    v113 = 0i64;
    if ( lpMem[2] + v111 >= v101 )
      v113 = v101;
    *(lpMem[1] + lpMem[2] + v111 - v113) = v112;
    v114 = v111 + 1;
    lpMem[3] = v114;
    if ( v114 == v101 )
    {
      sub_40A440(lpMem);
      v114 = lpMem[3];
      v101 = lpMem[0];
      v98 = lpMem[1];
      v100 = lpMem[2];
    }
    v115 = ((inp_i_2 >> 6) | (4 * inp_i_1)) & 0x3F;
    v116 = 0i64;
    if ( &v100[v114] >= v101 )
      v116 = v101;
    *(v98 + &v100[v114] - v116) = v115;
    v117 = v114 + 1;
    lpMem[3] = v117;
    if ( v117 == v101 )
    {
      sub_40A440(lpMem);
      v117 = lpMem[3];
      v101 = lpMem[0];
      v98 = lpMem[1];
      v100 = lpMem[2];
    }
    v103 = inp_i_2 & 0x3F;
    v104 = 0i64;
    if ( &v100[v117] >= v101 )
      v104 = v101;
    *(v98 + &v100[v117] - v104) = v103;
    v102 = (v117 + 1);
    lpMem[3] = v102;
    i_add_2 += 3i64;
  }
  while ( i_add_2 != 35 );
```



```
enc(&Src, (v124 << 8) + (inp_32to44[v120 - v122 + 1] << 16) - 0x4EFFFFE8, 0x3000201u);
```



```
# 提取出的22次enc的参数，用0000暂代被校验的两字节
l = [(0xb1000018, 0x03000201), (0xa4090000, 0x03020100), (0x002aa600, 0x02010003), (0x001b009e, 0x02000103), (0x00570096, 0x02000103), (0x00ad005d, 0x02000103), (0xae750000, 0x02030100), (0x0065ac00, 0x01020300), (0x00008c09, 0x01000203), (0x000076a0, 0x01000203), (0x472c0000, 0x02030100), (0x10000001, 0x00030201), (0x007c000f, 0x00020301), (0x00ba0047, 0x00020301), (0x00953000, 0x01020003), (0x74009b00, 0x03010200), (0x2d00003f, 0x03000102), (0x00009a2d, 0x01000203), (0x00003187, 0x01000302), (0x0000ba43, 0x00010302), (0x00002c70, 0x01000302), (0x56004c00, 0x03010200)]
for t in l:
    rslt = 0
    for i in range(4):
        x = (t[1] >> (i * 8)) & 0xFF
        rslt |= ((t[0] >> (x * 8)) & 0xFF) << (i * 8)
    print(hex(rslt))
```



```
if ( !Src.check_flag )
  {
    lpMem[0] = &off_443340; // "You Get FLAG!n"
    lpMem[1] = 1;
    lpMem[2] = &off_442D60;
    *&lpMem[3] = 0i64;
    result = sub_42E480(lpMem);
  }
```



```
if ( vm->r1 )
          ++vm->check_flag;
```



```
LOBYTE(v3) = vm->r2;
        vm->r1 ^= v3;
        return v3;
```



```
'''
movzx   eax, byte ptr [rsi+419h]
xor     [rsi+418h], al
'''
with open("vm_r", "w") as f:
    f.write("")
while True:
    wait_for_next_event(WFNE_CONT, 3)
    rsi = get_reg_value("rsi")
    with open("vm_r", "a") as f:
        s = get_bytes(rsi+0x418, 2)
        get = "0x" + hex(s[0])[2:].rjust(2, "0") + " ^ 0x" + hex(s[1])[2:].rjust(2, "0") + "n"
        f.write(get)
```



```
r1 = f(x)
r1 ^= y
r1 ^= C
```



```
l = []
for i in range(44*2):
    wait_for_next_event(WFNE_CONT, 3)
    if i & 1 == 0:
        rsi = get_reg_value("rsi")
        s = get_wide_byte(rsi+0x418)
        l.append(s)
print(l)
# [0, 130, 17, 146, 168, 57, 130, 40, 154, 97, 88, 139, 162, 67, 104, 137, 4, 143, 176, 67, 73, 58, 24, 57, 114, 12, 186, 118, 152, 19, 139, 70, 51, 43, 37, 162, 139, 39, 183, 97, 124, 63, 88, 86]
```



```
# from debugging
key1 = [0, 130, 17, 146, 168, 57, 130, 40, 154, 97, 88, 139, 162, 67, 104, 137, 4, 143, 176, 67, 73, 58, 24, 57, 114, 12, 186, 118, 152, 19, 139, 70, 51, 43, 37, 162, 139, 39, 183, 97, 124, 63, 88, 86]
# enc's args
key2 = []
l = [(0xb1000018, 0x03000201), (0xa4090000, 0x03020100), (0x002aa600, 0x02010003), (0x001b009e, 0x02000103), (0x00570096, 0x02000103), (0x00ad005d, 0x02000103), (0xae750000, 0x02030100), (0x0065ac00, 0x01020300), (0x00008c09, 0x01000203), (0x000076a0, 0x01000203), (0x472c0000, 0x02030100), (0x10000001, 0x00030201), (0x007c000f, 0x00020301), (0x00ba0047, 0x00020301), (0x00953000, 0x01020003), (0x74009b00, 0x03010200), (0x2d00003f, 0x03000102), (0x00009a2d, 0x01000203), (0x00003187, 0x01000302), (0x0000ba43, 0x00010302), (0x00002c70, 0x01000302), (0x56004c00, 0x03010200)]
for t in l:
    for i in range(4):
        x = (t[1] >> (i * 8)) & 0xFF
        if i in [2, 3]:
            key2.append((t[0] >> (x * 8)) & 0xFF)
# get flag's data
flag_data = []
for i in range(len(key1)):
    flag_data.append(key1[i] ^ key2[i])
flag = []
for i in range(0, len(flag_data), 4):
    b = ""
    for j in range(4):
        b += bin(flag_data[i+j])[2:].rjust(6, '0')
    flag += [int(b[i:i+8], 2) for i in range(0, 24, 8)]
print(b"DASCTF{" + bytes(flag)[:-1] + b"}")
# b'DASCTF{c669733af3ce4459b88016420b81cb15}'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/4-1725517079.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/3-1725517086.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/0-1725517090.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/1-1725517091.png)