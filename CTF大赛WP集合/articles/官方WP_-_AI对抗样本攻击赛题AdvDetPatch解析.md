# 官方WP | AI对抗样本攻击赛题AdvDetPatch解析

> 原文: https://www.ctfiot.com/118789.html
> ID: 118789

编者荐语：

本文分享了AI对抗样本攻击赛题AdvDetPatch的设计思路与解析，以及两个成功解决该题的队伍的方法和技巧。

“AdvDetPatch”赛题已部署在伽玛实验场，欢迎前去挑战。

AdvDetPatch解析

作者：中科大网络空间安全学院
AdvDetPatch题目要求选手针对目标检测模型进行对抗攻击，要求模型无法正确地检测出给定图片中的所有物体，并且对抗性补丁的面积不能超过图像面积的5%。

题目考察的是较为基础的针对深度学习任务的对抗性攻击知识。设计攻击方法的关键是设计损失函数与对抗性补丁模板。为了简化流程，题目仅约束补丁面积大小，对补丁的数量不作要求。题目中给出了补丁设计的相关提示即需要考虑补丁的形状、位置、纹理等因素。

首先是用于攻击的损失函数设计。从推理代码中可知预测的输出包含了图像中所有检测框的左上角和左下角的坐标、为物体的概率以及类别的概率向量。为了使得模型检测不到图片中的物体，损失函数可以设计为最小化所有检测框的判断为物体的概率。损失函数的设计需要对预测结果的组成有基本的了解。

损失函数示例如下：

其次考虑补丁的位置和形状。对于扰动位置， 与分类模型不同，当扰动处处在图片中的物体区域时对此目标的检测影响最大，而在背景区域时影响很小。因此，扰动可以放置在可能的检测框中心。对于形状，需要保证补丁面积大小不超过全图的5%，因此无法直接添加全局扰动。题目不对补丁数量做要求，因此可选项很多，例如方形、圆形、随机点、网格、星形等等，只要在给定扰动像素数量内尽可能的覆盖物体都可以。

以创建网格形mask为例（即只包含横线和竖线）：

最后可以使用常见的梯度攻击方法如PGD优化补丁的纹理，直到目标检测模型检测不到物体为止。一次循环中的攻击示例如下：

如果熟悉常见的攻击算法和图像处理能够比较快速地攻击成功，否则补丁的创建和损失的设计都可能会花费较多的时间。补丁的限制只有面积大小，因此补丁的形式非常多，只要能够最大限度地覆盖物体，都能较快的生成扰动。因为只有一张图片，因此肉眼选择补丁的位置并且手工设计mask也能快速确定mask。

一血队伍解法

作者：sfc9982@Maple_Leaves

1. 观察判题目录

ctf@engine-1:/home/adv$ ll
total 91476
drwxr-xr-x 1 root root 4096 May 29 07:49 ./
drwxr-xr-x 1 root root 4096 May 27 14:39 ../
drwxr-xr-x 1 ctf ctf 4096 May 27 14:38 adv_images/
-rwx------ 1 root root 42 May 29 07:49 flag*
-rwxr-xr-x 1 root root 5801 May 27 14:30 fool_me.py*
drwxr-xr-x 2 root root 4096 May 27 14:38 images/
drwxr-xr-x 2 root root 4096 May 27 14:38 models/
drwxr-xr-x 2 root root 4096 May 27 14:38 utils/
-rw-r--r-- 1 root root 93622629 May 24 16:04 yolov5l.pt

可以发现如下几点特性：

为了防止选手直接访问 flag 文件，去除了除 root 外的所有权限

由于(1)，进而使用 sudo 运行判题脚本 fool_me.py 以读取 flag 文件

由于(2)，只给选手开放了对于绝对路径命令 sudo python3 /home/adv/fool_me.py 的权限

判题脚本运行时会读取：图像资源文件、库文件、权重文件

除 flag 外都是我们现在的用户可读的，所以可以在任意目录下复刻一个没有 flag 的判题环境

这里针对(3)尝试滥用 sudo 命令，但是权限设计得很好，尝试了alias和链接，但未能成功读取。

转而利用(4)(5)，题目最终的要求是使用一个较低的置信度阈值，对处理过的图片进行目标检测（这里是红色路标）。如果无法识别出任何目标，则吐出 flag.

看了下图片处理部分，由于采用了掩码+处理后图片的方式，难以绕过。

