import math
import unittest

from chatbot.engine import faqs, faq_questions, find_best_match, load_faqs
from chatbot.preprocessing import preprocess_text


class PreprocessingTests(unittest.TestCase):
    def test_normalizes_text_and_preserves_negation(self):
        self.assertEqual(
            preprocess_text("The ORDERS were NOT delivered!"),
            "order not deliv",
        )

    def test_handles_empty_and_non_string_input(self):
        for value in ("", "   ", None, 42):
            with self.subTest(value=value):
                self.assertEqual(preprocess_text(value), "")


class MatchingTests(unittest.TestCase):
    def test_loads_faq_dataset_and_question_variations(self):
        loaded_faqs = load_faqs()
        self.assertEqual(loaded_faqs, faqs)
        self.assertEqual(len(loaded_faqs), 15)
        self.assertEqual(
            len(faq_questions),
            sum(len(faq["questions"]) for faq in loaded_faqs),
        )
        self.assertTrue(all(faq["answer"] and faq["intent"] for faq in loaded_faqs))

    def test_every_faq_question_maps_to_its_intent(self):
        for faq in faqs:
            for question in faq["questions"]:
                with self.subTest(question=question):
                    result = find_best_match(question)
                    self.assertIsNotNone(result)
                    self.assertEqual(result["intent"], faq["intent"])
                    self.assertEqual(result["answer"], faq["answer"])

    def test_matches_typos_and_unseen_paraphrases(self):
        cases = {
            "wher is my ordrr": "order_tracking",
            "plese cancl my oder": "cancellation",
            "i need a refnd": "refund",
            "not received my order": "order_tracking",
        }
        for question, expected_intent in cases.items():
            with self.subTest(question=question):
                result = find_best_match(question)
                self.assertIsNotNone(result)
                self.assertEqual(result["intent"], expected_intent)
                self.assertGreaterEqual(result["similarity"], 0.20)

    def test_returns_none_for_empty_unrelated_or_negated_requests(self):
        for question in (
            "",
            "   ",
            "the and if",
            "weather in Paris",
            "What is the capital of France?",
            "I need a new job",
            "I do not want to cancel",
            "I don't want to return my order",
        ):
            with self.subTest(question=question):
                self.assertIsNone(find_best_match(question))

        self.assertIsNone(find_best_match(None))
        self.assertIsNone(find_best_match(123))

    def test_threshold_controls_matching_and_is_validated(self):
        self.assertIsNotNone(find_best_match("Where is my order?", threshold=1))
        self.assertIsNone(find_best_match("wher is my ordrr", threshold=0.5))
        self.assertIsNone(find_best_match("weather in Paris", threshold=0.2))

        for threshold in ("0.2", None, True):
            with self.subTest(threshold=threshold):
                with self.assertRaises(TypeError):
                    find_best_match("Where is my order?", threshold=threshold)

        for threshold in (-0.1, 1.1, math.nan, math.inf):
            with self.subTest(threshold=threshold):
                with self.assertRaises(ValueError):
                    find_best_match("Where is my order?", threshold=threshold)


if __name__ == "__main__":
    unittest.main()
