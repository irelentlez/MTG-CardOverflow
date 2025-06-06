import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from mtg_card_overflow.logic import tracking, history
from mtg_card_overflow.logic.pdf_generator import generate_pdf
from mtg_card_overflow.logic.config import load_config, save_config


def run_gui(config):
    window = tk.Tk()
    window.title("MTG-CardOverflow")

    # Hintergrundbild laden und Fenstergröße anpassen
    bg_path = os.path.join(os.path.dirname(__file__), "background.jpg")
    if os.path.exists(bg_path):
        bg_img = Image.open(bg_path)
        width, height = bg_img.size
        window.geometry(f"{width}x{height}")
        window.resizable(False, False)
        bg_photo = ImageTk.PhotoImage(bg_img)
        bg_label = tk.Label(window, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_photo  # Referenz halten
    else:
        # Fallback falls kein Bild vorhanden ist
        width, height = 600, 800
        window.geometry("600x800")
        window.configure(bg="black")
        window.resizable(False, False)

    icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'mtg_card_printer_icon.ico'))
    if os.path.exists(icon_path):
        try:
            window.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon konnte nicht gesetzt werden: {e}")

    # Beispielhafte Platzierung der Buttons relativ zur Bildgröße
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

    # Buttons relativ zur Bildgröße platzieren
    btn_width = int(width * 0.33)
    btn_height = 40
    x_pos = int(width * 0.33)
    y_start = int(height * 0.07)
    y_gap = 60

    tk.Button(window, text="Input-Ordner ändern", command=change_input_dir).place(x=x_pos, y=y_start, width=btn_width, height=btn_height)
    tk.Button(window, text="Output-Ordner ändern", command=change_output_dir).place(x=x_pos, y=y_start + y_gap, width=btn_width, height=btn_height)
    tk.Button(window, text="PNG zu PDF", command=select_and_generate).place(x=x_pos, y=y_start + 2 * y_gap, width=btn_width, height=btn_height)

    window.mainloop()
