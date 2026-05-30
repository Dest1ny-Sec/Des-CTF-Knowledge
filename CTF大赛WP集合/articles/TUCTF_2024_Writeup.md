# TUCTF 2024 Writeup

> 原文: https://www.ctfiot.com/226943.html
> ID: 226943


```
S = "reingvbaonetr"
for s in S:
 tmp = ord(s) - 0x61
 print(chr(tmp + 0x54),end="")
```



```
from PIL import Image
import numpy as np
import crc8

def main():
 inp = input("""
 Welcome to the TU Image Program
 It can convert images to TIMGs
 It will also display TIGMs

 [1] Convert Image to TIMG
 [2] Display TIMG

 """)
 match inp:
 case "1":
 conv()
 case "2":
 display() #TODO: Add
 '''
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⠛⠛⠛⠿⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⡀⠠⠤⠒⢂⣉⣉⣉⣑⣒⣒⠒⠒⠒⠒⠒⠒⠒⠀⠀⠐⠒⠚⠻⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⡠⠔⠉⣀⠔⠒⠉⣀⣀⠀⠀⠀⣀⡀⠈⠉⠑⠒⠒⠒⠒⠒⠈⠉⠉⠉⠁⠂⠀⠈⠙⢿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠔⠁⠠⠖⠡⠔⠊⠀⠀⠀⠀⠀⠀⠀⠐⡄⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠉⠲⢄⠀⠀⠀⠈⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠊⠀⢀⣀⣤⣤⣤⣤⣀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠜⠀⠀⠀⠀⣀⡀⠀⠈⠃⠀⠀⠀⠸⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠥⠐⠂⠀⠀⠀⠀⡄⠀⠰⢺⣿⣿⣿⣿⣿⣟⠀⠈⠐⢤⠀⠀⠀⠀⠀⠀⢀⣠⣶⣾⣯⠀⠀⠉⠂⠀⠠⠤⢄⣀⠙⢿⣿⣿
⣿⡿⠋⠡⠐⠈⣉⠭⠤⠤⢄⡀⠈⠀⠈⠁⠉⠁⡠⠀⠀⠀⠉⠐⠠⠔⠀⠀⠀⠀⠀⠲⣿⠿⠛⠛⠓⠒⠂⠀⠀⠀⠀⠀⠀⠠⡉⢢⠙⣿
⣿⠀⢀⠁⠀⠊⠀⠀⠀⠀⠀⠈⠁⠒⠂⠀⠒⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⢀⣀⡠⠔⠒⠒⠂⠀⠈⠀⡇⣿
⣿⠀⢸⠀⠀⠀⢀⣀⡠⠋⠓⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠈⠢⠤⡀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⡠⠀⡇⣿
⣿⡀⠘⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⠈⠑⡦⢄⣀⠀⠀⠐⠒⠁⢸⠀⠀⠠⠒⠄⠀⠀⠀⠀⠀⢀⠇⠀⣀⡀⠀⠀⢀⢾⡆⠀⠈⡀⠎⣸⣿
⣿⣿⣄⡈⠢⠀⠀⠀⠀⠘⣶⣄⡀⠀⠀⡇⠀⠀⠈⠉⠒⠢⡤⣀⡀⠀⠀⠀⠀⠀⠐⠦⠤⠒⠁⠀⠀⠀⠀⣀⢴⠁⠀⢷⠀⠀⠀⢰⣿⣿
⣿⣿⣿⣿⣇⠂⠀⠀⠀⠀⠈⢂⠀⠈⠹⡧⣀⠀⠀⠀⠀⠀⡇⠀⠀⠉⠉⠉⢱⠒⠒⠒⠒⢖⠒⠒⠂⠙⠏⠀⠘⡀⠀⢸⠀⠀⠀⣿⣿⣿
⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠑⠄⠰⠀⠀⠁⠐⠲⣤⣴⣄⡀⠀⠀⠀⠀⢸⠀⠀⠀⠀⢸⠀⠀⠀⠀⢠⠀⣠⣷⣶⣿⠀⠀⢰⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠁⢀⠀⠀⠀⠀⠀⡙⠋⠙⠓⠲⢤⣤⣷⣤⣤⣤⣤⣾⣦⣤⣤⣶⣿⣿⣿⣿⡟⢹⠀⠀⢸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠑⠀⢄⠀⡰⠁⠀⠀⠀⠀⠀⠈⠉⠁⠈⠉⠻⠋⠉⠛⢛⠉⠉⢹⠁⢀⢇⠎⠀⠀⢸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠈⠢⢄⡉⠂⠄⡀⠀⠈⠒⠢⠄⠀⢀⣀⣀⣰⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⢀⣎⠀⠼⠊⠀⠀⠀⠘⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡀⠉⠢⢄⡈⠑⠢⢄⡀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⢀⠀⠀⠀⠀⠀⢻⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⡈⠑⠢⢄⡀⠈⠑⠒⠤⠄⣀⣀⠀⠉⠉⠉⠉⠀⠀⠀⣀⡀⠤⠂⠁⠀⢀⠆⠀⠀⢸⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠁⠉⠒⠂⠤⠤⣀⣀⣉⡉⠉⠉⠉⠉⢀⣀⣀⡠⠤⠒⠈⠀⠀⠀⠀⣸⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣤⣤⣤⣤⣀⣀⣤⣤⣤⣶⣾⣿⣿⣿⣿⣿
'''

 
 case _:
 return 0
 return 0

def conv():
 file = input("Enter the path to you image you want converted to a TIMG file:\n")
 out = input("Enter the path youd like to write the TIMG to:\n")
 img = Image.open(file)
 w,h = img.size
 write = [b'\x54',b'\x49',b'\x4D',b'\x47',b'\x00',b'\x01',b'\x00',b'\x02']
 for x in w.to_bytes(4):
 write.append(x.to_bytes(1))
 for y in h.to_bytes(4):
 write.append(y.to_bytes(1))
 write.append(b'\x52')
 write.append(b'\x55')
 write.append(b'\x42')
 write.append(b'\x59')

 for i in range(h):
 dat = [b'\x44',b'\x41',b'\x54',b'\x52']
 for j in range(w):
 dat.append(img.getpixel([j,i])[0].to_bytes(1))
 dat.append(getCheck(dat[4:]))
 for wa in dat:
 write.append(wa)

 for i in range(h): 
 dat = [b'\x44',b'\x41',b'\x54',b'\x47']
 for j in range(w):
 dat.append(img.getpixel([j,i])[1].to_bytes(1))
 dat.append(getCheck(dat[4:]))
 for wa in dat:
 write.append(wa)

 for i in range(h): 
 dat = [b'\x44',b'\x41',b'\x54',b'\x42' ]
 for j in range(w):
 print(img.getpixel([j,i])[2].to_bytes(1))
 dat.append(img.getpixel([j,i])[2].to_bytes(1)) 
 print(dat) 
 dat.append(getCheck(dat[4:]))
 for wa in dat:
 write.append(wa)

 write.append(b'\x44')
 write.append(b'\x41')
 write.append(b'\x54')
 write.append(b'\x45')

 with open(out,"ab") as f:
 for b in write:
 f.write(b)

 return 0 

def getCheck(datr):
 dat = ''
 for w in datr:
 dat+=chr(int.from_bytes(w))
 print(datr )
 print(dat.encode())
 return int.to_bytes(int(crc8.crc8(dat.encode()).hexdigest(),base=16),1)

if __name__=='__main__':
 main()
```



