# 调教GPT-4：一道签到题的生成过程

> 原文: https://www.ctfiot.com/108677.html
> ID: 108677

前言

在筹备数据安全产业人才能力挑战赛初赛的过程中，我心血来潮，想要尝试使用当前热门的GPT-4，来为大赛设计一道独特的签到题。

GPT-4，作为一款自然语言处理模型，已经在诸如文本生成、机器翻译、摘要提取等领域展现出了卓越的性能。我希望通过调教GPT-4，能够实现在签到题设计中的突破和创新，进一步激发参赛者的兴趣和参与热情。

在本篇文章中，我将向大家分享使用GPT-4制作签到题的实践经历，以及在这一过程中所收获的心得和感悟。

第一次prompt

一开始，带着好奇心的我为GPT-4设定了一个关于网络数据安全的初始prompt（提示词），旨在引导模型理解我的需求，并作出相应的回应。

帮我出一个基础的简单的web题，web题是网络数据安全比赛中的一种题型。我希望它是一个签到题，但所用到的技术点、漏洞点需要是新颖的，不要脑洞题，也不要是市面上常见的。最后，输出代码请一定要完整输出，如果代码太长的话，请分两次甚至三次输出给我。

（之所以有最后一句话，是因为GPT-4模型的每一次的输出长度有限制，我奢想能连续分几次输出给我，但事实上，一旦输出停止后，还需要手动输入“继续”以引导模型继续输出）

安装依赖：

在你的项目目录下，创建一个虚拟环境并激活它。

运行pip install Flask Flask-SQLAlchemy来安装所需的依赖。

解题思路：

首先观察app.py中的index视图函数，发现它从request.form中获取name和email，然后将其存入User表。这里没有过滤用户输入，因此可能存在注入漏洞。

仔细查看models.py文件，User表使用了SQLAlchemy ORM进行数据库操作。SQLAlchemy ORM通常能很好地防止SQL注入。但在这个问题中，我们需要找到一个不常见的漏洞点。

注意到email字段被设置为unique，这意味着我们可以尝试插入具有相同电子邮件的用户，以测试系统如何处理这种情况。

在签到系统中尝试输入以下信息：

提交表单后，你会看到Alice已成功签到。

现在我们知道，如果尝试插入具有相同电子邮件的用户，将导致操作失败。然而，这给我们提供了一个线索：我们可以尝试使用特殊字符对输入进行处理，以查看是否可以利用这个特点。

在签到系统中尝试输入以下信息：

我们发现，在某些情况下，由于不安全的SQLAlchemy ORM使用，使得输入不当的电子邮件地址可能导致数据记录被篡改。这就是这个题目的新颖漏洞点。

这题的flag在哪里，该如何设计进去？

（看了上面GPT-4给设计的“使得输入不当的电子邮件地址可能导致数据记录被篡改”，心生疑惑，但还是先让它把题目设计完整）

关于这题，选手不看源码的话能知道我们做题的要求吗？

在index.html模板中添加一个提示，指示有一个特殊的电子邮件地址可以解锁flag。例如：

当用户尝试使用特殊电子邮件地址签到但失败时，返回一个具有提示性的错误消息。例如，您可以修改index视图函数，以便在检查到特殊电子邮件地址时返回提示：

另外，您可以在题目描述中提供一些关于漏洞的线索。例如，您可以告诉选手这道题涉及到的是一个与电子邮件地址验证相关的漏洞，并鼓励他们尝试不同的输入来挖掘漏洞。

那选手又怎么能找到这个特殊的电子邮件地址呢？

我搭建好了，运行后报错

sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
[SQL: INSERT INTO user (name, email) VALUES (?, ?)]

首先，在app.py中导入db：

然后，在app.py的末尾添加以下代码：

（这里GPT-4的修改建议也是不行的，正确的做法如下）

db.init_app(app)
# 添加以下2行
with app.app_context():
    db.create_all()

（我自己修改后，再进行测试前面我所疑惑的点，果真是行不通的漏洞利用）

