from src.config import surgeon_repository
from src.config import Surgeon
from tkinter import messagebox
import customtkinter as ctk


class SurgeonForm(ctk.CTkToplevel):
    def __init__(
        self,
        parent,
        surgeon_name: str | None = None,
    ):
        super().__init__(parent)

        self.parent = parent
        self.original_name = surgeon_name
        self.surgeon_name = surgeon_name

        self.create_widgets()

        if surgeon_name:
            self.fill_form()

    def create_widgets(self):

        #
        # NOME
        #

        ctk.CTkLabel(
            self,
            text="Nome",
        ).pack(anchor="w", padx=20)

        self.name_entry = ctk.CTkEntry(
            self,
            width=400,
        )

        self.name_entry.pack(
            padx=20,
            pady=(0, 10),
        )

        #
        # PREFIXO
        #

        ctk.CTkLabel(
            self,
            text="Prefixo",
        ).pack(anchor="w", padx=20)

        self.prefix_combo = ctk.CTkComboBox(
            self,
            values=[
                "Dr.",
                "Dra.",
                "Prof. Dr.",
                "Profa. Dra.",
            ],
        )

        self.prefix_combo.pack(
            padx=20,
            pady=(0, 10),
        )

        #
        # CRM
        #

        ctk.CTkLabel(
            self,
            text="CRM",
        ).pack(anchor="w", padx=20)

        self.crm_entry = ctk.CTkEntry(
            self,
            width=400,
        )

        self.crm_entry.pack(
            padx=20,
            pady=(0, 10),
        )

        #
        # RQE
        #

        ctk.CTkLabel(
            self,
            text="RQE",
        ).pack(anchor="w", padx=20)

        self.rqe_entry = ctk.CTkEntry(
            self,
            width=400,
        )

        self.rqe_entry.pack(
            padx=20,
            pady=(0, 10),
        )

        #
        # ESPECIALIDADE
        #

        ctk.CTkLabel(
            self,
            text="Especialidade",
        ).pack(anchor="w", padx=20)

        self.specialty_entry = ctk.CTkEntry(
            self,
            width=400,
        )

        self.specialty_entry.pack(
            padx=20,
            pady=(0, 10),
        )

        #
        # BOTÃO
        #

        self.save_button = ctk.CTkButton(
            self,
            text="Salvar",
            command=self.save,
        )

        self.save_button.pack(
            pady=20,
        )

    def fill_form(self):
        surgeon = surgeon_repository.get(self.surgeon_name)

        if not surgeon:
            return

        self.name_entry.insert(
            0,
            self.surgeon_name,
        )

        self.prefix_combo.set(
            surgeon.prefixo,
        )

        self.crm_entry.insert(
            0,
            surgeon.crm,
        )

        self.rqe_entry.insert(
            0,
            surgeon.rqe or "",
        )

        self.specialty_entry.insert(
            0,
            surgeon.especialidade,
        )

    def save(self):
        name = self.name_entry.get().strip().upper()
        if not name:
            messagebox.showerror(
                "Erro",
                "Nome obrigatório.",
            )

            return

        surgeon = Surgeon(
            prefixo=self.prefix_combo.get(),
            crm=self.crm_entry.get().strip(),
            rqe=self.rqe_entry.get().strip(),
            especialidade=self.specialty_entry.get().strip(),
        )

        #
        # EDITAR
        #

        if self.original_name:
            try:
                surgeon_repository.update(
                    original_name=self.original_name,
                    new_name=name,
                    surgeon=surgeon,
                )

            except ValueError as e:
                messagebox.showerror(
                    "Erro",
                    str(e),
                )
                return

        #
        # ADICIONAR
        #

        else:
            surgeon_repository.add(
                name,
                surgeon,
            )

        #
        # Atualizar lista
        #

        self.parent.load_surgeons()

        #
        # Fechar janela
        #

        self.destroy()
