<p align="center">
  <a href="https://github.com/BMPixel/moffee">
  <img src="https://github.com/user-attachments/assets/37fa6c1b-df21-4df1-9ccf-6075f009c74d" alt="moffee logo" width="500">
  </a>
</p>
<p align="center">
  <strong>moffee</strong>: Make markdown ready to present
</p>

moffee is an open source slide maker. It transforms the markdown document you want to present into a clean slide sheet. 

- moffee handles layout, pagination and styling, so you can focus on your text.
- There are few things to learn. moffee brings simple syntax to allow arranging and styling content to your like.
- A live web interface updates slides as you type, where you can start the slideshow or export it to PDF.

## An Example

<details>
  <summary> Markdown Document (29 lines)</summary>
  
```markdown
# Moffee
## Make markdown ready to present
@(layout=centered)

## Why Moffee?

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

Result slide:

## Installation

moffie is written in python. It's recommended to install with `pipx`:

```bash
pipx install moffie
# or `pip install moffie`
```

Preview slides in a live web server or export to html:

```bash
moffee example.md --live # launch a server
# or
moffee example.md output_html/ # export to html
```

## Use moffee

moffee uses frontmatter to configure and repurposes dividers (`---`) for creating and arrange pages. This section covers everything about customize the slides.

