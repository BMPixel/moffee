import click
import os
from functools import partial
from moffee.builder import build, read_options
from livereload import Server
import tempfile


def run(md, output=None, live=False):
    """Process the markdown file to render slides."""
    if not output:
        output = tempfile.mkdtemp()
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    options = read_options(md)
    default_template_dir = os.path.join(template_dir, "default")
    if options.theme != "default":
        theme_template_dir = os.path.join(template_dir, options.theme)
    else:
        theme_template_dir = None
    render_handler = partial(
        build, document_path=md, output_dir=output, template_dir=default_template_dir, theme_dir=theme_template_dir
    )

    render_handler()
    print(f"Generated html written to {os.path.join(output, 'index.html')}")
    if live:
        server = Server()
        server.watch(md, render_handler)
        server.watch(default_template_dir, render_handler)
        if theme_template_dir:
            server.watch(theme_template_dir, render_handler)
        server.serve(root=output)


@click.group(help="""
Render markdown file into slides.

This tool allows you to convert markdown files into HTML slides,
either generating them once or launching a live server to continuously
update the output as changes are made to the markdown file.
""")
def cli():
    pass

@cli.command(help="""
Generate slides from a markdown file.

This command takes a markdown file as input and produces a set of slides
formatted as an HTML file. You can specify an output directory where the
HTML will be saved. 

Example usage:

\b
  python moffee.py make example.md -o output/
""")
@click.argument('markdown', metavar='<markdown-file>')
@click.option('-o', '--output', metavar='<output-path>', default=None, help='Output file path. If not specified, a temporary directory will be used.')
def make(markdown, output):
    """Generate slides from a markdown file."""
    run(markdown, output, live=False)

@cli.command(help="""
Launch live mode to update HTML outputs.

This command starts a live server that watches for changes to the specified
markdown file. As changes are made, the slides are automatically updated and
reflected in the browser. 

Example usage:

\b
  python moffee.py live example.md
""")
@click.argument('markdown', metavar='<markdown-file>')
def live(markdown):
    """Launch live mode to update html outputs."""
    run(markdown, output=None, live=True)

if __name__ == "__main__":
    cli()