import pytest
from moffie.utils.md_helper import (
    is_comment,
    is_empty,
    get_header_level,
    is_divider,
    contains_image,
    contains_deco,
    extract_title
)


def test_is_comment():
    assert is_comment("<!-- This is a comment -->") == True
    assert is_comment("This is not a comment") == False


def test_is_empty():
    assert is_empty("<!-- This is a comment -->") == True
    assert is_empty("This is not a comment") == False
    assert is_empty(" \n") == True


def test_get_header_level():
    assert get_header_level("# Header 1") == 1
    assert get_header_level("### Header 3") == 3
    assert get_header_level("Normal text") == 0
    assert get_header_level("####### Not a valid header") == 0


def test_is_divider():
    assert is_divider("---") == True
    assert is_divider("***") == True
    assert is_divider("___") == True
    assert is_divider("  ----  ") == True
    assert is_divider("--") == False
    assert is_divider("- - -") == False
    assert is_divider("This is not a divider") == False


def test_contains_image():
    assert contains_image("![Alt text](image.jpg)") == True
    assert contains_image("This is an image: ![Alt text](image.jpg)") == True
    assert contains_image("This is not an image") == False
    assert contains_image("![](image.jpg)") == True  # empty alt text
    assert contains_image("![]()") == True  # empty alt text and URL


def test_contains_deco():
    assert contains_deco("@(layout=split, background=blue)") == True
    assert contains_deco("  @(layout=default)  ") == True
    assert contains_deco("This is not a deco") == False
    assert contains_deco("@(key=value) Some text") == False
    assert contains_deco("@()") == True  # empty deco

import pytest

def test_extract_title():
    assert extract_title("# Main Title\nSome content") == "Main Title"
    assert extract_title("## Secondary Title\nSome content") == "Secondary Title"
    assert extract_title("# Main Title\n## Secondary Title\nSome content") == "Main Title"
    assert extract_title("## Secondary Title\n# Main Title\nSome content") == "Secondary Title"
    assert extract_title("Some content without headings") == None
    assert extract_title("") == None
    assert extract_title("#  Title with spaces  \nContent") == "Title with spaces"
    multi_para = "Para 1\n\nPara 2\n\n# Actual Title\nContent"
    assert extract_title(multi_para) == "Actual Title"