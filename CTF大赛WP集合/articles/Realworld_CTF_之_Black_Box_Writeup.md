# Realworld CTF 之 Black Box Writeup

> 原文: https://www.ctfiot.com/27566.html
> ID: 27566

题目描述

Black Box
Score: 451

Virtual Machine, Clone-and-Pwn, difficulty:normal

This is a challenge that is two years late about CVE-2020-14364. Enjoy it :)

nc 47.243.43.90 1234

启动

qemu-a575af0/bin/debug/naive/x86_64-softmmu/qemu-system-x86_64 --enable-kvm -m 4096 -usb -device usb-tablet,bus=usb-bus.0 ./OS64.img -net user,hostfwd=tcp::22222-:22 -net nic

使用的驱动是uhci

漏洞成因

在/qemu/hw/usb/core.c文件中存在如下代码

static void usb_process_one(USBPacket *p)
{
 USBDevice *dev = p->ep->dev;

 /*
 * Handlers expect status to be initialized to USB_RET_SUCCESS, but it
 * can be USB_RET_NAK here from a previous usb_process_one() call,
 * or USB_RET_ASYNC from going through usb_queue_one().
 */
 p->status = USB_RET_SUCCESS;

 if (p->ep->nr == 0) {
 /* control pipe */
 if (p->parameter) {
 do_parameter(dev, p);
 return;
 }
 switch (p->pid) {
 case USB_TOKEN_SETUP:
 do_token_setup(dev, p); // ①
 break;
 case USB_TOKEN_IN:
 do_token_in(dev, p); // ②
 break;
 case USB_TOKEN_OUT:
 do_token_out(dev, p); // ③
 break;
 default:
 p->status = USB_RET_STALL;
 }
 } else {
 /* data pipe */
 usb_device_handle_data(dev, p);
 }
}

上述代码中标注的三处都是存在问题的函数，我们一一来看。

do_token_setup函数

这里相当于进行一个初始化操作，允许你后续发送的数据包能够进入读写操作。问题主要在打有中文注释的地方，s->setup_buf的内容就是从我们的数据包中获取的，所以这里的s->setup_len受到我们的控制。这里进行的是先赋值后检测的操作，典型的先上车后补票（ 这也是此处的问题所在。

static void do_token_setup(USBDevice *s, USBPacket *p)
{
 int request, value, index;

 if (p->iov.size != 8) {
 p->status = USB_RET_STALL;
 return;
 }

 usb_packet_copy(p, s->setup_buf, p->iov.size);
 s->setup_index = 0;
 p->actual_length = 0;
 s->setup_len = (s->setup_buf[7] << 8) | s->setup_buf[6]; // 此处
 if (s->setup_len > sizeof(s->data_buf)) { // 此处
 fprintf(stderr,
 "usb_generic_handle_packet: ctrl buffer too small (%d > %zu)n",
 s->setup_len, sizeof(s->data_buf));
 p->status = USB_RET_STALL;
 return;
 }

 request = (s->setup_buf[0] << 8) | s->setup_buf[1];
 value = (s->setup_buf[3] << 8) | s->setup_buf[2];
 index = (s->setup_buf[5] << 8) | s->setup_buf[4];

 if (s->setup_buf[0] & USB_DIR_IN) {
 usb_device_handle_control(s, p, request, value, index,
 s->setup_len, s->data_buf);
 if (p->status == USB_RET_ASYNC) {
 s->setup_state = SETUP_STATE_SETUP;
 }
 if (p->status != USB_RET_SUCCESS) {
 return;
 }

 if (p->actual_length < s->setup_len) {
 s->setup_len = p->actual_length;
 }
 s->setup_state = SETUP_STATE_DATA;
 } else {
 if (s->setup_len == 0)
 s->setup_state = SETUP_STATE_ACK;
 else
 s->setup_state = SETUP_STATE_DATA;
 }

 p->actual_length = 8;
}

do_token_in函数

s->setup_len受到我们的控制，在do_token_setup函数中已经被我们赋值。来看标注的第二处，如果s->setup_index在一次次数据包发送的操作过程中逐渐累加，最终超出了我们的s->setup_len，s->setup_state就会被赋值为SETUP_STATE_ACK，意味着后续的包我们无法再进行读写操作。那么我们可以将其赋值为一个很大的值，来扩大我们可操作的范围。

static void do_token_in(USBDevice *s, USBPacket *p)
{
 int request, value, index;

 assert(p->ep->nr == 0);

 request = (s->setup_buf[0] << 8) | s->setup_buf[1];
 value = (s->setup_buf[3] << 8) | s->setup_buf[2];
 index = (s->setup_buf[5] << 8) | s->setup_buf[4];

 switch(s->setup_state) {
 case SETUP_STATE_ACK:
 if (!(s->setup_buf[0] & USB_DIR_IN)) {
 usb_device_handle_control(s, p, request, value, index,
 s->setup_len, s->data_buf);
 if (p->status == USB_RET_ASYNC) {
 return;
 }
 s->setup_state = SETUP_STATE_IDLE;
 p->actual_length = 0;
 }
 break;

 case SETUP_STATE_DATA:
 if (s->setup_buf[0] & USB_DIR_IN) {
 int len = s->setup_len - s->setup_index; // 第一处
 if (len > p->iov.size) {
 len = p->iov.size;
 }
 usb_packet_copy(p, s->data_buf + s->setup_index, len);
 s->setup_index += len;
 if (s->setup_index >= s->setup_len) { // 第二处
 s->setup_state = SETUP_STATE_ACK;
 }
 return;
 }
 s->setup_state = SETUP_STATE_IDLE;
 p->status = USB_RET_STALL;
 break;

 default:
 p->status = USB_RET_STALL;
 }
}

do_token_out函数

和上述的do_token_in函数一致，可以根据s->setup_len受控这一点，扩大我们可操作的范围。

static void do_token_out(USBDevice *s, USBPacket *p)
{
 assert(p->ep->nr == 0);

 switch(s->setup_state) {
 case SETUP_STATE_ACK:
 if (s->setup_buf[0] & USB_DIR_IN) {
 s->setup_state = SETUP_STATE_IDLE;
 /* transfer OK */
 } else {
 /* ignore additional output */
 }
 break;

 case SETUP_STATE_DATA:
 if (!(s->setup_buf[0] & USB_DIR_IN)) {
 int len = s->setup_len - s->setup_index;
 if (len > p->iov.size) {
 len = p->iov.size;
 }
 usb_packet_copy(p, s->data_buf + s->setup_index, len);
 s->setup_index += len;
 if (s->setup_index >= s->setup_len) {
 s->setup_state = SETUP_STATE_ACK;
 }
 return;
 }
 s->setup_state = SETUP_STATE_IDLE;
 p->status = USB_RET_STALL;
 break;

 default:
 p->status = USB_RET_STALL;
 }
}

