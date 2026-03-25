import importlib.util
import unittest
from pathlib import Path


def load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "starter_pack.py"
    spec = importlib.util.spec_from_file_location("starter_pack", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ProfileCatalogTests(unittest.TestCase):
    def test_catalog_exposes_five_ready_profiles_and_ten_total_profiles(self):
        module = load_module()
        starter_root = Path(__file__).resolve().parents[1]

        ready_profiles = module.list_profiles(starter_root)
        all_profiles = module.list_profiles(starter_root, include_planned=True)

        self.assertEqual(len(ready_profiles), 5)
        self.assertEqual(len(all_profiles), 10)


if __name__ == "__main__":
    unittest.main()
