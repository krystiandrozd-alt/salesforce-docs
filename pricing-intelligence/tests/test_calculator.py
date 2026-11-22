"""Offline tests for source-versioned Flex Credit estimates; no Salesforce API access."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from credit_calculator import calculate  # noqa: E402

RATE_CARD = json.loads((ROOT / "data" / "rate-card-2026-11-03.json").read_text(encoding="utf-8"))

def estimate(meter, quantity, environment="production", month="2026-12", **other):
    input_data = {"pricing_model": "FLEX_CREDITS", "usage": [
        {"meter": meter, "quantity": str(quantity), "environment": environment, "month": month}]}
    input_data.update(other)
    return calculate(input_data, RATE_CARD)

class CreditCalculatorTests(unittest.TestCase):
    def test_standard_action_production(self):
        x = estimate("agentforce-standard-action", 5000)
        self.assertEqual(x["priced_credits_only"], "100000")
        self.assertEqual(x["partial_list_price_equivalent"]["amount"], "500.00")
        self.assertEqual(x["status"], "ESTIMATE_NOT_QUOTE")

    def test_standard_action_sandbox(self):
        self.assertEqual(estimate("agentforce-standard-action", 5000, "sandbox")["priced_credits_only"], "80000")

    def test_voice_action(self):
        self.assertEqual(estimate("agentforce-standard-voice-action", 1000)["priced_credits_only"], "30000")

    def test_data360_prep_first_tier(self):
        self.assertEqual(estimate("data360-prep", 1000000)["priced_credits_only"], "40")

    def test_data360_crosses_first_tier(self):
        x = estimate("data360-prep", 8000000000)
        self.assertEqual(x["priced_credits_only"], "316000")
        self.assertEqual(x["priced_lines"][0]["tier_breakdown"][0]["credits"], "300000")
        self.assertEqual(x["priced_lines"][0]["tier_breakdown"][1]["credits"], "16000")

    def test_monthly_reset_and_repeat_lines_aggregate(self):
        x = calculate({"pricing_model": "FLEX_CREDITS", "usage": [
            {"month": "2026-12", "meter": "data360-prep", "environment": "production", "quantity": "4000000000"},
            {"month": "2026-12", "meter": "data360-prep", "environment": "production", "quantity": "4000000000"},
            {"month": "2027-01", "meter": "data360-prep", "environment": "production", "quantity": "8000000000"}
        ]}, RATE_CARD)
        self.assertEqual(x["priced_credits_only"], "632000")
        self.assertEqual(len(x["priced_lines"]), 2)

    def test_headless_tba_remains_unpriceable(self):
        x = estimate("headless-platform-interaction", 100)
        self.assertEqual(x["status"], "INCOMPLETE_UNPRICEABLE_USAGE")
        self.assertEqual(len(x["unpriceable_usage"]), 1)
        self.assertEqual(x["priced_credits_only"], "0")

    def test_slackbot_sandbox_unknown(self):
        self.assertEqual(estimate("slackbot-standard-action", 100, "sandbox")["status"], "INCOMPLETE_UNPRICEABLE_USAGE")

    def test_conversations_rejected(self):
        with self.assertRaisesRegex(ValueError, "Only FLEX_CREDITS"):
            calculate({"pricing_model": "CONVERSATIONS", "usage": []}, RATE_CARD)

    def test_bad_meter_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown meter"):
            estimate("fake-meter", 50)

    def test_negative_usage_rejected(self):
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            estimate("agentforce-standard-action", -1)

    def test_allowance_requires_provenance(self):
        with self.assertRaisesRegex(ValueError, "allowance_source"):
            estimate("agentforce-standard-action", 100, included_credits="1000")

    def test_allowance_subtraction(self):
        x = estimate("agentforce-standard-action", 5000, included_credits="20000",
                     allowance_source="Customer Order Form, local-only reference")
        self.assertEqual(x["net_priced_credits_only"], "80000")
        self.assertEqual(x["partial_list_price_equivalent"]["amount"], "400.00")

if __name__ == "__main__":
    unittest.main()
