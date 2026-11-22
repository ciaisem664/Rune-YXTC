# RPP 插件说明

RPP 是 Rune 内置的轻量脚本语言，用来写没有外部依赖的小插件：页面、输入框、按钮、分组、路径和宿主文字覆盖都在 Rune 进程内解释执行。

## 1. 目录与清单

一个插件是一个目录，放在 `plugin/` 下：

```
plugin/计算器/
├─ plugin.rtl
└─ rpp/
   └─ main.rpp
```

`plugin.rtl` 是清单，不是脚本：

```ini
name = "计算器"
id = "calculator"
desc = "用 RPP 写的四则运算示例"
lang = "rpp"
entry = "rpp/main.rpp"
about = "about"
```

- `name` / `id` / `desc` 必填；`id` 是稳定标识，不要含 `/`、`\`、`:`。
- `lang` 可省略，默认 `rpp`；`entry` 可省略。
- 没有 `entry` 的条目仍会出现在插件列表里，但只进入介绍页，不能「打开插件」。
- `about` 可选：声明后，详情页会调用脚本里的同名函数，把返回的页面追加到 `desc` 后面。
- `permissions` 可选；只有声明了 `ui.host.write` 的插件才能用 `ui.host`。

清单完整（`name`、`id`、`desc` 非空）就会注册，建议 `desc` 用一句话说清用途。

## 2. 语法

RPP 刻意不用缩进、不用大括号：

- 行尾 `:` 开一个块；
- 普通语句以 `;` 结束；
- 单独一行 `.` 关闭最近的块；
- `#` 开始注释。

```rpp
# 两个数相加
func add(a, b):
    return a + b;
.

func main:
    ui.page("home", "示例");
    ui.text("你好");
    ui.show();
.
```

### 关键字

`func` / `if` / `elif` / `else` / `while` / `for` / `in` / `break` / `continue` / `return` / `true` / `false` / `none`

- 函数只能定义在顶层，`main` 无参。
- 支持递归。
- `else:` 和 `elif ...:` 只是分支标签；整个 `if` 只用一个 `.` 收尾。

```rpp
func fib(n):
    if n < 2:
        return n;
    else:
        return fib(n - 1) + fib(n - 2);
    .
.
```

### 表达式与内置函数

- 算术：`+ - * / %`；比较：`== != < <= > >=`。
- 逻辑用符号：`&&` / `||` / `!`。
- 列表：`[]`、下标、`for x in xs`。
- 内置：`float(x)`、`int(x)`、`str(x)`、`len(x)`。

没有 `map` 字面量；需要键值结构时用多个变量或列表。

## 3. 页面、路径与分组

| 命令 | 作用 |
| --- | --- |
| `ui.page(id, title)` | 切到（或新建）一个页面；当前页会压入内部返回栈 |
| `ui.goto(id)` | 跳到已经存在的页面，不新建 |
| `ui.back()` | 弹出内部返回栈；栈空时交给宿主关闭插件 |
| `ui.group(id, label)` | 开始一个 UI 组，后续元素归入该组 |
| `ui.end_group()` | 结束当前组 |
| `ui.text(label)` | 加一行只读文字 |
| `ui.input(id, label)` | 加输入框 |
| `ui.button(id, label, func)` | 加按钮；点击时调用顶层函数 `func` |
| `ui.find(id)` | 取回元素句柄，可读写属性 |
| `ui.show()` | 标记页面已经可以显示 |
| `ui.toast(text)` | 在页面顶部显示一条临时提示 |

页面路径由 `ui.page` / `ui.goto` / `ui.back` 的历史决定，面包屑会显示成：

```
[主界面/开始/插件/计算器/帮助]
[主界面/选项/插件列表/计算器/帮助]
```

从「开始」页或「插件列表」进入时，前缀不同，但插件内部路径一致。

### 分组

```rpp
ui.group("input", "输入");
ui.input("a", "A");
ui.input("b", "B");
ui.end_group();

ui.group("actions", "运算");
ui.button("add", "加", add);
ui.button("sub", "减", sub);
ui.end_group();
```

组会画成 `# 标题`，组内元素缩进。组内元素仍然按添加顺序纵向排列。

## 4. 元素属性

`ui.find(id)` 返回元素句柄，支持：

```rpp
el = ui.find("result");
el.text = "42";          # 只读文字/按钮标签
el.value = "abc";        # 输入框的值
el.visible = false;
el.enabled = false;
```

- `text` 对 Text / Button 可写；Input 用 `value`。
- `visible` / `enabled` 控制显示和可交互。
- 修改的是当前页元素；不会自动创建新元素。

## 5. 宿主文字覆盖（需要权限）

清单声明：

```ini
permissions = ["ui.host.write"]
```

脚本里：

```rpp
ui.host("brand.1", "v0.26.11.22.01");
ui.host("title.settings", "设置");
```

可用 key：

- `brand.0` / `brand.1` / `brand.2`：右下角三行；
- `crumb.<page>`：某个宿主页面的面包屑；
- `title.<page>`：某个宿主页面的标题；
- `menu.<page>.<index>`：某个宿主页面第 index 个菜单项。

`<page>` 使用 `Page::key()`，例如 `main`、`start`、`settings`、`plugins`、`builtin_plugins`。没有权限时调用 `ui.host` 会报错。

## 6. 详情页 `about`

```ini
about = "about"
```

```rpp
func about:
    ui.page("about", "关于计算器");
    ui.text("用 RPP 写的四则运算示例。");
    ui.text("输入 A/B，按运算按钮，结果写回 result。");
    ui.show();
.
```

Rune 在插件列表的详情页里调用 `about`，把页面内容转换成只读条目；随后追加 `-打开插件-` 和 `-返回-`。`desc` 永远先显示，`about` 追加在其后。

## 7. 运行与调试

```powershell
# 直接打开
.\rune.exe --plugin calculator

# 打开后调用某个函数（调试用）
.\rune.exe --plugin calculator --plugin-call help

# 直接看详情页
.\rune.exe --plugin-detail calculator

# 离屏快照
.\rune.exe --snapshot calc.bmp --plugin calculator --time 2
```

解释器有步数上限；死循环会报错而不是卡死。语法/运行错误会显示在插件页面上，带行号。`stderr` 不显示在界面里，复杂脚本建议先拆小段测试。

## 8. 当前限制

- `input.*`（应用内输入模态）、`data.*`、`file.*` 还没实现；
- 宿主页面的 `mount` / `override` / `place` / `pin` 还没实现（规划中）；
- 没有真实的多语言 ABI：RPP 只能调用本文列出的宿主命令；
- 每个插件进程内共享一份页面状态；宿主不持久化插件变量。

## 9. 示例

完整示例见 `plugin/计算器/`：

- `plugin.rtl`：清单 + `about`；
- `rpp/main.rpp`：输入组、结果组、运算组、清空、帮助页、`ui.back()`。

`plugin/图片编译器/` 是一个只有 `desc`、没有 `entry` 的「仅介绍」插件，用来演示注册但不执行。
