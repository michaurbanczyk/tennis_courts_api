import json
import os


def open_json_file(base_dir: str, path: str):
    full_path = os.path.join(base_dir, path)
    with open(full_path, encoding="utf-8") as json_file:
        data = json.load(json_file)

    return data
