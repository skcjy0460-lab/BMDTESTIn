import unittest

from diabetes_engine import (
    candidate_additions,
    clinical_review,
    evaluate_injectable_regimen,
    evaluate_regimen,
    load_catalog,
    matrix_status,
    POLICY_EFFECTIVE_DATE,
    POLICY_REFERENCE,
)


class PairMatrixTests(unittest.TestCase):
    def test_metformin_and_dpp4_is_allowed(self):
        self.assertEqual(matrix_status("MET", "DPP4"), "O")
        self.assertEqual(evaluate_regimen(("MET", "DPP4")).status, "조합 가능")

    def test_dpp4_and_sglt2_pair_is_not_allowed(self):
        review = evaluate_regimen(("DPP4", "SGLT2_DA"))
        self.assertEqual(review.status, "조합 불가")
        self.assertEqual(matrix_status("DPP4", "SGLT2_DA"), "X")

    def test_su_and_enavogliflozin_is_allowed_from_june_notice(self):
        self.assertEqual(matrix_status("SU", "SGLT2_EN"), "O")
        self.assertEqual(evaluate_regimen(("SU", "SGLT2_EN")).status, "조합 가능")

    def test_policy_metadata_tracks_june_notice(self):
        self.assertEqual(POLICY_EFFECTIVE_DATE, "2026-06-01")
        self.assertIn("2026-117", POLICY_REFERENCE)


class ThreeDrugTests(unittest.TestCase):
    def test_met_dpp4_sglt2_is_exception_allowed(self):
        review = evaluate_regimen(("MET", "DPP4", "SGLT2_EM"))
        self.assertEqual(review.status, "조합 가능")
        self.assertTrue(any("예외" in message for message in review.basis))

    def test_met_tzd_enavogliflozin_is_excluded(self):
        review = evaluate_regimen(("MET", "TZD", "SGLT2_EN"))
        self.assertEqual(review.status, "조합 불가")

    def test_candidate_lists_show_blocked_additions(self):
        additions = dict(candidate_additions(("DPP4",)))
        self.assertEqual(additions["SGLT2_DA"].status, "조합 불가")


class CatalogAndNarrativeTests(unittest.TestCase):
    def test_catalog_has_searchable_products(self):
        products = load_catalog("data/drug_catalog.csv")
        self.assertTrue(any(item.product_name == "포시리진정10밀리그램" for item in products))
        self.assertTrue(any(item.price_krw == 334 for item in products))

    def test_clinical_review_mentions_initial_dual_threshold(self):
        review = evaluate_regimen(("MET", "DPP4"))
        notes = clinical_review(review, 7.8, 0, False)
        self.assertTrue(any("초기 2제요법" in note for note in notes))


class InjectableCoverageTests(unittest.TestCase):
    def test_insulin_with_two_allowed_orals_is_supported(self):
        review = evaluate_injectable_regimen(
            "INSULIN", ("MET", "DPP4"), 7.2, "경구제 또는 Insulin 투여 후 미조절"
        )
        self.assertEqual(review.status, "조합 가능")

    def test_insulin_with_enavogliflozin_is_not_supported(self):
        review = evaluate_injectable_regimen(
            "INSULIN", ("SGLT2_EN",), 8.0, "경구제 또는 Insulin 투여 후 미조절"
        )
        self.assertEqual(review.status, "조합 불가")
        self.assertTrue(any("Enavogliflozin" in message for message in review.basis))

    def test_glp1_with_met_su_and_bmi_threshold_is_supported(self):
        review = evaluate_injectable_regimen(
            "GLP1", ("MET", "SU"), 7.0, "경구제 또는 Insulin 투여 후 미조절", bmi=25.0
        )
        self.assertEqual(review.status, "조합 가능")

    def test_fixed_degludec_liraglutide_requires_metformin(self):
        review = evaluate_injectable_regimen(
            "FIXED_DEG", (), 7.3, "기저 Insulin 투여 후 미조절"
        )
        self.assertEqual(review.status, "추가 확인 필요")


if __name__ == "__main__":
    unittest.main()
