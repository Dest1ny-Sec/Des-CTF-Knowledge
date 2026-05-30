# flare-on之anode解题技巧

> 原文: https://www.ctfiot.com/80126.html
> ID: 80126

类型判断 

Anode是一道类型非常经典的逆向题，请求用户输入flag，判断是否正确：

从IDA给出的信息来判断，这题是由NodeJS语言进行编写，然后NEXE打包成可执行文件：

 源码获取 

NEXE会将JS源码直接打包到EXE中，不经过任何加密或者压缩，所以很容易使用十六进制编辑工具将源码提取出来，搜索特征字符串“Enter flag”,就能快速定位到源码位置：

JS代码如下所示，分析代码可知，程序接受用户的输入flag，经过了一个非常长的switch运算最后和加密后的flag进行比较，解题必须将加密的flag逆推回去。

readline.question(`Enter flag: `, flag => {
  readline.close();
  if (flag.length !== 44) {
    console.log("Try again.");
    process.exit(0);
  }
  var b = [];
  for (var i = 0; i < flag.length; i++) {
    b.push(flag.charCodeAt(i));
  }

  // something strange is happening...
  if (1n) {
    console.log("uh-oh, math is too correct...");
    process.exit(0);
  }

  var state = 1337;
  while (true) {
    state ^= Math.floor(Math.random() * (2**30));
    switch (state) {
      case 306211:
        if (Math.random() < 0.5) {
          b[30] -= b[34] + b[23] + b[5] + b[37] + b[33] + b[12] + Math.floor(Math.random() * 256);
          b[30] &= 0xFF;
        } else {
          b[26] -= b[24] + b[41] + b[13] + b[43] + b[6] + b[30] + 225;
          b[26] &= 0xFF;
        }
        state = 868071080;
        continue;
      case 311489:
        if (Math.random() < 0.5) {
          b[10] -= b[32] + b[1] + b[20] + b[30] + b[23] + b[9] + 115;
          b[10] &= 0xFF;
        } else {
          b[7] ^= (b[18] + b[14] + b[11] + b[25] + b[31] + b[21] + 19) & 0xFF;
        }
        state = 22167546;
        continue;
      case 755154:
        if (93909087n) {
          b[4] -= b[42] + b[6] + b[26] + b[39] + b[35] + b[16] + 80;
          b[4] &= 0xFF;
        } else {
          b[16] += b[36] + b[2] + b[29] + b[10] + b[12] + b[18] + 202;
          b[16] &= 0xFF;
        }
        state = 857247560;
        continue;
     
      case 1045388446:
        if (Math.random() < 0.5) {
          b[33] += b[40] + b[17] + b[43] + b[21] + b[36] + b[23] + 76;
          b[33] &= 0xFF;
        } else {
          b[20] -= b[37] + b[30] + b[12] + b[15] + b[6] + b[7] + 88;
          b[20] &= 0xFF;
        }
        state = 204284567;
        continue;
        //......省略，代码非常长
        //......省略，代码非常长
        //......省略，代码非常长
      case 1071767211:
        if (Math.random() < 0.5) {
          b[30] ^= (b[42] + b[9] + b[2] + b[36] + b[12] + b[16] + 241) & 0xFF;
        } else {
          b[20] ^= (b[41] + b[2] + b[40] + b[21] + b[36] + b[17] + 37) & 0xFF;
        }
        state = 109621765;
        continue;
      default:
        console.log("uh-oh, math.random() is too random...");
        process.exit(0);
    }
    break;
  }

  var target = [106, 196, 106, 178, 174, 102, 31, 91, 66, 255, 86, 196, 74, 139, 219, 166, 106, 4, 211, 68, 227, 72, 156, 38, 239, 153, 223, 225, 73, 171, 51, 4, 234, 50, 207, 82, 18, 111, 180, 212, 81, 189, 73, 76];
  if (b.every((x,i) => x === target[i])) {
    console.log('Congrats!');
  } else {
    console.log('Try again.');
  }
});

 坑点 

这题有埋坑的地方，题目源码很明显给了提示，正常情况下，if块将会被执行，但是从实际运行结果来看，这个字符串并没有输出，程序也没有退出，很明显，这题修改了V8引擎。

不仅bigint类型的真假值判断被修改了，随机数生成也被修改了，因为程序每次都会走到相同的switch分支：

