# Apiculture 1 write-up-针对API的渗透测试

> 原文: https://www.ctfiot.com/107011.html
> ID: 107011

养蜂业挑战赛专门针对API攻击。这基本上是一个蜂蜜成瘾者网站：

为了解决第一个挑战，我们应该注意对/API/products/ API的调用：

此端点向Angular前端提供信息，以便页面可以在浏览器中呈现……但它受到不当数据过滤漏洞的影响，因为它会显示网页中未使用的数据[即vendorID字段]。我们确实可以发现所有产品都是由同一个供应商发布的，其ID为57336：

然后，我们应该尝试发现其他端点。幸运的是，开发人员在/api/swagger.json中保留了他的API的详细描述：

/API/flags/ endpoint听起来特别有趣…但它受到Basic Auth的保护：

让我们看看/API/vendors/端点。当我们提供通过最初的不当数据过滤漏洞泄露的供应商ID时，它会显示有趣的信息：

因此，我们知道供应商是一个简单的用户，我们有他的密码哈希。这个SHA1哈希可以快速破解，或者简单地在谷歌上搜索以获得该供应商的弱密码：

然而，它不允许访问受限的/API/flags/ endpoint……但是我们可以利用不安全的直接对象引用漏洞来获取其他供应商的信息：

经过几次尝试后，我们发现供应商57332是管理员：

而且他的弱密码也可以很容易地被谷歌到：

我们现在可以使用www.example.com用户和abeille密码以Antonio Rodrigo NOGUEIRA的身份登录arn@gmail.br：

最后欣赏我们的Flag：

原文始发于微信公众号（闲聊知识铺）：Apiculture 1 write-up-针对API的渗透测试

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/3-1680276600.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/2-1680276600.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/10-1680276601.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/0-1680276601.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/0-1680276601.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/3-1680276602.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/10-1680276602.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/6-1680276603.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/3-1680276603.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/1-1680276603.png)