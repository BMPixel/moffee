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


def redirect_url(document: str, document_path: str, resource_dir: str = ".") -> str:
    """
    Redirect all relative paths in markdown document to absolute paths with some guessing.
    Following possible base paths will be tried:
    - The original path itself maybe a valid absolute url (Absolute path or http)
    - The direct parent dir of the document
    - The resource dir (if it exists as an absolute path)
    - The resource dir relative to the document (Otherwise)

    :param document: Markdown document string
    :param document_path: Path to the document
    :param resource_dir: Optional resource path
    :return: Document string with all urls redirected.
    """

    def is_absolute_url(url):
        return bool(urlparse(url).netloc) or (os.path.isabs(url) and os.path.exists(url))

    def make_absolute(base, relative):
        return os.path.abspath(os.path.normpath(os.path.join(base, relative)))

    def replace_url(match):
        url = match.group(2)
        if is_absolute_url(url):
            return match.group(0) 
        # escape anchors(#) and queries(?)
        url = re.match(r'^[^#?]*', url).group(0)

        # Try different base paths to make the URL absolute
        base_paths = [
            os.path.dirname(document_path), 
            os.path.abspath(resource_dir), 
            os.path.join(
                os.path.dirname(document_path), resource_dir
            ),  
        ]

        for base in base_paths:
            absolute_url = make_absolute(base, url)
            if os.path.exists(absolute_url) or is_absolute_url(absolute_url):
                return match.group(0).replace(url, absolute_url)

        return match.group(0) 

    # Regular expression to find markdown links
    url_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    # Substitute all URLs in the document using the replace_url function
    redirected_document = url_pattern.sub(replace_url, document)

    return redirected_document
