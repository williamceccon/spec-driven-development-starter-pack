import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


def load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "skills"
        / "specify-workflow-pack"
        / "scripts"
        / "install_workflow_pack.py"
    )
    spec = importlib.util.spec_from_file_location("install_workflow_pack", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class InstallWorkflowPackTests(unittest.TestCase):
    def test_load_config_supports_profile_addons_and_recommended_skills(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "workflow-pack.json"
            config_path.write_text(
                json.dumps(
                    {
                        "project_name": "starter-demo",
                        "profile": "python-api",
                        "addons": ["postgres", "core-workflow"],
                        "bundled_skills": ["writing-plans", "skill-creator"],
                        "supported_platforms": ["Windows", "macOS", "Linux"],
                        "recommended_skills": {
                            "core-workflow": [
                                "brainstorming",
                                "writing-plans",
                                "verification-before-completion",
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )

            config = module.load_config(config_path)

        self.assertEqual(config["profile"], "python-api")
        self.assertEqual(config["addons"], ["postgres", "core-workflow"])
        self.assertEqual(config["bundled_skills"], ["writing-plans", "skill-creator"])
        self.assertEqual(config["supported_platforms"], ["Windows", "macOS", "Linux"])
        self.assertIn("core-workflow", config["recommended_skills"])
        self.assertTrue(config["pack_version"])
        self.assertTrue(config["core_version"])

    def test_build_manifest_tracks_profile_addons_and_generated_surfaces(self):
        module = load_module()
        config = {
            "project_name": "starter-demo",
            "pack_version": "1.0.0",
            "core_version": "1.0.0",
            "profile": "python-api",
            "addons": ["postgres", "core-workflow"],
            "required_skills": ["brainstorming"],
            "bundled_skills": ["writing-plans", "skill-creator"],
            "recommended_skills": {"core-workflow": ["writing-plans"]},
            "supported_workspaces": ["Codex", "Claude Code", "OpenCode", "GitHub Copilot", "Antigravity"],
        }

        manifest = module.build_manifest(config)

        self.assertEqual(manifest["project_name"], "starter-demo")
        self.assertEqual(manifest["profile"]["name"], "python-api")
        self.assertEqual(manifest["addons"], ["postgres", "core-workflow"])
        self.assertEqual(manifest["bundled_skills"], ["writing-plans", "skill-creator"])
        self.assertIn("AGENTS.md", manifest["generated_surfaces"])
        self.assertIn("CLAUDE.md", manifest["generated_surfaces"])
        self.assertIn(".github/copilot-instructions.md", manifest["generated_surfaces"])
        self.assertIn(".claude/commands/brief.md", manifest["generated_surfaces"])
        self.assertIn(".github/agents/brief.agent.md", manifest["generated_surfaces"])
        self.assertIn(".workflow-pack/manifest.json", manifest["generated_surfaces"])
        self.assertEqual(manifest["recommended_skills"]["core-workflow"], ["writing-plans"])
        self.assertIn("Claude Code", manifest["supported_workspaces"])

    def test_powershell_installer_runs_with_default_codex_home_resolution(self):
        repo_root = Path(__file__).resolve().parents[1]
        script_path = repo_root / "scripts" / "install-workflow-pack.ps1"

        with tempfile.TemporaryDirectory() as home_dir:
            env = os.environ.copy()
            env["HOME"] = home_dir
            env["USERPROFILE"] = home_dir
            env.pop("CODEX_HOME", None)
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(script_path),
                ],
                cwd=repo_root,
                env=env,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