正常的解题思路是分析V8源码修改的地方，使用bindiff和对比源码的方法去分析，不过由于时间有限，我决定另辟蹊径，通过黑盒的方法去把这些关键信息收集到，即使我对它如何修改V8引擎细节一无所知。

 信息收集 

通过修改exe中js源码的方法，将随机数值以及每个if判断数值为真或为假直接打印出来，通过收集到的信息修复JS代码，使得它在正常的JS引擎也能运行起来。如何修改呢？方法非常简单，只需要对ReadFile下断点，在它把JS数据读入内存中后进行修改：

直接修改js源码，插入两段代码，一个获取随机值：

一个获取if判断的值，为真还是为假：

 修复JS 

修复

知道以上信息就可以着手修复JS代码了，将if的值直接替换成true或者false:

import subprocess
import right
import re
import right_judge
all_case_num=[]
def fix_js(): 
 count=1
 n_c=0
 fix_flag=False
 out_line=''
 with open('test_no_input.js','rt') as fd:
  line=fd.readline()
  while line:
   if 'case' in line:
    fix_flag=True
   if fix_flag and 'if' in line  and '>' not in line and '<' not in line:
    p = re.compile(r'[(](.*?)[)]', re.S)
    all_case_num.append(re.findall(p, line)[0])
    if right_judge.all_case_judge[n_c]:

     line='      if (true) {n'
    else:
     line='      if (false) {n'
    fix_flag=False
    n_c+=1
   out_line+=line
   line=fd.readline()
 print(out_line)
 with open('fixed_test.js','wt+') as fdo:
  fdo.write(out_line)

  
if __name__ == '__main__':

 fix_js()

得到JS内容如下：

化简

为了进一步提高可读性，编写脚本进行进一步化简，将switch结构修改成顺序执行，并将随机值的运算结果进行求解。

import subprocess
import right
import re
import flare_random
import math
all_case_num=[]
end_num=185078700
random_magic_str='getrand(pos++)'
def fix_js(): 
 random_pos=0
 rcn=right.right_case
 rand_num=flare_random.randnum
 all_const_num=''

 out_line=[]
 with open('fixed_test.js','rt') as fd:
  data=fd.read()
 for case_num in rcn:
  random_pos+=1
  if case_num==end_num:
   break
  case_pos=data.find(str(case_num), 0)
  cond_block_start=data.find('(',case_pos)
  cond_block_end=data.find('{',case_pos)
  cond_block=data[cond_block_start:cond_block_end]
  if_true_block_start=data.find('{',case_pos)
  if_true_block_end=data.find('}', case_pos)
  if_true_block=data[if_true_block_start+1:if_true_block_end]
  if_false_block_start=data.find('{', if_true_block_end)
  if_false_block_end=data.find('}', if_true_block_end+1)
  cond_bool=None
  if random_magic_str in cond_block:
   if_rand_num=rand_num[random_pos]
   random_pos+=1
   sol_cond=cond_block.replace(random_magic_str,str(if_rand_num))
   cond_bool=eval(sol_cond)
  if 'true'  in cond_block:
   cond_bool=True
  if 'false'  in cond_block:
   cond_bool=False
  assert cond_bool!=None
  if_false_block=data[if_false_block_start+1:if_false_block_end]
  assert if_true_block.count(random_magic_str)<=1
  assert if_false_block.count(random_magic_str)<=1
  if cond_bool:
   exec_block=if_true_block
  else:
   exec_block=if_false_block
  #print(exec_block)
  line=exec_block
  if 'Math.floor(' in exec_block:
   m_start=exec_block.find('Math.floor',0)
   m_end=exec_block.find(')',m_start)
   m_end=exec_block.find(')',m_end+1)
   math_semt=exec_block[m_start:m_end+1]
   #print(math_semt)
   assert random_magic_str in math_semt
   math_semt_rand_num=rand_num[random_pos]
   sol_semt=math_semt.replace(random_magic_str,str(math_semt_rand_num)).replace('Math','math')
   #print(eval(sol_semt))
   random_pos+=1
   line=exec_block.replace(math_semt,str(eval(sol_semt)))
  if '&=' in line:
   line_list=line.split('n')
   formatline=line_list[1].replace(' ','')
  else:
   line_list=line.split('n')
   formatline=line_list[1].replace(' ','').replace('&0xFF','').replace('(','').replace(')','')
  #formatline)
  formatline_list=formatline.split('=')
  left_v=formatline_list[0][0:-1]
  op=formatline[len(left_v):len(left_v)+2]
  right_v=formatline_list[1].strip(';')
  add_nums=right_v.split('+')
  assert len(add_nums)==7
  const_num=add_nums[6]

  #获取所有下标，并且排序
  p = re.compile(r'[[](.*?)[]]', re.S)
  all_add_num=[]
  for i in range(6):
   all_add_num.append(int(re.findall(p, add_nums[i])[0]))
  all_add_num.sort()
  #print(all_add_num)
  fix_line=left_v+op
  for i in all_add_num:
   fix_line+='b[%d]+'%i
  fix_line+=const_num
  fix_line+='n'

  out_line.append(fix_line)
  
 print(''.join(out_line))
