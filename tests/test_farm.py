import unittest
from types import SimpleNamespace
from unittest.mock import patch

import costSystem
import plantSystem
import ressurceSystem
from scripts.update_readme_stamp import build_generated_block


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
        section = build_generated_block().split("### Field Layout")[1].split("### Module Overview")[0]
        self.assertEqual(section.count(" -> "), 6)
        self.assertIn("PumkinPlace", section)
        self.assertIn("plantTree", section)
        self.assertIn("plantGrass", section)
        self.assertNotIn("startSunflowerPlant", section)
