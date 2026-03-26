from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class DocsSiteTests(unittest.TestCase):
    def test_landing_page_assets_and_content_exist(self) -> None:
        index_path = DOCS / "index.html"
        styles_path = DOCS / "styles.css"
        post_path = DOCS / "github-feed-post.md"

        self.assertTrue(index_path.exists(), "docs/index.html should exist")
        self.assertTrue(styles_path.exists(), "docs/styles.css should exist")
        self.assertTrue(post_path.exists(), "docs/github-feed-post.md should exist")

        index = index_path.read_text(encoding="utf-8")
        styles = styles_path.read_text(encoding="utf-8")
        post = post_path.read_text(encoding="utf-8")

        self.assertIn("SPEC-DRIVEN DEVELOPMENT STARTER PACK", index)
        self.assertIn("Based on GitHub's spec-kit", index)
        self.assertIn("View on GitHub", index)
        self.assertIn("See first release", index)
        self.assertIn("idea", index)
        self.assertIn("repo ready", index)
        self.assertIn("profiles", index.lower())
        self.assertIn("add-ons", index.lower())
        self.assertIn("./styles.css", index)

        self.assertIn("--bg", styles)
        self.assertIn(".hero", styles)
        self.assertIn(".card-grid", styles)

        self.assertIn("spec-driven-development-starter-pack", post)
        self.assertIn("spec-kit", post)
        self.assertIn("Confira o repositório", post)


if __name__ == "__main__":
    unittest.main()
