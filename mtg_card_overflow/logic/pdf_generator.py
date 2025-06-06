from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
import os
import datetime

OUTPUT_DIR = "history"
CARD_WIDTH_MM = 63
CARD_HEIGHT_MM = 88
MARGIN_MM = 5

def mm_to_pt(mm):
    return mm * 72 / 25.4

CARD_WIDTH_PT = mm_to_pt(CARD_WIDTH_MM)
CARD_HEIGHT_PT = mm_to_pt(CARD_HEIGHT_MM)
MARGIN_PT = mm_to_pt(MARGIN_MM)
CARDS_PER_ROW = 3
CARDS_PER_COL = 3

PAGE_WIDTH, PAGE_HEIGHT = A4

def draw_cutting_lines(c, x, y, width, height, line_len=8, line_width=0.7):
    # Oben links
    c.setLineWidth(line_width)
    # Horizontal
    c.line(x - line_len, y + height, x, y + height)
    # Vertikal
    c.line(x, y + height, x, y + height + line_len)
    # Oben rechts
    c.line(x + width, y + height, x + width + line_len, y + height)
    c.line(x + width, y + height, x + width, y + height + line_len)
    # Unten links
    c.line(x - line_len, y, x, y)
    c.line(x, y, x, y - line_len)
    # Unten rechts
    c.line(x + width, y, x + width + line_len, y)
    c.line(x + width, y, x + width, y - line_len)

def generate_pdf(image_paths, output_dir=OUTPUT_DIR):
    os.makedirs(output_dir, exist_ok=True)
    pages = [image_paths[i:i+9] for i in range(0, len(image_paths), 9)]

    # Zielgröße in Pixeln für 300 DPI berechnen
    DPI = 300
    card_width_px = int(CARD_WIDTH_MM / 25.4 * DPI)
    card_height_px = int(CARD_HEIGHT_MM / 25.4 * DPI)

    for idx, page_images in enumerate(pages):
        # Erzeuge für jede Seite eine eigene PDF mit Zeitstempel und Seitennummer
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = os.path.join(output_dir, f"mtg_cards_{timestamp}_page{idx+1}.pdf")
        c = canvas.Canvas(pdf_path, pagesize=A4)

        for i, img_path in enumerate(page_images):
            img = Image.open(img_path)
            # Bild auf 300 DPI skalieren
            img = img.resize((card_width_px, card_height_px), Image.LANCZOS)

            row = i // CARDS_PER_ROW
            col = i % CARDS_PER_ROW

            x = MARGIN_PT + col * (CARD_WIDTH_PT + MARGIN_PT)
            y = PAGE_HEIGHT - ((row + 1) * (CARD_HEIGHT_PT + MARGIN_PT))

            # Bild einfügen
            temp_path = f"temp_{i}.png"
            img.save(temp_path, dpi=(DPI, DPI))
            c.drawImage(temp_path, x, y, width=CARD_WIDTH_PT, height=CARD_HEIGHT_PT)
            os.remove(temp_path)

            # Cutting lines zeichnen
            draw_cutting_lines(c, x, y, CARD_WIDTH_PT, CARD_HEIGHT_PT)

        c.showPage()
        c.save()