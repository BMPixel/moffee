import os
import pytest
import shutil
import tempfile

from moffee.utils.file_helper import (
    copy_assets,
) 


@pytest.fixture
def setup_test_environment():
    temp_dir = tempfile.mkdtemp()

    sample_image_path = os.path.join(temp_dir, "sample.png")
    sample_pdf_path = os.path.join(temp_dir, "document.pdf")

    with open(sample_image_path, "w") as f:
        f.write("This is a test image file.")

    with open(sample_pdf_path, "w") as f:
        f.write("This is a test PDF file.")

    yield temp_dir, sample_image_path, sample_pdf_path

    shutil.rmtree(temp_dir)


def test_copy_assets_updates_links(setup_test_environment):
    temp_dir, sample_image_path, sample_pdf_path = setup_test_environment
    target_dir = os.path.join(temp_dir, "asset_resources")

    markdown_doc = f"""
    Here is an image: "{sample_image_path}"
    And another file: "{sample_pdf_path}"
    """

    updated_doc = copy_assets(markdown_doc, target_dir)

    # Check that the target directory is created
    assert os.path.exists(target_dir)

    # Verify that files have been moved and renamed
    moved_files = os.listdir(target_dir)
    assert len(moved_files) == 2

    # Check if document URLs are updated with new file names
    for moved_file in moved_files:
        assert os.path.join(target_dir, moved_file) in updated_doc


def test_copy_assets_ignores_nonexistent_files():
    temp_dir = tempfile.mkdtemp()
    target_dir = os.path.join(temp_dir, "asset_resources")

    markdown_doc = """
    Here is an image: "images/nonexistent.png"
    And another file: "files/nonexistent.pdf"
    """

    updated_doc = copy_assets(markdown_doc, target_dir)

    # Verify that document URLs remain unchanged
    assert "images/nonexistent.png" in updated_doc
    assert "files/nonexistent.pdf" in updated_doc

    shutil.rmtree(temp_dir)


def test_copy_assets_creates_target_directory():
    temp_dir = tempfile.mkdtemp()
    target_dir = os.path.join(temp_dir, "asset_resources")

    markdown_doc = """
    Here is an image: "images/sample.png"
    """

    # Assuming the image does not exist, but we're checking the creation
    updated_doc = copy_assets(markdown_doc, target_dir)

    # Check that the target directory is created even if it's empty
    assert os.path.exists(target_dir)

    shutil.rmtree(temp_dir)