相关结构体

 
 #define USB_TOKEN_SETUP 0x2d
 #define USB_TOKEN_IN 0x69 /* device -> host */
 #define USB_TOKEN_OUT 0xe1 /* host -> device */

struct QEMUTimer {
 int64_t expire_time; /* in nanoseconds */
 QEMUTimerList *timer_list;
 QEMUTimerCB *cb;
 void *opaque;
 QEMUTimer *next;
 int attributes;
 int scale;
};
 
struct USBPacket {
 /* Data fields for use by the driver. */
 int pid;
 uint64_t id;
 USBEndpoint *ep;
 unsigned int stream;
 QEMUIOVector iov;
 uint64_t parameter; /* control transfers */
 bool short_not_ok;
 bool int_req;
 int status; /* USB_RET_* status code */
 int actual_length; /* Number of bytes actually transferred */
 /* Internal use by the USB layer. */
 USBPacketState state;
 USBCombinedPacket *combined;
 QTAILQ_ENTRY(USBPacket) queue;
 QTAILQ_ENTRY(USBPacket) combined_entry;
};
 
/* definition of a USB device */
 struct USBDevice {
 DeviceState qdev;
 USBPort *port; // 指向的是uhcistate中的ports
 char *port_path;
 char *serial;
 void *opaque;
 uint32_t flags;
 
 /* Actual connected speed */
 int speed;
 /* Supported speeds, not in info because it may be variable (hostdevs) */
 int speedmask;
 uint8_t addr;
 char product_desc[32];
 int auto_attach;
 int attached;
 
 int32_t state;
 uint8_t setup_buf[8];
 uint8_t data_buf[4096]; / 0x7fffxxxx 虚拟机地址
 int32_t remote_wakeup;
 int32_t setup_state;
 int32_t setup_len;
 int32_t setup_index;
 
 USBEndpoint ep_ctl;
 USBEndpoint ep_in[USB_MAX_ENDPOINTS];
 USBEndpoint ep_out[USB_MAX_ENDPOINTS];
 
 QLIST_HEAD(, USBDescString) strings;
 const USBDesc *usb_desc; /* Overrides class usb_desc if not NULL */
 const USBDescDevice *device; / 0x5ff55xxx 物理机虚拟地址
 
 int configuration;
 int ninterfaces;
 int altsetting[USB_MAX_INTERFACES];
 const USBDescConfig *config;
 const USBDescIface *ifaces[USB_MAX_INTERFACES];
 };

#define NB_PORTS 6
struct UHCIState {
 PCIDevice dev;
 MemoryRegion io_bar;
 USBBus bus; /* Note unused when we're a companion controller */
 uint16_t cmd; /* cmd register */
 uint16_t status;
 uint16_t intr; /* interrupt enable register */
 uint16_t frnum; /* frame number */
 uint32_t fl_base_addr; /* frame list base address */
 uint8_t sof_timing;
 uint8_t status2; /* bit 0 and 1 are used to generate UHCI_STS_USBINT */
 int64_t expire_time;
 QEMUTimer *frame_timer;
 QEMUBH *bh;
 uint32_t frame_bytes;
 uint32_t frame_bandwidth;
 bool completions_only;
 UHCIPort ports[NB_PORTS];

 /* Interrupts that should be raised at the end of the current frame. */
 uint32_t pending_int_mask;

 /* Active packets */
 QTAILQ_HEAD(, UHCIQueue) queues;
 uint8_t num_ports_vmstate;

 /* Properties */
 char *masterbus;
 uint32_t firstport;
 uint32_t maxframes;
};

typedef struct UHCI_QH {
 uint32_t link;
 uint32_t el_link;
} UHCI_QH;

struct UHCIState {
 PCIDevice dev;
 MemoryRegion io_bar;
 USBBus bus; /* Note unused when we're a companion controller */
 uint16_t cmd; /* cmd register */
 uint16_t status;
 uint16_t intr; /* interrupt enable register */
 uint16_t frnum; /* frame number */
 uint32_t fl_base_addr; /* frame list base address */
 uint8_t sof_timing;
 uint8_t status2; /* bit 0 and 1 are used to generate UHCI_STS_USBINT */
 int64_t expire_time;
 QEMUTimer *frame_timer;
 QEMUBH *bh;
 uint32_t frame_bytes;
 uint32_t frame_bandwidth;
 bool completions_only;
 UHCIPort ports[NB_PORTS];

 /* Interrupts that should be raised at the end of the current frame. */
 uint32_t pending_int_mask;

 /* Active packets */
 QTAILQ_HEAD(, UHCIQueue) queues;
 uint8_t num_ports_vmstate;

 /* Properties */
 char *masterbus;
 uint32_t firstport;
 uint32_t maxframes;
};

typedef struct UHCI_TD {
 uint32_t link; // 指向另外一个TD或者QH
 uint32_t ctrl; /* see TD_CTRL_xxx */
 uint32_t token;
 uint32_t buffer;
} UHCI_TD;
/*
link:
	Vf：告知HC，该深度遍历还是广度遍历。深度遍历就是跑向Link pointer的指向的TD；广度遍历跑向Link pointer指向的另外一个QH。1=depth first；0=breadth first。

	Q：表示Link pointer指向的是TD(0)还是QH(1)。

	T：1=Link pointer无效；0=Link pointer是有效的。该bit告知HC本TD中link pointer是否指向另外一个数据流入口。如果TD在一个队列里中，该bit代表告知HC，队列中已经没有另外的有效数据流入口了。也就是说本TD是最后一个TD。
*/

struct UHCIQueue {
 uint32_t qh_addr;
 uint32_t token;
 UHCIState *uhci;
 USBEndpoint *ep;
 QTAILQ_ENTRY(UHCIQueue) next;
 QTAILQ_HEAD(, UHCIAsync) asyncs;
 int8_t valid;
};

struct UHCIAsync {
 USBPacket packet;
 uint8_t static_buf[64]; /* 64 bytes is enough, except for isoc packets */
 uint8_t *buf;
 UHCIQueue *queue;
 QTAILQ_ENTRY(UHCIAsync) next;
 uint32_t td_addr;
 uint8_t done;
};

typedef struct UHCIPort {
 USBPort port;
 uint16_t ctrl;
} UHCIPort;

uhci发包协议

大致流程如图所示
img

再结合我们的uhci文档里描述的，其协议一共分为

首先是Frame_list_base_address，从UHCI的IO Register中读到的，指向了我们的Frame List。

其次是Frame List pointer，指向第一个需要调度的结构体的地址
image-20210112134735188

