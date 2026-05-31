from src.config import ensure_config_exists, surgeon_repository
from interface.interface import run
from tkinter import messagebox

created = ensure_config_exists()
if created:
    messagebox.showinfo(
        "Primeira execução",
        (
            "Foi criado um arquivo de configuração "
            "de exemplo.\n\n"
            "Acesse o menu 'Cirurgiões' para "
            "cadastrar os médicos."
        ),
    )


if __name__ == "__main__":
    surgeon_repository.load()
    run()
