#!/usr/bin/env python3

import argparse
import datetime
from pathlib import Path
from typing import Optional
import os

from loguru import logger
from dotenv import load_dotenv

load_dotenv()

DEFAULT_PATH = os.getenv("DAYBOOK_DEFAULT_PATH")
SHOW_HOW_MANY_LAST_LINES = int(os.getenv("DAYBOOK_SHOW_HOW_MANY_LAST_LINES", 10))


def add_line(old_content: str, line: str, trim_end=True, allow_duplicates=False) -> str:
    lines = old_content.splitlines()
    if not allow_duplicates:
        for i, old_line in enumerate(lines, 1):
            if line in old_line:
                old_line_with_new_line_number = i
                raise ValueError(f"{line} is already there (line {old_line_with_new_line_number}).")

    formatted_line = format_line(line)
    lines.append(formatted_line)
    new_content = "\n".join(lines)
    if new_content.startswith(old_content):
        logger.info("\n".join(lines[-SHOW_HOW_MANY_LAST_LINES:]))
        return new_content
    else:
        raise ValueError(f"Failed to append the line {line}")


def format_line(line: str) -> str:
    return f"* {line}"


def generate_dateline(date: Optional[datetime.date] = None) -> str:
    date = date or datetime.date.today()
    return f"## {date :%Y-%m-%d, %A}"


def add_dateline(old_content, date: Optional[datetime.date] = None) -> str:
    dateline = generate_dateline(date)
    lines = [line.strip() for line in old_content.splitlines()]
    if dateline in lines:
        return old_content
    logger.info(f"Added '{dateline}'.")
    return "\n".join(lines + ["", dateline, "", ""])


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--path", type=Path, help="path to the daybook file", default=Path(DEFAULT_PATH))
    # arg_parser.add_argument("-v", "--verbose", type=Path, action="store_true")
    arg_parser.add_argument("line", help="the line to add")
    args = arg_parser.parse_args()

    line = args.line
    path: Path = args.path
    if path:
        logger.info(f"Adding to {path}")
        old_content = path.read_text()
        new_content = add_dateline(old_content)
        new_content = add_line(new_content, line)
        path.write_text(new_content)


if __name__ == "__main__":
    main()
