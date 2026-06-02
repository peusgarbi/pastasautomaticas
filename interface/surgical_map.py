from src.empty_docx import create_empty_docx
from src.config import surgeon_repository
from src.models import Surgery
import customtkinter as ctk
from pathlib import Path
from tkinter import ttk
import os


class SurgicalMapWindow(ctk.CTkToplevel):
    def __init__(
        self,
        parent,
        surgeries: list[Surgery],
    ):
        super().__init__(parent)

        self.surgeries = surgeries

        self.title("Mapa Cirúrgico")
        self.geometry("1400x700")

        self.lift()
        self.focus_force()
        self.grab_set()

        self.create_widgets()
        self.populate_table()

    def create_widgets(self):

        #
        # TABELA
        #

        columns = (
            "hora",
            "paciente",
            "cirurgiao",
            "procedimento",
            "receita",
            "orientacao",
        )

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
        )

        self.tree.heading(
            "hora",
            text="Hora",
        )

        self.tree.heading(
            "paciente",
            text="Paciente",
        )

        self.tree.heading(
            "cirurgiao",
            text="Cirurgião",
        )

        self.tree.heading(
            "procedimento",
            text="Procedimento",
        )

        self.tree.heading(
            "receita",
            text="Receita",
        )

        self.tree.heading(
            "orientacao",
            text="Orientação",
        )

        self.tree.column(
            "hora",
            width=10,
            anchor="center",
        )

        self.tree.column(
            "paciente",
            width=150,
        )

        self.tree.column(
            "cirurgiao",
            width=150,
        )

        self.tree.column(
            "procedimento",
            width=400,
        )

        self.tree.column(
            "receita",
            width=5,
            anchor="center",
        )

        self.tree.column(
            "orientacao",
            width=5,
            anchor="center",
        )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20,
        )

        #
        # CORES
        #

        self.tree.tag_configure(
            "ok",
            background="#DFF0D8",
        )

        self.tree.tag_configure(
            "warning",
            background="#FCF8E3",
        )

        self.tree.tag_configure(
            "error",
            background="#F2DEDE",
        )

        #
        # FRAME DOS BOTÕES
        #

        self.buttons_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.buttons_frame.pack(
            padx=20,
            pady=(0, 20),
        )

        #
        # BOTÃO RECEITA
        #

        self.recipe_button = ctk.CTkButton(
            self.buttons_frame,
            text="Abrir Receita",
            command=self.open_recipe,
        )

        self.recipe_button.pack(
            side="left",
            padx=(0, 10),
        )

        #
        # BOTÃO PASTA RECEITA
        #

        self.recipe_folder_button = ctk.CTkButton(
            self.buttons_frame,
            text="Abrir pasta da Receita",
            command=self.open_recipe_folder,
        )

        self.recipe_folder_button.pack(
            side="left",
            padx=(0, 10),
        )

        #
        # BOTÃO ORIENTAÇÃO GENÉRICA
        #

        self.generic_orientation_button = ctk.CTkButton(
            self.buttons_frame,
            text="Abrir Orientação Genérica",
            command=self.open_generic_orientation,
        )

        self.generic_orientation_button.pack(
            side="left",
            padx=(0, 10),
        )

        #
        # BOTÃO ORIENTAÇÃO GENÉRICA PASTA
        #

        self.orientation_folder_button = ctk.CTkButton(
            self.buttons_frame,
            text="Abrir pasta de Orientações Genéricas",
            command=self.open_generic_orientation_folder,
        )

        self.orientation_folder_button.pack(
            side="left",
            padx=(0, 10),
        )

        #
        # BOTÃO ORIENTAÇÃO ESPECÍFICA
        #

        self.specifc_orientation_button = ctk.CTkButton(
            self.buttons_frame,
            text="Abrir Orientação Específica do Médico",
            command=self.open_specific_orientation,
        )

        self.specifc_orientation_button.pack(
            side="left",
            padx=(0, 10),
        )

        #
        # BOTÃO ORIENTAÇÃO ESPECÍFICA PASTA
        #

        self.specifc_orientation_button = ctk.CTkButton(
            self.buttons_frame,
            text="Abrir pasta de Orientação Específica do Médico",
            command=self.open_specific_orientation_folder,
        )

        self.specifc_orientation_button.pack(
            side="left",
            padx=(0, 10),
        )

        #
        # BOTÃO ATUALIZAR
        #

        self.refresh_button = ctk.CTkButton(
            self.buttons_frame,
            text="Atualizar Tabela",
            command=self.refresh_table,
        )

        self.refresh_button.pack(
            side="left",
            padx=(0, 10),
        )

    def populate_table(self):
        for index, surgery in enumerate(self.surgeries):
            surgeon_exists = surgery.cirurgiao in surgeon_repository.surgeons

            specific_orientation_path, generic_orientation_path = (
                surgery.orientation_template_path()
            )
            specific_orientation_exists = specific_orientation_path.exists()
            generic_orientation_exists = generic_orientation_path.exists()

            try:
                recipe_exists = surgery.get_recipe_text(Path("receitas")) is not None
            except Exception:
                recipe_exists = False

            #
            # COR DA LINHA
            #

            if not surgeon_exists:
                tag = "error"

            elif recipe_exists and (
                specific_orientation_exists or generic_orientation_exists
            ):
                tag = "ok"

            else:
                tag = "warning"

            self.tree.insert(
                "",
                "end",
                values=(
                    surgery.horario,
                    surgery.paciente,
                    f"{'✔' if surgeon_exists else '⚠'} {surgery.cirurgiao}",
                    " + ".join(surgery.procedimentos),
                    "✔" if recipe_exists else "❌",
                    "👨‍⚕️"
                    if specific_orientation_exists
                    else "📘"
                    if generic_orientation_exists
                    else "❌",
                ),
                iid=str(index),
                tags=(tag,),
            )

    def get_selected_surgery(self):
        selected = self.tree.selection()

        if not selected:
            return None

        index = int(selected[0])

        return self.surgeries[index]

    def open_recipe(self):
        surgery = self.get_selected_surgery()

        if not surgery:
            return

        recipe_path = surgery.recipe_template_path(Path("receitas"))

        recipe_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not recipe_path.exists():
            recipe_path.write_text(
                "",
                encoding="utf-8",
            )

        os.startfile(recipe_path)

        self.refresh_table()

    def open_recipe_folder(self):
        surgery = self.get_selected_surgery()
        if not surgery:
            return

        recipe_folder_path = surgery.recipe_template_path(Path("receitas")).parent

        recipe_folder_path.mkdir(
            parents=True,
            exist_ok=True,
        )
        os.startfile(recipe_folder_path)

    def open_generic_orientation(self):
        surgery = self.get_selected_surgery()

        if not surgery:
            return

        _, generic_orientation_path = surgery.orientation_template_path()

        generic_orientation_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not generic_orientation_path.exists():
            create_empty_docx(generic_orientation_path)

        os.startfile(generic_orientation_path)

        self.refresh_table()

    def open_generic_orientation_folder(self):
        os.startfile(Path("orientacoes"))

    def open_specific_orientation(self):
        surgery = self.get_selected_surgery()

        if not surgery:
            return

        specific_orientation_path, _ = surgery.orientation_template_path()

        specific_orientation_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not specific_orientation_path.exists():
            create_empty_docx(specific_orientation_path)

        os.startfile(specific_orientation_path)

        self.refresh_table()

    def open_specific_orientation_folder(self):
        surgery = self.get_selected_surgery()
        if not surgery:
            return

        specific_orientation_path, _ = surgery.orientation_template_path()

        specific_orientation_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        os.startfile(specific_orientation_path.parent)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.populate_table()
