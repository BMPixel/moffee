<p align="center">
  <a href="https://github.com/BMPixel/moffee">
    <img src="https://raw.githubusercontent.com/BMPixel/moffee/main/docs/images/logo.png" alt="moffee logo" width="150">
  </a>
</p>
<h1 align="center">
moffee
</h1>
<p align="center">
Make Markdown Ready to Present.
<p>
<p align="center">
  <a href="https://github.com/bmpixel/moffee/actions/workflows/python-app-test.yaml">
    <img src="https://github.com/bmpixel/moffee/actions/workflows/python-app-test.yaml/badge.svg" alt="GitHub Actions">
  </a>
  <a href="https://pypi.org/project/moffee/">
    <img src="https://img.shields.io/pypi/v/moffee.svg" alt="PyPI version">
  </a>
  <a href="https://github.com/bmpixel/moffee/blob/main/LICENSE">
    <img src="https://img.shields.io/pypi/l/moffee.svg" alt="License">
  </a>
  <a href="https://moffee.readthedocs.io/en/latest/">
    <img src="https://readthedocs.org/projects/moffee/badge/?version=latest" alt="Doc build status">
  </a>
  <a href="https://github.com/bmpixel/moffee">
    <img src="https://img.shields.io/github/stars/bmpixel/moffee.svg?style=social" alt="GitHub stars">
  </a>
</p>

moffee is an open-source slide maker that transforms markdown documents into clean, professional slide decks.

- **moffee handles layout, pagination, and styling**, so you can focus on your content.
- **There's little to learn**. moffee uses simple syntax to arrange and style content to your liking.
- **A live web interface** updates slides as you type, allowing you to start a slideshow or export it to PDF.

## An Example

<details>
  <summary> Click to expand input markdown document (29 lines)</summary>

```markdown
# moffee
## Make markdown ready to present
@(layout=centered)

## Why moffee?

- **80/20 Rule**[^1]: Creating slides can be time-consuming, often requiring 80% of the effort for just 20% of the outcome.
- `moffee` transforms markdown into professional presentations effortlessly.
    - Use simple markdown syntax.
    - Enjoy out-of-the-box paging and styling.
    - Easily arrange text and images.

[^1]: https://en.wikipedia.org/wiki/Pareto_principle

## Showcasing
### Style with Markdown

==Markdown== is all you need! Elements like $tex$ and `code` are rendered with elegant style.

!!! note
    moffee automatically breaks pages and chooses titles based on context.

### Media Layout

One of moffee's strengths is using dividers to organize text and images effectively.

===

- Use `---` to trigger page breaks.
- Use `<->` to arrange elements horizontally.
- Use `===` to split elements vertically.

moffee automatically adjusts element sizes to accommodate large blocks of text or complex illustrations.

<->

![blue coffee](coffee.png)
```
</details>

<p align="center">
  <img src="https://raw.githubusercontent.com/BMPixel/moffee/main/docs/images/moffee-example.png" alt="moffee example PDF">
</p>

Or you can use other built-in [themes](https://moffee.readthedocs.io/en/latest/theme/):

<table>
  <tr>
    <td align="center"><strong>default</strong></td>
    <td align="center"><strong>beam</strong></td>
    <td align="center"><strong>robo</strong></td>
  </tr>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/BMPixel/moffee/main/docs/images/default.png" alt="default theme" /></td>
    <td align="center"><img src="https://raw.githubusercontent.com/BMPixel/moffee/main/docs/images/beam.png" alt="beam theme" /></td>
    <td align="center"><img src="https://raw.githubusercontent.com/BMPixel/moffee/main/docs/images/robo.png" alt="robo theme" /></td>
  </tr>
  <tr>
    <td align="center"><strong>blue</strong></td>
    <td align="center"><strong>gaia</strong></td>
    <td></td>
  </tr>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/BMPixel/moffee/main/docs/images/blue.png" alt="blue theme" /></td>
    <td align="center"><img src="https://raw.githubusercontent.com/BMPixel/moffee/main/docs/images/gaia.png" alt="gaia theme" /></td>
    <td></td>
  </tr>
</table>

## Installation

moffee is written in Python and is recommended to install with `pipx`. See [our documentation](https://moffee.readthedocs.io/en/latest/installation/) for step-by-step instructions.

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

To start, write in standard markdown. moffee supports most extended syntax found in [Obsidian Flavored Markdown](https://help.obsidian.md/Editing+and+formatting/Obsidian+Flavored+Markdown). See [the syntax documentation](https://moffee.readthedocs.io/en/latest/syntax/) for more details.

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

In addition to `---`, moffee supports `<->` and `===` for in-slide layout. Use `<->` to separate elements horizontally:

```markdown
Text on the left.
<->
![Image on the right](https://placehold.co/600x400)
```

`===` places elements vertically and takes precedence over `<->`. Use them together for flexible layouts:

```markdown
Top bun
===
Patty on the left
<->
Lettuce on the right
===
Bottom bun
```

### Options and Styles

Front matter is used to define moffee's behavior. Here are some common used options. Refer to [Configuration](https://moffee.readthedocs.io/en/latest/configuration/) for the full list.

```yaml
---
theme: default # Other availble themes are "beam", "robo", "blue" and "gaia"
layout: content # HTML template. Use "centered" for centered alignment.
resource_dir: "." # Relative URLs are based on this directory.
aspect_ratio: "16:9" # Aspect ratio of the slides
---
```

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

## Contributing

Find moffee helpful? ![star](https://img.shields.io/github/stars/bmpixel/moffee.svg?style=social) are the best motivation to keep me improving. So thank you! ;)

To submit bug/feature requests/PR, please see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License © 2024 [Wenbo Pan](https://wenbo.io)
