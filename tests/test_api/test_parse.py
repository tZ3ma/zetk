import importlib
import os
from pathlib import Path

import pytest
from zettelkasten import add, defaults, initialize, parse


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("woodturning/tools/chisel", ("woodturning", "tools", "chisel")),
        ("my_zettel", (None, None, "my_zettel")),
        ("wrong_syntax/°_^%$!§", (None, None, "°_^%$!§")),
        ("too/many/seperators/zettel/test", (None, None, "test")),
        ("/seperators/galore/example/", ("seperators", "galore", "example")),
    ],
)
def test_zettel_name_parsing(name, expected):
    """Test correct zettel syntax parsing."""
    assert parse.zettel_name(name) == expected


def test_zettel_attribute_parsing():
    """Test correct attribute parsing"""

    parsed_attributes = parse.zettel_attributes(
        parsed_zettel_name=parse.ZettelName("woodturning", "tools", "chisel"),
        tags=["#Rework", "#NiceTry"],
        topics=["#Test"],
        not_showing="NotShowing",
    )

    expected_dict = {
        "#+Title:": "chisel",
        "#+Category:": "woodturning",
        "#+Subcategory:": "tools",
        "#+Author:": "Mathias Ammon",
        "#+DOC:": None,
        "#+DOLE:": None,
        "#+Topics:": ["#Test"],
        "#+Tags:": ["#Rework", "#NiceTry"],
    }

    assert parsed_attributes == expected_dict


@pytest.mark.parametrize(
    ("zettel", "path"),
    [
        (
            "woodturning/tools/chisel",
            os.path.join("woodturning", "tools", "chisel", "chisel.org"),
        ),
        ("my_zettel", os.path.join("lobby", "my_zettel", "my_zettel.org")),
        (
            "wrong_syntax/°_^%$!§",
            os.path.join("lobby", "°_^%$!§", "°_^%$!§.org"),
        ),
    ],
)
def test_zettel_path_parsing(zettel, path):
    """Test correct zettel path parsing"""

    # create a mock zettelkasten
    defaults.location = os.path.join(
        "tests",
        "pytest_dir",
        "pytest_kasten",
    )
    initialize.structure_zettelkasten()

    add.new_zettel(zettel, force_overwrite=True)

    concat_path = Path(os.path.join(Path(defaults.location), Path(path)))
    print(concat_path)

    # assert concat_path.is_file()
    assert parse.zettel_path(zettel) == concat_path

    importlib.reload(defaults)
