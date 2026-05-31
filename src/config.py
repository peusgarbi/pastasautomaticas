import json
from pathlib import Path
from pydantic import BaseModel


class Surgeon(BaseModel):
    crm: str


def load_surgeons() -> dict[str, Surgeon]:

    config_file = Path("config") / "surgeons.json"

    if not config_file.exists():
        raise FileNotFoundError(
            f"Arquivo de configuração não encontrado: {config_file}"
        )

    with open(
        config_file,
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    return {name: Surgeon(**info) for name, info in data.items()}


SURGEONS = load_surgeons()