Q：表示Link pointer指向的是TD(0)还是QH(1)。

T：表示告知HC，该Frame是否有有效的数据流入口。1、表示空的frame；0表示有效入口。

接着是Transfer Descriptor，描述了数据包里的情况
image-20210112135056364

Link pointer指指向另外一个TD或者QH。

Vf：告知HC，该深度遍历还是广度遍历。深度遍历就是跑向Link pointer的指向的TD；广度遍历跑向Link pointer指向的另外一个QH。1=depth first；0=breadth first。

Q：表示Link pointer指向的是TD(0)还是QH(1)。

T：1=Link pointer无效；0=Link pointer是有效的。该bit告知HC本TD中link pointer是否指向另外一个数据流入口。如果TD在一个队列里中，该bit代表告知HC，队列中已经没有另外的有效数据流入口了。也就是说本TD是最后一个TD。

Buffer Pointer指向了我们数据包里buffer内容的地址

发包流程

uhci的发送数据包逻辑大致就是发包的函数与时钟超时的回调函数绑定，每1000ns会自动调用一个时钟超时的回调函数来调整到期时间。

#define NANOSECONDS_PER_SECOND 1000000000LL
#define FRAME_TIMER_FREQ 1000
static void uhci_port_write(void *opaque, hwaddr addr,
 uint64_t val, unsigned size)
{
 UHCIState *s = opaque;

 trace_usb_uhci_mmio_writew(addr, val);

 switch(addr) {
 case 0x00:
 if ((val & UHCI_CMD_RS) && !(s->cmd & UHCI_CMD_RS)) {
 /* start frame processing */
 trace_usb_uhci_schedule_start();
 s->expire_time = qemu_clock_get_ns(QEMU_CLOCK_VIRTUAL) +
 (NANOSECONDS_PER_SECOND / FRAME_TIMER_FREQ); // 这里的s->expire_time就是设置时钟的到期时间，这里时间单位为ns
 timer_mod(s->frame_timer, s->expire_time); // 主要是在这里，s->frame_timer回调函数
 s->status &= ~UHCI_STS_HCHALTED;
 } else if (!(val & UHCI_CMD_RS)) {
 s->status |= UHCI_STS_HCHALTED;
 }
 ......
 }
 ......
}

// s->frame_timer = timer_new_ns(QEMU_CLOCK_VIRTUAL, uhci_frame_timer, s);

// 这里是设定一个定时器
void timer_mod(QEMUTimer *ts, int64_t expire_time)
{
 timer_mod_ns(ts, expire_time * ts->scale);
}

// 第一个参数为定时器对象，第二个参数则为到期时间
// timer_mod_ns 首先从所属的QEMUTimer删除定时器，然后再调用timer_mod_ns_locked添加定时器
void timer_mod_ns(QEMUTimer *ts, int64_t expire_time)
{
 QEMUTimerList *timer_list = ts->timer_list;
 bool rearm;

 qemu_mutex_lock(&timer_list->active_timers_lock);
 timer_del_locked(timer_list, ts);
 rearm = timer_mod_ns_locked(timer_list, ts, expire_time); 
 qemu_mutex_unlock(&timer_list->active_timers_lock);

 if (rearm) {
 timerlist_rearm(timer_list);
 }
}

static bool timer_mod_ns_locked(QEMUTimerList *timer_list,
 QEMUTimer *ts, int64_t expire_time)
{
 QEMUTimer **pt, *t;

 /* add the timer in the sorted list */
 pt = &timer_list->active_timers;
 for (;;) {
 t = *pt;
 if (!timer_expired_ns(t, expire_time)) {
 break;
 }
 pt = &t->next;
 }
 ts->expire_time = MAX(expire_time, 0); // 此处
 ts->next = *pt;
 atomic_set(pt, ts);

 return pt == &timer_list->active_timers;
}

static void uhci_frame_timer(void *opaque)
{
 ......
 for (i = 0; i < frames; i++) {
 s->frame_bytes = 0;
 trace_usb_uhci_frame_start(s->frnum);
 uhci_async_validate_begin(s);
 uhci_process_frame(s); // 这里发包
 uhci_async_validate_end(s);
 /* The spec says frnum is the frame currently being processed, and
 * the guest must look at frnum - 1 on interrupt, so inc frnum now */
 s->frnum = (s->frnum + 1) & 0x7ff;
 s->expire_time += frame_t;
 }
 ......
 timer_mod(s->frame_timer, t_now + frame_t); // 这里重新设定到期时间
}

利用思路

step1

do_token_setup -> 先发一个正常包设置 s->setup_state

在uhci_port_write中设置好frame_list_base，然后发送数据包。

原本想着在uhci_port_write函数中利用0x10和0x12端口，对s->fl_base_addr进行自定义，以达到精确定位。

但是后来发现s->fl_base_addr进行到这一步的时候会自动读取寄存器里面的值进行重置，而且每一次都不一样，所以就打算暴力覆盖

static void uhci_process_frame(UHCIState *s)
{
 ......
 uint32_t frame_addr, link, old_td_ctrl, val, int_mask;
 uint32_t curr_qh, td_count = 0;
 int cnt, ret;
 UHCI_TD td;
 UHCI_QH qh;
 QhDb qhdb;

 frame_addr = s->fl_base_addr + ((s->frnum & 0x3ff) << 2);

 pci_dma_read(&s->dev, frame_addr, &link, 4);
 le32_to_cpus(&link);
 ......
}

usb/core.c：do_token_setup函数中存在如下检测

static void do_token_setup(USBDevice *s, USBPacket *p)
{
 int request, value, index;

 if (p->iov.size != 8) {
 p->status = USB_RET_STALL;
 return;
 }
 ......
}

对其溯源，查看p->iov.size是在哪里被赋值的，可以发现usb/hcd-uhci.c：uhci_handle_td中存在这么一段

static int uhci_handle_td(UHCIState *s, UHCIQueue *q, uint32_t qh_addr,
 UHCI_TD *td, uint32_t td_addr, uint32_t *int_mask)
{
	......
	max_len = ((td->token >> 21) + 1) & 0x7ff; // 这里的max_len，td->token可控
 spd = (pid == USB_TOKEN_IN && (td->ctrl & TD_CTRL_SPD) != 0);
 usb_packet_setup(&async->packet, pid, q->ep, 0, td_addr, spd,
 (td->ctrl & TD_CTRL_IOC) != 0);
 if (max_len <= sizeof(async->static_buf)) {
 async->buf = async->static_buf;
 } else {
 async->buf = g_malloc(max_len);
 }
 usb_packet_addbuf(&async->packet, async->buf, max_len); // 以及这里的usb_packet_addbuf函数
 ......
}

