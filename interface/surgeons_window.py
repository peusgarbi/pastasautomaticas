from interface.surgeon_form import SurgeonForm
from src.config import surgeon_repository
from tkinter import ttk, messagebox
import customtkinter as ctk


class SurgeonsWindow(ctk.CTkToplevel):
    def __init__(
        self,
        parent,
    ):
        super().__init__(parent)
        self.iconbitmap("assets/icon.ico")

        self.title("Cadastro de Cirurgiões")
        self.geometry("800x500")

        # Trazer para frente
        self.lift()

        # Ficar acima da janela principal
        self.attributes("-topmost", True)

        # Remover topmost após abrir
        self.after(
            100,
            lambda: self.attributes(
                "-topmost",
                False,
            ),
        )

        self.surgeon_form = None

        self.create_widgets()
        self.load_surgeons()

    def create_widgets(self):

        #
        # TÍTULO
        #

        self.title_label = ctk.CTkLabel(
            self,
            text="Cirurgiões Cadastrados",
            font=("Calibri", 18, "bold"),
        )

        self.title_label.pack(pady=(20, 10))

        #
        # LISTA
        #

        columns = (
            "nome",
            "crm",
        )

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
        )

        self.tree.heading(
            "nome",
            text="Nome",
        )

        self.tree.heading(
            "crm",
            text="CRM",
        )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10,
        )

        #
        # BOTÕES
        #

        self.buttons_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.buttons_frame.pack(
            pady=10,
        )

        self.add_button = ctk.CTkButton(
            self.buttons_frame,
            text="Adicionar",
            command=self.add_surgeon,
        )

        self.add_button.pack(
            side="left",
            padx=5,
        )

        self.edit_button = ctk.CTkButton(
            self.buttons_frame,
            text="Editar",
            command=self.edit_surgeon,
        )

        self.edit_button.pack(
            side="left",
            padx=5,
        )

        self.delete_button = ctk.CTkButton(
            self.buttons_frame,
            text="Excluir",
            command=self.delete_surgeon,
        )

        self.delete_button.pack(
            side="left",
            padx=5,
        )

    def load_surgeons(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for name, surgeon in sorted(surgeon_repository.surgeons.items()):
            self.tree.insert(
                "",
                "end",
                values=(
                    name,
                    surgeon.crm,
                ),
            )

    def get_selected_surgeon_name(
        self,
    ) -> str | None:

        selection = self.tree.selection()

        if not selection:
            return None

        item = self.tree.item(selection[0])

        return item["values"][0]

    def edit_surgeon(self):
        surgeon_name = self.get_selected_surgeon_name()

        if not surgeon_name:
            ...
            return

        if self.surgeon_form and self.surgeon_form.winfo_exists():
            self.surgeon_form.focus()

            return

        self.surgeon_form = SurgeonForm(
            self,
            surgeon_name,
        )

    def add_surgeon(self):

        if self.surgeon_form and self.surgeon_form.winfo_exists():
            self.surgeon_form.focus()
            return

        self.surgeon_form = SurgeonForm(
            parent=self,
            surgeon_name=None,
        )

    def delete_surgeon(self):

        surgeon_name = self.get_selected_surgeon_name()

        if not surgeon_name:
            messagebox.showwarning(
                "Selecione um cirurgião",
                "Selecione um cirurgião para excluir.",
            )

            return

        confirm = messagebox.askyesno(
            "Confirmar exclusão",
            (f"Deseja realmente excluir:\n\n{surgeon_name}?"),
        )

        if not confirm:
            return

        surgeon_repository.remove(surgeon_name)

        self.load_surgeons()
