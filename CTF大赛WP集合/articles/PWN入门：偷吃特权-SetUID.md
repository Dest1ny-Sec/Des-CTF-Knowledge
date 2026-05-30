# PWN入门：偷吃特权-SetUID

> 原文: https://www.ctfiot.com/219247.html
> ID: 219247

01.

初探特权程序

struct cred {
 ......
 kuid_t uid; /* real UID of the task */
 kgid_t gid; /* real GID of the task */
 kuid_t suid; /* saved UID of the task */
 kgid_t sgid; /* saved GID of the task */
 kuid_t euid; /* effective UID of the task */
 kgid_t egid; /* effective GID of the task */
 kuid_t fsuid; /* UID for VFS ops */
 kgid_t fsgid; /* GID for VFS ops */
 ......
}

ls -lh /etc/ld.so.conf
-rw-r--r-- 1 root root 34 Apr 10 2024 /etc/ld.so.conf
| directory | owner | group | other |
| - | rw- | r-- | r-- |

ls -lh /etc/ld.so.conf
-rw-r--r-- 1 root root 34 Apr 10 2024 /etc/ld.so.conf
| | owner | group | other |
| d | rwx | rwx | rwx |

d：是否为目录
r：读权限
w：写权限
x：可执行权限 / s：Set-UID程序

statx(AT_FDCWD, "./Templates", ...)
lgetxattr("./Templates", "security.selinux", 0x55e9c62ab530, 255) = -1 ENODATA (No data available)
getxattr("./Templates", "system.posix_acl_access", NULL, 0) = -1 ENODATA (No data available)
getxattr("./Templates", "system.posix_acl_default", NULL, 0) = -1 ENODATA (No data available)

对应的系统调用号
#define __NR_statx 332
#define __NR_getxattr 191
#define __NR_lgetxattr 192
#define __NR_fgetxattr 193

do_new_mount
 -> fs_context_for_mount
 -> alloc_fs_context
 -> fs_context->file_system_type->init_fs_context
 -> fs_context->fs_context_operations = xxx

fs_context
 -> cred

do_new_mount
 -> fs_context_for_mount
 -> alloc_fs_context
 -> fs_context->cred = get_current_cred
 -> current->cred

current是内核记录当前进程的变量

fs_context
 -> const struct fs_context_operations *ops;
fs_context_operations
 -> get_tree

do_new_mount
 -> vfs_get_tree
 -> fs_context->ops->get_tree
 -> get_tree_nodev(fs_context, xxx)
 -> xxx

do_new_mount
 -> vfs_get_tree
 -> super_struct sb = fs_context->root->d_sb;

私有超级块：
fs_context
 -> s_fs_info
super_block
 -> s_fs_info

struct super_block {
 ......
 unsigned long s_flags;
 unsigned long s_iflags;
 ......
}

/* sb->s_flags */
#define SB_RDONLY BIT(0)	/* Mount read-only */
#define SB_NOSUID BIT(1)	/* Ignore suid and sgid bits */
......
#define SB_NOUSER BIT(31)

/* sb->s_iflags */
#define SB_I_CGROUPWB	0x00000001	/* cgroup-aware writeback enabled */
#define SB_I_NOEXEC	0x00000002	/* Ignore executables on this fs */
......
#define SB_I_RETIRED	0x00000800	/* superblock shouldn't be reused */

static inline bool sb_rdonly(const struct super_block *sb) { return sb->s_flags & SB_RDONLY; }

static int sb_permission(struct super_block *sb, struct inode *inode, int mask)
{
 if (unlikely(mask & MAY_WRITE)) {
 umode_t mode = inode->i_mode;

 /* Nobody gets write access to a read-only fs. */
 if (sb_rdonly(sb) && (S_ISREG(mode) || S_ISDIR(mode) || S_ISLNK(mode)))
 return -EROFS;
 }
 return 0;
}

super_block
 -> struct dentry* s_root;
 -> struct inode *d_inode;

struct task_struct
 ->	struct files_struct files
 ->	struct file __rcu * fd_array[NR_OPEN_DEFAULT];

文件类型：
套接字 #define S_IFSOCK 0140000
软链接文件 #define S_IFLNK 0120000
普通文件 #define S_IFREG 0100000
块设备 #define S_IFBLK 0060000
目录 #define S_IFDIR 0040000
字符设备 #define S_IFCHR 0020000
管道设备 #define S_IFIFO 0010000
特权用户程序	#define S_ISUID 0004000

访问权限：
#define S_IRWXU 00700
#define S_IRUSR 00400
......
#define S_IWOTH 00002
#define S_IXOTH 00001

