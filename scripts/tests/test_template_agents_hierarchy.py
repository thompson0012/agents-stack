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

TEMPLATE_PORTABLE_ASSETS = (
    "templates/base/.agents/router-manifest.json",
)

TEMPLATE_ROOT_PORTABLE_SNIPPETS = (
    ".agents/router-manifest.json",
)

TEMPLATE_ROOT_FORBIDDEN_SNIPPETS = (
    "scripts.tests.test_template_agents_hierarchy",
    "scripts.tests.test_goal_lineage_templates",
    "audit_base_template_skills.py",
    "templates/base/scripts/validate_agents_router.py",
    "python3 scripts/validate_agents_router.py",
)


REFERENCE_DOC_TRUTHS = {
    "templates/base/docs/reference/architecture.md": (
        "constitutional root",
        "first-read index",
        "local rule boundaries live under `docs/` and `.agents/`",
        "copied subtree has its own durable contract",
    ),
    "templates/base/docs/reference/codemap.md": (
        "Approved local guides live only at durable boundaries",
        "`docs/AGENTS.md`",
        "`.agents/AGENTS.md`",
        "`.agents/skills-optional/AGENTS.md`",
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

ROOT_CONSTITUTION_SNIPPETS = (
    "## Project Context",
    "packages a portable AGENTS and skill hierarchy that can be copied into another repository and localized there.",
    "## Mandatory First Reads",
    "Read this file first before acting in the copied hierarchy.",
    "## Operational Commands",
    "This template ships no seeded install, build, lint, or test commands by default.",
    "## Skill Invocation Precedence",
    "Check project-local shipped skills under `.agents/skills/` before relying on generic knowledge.",
    "## Safety Boundaries",
    "### Always do",
    "### Ask first",
    "### Never do",
    "## Injected Context Contract",
    "This root `AGENTS.md` is the only always-in-context index for the template hierarchy.",
    "## Hierarchical Discovery",
    "Every must-read local `AGENTS.md` must appear in the discovery index in the same change that adds or removes it.",
    "## Live-Doc Writeback Obligation",
    "If work changes the template live-doc contract or localization expectations, update the governing docs in the same change.",
    "## Reference Writeback Gate",
    "Before yielding after meaningful work, decide whether any `docs/reference/*` file must change to keep durable truth aligned.",
    "## Cross-System Precedence",
    "Root constitutional rules win over subtree guides.",
)

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

    def test_root_guide_contains_constitutional_contract(self) -> None:
        root_content = read("templates/base/AGENTS.md")

        for snippet in ROOT_CONSTITUTION_SNIPPETS:
            self.assertIn(snippet, root_content)

    def test_template_portable_router_assets_exist_and_are_indexed(self) -> None:
        root_content = read("templates/base/AGENTS.md")
        agents_guide = read("templates/base/.agents/AGENTS.md")

        for relative in TEMPLATE_PORTABLE_ASSETS:
            self.assertTrue((REPO_ROOT / relative).exists(), relative)

        self.assertFalse(
            (REPO_ROOT / "templates/base/scripts/validate_agents_router.py").exists(),
            "template should not ship a seeded validator script",
        )

        for snippet in TEMPLATE_ROOT_PORTABLE_SNIPPETS:
            self.assertIn(snippet, root_content)

        for snippet in TEMPLATE_ROOT_FORBIDDEN_SNIPPETS:
            self.assertNotIn(snippet, root_content)

        self.assertIn("router-manifest.json", agents_guide)


    def test_template_subtree_has_no_seeded_repo_paths(self) -> None:
        offenders: list[str] = []
        for path in (REPO_ROOT / "templates/base").rglob("*"):
            if path.suffix not in {".md", ".json", ".py"}:
                continue
            content = path.read_text(encoding="utf-8")
            if "templates/base/" in content:
                offenders.append(str(path.relative_to(REPO_ROOT)))

        self.assertEqual(offenders, [], f"seeded repo paths remain in: {offenders}")


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
