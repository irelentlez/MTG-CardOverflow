import os
from mtg_card_printer.logic.config import load_config
from mtg_card_printer.ui.main_window import run_gui

if __name__ == "__main__":
    config = load_config()
    output_dir = config.get("output_dir") or "history"
    os.makedirs(output_dir, exist_ok=True)
    run_gui(config)