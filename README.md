# Are You Free? (R-U-Free)

Are You Free 是一个基于`Python`的状态显示软件，可以让你的好损友快速知道你的状态（离线/在线、空闲/忙碌……也可以自定义）

## 使用方式

> [!Warning]
>
> 此项目还在开发，请稍后再来！

本软件提供两个版本：客户端`RUF-Client`和服务端`RUF-Server`，其中`RUF-Client`分为三个版本`Desktop`（桌面GUI）、`CLI`（命令行界面）和`ESP32`（嵌入式固件）。

若要安装此程序，你可从右侧Release一栏获取你需要的版本，或点此跳转最新版本→[![GitHub Release](https://img.shields.io/github/v/release/TuanZiGit/R-U-Free?sort=date&display_name=release&style=for-the-badge&logo=github&label=%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC&labelColor=blueviolet&color=blue)](https://github.com/TuanZiGit/R-U-Free/releases/latest)

### 客户端安装与配置

在上文中下载好压缩包后，我们可以开始安装并配置软件。

接下来本文将指导你完成配置。

下载好压缩包后，请将文件解压至一个目录里。本文中记为`/path/to/unzipped/data`。

<details>
	<summary>
        若您下载的是<code>RUF-Client.CLI</code>...
    </summary>
    首先，进入<code>/path/to/unzipped/data</code>，对于Linux用户，请正确配置好<code>cli.py</code>的权限为<code>-rwxr-xr-x(755)</code><br/>
    然后，使用<code>./cli.py init</code>初始化客户端（若您是第一次使用，也可直接运行<code>./cli.py</code>），它将在当前目录里创建<code>data</code>文件夹，并显示如下内容指导您进行初始化：<br/>
    <pre>[~] RUF-Client.CLI V1.0
[~] 初始化客户端中……
[~] 接下来，我们将用一个简单的向导指引您完成配置。
[~] 您也可以选择使用./cli.py init --config cli_config.json使用特定配置文件进行无人值守安装。
[?] 请设置服务器HTTP(S) API地址 > https://example.com/api
[#] API可用！
[?] 请在此配置你的令牌Token > RUF-1145141919810ABC
[#] Token有效！
[#] 下载个人配置完毕，现在为您显示可操作的命令……
[~] RUF-Client.CLI 命令帮助
[~] (省略）</pre><br/>
    初始化完毕后，可以通过使用<code>./cli.py set 状态值/ID</code>向服务器推送状态。<br/>
    更多指令可以通过<code>./cli.py help</code>获取。
</details>

<details>
	<summary>
        若您下载的是<code>RUF-Client.Desktop</code>...
    </summary>
    <code>Desktop</code>版只实现了Windows端，您可以直接双击运行<code>desktop.pyw</code>启动程序。
</details>

<details>
	<summary>
        若您下载的是<code>RUF-Client.ESP32</code>...
    </summary>
    这一版本程序适用于带有Wifi功能的ESP32，请使用Arduino IDE或支持<code>arduino-cli</code>的IDE打开<code>main.ino</code>，然后在Library Manager中导入<code>ESP8266WiFi</code>、<code>ESP8266HTTPClient</code>和<code>OneButton</code>，接着依据<code>Configure.sh</code>中的提示对<code>WiFi_SSIDs</code>、<code>WiFi_Passwords</code>、<code>Button_GPIOs</code>和<code>Button_Actions</code>四个数组、<code>RUF_Token</code>字符串以及<code>LED_GPIO</code>整数值完成配置，方可下载并运行。<br/>
    运行后，ESP32将开始按照设定的顺序在扫描到的WiFi中尝试连接，此时设定的LED灯慢闪，连接后将常亮，此时可通过设定的单击、双击和长按操作来向服务器推送状态。
</details>

## #服务端安装与配置

同理，对于服务端，我们也将其解压至一个目录里，本文中同样记为`/path/to/unzipped/data`，并配置好适当的权限（推荐：`-rwxr-xr-x(755)`。

首先，请找到`config.json`，根据下方格式进行修改：（注：若要将此文件作为模板，请删去注释，因为JSON不支持注释功能）

```json
{
    "version": 1, // 这是版本号，不要修改，用于在有格式变动时自动完成升级
    "host": "::", // 服务器运行的接口，::表示在所有IPv6和IPv4接口运行服务器
    "port": 80, // 服务器运行于TCP端口80/HTTP，可修改，范围1-65535
    "prefix": "/", // 路径前缀，适用于nginx反代（内心OS：真的有必要么）
    "next_uid": 2, // 下一个用户的UID
    "user_data": [
        { // 这是一个管理员块
            "uid": 0,
            "uid_str": "admin",
            "salt": "+cuGBWGur+oAfYRp", // 随机16位字符串，内容0-9,A-Z,a-z,+,/,=
            "password": "91f46441a65134e01cefda4c035e9b21d17193154e836c86c476d4bdf2e68167", // 密码的加盐哈希值
            "token": "f3128b575ccd4e9c312cfcb7edd3adc296be67a55c861dcbfe87ed03b5fa94bb", // Token的加盐哈希值
            "israw": false, // 通常用于人工配置，为true时服务器将自动转换password和token 注意：token为以"RUF-"加上一个八字节十六进制值
            "last_changed": -1590354886, // 最近一次状态更新时间Unix时间戳
            "status": 0, // 0离线 1空闲 2忙碌 其他参照下方自定义
            "deletion": false, // 是否要在下一次清理时删除此用户
            "admin": true, // 是否为管理员
            "custom": [
                { // 这是一个自定义状态块
                    "sorted_index": 0, // 自定义项排序索引
                    "sid_str": "extra_busy", // 状态
                    "display": "超TM忙", // 状态显示名
                    "color": "#FF0000" // 状态主颜色
                }
            ]
        },
        { // 这是一个用户块
            "uid": 1,
            "uid_str": "exampleuser",
            "salt": "u/G/oJGgymQp69U7", // 随机0-9,A-Z,a-z,+,/,=
            "password": "7f3447ba48562f103e8189622d9a82428f69e01a919551c246c2a8472e858380", // 密码的加盐哈希值
            "token": "3a343937ae19135b66d84ccfd868bc9ab9d47c25d6f8bbb21b072e59c438a5dd", // Token的加盐哈希值
            "israw": false, // 通常用于人工配置，为true时服务器将自动转换password和token 注意：token为以"RUF-"加上一个八字节十六进制值
            "last_changed": -1590354886, // 最近一次状态更新时间Unix时间戳
            "status": 0, // 0离线 1空闲 2忙碌 其他参照下方自定义
            "deletion": false, // 是否要在下一次清理时删除此用户
            "admin": false, // 是否为管理员
            "custom": [
                { // 这是一个自定义状态块
                    "sorted_index": 0, // 自定义项排序索引
                    "sid_str": "extra_busy", // 状态
                    "display": "超TM忙", // 状态显示名
                    "color": "#FF0000" // 状态主颜色
                }
            ]
        }
    ],
}
```

然后启动服务器`./server.py`，服务器将自动加载配置并启动。若没有配置，服务器会使用默认配置进行启动，默认管理员账号密码均为`admin`，请注意修改。面板可通过`http://<ip>:<port>/dashboard`（若定义了不同的`prefix`，如以`/abc`为例，面板地址为`http://<ip>:<port>/abc/dashboard`），API则对应为`http://<ip>:<port>/api`（`prefix`情况同面板）。

> [!Warning]
>
> 关闭服务器时请使用`^C`快捷键（即`Ctrl+C`）、2号信号（即`SIGINT`）或面板端关闭