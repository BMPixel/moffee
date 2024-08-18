# Getting Started

## Installation

moffee is written in Python and is recommended to install with `pipx`. See [Installation](installation.md) for detailed instructions.

```bash
pipx install moffee
# or `pip install moffee`
```

Preview slides in a live web server or export to HTML:

```bash
moffee live example.md # launch a server
# or
moffee make example.md -o output_html/ # export to HTML
```


## Usage

> [!tip]
> See [Syntax](syntax.md) for all supported syntax and their coresponding usages.

To start, write in standard markdown. moffee supports most extended syntax found in [Obsidian Flavored Markdown](https://help.obsidian.md/Editing+and+formatting/Obsidian+Flavored+Markdown).

```markdown
# Markdown Title
Use **bold** and *italic* for emphasis.

- Extended syntax like ~~strikethroughs~~ is supported.
```

To create a new slide, begin a new heading:

```markdown
## Page 1
Some text

## Page 2
This sentence will appear on the second slide.
```

Alternatively, use `---` to manually trigger a new slide:

```markdown
## Page 1
Text on the first slide
---
Text on the next slide.
```

You'll notice the second slide shares the `Page 1` title. moffee selects the most suitable title for each slide.

In addition to `---`, moffee supports `***` and `___` for in-slide layout. Use `***` to separate elements horizontally:

```markdown
Text on the left.
***
![Image on the right](https://placehold.co/600x400)
```

`___` places elements vertically and takes precedence over `***`. Use them together for flexible layouts:

```markdown
Top bun
___
Patty on the left
***
Lettuce on the right
___
Bottom bun
```

### Options and Styles

Front matter is used to define moffee's behavior. Default values are:

```yaml
---
theme: default # Other availble themes are "beam", "robo", "blue" and "gaia"
layout: content # HTML template. Use "centered" for centered alignment.
resource_dir: "." # Relative URLs are based on this directory.
default_h1: false # Inherit H1 from previous slides if not defined.
default_h2: true  # Inherit H2
default_h3: true  # Inherit H3
---
```

You can refer to [Configuration](configuration.md) for more information.

Any CSS property can be set in the front matter. For example, set a dark gray background for all slides:

```yaml
---
layout: content
background-color: darkgray
color: white
---
```

moffee also supports local style decorators with the syntax `@(property=value)`. Use these within the document to set attributes for specific slides:

```markdown
# A refined landing page
Our journey begins here
@(layout=content, background-image='url("https://placehold.co/600x400")')
```