注意到，读取模型使用了 weights='yolov5l.pt' （相对目录） 读取 flag 使用了 fd = open("/home/adv/flag") （绝对目录） 再加上我们对判题目录中所有除flag文件均有读权限，我们可以在自己的目录下创造一个“自主可控”的判题环境。

在这个目录中，我们只需要诱导脚本加载一个空或不能够提供足够置信度的权重文件即可。

这里我们解出 flag 时使用的是 YOLO 官方项目 (https://github.com/ultralytics/yolov5/releases) 发布的 yolov5n.pt 文件 (SHA-256: 4F180CF23BA0717ADA0BADD6C685026D73D48F184D00FC159C2641284B2AC0A3)。

图片稍微的处理了一下。

复制运行环境：

回显：

编者有话说
一血是在题目上线后1小时36分钟后解出的，此后经过沟通，发现是其发现调用的模型文件yolov5l.pt是通过相对路径加载的，所以就另外找一个模型替换掉原题目判定模型，从而轻松通过校验。

在一开始听到这个做法小编是十分惊喜的，这不就是“偷梁换柱”，这很有网络安全技巧那范儿。

其实在当天开赛不久后，小编就收到一个选手的反馈报错：

经过排查后是该选手在/home/ctf运行了命令，而yolov5l.pt是读取当前目录的，自然读取不到，这时候小编已经留意到相对路径这点，但一时没往深去想替换掉模型文件。

二血队伍解法

作者：机器猫@哈工大Lilac
这是一道对抗样本题目。题目用yolov5模型做目标检测，我们需要构造一个与stop.png很接近的input，让模型认为里面没有目标。

题目的模型是白盒，因此我们可以采用一个经典方法：冻结神经网络的参数，而去对input图片进行梯度下降，迭代到模型认为input里面不包含目标为止。

这套算法可以参考我2021年写的一篇文章：【CTF 中如何欺骗 AI】https://www.anquanke.com/post/id/251125

第一个问题是如何选择loss函数。yolov5首先产生25200个候选bbox，经过NMS流程之后选出最终结果。最理想的情况是直接使得最终预测结果为空集，但无法实现，因为不可导。

我们退而求其次，考虑尽量使得那25200个候选bbox的置信度变低。我们简单地选择loss为这25200个 bbox 的置信度之和。对原始图片，这个值大约是 71.7。

第二个问题是，题目只允许修改20480个像素，因此我们必须选择那些“更容易影响模型预测结果”的像素。我们的解决方式是：首先用原图跑一遍模型，进行反向传播，保留图像中梯度绝对值最大的20480个像素，认为这些像素对答案影响最大，以后就只修改这些像素。

细节上，我们使用了Adam优化器以期快速收敛，最终在第14轮迭代时成功欺骗了神经网络。另外，我们最后修改完的input是一个3×640×640浮点数矩阵，它每个元素不一定在 [0, 1]之间，我们要把它限制在[0, 1]范围内，再乘以255转uint8。

训练过程：

最终提交的图像：

掩膜：

代码：

其他挑战
2019年，第十二届全国大学生信息安全竞赛初赛，有一道对抗深度学习的题目Deep_Learning，当时是利用whitebox attack中的deepool attack来生成恶意样本使CV系统作出错误的分类决策。

题目里提供了一个样例图片（一朵花），要求选手上传一个图片，要求上传图片与样本平均误差小于0.8，且要被识别为wing（机翼），就得到flag。而因为题目要求的随机阈值很低，因此不可以使用FGSM等较为老的算法生成恶意样本，必须使用类似扰动值较小的deepool生成恶意样本才能过掉阈值检查，将生成好的样本提交就可以得到flag。（该题当年0解）

Deep_Learning这题也部署在伽玛实验场，欢迎挑战：


```
def attack_loss(preds):
    """
    Computes the attack loss for object detection.

    Args:
        preds (List[Tensor[N, :]]): List of detection results.

    Returns:
        Tuple[float, int]: Tuple containing the object probability loss and the number of detected objects.
    """
    conf_thres = 0.25
    obj_prob_loss = 0
    objects_num = 0
    for i, pred in enumerate(preds):
        conf_mask = (pred[:, 4] >= conf_thres).squeeze()
        pred = pred[conf_mask]
        obj_prob_loss += (pred[:, 4].sum() / conf_mask.sum())
        objects_num = conf_mask.sum()
    return obj_prob_loss, objects_num
```



```
def create_patch_mask(detections=None, width=1, line_distance=50, shape=(640,640)):
    """
    Creates a mask over the image where detections are located, with lines drawn at regular intervals.

    Args:
        detections (List[[N, 4]]): List of detections returned by non-maximum suppression, (int).
        width (int): Width of the lines.
        line_distance (int): Distance between the lines.
        shape (Tuple[int, int]): Shape of the output mask.

    Returns:
        Tensor containing the binary mask of the patches.
    """
    mask = torch.zeros(*shape, 3)
    for _, (x1, y1, x2, y2) in enumerate(detections):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        for i in range(1, 100):
            if mask.sum() > 20480*3: break
            if y1 + i*line_distance > y2: break
            tmp_mask = torch.zeros(*shape, 3)
            tmp_mask[np.clip(y1+i*line_distance, 0, shape[1]):np.clip(y1+i*line_distance+width, 0, shape[1]), x1:x2, :]=1
            mask = mask + tmp_mask
        for i in range(1,100):
            if mask.sum() > 20480*3: break
            if x1 + i*line_distance > x2: break
            tmp_mask = torch.zeros(*shape, 3)
            tmp_mask[y1:y2, np.clip(x1+i*line_distance, 0, shape[1]):np.clip(x1+i*line_distance+width, 0, shape[1]), :]=1
            mask = mask + tmp_mask
            
    mask = np.clip(mask,0,1)
    return mask
```



```
# initialize the patch
patch = torch.randn(input_tensor.shape).float() + 127/255  #大初始值加速收敛
patch = patch.to(input_tensor.device)
patch.requires_grad = True
# apply the patch to the image
patch_img = input_tensor * (1-mask) + patch * mask
patch_img = torch.clamp(patch_img,0,1)
patch_img = patch_img.to(device)
# attack
preds = model(patch_img, augment=opt.augment, visualize=opt.visualize)
attack_loss, obj_num = attack_loss(preds)
attack_loss.backward()
patch.data = patch - eps * patch.grad.sign()
```



```
ctf@engine-1:/home/adv$ ll
total 91476
drwxr-xr-x 1 root root 4096 May 29 07:49 ./
drwxr-xr-x 1 root root 4096 May 27 14:39 ../
drwxr-xr-x 1 ctf ctf 4096 May 27 14:38 adv_images/
-rwx------ 1 root root 42 May 29 07:49 flag*
-rwxr-xr-x 1 root root 5801 May 27 14:30 fool_me.py*
drwxr-xr-x 2 root root 4096 May 27 14:38 images/
drwxr-xr-x 2 root root 4096 May 27 14:38 models/
drwxr-xr-x 2 root root 4096 May 27 14:38 utils/
-rw-r--r-- 1 root root 93622629 May 24 16:04 yolov5l.pt
```



```
ctf@engine-1:~$ ln -s /home/adv/adv_images/ . 
ctf@engine-1:~$ ls
README.md adv_images yolov5l.pt
ctf@engine-1:~$ ln -s /home/adv/ .
adv_images/ flag fool_me.py images/ models/ utils/ yolov5l.pt
ctf@engine-1:~$ ln -s /home/adv/images/ .
ctf@engine-1:~$ ln -s /home/adv/models/ .
ctf@engine-1:~$ ln -s /home/adv/utils/ .
ctf@engine-1:~$ ln -s /home/adv/f .
flag fool_me.py 
ctf@engine-1:~$ ln -s /home/adv/flag .
ctf@engine-1:~$ sudo python3 /home/adv/fool_me.py
```



```
OpenBLAS WARNING - could not determine the L2 cache size on this system, assuming 256k
OpenBLAS WARNING - could not determine the L2 cache size on this system, assuming 256k
OpenBLAS WARNING - could not determine the L2 cache size on this system, assuming 256k
------------------Initializing detector-------------------
Fusing layers...
Model Summary: 213 layers, 1867405 parameters, 0 gradients
libpng warning: iCCP: known incorrect sRGB profile
libpng warning: iCCP: profile 'ICC Profile': 'RGB ': RGB color space not permitted on grayscale PNG
libpng warning: iCCP: known incorrect sRGB profile
libpng warning: iCCP: cHRM chunk does not match sRGB
---------------------Start detecting----------------------
[*]I see nothing!
[*]Give you the flag
flag{1998c094-64e4-4b06-99bb-d030a35660f3}
```



```
FileNotFoundError: [Errno 2] No such file or directory: 'yolov5l.pt'
```



```
import argparse
import cv2
import torch
import numpy as np
from models.common import DetectMultiBackend
from utils.datasets import LoadImages
from utils.general import non_max_suppression, check_patchsize
from utils.torch_utils import select_device, time_sync
import matplotlib.pyplot as plt
import matplotlib
import pickle
from PIL import Image

matplotlib.use('TkAgg')

# @torch.no_grad()
def run(weights='yolov5l.pt',  
        source='adv_images/stop.png',  # adversarial image path
        clean_path='images/stop.png',
        mask_path='adv_images/mask.png',
        imgsz=640,  # inference size (pixels)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='cpu',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        ):
    source = str(source)
    if not source.endswith(clean_path.split(".")[-1]):
        raise ValueError("File must have same format as clean image!")

    # Load model
    device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn)

    model.requires_grad_(False)

    stride, pt, jit = model.stride, model.pt, model.jit

    # Half
    half &= pt and device.type != 'cpu'  # half precision only supported by PyTorch on CUDA
    if pt:
        model.model.half() if half else model.model.float()

    clean_img = cv2.imread(clean_path)
    clean_img = cv2.cvtColor(clean_img, cv2.COLOR_BGR2RGB)
    clean_img = torch.from_numpy(clean_img).to(device)
    clean_img = clean_img.float() / 255
    clean_img = clean_img[None].permute(0,3,1,2)

    dataset = LoadImages(clean_path, img_size=imgsz, stride=stride, auto=pt and not jit)

    # Run inference

    for path, im, im0s, vid_cap, s in dataset:
        im = torch.from_numpy(im).to(device)
        im = im.half() if half else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0

        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim

        im.requires_grad_(True)

        assert im.shape == clean_img.shape, "Image shapes must match."
        # im = im * mask + clean_img * (1 - mask) # eval patch
        # Inference
        # print('---------------------Start detecting----------------------')

        # 首次运行，选择梯度绝对值最大的 20480 个像素

        # pred = model(im, augment=augment, visualize=visualize)
        # conf = pred[0, :, 4].sum()
        # print('box置信度总和', conf.detach())

        # conf.backward()
        # # print(im.grad)

        # t = [
        #     (im.grad[0, :, x, y].abs().sum(), x, y) 
        #         for x in range(640) 
        #             for y in range(640)]
        # t.sort(reverse=True)

        # # print(t)

        # pixels = [x[1:] for x in t[:20480]]
        # pickle.dump(pixels, open('pixels.pkl', 'wb'))
        pixels = pickle.load(open('pixels.pkl', 'rb'))
        
        mask = torch.zeros_like(im)
        for x, y in pixels:
            mask[0, :, x, y] = 1
        

        img = mask.detach().permute(0,2,3,1).numpy()[0] * 255
        img = img.round().astype(np.uint8)
        # print(img)
        Image.fromarray(img).save(f'out/mask.png')

        opti = torch.optim.Adam([im], lr=.1)

        for epoch in range(100):
            pred = model(im, augment=augment, visualize=visualize)
            conf = pred[0, :, 4].sum()

            
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

            pr = pred[0].cpu()
            
            print(f'epoch #{epoch}','box置信度总和', conf.detach(), '预测 box 个数', len(pr))

            conf.backward()
            opti.step()

            
            im.data = torch.clamp(im.data, min=0.0, max=1.0)
            im.data = im * mask + clean_img * (1 - mask)
            im.grad.zero_()

            # print(im.detach())
            pickle.dump(im.detach(), open(f'out/im{epoch}.pkl', 'wb'))
            
            img = im.detach().permute(0,2,3,1).numpy()[0] * 255
            img = img.round().astype(np.uint8)
            # print(img)
            Image.fromarray(img).save(f'out/{epoch}.png')

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='yolov5l.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default='adv_images/stop.png', help='file/dir/URL/glob')
    parser.add_argument('--clean_path', type=str, default='images/stop.png', help='clean_img')
    parser.add_argument('--mask_path', type=str, default='adv_images/mask.png', help='mask_img')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='cpu', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    # print_args(FILE.stem, opt)
    return opt

def main(opt):
    run(**vars(opt))
    

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/2-1685944462.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/8-1685944462.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1685944462.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/1-1685944463.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/9-1685944464.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/3-1685944464.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/0-1685944465.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/6-1685944466.gif)