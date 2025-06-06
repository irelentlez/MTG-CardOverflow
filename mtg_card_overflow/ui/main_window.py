import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import subprocess
import sys
from mtg_card_overflow.logic import tracking, history
from mtg_card_overflow.logic.pdf_generator import generate_pdf
from mtg_card_overflow.logic.config import load_config, save_config
from mtg_card_overflow.logic.history import get_last_pdfs


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
    else:
        width, height = 600, 800
        window.geometry("600x800")
        window.configure(bg="black")
        window.resizable(False, False)
        bg_photo = None

    icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'mtg_card_printer_icon.ico'))
    if os.path.exists(icon_path):
        try:
            window.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon konnte nicht gesetzt werden: {e}")

    # Tabs anlegen
    notebook = ttk.Notebook(window)
    main_frame = tk.Frame(notebook, width=width, height=height)
    history_frame = tk.Frame(notebook, width=width, height=height)
    notebook.add(main_frame, text="Start")
    notebook.add(history_frame, text="History")
    notebook.place(x=0, y=0, relwidth=1, relheight=1)

    # Hintergrundbild auf beide Tabs anwenden
    if bg_photo:
        for frame in (main_frame, history_frame):
            bg_label = tk.Label(frame, image=bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.image = bg_photo  # Referenz halten

    # --- Haupttab: Buttons relativ zur Bildgröße platzieren ---
    btn_width = int(width * 0.33)
    btn_height = 40
    x_pos = int(width * 0.33)
    y_start = int(height * 0.07)
    y_gap = 60

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

    tk.Button(main_frame, text="Input-Ordner ändern", command=change_input_dir).place(x=x_pos, y=y_start, width=btn_width, height=btn_height)
    tk.Button(main_frame, text="Output-Ordner ändern", command=change_output_dir).place(x=x_pos, y=y_start + y_gap, width=btn_width, height=btn_height)
    tk.Button(main_frame, text="PNG zu PDF", command=select_and_generate).place(x=x_pos, y=y_start + 2 * y_gap, width=btn_width, height=btn_height)

    # --- History-Tab: Zeige die letzten 10 PDFs als anklickbare Buttons ---
    def open_pdf(pdf_path):
        try:
            if sys.platform.startswith('darwin'):
                subprocess.Popen(['open', pdf_path])
            elif os.name == 'nt':
                os.startfile(pdf_path)
            elif os.name == 'posix':
                subprocess.Popen(['xdg-open', pdf_path])
        except Exception as e:
            messagebox.showerror("Fehler", f"PDF konnte nicht geöffnet werden:\n{e}")

    def show_history():
        output_dir = config.get("output_dir", "history")
        if not output_dir:
            output_dir = "history"
        os.makedirs(output_dir, exist_ok=True)
        for widget in history_frame.winfo_children():
            widget.destroy()
        # Hintergrundbild erneut setzen (sonst verschwindet es beim Tab-Wechsel)
        if bg_photo:
            bg_label = tk.Label(history_frame, image=bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.image = bg_photo
        last_pdfs = get_last_pdfs(output_dir)
        if not last_pdfs:
            tk.Label(history_frame, text="Keine PDFs gefunden.", bg="#000000", fg="white").pack(pady=20)
            return
        tk.Label(history_frame, text="Deine letzten 10 erstellte PDFs:", bg="#000000", fg="white", font=("Arial", 14, "bold")).pack(pady=10)
        for idx, pdf_path in enumerate(last_pdfs):
            fname = os.path.basename(pdf_path)
            btn = tk.Button(
                history_frame,
                text=f"{idx+1}. {fname}",
                bg="#222222",
                fg="white",
                font=("Arial", 12),
                relief=tk.RAISED,
                command=lambda p=pdf_path: open_pdf(p)
            )
            btn.pack(anchor="w", padx=30, pady=4)

    notebook.bind("<<NotebookTabChanged>>", lambda e: show_history() if notebook.index("current") == 1 else None)

    window.mainloop()
