from src.config import surgeon_repository


def generate_surgeon_signature(
    surgeon_name: str,
) -> str:
    surgeon = surgeon_repository.get(surgeon_name)

    #
    # Nome
    #

    if surgeon.prefixo:
        name_line = f"{surgeon.prefixo} {surgeon_name}"
    else:
        name_line = surgeon_name

    #
    # Segunda linha
    #

    if surgeon.especialidade:
        specialty_line = f"MÉDICO {surgeon.especialidade.upper()}"

    else:
        specialty_line = "MÉDICO"

    #
    # CRM / RQE
    #

    crm_line = f"CRM {surgeon.crm}"

    if surgeon.rqe:
        crm_line += f" | RQE {surgeon.rqe}"

    return f"{name_line}\n{specialty_line}\n{crm_line}"
