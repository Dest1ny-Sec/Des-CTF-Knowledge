# PBCTF2021中有意思的ARM CPU题

> 原文: https://www.ctfiot.com/10901.html
> ID: 10901

本篇文章由ChaMd5安全团IOT小组投稿

之前PBCTF2021，OutOfOrder这道题没有做出来，是一道关于ARM CPU的条件竞争的题目，赛后按照出题人的Writeup学习了一下，写一下其中感觉有意思的地方。

CPU的乱序执行

CPU并不关心你给它提供指令的顺序，但更关心这些指令之间的数据依赖关系。

1. add rax, rax ; rax += rax
2. add rax, rax ; rax += rax
3. add rax, rax ; rax += rax
4. add rax, rax ; rax += rax
5. add rbx, rax ; rbx += rax
6. add rcx, rdx ; rcx += rdx

比如上面这几条指令，CPU执行的时候第6条指令和前面的指令并没有数据依赖关系，所以第6条指令执行的顺序并不一定是最后。

获取语义和释放语义

一般来说，获取语义意味着该操作需要发生在其他操作之前，释放语义意味着该操作需要发生在其他操作之后。如何理解呢？用一个无锁编程的例子来说明：

// Thread 1
value = 123; // (1)
ready = 1; // (2)

// Thread 2
while (!ready); // (3)
print(value); // (4)

线程1首先给value变量赋值，然后将ready变量赋值为1。线程2判断ready变量的值，如果为零，则阻塞，如果非零，则打印value变量的值。那么(2)就必须是释放语义，其必须在其他操作之后才能进行。同理，(3)则是获取语义。否则，如果(2)指令在(1)指令之前执行，那么线程2执行的时候，变量value还并没有赋值，就会出现非预期。获取语义和释放语义就是用来保证CPU不会进行乱序执行。

volatile关键词

CPU的不同核在运行代码的时候，因为内存的读写速度小于CPU的运算速度，所以每个核都具有对应的高速缓存，对于内存的操作将在高速缓存中先进行，然后再写入内存中。C++中volatile关键词可以保证线程之间的可见性，即每次使用volatile声明的变量的值的时候，系统总是重新从它所在的内存读取数据。但是volatile关键词却并不代表着获取语义和释放语义。也就是说尽管使用了volatile关键词，也可能存在CPU乱序执行。

X86架构的CPU上，内存模型非常强大，以至于存储是完全有序的——所有存储都有一个单一的全局排序。但是ARM的内存模型较弱，他只关心数据依赖关系，其余的几乎任何操作都可以乱序执行。所以ARM上的无锁编程如果没有获取语义和释放语义就会存在条件竞争的问题。

回到题目

题目简单来说，存在两个进程，一个进程是生产者进程，一个是消费者进程。存在两个队列，一个是wq队列，生产者进程提出需求之后就写入这个队列，一个是rq队列，消费者进程从wq队列中读取需求之后，计算结果，然后写入rq队列，我们主要关注wq队列。生产者进程主要是生产需求，对于生产者进程主要关注的代码如下：

// New request
case 1: {
 puts("How many requests in this job?");
 unsigned int count = get_number();
 if (count > 100000) {
 puts("Too many!");
 exit(1);
 }
 for (unsigned int i = 0; i < count; i++) {
 if (!fgets_unlocked(buf, sizeof(buf), stdin))
 exit(0);

 wq.write(new Request{buf, 0}, wq_head);
 }
 break;
}

消费者部分的代码非常简单，就是一直从wq队列中读取需求。

void* thread_consumer(void* arg)
{
 uint64_t i = 0;
 unsigned int wq_tail = 0;
 unsigned int rq_head = 0;

 while (1) {
 auto data = wq.read(wq_tail);
 data->result = strlen(data->str);
 rq.write(std::
unique_ptr<Request>(data), rq_head);
 }
}

wq队列的长度为256,head和tail变量被声明为volatile。

volatile unsigned int head = 0;
volatile unsigned int tail = 0;

write方法和read方法会首先判断队列是否满了或者是空的，根据结果阻塞。