我按你上面所教的“提交表单后，你将发现Carol成功签到，尽管她使用的电子邮件与Alice相同。”，但事实上是前端提示需要正确的邮件格式，即使我绕过前端的限制，再去提交，页面报错(sqlite3.IntegrityError) UNIQUE constraint failed

在这个修订后的例子中，我们将关注如何使用不同的电子邮件地址绕过签到限制，而不是覆盖现有记录。现在，请按照以下步骤操作：

使用Alice的姓名和电子邮件地址（例如alice@example.com）进行签到。

现在，尝试使用Carol的姓名和相同的电子邮件地址（alice@example.com）进行签到。这将失败，因为电子邮件地址已经存在。

接下来，尝试使用Carol的姓名和以下电子邮件地址进行签到：alice@example.com#carol。这将成功，因为电子邮件地址在视觉上看起来与Alice的不同，但在实际处理时，注释符号（#）后面的部分将被忽略，从而使系统将此视为相同的电子邮件地址。

但这样插入的还是alice@example.com#carol，有没有可能真的绕过唯一性的限制。

为了帮助选手找到特殊电子邮件地址，您可以在题目中提供一些线索。以下是一些建议：

在HTML代码中隐藏线索。在index.html模板中，您可以将电子邮件地址的部分信息作为线索添加到注释中，例如：

在错误消息中提供线索。当选手尝试使用错误的电子邮件地址进行签到时，您可以返回一个具有提示性的错误消息。例如，您可以在index视图函数中添加一个条件，以便在检查到特殊电子邮件地址的部分匹配时返回提示：

在题目描述中提供线索。您可以告诉选手这道题涉及到的是一个与电子邮件地址相关的挑战，并鼓励他们尝试不同的输入来找到特殊电子邮件地址。例如，您可以在题目描述中添加如下内容：

能不能弄点有趣点的漏洞？

（感觉相当费力，生成的题目漏洞不能利用，其还能口若悬河般地输出，然后还需要我自己来进行验证和纠正。）

耐心的尝试

当然可以！这是一个有趣的漏洞示例，涉及到HTTP请求伪造。

题目描述：

欢迎来到签到系统！我们使用了最新的技术确保数据安全。然而，据说有一个HTTP请求伪造漏洞存在于这个系统中。你能利用这个漏洞成功签到两次吗？

漏洞原理：这个漏洞利用了HTTP头中X-Forwarded-For字段的缺陷。当处理用户请求时，我们的应用程序会将X-Forwarded-For字段的值作为用户的IP地址。攻击者可以通过伪造该字段的值，伪装成来自不同IP地址的用户，从而绕过限制，允许他们进行多次签到。

为了实现这个漏洞，我们需要修改app.py：

首先，添加一个新的字段ip到User模型：

在app.py的index视图函数中，我们需要从HTTP请求的头部获取X-Forwarded-For字段，并将其作为用户的IP地址存储到数据库中。首先，导入request：

更新index视图函数，以获取X-Forwarded-For字段的值，并将其作为用户的IP地址存储到数据库中：

要获取flag，选手需要：

使用一个有效的姓名和电子邮件地址进行签到。

伪造X-Forwarded-For头部字段，将其设置为不同的IP地址，然后再次使用相同的姓名和电子邮件地址进行签到。

怎么在原先的web签到系统上，设置简单的新颖的能利用的漏洞点？

（XFF头的考察方式过于基础，而且由于其常见性，它所涉及的内容并未满足我对“有趣”这词的期望。）

在models.py中，为User模型添加一个timestamp字段，以便记录签到时间：

修改app.py中的index视图函数，以获取最近签到的用户并将其传递给模板：

更新index.html模板以显示最近签到的用户列表：

但是这样是如何设计获取flag？

要获得 flag，选手需要执行以下步骤：

观察到最近签到用户列表中的名字没有进行 HTML 转义，发现 XSS 漏洞。

分析页面源代码，找到隐藏的 getFlag() 函数。

构造一个包含执行 getFlag() 函数的 JavaScript 代码的名字，例如：

提交签到表单，使用包含恶意 JavaScript 代码的名字。

