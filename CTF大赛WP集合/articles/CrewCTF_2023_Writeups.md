# CrewCTF 2023 Writeups

> 原文: https://www.ctfiot.com/124083.html
> ID: 124083


```
sequence = request.args.get('sequence', None)
if sequence is None:
 return render_template('index.html')

script_file = os.path.basename(sequence + '.dc')
if ' ' in script_file or 'flag' in script_file:
 return ':('

proc = subprocess.run(
 ['dc', script_file], 
 capture_output=True,
 text=True,
 timeout=1,
)
output = proc.stdout
```



```
const { FLAG } = await import(`http://${PROVIDER_HOST}/?token=${PROVIDER_TOKEN}`);
```



```
$ deno info
DENO_DIR location: /home/app/.cache/deno
Remote modules cache: /home/app/.cache/deno/deps
npm modules cache: /home/app/.cache/deno/npm
Emitted modules cache: /home/app/.cache/deno/gen
Language server registries cache: /home/app/.cache/deno/registries
Origin storage: /home/app/.cache/deno/location_data
```
