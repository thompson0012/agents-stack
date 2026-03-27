from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


class GoalLineageTemplateTests(unittest.TestCase):
    def test_live_doc_templates_are_inert(self) -> None:
        for relative in [
            "templates/base/docs/live/current-focus.md",
            "templates/base/docs/live/progress.md",
            "templates/base/docs/live/runtime.md",
            "templates/base/docs/live/qa.md",
            "templates/base/docs/live/todo.md",
        ]:
            content = read(relative)
            self.assertNotIn("Resume Task", content)
            self.assertNotIn("top-level skill audit", content)
            self.assertNotIn("Task 35", content)

    def test_roadmap_template_exposes_goal_lineage_fields(self) -> None:
        content = read("templates/base/docs/live/roadmap.md")
        self.assertIn("Source Goal", content)
        self.assertIn("Plan Goal", content)
        self.assertIn("Phase Ledger", content)
        self.assertIn("Goal Changes", content)
        self.assertIn("Resume Rules", content)

    def test_harness_skill_mentions_goal_lineage(self) -> None:
        content = read(
            "templates/base/.agents/skills/software-delivery/harness-design/SKILL.md"
        )
        self.assertIn("source goal", content)
        self.assertIn("plan goal", content)
        self.assertIn("current phase goal", content)
        self.assertIn("Preserve goal lineage", content)


if __name__ == "__main__":
    unittest.main()