// Reader-side functions
bool empty(const unsigned int& tail_local) const
{
	return head == tail_local;
}

T read(unsigned int& tail_local)
{
	while (empty(tail_local)); // Buffer is empty, block.

	T data = std::
move(backing_buf[tail_local]);
	tail_local = (tail_local + 1) % buffer_size;
	tail = tail_local;
	return std::
move(data);
}

// Writer-side functions
bool full(const unsigned int& head_local) const
{
	return (head_local + 1) % buffer_size == tail;
}

void write(T data, unsigned int& head_local)
{
	while (full(head_local)); // Buffer is full, block.

	backing_buf[head_local] = std::
move(data);
	head_local = (head_local + 1) % buffer_size;
	head = head_local;
}

根据先前讲述的内容，write方法中的head = head_local需要是释放语义，但是代码中没有任何措施来强制保证。下面是反编译的结果，可以看到wq队列缓冲区的赋值和head变量赋值之间并没有数据依赖关系。

此处的反汇编代码也可以看出，并没有强制措施来保证释放语义。

也就是说存在一种情况，在循环使用缓冲区一圈之后，生产者队列中，由于CPU乱序执行，head变量的更新可能早于wq队列缓冲区的赋值,在消费者队列中，由于head变量的更新，wq队列不再是空，就从中取出一个需求，而这个需求则是缓冲区一圈之前的需求。那么就会造成两个指针指向同一个对象的情况出现。后面的利用部分就是一些堆利用，就不再赘述。

实验验证

正好手头上有一个树莓派，就用writeup上的验证代码验证一下上述的论述是否成立，提出20000个请求，每个请求标识递增，验证结果如下：

可以看到第2189个需求返回的标识是1933,差值正好是256也就是返回了一圈缓冲区前的那个需求。

出题人writeup链接：

https://github.com/stong/how-to-exploit-a-double-free#user-content-fnref-1-bbe0f5bfb1d8a04c72117e62b182e4d6

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析+AI 长期招新

欢迎联系admin@chamd5.org


```
1. add rax, rax ; rax += rax
2. add rax, rax ; rax += rax
3. add rax, rax ; rax += rax
4. add rax, rax ; rax += rax
5. add rbx, rax ; rbx += rax
6. add rcx, rdx ; rcx += rdx
// Thread 1
value = 123; // (1)
ready = 1; // (2)

// Thread 2
while (!ready); // (3)
print(value); // (4)
// New request
case 1: {
 puts("How many requests in this job?");
 unsigned int count = get_number();
 if (count > 100000) {
 puts("Too many!");
 exit(1);
 }
 for (unsigned int i = 0; i < count; i++) {
 if (!fgets_unlocked(buf, sizeof(buf), stdin))
 exit(0);

 wq.write(new Request{buf, 0}, wq_head);
 }
 break;
}
void* thread_consumer(void* arg)
{
 uint64_t i = 0;
 unsigned int wq_tail = 0;
 unsigned int rq_head = 0;

 while (1) {
 auto data = wq.read(wq_tail);
 data->result = strlen(data->str);
 rq.write(std::
unique_ptr<Request>(data), rq_head);
 }
}
volatile unsigned int head = 0;
volatile unsigned int tail = 0;
// Reader-side functions
bool empty(const unsigned int& tail_local) const
{
	return head == tail_local;
}

T read(unsigned int& tail_local)
{
	while (empty(tail_local)); // Buffer is empty, block.

	T data = std::
move(backing_buf[tail_local]);
	tail_local = (tail_local + 1) % buffer_size;
	tail = tail_local;
	return std::
move(data);
}

// Writer-side functions
bool full(const unsigned int& head_local) const
{
	return (head_local + 1) % buffer_size == tail;
}

void write(T data, unsigned int& head_local)
{
	while (full(head_local)); // Buffer is full, block.

	backing_buf[head_local] = std::
move(data);
	head_local = (head_local + 1) % buffer_size;
	head = head_local;
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/0-1637122177.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/9-1637122177.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/8-1637122177.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/9-1637122177-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/2-1637122178.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/3-1637122178.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/11/2-1637122179.jpeg)