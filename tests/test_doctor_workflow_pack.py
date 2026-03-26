import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


def load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "skills"
        / "specify-workflow-pack"
        / "scripts"
        / "doctor_workflow_pack.py"
    )
    spec = importlib.util.spec_from_file_location("doctor_workflow_pack", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DoctorWorkflowPackTests(unittest.TestCase):
    def test_load_config_supports_profile_addons_and_recommended_skills(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "workflow-pack.json"
            config_path.write_text(
                json.dumps(
                    {
                        "project_name": "starter-demo",
                        "profile": "python-api",
                        "addons": ["postgres"],
                        "supported_workspaces": ["Codex", "Claude Code", "OpenCode", "GitHub Copilot", "Antigravity"],
                        "bundled_skills": ["writing-plans", "skill-creator"],
                        "recommended_skills": {"core-workflow": ["brainstorming"]}
                    }
                ),
                encoding="utf-8",
            )

            config = module.load_config(config_path)

        self.assertEqual(config["profile"], "python-api")
        self.assertEqual(config["addons"], ["postgres"])
        self.assertIn("Claude Code", config["supported_workspaces"])
        self.assertEqual(config["bundled_skills"], ["writing-plans", "skill-creator"])
        self.assertEqual(config["recommended_skills"]["core-workflow"], ["brainstorming"])

    def test_validate_repo_requires_manifest_for_new_contract(self):
        module = load_module()
        config = {
            "project_name": "starter-demo",
            "brief_artifact": "BRIEF.md",
            "local_skills_dir": "skills",
            "required_skills": ["brainstorming"],
            "profile": "python-api",
            "addons": ["postgres"],
            "supported_workspaces": ["Codex", "Claude Code", "OpenCode", "GitHub Copilot", "Antigravity"],
            "bundled_skills": [],
            "recommended_skills": {}
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            for rel in module.REQUIRED_FILES:
                if rel == ".workflow-pack/manifest.json":
                    continue
                path = repo / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("starter-demo /brief /workflow BRIEF.md", encoding="utf-8")
            local_skill = repo / "skills" / "brainstorming" / "SKILL.md"
            local_skill.parent.mkdir(parents=True, exist_ok=True)
            local_skill.write_text("skill", encoding="utf-8")

            failures = module.validate_repo(repo, config, check_tools=False)

        self.assertIn("Missing required file: .workflow-pack/manifest.json", failures)


if __name__ == "__main__":
    unittest.main()
