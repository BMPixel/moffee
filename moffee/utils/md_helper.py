import os
from urllib.parse import urljoin, urlparse
import re
from typing import Optional


def is_comment(line: str) -> bool:
    """
    Determines if a given line is a Markdown comment.
    Markdown comments are in the format <!-- comment -->

    :param line: The line to check
    :return: True if the line is a comment, False otherwise
    """
    return bool(re.match(r"^\s*<!--.*-->\s*$", line))


def get_header_level(line: str) -> int:
    """
    Determines the header level of a given line.

    :param line: The line to check
    :return: The header level (1-6) if it's a header, 0 otherwise
    """
    match = re.match(r"^(#{1,6})\s", line)
    if match:
        return len(match.group(1))
    else:
        return 0


def is_empty(line: str) -> bool:
    """
    Determines if a given line is an empty line in markdown.
    A line is empty if it is blank or comment only

    :param line: The line to check
    :return: True if the line is empty, False otherwise
    """
    return is_comment(line) or line.strip() == ""


def is_divider(line: str, type=None) -> bool:
    """
    Determines if a given line is a Markdown divider (horizontal rule).
    Markdown dividers are three or more hyphens, asterisks, or underscores,
    without any other characters except spaces.

    :param line: The line to check
    :param type: Which type to match, str. e.g. "*" to match "***" only. Defaults to "", match any of "*", "-" and "_".
    :return: True if the line is a divider, False otherwise
    """
    stripped_line = line.strip()
    if len(stripped_line) < 3:
        return False
    if type == None:
        type = "-*_"
        
    assert type in "-*_", "type must be either '*', '-' or '_'"
    return all(char in type for char in stripped_line) and any(
        char * 3 in stripped_line for char in type
    )


def contains_image(line: str) -> bool:
    """
    Determines if a given line contains a Markdown image.
    Markdown images are in the format ![alt text](image_url)

    :param line: The line to check
    :return: True if the line contains an image, False otherwise
    """
    return bool(re.search(r"!\[.*?\]\(.*?\)", line))


def contains_deco(line: str) -> bool:
    """
    Determines if a given line contains a deco (custom decorator).
    Decos are in the format @(key1=value1, key2=value2, ...)

    :param line: The line to check
    :return: True if the line contains a deco, False otherwise
    """
    return bool(re.match(r"^\s*@\(.*?\)\s*$", line))

def extract_title(document: str) -> Optional[str]:
    """
    Extracts proper title from document.
    The title should be the first-occurred level 1 or 2 heading.

    :param document: The document in markdown
    :return: title if there is one, otherwise None
    """
    heading_pattern = r"^(#|##)\s+(.*?)(?:\n|$)"
    match = re.search(heading_pattern, document, re.MULTILINE)

    if match:
        return match.group(2).strip()
    else:
        return None

def rm_comments(document):
    """
    Remove comments from markdown. Supports html and "%%"
    """
    document = re.sub(r'<!--[\s\S]*?-->', '', document)
    document = re.sub(r'^\s*%%.*$', '', document, flags=re.MULTILINE)

    return document.strip()

