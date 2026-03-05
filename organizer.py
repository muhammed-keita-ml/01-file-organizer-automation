import os
import shutil
import json
from datetime import datetime

# ─────────────────────────────────────────
# Automated File Organizer
# Sorts files in a folder by extension
# ─────────────────────────────────────────


def load_config(config_path="config.json"):
    """Load extension rules from config.json"""
    with open(config_path, "r") as f:
        return json.load(f)


def get_category(extension, config):
    """Return the folder category for a given file extension"""
    for category, extensions in config["extensions"].items():
        if extension.lower() in extensions:
            return category
    return "other"


def organize_files(source_folder, config):
    """Main function: scan folder and sort files into subfolders"""
    if not os.path.exists(source_folder):
        print(f"[ERROR] Folder not found: {source_folder}")
        return

    files_moved = 0
    log = []

    for filename in os.listdir(source_folder):
        filepath = os.path.join(source_folder, filename)

        # Skip folders, only process files
        if os.path.isdir(filepath):
            continue

        # Get file extension
        _, ext = os.path.splitext(filename)
        if not ext:
            ext = ".unknown"

        # Determine destination category folder
        category = get_category(ext, config)
        dest_folder = os.path.join(source_folder, category)

        # Create destination folder if it doesn't exist
        os.makedirs(dest_folder, exist_ok=True)

        # Move the file
        dest_path = os.path.join(dest_folder, filename)
        shutil.move(filepath, dest_path)

        log_entry = f"{filename} -> {category}/"
        log.append(log_entry)
        print(f"[MOVED] {log_entry}")
        files_moved += 1

    # Save log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"organizer_log_{timestamp}.txt"
    with open(log_file, "w") as f:
        f.write("\n".join(log))

    print(f"\n[DONE] {files_moved} files organized.")
    print(f"[LOG]  Saved to {log_file}")


if __name__ == "__main__":
    config = load_config("config.json")
    folder = config.get("source_folder", "sample_files")
    print(f"[START] Organizing files in: {folder}")
    organize_files(folder, config)
