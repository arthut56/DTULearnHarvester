import typer

from script import download_course
from typing import Annotated


def main(course_no, format_style: Annotated[str, typer.Argument()] = ""):
    download_course(course_no, format_style)


if __name__ == "__main__":
    typer.run(main)