from src.extractor import extract_surgery_date, extract_surgeries
from src.extract_text_from_pdf import extract_text_from_pdf
from src.docx_merger import merge_docx_files
from tkinter import filedialog
import customtkinter as ctk
from pathlib import Path


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.pdf_path = None

        self._configure_window()
        self._create_widgets()

    def _configure_window(self):
        self.title("Gerador de Receitas de Alta")
        self.geometry("800x500")

    def _create_widgets(self):

        #
        # TÍTULO
        #

        self.title_label = ctk.CTkLabel(
            self,
            text="Gerador de Receitas de Alta",
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

        self.select_pdf_button = ctk.CTkButton(
            self.pdf_frame,
            text="Selecionar PDF",
            command=self.select_pdf,
        )

        self.select_pdf_button.pack(
            padx=10,
            pady=(0, 10),
        )

        #
        # BOTÃO GERAR
        #

        self.generate_button = ctk.CTkButton(
            self,
            text="GERAR RECEITAS",
            height=40,
            command=self.generate_receipts,
        )

        self.generate_button.pack(
            padx=20,
            pady=20,
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

        except Exception as e:
            self.add_log(f"❌ Erro: {e}")

        finally:
            self.generate_button.configure(state="normal")


def run():
    app = MainWindow()
    app.mainloop()
