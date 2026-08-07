"""Initial-render smoke test for the Streamlit entry point."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest


QUESTIONS = "\n".join(
    f"{index}. Test interview question {index}?"
    for index in range(1, 6)
)
FEEDBACK = """
{
  "score": 8,
  "strengths": ["Specific example", "Clear result"],
  "improvements": ["Add context", "Quantify the impact"],
  "better_structure": ["Situation", "Action", "Result"]
}
""".strip()


class StreamlitSmokeTests(unittest.TestCase):
    def test_initial_page_renders_without_exceptions(self):
        app = AppTest.from_file("app.py", default_timeout=30).run()

        self.assertEqual(len(app.exception), 0)
        self.assertTrue(
            any(
                "Prepare for the interview" in block.value
                for block in app.markdown
            )
        )
        self.assertGreaterEqual(len(app.file_uploader), 1)
        self.assertTrue(
            any(toggle.label == "Accessibility" for toggle in app.toggle)
        )

    def test_sample_profile_completes_the_full_interview_flow(self):
        with (
            patch("utils.gemini_client.has_api_key", return_value=True),
            patch(
                "utils.summarizer.generate_text",
                return_value="## Candidate Overview\nStrong role fit.",
            ),
            patch(
                "utils.question_generator.generate_text",
                return_value=QUESTIONS,
            ),
            patch("utils.evaluator.generate_text", return_value=FEEDBACK),
        ):
            app = AppTest.from_file("app.py", default_timeout=30).run()
            app.button(key="sample_profile_full").click().run()

            self.assertEqual(
                app.text_input(key="target_role").value,
                "Junior Project Coordinator",
            )
            self.assertFalse(app.button(key="build_plan_full").disabled)

            app.button(key="build_plan_full").click().run()
            next(
                button
                for button in app.button
                if button.label == "Generate 5 interview questions"
            ).click().run()

            for question_index in range(5):
                next(
                    answer
                    for answer in app.text_area
                    if answer.label == "Your answer"
                ).input(
                    "I coordinated the team, tracked milestones, communicated "
                    "risks, and delivered the project on time."
                ).run()
                next(
                    button
                    for button in app.button
                    if button.label == "Get AI feedback"
                ).click().run()

                if question_index < 4:
                    next(
                        button
                        for button in app.button
                        if button.label == "Next"
                    ).click().run()

            self.assertEqual(len(app.exception), 0)
            self.assertTrue(
                any(
                    metric.label == "Average answer score"
                    and metric.value == "8.0/10"
                    for metric in app.metric
                )
            )
            self.assertTrue(
                any(
                    download.label == "Download report"
                    for download in app.download_button
                )
            )


if __name__ == "__main__":
    unittest.main()
