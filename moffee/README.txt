File tree of moffee:

├── __init__.py
├── builder.py
├── cli.py
├── compositor.py
├── markdown.py
├── README.txt
├── templates
│  ├── beam
│  ├── blue
│  ├── default
│  └── robo
└── utils
   ├── __pycache__
   ├── file_helper.py
   ├── md_helper.py
   └── md_obsidian_ext.py


builder.py:     Generates html with jinja2, and makes output directory
cli.py:         Serve cli interfaces, launches live servers if specified
compositor.py:  Transforms markdown document into input data for jinja3 placeholders
markdown.py:    Configures python markdown and pymdownx extensions
templates:      Directory that contains html templates and static assets
    default:    Default theme
    beam:       Professional theme inspired from beamer
    robo:       A simple and modern theme
    blue:       A theme with dark blue background
    gaia:       Theme with paper and handwritting style
utils:          Utility functions
    file_helper.py:     File and directory manipulation
    md_helper.py:       Functions that handle markdown syntax
    md_obsidian_ext.py: Markdown extension for obsidian style callouts