void usb_packet_addbuf(USBPacket *p, void *ptr, size_t len)
{
 qemu_iovec_add(&p->iov, ptr, len);
}

void qemu_iovec_add(QEMUIOVector *qiov, void *base, size_t len)
{
 assert(qiov->nalloc != -1);

 if (qiov->niov == qiov->nalloc) {
 qiov->nalloc = 2 * qiov->nalloc + 1;
 qiov->iov = g_renew(struct iovec, qiov->iov, qiov->nalloc);
 }
 qiov->iov[qiov->niov].iov_base = base;
 qiov->iov[qiov->niov].iov_len = len;
 qiov->size += len; // 可以看到，这里对其进行了赋值
 ++qiov->niov;
}

step2

do_token_setup -> 发一个size为0x5000的包设置 s->setup_len，以达到我们分析漏洞中扩大s->setup_index的操作范围

step3

do_token_out -> 越界写，控制 s->setup_index，设置为-8，以达到向上越界修改我们的s->setup_buf[0]的效果

usb/core.c中的do_token_out函数，作用是将我们伪造的数据写入到内存中

static void do_token_out(USBDevice *s, USBPacket *p)
{
 ......
 case SETUP_STATE_DATA:
 if (!(s->setup_buf[0] & USB_DIR_IN)) {
 int len = s->setup_len - s->setup_index;
 if (len > p->iov.size) {
 len = p->iov.size;
 }
 usb_packet_copy(p, s->data_buf + s->setup_index, len); // 这里
 s->setup_index += len;
 if (s->setup_index >= s->setup_len) {
 s->setup_state = SETUP_STATE_ACK;
 }
 return;
 }
 ......
}

void usb_packet_copy(USBPacket *p, void *ptr, size_t bytes)
{
 ......
 switch (p->pid) {
 case USB_TOKEN_SETUP:
 case USB_TOKEN_OUT: (0xe1)
 iov_to_buf(iov->iov, iov->niov, p->actual_length, ptr, bytes); // 这里
 break;
 ......
}
 
static inline size_t
iov_to_buf(const struct iovec *iov, const unsigned int iov_cnt,
 size_t offset, void *buf, size_t bytes)
{
 if (__builtin_constant_p(bytes) && iov_cnt &&
 offset <= iov[0].iov_len && bytes <= iov[0].iov_len - offset) {
 memcpy(buf, iov[0].iov_base + offset, bytes);
 return bytes;
 } else {
 return iov_to_buf_full(iov, iov_cnt, offset, buf, bytes);
 }
}
 
size_t iov_to_buf_full(const struct iovec *iov, const unsigned int iov_cnt,
 size_t offset, void *buf, size_t bytes)
{
 size_t done;
 unsigned int i;
 for (i = 0, done = 0; (offset || done < bytes) && i < iov_cnt; i++) {
 if (offset < iov[i].iov_len) {
 size_t len = MIN(iov[i].iov_len - offset, bytes - done);
 memcpy(buf + done, iov[i].iov_base + offset, len);
 done += len;
 offset = 0;
 } else {
 offset -= iov[i].iov_len;
 }
 }
 assert(offset == 0);
 return done;
}

对在iov.c文件里iov_to_buf_full函数中的iov[i].iov_base溯源，让我们康康其到底是 在哪里被赋值的

void usb_packet_copy(USBPacket *p, void *ptr, size_t bytes)
{
 QEMUIOVector *iov = p->combined ? &p->combined->iov : &p->iov; // 注意这里的iov
 ......
 case USB_TOKEN_OUT:
 iov_to_buf(iov->iov, iov->niov, p->actual_length, ptr, bytes); 
 break;
 ....
}

static inline size_t
iov_to_buf(const struct iovec *iov, const unsigned int iov_cnt,
 size_t offset, void *buf, size_t bytes)
{
 if (__builtin_constant_p(bytes) && iov_cnt &&
 offset <= iov[0].iov_len && bytes <= iov[0].iov_len - offset) {
 memcpy(buf, iov[0].iov_base + offset, bytes);
 return bytes;
 } else {
 return iov_to_buf_full(iov, iov_cnt, offset, buf, bytes);
 }
}

size_t iov_to_buf_full(const struct iovec *iov, const unsigned int iov_cnt,
 size_t offset, void *buf, size_t bytes)
{
 ......
	memcpy(buf + done, iov[i].iov_base + offset, len);
 ......
}

可以看到，在/usb/hcd-uhci.c函数中有这么一段，将你自定义的td->buffer copy到async->buf

/usb/hcd-uhci.c:891
pci_dma_read(&s->dev, td->buffer, async->buf, max_len); // 同样，此处的max_len也收到限制，最大为0x7ff，且每次copy的td->buffer都是一个起始地址

再来看async->buf究竟是什么

pwndbg> p &async->buf
$40 = (uint8_t **) 0x555557046788

pwndbg> p &(*async->buf)
$43 = (uint8_t *) 0x555556a2b400 ""

pwndbg> p *async->packet->iov->iov
$47 = {
 iov_base = 0x555556a2b400, 
 iov_len = 1029
}

可以看到，我们最开始copy的iob[i].iov_base的内容就是在/usb/hcd-uhci.c函数中由你td->buffer copy过来的，但是最长长度只有0x7ff，而且每次的基址都是从开头开始。所以这里我们就只能先copy三次脏数据，每次的长度为0x404，第四次再伪造数据，覆盖USBDevice结构体里的setup_index，setup_len，以及setup_state。

step4

do_token_out -> 越界写，控制 s->setup_buf[0]，将其改为0x80。

step3和step4步骤主要操作就是设置setup_index = 0xfffffff8，再次越界，修改setup_buf [0]的值，然后再次将setup_index修改为要读取的地址，以实现任意地址读取。

step5

do_token_in -> 读操作，泄漏usbdevice->data_buf和usbdevice对象地址。这里主要是泄露USBDevice结构体中ep_ctl->dev的数据，ep_ctl->dev指向的就是我们usbdevice的对象地址，通过这个地址，我们进而获取到usbdevice->data_buf的地址。以usbdevice->data_buf，我们就可以方便的计算其他地址距离usbdevice->data_buf的偏移，以此来修改我们的usbdevice->setup_index。

step6

do_token_in -> 读操作，泄露text段中的内容，以获取text_base和heap_base。借由text_base，加上system_plt的偏移，以得到system的地址。

step7

接下来我们需要的就是找一个地方，修改为我们的system_plt，参数改为xcalc。

此处参考了CVE-2019-6788的利用手法，借助了QEMUTimer。

在bss段有个全局数组main_loop_tlg，它是QEMUTimerList的数组。我们可以在堆中伪造一个QEMUTimerList，将cb指针覆盖成想要执行的函数，opaque为参数地址。再将其地址覆盖到main_loop_tlg中，等expire_time时间到，将会执行cb(opaque)，成功控制程序执行流。

// util/qemu-timer.c
struct QEMUTimerList {
 QEMUClock *clock;
 QemuMutex active_timers_lock;
 QEMUTimer *active_timers;
 QLIST_ENTRY(QEMUTimerList) list;
 QEMUTimerListNotifyCB *notify_cb;
 void *notify_opaque;

 /* lightweight method to mark the end of timerlist's running */
 QemuEvent timers_done_ev;
};

// include/qemu/timer.h
struct QEMUTimer {
 int64_t expire_time; /* in nanoseconds */
 QEMUTimerList *timer_list;
 QEMUTimerCB *cb; // 函数指针
 void *opaque; // 参数
 QEMUTimer *next;
 int attributes;
 int scale;
};

当然，也可以走hid_idle_timer

 ► f 0 557e590fa1a0 usb_hid_handle_control
 f 1 557e590d3ed7 usb_device_handle_control+151
 f 2 557e590d0f49 do_token_in+280
 f 3 557e590d165b usb_process_one+168
 f 4 557e590d1859 usb_handle_packet+335
 f 5 557e590dc76c uhci_handle_td+1285
 f 6 557e590dcd6c uhci_process_frame+674
 f 7 557e590dd18a uhci_frame_timer+407

usb_hid_handle_control –> hid_set_next_idle –> hid_idle_timer

static void usb_hid_handle_control(USBDevice *dev, USBPacket *p,
 int request, int value, int index, int length, uint8_t *data)
{
 USBHIDState *us = USB_HID(dev);
 HIDState *hs = &us->hid;
 int ret;
 ......
 case HID_SET_IDLE:
 hs->idle = (uint8_t) (value >> 8);
 hid_set_next_idle(hs);
 if (hs->kind == HID_MOUSE || hs->kind == HID_TABLET) {
 hid_pointer_activate(hs);
 }
 break;
 default:
 fail:
 p->status = USB_RET_STALL;
 break;
 }
}

