import os
import json

TRACKING_FILE = "processed_files.json"

def load_tracking():
    if not os.path.exists(TRACKING_FILE):
        return set()
    with open(TRACKING_FILE, "r") as f:
        try:
            return set(json.load(f))
        except json.JSONDecodeError:
            return set()

def save_tracking(processed):
    with open(TRACKING_FILE, "w") as f:
        json.dump(list(processed), f)

def is_processed(filename):
    processed = load_tracking()
    return filename in processed

def mark_as_processed(filenames):
    processed = load_tracking()
    processed.update(filenames)
    save_tracking(processed)
