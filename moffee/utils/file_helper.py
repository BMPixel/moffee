import os
import re
import shutil
from urllib.parse import urlparse
from pathlib import Path
import uuid

from bs4 import BeautifulSoup


def merge_directories(base_dir: str, output_dir: str, merge_dir: str = None):
    """Merge base_dir and merge_dir into output_dir, merge_dir overwrites base_dir if confliction happens"""
    # Clear the output_dir before writing the merged files
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    shutil.copytree(base_dir, output_dir, dirs_exist_ok=True)
    if merge_dir:
        shutil.copytree(
            merge_dir, output_dir, dirs_exist_ok=True, copy_function=shutil.copy2
        )


def redirect_paths(document: str, document_path: str, resource_dir: str = ".") -> str:
    """
    Redirect all relative paths in a document to absolute paths with some guessing.
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
        return bool(urlparse(url).netloc) or (
            os.path.isabs(url) and os.path.exists(url)
        )

    def make_absolute(base, relative):
        return os.path.abspath(os.path.normpath(os.path.join(base, relative)))

    def replace_url(match):
        url = match.group(1)
        if is_absolute_url(url):
            return match.group(0)

        # Try different base paths to make the URL absolute
        base_paths = [
            os.path.dirname(document_path),
            os.path.abspath(resource_dir),
            os.path.join(os.path.dirname(document_path), resource_dir),
        ]

        for base in base_paths:
            absolute_url = make_absolute(base, url)
            if os.path.exists(absolute_url) or is_absolute_url(absolute_url):
                return match.group(0).replace(url, absolute_url)

        return match.group(0)

    # Regular expression to find markdown links
    # import ipdb; ipdb.set_trace(context=15)
    url_pattern = re.compile(r'"(.+?)"')

    # Substitute all URLs in the document using the replace_url function
    redirected_document = url_pattern.sub(replace_url, document)

    return redirected_document


def copy_assets(document: str, target_dir: str) -> str:
    """
    Copy all asset resources in an HTML document to target_dir, then update URLs to target_dir/uuid_originalname.ext

    :param document: HTML document to process
    :param target_dir: Target directory
    :return: Updated document with URLs redirected
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    soup = BeautifulSoup(document, "html.parser")

    # Dictionary to store original path to new path mapping
    path_mapping = {}

    # Tags and attributes to check for URLs
    tag_attr_pairs = [
        ("img", "src"),
        ("link", "href"),
        ("script", "src"),
        ("a", "href"),
    ]

    for tag, attr in tag_attr_pairs:
        for element in soup.find_all(tag):
            if element.has_attr(attr):
                original_path = element[attr]

                # Skip if it's an external URL or a non-file path
                if urlparse(original_path).scheme or not os.path.isfile(original_path):
                    continue

                if original_path not in path_mapping:
                    # Generate a new filename
                    original_filename = os.path.basename(original_path)
                    name, ext = os.path.splitext(original_filename)
                    new_filename = f"{str(uuid.uuid4())[:8]}_{name}{ext}"
                    new_path = os.path.join(target_dir, new_filename)

                    # Copy the file
                    shutil.copy2(original_path, new_path)

                    # Store the mapping
                    path_mapping[original_path] = new_path

                # Update the attribute with the new path
                element[attr] = path_mapping[original_path]

    return str(soup)
