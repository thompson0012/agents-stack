from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]


class TemplateAgentsHierarchyTests(unittest.TestCase):
    def test_docs_guides_exist_and_are_indexed_by_root(self) -> None:
        root_content = (REPO_ROOT / "templates/base/AGENTS.md").read_text(encoding="utf-8")

        for relative in [
            "templates/base/docs/AGENTS.md",
            "templates/base/docs/live/AGENTS.md",
            "templates/base/docs/reference/AGENTS.md",
        ]:
            self.assertTrue((REPO_ROOT / relative).exists(), relative)

        self.assertIn("docs/AGENTS.md", root_content)
        self.assertIn("docs/live/AGENTS.md", root_content)
        self.assertIn("docs/reference/AGENTS.md", root_content)


if __name__ == "__main__":
    unittest.main()
