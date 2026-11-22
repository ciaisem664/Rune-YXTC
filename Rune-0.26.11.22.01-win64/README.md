# Rune 便携部署说明

版本：`0.26.11.22.01`（Cargo 包版本 `0.26.11`）
适用：Windows 10 / 11 x64。

## 1. 运行

解压后双击目录里的 `rune.exe`，或在终端运行：

```powershell
.\rune.exe
```

无需安装、无需 .NET/Python/C++ 运行时就能启动主程序；只有打开对应语言的插件时才需要该语言的工具链。

> exe 没有代码签名。若从网络/邮件到达，Windows 可能显示 SmartScreen。请只从你信任的来源获取；必要时核对 SHA-256。

## 2. 目录

```
Rune-0.26.11.22.01-win64/
├─ rune.exe
├─ rune.ico
├─ README.md                 ← 本文件
├─ assets/
│  └─ rune.png
├─ docs/
│  ├─ RPP-插件说明.md
│  └─ Python-插件说明.md
└─ plugin/
   ├─ 计算器/
   ├─ 图片编译器/
   ├─ hello-py/
   ├─ hello-java/
   ├─ hello-cs/
   └─ hello-cpp/
```

- `config.json` 会在第一次修改设置后生成在 `rune.exe` 旁边；删除它即恢复默认（1024x640、强调色 `#6366f1`、窗口模式）。
- 外部插件编译缓存放在 `%LOCALAPPDATA%\Rune\cache`；删掉即可强制重新编译。
- 插件源码就在 `plugin/` 下，可以直接改、直接加目录；重启 Rune 后重新扫描。

## 3. 插件工具链（可选）

| 语言 | 需要 | 说明 |
| --- | --- | --- |
| RPP | 无 | 内置解释器 |
| Python | Python 3.8+ | 优先找 `%LOCALAPPDATA%\Programs\Python\Python3xx\python.exe`，再 `py -3` / `python3` / `python`；跳过 WindowsApps 别名 |
| Java | JDK 11+ | `javac` 编译到用户缓存，`java -cp` 启动 |
| C# | .NET Framework `csc.exe` | 编译到用户缓存 |
| C++ | MSVC（VS 2019/2022 C++ 工具）或 clang++/g++ | 优先 MSVC，`/std:c++17` |

缺少工具链时，插件页会显示中文错误，主程序不受影响。编译/探测窗口已隐藏。

## 4. 已有插件

- `计算器`：RPP 示例，演示页面、组、输入、按钮、多页路径和 `about` 详情。
- `图片编译器`：只有 `desc`、没有入口，用来演示「仅介绍」注册。
- `hello-py` / `hello-java` / `hello-cs` / `hello-cpp`：四种外部语言的同一页示例，显示点击次数。

## 5. 常见问题

**双击没有反应**
确认运行的是本目录的 `rune.exe`，不是 `target\release` 里的构建产物；后者在开发机上可能是 Low 完整性，写用户缓存会被拒绝。若启动失败，看 exe 旁的 `error.log`。

**插件列表里缺少某个插件**
检查 `plugin.rtl` 的 `name` / `id` / `desc` 是否非空；`plugin.rtl` 必须放在 `plugin/<目录名>/` 下。

**Python 插件显示“插件进程已退出”**
先在该插件目录手动执行 `python main.py`，输入 `{"type":"open"}`；确认没有 BOM、stdout 只输出 JSON。若本机只有 Microsoft Store 的 Python 别名，请安装官方 Python 或把 `python.exe` 的目录加入 PATH。

**Java 第一次打开较慢**
第一次要 `javac` 编译并启动 JVM；之后编译缓存命中，但仍需启动 JVM，通常 1–3 秒，界面会先显示加载页。

**C++ 报找不到编译器**
安装 Visual Studio 的「使用 C++ 的桌面开发」工作负载，或安装 LLVM/Clang 并加入 PATH。Rune 会优先用 `vswhere` 找 VS。

**图标/版本**
exe 已嵌入多尺寸图标；主界面和开始页右下角显示 `RUNE / v0.26.11.22.01 / RUST / SOFTBUFFER`。

## 6. 从源码构建（可选）

```powershell
$env:CARGO_HOME="$PWD\.toolchain\cargo"
$env:RUSTUP_HOME="$PWD\.toolchain\rustup"
$env:TEMP="$PWD\.tmp"; $env:TMP=$env:TEMP
cargo build --release
```

产物在 `target\release\rune.exe`。图标资源是 `assets/rune.res`（由 `assets/rune.ico` 预编译），`build.rs` 只负责链接它；换图标后需要重新生成 `.res`，否则不会更新。
