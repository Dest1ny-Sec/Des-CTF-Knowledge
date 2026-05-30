# HXP 2021 CTP大赛LKVM虚拟机逃逸题writeup

> 原文: https://www.ctfiot.com/24005.html
> ID: 24005

在这个挑战中，我们被赋予了运行在hypervisor中的linux虚拟机的root权限，目标是实现hypervisor逃逸，以访问宿主机系统上的旗标文件。在这个过程中，我们发现了多个安全漏洞，通过它们可以实现lkvm的零日攻击，使得具有虚拟机访问权限的攻击者能够在宿主机上执行任意命令。

在这篇文章中，当提到行号时，请参考kvmtool的git checkout 39181fc6429f4e9e71473284940e35857b42772a。

攻击面

由于我们是在hypervisor内运行，并且宿主机和虚拟机内存之间实现了显式的隔离，因此，我们需要找到一种方法与宿主机的进程进行通信。实际上，我们可以通过pci与宿主机进行通信，因为Lkvm通过pci模拟了3个硬件设备：virtio-console、virtio-net和virtio-balloon。我们可以使用内存映射的IO与这些设备进行交互，也就是对特定的物理内存地址进行读取和写入操作。如果我们对0xd2000000-0xd20000ff(balloon-virtio)范围内的地址进行写操作，虚拟机就会被中断，并且控制流将被传递给linux系统的kvm驱动程序，然后进一步传递给lkvm进程。

信息泄露

当从这个地址执行读取操作时，我们首先遇到的一个函数是virtio/pci.c第148行的virtio_pci__data_in函数：

该函数可以将偏移量映射为bar（地址范围），这意味着，如果我们在地址0xD2000000+VIRTIO_PCI_QUEUE_NUM==0xD2000008处执行读取操作，我们将进入第二个case子句。需要注意的是，这里的默认case子句非常有趣：在第118行调用virtio_pci__specific_data_in：

在这里，我们总是以else if的case子句结束，因为这不是MSIX操作。另外，config_offset是根据从virtio_pci__data_in传递的偏移量来计算的，我们看到它具有完整的访问权限，并且没有进行任何绑定检查。并且，config_offset的值是在调用virtio__get_dev_specific_field时作为返回参数进行计算的。如果我们没有执行MSIX操作，config_offset就是设置为传递给virtio__get_dev_specific_field的第一个参数的值，其偏移量为-20。

到目前为止，我们只讨论了virtio和pci泛型函数，但这里调用了ops->get_config，在本例中，它从balloon驱动程序中提取了u8*配置。这个函数只是一个简单的getter，代码如下所示：

正如我们在下面所看到的，virtio_balloon_config是结构体的最后一个元素；读者可能已经注意到了，config结构体非常小。由于bar（地址范围）为0x100(0xD2000000-0xD20000FF)，因此，只要将偏移量设置为大于20，我们就能以0x100>20+sizeof(virtio_balloon_config)的形式访问这个config结构体。在这个地址范围内执行写入操作时，相当于对config结构体执行写操作，这意味着我们获得了一个越界读/写原语。

这段内存并没有分配在堆栈上，而是分配到一个mmaped区域中。这意味着我们无法通过破坏这个内存区来控制程序流。但是，我们能够利用这个漏洞来泄露信息，即泄露两个感兴趣的指针，其中一个指向bln_dev结构体本身的地址，另一个指向lkvm二进制文件的基址。

为了在用户空间进程中泄漏这两个指针，我们可以使用/dev/mem来访问虚拟机的物理内存，具体代码如下所示：

这里，leak_u64使用ioread8从virtio-balloon所在的0xD2000000处的mmap/dev/mem区域读取数据。我们将这20个字节加上一个越界的偏移量，使其正好指向lkvm可执行文件的地址，这样我们就能实现信息泄漏了。对于bln_dev泄漏，我们可以重复相同的过程。

获得程序流程的控制权

现在终于到了最有趣的部分：控制rip。假如我们能利用前面的漏洞来编写任意的越界代码，那么，我们可以破坏哪些有趣的数据呢？在下图中，我在virtio_pci__specific_data_in函数中设置了一个断点来检查bln_dev内存。在这里，我转储了位于config结构体后面的内存内容。其中，我们看到一些名为exit_lists的结构体，不幸的是，由于我们可以突破0x100的限制，所以，这些结构体都是可达的。但这些到底是什么？

由于virtio_pci__specific_data_in中的偏移量-20导致转储不是0x10对齐的，所以地址可能会有点乱

当lkvm二进制文件关闭时，它会进行拆卸处理，包括调用一些退出处理程序，这就是我们在这里发现的东西。如果我们查看init.c内部的第51行，我们会发现代码非常平易近人：

这里可以看到，在退出lkvm时，会遍历struct init_item数组，并从数组中的最后一个元素开始，对每个元素调用t->init函数。这就是前面发现的exit_lists。列表中的每个条目都是指向init_item的指针（该结构体也用于初始化，它也因此得名）。如果我们能够控制其中的指针，我们就就能伪造一个init_item，并在终止虚拟机操作系统时改变程序流程。

