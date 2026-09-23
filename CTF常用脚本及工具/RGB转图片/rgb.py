from PIL import Image

x = y = 200 # 需要手动将()去掉
img = Image.new("RGB",(x,y))
file = open('./qr.txt','r')

for width in range(0,x):
    for height in range(0,y):
        line = file.readline()
        rgb = line.split(',')
        img.putpixel((width,height),(int(rgb[0]),int(rgb[1]),int(rgb[2])))
img.save('flag.jpg')