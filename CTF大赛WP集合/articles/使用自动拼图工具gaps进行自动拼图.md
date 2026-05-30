# 使用自动拼图工具gaps进行自动拼图

> 原文: https://www.ctfiot.com/162924.html
> ID: 162924

拼图在手动的情况下还是有很多限制，以这一题为例，共计600张图片。

图片名称没有任何规律。如果手动拼图的话，总的尝试次数会非常大，而且非常耗时，所以需要依赖自动拼图的工具。

图片拼接

首先需要将图片全部拼接到一张图片中，并且获取每张图片的尺寸，每张图的尺寸为40×40

因为共计600张图片，所以猜测总图片应该是20×30的数量排列

安装montage

montage拼接图片

常规命令只需要用到tile和geometry两个参数就可以。

tile是拼成的大小，geometry为图片之间的缝隙大小。

拼接完的效果

拼图调整

然后安装gaps自动拼图工具。

首先安装poetry：

可以看出图片的尺寸应该是30×20，调整后再运行一次

图片还是有部分没有修改完成，修改gaps的参数，增加迭代


```
apt-get install -y graphicsmagick-imagemagick-compat
```



```
montage
GraphicsMagick 1.3.28 2018-01-20 Q16 http://www.GraphicsMagick.org/
Copyright (C) 2002-2018 GraphicsMagick Group.
Additional copyrights and licenses apply to this software.
See http://www.GraphicsMagick.org/www/Copyright.html for details.
Usage: montage montage [options ...] file [ [options ...] file ...]

Where options include: 
 -adjoin join images into a single multi-image file
 -affine matrix affine transform matrix
 -authenticate value decrypt image with this password
 -background color background color
 -blue-primary point chomaticity blue primary point
 -blur factor apply a filter to blur the image
 -bordercolor color border color
 -borderwidth geometry
 border width
 -colors value preferred number of colors in the image
 -colorspace type alternate image colorsapce
 -comment string annotate image with comment
 -compose operator composite operator
 -compress type image compression type
 -crop geometry preferred size and location of the cropped image
 -debug events display copious debugging information
 -define values Coder/decoder specific options
 -density geometry horizontal and vertical density of the image
 -depth value image depth
 -display server query font from this X server
 -dispose method Undefined, None, Background, Previous
 -dither apply Floyd/Steinberg error diffusion to image
 -draw string annotate the image with a graphic primitive
 -encoding type text encoding type
 -endian type multibyte word order (LSB, MSB, or Native)
 -fill color color to use when filling a graphic primitive
 -filter type use this filter when resizing an image
 -flip flip image in the vertical direction
 -flop flop image in the horizontal direction
 -font name font to use when annotating with text
 -format string output formatted image characteristics
 -frame geometry surround image with an ornamental border
 -gamma value level of gamma correction
 -geometry geometry preferred tile and border sizes
 -gravity direction which direction to gravitate towards
 -green-primary point chomaticity green primary point
 -help print program options
 -interlace type None, Line, Plane, or Partition
 -label name assign a label to an image
 -limit type value Disk, File, Map, Memory, Pixels, Width, Height or
 Threads resource limit
 -log format format of debugging information
 -matte store matte channel if the image has one
 -mattecolor color color to be used with the -frame option
 -mode type Frame, Unframe, or Concatenate
 -monitor show progress indication
 -monochrome transform image to black and white
 -noop do not apply options to image
 +page reset current page offsets to default
 -page geometry size and location of an image canvas
 -pointsize value font point size
 -quality value JPEG/MIFF/PNG compression level
 -red-primary point chomaticity red primary point
 +repage reset current page offsets to default
 -repage geometry adjust current page offsets by geometry
 -resize geometry resize the image
 -rotate degrees apply Paeth rotation to the image
 -sampling-factor HxV[,...]
 horizontal and vertical sampling factors
 -scenes range image scene range
 -set attribute value set image attribute
 +set attribute unset image attribute
 -shadow add a shadow beneath a tile to simulate depth
 -sharpen geometry sharpen the image
 -size geometry width and height of image
 -strip strip all profiles and text attributes from image
 -stroke color color to use when stroking a graphic primitive
 -strokewidth value stroke (line) width
 -texture filename name of texture to tile onto the image background
 -thumbnail geometry resize the image (optimized for thumbnails)
 -tile geometry number of tiles per row and column
 -title string thumbnail title
 -transform affine transform image
 -transparent color make this color transparent within the image
 -treedepth value color tree depth
 -trim trim image edges
 -type type image type
 -verbose print detailed information about the image
 -version print version information
 -virtual-pixel method
 Constant, Edge, Mirror, or Tile
 -white-point point chomaticity white point

In addition to those listed above, you can specify these standard X
resources as command line options: -background, -bordercolor,
-borderwidth, -font, -mattecolor, or -title

By default, the image format of `file' is determined by its magic
number. To specify a particular image format, precede the filename
with an image format name and a colon (i.e. ps:image) or specify the
image type as the filename suffix (i.e. image.ps). Specify 'file' as
'-' for standard input or output.
montage montage: Improper arguments supplied, please see manual.
```



```
montage ./files/*.png -tile 20X30 -geometry +0+0 flag.png
```



```
curl -sSL https://install.python-poetry.org | python3 -
```



```
sudo apt-get install python-tk
git clone https://github.com/nemanja-m/gaps
cd gaps
pip install . -i https://pypi.tuna.tsinghua.edu.cn/simple
```



```
Usage: gaps run [OPTIONS] PUZZLE SOLUTION

 Run puzzle solver.

 PUZZLE is the input puzzle image with square pieces.
 SOLUTION is the output image file for solved puzzle.

 Examples:

 $ gaps run puzzle.jpg solution.jpg --size=32 --generations=100
 --population=1000

Options:
 -s, --size INTEGER Size of single square puzzle piece in pixels.
 Autodetected if not specified.
 -g, --generations INTEGER The number of generations for genetic algorithm.
 [default: 20]
 -p, --population INTEGER The size of the initial population for genetic
 algorithm. [default: 200]
 -d, --debug If enabled, shows the best individual after each
 generation.
 -h, --help Show this message and exit.
```



```
gaps run ./flag.png resolve.png --generations=20 --population=200 --size=40
```



```
montage ./files/*.png -tile 30X20 -geometry +0+0 flag.png  
gaps run ./flag.png resolve.png --generations=20 --population=200 --size=40
```



```
gaps run ./flag.png resolve.png --generations=400 --population=400 --size=40
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/2-1708415139.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/7-1708415140.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/6-1708415141.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/10-1708415146.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/3-1708415154.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/9-1708415159.png)