# Frida Hook Android method（一）

> 原文: https://www.ctfiot.com/151304.html
> ID: 151304

MainActivity.this.check(i, Integer.parseInt(obj));

final int i = get_random();

int get_random() { return new Random().nextInt(100);}

void check(int i, int i2) { if ((i * 2) + 4 == i2) { Toast.makeText(getApplicationContext(), "Yey you guessed it right", 1).show(); StringBuilder sb = new StringBuilder(); for (int i3 = 0; i3 < 20; i3++) { char charAt = "AMDYV{WVWT_CJJF_0s1}".charAt(i3); if (charAt < 'a' || charAt > 'z') { if (charAt >= 'A') { if (charAt <= 'Z') { charAt = (char) (charAt - 21); if (charAt >= 'A') { } charAt = (char) (charAt + 26); } } sb.append(charAt); } else { charAt = (char) (charAt - 21); if (charAt >= 'a') { sb.append(charAt); } charAt = (char) (charAt + 26); sb.append(charAt); } } this.t1.setText(sb.toString()); return; } Toast.makeText(getApplicationContext(), "Try again", 1).show(); }

(i * 2) + 4 == i2

Java.perform(function() { var a = Java.use("com.ad2001.frida0x1.MainActivity"); a.get_random.implementation = function() { console.log("成功Hook获取0-99随机整数的方法"); var ret_val = this.get_random(); console.log("随机数为：" + ret_val); return ret_val; } });

Java.perform(function() { var a = Java.use("com.ad2001.frida0x1.MainActivity"); a.get_random.implementation = function() { console.log("成功Hook获取0-99随机整数的方法"); var ret_val = this.get_random(); console.log("随机数为：" + ret_val); console.log("答案是：" + (ret_val * 2 + 4 ))//TO bypass the check return ret_val; } });

Java.perform(function() { var a = Java.use("com.ad2001.frida0x1.MainActivity"); a.check.overload('int', 'int').implementation = function(a, b) { console.log("你输入的是：" + b); this.check(8, 20); }});


```
MainActivity.this.check(i, Integer.parseInt(obj));
```



```
final int i = get_random();
```



```
int get_random() { return new Random().nextInt(100);}
```



```
void check(int i, int i2) { if ((i * 2) + 4 == i2) { Toast.makeText(getApplicationContext(), "Yey you guessed it right", 1).show(); StringBuilder sb = new StringBuilder(); for (int i3 = 0; i3 < 20; i3++) { char charAt = "AMDYV{WVWT_CJJF_0s1}".charAt(i3); if (charAt < 'a' || charAt > 'z') { if (charAt >= 'A') { if (charAt <= 'Z') { charAt = (char) (charAt - 21); if (charAt >= 'A') { } charAt = (char) (charAt + 26); } } sb.append(charAt); } else { charAt = (char) (charAt - 21); if (charAt >= 'a') { sb.append(charAt); } charAt = (char) (charAt + 26); sb.append(charAt); } } this.t1.setText(sb.toString()); return; } Toast.makeText(getApplicationContext(), "Try again", 1).show(); }
```



```
(i * 2) + 4 == i2
```



```
Java.perform(function() { var a = Java.use("com.ad2001.frida0x1.MainActivity"); a.get_random.implementation = function() { console.log("成功Hook获取0-99随机整数的方法"); var ret_val = this.get_random(); console.log("随机数为：" + ret_val); return ret_val; } });
```



```
Java.perform(function() { var a = Java.use("com.ad2001.frida0x1.MainActivity"); a.get_random.implementation = function() { console.log("成功Hook获取0-99随机整数的方法"); var ret_val = this.get_random(); console.log("随机数为：" + ret_val); console.log("答案是：" + (ret_val * 2 + 4 ))//TO bypass the check return ret_val; } });
```



```
Java.perform(function() { var a = Java.use("com.ad2001.frida0x1.MainActivity"); a.check.overload('int', 'int').implementation = function(a, b) { console.log("你输入的是：" + b); this.check(8, 20); }});
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/6-1702468722.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1702468723.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/8-1702468725.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/4-1702468726.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1702468728.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/2-1702468729.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/8-1702468730.png)