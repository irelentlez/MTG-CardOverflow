import os
import logging
import sys
from mtg_card_overflow.logic.config import load_config
#from mtg_card_overflow.ui.main_window import run_gui
from mtg_card_overflow.ui.main_window_qt import run_gui

# Logging-Konfiguration
logging.basicConfig(
    filename="error.log",
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s: %(message)s"
)

def log_uncaught_exceptions(exctype, value, tb):
    logging.error("Unbehandelte Ausnahme", exc_info=(exctype, value, tb))

# Globalen Exception-Handler setzen
sys.excepthook = log_uncaught_exceptions

if __name__ == "__main__":
    config = load_config()
    output_dir = config.get("output_dir") or "history"
    os.makedirs(output_dir, exist_ok=True)
    run_gui(config)