struct inode {
 umode_t i_mode;
 unsigned short i_opflags;
 kuid_t i_uid;
 kgid_t i_gid;
 ......
 i_ino
 ......
}

ls -lh /bin/sudo
-rwsr-xr-x 1 root root 276K Jun 27 2023 /bin/sudo

ls -lh /bin/ping
-rwxr-xr-x 1 root root 89K Nov 27 2022 /bin/ping

struct stask_struct {
 ......
 const struct cred __rcu *ptracer_cred;
 const struct cred __rcu *real_cred;
 const struct cred __rcu *cred;
 ......
}

sysycall execve
 -> do_execve
 -> do_execveat_common
 -> bprm_execve
 |-> prepare_bprm_creds
 |-> exec_binprm
 -> search_binary_handler
 -> load_binary

prepare_exec_creds
 -> prepare_exec_creds
 -> prepare_creds
 |-> struct task_struct *task = current;
 |-> old = task->cred;
 |-> memcpy(new, old, sizeof(struct cred));

list_for_each_entry(fmt, &formats, lh) {
 if (!try_module_get(fmt->module))
 continue;
 read_unlock(&binfmt_lock);

 retval = fmt->load_binary(bprm);

 read_lock(&binfmt_lock);
 put_binfmt(fmt);
 if (bprm->point_of_no_return || (retval != -ENOEXEC)) {
 read_unlock(&binfmt_lock);
 return retval;
 }
}

static struct linux_binfmt elf_format = {
 .module = THIS_MODULE,
 .load_binary	= load_elf_binary,
 .load_shlib	= load_elf_library,
#ifdef CONFIG_COREDUMP
 .core_dump	= elf_core_dump,
 .min_coredump	= ELF_EXEC_PAGESIZE,
#endif
};

load_elf_binary
 -> begin_new_exec
 -> bprm_creds_from_file
 |-> bprm_fill_uid
 |-> security_bprm_creds_from_file

bprm_fill_uid (...) {
 ......
 uid = i_uid_into_mnt(mnt_userns, inode);
 gid = i_gid_into_mnt(mnt_userns, inode);
 ......
 if (mode & S_ISUID) {
 bprm->per_clear |= PER_CLEAR_ON_SETID;
 bprm->cred->euid = uid;
 }

 if ((mode & (S_ISGID | S_IXGRP)) == (S_ISGID | S_IXGRP)) {
 bprm->per_clear |= PER_CLEAR_ON_SETID;
 bprm->cred->egid = gid;
 }
 ......
}

security_bprm_creds_from_file
 -> cap_bprm_creds_from_file
 |-> new->suid = new->fsuid = new->euid;
 |->	new->sgid = new->fsgid = new->egid;

begin_new_exec
 -> commit_creds

02.

示例讲解

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

void vuln_by_user_input(const char* input)
{
 char cmd[0x100];

 snprintf(cmd, 0x100, "echo %s", input);
 system(cmd);
}

void vuln_by_permission_leak(void)
{
 int my_fd;

 printf("will get passwordn");

 my_fd = open("./private_data.bin", O_RDWR | O_APPEND);
 if (my_fd > 0) {
 printf("get fd num %dn", my_fd);
 }
 else {
 printf("open file failed [errno %d], will exit.n", errno);

 return;
 }

 system("/bin/sh");
}

int main(int argc, char** argv)
{
 switch (argc) {
 case 1:
 vuln_by_permission_leak();
 break;
 case 2:
 vuln_by_user_input(argv[1]);
 break;
 default:
 break;
 }

 return 0;
}

chown root:root ./private_data.bin
chmod 600 ./private_data.bin

chown root:root ./set_uid_example
chmod 4755 ./set_uid_example

-rw------- 1 root root 8 Nov 8 08:13 private_data.bin
-rwsr-xr-x 1 root root 18K Nov 8 08:49 set_uid_example

execl("/bin/sh", "sh", "-c", command, (char *) NULL);

./set_uid_example "233333 ; /bin/sh"
233333
$ exit

./set_uid_example "233333 && /bin/sh"
233333
$ exit

cat private_data.bin 
cat: private_data.bin: Permission denied

./set_uid_example 
will get password
get fd num 3
$ echo "CCCCC" >& 3
$ exit

sudo cat private_data.bin 
12345678CCCCC

看雪ID：福建炒饭乡会

https://bbs.kanxue.com/user-home-1000123.htm

*本文为看雪论坛优秀文章，由 福建炒饭乡会 原创，转载请注明来自看雪社区

# 往期推荐

1、PWN入门-SROP拜师

2、一种apc注入型的Gamarue病毒的变种

