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

    # Hintergrundbild laden und Fenstergröße setzen
    bg_path = os.path.join(os.path.dirname(__file__), "background.jpg")
    if os.path.exists(bg_path):
        bg_img = Image.open(bg_path)
        width, height = bg_img.size
    else:
        width, height = 800, 1200  # Fallback-Größe

    window.geometry(f"{width}x{height}")
    window.resizable(False, False)

    # Modernes Button-Design mit ttk.Style
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(
        "Modern.TButton",
        font=("Segoe UI", 20, "bold"),  # Hauptbutton: größere Schrift
        foreground="#ffffff",
        background="#444444",
        borderwidth=0,
        focusthickness=3,
        focuscolor="#888888",
        padding=16
    )
    style.configure(
        "Small.TButton",
        font=("Segoe UI", 13),  # Kleine Buttons: mittlere Schrift
        foreground="#ffffff",
        background="#444444",
        borderwidth=0,
        focusthickness=2,
        focuscolor="#888888",
        padding=8
    )
    style.map(
        "Modern.TButton",
        background=[("active", "#666666"), ("pressed", "#222222")]
    )
    style.map(
        "Small.TButton",
        background=[("active", "#666666"), ("pressed", "#222222")]
    )

    # Tabs anlegen
    notebook = ttk.Notebook(window)
    main_frame = tk.Frame(notebook, width=width, height=height)
    history_frame = tk.Frame(notebook, width=width, height=height)
    notebook.add(main_frame, text="Start")
    notebook.add(history_frame, text="History")
    notebook.pack(fill="both", expand=True)

    # Hintergrundbild auf beide Tabs anwenden
    if os.path.exists(bg_path):
        bg_img = bg_img.resize((width, height), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_img)
        for frame in (main_frame, history_frame):
            bg_label = tk.Label(frame, image=bg_photo, borderwidth=0, highlightthickness=0)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
            bg_label.image = bg_photo
    else:
        window.configure(bg="black")

    icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'mtg_card_printer_icon.ico'))
    if os.path.exists(icon_path):
        try:
            window.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon konnte nicht gesetzt werden: {e}")

    # --- Haupttab: Buttons platzieren ---
    # Hauptbutton (PNG zu PDF) groß und zentriert
    main_btn_width = int(width * 0.5)
    main_btn_height = 70
    main_btn_x = int((width - main_btn_width) / 2)
    main_btn_y = int(height * 0.22)

    # Kleine Buttons nebeneinander darunter
    small_btn_width = int(width * 0.22)
    small_btn_height = 38
    spacing = int(width * 0.04)
    small_btn_y = main_btn_y + main_btn_height + 40
    left_btn_x = int((width - (2 * small_btn_width + spacing)) / 2)
    right_btn_x = left_btn_x + small_btn_width + spacing

    def change_input_dir():
        new_dir = filedialog.askdirectory(title="Input-Ordner")
        if new_dir:
            config["input_dir"] = new_dir
            save_config(config)
            messagebox.showinfo("Info", f"Input-Ordner geändert zu:\n{new_dir}")

    def change_output_dir():
        new_dir = filedialog.askdirectory(title="Output-Ordner")
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

    # Hauptbutton
    ttk.Button(
        main_frame,
        text="PNG zu PDF",
        style="Modern.TButton",
        command=select_and_generate
    ).place(x=main_btn_x, y=main_btn_y, width=main_btn_width, height=main_btn_height)

    # Kleine Buttons nebeneinander
    ttk.Button(
        main_frame,
        text="Input-Ordner",
        style="Small.TButton",
        command=change_input_dir
    ).place(x=left_btn_x, y=small_btn_y, width=small_btn_width, height=small_btn_height)

    ttk.Button(
        main_frame,
        text="Output-Ordner",
        style="Small.TButton",
        command=change_output_dir
    ).place(x=right_btn_x, y=small_btn_y, width=small_btn_width, height=small_btn_height)

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
        if os.path.exists(bg_path):
            bg_img = Image.open(bg_path).resize((width, height), Image.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_img)
            bg_label = tk.Label(history_frame, image=bg_photo, borderwidth=0, highlightthickness=0)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
            bg_label.image = bg_photo
        last_pdfs = get_last_pdfs(output_dir)
        if not last_pdfs:
            tk.Label(history_frame, text="Keine PDFs gefunden.", bg="#000000", fg="white").pack(pady=20)
            return
        tk.Label(history_frame, text="Deine letzten 10 erstellte PDFs:", bg="#000000", fg="white", font=("Arial", 14, "bold")).pack(pady=10)
        for idx, pdf_path in enumerate(last_pdfs):
            fname = os.path.basename(pdf_path)
            ttk.Button(
                history_frame,
                text=f"{idx+1}. {fname}",
                style="Modern.TButton",
                command=lambda p=pdf_path: open_pdf(p)
            ).pack(anchor="w", padx=30, pady=4)

    notebook.bind("<<NotebookTabChanged>>", lambda e: show_history() if notebook.index("current") == 1 else None)

    window.mainloop()