"""Initial-render smoke test for the Streamlit entry point."""

from __future__ import annotations

import unittest

from streamlit.testing.v1 import AppTest


class StreamlitSmokeTests(unittest.TestCase):
    def test_initial_page_renders_without_exceptions(self):
        app = AppTest.from_file("app.py", default_timeout=30).run()

        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.title[0].value, "AI Interview Coach")
        self.assertTrue(any("Upload" in message.value for message in app.info))


if __name__ == "__main__":
    unittest.main()
