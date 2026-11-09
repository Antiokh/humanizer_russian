import unittest

from scripts.rhetorical_metrics import audit, prose_paragraphs


class RhetoricalMetricsTests(unittest.TestCase):
    def test_repetition_is_counted_but_not_condemned(self):
        text = (
            "В этой главе изложена первая версия. Это важно.\n\n"
            "В этой главе изложена вторая версия. Это важно.\n\n"
            "В этой главе изложена третья версия. Это важно."
        )
        report = audit(text)
        self.assertEqual(report["classification"], "METRIC_ONLY")
        self.assertIn(
            {"text": "в этой", "count": 3},
            report["repeated_two_word_sentence_openers"],
        )
        self.assertIn(
            {"text": "это важно", "count": 3},
            report["repeated_two_word_paragraph_endings"],
        )
        self.assertNotIn("severity", report)
        self.assertNotIn("score", report)
        self.assertNotIn("findings", report)

    def test_question_answer_is_descriptive_only(self):
        report = audit("Почему проект задержался? Потому что сервер был недоступен.")
        self.assertEqual(report["immediate_question_answer_pairs"], 1)
        self.assertEqual(report["classification"], "METRIC_ONLY")

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

    def test_dashes_passive_and_literary_fragments_do_not_create_findings(self):
        report = audit("Было решено уехать. Без объяснений. Тихо — и навсегда.")
        self.assertEqual(report["classification"], "METRIC_ONLY")
        self.assertEqual(report["repeated_two_word_sentence_openers"], [])

    def test_empty_input(self):
        report = audit("")
        self.assertEqual(report["paragraph_count"], 0)
        self.assertEqual(report["sentence_count"], 0)
        self.assertEqual(report["same_length_three_sentence_windows"], 0)


if __name__ == "__main__":
    unittest.main()
