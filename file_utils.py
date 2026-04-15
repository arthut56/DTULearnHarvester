import os
from pathlib import Path
import re


def create_directory(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '-', name)


def download_file(name, api_response, directory="", suffix=""):
    filename = os.path.join(directory, name)
    with open(f"{filename}.{suffix}", "wb") as f:
        f.write(api_response.content)


def get_file_type_from_headers(response_headers):
    return response_headers.get("Content-Type").split("/")[1]
