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

    def test_empty_input(self):
        report = audit("")
        self.assertEqual(report["paragraph_count"], 0)
        self.assertEqual(report["sentence_count"], 0)
        self.assertEqual(report["same_length_sentence_run_count"], 0)


if __name__ == "__main__":
    unittest.main()
