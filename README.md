<p align="center">
  <a href="https://github.com/BMPixel/moffee">
    <img src="https://github.com/user-attachments/assets/37fa6c1b-df21-4df1-9ccf-6075f009c74d" alt="moffee logo" width="500">
  </a>
</p>
<p align="center">
  <strong>moffee</strong>: Make Markdown Ready to Present
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

___

- Use `---` to trigger page breaks.
- Use `***` to arrange elements horizontally.
- Use `___` to split elements vertically.

moffee automatically adjusts element sizes to accommodate large blocks of text or complex illustrations.

***

![blue coffee](coffee.png)
```
</details>

<p align="center">
  <img src="https://github.com/user-attachments/assets/b766cf39-e46c-4b7d-8dfc-bb717feba974" alt="moffee example PDF">
</p>

## Installation

moffee is written in Python and is recommended to install with `pipx`:

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
layout: content # HTML template. Use "centered" for centered alignment.
resource_dir: "." # Relative URLs are based on this directory.
default_h1: false # Inherit H1 from previous slides if not defined.
default_h2: true  # Inherit H2
default_h3: true  # Inherit H3
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

## License

MIT License © 2024 [Wenbo Pan](https://wenbo.io)