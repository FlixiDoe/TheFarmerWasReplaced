from collections import Counter
from dataclasses import dataclass
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import costSystem
import ensureSystem
import HarvestSystem
import movingSystem
import needSystem
import placeSystem
import plantSystem
import ressurceSystem
import unlockSystem


def names(*values):
    return SimpleNamespace(**{value: value for value in values})


@dataclass
class Tile:
    entity: str | None = "Grass"
    ground: str = "Grassland"
    ready: bool = False
    water: int = 0


class FakeFarm:
    """Single drone with explicit crop outcomes and a bounded API call count."""

    size = 7
    recipes = {"Pumpkin": {"Carrot": 2}, "Carrot": {"Hay": 1, "Wood": 1}}

    def __init__(self):
        self.position = (3, 0)
        self.tiles = {(x, y): Tile() for x in range(self.size) for y in range(self.size)}
        self.inventory = Counter()
        self.unlocked = {"Carrots", "Pumpkins", "Watering"}
        self.death_on_next_readiness_check = set()
        self.moves = []
        self.plants = []
        self.harvests = []
        self.calls_left = 250

    @property
    def tile(self):
        return self.tiles[self.position]

    def install(self, test):
        api = {
            "Entities": names("Grass", "Carrot", "Pumpkin", "Dead_Pumpkin", "Sunflower", "Tree", "Bush"),
            "Grounds": names("Soil", "Grassland"),
            "Unlocks": names("Carrots", "Pumpkins", "Sunflowers", "Watering", "Trees"),
            "Items": names("Hay", "Wood", "Carrot", "Pumpkin", "Water"),
            "North": "North",
            "East": "East",
        }
        actions = {
            "get_world_size": lambda: self.size,
            "get_pos_x": lambda: self.position[0],
            "get_pos_y": lambda: self.position[1],
            "get_companion": lambda: None,
            "get_entity_type": lambda: self.tile.entity,
            "get_ground_type": lambda: self.tile.ground,
            "get_water": lambda: self.tile.water,
            "num_unlocked": lambda unlock: int(unlock in self.unlocked),
            "num_items": self.inventory.__getitem__,
            "get_cost": self.recipes.__getitem__,
            "can_harvest": self.can_harvest,
            "harvest": self.harvest,
            "plant": self.plant,
            "till": self.till,
            "use_item": self.use_item,
            "move": self.move,
        }
        api.update({name: self.bounded(action) for name, action in actions.items()})
        for module in (costSystem, ensureSystem, HarvestSystem, movingSystem, needSystem,
                       placeSystem, plantSystem, ressurceSystem, unlockSystem):
            test.enterContext(patch.multiple(module, create=True, **api))
        test.enterContext(patch.multiple(costSystem, carrotCosts=[-1, -1], pumkinCosts=[-1]))

    def bounded(self, action):
        def call(*args):
            self.calls_left -= 1
            if self.calls_left < 0:
                raise AssertionError(
                    f"Game API budget exhausted at {self.position} after "
                    f"{len(self.moves)} moves and {len(self.plants)} plant attempts "
                    f"with {self.tile.entity} and {self.inventory['Carrot']} carrots"
                )
            return action(*args)
        return call

    def move(self, direction):
        x, y = self.position
        self.moves.append(direction)
        if direction == "North":
            self.position = (x, (y + 1) % self.size)
        else:
            self.position = ((x + 1) % self.size, y)
        return True

    def till(self):
        tile = self.tile
        tile.ground = "Grassland" if tile.ground == "Soil" else "Soil"
        tile.entity = "Grass" if tile.ground == "Grassland" else None
        tile.ready = False

    def can_harvest(self):
        tile = self.tile
        if tile.entity == "Pumpkin" and self.position in self.death_on_next_readiness_check:
            self.death_on_next_readiness_check.remove(self.position)
            tile.entity = "Dead_Pumpkin"
            tile.ready = False
        return tile.ready

    def harvest(self):
        tile = self.tile
        if not tile.ready:
            raise AssertionError(f"Harvested an unready tile at {self.position}")
        self.harvests.append((self.position, tile.entity))
        item = {"Grass": "Hay", "Carrot": "Carrot", "Pumpkin": "Pumpkin"}[tile.entity]
        self.inventory[item] += 1
        tile.entity = "Grass" if tile.ground == "Grassland" else None
        tile.ready = False
        return True

    def plant(self, entity):
        self.plants.append((self.position, entity))
        tile = self.tile
        required_ground = "Soil" if entity in self.recipes else "Grassland"
        cost = self.recipes.get(entity, {})
        if tile.ground != required_ground or tile.entity not in (None, "Grass", "Dead_Pumpkin"):
            return False
        if any(self.inventory[item] < amount for item, amount in cost.items()):
            return False
        self.inventory.subtract(cost)
        tile.entity = entity
        tile.ready = False
        return True

    def use_item(self, item):
        if item != "Water" or self.inventory[item] < 1:
            raise AssertionError(f"Unexpected item use: {item}")
        self.inventory[item] -= 1
        self.tile.water = 1
        return True