void hid_set_next_idle(HIDState *hs)
{
 if (hs->idle) {
 uint64_t expire_time = qemu_clock_get_ns(QEMU_CLOCK_VIRTUAL) +
 NANOSECONDS_PER_SECOND * hs->idle * 4 / 1000;
 if (!hs->idle_timer) {
 hs->idle_timer = timer_new_ns(QEMU_CLOCK_VIRTUAL, hid_idle_timer, hs);
 }
 timer_mod_ns(hs->idle_timer, expire_time);
 } else {
 hid_del_idle_timer(hs);
 }
}

static void hid_idle_timer(void *opaque)
{
 HIDState *hs = opaque;

 hs->idle_pending = true;
 hs->event(hs); // 这里
}

最终结果
image-20210112152526748


```
Black Box
Score: 451

Virtual Machine, Clone-and-Pwn, difficulty:normal

This is a challenge that is two years late about CVE-2020-14364. Enjoy it :)

nc 47.243.43.90 1234
```



```
qemu-a575af0/bin/debug/naive/x86_64-softmmu/qemu-system-x86_64 --enable-kvm -m 4096 -usb -device usb-tablet,bus=usb-bus.0 ./OS64.img -net user,hostfwd=tcp::22222-:22 -net nic
```



```
static void usb_process_one(USBPacket *p)
{
 USBDevice *dev = p->ep->dev;

 /*
 * Handlers expect status to be initialized to USB_RET_SUCCESS, but it
 * can be USB_RET_NAK here from a previous usb_process_one() call,
 * or USB_RET_ASYNC from going through usb_queue_one().
 */
 p->status = USB_RET_SUCCESS;

 if (p->ep->nr == 0) {
 /* control pipe */
 if (p->parameter) {
 do_parameter(dev, p);
 return;
 }
 switch (p->pid) {
 case USB_TOKEN_SETUP:
 do_token_setup(dev, p); // ①
 break;
 case USB_TOKEN_IN:
 do_token_in(dev, p); // ②
 break;
 case USB_TOKEN_OUT:
 do_token_out(dev, p); // ③
 break;
 default:
 p->status = USB_RET_STALL;
 }
 } else {
 /* data pipe */
 usb_device_handle_data(dev, p);
 }
}
```



```
static void do_token_setup(USBDevice *s, USBPacket *p)
{
 int request, value, index;

 if (p->iov.size != 8) {
 p->status = USB_RET_STALL;
 return;
 }

 usb_packet_copy(p, s->setup_buf, p->iov.size);
 s->setup_index = 0;
 p->actual_length = 0;
 s->setup_len = (s->setup_buf[7] << 8) | s->setup_buf[6]; // 此处
 if (s->setup_len > sizeof(s->data_buf)) { // 此处
 fprintf(stderr,
 "usb_generic_handle_packet: ctrl buffer too small (%d > %zu)n",
 s->setup_len, sizeof(s->data_buf));
 p->status = USB_RET_STALL;
 return;
 }

 request = (s->setup_buf[0] << 8) | s->setup_buf[1];
 value = (s->setup_buf[3] << 8) | s->setup_buf[2];
 index = (s->setup_buf[5] << 8) | s->setup_buf[4];

 if (s->setup_buf[0] & USB_DIR_IN) {
 usb_device_handle_control(s, p, request, value, index,
 s->setup_len, s->data_buf);
 if (p->status == USB_RET_ASYNC) {
 s->setup_state = SETUP_STATE_SETUP;
 }
 if (p->status != USB_RET_SUCCESS) {
 return;
 }

 if (p->actual_length < s->setup_len) {
 s->setup_len = p->actual_length;
 }
 s->setup_state = SETUP_STATE_DATA;
 } else {
 if (s->setup_len == 0)
 s->setup_state = SETUP_STATE_ACK;
 else
 s->setup_state = SETUP_STATE_DATA;
 }

 p->actual_length = 8;
}
```



