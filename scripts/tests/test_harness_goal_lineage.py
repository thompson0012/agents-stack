from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


class HarnessGoalLineageTests(unittest.TestCase):
    def test_router_mentions_harness_and_goal_lineage(self) -> None:
        router = read("templates/base/.agents/skills/software-delivery/SKILL.md")
        self.assertIn("cross-session delivery control or harness design", router)

        children = read(
            "templates/base/.agents/skills/software-delivery/references/children.json"
        )
        self.assertIn("goal lineage", children)

    def test_evals_cover_roadmap_drift(self) -> None:
        evals = read("templates/base/.agents/skills/software-delivery/evals/evals.json")
        triggers = read(
            "templates/base/.agents/skills/software-delivery/evals/trigger-evals.json"
        )
        self.assertIn("direct-roadmap-drift", evals)
        self.assertIn("should-trigger-roadmap-drift", triggers)


if __name__ == "__main__":
    unittest.main()
