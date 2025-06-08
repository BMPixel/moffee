# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

moffee uses uv for dependency management and build processes:

```bash
# Install dependencies
uv sync --dev

# Run moffee CLI directly
uv run moffee live example.md        # Launch live server for development
uv run moffee make example.md -o output/  # Generate static HTML slides

# Run tests
uv run pytest                        # Run all tests
uv run pytest tests/test_builder.py  # Run specific test file

# Code quality
uv run flake8 .                      # Lint code
uv run black .                       # Format code
uv run pre-commit run --all-files    # Run all pre-commit hooks
```

## Architecture Overview

moffee is a markdown-to-slides generator with a modular architecture:

### Core Pipeline
1. **cli.py** - Entry point that handles command-line interface and live server
2. **compositor.py** - Parses markdown into Page objects with frontmatter and layout decorators
3. **builder.py** - Orchestrates the build process and Jinja2 rendering
4. **markdown.py** - Configures Python-Markdown with extensions

### Key Components

**compositor.py** is the heart of the system:
- `composite()` function splits markdown into slides based on headers (h1-h3) and `---` dividers
- `PageOption` dataclass handles frontmatter configuration and local style decorators `@(key=value)`
- `Chunk` class creates hierarchical layout trees using `===` (vertical) and `<->` (horizontal) dividers
- Supports Obsidian-flavored markdown syntax

**builder.py** handles rendering:
- `render_jinja2()` processes Page objects into HTML using templates
- `retrieve_structure()` builds navigation/outline from heading hierarchy
- Asset management and path redirection for embedded resources

**Templates system**:
- Base template in `templates/base/` with core HTML structure and JavaScript
- Theme-specific CSS in `templates/{theme}/` directories (default, beam, robo, blue, gaia)
- Jinja2 layouts in `layouts/` subdirectories (content.html, centered.html, product.html)

### Slide Layout System
- Page breaks: New headers (h1-h3) or `---` dividers
- Horizontal layout: `<->` separator 
- Vertical layout: `===` separator (higher precedence)
- Style decorators: `@(layout=centered, background-color=blue)` for per-slide customization

### Configuration
- Global options via YAML frontmatter
- Local overrides using `@(property=value)` decorators
- Themes, aspect ratios, and custom CSS properties supported
- Resource directory handling for relative asset paths