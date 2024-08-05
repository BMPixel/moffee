import os
import pytest

from moffie.utils.md_helper import redirect_url

@pytest.fixture(scope='module', autouse=True)
def setup_test_env():
    # Create test directories and files
    os.makedirs('/tmp/redirect_url_pytest/test_env/images', exist_ok=True)
    os.makedirs('/tmp/redirect_url_pytest/test_env/docs', exist_ok=True)
    os.makedirs('/tmp/redirect_url_pytest/resources', exist_ok=True)
    os.makedirs('/tmp/redirect_url_pytest/another_dir', exist_ok=True)

    # Create test files to simulate the environment
    with open('/tmp/redirect_url_pytest/test_env/images/photo.png', 'w') as f:
        f.write('This is a test image file.')

    with open('/tmp/redirect_url_pytest/test_env/docs/readme.md', 'w') as f:
        f.write('This is a test markdown file.')

    with open('/tmp/redirect_url_pytest/resources/external.txt', 'w') as f:
        f.write('This is a resource file in the absolute resource directory.')

    with open('/tmp/redirect_url_pytest/another_dir/test.md', 'w') as f:
        f.write('Another test markdown file.')

def test_absolute_urls():
    document = """
    Here is a link to an absolute URL [Google](https://www.google.com).
    Here is a link to an absolute file path ![File](/tmp/redirect_url_pytest/test_env/images/photo.png).
    """

    document_path = "/tmp/redirect_url_pytest/test_env/markdown.md"
    resource_dir = "/tmp/redirect_url_pytest/resources"

    expected_document = """
    Here is a link to an absolute URL [Google](https://www.google.com).
    Here is a link to an absolute file path ![File](/tmp/redirect_url_pytest/test_env/images/photo.png).
    """

    result = redirect_url(document, document_path, resource_dir)
    assert result == expected_document

def test_nonexistent_paths():
    document = """
    This link should remain unchanged [Nonexistent](nonexistent/path/file.txt).
    """

    document_path = "/tmp/redirect_url_pytest/test_env/markdown.md"
    resource_dir = "/tmp/redirect_url_pytest/resources"

    expected_document = """
    This link should remain unchanged [Nonexistent](nonexistent/path/file.txt).
    """

    result = redirect_url(document, document_path, resource_dir)
    assert result == expected_document

def test_multiple_links():
    document = """
    ![Image](images/photo.png)
    [Readme](docs/readme.md)
    [External](external.txt)
    [Another](../another_dir/test.md)
    """

    document_path = "/tmp/redirect_url_pytest/test_env/markdown.md"
    resource_dir = "/tmp/redirect_url_pytest/resources"

    expected_document = """
    ![Image](/tmp/redirect_url_pytest/test_env/images/photo.png)
    [Readme](/tmp/redirect_url_pytest/test_env/docs/readme.md)
    [External](/tmp/redirect_url_pytest/resources/external.txt)
    [Another](/tmp/redirect_url_pytest/another_dir/test.md)
    """

    result = redirect_url(document, document_path, resource_dir)
    assert result == expected_document

def test_complex_relative_paths():
    document = """
    ![Parent Image](../test_env/images/photo.png)
    [Parent Readme](../test_env/docs/readme.md)
    """

    document_path = "/tmp/redirect_url_pytest/test_env/docs/nested/markdown.md"
    resource_dir = "/tmp/redirect_url_pytest/resources"

    expected_document = """
    ![Parent Image](/tmp/redirect_url_pytest/test_env/images/photo.png)
    [Parent Readme](/tmp/redirect_url_pytest/test_env/docs/readme.md)
    """

    result = redirect_url(document, document_path, resource_dir)
    assert result == expected_document

def test_links_with_anchors_and_queries():
    document = """
    [Section](docs/readme.md#section)
    [Query](docs/readme.md?query=1)
    """

    document_path = "/tmp/redirect_url_pytest/test_env/markdown.md"
    resource_dir = "/tmp/redirect_url_pytest/resources"

    expected_document = """
    [Section](/tmp/redirect_url_pytest/test_env/docs/readme.md#section)
    [Query](/tmp/redirect_url_pytest/test_env/docs/readme.md?query=1)
    """

    result = redirect_url(document, document_path, resource_dir)
    assert result == expected_document

def test_no_resource_dir():
    document = """
    ![Image](images/photo.png)
    [Readme](docs/readme.md)
    [Nonexistent](nonexistent/path/file.txt)
    """

    document_path = "/tmp/redirect_url_pytest/test_env/markdown.md"
    # No resource_dir provided

    expected_document = """
    ![Image](/tmp/redirect_url_pytest/test_env/images/photo.png)
    [Readme](/tmp/redirect_url_pytest/test_env/docs/readme.md)
    [Nonexistent](nonexistent/path/file.txt)
    """

    result = redirect_url(document, document_path)
    assert result == expected_document
    

if __name__ == "__main__":
    pytest.main([__file__])
