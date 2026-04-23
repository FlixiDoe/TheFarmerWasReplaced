from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


README_PATH = Path("Readme.md")
START_MARKER = "<!-- AUTO_DOCS_UPDATE_START -->"
END_MARKER = "<!-- AUTO_DOCS_UPDATE_END -->"
TIMEZONE = ZoneInfo("Europe/Berlin")


def build_replacement() -> str:
    timestamp = datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M Europe/Berlin")
    return (
        f"{START_MARKER}\n"
        f"Last automated documentation update: {timestamp}\n"
        f"{END_MARKER}"
    )


def main() -> int:
    content = README_PATH.read_text(encoding="utf-8")

    start_index = content.find(START_MARKER)
    end_index = content.find(END_MARKER)
    if start_index == -1 or end_index == -1 or end_index < start_index:
        raise RuntimeError("README markers for automated docs update were not found.")

    end_index += len(END_MARKER)
    updated = content[:start_index] + build_replacement() + content[end_index:]

    if updated == content:
        print("README already up to date.")
        return 0

    README_PATH.write_text(updated, encoding="utf-8")
    print("Updated README documentation timestamp.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
