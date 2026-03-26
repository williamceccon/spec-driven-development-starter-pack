import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


def load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "starter_pack.py"
    spec = importlib.util.spec_from_file_location("starter_pack", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class NewProjectGenerationTests(unittest.TestCase):
    def test_create_project_generates_beginner_files_from_profile_and_addons(self):
        module = load_module()
        starter_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as tmpdir:
            target_root = Path(tmpdir)
            project_path = module.create_project(
                starter_root=starter_root,
                project_name="demo-api",
                target_root=target_root,
                profile_name="python-api",
                addon_names=["postgres", "core-workflow"],
                initialize_git=False,
            )

            workflow_config = json.loads((project_path / "workflow-pack.json").read_text(encoding="utf-8"))
            manifest = json.loads((project_path / ".workflow-pack" / "manifest.json").read_text(encoding="utf-8"))
            env_example = (project_path / ".env.example").read_text(encoding="utf-8")
            readme = (project_path / "README.md").read_text(encoding="utf-8")
            agents = (project_path / "AGENTS.md").read_text(encoding="utf-8")
            claude = (project_path / "CLAUDE.md").read_text(encoding="utf-8")
            claude_brief = (project_path / ".claude" / "commands" / "brief.md").read_text(encoding="utf-8")
            claude_workflow = (project_path / ".claude" / "commands" / "workflow.md").read_text(encoding="utf-8")
            copilot_instructions = (project_path / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
            copilot_brief_agent = (project_path / ".github" / "agents" / "brief.agent.md").read_text(encoding="utf-8")
            skill_creator_exists = (project_path / "skills" / "skill-creator" / "SKILL.md").exists()
            writing_plans_exists = (project_path / "skills" / "writing-plans" / "SKILL.md").exists()
            opencode_skill_exists = (project_path / ".opencode" / "skills" / "writing-plans" / "SKILL.md").exists()
            claude_skill_exists = (project_path / ".claude" / "skills" / "writing-plans" / "SKILL.md").exists()
            agents_skill_exists = (project_path / ".agents" / "skills" / "writing-plans" / "SKILL.md").exists()

        self.assertEqual(workflow_config["profile"], "python-api")
        self.assertEqual(workflow_config["addons"], ["postgres", "core-workflow"])
        self.assertIn("bundled_skills", workflow_config)
        self.assertIn("skill-creator", workflow_config["bundled_skills"])
        self.assertIn("DATABASE_URL", env_example)
        self.assertIn("First 30 Minutes", readme)
        self.assertIn("Create a GitHub repository and push", readme)
        self.assertIn("Bundled Skills", readme)
        self.assertIn(".workflow-pack/manifest.json", agents)
        self.assertIn("python-api", agents)
        self.assertIn("demo-api", claude)
        self.assertIn("/brief", claude)
        self.assertIn("BRIEF.md", claude_brief)
        self.assertIn("slug", claude_workflow.lower())
        self.assertIn("python-api", copilot_instructions)
        self.assertIn("BRIEF.md", copilot_brief_agent)
        self.assertIn("Claude Code", workflow_config["supported_workspaces"])
        self.assertTrue(skill_creator_exists)
        self.assertTrue(writing_plans_exists)
        self.assertTrue(opencode_skill_exists)
        self.assertTrue(claude_skill_exists)
        self.assertTrue(agents_skill_exists)
        self.assertEqual(manifest["profile"]["name"], "python-api")
        self.assertEqual(manifest["addons"], ["postgres", "core-workflow"])
        self.assertIn("skill-creator", manifest["bundled_skills"])
        self.assertIn("CLAUDE.md", manifest["generated_surfaces"])
        self.assertIn(".github/copilot-instructions.md", manifest["generated_surfaces"])

    def test_nextjs_profile_bundles_playwright(self):
        module = load_module()
        starter_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as tmpdir:
            target_root = Path(tmpdir)
            project_path = module.create_project(
                starter_root=starter_root,
                project_name="demo-web",
                target_root=target_root,
                profile_name="nextjs-webapp",
                initialize_git=False,
            )

            workflow_config = json.loads((project_path / "workflow-pack.json").read_text(encoding="utf-8"))
            playwright_exists = (project_path / "skills" / "playwright" / "SKILL.md").exists()

        self.assertIn("playwright", workflow_config["bundled_skills"])
        self.assertTrue(playwright_exists)


if __name__ == "__main__":
    unittest.main()