if __name__ == '__main__':

 fix_js()

最后得到结果如下所示：

 求解 

观察这个得到化简的结果，只有三种运算，分别是：+= 、^=、,-=  ,为了可以将密文逆推回去，直接将 -= 替换成 +=  ,将 += 替换成 -= ,运算顺序进行反转就可以解密flag：Flag为：n0t_ju5t_A_j4vaSCriP7_ch4l1eng3@flare-on.com

 总结 

这个题目虽然不难，但是十分考验细节，比如会考察选手是否能够快速发现V8引擎被修改过的痕迹，考察选手对算法的一些观察能力，总的来说，细节决定成败，尤其是逆向分析一些算法的时候，一点点修改就可能导致运算结果并不相同。

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
readline.question(`Enter flag: `, flag => {
  readline.close();
  if (flag.length !== 44) {
    console.log("Try again.");
    process.exit(0);
  }
  var b = [];
  for (var i = 0; i < flag.length; i++) {
    b.push(flag.charCodeAt(i));
  }

  // something strange is happening...
  if (1n) {
    console.log("uh-oh, math is too correct...");
    process.exit(0);
  }

  var state = 1337;
  while (true) {
    state ^= Math.floor(Math.random() * (2**30));
    switch (state) {
      case 306211:
        if (Math.random() < 0.5) {
          b[30] -= b[34] + b[23] + b[5] + b[37] + b[33] + b[12] + Math.floor(Math.random() * 256);
          b[30] &= 0xFF;
        } else {
          b[26] -= b[24] + b[41] + b[13] + b[43] + b[6] + b[30] + 225;
          b[26] &= 0xFF;
        }
        state = 868071080;
        continue;
      case 311489:
        if (Math.random() < 0.5) {
          b[10] -= b[32] + b[1] + b[20] + b[30] + b[23] + b[9] + 115;
          b[10] &= 0xFF;
        } else {
          b[7] ^= (b[18] + b[14] + b[11] + b[25] + b[31] + b[21] + 19) & 0xFF;
        }
        state = 22167546;
        continue;
      case 755154:
        if (93909087n) {
          b[4] -= b[42] + b[6] + b[26] + b[39] + b[35] + b[16] + 80;
          b[4] &= 0xFF;
        } else {
          b[16] += b[36] + b[2] + b[29] + b[10] + b[12] + b[18] + 202;
          b[16] &= 0xFF;
        }
        state = 857247560;
        continue;
     
      case 1045388446:
        if (Math.random() < 0.5) {
          b[33] += b[40] + b[17] + b[43] + b[21] + b[36] + b[23] + 76;
          b[33] &= 0xFF;
        } else {
          b[20] -= b[37] + b[30] + b[12] + b[15] + b[6] + b[7] + 88;
          b[20] &= 0xFF;
        }
        state = 204284567;
        continue;
        //......省略，代码非常长
        //......省略，代码非常长
        //......省略，代码非常长
      case 1071767211:
        if (Math.random() < 0.5) {
          b[30] ^= (b[42] + b[9] + b[2] + b[36] + b[12] + b[16] + 241) & 0xFF;
        } else {
          b[20] ^= (b[41] + b[2] + b[40] + b[21] + b[36] + b[17] + 37) & 0xFF;
        }
        state = 109621765;
        continue;
      default:
        console.log("uh-oh, math.random() is too random...");
        process.exit(0);
    }
    break;
  }

  var target = [106, 196, 106, 178, 174, 102, 31, 91, 66, 255, 86, 196, 74, 139, 219, 166, 106, 4, 211, 68, 227, 72, 156, 38, 239, 153, 223, 225, 73, 171, 51, 4, 234, 50, 207, 82, 18, 111, 180, 212, 81, 189, 73, 76];
  if (b.every((x,i) => x === target[i])) {
    console.log('Congrats!');
  } else {
    console.log('Try again.');
  }
});
```



```
import subprocess
import right
import re
import right_judge
all_case_num=[]
def fix_js(): 
 count=1
 n_c=0
 fix_flag=False
 out_line=''
 with open('test_no_input.js','rt') as fd:
  line=fd.readline()
  while line:
   if 'case' in line:
    fix_flag=True
   if fix_flag and 'if' in line  and '>' not in line and '<' not in line:
    p = re.compile(r'[(](.*?)[)]', re.S)
    all_case_num.append(re.findall(p, line)[0])
    if right_judge.all_case_judge[n_c]:

     line='      if (true) {n'
    else:
     line='      if (false) {n'
    fix_flag=False
    n_c+=1
   out_line+=line
   line=fd.readline()
 print(out_line)
 with open('fixed_test.js','wt+') as fdo:
  fdo.write(out_line)

  