```
static void do_token_in(USBDevice *s, USBPacket *p)
{
 int request, value, index;

 assert(p->ep->nr == 0);

 request = (s->setup_buf[0] << 8) | s->setup_buf[1];
 value = (s->setup_buf[3] << 8) | s->setup_buf[2];
 index = (s->setup_buf[5] << 8) | s->setup_buf[4];

 switch(s->setup_state) {
 case SETUP_STATE_ACK:
 if (!(s->setup_buf[0] & USB_DIR_IN)) {
 usb_device_handle_control(s, p, request, value, index,
 s->setup_len, s->data_buf);
 if (p->status == USB_RET_ASYNC) {
 return;
 }
 s->setup_state = SETUP_STATE_IDLE;
 p->actual_length = 0;
 }
 break;

 case SETUP_STATE_DATA:
 if (s->setup_buf[0] & USB_DIR_IN) {
 int len = s->setup_len - s->setup_index; // 第一处
 if (len > p->iov.size) {
 len = p->iov.size;
 }
 usb_packet_copy(p, s->data_buf + s->setup_index, len);
 s->setup_index += len;
 if (s->setup_index >= s->setup_len) { // 第二处
 s->setup_state = SETUP_STATE_ACK;
 }
 return;
 }
 s->setup_state = SETUP_STATE_IDLE;
 p->status = USB_RET_STALL;
 break;

 default:
 p->status = USB_RET_STALL;
 }
}
```



```
static void do_token_out(USBDevice *s, USBPacket *p)
{
 assert(p->ep->nr == 0);

 switch(s->setup_state) {
 case SETUP_STATE_ACK:
 if (s->setup_buf[0] & USB_DIR_IN) {
 s->setup_state = SETUP_STATE_IDLE;
 /* transfer OK */
 } else {
 /* ignore additional output */
 }
 break;

 case SETUP_STATE_DATA:
 if (!(s->setup_buf[0] & USB_DIR_IN)) {
 int len = s->setup_len - s->setup_index;
 if (len > p->iov.size) {
 len = p->iov.size;
 }
 usb_packet_copy(p, s->data_buf + s->setup_index, len);
 s->setup_index += len;
 if (s->setup_index >= s->setup_len) {
 s->setup_state = SETUP_STATE_ACK;
 }
 return;
 }
 s->setup_state = SETUP_STATE_IDLE;
 p->status = USB_RET_STALL;
 break;

 default:
 p->status = USB_RET_STALL;
 }
}
```



```
#define USB_TOKEN_SETUP 0x2d
 #define USB_TOKEN_IN 0x69 /* device -> host */
 #define USB_TOKEN_OUT 0xe1 /* host -> device */

struct QEMUTimer {
 int64_t expire_time; /* in nanoseconds */
 QEMUTimerList *timer_list;
 QEMUTimerCB *cb;
 void *opaque;
 QEMUTimer *next;
 int attributes;
 int scale;
};
 
struct USBPacket {
 /* Data fields for use by the driver. */
 int pid;
 uint64_t id;
 USBEndpoint *ep;
 unsigned int stream;
 QEMUIOVector iov;
 uint64_t parameter; /* control transfers */
 bool short_not_ok;
 bool int_req;
 int status; /* USB_RET_* status code */
 int actual_length; /* Number of bytes actually transferred */
 /* Internal use by the USB layer. */
 USBPacketState state;
 USBCombinedPacket *combined;
 QTAILQ_ENTRY(USBPacket) queue;
 QTAILQ_ENTRY(USBPacket) combined_entry;
};
 
/* definition of a USB device */
 struct USBDevice {
 DeviceState qdev;
 USBPort *port; // 指向的是uhcistate中的ports
 char *port_path;
 char *serial;
 void *opaque;
 uint32_t flags;
 
 /* Actual connected speed */
 int speed;
 /* Supported speeds, not in info because it may be variable (hostdevs) */
 int speedmask;
 uint8_t addr;
 char product_desc[32];
 int auto_attach;
 int attached;
 
 int32_t state;
 uint8_t setup_buf[8];
 uint8_t data_buf[4096]; / 0x7fffxxxx 虚拟机地址
 int32_t remote_wakeup;
 int32_t setup_state;
 int32_t setup_len;
 int32_t setup_index;
 
 USBEndpoint ep_ctl;
 USBEndpoint ep_in[USB_MAX_ENDPOINTS];
 USBEndpoint ep_out[USB_MAX_ENDPOINTS];
 
 QLIST_HEAD(, USBDescString) strings;
 const USBDesc *usb_desc; /* Overrides class usb_desc if not NULL */
 const USBDescDevice *device; / 0x5ff55xxx 物理机虚拟地址
 
 int configuration;
 int ninterfaces;
 int altsetting[USB_MAX_INTERFACES];
 const USBDescConfig *config;
 const USBDescIface *ifaces[USB_MAX_INTERFACES];
 };

#define NB_PORTS 6
struct UHCIState {
 PCIDevice dev;
 MemoryRegion io_bar;
 USBBus bus; /* Note unused when we're a companion controller */
 uint16_t cmd; /* cmd register */
 uint16_t status;
 uint16_t intr; /* interrupt enable register */
 uint16_t frnum; /* frame number */
 uint32_t fl_base_addr; /* frame list base address */
 uint8_t sof_timing;
 uint8_t status2; /* bit 0 and 1 are used to generate UHCI_STS_USBINT */
 int64_t expire_time;
 QEMUTimer *frame_timer;
 QEMUBH *bh;
 uint32_t frame_bytes;
 uint32_t frame_bandwidth;
 bool completions_only;
 UHCIPort ports[NB_PORTS];

 /* Interrupts that should be raised at the end of the current frame. */
 uint32_t pending_int_mask;

 /* Active packets */
 QTAILQ_HEAD(, UHCIQueue) queues;
 uint8_t num_ports_vmstate;

 /* Properties */
 char *masterbus;
 uint32_t firstport;
 uint32_t maxframes;
};

typedef struct UHCI_QH {
 uint32_t link;
 uint32_t el_link;
} UHCI_QH;

struct UHCIState {
 PCIDevice dev;
 MemoryRegion io_bar;
 USBBus bus; /* Note unused when we're a companion controller */
 uint16_t cmd; /* cmd register */
 uint16_t status;
 uint16_t intr; /* interrupt enable register */
 uint16_t frnum; /* frame number */
 uint32_t fl_base_addr; /* frame list base address */
 uint8_t sof_timing;
 uint8_t status2; /* bit 0 and 1 are used to generate UHCI_STS_USBINT */
 int64_t expire_time;
 QEMUTimer *frame_timer;
 QEMUBH *bh;
 uint32_t frame_bytes;
 uint32_t frame_bandwidth;
 bool completions_only;
 UHCIPort ports[NB_PORTS];

 /* Interrupts that should be raised at the end of the current frame. */
 uint32_t pending_int_mask;

 /* Active packets */
 QTAILQ_HEAD(, UHCIQueue) queues;
 uint8_t num_ports_vmstate;

 /* Properties */
 char *masterbus;
 uint32_t firstport;
 uint32_t maxframes;
};

typedef struct UHCI_TD {
 uint32_t link; // 指向另外一个TD或者QH
 uint32_t ctrl; /* see TD_CTRL_xxx */
 uint32_t token;
 uint32_t buffer;
} UHCI_TD;
/*
link:
	Vf：告知HC，该深度遍历还是广度遍历。深度遍历就是跑向Link pointer的指向的TD；广度遍历跑向Link pointer指向的另外一个QH。1=depth first；0=breadth first。

	Q：表示Link pointer指向的是TD(0)还是QH(1)。

	T：1=Link pointer无效；0=Link pointer是有效的。该bit告知HC本TD中link pointer是否指向另外一个数据流入口。如果TD在一个队列里中，该bit代表告知HC，队列中已经没有另外的有效数据流入口了。也就是说本TD是最后一个TD。
*/

struct UHCIQueue {
 uint32_t qh_addr;
 uint32_t token;
 UHCIState *uhci;
 USBEndpoint *ep;
 QTAILQ_ENTRY(UHCIQueue) next;
 QTAILQ_HEAD(, UHCIAsync) asyncs;
 int8_t valid;
};

struct UHCIAsync {
 USBPacket packet;
 uint8_t static_buf[64]; /* 64 bytes is enough, except for isoc packets */
 uint8_t *buf;
 UHCIQueue *queue;
 QTAILQ_ENTRY(UHCIAsync) next;
 uint32_t td_addr;
 uint8_t done;
};

typedef struct UHCIPort {
 USBPort port;
 uint16_t ctrl;
} UHCIPort;
```



