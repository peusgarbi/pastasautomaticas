import json
from pathlib import Path
from pydantic import BaseModel


class Surgeon(BaseModel):
    crm: str
    prefixo: str = ""
    rqe: str = ""
    especialidade: str = ""


MOCK_SURGEONS = {
    "FULANO DA SILVA SAURO": {
        "prefixo": "Dr.",
        "crm": "123456",
        "rqe": "12345",
        "especialidade": "Otorrinolaringologista",
    }
}


def ensure_config_exists():
    config_dir = Path("config")

    config_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    surgeons_file = config_dir / "surgeons.json"

    if surgeons_file.exists():
        return False

    surgeons_file.write_text(
        json.dumps(
            MOCK_SURGEONS,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return True


class SurgeonRepository:
    def __init__(
        self,
        config_file: Path,
    ):
        self.config_file = config_file
        self.surgeons: dict[str, Surgeon] = {}

    def load(self) -> None:

        if not self.config_file.exists():
            self.surgeons = {}
            return

        data = json.loads(self.config_file.read_text(encoding="utf-8"))

        self.surgeons = {name: Surgeon(**info) for name, info in data.items()}

    def save(self) -> None:
        data = {name: surgeon.model_dump() for name, surgeon in self.surgeons.items()}

        self.config_file.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def exists(
        self,
        surgeon_name: str,
    ) -> bool:

        return surgeon_name in self.surgeons

    def remove(
        self,
        surgeon_name: str,
    ):

        if surgeon_name not in self.surgeons:
            return

        del self.surgeons[surgeon_name]

        self.save()

    def update(
        self,
        original_name: str,
        new_name: str,
        surgeon: Surgeon,
    ):

        if original_name != new_name and new_name in self.surgeons:
            raise ValueError(f"Já existe um cirurgião chamado '{new_name}'.")

        if original_name != new_name and original_name in self.surgeons:
            del self.surgeons[original_name]

        self.surgeons[new_name] = surgeon

        self.save()

    def add(
        self,
        name: str,
        surgeon: Surgeon,
    ):

        if name in self.surgeons:
            raise ValueError(f"Cirurgião já cadastrado: {name}")

        self.surgeons[name] = surgeon

        self.save()

    def get(
        self,
        surgeon_name: str,
    ) -> Surgeon | None:

        return self.surgeons.get(surgeon_name)


surgeon_repository = SurgeonRepository(Path("config/surgeons.json"))
