from src.models import Surgery
from src.config import Surgeon
import re


def extract_surgery_date(text: str) -> str:
    match = re.search(r"Data:\s*(\d{2}/\d{2}/\d{2})", text)

    if not match:
        raise ValueError("Data não encontrada no relatório")

    return match.group(1)


def split_surgeries(text: str) -> list[tuple[int, str]]:
    surgeries = []

    current_room = None

    room_pattern = re.compile(r"Sala de Cirurgia\s+(\d+)")

    lines = text.splitlines()

    current_block = []

    for line in lines:
        room_match = room_pattern.search(line)

        if room_match:
            current_room = int(room_match.group(1))
            continue

        if line.startswith("Horário:"):
            if current_block:
                surgeries.append((current_room, "\n".join(current_block)))

            current_block = [line]

        elif current_block:
            current_block.append(line)

    if current_block:
        surgeries.append((current_room, "\n".join(current_block)))

    return surgeries


def extract_procedures(block: str) -> list[str]:

    match = re.search(r"Serviços:\s*(.*?)\s*Plano:", block, re.S)

    if not match:
        return []

    services_text = match.group(1)

    services_text = services_text.replace("\n", " ")

    return [item.strip() for item in services_text.split("+") if item.strip()]


def extract_materials(block: str) -> list[str]:
    match = re.search(r"Materiais:\s*Autorizados:\s*(.*?)(?:Obs:|$)", block, re.S)

    if not match:
        return []

    materials_text = match.group(1)

    materials_text = materials_text.replace("\n", " ")

    return [item.strip() for item in materials_text.split("+") if item.strip()]


def extract_obs(block: str) -> str:
    match = re.search(r"Obs:\s*(.*)$", block, re.S)

    if not match:
        return ""

    return match.group(1).strip()


def parse_surgery(room: int, block: str) -> Surgery:
    header = re.search(
        r"Horário:\s*(.*?)\s+Paciente:\s*(.*?)\s+Sexo:\s*(.*?)\s+Idade:\s*(\d+).*?Nascimento:\s*([\d/]+)",
        block,
        re.S,
    )

    if not header:
        raise ValueError(f"Não foi possível extrair cabeçalho:\n{block}")

    endereco = re.search(r"Endereço:\s*(.*)", block)

    doctor = re.search(
        r"Cirurgião:\s*(.*?)\s+Acomodação\s+(.*?)\s+Convênio:\s*(.*)", block
    )

    plano = re.search(r"Plano:\s*(.*)", block)

    return Surgery(
        sala=room,
        horario=header.group(1).strip(),
        paciente=header.group(2).strip(),
        sexo=header.group(3).strip(),
        idade=int(header.group(4)),
        nascimento=header.group(5),
        endereco=endereco.group(1).strip(),
        cirurgiao=doctor.group(1).strip(),
        acomodacao=doctor.group(2).strip(),
        convenio=doctor.group(3).strip(),
        plano=plano.group(1).strip(),
        procedimentos=extract_procedures(block),
        materiais=extract_materials(block),
        observacoes=extract_obs(block),
    )


def extract_surgeries(text: str) -> list[Surgery]:
    surgeries = []

    for room, block in split_surgeries(text):
        try:
            surgeries.append(parse_surgery(room, block))

        except Exception as e:
            print(f"Erro ao processar cirurgia da sala {room}")
            print(e)

    return surgeries


def filter_registered_surgeons(
    surgeries: list[Surgery],
    surgeons: dict[str, Surgeon],
) -> tuple[list[Surgery], list[str]]:

    valid_surgeries: list[Surgery] = []
    missing_surgeons: set[str] = set()

    for surgery in surgeries:
        if surgery.cirurgiao in surgeons:
            valid_surgeries.append(surgery)
        else:
            missing_surgeons.add(surgery.cirurgiao)

    return (
        valid_surgeries,
        sorted(missing_surgeons),
    )