```
#define NANOSECONDS_PER_SECOND 1000000000LL
#define FRAME_TIMER_FREQ 1000
static void uhci_port_write(void *opaque, hwaddr addr,
 uint64_t val, unsigned size)
{
 UHCIState *s = opaque;

 trace_usb_uhci_mmio_writew(addr, val);

 switch(addr) {
 case 0x00:
 if ((val & UHCI_CMD_RS) && !(s->cmd & UHCI_CMD_RS)) {
 /* start frame processing */
 trace_usb_uhci_schedule_start();
 s->expire_time = qemu_clock_get_ns(QEMU_CLOCK_VIRTUAL) +
 (NANOSECONDS_PER_SECOND / FRAME_TIMER_FREQ); // 这里的s->expire_time就是设置时钟的到期时间，这里时间单位为ns
 timer_mod(s->frame_timer, s->expire_time); // 主要是在这里，s->frame_timer回调函数
 s->status &= ~UHCI_STS_HCHALTED;
 } else if (!(val & UHCI_CMD_RS)) {
 s->status |= UHCI_STS_HCHALTED;
 }
 ......
 }
 ......
}

// s->frame_timer = timer_new_ns(QEMU_CLOCK_VIRTUAL, uhci_frame_timer, s);

// 这里是设定一个定时器
void timer_mod(QEMUTimer *ts, int64_t expire_time)
{
 timer_mod_ns(ts, expire_time * ts->scale);
}

// 第一个参数为定时器对象，第二个参数则为到期时间
// timer_mod_ns 首先从所属的QEMUTimer删除定时器，然后再调用timer_mod_ns_locked添加定时器
void timer_mod_ns(QEMUTimer *ts, int64_t expire_time)
{
 QEMUTimerList *timer_list = ts->timer_list;
 bool rearm;

 qemu_mutex_lock(&timer_list->active_timers_lock);
 timer_del_locked(timer_list, ts);
 rearm = timer_mod_ns_locked(timer_list, ts, expire_time); 
 qemu_mutex_unlock(&timer_list->active_timers_lock);

 if (rearm) {
 timerlist_rearm(timer_list);
 }
}

static bool timer_mod_ns_locked(QEMUTimerList *timer_list,
 QEMUTimer *ts, int64_t expire_time)
{
 QEMUTimer **pt, *t;

 /* add the timer in the sorted list */
 pt = &timer_list->active_timers;
 for (;;) {
 t = *pt;
 if (!timer_expired_ns(t, expire_time)) {
 break;
 }
 pt = &t->next;
 }
 ts->expire_time = MAX(expire_time, 0); // 此处
 ts->next = *pt;
 atomic_set(pt, ts);

 return pt == &timer_list->active_timers;
}

static void uhci_frame_timer(void *opaque)
{
 ......
 for (i = 0; i < frames; i++) {
 s->frame_bytes = 0;
 trace_usb_uhci_frame_start(s->frnum);
 uhci_async_validate_begin(s);
 uhci_process_frame(s); // 这里发包
 uhci_async_validate_end(s);
 /* The spec says frnum is the frame currently being processed, and
 * the guest must look at frnum - 1 on interrupt, so inc frnum now */
 s->frnum = (s->frnum + 1) & 0x7ff;
 s->expire_time += frame_t;
 }
 ......
 timer_mod(s->frame_timer, t_now + frame_t); // 这里重新设定到期时间
}
```



```
static void uhci_process_frame(UHCIState *s)
{
 ......
 uint32_t frame_addr, link, old_td_ctrl, val, int_mask;
 uint32_t curr_qh, td_count = 0;
 int cnt, ret;
 UHCI_TD td;
 UHCI_QH qh;
 QhDb qhdb;

 frame_addr = s->fl_base_addr + ((s->frnum & 0x3ff) << 2);

 pci_dma_read(&s->dev, frame_addr, &link, 4);
 le32_to_cpus(&link);
 ......
}
```



```
static void do_token_setup(USBDevice *s, USBPacket *p)
{
 int request, value, index;

 if (p->iov.size != 8) {
 p->status = USB_RET_STALL;
 return;
 }
 ......
}
```



```
static int uhci_handle_td(UHCIState *s, UHCIQueue *q, uint32_t qh_addr,
 UHCI_TD *td, uint32_t td_addr, uint32_t *int_mask)
{
	......
	max_len = ((td->token >> 21) + 1) & 0x7ff; // 这里的max_len，td->token可控
 spd = (pid == USB_TOKEN_IN && (td->ctrl & TD_CTRL_SPD) != 0);
 usb_packet_setup(&async->packet, pid, q->ep, 0, td_addr, spd,
 (td->ctrl & TD_CTRL_IOC) != 0);
 if (max_len <= sizeof(async->static_buf)) {
 async->buf = async->static_buf;
 } else {
 async->buf = g_malloc(max_len);
 }
 usb_packet_addbuf(&async->packet, async->buf, max_len); // 以及这里的usb_packet_addbuf函数
 ......
}

void usb_packet_addbuf(USBPacket *p, void *ptr, size_t len)
{
 qemu_iovec_add(&p->iov, ptr, len);
}

void qemu_iovec_add(QEMUIOVector *qiov, void *base, size_t len)
{
 assert(qiov->nalloc != -1);

 if (qiov->niov == qiov->nalloc) {
 qiov->nalloc = 2 * qiov->nalloc + 1;
 qiov->iov = g_renew(struct iovec, qiov->iov, qiov->nalloc);
 }
 qiov->iov[qiov->niov].iov_base = base;
 qiov->iov[qiov->niov].iov_len = len;
 qiov->size += len; // 可以看到，这里对其进行了赋值
 ++qiov->niov;
}
```