3、野蛮fuzz：提升性能

4、关于安卓注入几种方式的讨论，开源注入模块实现

5、2024年KCTF水泊梁山-反混淆

球分享

球点赞

球在看

点击阅读原文查看更多


```
struct cred {
 ......
 kuid_t uid; /* real UID of the task */
 kgid_t gid; /* real GID of the task */
 kuid_t suid; /* saved UID of the task */
 kgid_t sgid; /* saved GID of the task */
 kuid_t euid; /* effective UID of the task */
 kgid_t egid; /* effective GID of the task */
 kuid_t fsuid; /* UID for VFS ops */
 kgid_t fsgid; /* GID for VFS ops */
 ......
}
```



```
ls -lh /etc/ld.so.conf
-rw-r--r-- 1 root root 34 Apr 10 2024 /etc/ld.so.conf
| directory | owner | group | other |
| - | rw- | r-- | r-- |
```



```
ls -lh /etc/ld.so.conf
-rw-r--r-- 1 root root 34 Apr 10 2024 /etc/ld.so.conf
| | owner | group | other |
| d | rwx | rwx | rwx |

d：是否为目录
r：读权限
w：写权限
x：可执行权限 / s：Set-UID程序
```



```
statx(AT_FDCWD, "./Templates", ...)
lgetxattr("./Templates", "security.selinux", 0x55e9c62ab530, 255) = -1 ENODATA (No data available)
getxattr("./Templates", "system.posix_acl_access", NULL, 0) = -1 ENODATA (No data available)
getxattr("./Templates", "system.posix_acl_default", NULL, 0) = -1 ENODATA (No data available)

对应的系统调用号
#define __NR_statx 332
#define __NR_getxattr 191
#define __NR_lgetxattr 192
#define __NR_fgetxattr 193
```



```
do_new_mount
 -> fs_context_for_mount
 -> alloc_fs_context
 -> fs_context->file_system_type->init_fs_context
 -> fs_context->fs_context_operations = xxx
```



```
fs_context
 -> cred

do_new_mount
 -> fs_context_for_mount
 -> alloc_fs_context
 -> fs_context->cred = get_current_cred
 -> current->cred

current是内核记录当前进程的变量
```



```
fs_context
 -> const struct fs_context_operations *ops;
fs_context_operations
 -> get_tree

do_new_mount
 -> vfs_get_tree
 -> fs_context->ops->get_tree
 -> get_tree_nodev(fs_context, xxx)
 -> xxx
```



```
do_new_mount
 -> vfs_get_tree
 -> super_struct sb = fs_context->root->d_sb;

私有超级块：
fs_context
 -> s_fs_info
super_block
 -> s_fs_info
```



```
struct super_block {
 ......
 unsigned long s_flags;
 unsigned long s_iflags;
 ......
}

/* sb->s_flags */
#define SB_RDONLY BIT(0)	/* Mount read-only */
#define SB_NOSUID BIT(1)	/* Ignore suid and sgid bits */
......
#define SB_NOUSER BIT(31)

/* sb->s_iflags */
#define SB_I_CGROUPWB	0x00000001	/* cgroup-aware writeback enabled */
#define SB_I_NOEXEC	0x00000002	/* Ignore executables on this fs */
......
#define SB_I_RETIRED	0x00000800	/* superblock shouldn't be reused */
```



```
static inline bool sb_rdonly(const struct super_block *sb) { return sb->s_flags & SB_RDONLY; }

static int sb_permission(struct super_block *sb, struct inode *inode, int mask)
{
 if (unlikely(mask & MAY_WRITE)) {
 umode_t mode = inode->i_mode;

 /* Nobody gets write access to a read-only fs. */
 if (sb_rdonly(sb) && (S_ISREG(mode) || S_ISDIR(mode) || S_ISLNK(mode)))
 return -EROFS;
 }
 return 0;
}
```



```
super_block
 -> struct dentry* s_root;
 -> struct inode *d_inode;
```



```
struct task_struct
 ->	struct files_struct files
 ->	struct file __rcu * fd_array[NR_OPEN_DEFAULT];
```



```
文件类型：
套接字 #define S_IFSOCK 0140000
软链接文件 #define S_IFLNK 0120000
普通文件 #define S_IFREG 0100000
块设备 #define S_IFBLK 0060000
目录 #define S_IFDIR 0040000
字符设备 #define S_IFCHR 0020000
管道设备 #define S_IFIFO 0010000
特权用户程序	#define S_ISUID 0004000

访问权限：
#define S_IRWXU 00700
#define S_IRUSR 00400
......
#define S_IWOTH 00002
#define S_IXOTH 00001

struct inode {
 umode_t i_mode;
 unsigned short i_opflags;
 kuid_t i_uid;
 kgid_t i_gid;
 ......
 i_ino
 ......
}
```



