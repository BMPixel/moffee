from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from md_helper import get_header_level, is_divider, is_empty, contains_image

@dataclass
class PageOption:
    default_h1: bool = False
    default_h2: bool = True
    default_h3: bool = True
    layout: str = "top-down"

@dataclass
class Chunk:
    content: str
    type: str = "paragraph"


@dataclass
class Page:
    raw_md: str
    option: PageOption
    chunks: List[Chunk] = field(default_factory=list)
    h1: Optional[str] = None
    h2: Optional[str] = None
    h3: Optional[str] = None

    @property
    def title(self) -> Optional[str]:
        return self.h1 or self.h2 or self.h3

    @property
    def subtitle(self) -> Optional[str]:
        if self.h1:
            return self.h2 or self.h3
        elif self.h2:
            return self.h3
        return None
    
    def chunk(self):
        """
        Split raw_md into chunks based on the following criteria:
        - Before/after lines that contain images
        - Two consecutive blank lines

        Modifies the page's 'chunks' list in-place.
        """
        lines = self.raw_md.split("\n")
        current_chunk = []
        blank_line_count = 0

        for i, line in enumerate(lines):
            if contains_image(line):
                if current_chunk:
                    self.chunks.append(Chunk(content="\n".join(current_chunk)))
                    current_chunk = []
                self.chunks.append(Chunk(content=line, type="image"))
                blank_line_count = 0
            elif is_empty(line):
                blank_line_count += 1
                if blank_line_count == 2:
                    if current_chunk:
                        self.chunks.append(Chunk(content="\n".join(current_chunk)))
                        current_chunk = []
                    blank_line_count = 0
                else:
                    current_chunk.append(line)
            else:
                current_chunk.append(line)
                blank_line_count = 0

            # Check if it's the last line
            if i == len(lines) - 1 and current_chunk:
                self.chunks.append(Chunk(content="\n".join(current_chunk)))

    def process(self):
        # Any additional processing needed for the page
        pass

def parse_md_yaml(document: str) -> Tuple[str, PageOption]:
    """
    Parse the yaml header in a given markdown document
    TODO: actual option retrival

    :param document: Input markdown document as a string.
    :return: document with yaml removed and the PageOption
    """
    document = document.strip()
    option = PageOption()
    return document, option

def paginate(document: str, option: PageOption = None) -> List[Page]:
    """
    Paginates a markdown document into slide pages.

    Splitting criteria:
    - New h1/h2/h3 header (except when following another header)
    - More than 12 non-empty lines in a page
    - Divider (___, ***, +++)

    :param document: Input markdown document as a string.
    :param option: PageOption object containing pagination configuration. Will try to parse from document yaml area if None.
    :return: List of Page objects representing paginated slides.
    """
    pages: List[Page] = []
    current_page_lines = []
    current_h1 = current_h2 = current_h3 = None
    line_count = 0
    prev_line_was_header = False
    
    document, parsed_option = parse_md_yaml(document)
    if option == None:
        option = parsed_option

    lines = document.split("\n")

    def create_page():
        nonlocal current_page_lines, line_count, current_h1, current_h2, current_h3
        # Only make new page if has non empty lines

        if all([l.strip() == '' for l in current_page_lines]):
            return

        raw_md = "\n".join(current_page_lines)
        page = Page(raw_md=raw_md, 
                    option=option, 
                    h1=current_h1,
                    h2=current_h2,
                    h3=current_h3)

        pages.append(page)
        current_page_lines = []
        line_count = 0
        current_h1 = current_h2 = current_h3 = None

    for _, line in enumerate(lines):
        header_level = get_header_level(line)

        # Check if this is a new header and not consecutive
        if header_level > 0 and not prev_line_was_header:
            # Check if the next line is also a header
            create_page()

        if line_count > 12:
            create_page()
            
        if is_divider(line):
            create_page()
            continue

        match header_level:
            case 1:
                current_h1 = line.lstrip("#").strip()
            case 2:
                current_h2 = line.lstrip("#").strip()
            case 3:
                current_h3 = line.lstrip("#").strip()
            case _:
                pass  # Handle other cases or do nothing

        current_page_lines.append(line)
        if not is_empty(line):
            line_count += 1

        if header_level > 0:
            prev_line_was_header = True
        if header_level == 0 and not is_empty(line):
            prev_line_was_header = False

    # Create the last page if there's remaining content
    create_page()

    # Process each page
    env_h1 = env_h2 = env_h3 = None
    for page in pages:
        inherit_h1 = page.option.default_h1
        inherit_h2 = page.option.default_h2
        inherit_h3 = page.option.default_h3
        if page.h1 != None:
            env_h1 = page.h1
            env_h2 = env_h3 = None
            inherit_h1 = inherit_h2 = inherit_h3 = False
        if page.h2 != None:
            env_h2 = page.h2
            env_h3 = None
            inherit_h2 = inherit_h3 = False
        if page.h3 != None:
            env_h3 = page.h3
            inherit_h3 = False
        if inherit_h1:
            page.h1 = env_h1
        if inherit_h2:
            page.h2 = env_h2
        if inherit_h3:
            page.h3 = env_h3

        page.chunk()

    return pages

if __name__ == "__main__":
    # Test the paginate function
    test_document = """
# Main Title

## Subtitle

Content of the first slide.

---

## Second Slide

- Bullet point 1
- Bullet point 2

### Subheader
More content.
![](Image.png)

## Another Header
### Consecutive Header

Normal text here.

# New Main Title

1. Numbered list
2. Second item
3. Third item

This is a long paragraph that should trigger a new page due to line count.
It continues for several lines to demonstrate the line count limit.
We'll add more lines to ensure it goes over the 12 non-empty lines limit.
This is line 4.
This is line 5.
This is line 6.
This is line 7.
This is line 8.
This is line 9.
This is line 10.
This is line 11.
This is line 12.
This line should be on a new page.
    """

    option = PageOption(default_h1=False, default_h2=True, default_h3=True)
    pages = paginate(test_document, option)

    print(f"Total pages created: {len(pages)}")
    for i, page in enumerate(pages, 1):
        print(f"\nPage {i}:")
        print(f"H1: {page.h1}")
        print(f"H2: {page.h2}")
        print(f"H3: {page.h3}")
        print(f"Title: {page.title}")
        print(f"Subtitle: {page.subtitle}")
        print("Content:")
        print(page.raw_md)
        print("Chunks:")
        for j, chunk in enumerate(page.chunks, 1):
            print(f"  Chunk {j}:")
            print(f"    Type: {chunk.type}")
            print(f"    Content:")
            print(f"      {chunk.content.replace(chr(10), chr(10) + '      ')}")
        print("-" * 40)