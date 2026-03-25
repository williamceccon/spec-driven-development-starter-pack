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
        }

        manifest = module.build_manifest(config)

        self.assertEqual(manifest["project_name"], "starter-demo")
        self.assertEqual(manifest["profile"]["name"], "python-api")
        self.assertEqual(manifest["addons"], ["postgres", "core-workflow"])
        self.assertEqual(manifest["bundled_skills"], ["writing-plans", "skill-creator"])
        self.assertIn("AGENTS.md", manifest["generated_surfaces"])
        self.assertIn(".workflow-pack/manifest.json", manifest["generated_surfaces"])
        self.assertEqual(manifest["recommended_skills"]["core-workflow"], ["writing-plans"])


if __name__ == "__main__":
    unittest.main()
