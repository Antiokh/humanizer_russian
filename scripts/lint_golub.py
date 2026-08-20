#!/usr/bin/env python3
"""Conservative mechanical checks for the unified Golub source library."""
from __future__ import annotations
import argparse, json, re, statistics, sys
from pathlib import Path

from shared_russian_norm_surfaces import (
    SOGLASNO_DATIVE,
    iter_double_comparative,
    iter_mixed_correlative,
    iter_oplatit_za_payment_object,
    iter_soglasno_genitive,
    prose_surface,
)

SENTENCE = re.compile(r"[^.!?]+[.!?]?", re.S)
WORD = re.compile(r"[А-Яа-яЁёA-Za-z0-9]+")
PARTICIPLE_LIKE = re.compile(
    r"\b[А-Яа-яЁё]{4,}(?:вш(?:ий|ая|ее|ие)|ющ(?:ий|ая|ее|ие)|ащ(?:ий|ая|ее|ие)|енн(?:ый|ая|ое|ые)|анн(?:ый|ая|ое|ые))\b",
    re.I,
)

def _line(text,pos): return text.count('\n',0,pos)+1

def _finding(rule_id,pid,m,text,reason,operation,*,project_class='NORM',automation='DEFAULT_MECHANICAL',verdict='CHANGE',confidence='high'):
    return {'rule_id':rule_id,'phenomenon_id':pid,'project_class':project_class,'automation_level':automation,'verdict':verdict,'line':_line(text,m.start()),'excerpt':m.group(0)[:180],'reason':reason,'operation':operation,'confidence':confidence}

def review(text,context=None):
    prose=prose_surface(text); findings=[]
    for m in iter_soglasno_genitive(prose):
        tail=m.group(0).split()[-1].lower(); good=SOGLASNO_DATIVE.get(tail)
        op=f'replace_with: согласно {good}' if good else 'replace_genitive_after_soglasno_with_dative'
        findings.append(_finding('GOLUB-R40','norm.soglasno_dative',m,prose,'По формализованной системе Голуб и современной норме: «согласно» требует дательного падежа. Используется общий source-neutral surface detector; цитаты/code/URL/markup исключены.',op))
    for m in iter_oplatit_za_payment_object(prose):
        findings.append(_finding('GOLUB-R41','norm.payment_verb_government',m,prose,'Для узкого набора подтверждённых объектов нормативно «оплатить что» или «заплатить за что». Общий surface detector намеренно не моделирует все значения «за».','remove_za_or_use_zaplatit'))
    for m in iter_double_comparative(prose):
        findings.append(_finding('GOLUB-R44','norm.double_comparative_marking',m,prose,'Два способа образования сравнительной степени не должны механически совмещаться.','keep_one_comparative_marker'))
    for m in iter_mixed_correlative(prose):
        findings.append(_finding('GOLUB-R59','editing.paired_conjunction_alignment',m,prose,'По системе Голуб это кандидат на проверку симметрии соотносительного союза. Surface detector общий с Rosenthal library; длинную синтаксическую структуру проверять контекстно.','restore_correlative_pair',project_class='EDITING',automation='EXTENDED_SOFT',verdict='REVIEW',confidence=None))
    lengths=[len(WORD.findall(s.group(0))) for s in SENTENCE.finditer(prose) if s.group(0).strip()]
    words=[w.lower() for w in WORD.findall(prose)]
    echoes=sum(1 for a,b in zip(words,words[1:]) if len(a)>=5 and len(b)>=5 and a!=b and (a[:3]==b[:3] or a[-3:]==b[-3:]))
    metrics={'sentences':len(lengths),'sentence_word_counts':lengths,'sentence_word_max':max(lengths,default=0),'sentence_word_median':statistics.median(lengths) if lengths else 0,'participle_like_tokens':len(PARTICIPLE_LIKE.findall(prose)),'sound_echo_adjacent_pairs':echoes,'metric_rule_ids':['GOLUB-R63','GOLUB-R80'],'metrics_are_descriptive':True}
    return {'findings':findings,'metrics':metrics}

def self_test():
    cases=[
      ('Согласно приказа директора встреча переносится.','GOLUB-R40',True),('Согласно приказу директора встреча переносится.','GOLUB-R40',False),
      ('Оплатить за проезд можно картой.','GOLUB-R41',True),('Заплатить за проезд можно картой.','GOLUB-R41',False),('Оплатить за друга счёт можно картой.','GOLUB-R41',False),
      ('Этот вариант более лучше предыдущего.','GOLUB-R44',True),('Этот вариант намного лучше предыдущего.','GOLUB-R44',False),
      ('Он не только проверил данные, а также исправил отчёт.','GOLUB-R59',True),('Он не только проверил данные, но и исправил отчёт.','GOLUB-R59',False),
      ('`согласно приказа` — цитируемая строка кода.','GOLUB-R40',False),('«Согласно приказа» — пример обсуждаемой формы.','GOLUB-R40',False),
      ('# Согласно приказа директора','GOLUB-R40',False),('> Оплатить за проезд — обсуждаемый пример.','GOLUB-R41',False),
    ]
    for text,rid,want in cases:
        got=any(x['rule_id']==rid for x in review(text)['findings'])
        assert got==want,(text,rid,want,review(text))
    assert review('Очень длинное предложение состоит из нескольких слов.')['metrics']['sentences']==1
    print('golub linter self-test: OK')

def main():
    p=argparse.ArgumentParser(); p.add_argument('file',nargs='?'); p.add_argument('--self-test',action='store_true'); p.add_argument('--json',action='store_true',dest='as_json'); a=p.parse_args()
    if a.self_test: self_test(); return
    text=Path(a.file).read_text(encoding='utf-8') if a.file else sys.stdin.read(); out=review(text)
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.as_json else '\n'.join(f"{x['rule_id']}:{x['line']} {x['excerpt']} — {x['reason']}" for x in out['findings']))
if __name__=='__main__': main()
