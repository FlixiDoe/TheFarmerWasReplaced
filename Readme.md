# The Farmer Was Replaced Automation System

This repository contains my modular farming script setup for **The Farmer Was Replaced**.
The goal is to keep the main loop small and move crop logic, unlock checks, and resource handling into separate modules.

## What the script does

`main.py` runs an endless farm loop and assigns crop types by column:

- `x == 0` or `11`: grass
- `x == 1`, `10`, `13`, `15`: trees
- `x == 2`, `8`, `9`, `12`, `14`: carrots
- `x == 3` to `7`: pumpkin area with spacing logic
- everything else: grass fallback

Before each full pass, the script refreshes crop costs with `costSystem.setCosts()`.
If a tile is harvestable, it gets harvested before replanting.

## Project structure

- `main.py`: main farm loop and field layout
- `plantSystem.py`: planting functions for grass, carrots, pumpkins, trees, and the unfinished sunflower stub
- `placeSystem.py`: decides where pumpkins may be planted inside the pumpkin zone
- `unlockSystem.py`: checks whether items or entities are unlocked
- `ressurceSystem.py`: verifies whether enough materials are available for carrots and pumpkins
- `costSystem.py`: reads current in-game crop costs
- `needSystem.py`: uses water and fertilizer if unlocked and available
- `ensureSystem.py`: switches between ground and soil
- `helpers.py`: small movement helper

## How it works

### Crop handling

- Grass is used as the safe fallback if something is locked or resources are missing.
- Carrots are only planted when hay and wood are available.
- Pumpkins are only planted when enough carrots are available.
- Trees alternate between `Tree` and `Bush` using the global `isTree` flag.

### Pumpkin placement

Pumpkins are not planted on every tile in their column range.
`placeSystem.PumkinPlace(5)` creates gaps based on the current `y` position and world size so the pumpkin section stays structured.

### Unlock and safety behavior

If an entity is still locked, the system falls back to planting grass.
That keeps the farm running even when a save is still progressing.

## Requirements

This code is written for the in-game Python-like environment of **The Farmer Was Replaced**.
It is not meant to run as normal desktop Python.

The project expects the game-provided builtins such as:

- `plant`
- `harvest`
- `move`
- `get_cost`
- `num_items`
- `num_unlocked`
- `get_world_size`

## Usage

1. Copy the repository files into your save script folder.
2. Use `main.py` as the entry point.
3. Adjust the column layout in `main.py` if you want a different farm design.
4. Expand the helper systems as new unlocks become available.

## Notes

- `__builtins__.py` and `save.json` are intentionally kept local and are not part of the Git history.
- `plantSunflower()` is currently only a placeholder.
- Several names in the code still reflect early versions, for example `PumkinPlace` and `ressurceSystem`.

## Planned improvements

- finish sunflower support
- improve naming consistency
- make field layout configurable instead of hard-coded by column
- extend fertilizer handling for pumpkins
