#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最小外部插件：读 JSON Lines，回页面 JSON。"""

import json
import sys

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

inputs = {"a": "", "b": ""}
result = "0"


def page():
    return {
        "type": "page",
        "title": "Python 计算器",
        "elements": [
            {"kind": "text", "label": "用 Python 写的四则运算示例"},
            {"kind": "input", "id": "a", "label": "A", "value": inputs["a"]},
            {"kind": "input", "id": "b", "label": "B", "value": inputs["b"]},
            {"kind": "text", "label": "结果：" + result},
            {"kind": "button", "id": "add", "label": "加"},
            {"kind": "button", "id": "sub", "label": "减"},
            {"kind": "button", "id": "mul", "label": "乘"},
            {"kind": "button", "id": "div", "label": "除"},
            {"kind": "button", "id": "clear", "label": "清空"},
            {"kind": "button", "id": "close", "label": "返回"},
        ],
    }


def emit(value):
    sys.stdout.write(json.dumps(value, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def number(text):
    try:
        return float(text)
    except ValueError:
        return 0.0


def handle(action):
    global result
    if action == "clear":
        inputs["a"] = ""
        inputs["b"] = ""
        result = "0"
    elif action == "close":
        emit({"type": "close"})
        return
    else:
        a = number(inputs["a"])
        b = number(inputs["b"])
        if action == "add":
            result = str(a + b)
        elif action == "sub":
            result = str(a - b)
        elif action == "mul":
            result = str(a * b)
        elif action == "div":
            result = "不能除以 0" if b == 0 else str(a / b)
        result = result.removesuffix(".0")
    emit(page())


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        message = json.loads(line)
    except json.JSONDecodeError:
        continue
    kind = message.get("type")
    if kind == "open":
        emit(page())
    elif kind == "action":
        values = message.get("values") or {}
        for key in ("a", "b"):
            if key in values:
                inputs[key] = str(values[key])
        handle(message.get("id", ""))
