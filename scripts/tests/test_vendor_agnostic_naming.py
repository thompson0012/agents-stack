import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
AUDIT_MODULE_PATH = REPO_ROOT / "scripts" / "audit_base_template_skills.py"
COMMENT_SCRIPT_PATH = (
    REPO_ROOT
    / "templates"
    / "base"
    / ".agents"
    / "skills"
    / "using-documents"
    / "docx"
    / "scripts"
    / "comment.py"
 )


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class VendorAgnosticNamingTests(unittest.TestCase):
    def test_targeted_template_asset_paths_use_generic_names(self) -> None:
        audit = load_module("audit_base_template_skills_generic_names", AUDIT_MODULE_PATH)
        targeted = {path.relative_to(audit.SKILLS_ROOT).as_posix() for path in audit.targeted_template_asset_paths()}

        self.assertIn("website-building/shared/provenance_metadata.html", targeted)
        self.assertIn(
            "website-building/webapp/template/client/src/components/OptionalAttribution.tsx",
            targeted,
        )

    def test_docx_comment_defaults_are_generic(self) -> None:
        content = COMMENT_SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn('DEFAULT_AUTHOR = "Agent"', content)
        self.assertIn('DEFAULT_INITIALS = "AG"', content)


if __name__ == "__main__":
    unittest.main()
