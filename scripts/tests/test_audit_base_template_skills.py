import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "audit_base_template_skills.py"


def load_audit_module():
    spec = importlib.util.spec_from_file_location("audit_base_template_skills", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class AuditBaseTemplateSkillsTests(unittest.TestCase):
    def test_scan_targeted_template_assets_flags_vendor_strings(self) -> None:
        audit = load_audit_module()
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            skills_root = repo_root / "templates" / "base" / ".agents" / "skills"
            write_file(
                skills_root / "website-building" / "shared" / "provenance_metadata.html",
                '<meta name="generator" content="Vendor Computer">\n',
            )

            with patch.object(audit, "REPO_ROOT", repo_root), patch.object(audit, "SKILLS_ROOT", skills_root):
                findings = audit.scan_targeted_template_assets()

            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0].kind, "vendor-string:vendor-computer branding")
            self.assertEqual(
                findings[0].path,
                Path("templates/base/.agents/skills/website-building/shared/provenance_metadata.html"),
            )

    def test_scan_targeted_template_assets_flags_port_placeholders(self) -> None:
        audit = load_audit_module()
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            skills_root = repo_root / "templates" / "base" / ".agents" / "skills"
            write_file(
                skills_root
                / "website-building"
                / "webapp"
                / "template"
                / "client"
                / "src"
                / "lib"
                / "queryClient.ts",
                'const API_BASE = "__PORT_5000__".startsWith("__") ? "" : "__PORT_5000__";\n',
            )

            with patch.object(audit, "REPO_ROOT", repo_root), patch.object(audit, "SKILLS_ROOT", skills_root):
                findings = audit.scan_targeted_template_assets()

            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0].kind, "template-placeholder:port-token")
            self.assertEqual(
                findings[0].path,
                Path(
                    "templates/base/.agents/skills/website-building/webapp/template/client/src/lib/queryClient.ts"
                ),
            )


    def test_main_flags_router_metadata_drift(self) -> None:
        audit = load_audit_module()
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            skills_root = repo_root / "templates" / "base" / ".agents" / "skills"
            write_file(
                skills_root / "using-superpowers" / "references" / "children.json",
                "{\n"
                '  "children": [{"path": "skills/legacy-skill", "label": "Vendor Computer", "href": "__PORT_5000__"}]\n'
                "}\n",
            )

            with (
                patch.object(audit, "REPO_ROOT", repo_root),
                patch.object(audit, "SKILLS_ROOT", skills_root),
                patch.object(audit, "validate_skill_files", return_value=[]),
                patch.object(audit, "scan_artifacts", return_value=[]),
                patch("sys.stdout", new_callable=__import__("io").StringIO) as stdout,
            ):
                rc = audit.main()

            self.assertEqual(rc, 1)
            output = stdout.getvalue()
            self.assertIn("templates/base/.agents/skills/using-superpowers/references/children.json:2 [stale-skill-path]", output)
            self.assertIn(
                "templates/base/.agents/skills/using-superpowers/references/children.json:2 [vendor-string:vendor-computer branding]",
                output,
            )
            self.assertIn(
                "templates/base/.agents/skills/using-superpowers/references/children.json:2 [template-placeholder:port-token]",
                output,
            )

if __name__ == "__main__":
    unittest.main()
