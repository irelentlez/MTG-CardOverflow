import os
import sys
import subprocess

def print_pdf(pdf_path):
    """
    Druckt eine PDF-Datei auf dem Standarddrucker des Systems.
    Funktioniert unter Windows, macOS und Linux.
    """
    try:
        if os.name == 'nt':
            os.startfile(pdf_path, "print")
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['lp', pdf_path])
        elif os.name == 'posix':
            subprocess.Popen(['lp', pdf_path])
    except Exception as e:
        raise RuntimeError(f"PDF konnte nicht gedruckt werden: {e}")