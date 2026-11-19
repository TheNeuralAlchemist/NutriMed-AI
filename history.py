"""Saves results to history.json (Phase 9). On free hosting this file can reset."""
import json
import os
from datetime import datetime

FILE = "history.json"


def load():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def add(kind, title, content):
    items = load()
    items.insert(0, {
        "time": datetime.now().strftime("%d %b %Y, %H:%M"),
        "kind": kind,
        "title": title,
        "content": content,
    })
    try:
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(items[:50], f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # saving history must never crash the app


def clear():
    try:
        if os.path.exists(FILE):
            os.remove(FILE)
    except Exception:
        pass
