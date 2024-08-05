from markdown import markdown
from markupsafe import Markup
import pymdownx.superfences

extensions = [
    "pymdownx.tasklist",
    "pymdownx.extra",
    "pymdownx.caret",
    "pymdownx.tilde",
    "nl2br", 
    "admonition",
    "pymdownx.superfences",
    "pymdownx.saneheaders",
    "pymdownx.betterem",
    "pymdownx.mark",
    "pymdownx.magiclink",
    "toc",
    "wikilinks",
    "pymdownx.inlinehilite",
    "moffee.utils.md_obsidian_ext"
]

extension_configs = {
    "pymdownx.superfences": {
        "custom_fences": [
            {
                "name": "mermaid",
                "class": "mermaid",
                "format": pymdownx.superfences.fence_div_format,
            }
        ]
    }
}

def md(text):
    return Markup(markdown(text, extensions=extensions, extension_configs=extension_configs))
