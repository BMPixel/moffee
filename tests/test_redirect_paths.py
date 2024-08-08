import pytest
import tempfile
import os
from moffee.utils.file_helper import redirect_paths

@pytest.fixture(scope='module', autouse=True)
def setup_test_env():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Setup test files and directories
        doc_path = os.path.join(temp_dir, "test.md")
        res_dir = os.path.join(temp_dir, "resources")
        os.mkdir(res_dir)

        # Create various test files
        with open(doc_path, "w") as f:
            f.write('This is a test document with links: "image.png", "http://example.com", "/absolute/path/image2.png"')

        with open(os.path.join(temp_dir, "image.png"), "w") as f:
            f.write('fake image content')

        with open(os.path.join(res_dir, "image2.png"), "w") as f:
            f.write('fake image content')

        yield temp_dir, doc_path, res_dir

def test_redirect_paths(setup_test_env):
    temp_dir, doc_path, res_dir = setup_test_env

    document = """
Image Path: "image.png"
Image in resource: "image2.png"
URL: "http://example.com"
"""

    redirected_document = redirect_paths(document, doc_path, res_dir)

    expected_path_image1 = os.path.abspath(os.path.join(temp_dir, "image.png"))
    expected_path_image2 = os.path.abspath(os.path.join(res_dir, "image2.png"))

    assert f'"{expected_path_image1}"' in redirected_document
    assert '"http://example.com"' in redirected_document
    assert f'"{expected_path_image2}"' in redirected_document


def test_redirect_paths_no_res_dir(setup_test_env):
    temp_dir, doc_path, res_dir = setup_test_env

    document = """
Image Path: "image.png"
Image in resource: "image2.png"
URL: "http://example.com"
"""

    redirected_document = redirect_paths(document, doc_path)

    expected_path_image1 = os.path.abspath(os.path.join(temp_dir, "image.png"))
    expected_path_image2 = os.path.abspath(os.path.join(res_dir, "image2.png"))

    assert f'"{expected_path_image1}"' in redirected_document
    assert '"http://example.com"' in redirected_document
    assert not f'"{expected_path_image2}"' in redirected_document
    assert f'"image2.png"' in redirected_document

def test_redirect_paths_trivial(setup_test_env):
    temp_dir, doc_path, res_dir = setup_test_env

    document = """
empty: ""
invalid: "invalid.txt"
"""
    redirected_document = redirect_paths(document, doc_path)
    assert redirected_document == document
