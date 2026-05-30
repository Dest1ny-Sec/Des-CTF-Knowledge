`Dirsearch` 是一个用 Python 编写的目录和文件爆破工具，广泛用于网站安全测试中以发现隐藏的目录和文件。它非常适合用于渗透测试和漏洞扫描。以下是 `Dirsearch` 的详细使用说明，包括安装、配置和基本用法。

### 1. **安装 Dirsearch**

#### 1.1 克隆 GitHub 仓库

```bash
bash

 代码解读
复制代码git clone https://github.com/maurosoria/dirsearch.git
```

#### 1.2 安装依赖

`Dirsearch` 依赖于 `requests` 库，你需要安装它。进入 `dirsearch` 目录并使用 `pip` 安装依赖：

```bash
bash 代码解读复制代码cd dirsearch
pip install -r requirements.txt
```

### 2. **基本使用**

#### 2.1 运行 Dirsearch

`Dirsearch` 的基本运行命令如下：

```bash
bash

 代码解读
复制代码python3 dirsearch.py -u <URL>
```

- `-u <URL>`：目标 URL。确保以 `http://` 或 `https://` 开头。

#### 2.2 常用选项

- `-u`：指定要扫描的目标 URL。
- `-e`：指定要扫描的文件扩展名，多个扩展名用逗号分隔（例如：`-e php,html,js`）。
- `-w`：指定自定义字典文件路径。默认情况下，`Dirsearch` 使用内置字典。
- `-t`：设置并发线程数（默认 10），提高扫描速度（例如：`-t 20`）。
- `-x`：排除某些 HTTP 状态码（例如：`-x 404,403`）。
- `-o`：指定输出文件路径，将扫描结果保存到文件中。
- `--format`：指定输出格式（`plain`、`json`、`csv`）。

#### 2.3 示例命令

1. **基本扫描**：

   ```bash
   bash
   
    代码解读
   复制代码python3 dirsearch.py -u http://example.com
   ```

2. **指定文件扩展名**：

   ```bash
   bash
   
    代码解读
   复制代码python3 dirsearch.py -u http://example.com -e php,html,js
   ```

3. **使用自定义字典**：

   ```bash
   bash
   
    代码解读
   复制代码python3 dirsearch.py -u http://example.com -w /path/to/custom/wordlist.txt
   ```

4. **设置并发线程数**：

   ```bash
   bash
   
    代码解读
   复制代码python3 dirsearch.py -u http://example.com -t 20
   ```

5. **排除特定状态码**：

   ```bash
   bash
   
    代码解读
   复制代码python3 dirsearch.py -u http://example.com -x 404,403
   ```

6. **将结果保存到文件**：

   ```bash
   bash
   
    代码解读
   复制代码python3 dirsearch.py -u http://example.com -o results.txt
   ```

7. **指定输出格式**：

   ```bash
   bash
   
    代码解读
   复制代码python3 dirsearch.py -u http://example.com --format json -o results.json
   ```

### 3. **配置和自定义**

#### 3.1 修改默认字典

`Dirsearch` 使用内置字典来进行扫描。你可以根据需要替换或修改这些字典文件。默认字典位于 `dirsearch/db/` 目录下。

1. **创建自定义字典**：你可以使用任何字典文件，只需指定 `-w` 参数即可。
2. **替换默认字典**：将新的字典文件替换 `dirsearch/db` 目录中的现有文件。

#### 3.2 配置文件

`Dirsearch` 目前没有配置文件功能，但你可以通过命令行选项配置扫描行为。如果你需要更复杂的设置，可以创建一个脚本来自动化运行命令。

### 4. **进阶用法**

#### 4.1 扫描多个目标

如果你需要对多个目标进行扫描，可以使用循环脚本。例如，使用 Bash 脚本对一组 URL 进行扫描：

```bash
bash 代码解读复制代码#!/bin/bash
for url in $(cat urls.txt); do
    python3 dirsearch.py -u "$url" -o "${url//http:\/\/}/results.txt"
done
```

#### 4.2 集成到渗透测试工具

`Dirsearch` 可以与其他安全工具（如 Burp Suite）一起使用，通常通过导出结果和结合其他扫描结果来进行综合分析。

### 5. **结果分析**

`Dirsearch` 扫描的结果通常包括：

- **发现的目录和文件**：列出找到的目录和文件路径。
- **HTTP 状态码**：显示每个路径的 HTTP 响应状态码。
- **其他信息**：包括响应时间、大小等。

#### 5.1 结果格式示例

- **文本格式**：简单的文本输出，显示发现的路径和状态码。
- **JSON 格式**：适合程序化处理和分析，可以导入到其他工具或平台进行进一步分析。
- **CSV 格式**：适合电子表格软件分析和报告生成。

### 6. **注意事项**

- **合法性**：仅在合法授权的情况下对目标进行扫描。未经授权的扫描可能违反法律和道德规范。
- **性能**：调整线程数和字典大小以平衡扫描速度和系统负载。过高的并发线程数可能导致目标服务器拒绝服务或出现 IP 封锁。
- **过滤和排除**：使用 `-x` 选项排除不需要的状态码（如 404 或 403），减少结果噪声。

### 7. **总结**

`Dirsearch` 是一个强大的目录和文件爆破工具，适合用于网站安全测试和渗透测试。通过灵活的命令行选项，你可以定制扫描过程并优化扫描结果。正确使用 `Dirsearch` 可以帮助你发现网站上的隐藏文件和目录，从而提高安全性。

作者：wsl0224
链接：https://juejin.cn/post/7401106213882527754
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。