class MovementTests(unittest.TestCase):
    def setUp(self):
        self.farm = FakeFarm()
        self.farm.install(self)

    def run_column(self):
        costSystem.setCosts()
        movingSystem.startMove()

    def test_last_carrots_spent_on_pumpkin_that_dies(self):
        farm = self.farm
        farm.tiles[3, 0] = Tile("Dead_Pumpkin", "Soil")
        farm.inventory["Carrot"] = 2
        farm.inventory["Water"] = 1
        farm.death_on_next_readiness_check.add((3, 0))

        self.run_column()

        self.assertEqual(farm.moves, ["North"] * 7 + ["East"])
        self.assertEqual(farm.position, (4, 0))
        self.assertEqual(farm.inventory["Carrot"], 0)
        self.assertEqual(farm.inventory["Water"], 0)
        self.assertEqual(farm.tiles[3, 0], Tile("Pumpkin", "Soil", water=1))
        self.assertEqual([pos for pos, entity in farm.plants if entity == "Pumpkin"], [(3, 0)])

        farm.position = (3, 0)
        farm.inventory["Carrot"] = 2
        self.run_column()

        self.assertEqual(farm.position, (4, 0))
        self.assertEqual(farm.inventory["Carrot"], 0)
        self.assertEqual(farm.tiles[3, 0], Tile("Pumpkin", "Soil", water=1))
        self.assertEqual([pos for pos, entity in farm.plants if entity == "Pumpkin"], [(3, 0), (3, 0)])
        self.assertEqual(farm.harvests, [])

    def test_short_inventory_preserves_immature_pumpkin_and_carrot(self):
        farm = self.farm
        pumpkin = Tile("Pumpkin", "Soil")
        carrot = Tile("Carrot", "Soil")
        farm.tiles[3, 0] = pumpkin
        farm.tiles[1, 0] = carrot
        farm.inventory["Water"] = 1

        self.run_column()
        farm.position = (1, 0)
        self.run_column()

        self.assertEqual(pumpkin, Tile("Pumpkin", "Soil", water=1))
        self.assertEqual(carrot, Tile("Carrot", "Soil"))
        self.assertEqual(farm.harvests, [])

    def test_harvests_ready_pumpkin_and_replants_only_affordable_plot(self):
        farm = self.farm
        farm.tiles[3, 0] = Tile("Pumpkin", "Soil", ready=True)
        farm.tiles[3, 1] = Tile("Dead_Pumpkin", "Soil")
        farm.tiles[3, 2] = Tile("Pumpkin", "Soil")
        farm.inventory["Carrot"] = 2

        self.run_column()

        self.assertEqual(farm.harvests, [((3, 0), "Pumpkin")])
        self.assertEqual(farm.inventory["Pumpkin"], 1)
        self.assertEqual(farm.tiles[3, 0], Tile("Pumpkin", "Soil"))
        self.assertEqual(farm.tiles[3, 1], Tile())
        self.assertEqual(farm.tiles[3, 2], Tile("Pumpkin", "Soil"))
        self.assertEqual([pos for pos, entity in farm.plants if entity == "Pumpkin"], [(3, 0)])

    def test_skips_occupied_tree_plot_and_keeps_alternation(self):
        farm = self.farm
        farm.unlocked.add("Trees")
        farm.tiles[3, 0] = Tile("Carrot", "Soil")
        with patch.object(plantSystem, "isTree", False):
            plantSystem.plantTree()
            farm.move("North")
            plantSystem.plantTree()
        self.assertEqual(farm.tiles[3, 0], Tile("Carrot", "Soil"))
        self.assertEqual(farm.plants, [((3, 1), "Bush")])

    def test_affordable_pumpkins_stay_out_of_separator_and_remainder(self):
        farm = self.farm
        farm.inventory["Carrot"] = 14

        self.run_column()

        self.assertEqual([pos for pos, entity in farm.plants if entity == "Pumpkin"],
                         [(3, y) for y in range(5)])
        self.assertEqual(farm.tiles[3, 5], Tile())
        self.assertEqual(farm.tiles[3, 6], Tile())
        self.assertEqual(farm.inventory["Carrot"], 4)
