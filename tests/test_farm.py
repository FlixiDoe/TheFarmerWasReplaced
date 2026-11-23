from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import costSystem
import plantSystem
import ressurceSystem
from scripts import update_readme_stamp


class CropCostTests(unittest.TestCase):
    def setUp(self):
        entities = SimpleNamespace(Carrot="Carrot", Pumpkin="Pumpkin", Sunflower="Sunflower")
        unlocks = SimpleNamespace(Carrots="Carrots", Pumpkins="Pumpkins", Sunflowers="Sunflowers")
        items = SimpleNamespace(Hay="Hay", Wood="Wood", Carrot="Carrot")
        self.unlocked = set()
        self.costs = {"Carrot": {"Hay": 7, "Wood": 5}, "Pumpkin": {"Carrot": 3}, "Sunflower": {"Carrot": 2}}
        self.queries = []
        def get_cost(entity):
            self.queries.append(entity)
            return self.costs[entity]
        self.inventory = {}
        self.planted = []
        for mod, name, value in [
            (costSystem, "Entities", entities), (costSystem, "Unlocks", unlocks),
            (costSystem, "Items", items), (costSystem, "get_cost", get_cost),
            (costSystem, "num_unlocked", lambda key: int(key in self.unlocked)),
            (plantSystem, "Entities", entities), (plantSystem, "Unlocks", unlocks),
            (plantSystem, "plant", self.planted.append),
            (plantSystem.ensureSystem, "ensureSoil", lambda: None),
            (plantSystem.unlockSystem, "num_unlocked", lambda key: int(key in self.unlocked)),
            (ressurceSystem, "Items", items),
            (ressurceSystem, "num_items", lambda item: self.inventory.get(item, 0)),
        ]:
            self.enterContext(patch.object(mod, name, value, create=True))

    def test_skips_cost_queries_for_locked_crops(self):
        costSystem.setCosts()
        self.assertEqual(self.queries, [])

    def test_sunflower_uses_own_price_after_refresh(self):
        self.unlocked.update(["Carrots", "Pumpkins", "Sunflowers"])
        costSystem.setCosts()
        self.assertIn("Sunflower", self.queries)
        self.inventory["Carrot"] = 1
        self.assertFalse(ressurceSystem.SunflowerRessurces())
        self.inventory["Carrot"] = 2
        self.assertTrue(ressurceSystem.SunflowerRessurces())

    def test_planting_uses_all_items_in_the_current_recipe(self):
        self.unlocked.add("Sunflowers")
        self.costs["Sunflower"] = {"Carrot": 3, "Hay": 2}
        costSystem.setCosts()
        self.assertEqual(self.queries, ["Sunflower"])
        self.inventory.update({"Carrot": 3, "Hay": 1})
        with patch.object(plantSystem, "plantGrass") as grass:
            plantSystem.plantSunflower()
            grass.assert_called_once_with()
        self.assertEqual(self.planted, [])
        self.inventory["Hay"] = 2
        plantSystem.plantSunflower()
        self.assertEqual(self.planted, ["Sunflower"])


class DocumentationTests(unittest.TestCase):
    def test_documents_each_active_field_route(self):
        section = update_readme_stamp.build_generated_block().split("### Field Layout")[1].split("### Module Overview")[0]
        self.assertEqual(section.count(" -> "), 6)
        self.assertIn("PumkinPlace", section)
        self.assertIn("plantTree", section)
        self.assertIn("plantGrass", section)
        self.assertNotIn("startSunflowerPlant", section)


class ReadmeUpdateTests(unittest.TestCase):
    def setUp(self):
        directory = self.enterContext(TemporaryDirectory(dir=update_readme_stamp.REPO_ROOT))
        self.readme = Path(directory) / "Readme.md"
        self.enterContext(patch.object(update_readme_stamp, "README_PATH", self.readme))
        self.enterContext(redirect_stdout(StringIO()))

    def test_marker_mentions_in_prose_leave_handwritten_content_intact(self):
        start = update_readme_stamp.START_MARKER
        end = update_readme_stamp.END_MARKER
        before = (f"# Farm notes\n\nThe section opens with `{start}`.\n"
                  f"Keep these notes.\nThe section closes with `{end}`.\n\n")
        after = "\nKeep these notes too.\n"
        self.readme.write_text(f"{before}{start}\nStale snapshot\n{end}\n{after}", encoding="utf-8")

        self.assertEqual(update_readme_stamp.main(), 0)
        updated = self.readme.read_text(encoding="utf-8")
        self.assertTrue(updated.startswith(f"{before}{start}\n## Generated Snapshot\n"), updated)
        self.assertTrue(updated.endswith(f"{end}\n{after}"), updated)
        self.assertNotIn("Stale snapshot", updated)

    def test_duplicate_marker_lines_leave_the_readme_intact(self):
        start = update_readme_stamp.START_MARKER
        end = update_readme_stamp.END_MARKER
        for markers in [(start, start, end), (start, end, end)]:
            with self.subTest(markers=markers):
                original = "\nKeep this text.\n".join(markers) + "\n"
                self.readme.write_text(original, encoding="utf-8")

                result = update_readme_stamp.main()

                self.assertEqual(self.readme.read_text(encoding="utf-8"), original)
                self.assertEqual(result, 1)
