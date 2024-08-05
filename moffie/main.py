import os
import shutil
from functools import partial
from jinja2 import Environment, FileSystemLoader
from moffie.compositor import composite
from moffie.markdown import md
from moffie.utils.md_helper import extract_title
from livereload import Server
import click

def render(document: str, template_dir) -> str:
    # Setup Jinja 2
    env = Environment(loader=FileSystemLoader(template_dir))

    env.filters["markdown"] = md

    template = env.get_template("index.html")

    # Fill template
    title = extract_title(document) or "Untitled"
    pages = composite(document)

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

    # Render
    return template.render(data)
        

def render_and_write(document_path: str, output_dir: str, template_dir):
    with open(document_path) as f:
        document = f.read()
    output_html = render(document, template_dir)

    os.makedirs(output_dir, exist_ok=True)

    shutil.copytree(template_dir, output_dir, dirs_exist_ok=True)
    output_file = os.path.join(output_dir, f"index.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_html)


@click.command()
@click.argument("md")
@click.argument("output")
@click.option(
    "--theme", default="base", help='Theme of slides, defaults to "base"'
)
@click.option(
    "--live",
    is_flag=True,
    help="Launch a live web server which updates html outputs on the markdown file, defaults to false",
)
def html(md: str, output: str, theme: str = "base", live: bool = False):
    """
    Render markdown file into slides, displayed in an html webpage.
    """

    template_dir = os.path.join(os.path.dirname(__file__), "..", "templates", theme)
    render_handler = partial(
        render_and_write, document_path=md, output_dir=output, template_dir=template_dir
    )

    render_handler()
    print(f"Generated html written to {os.path.join(output, "index.html")}")
    if live:
        server = Server()
        server.watch(md, render_handler)
        server.watch(template_dir, render_handler)
        server.serve(root=output)


if __name__ == "__main__":
    html()
