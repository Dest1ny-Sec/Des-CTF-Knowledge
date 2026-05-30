# OSCTF Writeups

> 原文: https://www.ctfiot.com/194159.html
> ID: 194159


```
function checkFlag() {
 const flagInput = document.getElementById('flagInput').value;
 const result = document.getElementById('result');
 const flag = "OSCTF{■■■■■■■■■■■■}";

 if (flagInput === flag) {
 result.textContent = "Congratulations! You found the flag!";
 result.style.color = "green";
 } else {
 result.textContent = "Incorrect flag. Try again.";
 result.style.color = "red";
 }
}
OPTIONS /get-flag HTTP/1.1
Host: 34.16.207.52:
4789
HEAD /get-flag HTTP/1.1
Host: 34.16.207.52:
4789
```