if __name__ == '__main__':

 fix_js()
```



```
import subprocess
import right
import re
import flare_random
import math
all_case_num=[]
end_num=185078700
random_magic_str='getrand(pos++)'
def fix_js(): 
 random_pos=0
 rcn=right.right_case
 rand_num=flare_random.randnum
 all_const_num=''

 out_line=[]
 with open('fixed_test.js','rt') as fd:
  data=fd.read()
 for case_num in rcn:
  random_pos+=1
  if case_num==end_num:
   break
  case_pos=data.find(str(case_num), 0)
  cond_block_start=data.find('(',case_pos)
  cond_block_end=data.find('{',case_pos)
  cond_block=data[cond_block_start:cond_block_end]
  if_true_block_start=data.find('{',case_pos)
  if_true_block_end=data.find('}', case_pos)
  if_true_block=data[if_true_block_start+1:if_true_block_end]
  if_false_block_start=data.find('{', if_true_block_end)
  if_false_block_end=data.find('}', if_true_block_end+1)
  cond_bool=None
  if random_magic_str in cond_block:
   if_rand_num=rand_num[random_pos]
   random_pos+=1
   sol_cond=cond_block.replace(random_magic_str,str(if_rand_num))
   cond_bool=eval(sol_cond)
  if 'true'  in cond_block:
   cond_bool=True
  if 'false'  in cond_block:
   cond_bool=False
  assert cond_bool!=None
  if_false_block=data[if_false_block_start+1:if_false_block_end]
  assert if_true_block.count(random_magic_str)<=1
  assert if_false_block.count(random_magic_str)<=1
  if cond_bool:
   exec_block=if_true_block
  else:
   exec_block=if_false_block
  #print(exec_block)
  line=exec_block
  if 'Math.floor(' in exec_block:
   m_start=exec_block.find('Math.floor',0)
   m_end=exec_block.find(')',m_start)
   m_end=exec_block.find(')',m_end+1)
   math_semt=exec_block[m_start:m_end+1]
   #print(math_semt)
   assert random_magic_str in math_semt
   math_semt_rand_num=rand_num[random_pos]
   sol_semt=math_semt.replace(random_magic_str,str(math_semt_rand_num)).replace('Math','math')
   #print(eval(sol_semt))
   random_pos+=1
   line=exec_block.replace(math_semt,str(eval(sol_semt)))
  if '&=' in line:
   line_list=line.split('n')
   formatline=line_list[1].replace(' ','')
  else:
   line_list=line.split('n')
   formatline=line_list[1].replace(' ','').replace('&0xFF','').replace('(','').replace(')','')
  #formatline)
  formatline_list=formatline.split('=')
  left_v=formatline_list[0][0:-1]
  op=formatline[len(left_v):len(left_v)+2]
  right_v=formatline_list[1].strip(';')
  add_nums=right_v.split('+')
  assert len(add_nums)==7
  const_num=add_nums[6]

  #获取所有下标，并且排序
  p = re.compile(r'[[](.*?)[]]', re.S)
  all_add_num=[]
  for i in range(6):
   all_add_num.append(int(re.findall(p, add_nums[i])[0]))
  all_add_num.sort()
  #print(all_add_num)
  fix_line=left_v+op
  for i in all_add_num:
   fix_line+='b[%d]+'%i
  fix_line+=const_num
  fix_line+='n'

  out_line.append(fix_line)
  
 print(''.join(out_line))
if __name__ == '__main__':

 fix_js()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1669433463.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1669433464.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1669433466.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1669433467.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1669433468.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669433470.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1669433474.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1669433475.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669433478.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1669433480.png)