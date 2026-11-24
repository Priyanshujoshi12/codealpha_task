import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


class StreamlitAppTests(unittest.TestCase):
    def run_app(self):
        return AppTest.from_file(str(APP_PATH)).run(timeout=15)

    def test_app_renders_without_errors(self):
        app = self.run_app()

        self.assertFalse(app.exception)
        self.assertEqual(len(app.title), 1)
        self.assertEqual(len(app.chat_input), 1)
        self.assertEqual(len(app.button), 1)

    def test_matching_response_and_clear_conversation(self):
        app = self.run_app()
        app.chat_input[0].set_value("Where is my order?").run(timeout=15)

        self.assertFalse(app.exception)
        self.assertEqual(len(app.chat_message), 2)
        self.assertIn("track your order", app.chat_message[1].markdown[0].value)
        self.assertEqual(len(app.session_state["messages"]), 2)

        app.button[0].click().run(timeout=15)
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["messages"], [])
        self.assertEqual(len(app.chat_message), 0)

    def test_unmatched_question_shows_fallback(self):
        app = self.run_app()
        app.chat_input[0].set_value("weather in Paris").run(timeout=15)

        self.assertFalse(app.exception)
        self.assertEqual(len(app.chat_message), 2)
        self.assertIn(
            "couldn't find a suitable answer",
            app.chat_message[1].markdown[0].value,
        )


if __name__ == "__main__":
    unittest.main()
