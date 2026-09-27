#!/usr/bin/env python3
"""Render the authoritative Markdown manuscript to a self-contained review HTML.

This intentionally supports only the Markdown constructs used by the manuscript.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/working-paper/WHU_WORKING_PAPER_MANUSCRIPT.md"
OUT = DOC.with_suffix(".html")


def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"!\[([^]]*)\]\(([^)]+)\)", r'<figure><img src="\2" alt="\1"><figcaption>\1</figcaption></figure>', s)
    s = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"`([^`]+)`", r'<code>\1</code>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r'<strong>\1</strong>', s)
    s = re.sub(r"\*([^*]+)\*", r'<em>\1</em>', s)
    return s


def render(md: str) -> str:
    out, para, items, quote = [], [], [], []

    def flush():
        nonlocal para, items, quote
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []
        if items:
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
            items = []
        if quote:
            out.append("<blockquote>" + inline(" ".join(quote)) + "</blockquote>")
            quote = []

    for raw in md.splitlines():
        line = raw.strip()
        if not line:
            flush(); continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush(); n=len(m.group(1)); out.append(f"<h{n}>{inline(m.group(2))}</h{n}>"); continue
        if line.startswith(">"):
            if para or items: flush()
            quote.append(line[1:].strip()); continue
        m = re.match(r"^\d+\.\s+(.*)$", line)
        if m:
            if para or quote: flush()
            items.append(m.group(1)); continue
        if line.startswith("!["):
            flush(); out.append(inline(line)); continue
        para.append(line.rstrip("  "))
    flush()
    return "\n".join(out)


css = """
body{font:17px/1.62 ui-serif,Georgia,serif;color:#1f2933;max-width:920px;margin:40px auto;padding:0 28px;background:#fcfbf8}
h1,h2,h3{font-family:ui-sans-serif,system-ui,sans-serif;color:#13293d;line-height:1.2;margin-top:1.7em}h1{font-size:2.45em}h2{border-top:1px solid #ccd3d8;padding-top:.8em}
p{margin:1em 0}blockquote{border-left:5px solid #557a95;margin:1.4em 0;padding:.2em 1.3em;color:#334e68;background:#eef3f6}
code{background:#edf1f3;padding:.08em .3em;border-radius:4px}figure{margin:2em 0}img{max-width:100%;height:auto;border:1px solid #d5d8dc;background:white}figcaption{font:14px ui-sans-serif,system-ui;color:#566573;margin-top:.5em}
a{color:#175d8d}ol{padding-left:1.5em}li{margin:.5em 0}@media print{body{max-width:none;margin:0;background:white}h2{break-before:page}figure{break-inside:avoid}}
"""

OUT.write_text(f"<!doctype html><html><head><meta charset='utf-8'><title>WHU Working Paper</title><style>{css}</style></head><body>{render(DOC.read_text())}</body></html>\n")
print(OUT)
