from enum import Enum

import typer

from script import download_course, FORMAT_MAPPING
from typing import Annotated

FormatStyle = Enum("FormatStyle", {k: k for k in FORMAT_MAPPING})

def main(course_no, format_style: Annotated[FormatStyle, typer.Argument()] = ''):
    download_course(course_no, format_style.value)


if __name__ == "__main__":
    typer.run(main)
