import unittest

from scripts.rhetorical_metrics import audit, prose_paragraphs


class RhetoricalMetricsTests(unittest.TestCase):
    def test_repetition_is_descriptive_only(self):
        text = (
            "В этой главе изложена первая версия. Это важно.\n\n"
            "В этой главе изложена вторая версия. Это важно.\n\n"
            "В этой главе изложена третья версия. Это важно."
        )
        report = audit(text)
        self.assertEqual(report["classification"], "METRIC_ONLY")
        self.assertIn({"text": "в этой", "count": 3},
                      report["repeated_two_word_sentence_openers"])
        self.assertIn({"text": "это важно", "count": 3},
                      report["repeated_two_word_paragraph_endings"])
        for banned in ("severity", "score", "findings", "rewrite"):
            self.assertNotIn(banned, report)

    def test_question_answer_is_a_narrow_proxy(self):
        report = audit("Почему проект задержался? Потому что сервер был недоступен.")
        self.assertEqual(report["explicit_question_answer_marker_pairs"], 1)
        self.assertEqual(audit("Что произошло? Ответ: сервер выключили.")[
            "explicit_question_answer_marker_pairs"], 1)
        self.assertEqual(audit("Что произошло? Ответ директору уже отправили.")[
            "explicit_question_answer_marker_pairs"], 0)

    def test_question_answer_handles_quotes(self):
        text = "«Почему проект задержался?» Потому что сервер был недоступен."
        self.assertEqual(audit(text)["sentence_count"], 2)
        self.assertEqual(audit(text)["explicit_question_answer_marker_pairs"], 1)

    def test_abbreviations_decimals_and_initials_not_split(self):
        cases = [
            "В 2024 г. проект работал. В 2025 г. его закрыли.",
            "В отчёте указали 3.14 млн рублей. Позже сумму пересчитали.",
            "А. П. Чехов написал рассказ. Потом его опубликовали.",
            "См. рис. 2 в отчёте. Там показан результат.",
        ]
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(audit(text)["sentence_count"], 2)

    def test_runs_are_maximal_and_do_not_cross_paragraphs(self):
        five = "Он пришёл. Он ушёл. Он вернулся. Он лёг. Он уснул."
        found = audit(five)
        self.assertEqual(found["same_length_sentence_run_count"], 1)
        self.assertEqual(found["same_length_sentence_runs"], [
            {"paragraph_index": 1, "bin": "short", "sentences": 5}
        ])
        split = audit("Он пришёл. Он ушёл.\n\nОн вернулся. Он лёг.")
        self.assertEqual(split["same_length_sentence_run_count"], 0)
        self.assertEqual(split["same_length_sentence_runs"], [])

    def test_markup_code_quotes_and_lists_are_excluded(self):
        text = (
            "# В этой главе\n\n"
            "> В этой главе повторён тезис.\n\n"
            "- В этой главе пункт списка.\n\n"
            "~~~python\n"
            "print('В этой главе снова повторён тезис.')\n"
            "~~~\n\n"
            "Это обычный абзац. Он закончен."
        )
        self.assertEqual(prose_paragraphs(text), ["Это обычный абзац. Он закончен."])
        report = audit(text)
        self.assertEqual(report["paragraph_count"], 1)
        self.assertEqual(report["sentence_count"], 2)
        self.assertEqual(report["repeated_two_word_sentence_openers"], [])

    def test_long_fences_cannot_close_with_shorter_or_suffixed_markers(self):
        text = (
            "\x60\x60\x60\x60python\n"
            "В этой главе написан код.\n"
            "\x60\x60\x60\n"
            "В этой главе всё ещё код.\n"
            "\x60\x60\x60\x60 suffix\n"
            "В этой главе тоже код.\n"
            "\x60\x60\x60\x60\n\n"
            "А это обычный абзац."
        )
        self.assertEqual(prose_paragraphs(text), ["А это обычный абзац."])
        self.assertEqual(audit(text)["sentence_count"], 1)

    def test_inline_markdown_is_masked_without_dropping_prose(self):
        text = (
            "Прочитайте [справку](https://site.ru/help) и \x60code.alpha\x60. "
            "<!-- Не считайте это предложением. --> Данные доступны."
        )
        self.assertEqual(audit(text)["sentence_count"], 2)

    def test_dashes_passive_and_fragments_are_not_findings(self):
        report = audit("Было решено уехать. Без объяснений. Тихо — и навсегда.")
        self.assertEqual(report["classification"], "METRIC_ONLY")
        self.assertEqual(report["repeated_two_word_sentence_openers"], [])
        self.assertEqual(report["parameters"]["status"],
                         "provisional_not_corpus_calibrated")

    def test_sentence_final_abbreviations(self):
        self.assertEqual(audit(
            "Доклад опубликован в 2024 г. Результаты обсуждали отдельно."
        )["sentence_count"], 2)
        self.assertEqual(audit(
            "Отрезок имеет длину 5 см. Измерение повторили."
        )["sentence_count"], 2)
        self.assertEqual(audit(
            "Работу проводили в г. Москве. Затем опубликовали отчёт."
        )["sentence_count"], 2)
        self.assertEqual(audit(
            "В 2024 г. проект работал. В 2025 г. его закрыли."
        )["sentence_count"], 2)

    def test_thematic_break_setext_and_indented_code_not_prose(self):
        self.assertEqual(prose_paragraphs(
            "Первый абзац.\n\n---\n\nВторой абзац."
        ), ["Первый абзац.", "Второй абзац."])
        self.assertEqual(prose_paragraphs(
            "Название главы\n============\n\n"
            "    В этой главе не проза.\n"
            "    И здесь тоже код.\n\n"
            "Обычная проза."
        ), ["Обычная проза."])
        self.assertEqual(audit(
            "Один абзац.\n\n* * *\n\nДругой абзац."
        )["paragraph_count"], 2)

    def test_qa_across_adjacent_prose_paragraphs(self):
        self.assertEqual(audit(
            "Почему проект задержался?\n\n"
            "Потому что сервер был недоступен."
        )["explicit_question_answer_marker_pairs"], 1)

    def test_numbers_are_tokens_for_counts_and_exact_openers(self):
        text = (
            "В 2022 году проект начался.\n\n"
            "В 2023 году проект продолжился.\n\n"
            "В 2024 году проект завершился."
        )
        report = audit(text)
        self.assertEqual(report["repeated_two_word_sentence_openers"], [])
        self.assertEqual(audit("Купили 5 машин.")["word_count"], 3)
        self.assertEqual(audit("Оценка составила 3.14 балла.")["word_count"], 4)
        self.assertIn({"text": "в 2024", "count": 3}, audit(
            "В 2024 году начали. В 2024 году продолжили. В 2024 году закончили."
        )["repeated_two_word_sentence_openers"])

    def test_question_answer_combined_punctuation_and_dialogue_dash(self):
        self.assertEqual(audit("Почему?! Ответ: сервер недоступен.")[
            "explicit_question_answer_marker_pairs"], 1)
        self.assertEqual(audit("Почему? — Потому что сервер недоступен.")[
            "explicit_question_answer_marker_pairs"], 1)
        self.assertEqual(audit("Почему!? «Ответ: сервер недоступен.»")[
            "explicit_question_answer_marker_pairs"], 1)
        self.assertEqual(audit("Почему?! — Ответ директору отправлен.")[
            "explicit_question_answer_marker_pairs"], 0)
    def test_code_spans_with_inner_backticks_do_not_become_prose(self):
        text = (
            "\x60\x60В этой главе \x60код\x60 объяснён.\x60\x60\n\n"
            "\x60\x60В этой главе \x60пример\x60 объяснён.\x60\x60\n\n"
            "\x60\x60В этой главе \x60шаблон\x60 объяснён.\x60\x60\n\n"
            "Обычный абзац."
        )
        self.assertEqual(prose_paragraphs(text), ["Обычный абзац."])
        self.assertEqual(audit(text)["repeated_two_word_sentence_openers"], [])

    def test_multiline_code_span_is_not_counted(self):
        text = "\x60В этой главе\nЕсть два предложения. Всё ещё код.\x60\n\nВидимая проза."
        self.assertEqual(prose_paragraphs(text), ["Видимая проза."])

    def test_comment_tokens_inside_code_do_not_consume_prose(self):
        text = "\x60<!--\x60\n\nНастоящая проза.\n\n\x60-->\x60\n\nДругой абзац."
        self.assertEqual(
            prose_paragraphs(text), ["Настоящая проза.", "Другой абзац."]
        )

    def test_unclosed_html_comment_is_not_prose(self):
        text = "Вводный текст.\n\n<!--\nСкрытая строка.\n\nИ эта тоже."
        self.assertEqual(prose_paragraphs(text), ["Вводный текст."])

    def test_fences_inside_html_comments_do_not_hide_prose(self):
        text = "<!--\n```\n-->\n\nНастоящая проза. Следующее предложение."
        self.assertEqual(prose_paragraphs(text), [
            "Настоящая проза. Следующее предложение."
        ])
        self.assertEqual(audit(text)["sentence_count"], 2)

    def test_backticks_in_fence_info_string_are_not_a_fence(self):
        text = "```inline```\n\nНастоящая проза. Следующее предложение."
        self.assertEqual(audit(text)["sentence_count"], 2)

    def test_comment_backticks_do_not_pair_with_real_inline_code(self):
        text = "<!-- ` -->\n\nНастоящая проза. `sample` Другой текст."
        self.assertEqual(audit(text)["sentence_count"], 2)

    def test_indented_html_marker_does_not_hide_following_prose(self):
        text = "    <!--\n\nНастоящая проза. Следующее предложение."
        self.assertEqual(audit(text)["sentence_count"], 2)

    def test_abbreviation_can_terminate_sentence(self):
        for text in (
            "Книги, журналы и т. д. Далее идут примеры.",
            "Тексты, таблицы и т. п. Далее идут примеры.",
        ):
            with self.subTest(text=text):
                self.assertEqual(audit(text)["sentence_count"], 2)

    def test_unclosed_backtick_does_not_swallow_fence_or_prose(self):
        text = (
            "Вводный текст с одинокой ` кавычкой.\n\n"
            "```python\n"
            "print(`x`)\n"
            "В этой главе написан код.\n"
            "```\n\n"
            "Настоящая проза. Другой абзац."
        )
        self.assertEqual(prose_paragraphs(text), [
            "Вводный текст с одинокой ` кавычкой.",
            "Настоящая проза. Другой абзац.",
        ])
        self.assertEqual(audit(text)["sentence_count"], 3)

    def test_unclosed_backtick_does_not_pair_across_paragraphs(self):
        text = "Первый абзац с одинокой ` кавычкой.\n\nВторой абзац с `кодом` и текстом."
        self.assertEqual(prose_paragraphs(text), [
            "Первый абзац с одинокой ` кавычкой.",
            "Второй абзац с и текстом.",
        ])

    def test_emphasized_sentence_endings_and_question_answers(self):
        text = (
            "**Почему проект задержался?** "
            "**Потому что сервер недоступен.** "
            "**Это подтвердили позже.**"
        )
        report = audit(text)
        self.assertEqual(report["sentence_count"], 3)
        self.assertEqual(report["explicit_question_answer_marker_pairs"], 1)
    def test_empty_input(self):
        report = audit("")
        self.assertEqual(report["paragraph_count"], 0)
        self.assertEqual(report["sentence_count"], 0)
        self.assertEqual(report["same_length_sentence_run_count"], 0)


if __name__ == "__main__":
    unittest.main()
