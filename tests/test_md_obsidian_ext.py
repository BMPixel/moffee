import pytest
from markdown import markdown


def check_markdown_conversion(text, expected):
    md = markdown(text, extensions=["mdbeamer.utils.md_obsidian_ext"])
    assert md.strip() == expected.strip()


def test_no_obsd():
    text = "Hello!"
    expected = "<p>Hello!</p>"
    check_markdown_conversion(text, expected)


def test_no_title():
    text = """
> [!note]
> Text
"""
    expected = """
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Text</p>
</div>
"""
    check_markdown_conversion(text, expected)


def test_with_title():
    text = """
> [!danger] title here
"""
    expected = """
<div class="admonition danger">
<p class="admonition-title">title here</p>
</div>
"""
    check_markdown_conversion(text, expected)


def test_complex():
    text = """
> [!note]
> co
>[!note]
 
> [!warning]
> co
> 
> - item1
> - item2
"""
    expected = """
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>co
[!note]</p>
</div>
<div class="admonition warning">
<p class="admonition-title">Warning</p>
<p>co</p>
<ul>
<li>item1</li>
<li>item2</li>
</ul>
</div>
"""
    check_markdown_conversion(text, expected)


def test_admonition_multiline():
    text = """
> [!info]
> This is a multiline
> admonition test case.
"""
    expected = """
<div class="admonition info">
<p class="admonition-title">Info</p>
<p>This is a multiline
admonition test case.</p>
</div>
"""
    check_markdown_conversion(text, expected)


def test_admonition_with_list():
    text = """
> [!tip]
> Here are some tips:
>
> - Tip 1
> - Tip 2
"""
    expected = """
<div class="admonition tip">
<p class="admonition-title">Tip</p>
<p>Here are some tips:</p>
<ul>
<li>Tip 1</li>
<li>Tip 2</li>
</ul>
</div>
"""
    check_markdown_conversion(text, expected)


def test_nested_admonitions():
    text = """
> [!warning] Outer warning
> > [!note] Inner note
> > Inner note text.
"""
    expected = """
<div class="admonition warning">
<p class="admonition-title">Outer warning</p>
<div class="admonition note">
<p class="admonition-title">Inner note</p>
<p>Inner note text.</p>
</div>
</div>
"""
    check_markdown_conversion(text, expected)


def test_admonition_no_content():
    text = """
> [!quote]
"""
    expected = """
<div class="admonition quote">
<p class="admonition-title">Quote</p>
</div>
"""
    check_markdown_conversion(text, expected)


def test_admonition_with_inline_markdown():
    text = """
> [!note] Inline Markdown
> This is **bold** text and *italic* text.
"""
    expected = """
<div class="admonition note">
<p class="admonition-title">Inline Markdown</p>
<p>This is <strong>bold</strong> text and <em>italic</em> text.</p>
</div>
"""
    check_markdown_conversion(text, expected)


def test_admonition_with_code_block():
    text = """
> [!info] Code Example
> ```
> def hello():
>     return "Hello, World!"
> ```
"""
    expected = """
<div class="admonition info">
<p class="admonition-title">Code Example</p>
<p><code>def hello():
    return "Hello, World!"</code></p>
</div>
"""
    check_markdown_conversion(text, expected)