但是我如果可以看到源代码，看到getFlag()函数，我不就可以直接看到flag了吗？

在 app.py 文件中，添加一个新的路由，用于处理获取 flag 的请求：

在 index.html 文件中，添加一个 JavaScript 函数，用于触发 AJAX 请求并在成功时显示 flag：

那我还是可以直接调用这个requestFlag()来获得flag，这个验证逻辑该怎么写？

（我按下了“Stop generating”按钮）

算了，我不要xss漏洞，我希望能在原来的web签到系统里，增加sql注入漏洞，注入方式得较新颖。

（再回到最开始，直接指明sql注入，看能得到什么）

在app.py中，添加一个新的路由，用于处理搜索请求：

创建一个新的模板文件search.html，用于显示搜索表单和结果：

为了使漏洞更具挑战性，您可以将flag隐藏在一个特殊的用户记录中。例如，在数据库中添加一个具有以下信息的用户：

名字：Flag Bearer

电子邮件：flag{SQL_Inj3cti0n_N3w_Styl3}@example.com

那么能否给我设计一个SQLAlchemy的漏洞，要真实有用的。

能发散你的思维吗，给我一个新颖的简单的有趣的ctf签到题。

（想在SQLAlchemy查询上搞出新花样，似乎对它有点苛求。）

在app.py中，添加一个新的路由，用于显示包含加密flag的页面：

创建一个简单的加密函数encrypt()：

创建一……

（又一次按下“Stop generating”按钮）

我要的是新颖的，凯撒密码这种很基础很常见了。

在app.py中，添加一个新的路由，用于显示包含编码flag的页面：

创建一个简单的自定义编码函数custom_encode()：

作为一名选手，你该如何分析出来解码器呢？还有你这样这题的考察点就偏重于编码解密。能否给我一个web上的新颖（重点）+简单的漏洞？

（对于分析解码器的这类题目，缺乏密码学技能的选手很难完成。）

在app.py中，添加一个新的路由，用于处理请求头挑战：

创建两个模板文件。首先是header_challenge.html，它包含关于如何完成挑战的提示：

（再一次按下“Stop generating”按钮）

我需要一个新颖，一般没考过的web题考点。

SVG签到挑战

了解您的需求，这里有一个使用SVG图片的XXE漏洞挑战，相对较新颖且不常见。

我们将创建一个简单的Web应用程序，允许用户上传SVG图片。然后，我们将在服务器端解析这些图片，这就为XXE漏洞提供了机会。

在app.py中，添加一个新的路由以处理文件上传和显示结果：

创建一个上传表单模板upload.html：

创建一个用于显示SVG的模板svg_viewer.html：

怎么我测试后，能看到的红色举行上面的是 &xxe; 并没有解析

（SVG中的XXE漏洞较少被考察，而且利用难度不高，就先尝试往这个方面去出个签到题吧）

修改app.py中的uploaded_file函数，将其改为允许访问内部Web应用程序：

在服务器上创建一个内部Web应用程序，例如一个包含flag的简单页面：

（这里它这么折腾，还是我自己改吧，修改python代码让其允许外部实体解析：parser = etree.XMLParser(resolve_entities=True)）

回到上一步吧，app.py里至少有/的路由，有按钮可以指向/upload，另外整体页面请变得好看。

代码里自动新建uploads文件夹，且查看具体文件那里加个返回首页的按钮。

所有界面加个底部栏 coded by GPT-4

我按你上面所写的去修改了，但是没有显示底部栏，这是为何？

我希望首页默认就显示一个svg图，在其底下才是现在的挑战按钮。至于svg图我希望是跟“数据安全”有关的。

（我与GPT-4探讨了关于SVG形状构造的复杂性和创意。然而，它创作出的SVG形状过于基础且单调。关于这一过程的讨论，就不在此赘述了。）

（关于前端样式的调教过程，也略过。）

在首页增加一个提示按钮，点击后弹窗，弹窗里有一个公众号二维码，底部有一句关注公众号发送xx获取提示。

首先是2个按钮重叠在一起了，得排版好其位置。其次是点击获取提示的按钮，没有弹框。

