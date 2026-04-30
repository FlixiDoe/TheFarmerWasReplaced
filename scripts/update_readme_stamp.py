from datetime import datetime
from pathlib import Path
import re
from zoneinfo import ZoneInfo

# Pfad-Logik: SCRIPT_DIR ist /scripts, REPO_ROOT ist das Hauptverzeichnis
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

README_PATH = REPO_ROOT / "Readme.md"
TIMEZONE = ZoneInfo("Europe/Berlin")
START_MARKER = "<!-- AUTO_DOCS_CONTENT_START -->"
END_MARKER = "<!-- AUTO_DOCS_CONTENT_END -->"

# Hier habe ich die Liste basierend auf deinem 'ls' Befehl vervollständigt
MODULE_FILES = [
    "main.py",
    "plantSystem.py",
    "placeSystem.py",
    "unlockSystem.py",
    "costSystem.py",
    "ressurceSystem.py", # Beachte den Tippfehler (doppeltes 's', kein 'o')
    "needSystem.py",
    "ensureSystem.py",
    "helpers.py",
    "HarvestSystem.py",   # Neu hinzugefügt aus deinem Verzeichnis-Listing
    "movingSystem.py",    # Neu hinzugefügt
    "seedingSystem.py",   # Neu hinzugefügt
]

LOCAL_ONLY_FILES = ["__builtins__.py", "save.json"]

def read_file(filename: str) -> str:
    """Liest Dateien relativ zum Repo-Root."""
    file_path = REPO_ROOT / filename
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"⚠️ Warnung: Datei {filename} wurde nicht gefunden.")
        return ""

# ... (Die restlichen Parser-Funktionen parse_imports, parse_functions etc. bleiben gleich) ...

def parse_imports(content: str) -> list[str]:
    return re.findall(r"^import\s+([A-Za-z_][A-Za-z0-9_]*)", content, re.MULTILINE)

def parse_functions(content: str) -> list[str]:
    return re.findall(r"^def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", content, re.MULTILINE)

def format_inline_list(items: list[str]) -> str:
    if not items:
        return "none"
    return ", ".join(f"`{item}`" for item in items)

def parse_route_rules(content: str) -> list[tuple[str, str]]:
    lines = content.splitlines()
    routes: list[tuple[str, str]] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped: continue
        if (stripped.startswith("if ") or stripped.startswith("elif ")) and "x ==" in stripped:
            condition_parts = stripped.split("(", 1)
            condition = condition_parts[1].rsplit(")", 1)[0].strip() if len(condition_parts) > 1 else stripped
            action = find_next_action(lines, index + 1)
            routes.append((condition, action))
        elif stripped == "else:":
            action = find_next_action(lines, index + 1)
            routes.append(("fallback", action))
    return routes

def find_next_action(lines: list[str], start_index: int) -> str:
    call_pattern = re.compile(r"([A-Za-z_][A-Za-z0-9_\.]*)\((.*)\)")
    for line in lines[start_index:]:
        stripped = line.strip()
        if not stripped: continue
        match = call_pattern.match(stripped)
        if match: return f"`{match.group(1)}(...)`"
        return f"`{stripped}`"
    return "`unknown`"

def build_main_loop_section(main_content: str) -> list[str]:
    lines = [
        "## Generated Snapshot",
        "",
        f"Generated from the current repository files on {datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M Europe/Berlin')}.",
        "",
        "### Main Loop",
        "",
        "- Entry point: `main.py`.",
        f"- Imports: {format_inline_list(parse_imports(main_content))}.",
    ]
    if "costSystem.setCosts()" in main_content:
        lines.append("- Refreshes crop costs once per full world pass with `costSystem.setCosts()`.")
    if "can_harvest()" in main_content and "harvest()" in main_content:
        lines.append("- Harvests a tile before replanting when `can_harvest()` is true.")
    
    lines.extend(["", "### Field Layout", ""])
    for condition, action in parse_route_rules(main_content):
        if condition == "fallback":
            lines.append(f"- Fallback route -> {action}.")
        else:
            lines.append(f"- `{condition}` -> {action}.")
    return lines

def build_module_section() -> list[str]:
    lines = ["", "### Module Overview", ""]
    for module_path in MODULE_FILES:
        content = read_file(module_path)
        if not content: continue
        imports = parse_imports(content)
        functions = parse_functions(content)
        lines.append(f"- `{module_path}`")
        lines.append(f"  Imports: {format_inline_list(imports)}.")
        lines.append(f"  Functions: {format_inline_list(functions)}.")
    return lines

def build_maintenance_notes() -> list[str]:
    lines = ["", "### Detected Maintenance Notes", ""]
    todo_hits: list[str] = []
    for module_path in MODULE_FILES:
        content = read_file(module_path)
        if "TODO" in content:
            todo_hits.append(f"`{module_path}` contains a TODO marker.")

    naming_hits = ["`PumkinPlace`", "`pumkinCosts`", "`ressurceSystem`", "`entitiyIsUnlocked`"]
    if todo_hits:
        lines.extend(f"- {item}" for item in todo_hits)
    lines.append(f"- Current naming inconsistencies detected in code: {', '.join(naming_hits)}.")
    lines.append(f"- Local-only files excluded from Git: {format_inline_list(LOCAL_ONLY_FILES)}.")
    lines.append("- This section is regenerated by `.github/workflows/daily-docs.yml`.")
    return lines

def build_generated_block() -> str:
    main_content = read_file("main.py")
    lines: list[str] = []
    if main_content:
        lines.extend(build_main_loop_section(main_content))
    lines.extend(build_module_section())
    lines.extend(build_maintenance_notes())
    return "\n".join(lines).rstrip()

def main() -> int:
    if not README_PATH.exists():
        print(f"Error: {README_PATH} nicht gefunden!")
        return 1
        
    readme = README_PATH.read_text(encoding="utf-8")
    start_index = readme.find(START_MARKER)
    end_index = readme.find(END_MARKER)
    
    if start_index == -1 or end_index == -1 or end_index < start_index:
        print("Fehler: Marker <!-- AUTO_DOCS_CONTENT_START --> nicht in Readme.md gefunden.")
        return 1

    generated_content = build_generated_block()
    
    # Wir behalten den Marker selbst bei
    updated = (
        readme[:start_index] + 
        START_MARKER + "\n" + 
        generated_content + "\n" + 
        readme[end_index:]
    )

    if updated == readme:
        print("README bereits aktuell.")
        return 0

    README_PATH.write_text(updated, encoding="utf-8")
    print("README erfolgreich aktualisiert.")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())