```
static void do_token_out(USBDevice *s, USBPacket *p)
{
 ......
 case SETUP_STATE_DATA:
 if (!(s->setup_buf[0] & USB_DIR_IN)) {
 int len = s->setup_len - s->setup_index;
 if (len > p->iov.size) {
 len = p->iov.size;
 }
 usb_packet_copy(p, s->data_buf + s->setup_index, len); // 这里
 s->setup_index += len;
 if (s->setup_index >= s->setup_len) {
 s->setup_state = SETUP_STATE_ACK;
 }
 return;
 }
 ......
}

void usb_packet_copy(USBPacket *p, void *ptr, size_t bytes)
{
 ......
 switch (p->pid) {
 case USB_TOKEN_SETUP:
 case USB_TOKEN_OUT: (0xe1)
 iov_to_buf(iov->iov, iov->niov, p->actual_length, ptr, bytes); // 这里
 break;
 ......
}
 
static inline size_t
iov_to_buf(const struct iovec *iov, const unsigned int iov_cnt,
 size_t offset, void *buf, size_t bytes)
{
 if (__builtin_constant_p(bytes) && iov_cnt &&
 offset <= iov[0].iov_len && bytes <= iov[0].iov_len - offset) {
 memcpy(buf, iov[0].iov_base + offset, bytes);
 return bytes;
 } else {
 return iov_to_buf_full(iov, iov_cnt, offset, buf, bytes);
 }
}
 
size_t iov_to_buf_full(const struct iovec *iov, const unsigned int iov_cnt,
 size_t offset, void *buf, size_t bytes)
{
 size_t done;
 unsigned int i;
 for (i = 0, done = 0; (offset || done < bytes) && i < iov_cnt; i++) {
 if (offset < iov[i].iov_len) {
 size_t len = MIN(iov[i].iov_len - offset, bytes - done);
 memcpy(buf + done, iov[i].iov_base + offset, len);
 done += len;
 offset = 0;
 } else {
 offset -= iov[i].iov_len;
 }
 }
 assert(offset == 0);
 return done;
}
```



```
void usb_packet_copy(USBPacket *p, void *ptr, size_t bytes)
{
 QEMUIOVector *iov = p->combined ? &p->combined->iov : &p->iov; // 注意这里的iov
 ......
 case USB_TOKEN_OUT:
 iov_to_buf(iov->iov, iov->niov, p->actual_length, ptr, bytes); 
 break;
 ....
}

static inline size_t
iov_to_buf(const struct iovec *iov, const unsigned int iov_cnt,
 size_t offset, void *buf, size_t bytes)
{
 if (__builtin_constant_p(bytes) && iov_cnt &&
 offset <= iov[0].iov_len && bytes <= iov[0].iov_len - offset) {
 memcpy(buf, iov[0].iov_base + offset, bytes);
 return bytes;
 } else {
 return iov_to_buf_full(iov, iov_cnt, offset, buf, bytes);
 }
}

size_t iov_to_buf_full(const struct iovec *iov, const unsigned int iov_cnt,
 size_t offset, void *buf, size_t bytes)
{
 ......
	memcpy(buf + done, iov[i].iov_base + offset, len);
 ......
}
```



```
/usb/hcd-uhci.c:891
pci_dma_read(&s->dev, td->buffer, async->buf, max_len); // 同样，此处的max_len也收到限制，最大为0x7ff，且每次copy的td->buffer都是一个起始地址
```



```
pwndbg> p &async->buf
$40 = (uint8_t **) 0x555557046788

pwndbg> p &(*async->buf)
$43 = (uint8_t *) 0x555556a2b400 ""

pwndbg> p *async->packet->iov->iov
$47 = {
 iov_base = 0x555556a2b400, 
 iov_len = 1029
}
```



```
// util/qemu-timer.c
struct QEMUTimerList {
 QEMUClock *clock;
 QemuMutex active_timers_lock;
 QEMUTimer *active_timers;
 QLIST_ENTRY(QEMUTimerList) list;
 QEMUTimerListNotifyCB *notify_cb;
 void *notify_opaque;

 /* lightweight method to mark the end of timerlist's running */
 QemuEvent timers_done_ev;
};

// include/qemu/timer.h
struct QEMUTimer {
 int64_t expire_time; /* in nanoseconds */
 QEMUTimerList *timer_list;
 QEMUTimerCB *cb; // 函数指针
 void *opaque; // 参数
 QEMUTimer *next;
 int attributes;
 int scale;
};
```



```
► f 0 557e590fa1a0 usb_hid_handle_control
 f 1 557e590d3ed7 usb_device_handle_control+151
 f 2 557e590d0f49 do_token_in+280
 f 3 557e590d165b usb_process_one+168
 f 4 557e590d1859 usb_handle_packet+335
 f 5 557e590dc76c uhci_handle_td+1285
 f 6 557e590dcd6c uhci_process_frame+674
 f 7 557e590dd18a uhci_frame_timer+407
```



```
static void usb_hid_handle_control(USBDevice *dev, USBPacket *p,
 int request, int value, int index, int length, uint8_t *data)
{
 USBHIDState *us = USB_HID(dev);
 HIDState *hs = &us->hid;
 int ret;
 ......
 case HID_SET_IDLE:
 hs->idle = (uint8_t) (value >> 8);
 hid_set_next_idle(hs);
 if (hs->kind == HID_MOUSE || hs->kind == HID_TABLET) {
 hid_pointer_activate(hs);
 }
 break;
 default:
 fail:
 p->status = USB_RET_STALL;
 break;
 }
}

void hid_set_next_idle(HIDState *hs)
{
 if (hs->idle) {
 uint64_t expire_time = qemu_clock_get_ns(QEMU_CLOCK_VIRTUAL) +
 NANOSECONDS_PER_SECOND * hs->idle * 4 / 1000;
 if (!hs->idle_timer) {
 hs->idle_timer = timer_new_ns(QEMU_CLOCK_VIRTUAL, hid_idle_timer, hs);
 }
 timer_mod_ns(hs->idle_timer, expire_time);
 } else {
 hid_del_idle_timer(hs);
 }
}

static void hid_idle_timer(void *opaque)
{
 HIDState *hs = opaque;

 hs->idle_pending = true;
 hs->event(hs); // 这里
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/02/9-1645925655.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/02/7-1645925655.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/02/0-1645925655.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/02/1-1645925655.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/02/0-1645925655.jpeg)