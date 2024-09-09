# Adapt from https://github.com/sgryjp/markdown_math_escape/blob/main/markdown_math_escape/core.py
import io
import logging
import re
import xml.etree.ElementTree as etree
from base64 import b64decode, b64encode
from typing import List, Match

import markdown
import markdown.blockprocessors
import markdown.extensions
import markdown.inlinepatterns
import markdown.postprocessors
import markdown.preprocessors

_logger = logging.getLogger(__name__)
_default_delimiters = "dollers"

_re_dollers_inline = re.compile(r"(?<!\\)\$(?!\$)(?P<expr>[^\$]*)(?<!\\)\$(?!\$)")
_re_dollers_block_begin = re.compile(r"^(?P<indent>\s*)(?P<fence>\$\$)")
_re_dollers_block_end = re.compile(r"^(?P<indent>\s*)(?P<fence>\$\$)(?P<trailings>.*)$")

_re_brackets_inline = re.compile(r"\\\((?P<expr>[^\$]+(?!\)))\\\)")
_re_brackets_block_begin = re.compile(r"^(?P<indent>\s*)(?P<fence>\\\[)")
_re_brackets_block_end = re.compile(
    r"^(?P<indent>\s*)(?P<fence>\\\])(?P<trailings>.*)$"
)

_re_gitlab_inline = re.compile(r"(?<!\\)\$`(?P<expr>[^`]*)`\$")
_re_gitlab_block_begin = re.compile(r"^(?P<indent>\s*)(?P<fence>```+|~~~+)math")
_re_gitlab_block_end = re.compile(
    r"^(?P<indent>\s*)(?P<fence>```+|~~~+)(?P<trailings>.*)$"
)

_re_escaped_inline_math = re.compile(
    r'<code class="--markdown-math-escape">([A-Za-z0-9+/=]+)</code>'
)
_escaped_block_math_begin = '<pre class="--markdown-math-escape">'


_profiles = {
    "dollers": {
        "re_inline": _re_dollers_inline,
        "re_block_begin": _re_dollers_block_begin,
        "re_block_end": _re_dollers_block_end,
        "match_fences": lambda o, c: True,
    },
    "brackets": {
        "re_inline": _re_brackets_inline,
        "re_block_begin": _re_brackets_block_begin,
        "re_block_end": _re_brackets_block_end,
        "match_fences": lambda o, c: True,
    },
    "gitlab": {
        "re_inline": _re_gitlab_inline,
        "re_block_begin": _re_gitlab_block_begin,
        "re_block_end": _re_gitlab_block_end,
        "match_fences": lambda o, c: o == c,
    },
}


def _encode(s: str) -> str:
    s2 = s.replace("&", "&amp;")
    s2 = s2.replace("<", "&lt;")
    s2 = s2.replace(">", "&gt;")
    try:
        return b64encode(s2.encode("utf-8")).decode("utf-8")
    except Exception:
        _logger.warning("Failed to encode %s", repr(s))
        return s


def _decode(s: str) -> str:
    try:
        return b64decode(s.encode("utf-8")).decode("utf-8")
    except Exception:
        _logger.warning("Failed to decode %s", repr(s))
        return s


def makeExtension(**kwargs):
    """Register this extension to Python-Markdown."""
    _logger.debug("Registering...")
    return MathEscapeExtension(**kwargs)