查看上面init_item的struct定义，我们就会发现它其实非常简单：其中包含2个链表指针、一个名称指针和我们想要控制的函数指针，它相对于init_item顶部的偏移量为0x18。

实际上，我们之前在virtio_pci__data_in函数中还发现了其他功能，而不仅仅是对config进行读取和写入操作。下面，让我们看一下virtio/pci.c第287行中该函数的等价物data_out：

这里，我们对VIRTIO_PCI_QUEUE_PFN的第二个case子句非常感兴趣，因为它调用了virtio-balloon特定的init虚拟队列函数。我们可以在virtio/balloon.c中的第200行找到这个函数，具体如下所示：

正如我们所看到的，当调用vring_init时，它将vr->desc=p设置为完全处于我们控制之下的虚拟机物理页面。我们可以看到，vring_init是从init_vq中调用的，参数是p，而p是从virtio_get_vq中获得的，在那里它可以找到给定页帧号（pfn）的宿主机虚拟地址。在init_vq中，我们看到参数vq被用来计算进入bdev->vqs数组的偏移量。这个queue = &bdev->vqs[vq]; 语句又是完全没有任何约束检查的，尽管在任何给定时间只有3个队列。这意味着，只要控制了vq参数，我们就可以有效地插入一个指向虚拟机内存的边界之外的指针。

在virtio_pci__data_out的代码清单中，对init_vq的调用是作为vq的参数通过vpci->queue_selector进行传递的，在同一个清单中，我们还发现完全可以通过switch语句中的VIRTIO_PCI_QUEUE_SEL子句来控制vpci->queue_selector。

通过下面vring*vr的结构体定义，我们可以看到它有4个成员，大小为0x20，这意味着我们不能在任意位置插入这个指针。实际上，只有在偏移量0x20*x+8处，我们才能完全控制x。

大家肯定还记得，我们的exit_lists离这个bdev结构体的位置并不远，而且，现在我们还获得了一个未绑定的、指示插入位置的指针，所以，我们只要将vq设置为0x16，那么，我们就能在这个exit_lists的最后一个条目中插入这个指针，具体代码如下所示：

这里，我们将页帧号设置为0x1，这表示虚拟机物理地址0x1000，并再次使用/dev/mem，将物理地址0x1000映射为我们具有读写权限的用户空间进程中的一个地址。显然，以任何正常的方式重新引导或退出虚拟机操作系统，都不会调用这些退出处理程序，但幸运的是，在未定义的指令导致内核崩溃时，却会调用这些程序。哈哈，大家还记得echo c > /proc/sysrq-trigger吗？

退出前的内存转储：

0x41代表字母A

这里我们看到，所有从上面的memset插入的“A”，都出现在exit_lists+72内的地址上。很明显，我们现在已经控制了程序流程，因为t->init(kvm)调用的这个地址完全处于我们的控制之下。既然已经得到了控制权，我们自然就可以重定向程序流程了。

现在，我们需要将代码重定向到一个目标，以便在宿主机系统上执行代码或命令，幸运的是，这个二进制文件含有返回函数virtio_net_exec_script的ret gadget：

超级好用的ret gadget

现在，如果我们能够控制$rdi寄存器并跳转到virtio_net_exec_script中用红色箭头标记的指令，就可以成功调用execl(command_we_control,…），从而在宿主机系统上执行命令。

综合起来

现在，我们已经能够伪造init_item，启动调用exevl的ROP链，或者说是JOP链，接下来，我们将借助于Jump oriented programming技术实现我们的目标。总而言之，我们现在利用第一个安全漏洞实现了指针泄露，并能控制该内存区域中一些字节的值，因为我们可以在泄漏的内区域中随意执行写入操作。同时，我们还找到了一种控制rip的方法，但遗憾的是，我们还无法控制函数调用t->init(kvm)中的参数kvm。

当我们第一次调用t->init时，$rbx指向我们伪造的init_item，也就是处于我们的控制之下的一段内存。

首先，我们要跳到这个gadget：mov rax, qword ptr [rbx + 0x28]; mov rdi, rbx; mov rsi, qword ptr [rax + 8]; call qword ptr [rax];

这将交换rbx和rdi寄存器中的值，使我们能够控制任何函数调用的第一个参数，并再次通过[$rbx + 0x28]获取一个新的跳转位置。

现在，我们可以直接跳到前面介绍的那个超级棒的gadget代码处了，因为我们现在能够控制$rdi了。

大功告成

现在，代码将调用execl(“/bin/sh”, “”, null); ，并返回一个shell！我们已经为这个漏洞申请了编号CVE-2021-45464，目前正在等待批准。至于完整的exploit，请参考原文末尾；但要注意的是，对于所有版本的lkvm来说，必须对利用代码进行相应的修改：根据特定的二进制代码修改gadget的偏移量。

参考来源：https://www.kalmarunionen.dk/writeups/2021/hxp-2021/lkvm/

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/8-1642924682.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/6-1642924682.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/1-1642924682.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/1-1642924682-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/4-1642924682.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/0-1642924682.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/2-1642924682.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/10-1642924682.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/5-1642924682.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/8-1642924683.png)