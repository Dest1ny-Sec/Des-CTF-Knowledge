---
title: ByteCTF 2022 mobile 系列 - Silver Droid
contest: ByteCTF
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [WebView拦截, /local_cache/ 路径, 腾讯COS POC URL, am broadcast SET_FLAG, FlagReceiver exported=false, root bypass, FileInputStream, .myqcloud.com白名单, byte_unzip, run.sh, avdmanager, emulator, WebViewClient.shouldInterceptRequest]
attack_chain:
  - 攻击者提供 https://...cos.ap-nanjing.myqcloud.com/.../poc.apk
  - server.py 启动 emulator pixel_xl_api_30 + adb install poc.apk
  - am broadcast -W -a com.wuhengctf.SET_FLAG -n com.bytectf.silverdroid/.FlagReceiver -e flag 'flag{...}'
  - root 状态绕过 exported=false 限制
  - am start -W -n com.bytectf.silverdroid/.MainActivity -d "https://...cos..."
  - MainActivity: getIntent().getData() 拿 URL
  - WebView loadUrl("https://bytectf-...myqcloud.com/jump.html?url=" + uri0)
  - shouldOverrideUrlLoading 拦截: scheme=https + host .myqcloud.com 结尾返回 false 不拦截
  - shouldInterceptRequest: 拦截 /local_cache/ 路径, 读 cacheDir 文件返回
key_payload: 'cos.ap-nanjing.myqcloud.com URL / am broadcast -e flag / root bypass exported / /local_cache/ cacheDir / shouldInterceptRequest'
one_liner: ByteCTF 2022 Silver Droid — 攻击者提供腾讯 COS POC URL + 模拟器启动 + am broadcast SET_FLAG 走 root 旁路 exported + MainActivity WebView + shouldOverrideUrlLoading 验证 .myqcloud.com + shouldInterceptRequest 拦截 /local_cache/ cacheDir 文件。
lesson: WebView shouldOverrideUrlLoading + shouldInterceptRequest 是 Android 经典链;root 状态下 exported=false 可被 am broadcast bypass;cos.ap-nanjing.myqcloud.com 白名单是 bypass 套路。
quality: high
---

# ByteCTF 2022 mobile 系列 - Silver Droid

## 速读
ByteCTF 2022 mobile 题 — Silver Droid 模拟器 + 腾讯 COS POC + WebView 拦截。

## 流程

### 1. 攻击者 POC
- URL: `https://your-cos.cos.ap-nanjing.myqcloud.com/poc.apk`
- 必须 https 开头 + .myqcloud.com 结尾

### 2. server.py
```python
# 启动 emulator
emulator = setup_emulator()  # pixel_xl_api_30 -no-cache -no-snapshot

# 装 apk
adb_install(APK_FILE)

# 广播传 flag (root 绕过 exported=false)
adb_broadcast("com.wuhengctf.SET_FLAG", 
              f"{VULER}/.FlagReceiver", 
              extras={"flag": f.read()})

# 启动 MainActivity 传 URL
adb_activity(f"{VULER}/.MainActivity", 
             wait=True, 
             data=url)
```

### 3. MainActivity
```java
Uri uri0 = this.getIntent().getData();
if (uri0 != null) {
    WebView webView = new WebView(this);
    webView.setWebViewClient(new WebViewClient() {
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
            try {
                Uri u = Uri.parse(url);
                if (u.getScheme().equals("https")) {
                    return !u.getHost().endsWith(".myqcloud.com");
                }
            } catch (Exception e) {
                return true;
            }
            return true;
        }
    });
    
    webView.setWebViewClient(new WebViewClient() {
        @Override
        public WebResourceResponse shouldInterceptRequest(
                WebView view, WebResourceRequest request) {
            Uri uri0 = request.getUrl();
            if (uri0.getPath().startsWith("/local_cache/")) {
                File cacheFile = new File(
                    MainActivity.this.getCacheDir(), 
                    uri0.getLastPathSegment());
                if (cacheFile.exists()) {
                    InputStream is = new FileInputStream(cacheFile);
                    HashMap headers = new HashMap();
                    headers.put("Access-Control-Allow-Origin", "*");
                    return new WebResourceResponse(
                        "text/html", "utf-8", 200, "OK", 
                        headers, is);
                }
            }
            return super.shouldInterceptRequest(view, request);
        }
    });
    
    webView.loadUrl("https://bytectf-...cos.ap-nanjing.myqcloud.com/jump.html?url=" + uri0);
}
```

## 关键
- 腾讯 COS 是白名单 (.myqcloud.com)
- `/local_cache/` 路径被拦截,读 cacheDir 文件
- root 状态下 am broadcast 可绕过 exported=false