class MathEscapeExtension(markdown.extensions.Extension):
    def __init__(self, **kwargs):
        self.config = {
            "delimiters": [
                _default_delimiters,
                "Delimiters surrounding math expressions.",
            ],
        }
        super(MathEscapeExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        delimiters = self.getConfig("delimiters")
        if delimiters not in _profiles:
            _logger.warning(
                'Falling back "delimiters" to "%s"; "%s" is not of (%s).',
                _default_delimiters,
                delimiters,
                ", ".join([f'"{k}"' for k in _profiles]),
            )
            delimiters = _default_delimiters

        md.preprocessors.register(
            MathEscapePreprocessor(md, delimiters),
            "math_escape",
            priority=1000,
        )
        md.postprocessors.register(
            MathEscapePostprocessor(md, delimiters),
            "math_escape",
            priority=0,
        )
        md.inlinePatterns.register(
            MathEscapeInlineProcessor(md, delimiters),
            "math_escape",
            priority=1000,
        )


class MathEscapePreprocessor(markdown.preprocessors.Preprocessor):
    """Preprocessor to base64 encode math blocks and enclose them in '<pre>'s."""

    def __init__(self, md, delimiters):
        self._re_block_begin = _profiles[delimiters]["re_block_begin"]
        self._re_block_end = _profiles[delimiters]["re_block_end"]
        self._match_fences = _profiles[delimiters]["match_fences"]
        super().__init__(md)

    def run(self, lines: List[str]):
        i = 0
        while i < len(lines):
            match1 = self._re_block_begin.match(lines[i])
            if match1:
                j, match2 = self._find_closing_pair(lines, i, match1)
                if 0 <= j:
                    # Replace opening fence with "<pre>\["
                    lines[i] = (
                        match1.group("indent") + _escaped_block_math_begin + r"\["
                    )

                    # Encode lines inside the block
                    for k in range(i + 1, j):
                        lines[k] = _encode(lines[k])

                    # Replace closing fence with "\]</pre>"
                    lines[j] = (
                        match2.group("indent")
                        + r"\]"
                        + match2.group("trailings")
                        + "</pre>"
                    )
                    i = j
            i += 1
        return lines

    def _find_closing_pair(self, lines: List[str], i, match):
        for j in range(i + 1, len(lines)):
            match2 = self._re_block_end.match(lines[j])
            if (
                match2
                and match2.group("indent") == match.group("indent")
                and self._match_fences(match.group("fence"), match2.group("fence"))
            ):
                return j, match2
        return -1, None


class MathEscapePostprocessor(markdown.postprocessors.Postprocessor):
    def __init__(self, md, delimiters):
        super().__init__(md)

    def run(self, text: str):
        num_blocks = 0
        num_inlines = 0
        lines = []
        newline = "\n"
        istream = io.StringIO(text)
        try:
            in_block = False
            for i, line in enumerate(istream):
                # Use the new line code used for the first line
                if i == 0:
                    match = re.search(r"\r?\n$", line, re.MULTILINE)
                    if match:
                        newline = match.group(0)

                # Discard just one new line code from the input if exists
                if line.endswith(newline):
                    line = line[: -len(newline)]

                # Replace blocks
                if not in_block and _escaped_block_math_begin in line:
                    in_block = True
                    lines.append(line.replace(_escaped_block_math_begin, ""))
                elif in_block and "</pre>" in line:
                    in_block = False
                    lines.append(line.replace("</pre>", "", 1))
                    num_blocks += 1
                elif in_block:
                    decoded = _decode(line)
                    lines.append(decoded)
                else:  # if not inside a math block
                    # Replace all inline math expressions in this line
                    tokens = []
                    offset = 0
                    while True:
                        match = _re_escaped_inline_math.search(line, offset)
                        if not match:
                            break
                        mathexpr = _decode(match.group(1))
                        tokens.append(line[offset : match.start()] + mathexpr)
                        offset = match.end()
                        num_inlines += 1
                    tokens.append(line[offset:])
                    lines.append("".join(tokens))

            # Log summary
            if 0 < num_blocks + num_inlines:
                _logger.debug(
                    "Processed %d blocks and %d inlines.",
                    num_blocks,
                    num_inlines,
                )
            return newline.join(lines)
        finally:
            istream.close()


class MathEscapeInlineProcessor(markdown.inlinepatterns.InlineProcessor):
    def __init__(self, md, delimiters):
        pattern = _profiles[delimiters]["re_inline"].pattern
        super().__init__(pattern, md)

    def handleMatch(self, match: Match, data: str):
        elm = etree.Element("code")
        elm.set("class", "--markdown-math-escape")
        elm.text = _encode(r"\(" + match.group(1) + r"\)")
        return elm, match.start(0), match.end(0)
