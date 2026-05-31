from src.models import Surgery
from pathlib import Path


def find_orientation_files(
    surgeries: list[Surgery],
) -> tuple[list[Path], list[str]]:

    files = []
    missing = []
    for surgery in surgeries:
        path = surgery.get_orientation_path()

        if path:
            files.append(path)

        else:
            missing.append(f"{surgery.cirurgiao}: {surgery.procedures_filename}")

    return files, missing