（尽管与GPT-4讨论了很长时间，但它仍未能解决模态框无法弹出的问题。后面我发现模态框代码使用的是data-bs-target这个属性，经搜索发现是bootstrap 5的新属性，而项目里是使用flaskbootstrap模块，默认是4版本，把5的新属性全改为4的即可）

/upload如果上传非svg文件得报错提示。

RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.

当我上传一个非svg文件时，flash的内容怎么没看到？

（flash是Flask框架中的一个功能，用于在不同请求之间传递消息的方法。通常情况下，这些消息只会显示一次，主要用于向用户显示有关表单提交或其他操作的反馈。）

（随后，我又讨论了许多前端样式等细节问题，并最终使用Bing Images生成了背景图片，并在公众号里设置了相关的提示。至此，一道签到题终于完成了。）

总结

事情的进展并非总能如愿，刚开始的尝试阶段，GPT-4生成的签到题并未达到我所期望的水平。尽管模型展现出了一定的语义理解能力和创造力，但生成的签到题过于普通，缺乏足够的挑战性和针对性。

准确性问题同样令人头疼，GPT-4生成的题目或多或少存在一些技术细节上的错误，需要使用者亲自核查和修正，这无疑对使用者的能力提出了更高的要求。

当然，GPT-4的一些优势相当明显：迅速生成题目以节省时间，涵盖众多领域，通过多次互动实现持续优化。

从目前的情况来看，要使用GPT-4制作满足需求的CTF题目，仍需投入更多精力，深入挖掘其潜能，并在实践过程中不断调整和优化。

在下一次比赛中，我将继续使用GPT-4创作出更出色的题目，请大家拭目以待。

春秋伽玛，邀请大家踊跃投稿，期待大家的智慧火花，一起书写精彩篇章。

✦  +

+

有话说

如果您有比赛想要宣传，欢迎联系我们刊登发布

如果您想练习历史大赛CTF题目，欢迎体验演武场

https://arena.ichunqiu.com/

扫描关注下方春秋GAME官方公众号

发送“演武场”三字可了解更多关于演武场的信息

发送“了解”两字即可加入春秋赛事宇宙官方微信群

春秋GAME期待与您的见面~~~

+ + + + + + + + + + +


