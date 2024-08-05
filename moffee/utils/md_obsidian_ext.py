"""
Adds obsidian callout/panel. Obsidian callout block is parsed to admonition format
    to make use of existing admonition styles.
"""

from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re
from markdown import blockparser

class ObsidianExtension(Extension):
    """ Obsidian extension for Python-Markdown. """

    def extendMarkdown(self, md):
        """ Add Obsidian to Markdown instance. """
        md.registerExtension(self)

        md.parser.blockprocessors.register(ObsidianProcessor(md.parser), 'obsidian', 105)


class ObsidianProcessor(BlockProcessor):

    CLASSNAME = 'admonition'
    CLASSNAME_TITLE = 'admonition-title'
    RE = re.compile(r'(?:^|\n)> \[!([\w\-]+)\] *(?: (.*?))? *(?:\n|$)')
    RE_SPACES = re.compile('  +')

    def __init__(self, parser: blockparser.BlockParser):
        """Initialization."""

        super().__init__(parser)

        self.current_sibling: etree.Element | None = None
        self.content_indent = 0

    def test(self, parent: etree.Element, block: str) -> bool:
        
        return self.RE.search(block)

    def dequote(self, text: str) -> tuple[str, str]:
        """ Remove a quote mark (>) from the front of each line of the given text. """
        newtext = []
        lines = text.split('\n')
        for line in lines:
            if line.startswith('> '):
                newtext.append(line[2:])
            elif line.startswith('>'):
                newtext.append(line[1:])
            elif not line.strip():
                newtext.append('')
            else:
                break
        return '\n'.join(newtext), '\n'.join(lines[len(newtext):])


    def run(self, parent: etree.Element, blocks: list[str]) -> None:
        block = blocks.pop(0)
        m = self.RE.search(block)

        if not m:
            raise ValueError()

        if m.start() > 0:
            self.parser.parseBlocks(parent, [block[:m.start()]])
        block = block[m.end():]  # removes the first line
        block, theRest = self.dequote(block)

        klass, title = self.get_class_and_title(m)
        div = etree.SubElement(parent, 'div')
        div.set('class', '{} {}'.format(self.CLASSNAME, klass))
        if title:
            p = etree.SubElement(div, 'p')
            p.text = title
            p.set('class', self.CLASSNAME_TITLE)

        self.parser.parseChunk(div, block)

        if theRest:
            # This block contained unindented line(s) after the first indented
            # line. Insert these lines as the first block of the master blocks
            # list for future processing.
            blocks.insert(0, theRest)

    def get_class_and_title(self, match: re.Match[str]) -> tuple[str, str | None]:
        klass, title = match.group(1).lower(), match.group(2)
        klass = self.RE_SPACES.sub(' ', klass)
        if title is None:
            # no title was provided, use the capitalized class name as title
            # e.g.: `> [!note]` will render
            # `<p class="admonition-title">Note</p>`
            title = klass.split(' ', 1)[0].capitalize()
        elif title == '':
            # an explicit blank title should not be rendered
            # e.g.: `> [!warning] ""` will *not* render `p` with a title
            title = None
        return klass, title


def makeExtension(**kwargs):  # pragma: no cover
    return ObsidianExtension(**kwargs)