```
from PIL import Image
import numpy as np
import struct
import crc8

def timg_to_jpg(timg_file, output_file):
 try:
 with open(timg_file, "rb") as f:
 data = f.read()

 # Check TIMG header
 if data[:4] != b'TIMG':
 raise ValueError("Invalid TIMG file")

 # Extract width and height
 width = int.from_bytes(data[8:12], "big")
 height = int.from_bytes(data[12:16], "big")

 # Verify header consistency
 if data[16:20] != b'RUBY':
 raise ValueError("Invalid RUBY header")

 # Initialize RGB arrays
 r_channel = np.zeros((height, width), dtype=np.uint8)
 g_channel = np.zeros((height, width), dtype=np.uint8)
 b_channel = np.zeros((height, width), dtype=np.uint8)

 # Parse data sections
 offset = 20 # Start after header
 for color, channel in zip([b'DATR', b'DATG', b'DATB'], [r_channel, g_channel, b_channel]):
 for i in range(height):
 if data[offset:offset+4] != color:
 raise ValueError(f"Missing {color.decode()} section")
 offset += 4 # Skip section header
 for j in range(width):
 channel[i, j] = data[offset]
 offset += 1

 # Skip checksum (1 byte)
 offset += 1

 # Verify footer
 if data[offset:offset+4] != b'DATE':
 raise ValueError("Invalid footer")

 # Combine channels into an image
 rgb_array = np.stack((r_channel, g_channel, b_channel), axis=2)
 img = Image.fromarray(rgb_array, "RGB")

 # Save as JPG
 img.save(output_file, "JPEG")
 print(f"Successfully converted TIMG to {output_file}")

 except Exception as e:
 print(f"Error: {e}")

# Example usage
timg_to_jpg("flag.timg", "output.jpg")
```



```
airodump-ng -r dump-05.cap
```



```
aircrack-ng -w /usr/share/wordlists/rockyou.txt -b D8:3A:DD:07:AA:5A dump-05.cap
```
