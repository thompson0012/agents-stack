from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_GUIDES = (
    "templates/base/docs/AGENTS.md",
    "templates/base/docs/live/AGENTS.md",
    "templates/base/docs/reference/AGENTS.md",
)

AGENT_GUIDES = (
    "templates/base/.agents/AGENTS.md",
    "templates/base/.agents/skills/AGENTS.md",
    "templates/base/.agents/skills-optional/AGENTS.md",
)

REFERENCE_DOC_TRUTHS = {
    "templates/base/docs/reference/architecture.md": (
        "constitutional root",
        "first-read index",
        "must-read local `AGENTS.md`",
        "inert until a copied repo localizes them",
    ),
    "templates/base/docs/reference/codemap.md": (
        "Approved local guides live only at durable boundaries",
        "`templates/base/docs/AGENTS.md`",
        "`templates/base/.agents/AGENTS.md`",
        "`templates/base/.agents/skills-optional/AGENTS.md`",
    ),
    "templates/base/docs/reference/memory.md": (
        "Root discovery index must list every must-read local guide",
        "Shipped and optional skill-package truth stay separate",
        "Optional packages are not shipped default truth",
    ),
    "templates/base/docs/reference/lessons.md": (
        "Hidden must-read local guides",
        "Non-durable local guides",
    ),
}



def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


class TemplateAgentsHierarchyTests(unittest.TestCase):
    def test_module_exposes_shared_doc_helpers(self) -> None:
        self.assertEqual(
            DOC_GUIDES,
            (
                "templates/base/docs/AGENTS.md",
                "templates/base/docs/live/AGENTS.md",
                "templates/base/docs/reference/AGENTS.md",
            ),
        )
        self.assertEqual(read(DOC_GUIDES[0]), read("templates/base/docs/AGENTS.md"))

    def test_docs_guides_exist_and_are_indexed_by_root(self) -> None:
        root_content = read("templates/base/AGENTS.md")

        for relative in DOC_GUIDES:
            self.assertTrue((REPO_ROOT / relative).exists(), relative)

        self.assertIn("docs/AGENTS.md", root_content)
        self.assertIn("docs/live/AGENTS.md", root_content)
        self.assertIn("docs/reference/AGENTS.md", root_content)

    def test_agents_guides_exist_and_are_indexed_by_root(self) -> None:
        root_content = read("templates/base/AGENTS.md")

        for relative in AGENT_GUIDES:
            self.assertTrue((REPO_ROOT / relative).exists(), relative)

        self.assertIn(".agents/AGENTS.md", root_content)
        self.assertIn(".agents/skills/AGENTS.md", root_content)
        self.assertIn(".agents/skills-optional/AGENTS.md", root_content)


    def test_reference_guide_describes_all_current_reference_docs(self) -> None:
        reference_guide = read("templates/base/docs/reference/AGENTS.md")

        for name in [
            "architecture.md",
            "codemap.md",
            "implementation.md",
            "design.md",
            "memory.md",
            "lessons.md",
        ]:
            self.assertIn(f"`{name}`", reference_guide)


    def test_reference_docs_encode_the_template_agents_hierarchy_truth(self) -> None:
        for relative, expected_snippets in REFERENCE_DOC_TRUTHS.items():
            content = read(relative)
            for snippet in expected_snippets:
                self.assertIn(snippet, content, f"{relative} missing {snippet!r}")


if __name__ == "__main__":
    unittest.main()
