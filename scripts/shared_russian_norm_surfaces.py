#!/usr/bin/env python3
"""Source-neutral conservative Russian surfaces shared by source adapters."""
from __future__ import annotations
import re
URL=re.compile(r"https?://\S+",re.I)
FENCED=re.compile(r"```.*?```|~~~.*?~~~",re.S)
INLINE_CODE=re.compile(r"`[^`\n]+`")
QUOTED=[re.compile(r"«[^»]*»",re.S),re.compile(r"“[^”]*”",re.S),re.compile(r'"[^"\n]*"')]
MARKDOWN_NON_PROSE=re.compile(r"^\s*(#|\||[-*+]\s|\d+[.)]\s|>)")
SOGLASNO_GENITIVE=re.compile(r"\bсогласно\s+(?:приказа|договора|закона|указа|регламента|протокола|плана|графика|кодекса|распоряжения|положения|решения|требования|постановления|соглашения|контракта|устава|(?:данного|этого|нового|действующего|утвержд[её]нного|указанного|федерального|внутреннего|текущего|последнего)\s+(?:[А-Яа-яЁё-]+(?:ого|его)\s+){0,2}[А-Яа-яЁё-]+(?:а|я))\b",re.I)
MIXED_CORRELATIVE=re.compile(r"\bне\s+только\b(?:(?![.!?]).){0,180}?\bа\s+также\b",re.I|re.S)
OPLATIT_ZA_PAYMENT_OBJECT=re.compile(r"\b(оплат(?:ить|ил|ила|или|ит|ите|им|ят|ив|ишь))\s+за\s+(проезд|билет|билеты|заказ|покупку|услугу|услуги|обучение|доставку|парковку)\b",re.I)
DOUBLE_COMPARATIVE=re.compile(r"\b(?:более|менее)\s+(?:лучше|хуже|больше|меньше|выше|ниже|старше|младше|дальше|ближе|быстрее|медленнее|сильнее|слабее|дороже|дешевле|красивее|точнее|яснее|проще|сложнее|лучший|худший)\b",re.I)
SOGLASNO_DATIVE={'приказа':'приказу','договора':'договору','распоряжения':'распоряжению','плана':'плану','решения':'решению','положения':'положению','устава':'уставу','закона':'закону','контракта':'контракту','графика':'графику','указа':'указу','регламента':'регламенту','протокола':'протоколу','кодекса':'кодексу','требования':'требованию','постановления':'постановлению','соглашения':'соглашению'}
def _blank(m): return ''.join('\n' if c=='\n' else ' ' for c in m.group(0))
def prose_surface(text):
    out=FENCED.sub(_blank,text); out=INLINE_CODE.sub(_blank,out); out=URL.sub(_blank,out)
    for rx in QUOTED: out=rx.sub(_blank,out)
    lines=[]; fm=False
    for i,line in enumerate(out.splitlines()):
        if i==0 and line.strip()=='---': fm=True; lines.append(''); continue
        if fm:
            lines.append('')
            if line.strip()=='---': fm=False
            continue
        lines.append('' if MARKDOWN_NON_PROSE.match(line) else line)
    return '\n'.join(lines)
def iter_soglasno_genitive(text): return SOGLASNO_GENITIVE.finditer(text)
def iter_mixed_correlative(text): return MIXED_CORRELATIVE.finditer(text)
def iter_oplatit_za_payment_object(text): return OPLATIT_ZA_PAYMENT_OBJECT.finditer(text)
def iter_double_comparative(text): return DOUBLE_COMPARATIVE.finditer(text)
