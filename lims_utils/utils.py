import json
import os
from pathlib import Path
from typing import Any, Union

archivePath = Path("archive")


def save_file(filename: Path, data: Union[dict, list]):
    with open(filename, "w+") as f:
        json.dump(data, f, indent=2)


def save_text(filename: Path, text: str):
    with open(filename, "w+") as f:
        f.write(text)


def load_file(filename: Path) -> Any:
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return None


def load_text(filename: Path) -> Union[str, None]:
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return f.read()
    return None
