import pytest

from moffee.compositor import parse_deco, PageOption


def test_basic_deco():
    line = "@(layout=split, background=blue)"
    option = parse_deco(line)
    assert option.layout == "split"
    assert option.styles == {"background": "blue"}


def test_empty_deco():
    line = "@()"
    option = parse_deco(line)
    assert option == PageOption()


def test_invalid_deco():
    line = "This is not a deco"
    with pytest.raises(ValueError):
        _ = parse_deco(line)


def test_deco_with_base_option():
    line = "@(layout=split, default_h1=true, custom_key=value)"
    base_option = PageOption(
        layout="content", default_h1=False, default_h2=True, default_h3=True
    )
    updated_option = parse_deco(line, base_option)

    assert updated_option.styles == {"custom_key": "value"}
    assert updated_option.layout == "split"
    assert updated_option.default_h1 is True
    assert updated_option.default_h2 is True
    assert updated_option.default_h3 is True


def test_deco_with_type_conversion():
    line = "@(default_h1=true, default_h2=false, layout=centered, custom_int=42, custom_float=3.14)"
    base_option = PageOption()
    updated_option = parse_deco(line, base_option)

    assert updated_option.styles == {"custom_int": 42, "custom_float": 3.14}
    assert updated_option.default_h1 is True
    assert updated_option.default_h2 is False
    assert updated_option.layout == "centered"


def test_deco_with_spaces():
    line = "@(  layout = split,   background = blue  )"
    option = parse_deco(line)
    assert option.layout == "split"
    assert option.styles == {"background": "blue"}


def test_deco_with_quotes():
    line = "@(layout = \"split\",length='34px')"
    option = parse_deco(line)
    assert option.layout == "split"
    assert option.styles == {"length": "34px"}


def test_deco_with_hyphen():
    line = "@(background-color='red')"
    option = parse_deco(line)
    assert option.styles == {"background-color": "red"}


def test_deco_with_complex_url():
    line = """@(background-image='url("https://www.example.com/hello(world, this%20isa complex@url)")')"""
    option = parse_deco(line)
    assert option.styles == {
        "background-image": 'url("https://www.example.com/hello(world, this%20isa complex@url)")'
    }


def test_computed_slide_size():
    page_option = PageOption()
    assert page_option.computed_slide_size == (720, 405)

    page_option = PageOption(slide_width=1280)
    assert page_option.computed_slide_size == (1280, 405)

    page_option = PageOption(slide_height=540)
    assert page_option.computed_slide_size == (720, 540)

    page_option = PageOption(aspect_ratio="4:3")
    assert page_option.computed_slide_size == (720, 540)

    page_option = PageOption(slide_width=1024, aspect_ratio="4:3")
    assert page_option.computed_slide_size == (1024, 768)

    page_option = PageOption(slide_height=768, aspect_ratio="16:10")
    assert page_option.computed_slide_size == (1228.8, 768)

    with pytest.raises(
        ValueError,
        match="Aspect ratio, width and height cannot be changed at the same time!",
    ):
        PageOption(
            slide_width=1280, slide_height=720, aspect_ratio="4:3"
        ).computed_slide_size

    with pytest.raises(ValueError, match="Incorrect aspect ratio format:"):
        PageOption(aspect_ratio="16-9").computed_slide_size


if __name__ == "__main__":
    pytest.main()
