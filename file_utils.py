import os
from pathlib import Path
import re

def create_directory(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '-', name)

def get_file_extension_from_headers(response_headers):
    return response_headers.get("Content-Type").split("/")[1]

def write_file(name, api_response, directory="", file_extension="pdf"):
    filename = os.path.join(directory, name)
    with open(f"{filename}.{file_extension}", "wb") as f:
        f.write(api_response.content)

def default_format(title):
    return title

def lowercase(title):
    return title.lower()

def snake_case(title):
    return title.lower().replace(" ", "_").replace("-", "_")

def kebab_case(title):
    return title.lower().replace(" ", "-").replace("_", "-")

FORMAT_MAPPING = {
    "default" : default_format,
    "lower" : lowercase,
    "snake" : snake_case,
    "kebab" : kebab_case
}