```
from flask import Flask, render_template, request, redirect, url_for
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('index.html')

@app
.route('/success')
def success():
    users = User.query.all()
    return render_template('success.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>签到系统</title>
</head>

    <h1>欢迎来到签到系统</h1>
    <form method="post" action="/">
        <label for="name">姓名：</label>
        


        <label for="email">邮箱：</label>
        


        签到
    </form>

</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>签到成功</title>
</head>

    <h1>签到成功！</h1>
    <h2>已签到的用户列表：</h2>
    
        {% for user in users %}
        <li>{{ user.name }} - {{ user.email }}</li>
        {% endfor %}
    

</html>
姓名：Alice
邮箱：test@example.com
姓名：Bob
邮箱：test@example.com
姓名：Carol
邮箱：test@example.com' -- '
import re
def is_valid_email(email):
    pattern = r'^[w.-]+@[w.-]+.w+$'
    return bool(re.match(pattern, email))
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        if not is_valid_email(email):
            # 如果电子邮件无效，返回错误信息
            return 'Invalid email address', 400

        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('index.html')
existing_user = User.query.filter_by(email=email).first()
if existing_user:
    # 如果电子邮件已存在，返回错误信息
    return 'Email address already exists', 400
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        if not is_valid_email(email):
            # 如果电子邮件无效，返回错误信息
            return 'Invalid email address', 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # 如果电子邮件已存在，返回错误信息
            return 'Email address already exists', 400

        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('index.html')
SPECIAL_EMAIL = 'flag@example.com'
FLAG = 'flag{5ql4lch3my_0rm_1nj3ct10n}'
@app.route('/success')
def success():
    users = User.query.all()
    show_flag = any(user.email == SPECIAL_EMAIL for user in users)
    return render_template('success.html', users=users, show_flag=show_flag, flag=FLAG)
{% if show_flag %}
    <h2>恭喜！你找到了flag：</h2>
    {{ flag }}
{% endif %}
<!-- 提示：找到特殊的电子邮件地址，解锁flag！ -->
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        if not is_valid_email(email):
            # 如果电子邮件无效，返回错误信息
            return 'Invalid email address', 400

        if email == SPECIAL_EMAIL:
            # 如果电子邮件是特殊的电子邮件地址，给出提示
            return 'Hmm... this email address looks special, but something is not quite right.', 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # 如果电子邮件已存在，返回错误信息
            return 'Email address already exists', 400

        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('index.html')
<!-- 有传言说，一个特殊的电子邮件地址可能会为你带来惊喜。它看起来像这样：flag@*****
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
[SQL: INSERT INTO user (name, email) VALUES (?, ?)]
from models import db
if __name__ == '__main__':
    db.create_all(app=app)
    app.run(debug=True)
db.init_app(app)
# 添加以下2行
with app.app_context():
    db.create_all()
<!-- 有传言说，一个特殊的电子邮件地址可能会为你带来惊喜。它看起来像这样：flag@*****.com -->
if "flag@" in email and email != SPECIAL_EMAIL:
    return 'You are close! Keep searching for the special email address.', 400
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    ip = db.Column(db.String(40), nullable=False)  # 新增字段
from flask import Flask, render_template, request, redirect, url_for
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        # ...其他代码...

        user = User(name=name, email=email, ip=ip)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    # ...其他代码...
from datetime import datetime

class User(db.Model):
    # ...其他字段...
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
@app.route('/', methods=['GET', 'POST'])
def index():
    # ...其他代码...

    recent_users = User.query.order_by(User.timestamp.desc()).limit(5).all()
    return render_template('index.html', recent_users=recent_users)
<!-- 其他HTML代码 -->

<h3>最近签到的用户：</h3>

{% for user in recent_users %}
  <li>{{ user.name }}</li>
{% endfor %}


<!-- 其他HTML代码 -->
<script>alert('XSS!')</script>
<li>{{ user.name|safe }}</li>
<script>
  function getFlag() {
    var flag = "FLAG{XSS_1s_Fun_123}";
    alert("恭喜！你找到了 flag：" + flag);
  }
</script>
<script>getFlag();</script>
@app.route('/get_flag', methods=['POST'])
def get_flag():
    # 可以添加验证逻辑，例如检查请求头或其他信息以确认是通过 XSS 触发的请求
    flag = "FLAG{XSS_1s_Fun_123}"
    return jsonify({'flag': flag})
<script>
  function requestFlag() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/get_flag", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4 && xhr.status == 200) {
        var jsonResponse = JSON.parse(xhr.responseText);
        var flag = jsonResponse.flag;
        alert("恭喜！你找到了 flag：" + flag);
      }
    };
    xhr.send();
  }
</script>
from flask import request, jsonify

@app.route('/get_flag', methods=['POST'])
def get_flag():
    # 验证 Referer 请求头是否来自预期的来源
    expected_referer = request.url_root
    actual_referer = request.headers.get('Referer', '')

    if actual_referer.startswith(expected_referer):
        flag = "FLAG{XSS_1s_Fun_123}"
        return jsonify({'flag': flag})
    else:
        return jsonify({'error': 'Invalid request'}), 403
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        search_name = request.form['search_name']
        
        # 使用原始 SQL 查询，而不是使用 SQLAlchemy 的查询构造器
        sql_query = "SELECT * FROM user WHERE name LIKE '%" + search_name + "%'"
        results = db.engine.execute(sql_query)

    return render_template('search.html', results=results)
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <title>搜索签到记录</title>
  </head>
  
    
      <h1>搜索签到记录</h1>
      <form method="POST" action="{{ url_for('search') }}">
        
          <label for="search_name" class="form-label">名字：</label>
          
        
        搜索
      </form>
  {% if results %}
    <h3>搜索结果：</h3>
    
      
        
          ID
          名字
          电子邮件
        
      
      
        {% for result in results %}
          
            {{ result.id }}
            {{ result.name }}
            {{ result.email }}
          
        {% endfor %}
      
    
  {% endif %}


<!-- Optional JavaScript -->
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.7/dist/umd/popper.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js"></script>
  
</html>
%' OR 1=1;--
SELECT * FROM user WHERE name LIKE '%%' OR 1=1;--%'
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        search_name = request.form['search_name']
        
        # 使用不安全的字符串格式化
        unsafe_sql = "name LIKE '%%%s%%'" % search_name
        results = User.query.filter(db.text(unsafe_sql)).all()

    return render_template('search.html', results=results)
results = User.query.filter(User.name.like('%' + search_name + '%')).all()
@app.route('/crypto_challenge')
def crypto_challenge():
    flag = "FLAG{CrYpTo_Ch@LL3nGe}"
    encrypted_flag = encrypt(flag)
    return render_template('crypto_challenge.html', encrypted_flag=encrypted_flag)
def encrypt(plain_text):
    key = 13
    encrypted_text = ""
    for char in plain_text:
        if char.isalpha():
            shift = key % 26
            if char.islower():
                encrypted_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:
                encrypted_text += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            encrypted_text += char
    return encrypted_text
@app.route('/custom_encoding_challenge')
def custom_encoding_challenge():
    flag = "FLAG{Cu5t0m_3nc0d1nG}"
    encoded_flag = custom_encode(flag)
    return render_template('custom_encoding_challenge.html', encoded_flag=encoded_flag)
def custom_encode(plain_text):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_{}"
    custom_alphabet = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM5678901234}{"
    encoding_map = str.maketrans(alphabet, custom_alphabet)
    encoded_text = plain_text.translate(encoding_map)
    return encoded_text
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Custom Encoding Challenge</title>
  </head>
  
    
      <h1>自定义编码挑战</h1>
      以下是经过自定义编码的flag：
      {{ encoded_flag }}
      你的任务是解码flag并提交。
    
    <!-- Optional JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.7/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js"></script>
  
</html>
def custom_decode(encoded_text):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_{}"
    custom_alphabet = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM5678901234}{"
    decoding_map = str.maketrans(custom_alphabet, alphabet)
    decoded_text = encoded_text.translate(decoding_map)
    return decoded_text
from flask import request

@app.route('/header_challenge')
def header_challenge():
    user_agent = request.headers.get('User-Agent')
    if user_agent and "SecretBrowser" in user_agent:
        return render_template('header_flag.html')
    else:
        return render_template('header_challenge.html')
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Header Challenge</title>
  </head>
  
    
      <h1>请求头挑战</h1>
      你必须使用一种名为“SecretBrowser”的特殊浏览器访问此页面，以查看flag。
    
    <script src="
import os
from flask import request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from lxml import etree

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'svg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    parser = etree.XMLParser(resolve_entities=False)
    try:
        tree = etree.parse(file_path, parser)
        svg_data = etree.tostring(tree, encoding='unicode', pretty_print=True)
        return render_template('svg_viewer.html', svg_data=svg_data)
    
except Exception as e:
        return str(e)
<!doctype html>
<html>
  <head>
    <title>SVG上传</title>
  </head>
  
    <h1>上传SVG文件</h1>
    <form method="post" enctype="multipart/form-data">
      
      
    </form>
  
</html>
<!doctype html>
<html>
  <head>
    <title>SVG查看器</title>
  </head>
  
    <h1>SVG查看器</h1>
    {{ svg_data | safe }}
  
</html>
FLAG{Svg_XxE_Fun}
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [
    <!ENTITY xxe SYSTEM "file:///path/to/flag.txt">
]>
<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="red"/>
  <text x="50%" y="50%" font-size="24" text-anchor="middle" fill="white">&xxe;</text>
</svg>
from urllib.parse import unquote
import requests

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    parser = etree.XMLParser(resolve_entities=False)
    try:
        tree = etree.parse(file_path, parser)
        xlink_ns = "http://www.w3.org/1999/xlink"
        for element in tree.iterfind(".//{*}image"):
            href = element.get("{%s}href" % xlink_ns)
            if href and href.startswith("http"):
                response = requests.get(href)
                element.set("{%s}href" % xlink_ns, f"data:
image/png;base64,{response.content.decode('utf-8')}")
        svg_data = etree.tostring(tree, encoding='unicode', pretty_print=True)
        return render_template('svg_viewer.html', svg_data=svg_data)
    
except Exception as e:
        return str(e)
@app.route('/internal_flag')
def internal_flag():
    return "FLAG{Svg_Ssrf_Fun}"
<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg" xmlns:
xlink="http://www.w3.org/1999/xlink">
  
</svg>
pip install Flask-Bootstrap
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')
{% extends "bootstrap/base.html" %}

{% block title %}SVG挑战{% endblock %}

{% block content %}
  
    <h1 class="text-center">SVG挑战</h1>
    
      [上传SVG文件]({{ url_for('upload_file') }})
    
  
{% endblock %}
{% extends "bootstrap/base.html" %}

{% block title %}SVG上传{% endblock %}

{% block content %}
  
    <h1 class="text-center">上传SVG文件</h1>
    <form method="post" enctype="multipart/form-data" class="text-center">
      
        
      
      上传
    </form>
  
{% endblock %}
{% extends "bootstrap/base.html" %}

{% block title %}SVG查看器{% endblock %}

{% block content %}
  
    <h1 class="text-center">SVG查看器</h1>
    {{ svg_data | safe }}
  
{% endblock %}
import os

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
{% extends "bootstrap/base.html" %}

{% block title %}SVG查看器{% endblock %}

{% block content %}
  
    <h1 class="text-center">SVG查看器</h1>
    {{ svg_data | safe }}
    
      [返回首页]({{ url_for('index') }})
    
  
{% endblock %}
{% extends "bootstrap/base.html" %}

{% block footer %}
  <footer class="footer mt-auto py-3 bg-light fixed-bottom">
    
      coded by GPT-4
    
  </footer>
{% endblock %}
{% extends "base.html" %}

{% block title %}SVG挑战{% endblock %}

{% block content %}
  
    <h1 class="text-center">SVG挑战</h1>
    
      [上传SVG文件]({{ url_for('upload_file') }})
    
  
{% endblock %}
{% extends "base.html" %}

{% block title %}SVG上传{% endblock %}

{% block content %}
  
    <h1 class="text-center">上传SVG文件</h1>
    <form method="post" enctype="multipart/form-data" class="text-center">
      
        
      
      上传
    </form>
  
{% endblock %}
{% extends "base.html" %}

{% block title %}SVG查看器{% endblock %}

{% block content %}
  
    <h1 class="text-center">SVG查看器</h1>
    {{ svg_data | safe }}
    
      [返回首页]({{ url_for('index') }})
    
  
{% endblock %}
<footer class="footer mt-auto py-3 bg-light fixed-bottom">
  
    coded by ChatGPT
  
</footer>
{% include '_footer.html' %}
{% extends "base.html" %}

{% block title %}SVG挑战{% endblock %}

{% block content %}
  
    <h1 class="text-center">SVG挑战</h1>
    
      
    
    
      获取提示
    
    
      [上传SVG文件]({{ url_for('upload_file') }})
    
  

  <!-- Hint Modal -->
  
    
      
        
          <h5 class="modal-title" id="hintModalLabel">获取提示</h5>
          
        
        
            
        
        
            关注公众号发送xx获取提示
        
    
  

{% include '_footer.html' %}
{% endblock %}
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Check if the file is an SVG
            if file.filename.rsplit('.', 1)[1].lower() != 'svg':
                flash('只允许上传 SVG 文件！', 'danger')
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
        else:
            flash('请选择一个文件！', 'warning')
    return render_template('upload.html')
app.secret_key = os.urandom(24)
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      
        {{ message }}
        
      
    {% endfor %}
  {% endif %}
{% endwith %}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/8-1681116874.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/1-1681116874.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/5-1681116875.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1681116875.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/5-1681116875.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/10-1681116875.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1681116875.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1681116876.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/7-1681116876.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/1-1681116876.png)