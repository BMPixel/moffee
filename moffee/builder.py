import os
import shutil
from jinja2 import Environment, FileSystemLoader
from moffee.compositor import PageOption, composite, parse_frontmatter
from moffee.markdown import md
from moffee.utils.md_helper import extract_title
from moffee.utils.file_helper import redirect_paths, copy_assets, merge_directories

def read_options(document_path) -> PageOption:
    """Read frontmatter options from the document path"""
    with open(document_path, 'r') as f:
        document = f.read()
    _, options = parse_frontmatter(document)
    return options

def render_jinja2(document: str, template_dir) -> str:
    """Run jinja2 templating to create html"""
    # Setup Jinja 2
    env = Environment(loader=FileSystemLoader(template_dir))

    env.filters["markdown"] = md

    template = env.get_template("index.html")

    # Fill template
    pages = composite(document)
    title = extract_title(document) or "Untitled"

    data = {
        "title": title,
        "slides": [
            {
                "h1": page.h1,
                "h2": page.h2,
                "h3": page.h3,
                "chunk": page.chunk,
                "layout": page.option.layout,
                "styles": page.option.styles
            }
            for page in pages
        ],
    }

    return template.render(data)


def build(document_path: str, output_dir: str, template_dir: str, theme_dir: str=None):
    """Render document, create output directories and write result html."""
    with open(document_path) as f:
        document = f.read()
    asset_dir = os.path.join(output_dir, "assets")

    merge_directories(template_dir, output_dir, theme_dir)
    options = read_options(document_path)
    output_html = render_jinja2(document, output_dir)
    output_html = redirect_paths(output_html, document_path=document_path, resource_dir=options.resource_dir)
    output_html = copy_assets(output_html, asset_dir).replace(asset_dir, "assets")

    output_file = os.path.join(output_dir, f"index.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_html)