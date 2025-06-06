import os

def get_last_pdfs(output_dir, n=10):
    pdfs = [f for f in os.listdir(output_dir) if f.lower().endswith(".pdf")]
    pdfs = sorted(pdfs, key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)
    return [os.path.join(output_dir, f) for f in pdfs[:n]]