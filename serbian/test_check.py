import unittest

from serbian.check import (
    heading_fragmentation,
    negative_parallelism_density,
    normalize_script,
    repeated_section_scaffold,
    review,
    triplet_density,
)


class SerbianSeedChecksTests(unittest.TestCase):
    def test_cyrillic_normalization(self):
        self.assertEqual(
            normalize_script("Људи њему кажу: ђак, ћирилица, џем."),
            "Ljudi njemu kažu: đak, ćirilica, džem.",
        )

    def test_single_negative_parallelism_is_not_flagged(self):
        text = "Ovo nije samo pitanje tehnike, već i pitanje prioriteta."
        self.assertIsNone(negative_parallelism_density(text))

    def test_repeated_negative_parallelism_is_flagged(self):
        text = " ".join(
            [
                "Sistem nije samo efikasan, već i pouzdan.",
                "Proces nije samo brz, već i transparentan.",
                "Rešenje nije samo moderno, već i održivo.",
                "Promena nije samo tehnička, već i društvena.",
            ]
        )
        finding = negative_parallelism_density(text)
        self.assertIsNotNone(finding)
        self.assertEqual(finding.rule_id, "sr_ai_negative_parallelism_density")

    def test_cyrillic_parallelism_is_detected_too(self):
        text = " ".join(
            [
                "Систем није само ефикасан, већ и поуздан.",
                "Процес није само брз, већ и транспарентан.",
                "Решење није само модерно, већ и одрживо.",
                "Промена није само техничка, већ и друштвена.",
            ]
        )
        self.assertIsNotNone(negative_parallelism_density(text))

    def test_single_triplet_is_not_flagged(self):
        self.assertIsNone(triplet_density("Potrebni su red, mir i stabilnost."))

    def test_repeated_triplets_are_flagged(self):
        text = " ".join(
            [
                "Sistem je brz, pouzdan i transparentan.",
                "Rešenje je moderno, održivo i inkluzivno.",
                "Proces je jasan, efikasan i predvidljiv.",
                "Cilj je rast, razvoj i stabilnost.",
            ]
        )
        finding = triplet_density(text)
        self.assertIsNotNone(finding)
        self.assertEqual(finding.rule_id, "sr_ai_triplet_density")

    def test_repeated_headings_are_flagged(self):
        text = """## Cilj kom stremimo
Prva mera ima duži opis koji objašnjava šta se tačno menja u sistemu i zašto.

## Promene koje dolaze
Prva promena ima konkretan opis sa dovoljno proze da ovaj test ne zavisi od gustine naslova.

## Cilj kom stremimo
Druga mera ima duži opis koji objašnjava šta se tačno menja u sistemu i zašto.

## Promene koje dolaze
Druga promena ima konkretan opis sa dovoljno proze da ovaj test ne zavisi od gustine naslova.

## Cilj kom stremimo
Treća mera ima duži opis koji objašnjava šta se tačno menja u sistemu i zašto.

## Promene koje dolaze
Treća promena ima konkretan opis sa dovoljno proze da ovaj test ne zavisi od gustine naslova.
"""
        finding = repeated_section_scaffold(text)
        self.assertIsNotNone(finding)
        self.assertEqual(finding.rule_id, "sr_ai_repeated_section_scaffold")

    def test_em_dash_is_not_a_rule(self):
        findings = review("Pišem ovako — sa crtom — još od škole.")
        self.assertEqual(findings, [])

    def test_both_scripts_are_clean_by_default(self):
        self.assertEqual(review("Ово је сасвим обична реченица на српском."), [])
        self.assertEqual(review("Ovo je sasvim obična rečenica na srpskom."), [])

    def test_dense_micro_headings_can_be_flagged(self):
        text = "\n\n".join(
            [
                "## Prvo\nKratko.",
                "## Drugo\nKratko.",
                "## Treće\nKratko.",
                "## Četvrto\nKratko.",
                "## Peto\nKratko.",
                "## Šesto\nKratko.",
            ]
        )
        finding = heading_fragmentation(text)
        self.assertIsNotNone(finding)
        self.assertEqual(finding.rule_id, "sr_ai_heading_fragmentation")


if __name__ == "__main__":
    unittest.main()
