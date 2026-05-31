from src.extractor import (
    extract_surgery_date,
    extract_surgeries,
    filter_registered_surgeons,
)
from src.find_orientation_files import find_orientation_files
from src.extract_text_from_pdf import extract_text_from_pdf
from interface.surgeons_window import SurgeonsWindow
from src.docx_merger import merge_docx_files
from src.resource_path import resource_path
from tkinter import filedialog, messagebox
from src.config import surgeon_repository
from src.version import VERSION
import customtkinter as ctk
from pathlib import Path
import ctypes
import os

myappid = "pedrosgarbi.geradorpastas.1.0"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(resource_path("assets/icon.ico"))

        self.pdf_path = None

        self._configure_window()
        self._create_widgets()

    def _configure_window(self):
        self.title(f"Gerador Automático de Pastas v{VERSION}")
        self.geometry("800x500")

    def _create_widgets(self):

        #
        # TÍTULO
        #

        self.title_label = ctk.CTkLabel(
            self,
            text="Gerador Automático de Pastas",
            font=("Calibri", 20, "bold"),
        )

        self.title_label.pack(pady=(20, 10))

        #
        # FRAME PDF
        #

        self.pdf_frame = ctk.CTkFrame(self)

        self.pdf_frame.pack(
            fill="x",
            padx=20,
            pady=10,
        )

        self.pdf_title = ctk.CTkLabel(self.pdf_frame, text="Agenda Cirúrgica (PDF)")

        self.pdf_title.pack(
            anchor="w",
            padx=10,
            pady=(10, 5),
        )

        self.pdf_path_label = ctk.CTkLabel(
            self.pdf_frame,
            text="Nenhum arquivo selecionado",
            anchor="w",
        )

        self.pdf_path_label.pack(
            fill="x",
            padx=10,
            pady=(0, 10),
        )

        #
        # FRAME DOS BOTÕES
        #

        self.buttons_frame = ctk.CTkFrame(
            self.pdf_frame,
            fg_color="transparent",
        )

        self.buttons_frame.pack(
            padx=10,
            pady=(0, 10),
        )

        #
        # BOTÃO SELECIONAR PDF
        #

        self.select_pdf_button = ctk.CTkButton(
            self.buttons_frame,
            text="Selecionar PDF",
            command=self.select_pdf,
        )

        self.select_pdf_button.pack(
            side="left",
            padx=(0, 10),
        )

        #
        # BOTÃO LIMPAR IMPRESSOS
        #

        self.clear_button = ctk.CTkButton(
            self.buttons_frame,
            text="Limpar Impressos",
            command=self.clear_prints,
        )
        self.clear_button.pack(
            side="left",
            padx=(0, 10),
        )

        #
        # BOTÃO CIRURGIÕES
        #

        self.surgeons_button = ctk.CTkButton(
            self.buttons_frame,
            text="Cirurgiões",
            command=self.open_surgeons_window,
        )
        self.surgeons_button.pack(
            side="left",
            padx=(0, 10),
        )

        #
        # FRAME DE AÇÕES
        #

        self.actions_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.actions_frame.pack(
            pady=20,
        )

        #
        # BOTÃO GERAR
        #

        self.generate_button = ctk.CTkButton(
            self.actions_frame,
            text="GERAR DOCUMENTOS",
            height=40,
            command=self.generate_receipts,
        )

        self.generate_button.pack(
            side="left",
            padx=10,
            pady=10,
        )

        #
        # BOTÃO ABRIR IMPRESSOS
        #

        self.open_prints_button = ctk.CTkButton(
            self.actions_frame,
            height=40,
            text="ABRIR IMPRESSOS",
            command=self.open_prints_folder,
        )

        self.open_prints_button.pack(
            side="left",
            padx=10,
            pady=10,
        )

        #
        # LOGS
        #

        self.logs_label = ctk.CTkLabel(self, text="Logs")

        self.logs_label.pack(
            anchor="w",
            padx=20,
        )

        self.logs = ctk.CTkTextbox(
            self,
            height=200,
        )

        self.logs.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 20),
        )

        self.logs.insert("end", "Aguardando arquivo PDF...\n")

        self.logs.configure(state="disabled")

    def open_surgeons_window(self):
        if hasattr(self, "surgeons_window"):
            if self.surgeons_window.winfo_exists():
                self.surgeons_window.focus()

                return

        self.surgeons_window = SurgeonsWindow(self)

    def select_pdf(self):

        pdf_path = filedialog.askopenfilename(
            title="Selecione a agenda cirúrgica", filetypes=[("Arquivos PDF", "*.pdf")]
        )

        if not pdf_path:
            return

        self.pdf_path = Path(pdf_path)

        self.pdf_path_label.configure(text=self.pdf_path.name)

    def add_log(self, message: str):

        self.logs.configure(state="normal")

        self.logs.insert("end", f"{message}\n")

        self.logs.see("end")

        self.logs.configure(state="disabled")

    def clear_prints(self):

        confirm = messagebox.askyesno(
            "Confirmar exclusão",
            (
                "Deseja realmente excluir todos os "
                "arquivos da pasta 'impressos'?\n\n"
                "Esta ação não pode ser desfeita."
            ),
        )

        if not confirm:
            return

        output_dir = Path("impressos")

        if not output_dir.exists():
            self.add_log("⚠ Pasta 'impressos' não encontrada.")

            return

        deleted = 0
        blocked = []

        for file in output_dir.iterdir():
            if not file.is_file():
                continue

            try:
                file.unlink()
                deleted += 1

            except PermissionError:
                blocked.append(file.name)

        self.add_log(f"🗑 {deleted} arquivo(s) removido(s) da pasta 'impressos'.")

        if blocked:
            messagebox.showwarning(
                "Arquivos em uso",
                (
                    "Os seguintes arquivos não puderam "
                    "ser removidos porque estão abertos:\n\n" + "\n".join(blocked)
                ),
            )

    def open_prints_folder(self):

        try:
            output_dir = Path("impressos")

            output_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            os.startfile(output_dir)

        except Exception as error:
            messagebox.showerror(
                "Erro",
                (f"Não foi possível abrir a pasta de impressos.\n\n{error}"),
            )

    def generate_receipts(self):

        if not self.pdf_path:
            self.add_log("❌ Nenhum PDF selecionado.")

            return

        self.generate_button.configure(state="disabled")

        try:
            self.add_log(f"📄 Processando {self.pdf_path.name}")

            texto = extract_text_from_pdf(self.pdf_path)
            surgery_date = extract_surgery_date(texto)
            surgeries = extract_surgeries(texto)
            self.add_log(
                f"⚠ {len(surgeries)} Cirurgias totais identificadas no arquivo."
            )

            surgeries, missing_surgeons = filter_registered_surgeons(
                surgeries, surgeon_repository.surgeons
            )
            if missing_surgeons:
                self.add_log("⚠ Cirurgiões não cadastrados:")
                for surgeon in missing_surgeons:
                    self.add_log(f"   • {surgeon}")
            self.add_log(f"⚠ {len(surgeries)} Cirurgias de cirurgiões cadastrados.")

            generated_receipts: int = 0
            not_generated_receipts: int = 0
            generated_certificates: int = 0
            generated_declarations: int = 0
            generated_files: list[Path] = []
            not_generated_patients: list[str] = []
            for surgery in surgeries:
                try:
                    file_path = surgery.generate_receipt(surgery_date)
                    generated_files.append(file_path)
                    generated_files.append(file_path)
                    generated_receipts += 1
                    file_path = surgery.generate_certificate(surgery_date)
                    generated_files.append(file_path)
                    generated_certificates += 1
                    file_path = surgery.generate_companion_declaration(surgery_date)
                    generated_files.append(file_path)
                    generated_declarations += 1

                except PermissionError as e:
                    messagebox.showerror(
                        "Arquivo em uso",
                        (
                            f"Não foi possível processar o documento {e.filename}.\n\n"
                            "Provavelmente o arquivo DOCX está aberto no Word.\n\n"
                            "Feche o documento e tente novamente."
                        ),
                    )
                except Exception as e:
                    self.add_log(f"❌ {e}")
                    not_generated_patients.append(surgery.paciente)
                    not_generated_receipts += 1

            self.add_log(f"✅ {generated_receipts} Receitas geradas com sucesso.")
            self.add_log(f"{generated_certificates} Atestados gerados.")
            self.add_log(
                f"{generated_declarations} Declarações de acompanhante geradas."
            )
            self.add_log(
                f"❌ {not_generated_receipts} Receitas não geradas devido a erro."
            )
            self.add_log(f"Pacientes pendentes: {not_generated_patients}")

            consolidated_path = merge_docx_files(
                generated_files, Path("impressos/RECEITAS CONSOLIDADAS.docx")
            )
            self.add_log(
                f"Arquivo com todas as receitas gerado em: {consolidated_path}"
            )

            orientation_files, missing_orientations = find_orientation_files(surgeries)
            self.add_log(f"✅ {len(orientation_files)} Orientações encontradas.")
            self.add_log(f"❌ {len(missing_orientations)} Orientações faltando.")
            self.add_log(f"Orientações pendentes: {missing_orientations}")
            consolidated_orientations_path = merge_docx_files(
                orientation_files, Path("impressos/ORIENTACOES CONSOLIDADAS.docx")
            )
            self.add_log(
                f"Arquivo com todas as orientações gerado em: {consolidated_orientations_path}"
            )

        except PermissionError as e:
            messagebox.showerror(
                "Arquivo em uso",
                (
                    f"Não foi possível processar o documento {e.filename}.\n\n"
                    "Provavelmente o arquivo DOCX está aberto no Word.\n\n"
                    "Feche o documento e tente novamente."
                ),
            )
        except Exception as e:
            self.add_log(f"❌ Erro: {e}")

        finally:
            self.generate_button.configure(state="normal")


def run():
    app = MainWindow()
    app.mainloop()
