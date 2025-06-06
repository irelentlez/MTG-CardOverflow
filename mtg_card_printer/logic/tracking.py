import json
import os

TRACKING_PATH = "processed_files.json"

def load_processed():
    if not os.path.exists(TRACKING_PATH):
        return []
    with open(TRACKING_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_processed(processed_list):
    with open(TRACKING_PATH, "w", encoding="utf-8") as f:
        json.dump(processed_list, f, indent=2)

def mark_as_processed(filename):
    processed = load_processed()
    if filename not in processed:
        processed.append(filename)
        save_processed(processed)

def is_processed(filename):
    processed = load_processed()
    return filename in processed
