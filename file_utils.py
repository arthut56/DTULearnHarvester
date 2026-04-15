import os
from pathlib import Path
import re

def create_directory(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '-', name)

def get_file_extension_from_headers(response_headers):
    return response_headers.get("Content-Type").split("/")[1]
