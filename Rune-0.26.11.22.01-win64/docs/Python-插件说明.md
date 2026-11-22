# Python 插件说明

Rune 的 Python 插件不是 DLL，也不是嵌入 Python 解释器：宿主把 `main.py` 作为**独立子进程**启动，双方用 stdin/stdout 的 JSON Lines 通信。页面、输入框、按钮和命中测试仍由 Rune 绘制，Python 只负责状态和返回页面描述。

## 1. 目录

```
plugin/my-python/
├─ plugin.rtl
└─ main.py
```

`plugin.rtl`：

```ini
name = "Python 计算器"
id = "python-calculator"
desc = "用 Python 写的四则运算示例"
lang = "python"
entry = "main.py"
```

- `name` / `id` / `desc` 必填。
- `lang = "python"`，`entry` 指向 `.py` 文件。
- 没有 `entry` 时只注册为「仅介绍」插件；`permissions` / `about` 目前对 Python 插件不生效。
- 宿主在插件目录下启动 `python main.py`，工作目录就是插件目录。

## 2. 运行方式

Rune 按以下顺序找 Python：

1. `%LOCALAPPDATA%\Programs\Python\Python3xx\python.exe`（用户安装的官方发行版）；
2. `py -3`（有 py 启动器时）；
3. `python3` / `python`，但会跳过 `WindowsApps` 下的商店占位别名。

所以：

- 没装 Python，或只有 Microsoft Store 别名时，插件会显示「插件进程已退出」或启动超时；
- 装了 Python 但没加 PATH 也能用，因为宿主直接找安装目录；
- 需要 Python 3.8+；脚本里请用 UTF-8。

测试时先在插件目录手动跑：

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" main.py
```

然后输入一行 `{"type":"open"}`，应看到一行 `{"type":"page",...}`。

## 3. 协议

一行一条 JSON，UTF-8；不要输出多行缩进的 JSON。宿主 → 插件：

```json
{"type":"open"}
{"type":"action","id":"add","values":{"a":"12","b":"4"}}
```

插件 → 宿主：

```json
{"type":"page","title":"Python 计算器","elements":[
  {"kind":"text","label":"用 Python 写的四则运算示例"},
  {"kind":"input","id":"a","label":"A","value":"12"},
  {"kind":"input","id":"b","label":"B","value":"4"},
  {"kind":"text","label":"结果：16"},
  {"kind":"button","id":"add","label":"加"},
  {"kind":"button","id":"clear","label":"清空"},
  {"kind":"button","id":"close","label":"返回"}
]}
{"type":"toast","text":"已清空"}
{"type":"close"}
```

- 元素 `kind` 只支持 `text` / `input` / `button`；
- `input` 的 `id` 会出现在宿主发回的 `values` 里；
- `button` 的 `id` 会作为 `action.id` 发回；
- `close` 关闭插件并回到进入前的页面；
- 每次宿主发 `open`/`action` 后，插件应回一行 `page`（可先回 `toast`）；
- 宿主等待一行响应最多 10 秒；超时显示错误页。

## 4. 最小示例

```python
import json
import sys

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

values = {"a": "", "b": ""}
result = "0"


def page():
    return {
        "type": "page",
        "title": "Python 计算器",
        "elements": [
            {"kind": "input", "id": "a", "label": "A", "value": values["a"]},
            {"kind": "input", "id": "b", "label": "B", "value": values["b"]},
            {"kind": "text", "label": f"结果：{result}"},
            {"kind": "button", "id": "add", "label": "加"},
            {"kind": "button", "id": "close", "label": "返回"},
        ],
    }


def emit(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


for line in sys.stdin:
    msg = json.loads(line)
    if msg.get("type") == "action":
        values.update(msg.get("values") or {})
        if msg.get("id") == "add":
            try:
                result = str(float(values["a"]) + float(values["b"]))
            except ValueError:
                result = "0"
        elif msg.get("id") == "close":
            emit({"type": "close"})
            continue
    emit(page())
```

启动时先发一帧 `page`；宿主打开插件后会在收到第一帧后显示。

## 5. 限制与注意

- 单页：没有 RPP 的 `ui.page` / `ui.goto` / `ui.back` 多页栈；
- 没有 `about` 详情扩展；
- 没有权限系统、没有 `ui.host` 覆盖；
- 子进程随插件关闭而终止，变量不跨会话保存；
- 编译/解释器缺失时会显示中文错误，不会弹出系统控制台窗口；
- 只支持本机已安装的 Python；不会自动下载。

## 6. 调试

- 先手动执行上面的命令行测试，排除 JSON 格式问题；
- 确认每行都是合法 JSON、没有 BOM；
- 确认 `values` 里的键和输入框 `id` 一致；
- 不要在 stdout 打日志；日志请写 stderr（宿主不显示，但可重定向）；
- 复杂逻辑先在普通 Python 里跑通，再套协议。

示例见 `plugin/hello-py/`。
