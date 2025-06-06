import os
import tkinter as tk
from tkinter import filedialog, messagebox
from mtg_card_printer.logic import tracking, history
from mtg_card_printer.logic.pdf_generator import generate_pdf
from mtg_card_printer.logic.config import load_config, save_config


def run_gui(config):
    window = tk.Tk()
    window.title("MTG Card Printer")

    def change_input_dir():
        new_dir = filedialog.askdirectory(title="Input-Ordner wählen")
        if new_dir:
            config["input_dir"] = new_dir
            save_config(config)
            messagebox.showinfo("Info", f"Input-Ordner geändert zu:\n{new_dir}")

    def change_output_dir():
        new_dir = filedialog.askdirectory(title="Output-Ordner wählen")
        if new_dir:
            config["output_dir"] = new_dir
            save_config(config)
            messagebox.showinfo("Info", f"Output-Ordner geändert zu:\n{new_dir}")

    def select_and_generate():
        input_path = config.get("input_dir", "")
        if not input_path or not os.path.isdir(input_path):
            messagebox.showerror("Fehler", "Input-Ordner ist ungültig oder nicht gesetzt.")
            return

        input_files = [
            os.path.join(input_path, f)
            for f in os.listdir(input_path)
            if f.lower().endswith(".png") or f.lower().endswith(".jpg") or f.lower().endswith(".jpeg")
        ]

        to_process = [f for f in input_files if not tracking.is_processed(f)]

        if not to_process:
            messagebox.showinfo("Keine neuen Karten", "Alle Karten wurden bereits verarbeitet.")
            return

        generate_pdf(to_process, output_dir=config.get("output_dir", "history"))
        for file in to_process:
            tracking.mark_as_processed(file)
        messagebox.showinfo("Fertig", f"{len(to_process)} Karten verarbeitet.")

    tk.Button(window, text="Input-Ordner ändern", command=change_input_dir).pack(pady=10)
    tk.Button(window, text="Output-Ordner ändern", command=change_output_dir).pack(pady=10)
    btn_generate = tk.Button(window, text="PNG zu PDF", command=select_and_generate)
    btn_generate.pack(pady=20)

    window.mainloop()
