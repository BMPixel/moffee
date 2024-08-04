import pytest

from moffie.splitter import parse_deco, PageOption


def test_basic_deco():
    line = "@(layout=split, background=blue)"
    deco, option = parse_deco(line)
    assert deco == {"layout": "split", "background": "blue"}
    assert option is None


def test_empty_deco():
    line = "@()"
    deco, option = parse_deco(line)
    assert deco == {}
    assert option is None


def test_invalid_deco():
    line = "This is not a deco"
    with pytest.raises(ValueError):
        _, _ = parse_deco(line)


def test_deco_with_base_option():
    line = "@(layout=split, default_h1=true, custom_key=value)"
    base_option = PageOption(
        layout="content", default_h1=False, default_h2=True, default_h3=True
    )
    deco, updated_option = parse_deco(line, base_option)

    assert deco == {"custom_key": "value"}
    assert updated_option.layout == "split"
    assert updated_option.default_h1 is True
    assert updated_option.default_h2 is True
    assert updated_option.default_h3 is True


def test_deco_with_type_conversion():
    line = "@(default_h1=true, default_h2=false, layout=centered, custom_int=42, custom_float=3.14)"
    base_option = PageOption()
    deco, updated_option = parse_deco(line, base_option)

    assert deco == {"custom_int": 42, "custom_float": 3.14}
    assert updated_option.default_h1 is True
    assert updated_option.default_h2 is False
    assert updated_option.layout == "centered"


def test_deco_with_spaces():
    line = "@(  layout = split,   background = blue  )"
    deco, option = parse_deco(line)
    assert deco == {"layout": "split", "background": "blue"}


if __name__ == "__main__":
    pytest.main()
