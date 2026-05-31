from src.generate_companion_declaration import generate_companion_declaration
from src.medical_certificate_generator import generate_medical_certificate
from src.receipt_generator import generate_discharge_prescription
from pydantic import BaseModel, Field
from src.config import SURGEONS
from pathlib import Path
import re


class Surgery(BaseModel):
    sala: int
    horario: str
    paciente: str
    sexo: str
    idade: int
    nascimento: str
    endereco: str
    cirurgiao: str
    acomodacao: str
    convenio: str
    plano: str
    procedimentos: list[str] = Field(default_factory=list)
    materiais: list[str] = Field(default_factory=list)
    observacoes: str = ""

    def normalized_procedures(self) -> list[str]:
        """
        Regras de negócio para busca de modelos.
        Pode evoluir sem impactar o parser.
        """
        return [proc.strip() for proc in self.procedimentos]

    def sorted_procedures(self) -> list[str]:
        return sorted(self.procedimentos)

    @property
    def is_child(self) -> bool:
        return self.idade < 18

    @property
    def faixa_etaria(self) -> str:
        return "CRIANCA" if self.is_child else "ADULTO"

    def surgeon_folder(self) -> str:
        return self.cirurgiao.replace("/", "_").strip()

    def procedure_key(self) -> str:
        procedimentos = [
            re.sub(r"\s+", " ", proc).strip() for proc in self.procedimentos
        ]

        return "+".join(sorted(procedimentos))

    @property
    def recipe_filename(self) -> str:
        return f"{self.procedure_key()}.txt"

    def recipe_template_path(
        self,
        recipes_root: Path,
    ) -> Path:

        return recipes_root / self.cirurgiao / self.faixa_etaria / self.recipe_filename

    def get_recipe_text(
        self,
        recipes_root: Path,
    ) -> str:

        recipe_path = self.recipe_template_path(recipes_root)

        if not recipe_path.exists():
            raise FileNotFoundError(f"Receita não encontrada: {recipe_path}")

        return recipe_path.read_text(encoding="utf-8")

    @property
    def surgeon_crm(self) -> str:
        surgeon = SURGEONS.get(self.cirurgiao)
        if surgeon is None:
            return ""
        return SURGEONS[self.cirurgiao].crm

    def generate_receipt(self, surgery_date: str) -> Path:
        receipt_txt = self.get_recipe_text(Path("receitas"))
        receipt_path = generate_discharge_prescription(
            self.paciente,
            self.idade,
            self.sexo,
            self.endereco,
            self.cirurgiao,
            self.surgeon_crm,
            receipt_txt,
            Path("impressos"),
            surgery_date,
        )
        return receipt_path

    def generate_certificate(self, surgery_date: str) -> Path:
        certificate_path = generate_medical_certificate(
            self.paciente,
            self.idade,
            self.sexo,
            self.endereco,
            self.cirurgiao,
            self.surgeon_crm,
            Path("impressos"),
            surgery_date,
        )
        return certificate_path

    def generate_companion_declaration(self, surgery_date: str) -> Path:
        declaration_path = generate_companion_declaration(
            self.paciente,
            self.idade,
            self.sexo,
            self.endereco,
            self.cirurgiao,
            self.surgeon_crm,
            Path("impressos"),
            surgery_date,
        )
        return declaration_path
