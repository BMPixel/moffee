import os
import pytest
import tempfile

from moffee.utils.md_helper import redirect_url

@pytest.fixture(scope='module', autouse=True)
def setup_test_env():
    # Use tempfile to create a temporary directory for the test environment
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test directories and files
        test_env_path = os.path.join(temp_dir, 'test_env')
        resources_path = os.path.join(temp_dir, 'resources')
        another_dir_path = os.path.join(temp_dir, 'another_dir')

        os.makedirs(os.path.join(test_env_path, 'images'), exist_ok=True)
        os.makedirs(os.path.join(test_env_path, 'docs'), exist_ok=True)
        os.makedirs(resources_path, exist_ok=True)
        os.makedirs(another_dir_path, exist_ok=True)

        # Create test files to simulate the environment
        with open(os.path.join(test_env_path, 'images', 'photo.png'), 'w') as f:
            f.write('This is a test image file.')

        with open(os.path.join(test_env_path, 'docs', 'readme.md'), 'w') as f:
            f.write('This is a test markdown file.')

        with open(os.path.join(resources_path, 'external.txt'), 'w') as f:
            f.write('This is a resource file in the absolute resource directory.')

        with open(os.path.join(another_dir_path, 'test.md'), 'w') as f:
            f.write('Another test markdown file.')

        # Provide the test environment paths to the tests
        yield {
            'test_env_path': test_env_path,
            'resources_path': resources_path,
            'another_dir_path': another_dir_path
        }

def test_absolute_urls(setup_test_env):
    document = """
    Here is a link to an absolute URL [Google](https://www.google.com).
    Here is a link to an absolute file path ![File](/tmp/redirect_url_pytest/test_env/images/photo.png).
    """

    document_path = os.path.join(setup_test_env['test_env_path'], 'markdown.md')
    resource_dir = setup_test_env['resources_path']

    expected_document = """
    Here is a link to an absolute URL [Google](https://www.google.com).
    Here is a link to an absolute file path ![File](/tmp/redirect_url_pytest/test_env/images/photo.png).
    """

    result = redirect_url(document, document_path, resource_dir)
    assert result == expected_document

def test_nonexistent_paths(setup_test_env):
    document = """
    This link should remain unchanged [Nonexistent](nonexistent/path/file.txt).
    """

    document_path = os.path.join(setup_test_env['test_env_path'], 'markdown.md')
    resource_dir = setup_test_env['resources_path']

    expected_document = """
    This link should remain unchanged [Nonexistent](nonexistent/path/file.txt).
    """

    result = redirect_url(document, document_path, resource_dir)
    assert result == expected_document

def test_multiple_links(setup_test_env):
    document = """
    ![Image](images/photo.png)
    [Readme](docs/readme.md)
    [External](external.txt)
    [Another](../another_dir/test.md)
    """

    document_path = os.path.join(setup_test_env['test_env_path'], 'markdown.md')
    resource_dir = setup_test_env['resources_path']

    expected_document = f"""
    ![Image]({os.path.join(setup_test_env['test_env_path'], 'images/photo.png')})
    [Readme]({os.path.join(setup_test_env['test_env_path'], 'docs/readme.md')})
    [External]({os.path.join(setup_test_env['resources_path'], 'external.txt')})
    [Another]({os.path.join(setup_test_env['another_dir_path'], 'test.md')})
    """

    result = redirect_url(document, document_path, resource_dir)
    assert result == expected_document

def test_complex_relative_paths(setup_test_env):
    document = """
    ![Parent Image](../test_env/images/photo.png)
    [Parent Readme](../test_env/docs/readme.md)
    """

    document_path = os.path.join(setup_test_env['test_env_path'], 'docs/nested/markdown.md')
    resource_dir = setup_test_env['resources_path']

    expected_document = f"""
    ![Parent Image]({os.path.join(setup_test_env['test_env_path'], 'images/photo.png')})
    [Parent Readme]({os.path.join(setup_test_env['test_env_path'], 'docs/readme.md')})
    """

    result = redirect_url(document, document_path, resource_dir)
    assert result == expected_document

def test_links_with_anchors_and_queries(setup_test_env):
    document = """
    [Section](docs/readme.md#section)
    [Query](docs/readme.md?query=1)
    """

    document_path = os.path.join(setup_test_env['test_env_path'], 'markdown.md')
    resource_dir = setup_test_env['resources_path']

    expected_document = f"""
    [Section]({os.path.join(setup_test_env['test_env_path'], 'docs/readme.md')}#section)
    [Query]({os.path.join(setup_test_env['test_env_path'], 'docs/readme.md')}?query=1)
    """

    result = redirect_url(document, document_path, resource_dir)
    assert result == expected_document

def test_no_resource_dir(setup_test_env):
    document = """
    ![Image](images/photo.png)
    [Readme](docs/readme.md)
    [Nonexistent](nonexistent/path/file.txt)
    """

    document_path = os.path.join(setup_test_env['test_env_path'], 'markdown.md')
    # No resource_dir provided

    expected_document = f"""
    ![Image]({os.path.join(setup_test_env['test_env_path'], 'images/photo.png')})
    [Readme]({os.path.join(setup_test_env['test_env_path'], 'docs/readme.md')})
    [Nonexistent](nonexistent/path/file.txt)
    """

    result = redirect_url(document, document_path)
    assert result == expected_document

if __name__ == "__main__":
    pytest.main([__file__])