```
ls -lh /bin/sudo
-rwsr-xr-x 1 root root 276K Jun 27 2023 /bin/sudo

ls -lh /bin/ping
-rwxr-xr-x 1 root root 89K Nov 27 2022 /bin/ping
```



```
struct stask_struct {
 ......
 const struct cred __rcu *ptracer_cred;
 const struct cred __rcu *real_cred;
 const struct cred __rcu *cred;
 ......
}
```



```
sysycall execve
 -> do_execve
 -> do_execveat_common
 -> bprm_execve
 |-> prepare_bprm_creds
 |-> exec_binprm
 -> search_binary_handler
 -> load_binary

prepare_exec_creds
 -> prepare_exec_creds
 -> prepare_creds
 |-> struct task_struct *task = current;
 |-> old = task->cred;
 |-> memcpy(new, old, sizeof(struct cred));
```



```
list_for_each_entry(fmt, &formats, lh) {
 if (!try_module_get(fmt->module))
 continue;
 read_unlock(&binfmt_lock);

 retval = fmt->load_binary(bprm);

 read_lock(&binfmt_lock);
 put_binfmt(fmt);
 if (bprm->point_of_no_return || (retval != -ENOEXEC)) {
 read_unlock(&binfmt_lock);
 return retval;
 }
}
```



```
static struct linux_binfmt elf_format = {
 .module = THIS_MODULE,
 .load_binary	= load_elf_binary,
 .load_shlib	= load_elf_library,
#ifdef CONFIG_COREDUMP
 .core_dump	= elf_core_dump,
 .min_coredump	= ELF_EXEC_PAGESIZE,
#endif
};

load_elf_binary
 -> begin_new_exec
 -> bprm_creds_from_file
 |-> bprm_fill_uid
 |-> security_bprm_creds_from_file

bprm_fill_uid (...) {
 ......
 uid = i_uid_into_mnt(mnt_userns, inode);
 gid = i_gid_into_mnt(mnt_userns, inode);
 ......
 if (mode & S_ISUID) {
 bprm->per_clear |= PER_CLEAR_ON_SETID;
 bprm->cred->euid = uid;
 }

 if ((mode & (S_ISGID | S_IXGRP)) == (S_ISGID | S_IXGRP)) {
 bprm->per_clear |= PER_CLEAR_ON_SETID;
 bprm->cred->egid = gid;
 }
 ......
}
```



```
security_bprm_creds_from_file
 -> cap_bprm_creds_from_file
 |-> new->suid = new->fsuid = new->euid;
 |->	new->sgid = new->fsgid = new->egid;
```



```
begin_new_exec
 -> commit_creds
```



```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

void vuln_by_user_input(const char* input)
{
 char cmd[0x100];

 snprintf(cmd, 0x100, "echo %s", input);
 system(cmd);
}

void vuln_by_permission_leak(void)
{
 int my_fd;

 printf("will get passwordn");

 my_fd = open("./private_data.bin", O_RDWR | O_APPEND);
 if (my_fd > 0) {
 printf("get fd num %dn", my_fd);
 }
 else {
 printf("open file failed [errno %d], will exit.n", errno);

 return;
 }

 system("/bin/sh");
}

int main(int argc, char** argv)
{
 switch (argc) {
 case 1:
 vuln_by_permission_leak();
 break;
 case 2:
 vuln_by_user_input(argv[1]);
 break;
 default:
 break;
 }

 return 0;
}
```



```
chown root:root ./private_data.bin
chmod 600 ./private_data.bin

chown root:root ./set_uid_example
chmod 4755 ./set_uid_example
```



```
-rw------- 1 root root 8 Nov 8 08:13 private_data.bin
-rwsr-xr-x 1 root root 18K Nov 8 08:49 set_uid_example
```



```
execl("/bin/sh", "sh", "-c", command, (char *) NULL);
```



```
./set_uid_example "233333 ; /bin/sh"
233333
$ exit

./set_uid_example "233333 && /bin/sh"
233333
$ exit
```



```
cat private_data.bin 
cat: private_data.bin: Permission denied
```



```
./set_uid_example 
will get password
get fd num 3
$ echo "CCCCC" >& 3
$ exit
```



```
sudo cat private_data.bin 
12345678CCCCC
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/1-1733843090.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/7-1733843092.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/9-1733843092.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/3-1733843094.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/0-1733843094.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1733843095.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1733843096.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/4-1733843098.gif)