"""Module for testing zettel and source addition."""
import os
from pathlib import Path

import pytest

import zettelkasten.defaults
from zettelkasten import add
from zettelkasten import initialize
from zettelkasten import parse

# from zettelkasten.defaults import location


@pytest.mark.parametrize(
    ("parsed_zettel_name", "expected_path_addendum"),
    [
        (
            ("woodturning", "tools", "chisel"),
            os.path.join("woodturning", "tools", "chisel"),
        ),
        ((None, None, "my_zettel"), os.path.join("lobby", "my_zettel")),
        ((None, None, "°_^%$!§"), os.path.join("lobby", "°_^%$!§")),
    ],
)
def test_zettel_location_creation(
    tmp_path, parsed_zettel_name, expected_path_addendum
):
    """Test correct zettel path creation."""
    complete_path = add.create_zettel_location(
        parsed_zettel_name=parse.ZettelName(*parsed_zettel_name),
        dummy_location=tmp_path / "zettelkasten",
    )

    expected_path = tmp_path / "zettelkasten" / expected_path_addendum

    assert complete_path == expected_path


@pytest.mark.dependency(name="addition")
# @pytest.fixture(scope="session")
def test_zettel_addition(tmp_path):
    """Test succesfull zettel addition."""
    # reassure dummy location zettel initiaion:
    initialize.structure_zettelkasten(tmp_path / "zettelkasten")

    add.new_zettel(
        name="woodturning/tools/chisel",
        dummy_location=tmp_path / "zettelkasten",
    )
    org_file = (
        tmp_path
        / "zettelkasten"
        / "woodturning"
        / "tools"
        / "chisel"
        / "chisel.org"
    )
    assert org_file.is_file()


@pytest.mark.dependency(name="unintended_addition", depends=["addition"])
def test_unintended_zettel_addition(tmp_path):
    """Test unintentionally requesting to overwrite an existing zettel."""
    # reassure dummy location zettel initiaion:
    initialize.structure_zettelkasten(tmp_path / "zettelkasten")

    add.new_zettel(
        name="woodturning/tools/chisel",
        dummy_location=tmp_path / "zettelkasten",
        force_overwrite=True,  # true to overwrite the existing bib entries
    )
    with pytest.raises(FileExistsError):
        add.new_zettel(
            name="woodturning/tools/chisel",
            dummy_location=tmp_path / "zettelkasten",
        )


zettel_attributes_dict = {
    "#+Title:": "chisel",
    "#+Category:": "woodturning",
    "#+Subcategory:": "tools",
    "#+Author:": "Mathias Ammon",
    "#+DOC:": None,
    "#+DOLE:": None,
    "#+Topics:": ["#Test"],
    "#+Tags:": ["#Rework", "#NiceTry"],
}
zettel_attributes_list = [
    "#+Title: chisel \n",
    "#+Category: woodturning \n",
    "#+Subcategory: tools \n",
    "#+Author: Mathias Ammon \n",
    "#+DOC: None \n",
    "#+DOLE: None \n",
    "#+Topics: ['#Test'] \n",
    "#+Tags: ['#Rework', '#NiceTry'] \n",
]


def test_zettel_attribute_writing(tmp_path):
    """Test succesfull attribute writing during zettel creation."""
    zettel_folder = tmp_path / "lobby" / "attributes"

    zettel_folder.mkdir(parents=True, exist_ok=True)

    org_file = zettel_folder / "attrbiutes.org"

    add.write_org_zettel_attributes(
        org_file_path=org_file,
        zettel_attributes=zettel_attributes_dict,
    )

    with open(org_file) as f:
        lines = f.readlines()
        assert lines == zettel_attributes_list


@pytest.mark.dependency(name="bib_creation")
def test_bibtex_file_creation(tmp_path):
    """Test succesfull bibliography file creation."""
    zettel_folder = tmp_path / "lobby" / "bibliography"

    zettel_folder.mkdir(parents=True, exist_ok=True)

    bib_file = zettel_folder / "bibliography.bib"

    add.create_bibliography_file(bibliography_file_path=bib_file)

    assert bib_file.is_file()


@pytest.mark.dependency(name="bib_creation", depends=["bib_creation"])
def test_repeated_bibtex_file_creation(tmp_path):
    """Test creating the same bibfile over and over."""
    zettel_folder = tmp_path / "lobby" / "bibliography"

    zettel_folder.mkdir(parents=True, exist_ok=True)

    bib_file = zettel_folder / "bibliography.bib"

    # initial creation
    add.create_bibliography_file(bibliography_file_path=bib_file)
    assert bib_file.is_file()

    # repeated creation without forced overwrite
    with pytest.raises(FileExistsError):
        add.create_bibliography_file(bibliography_file_path=bib_file)

    # repeated creation with forced overwrite
    add.create_bibliography_file(
        bibliography_file_path=bib_file,
        force_overwrite=True,
    )
    assert bib_file.is_file()


def test_org_zettel_bibtex_writing(tmp_path):
    """Test succesfull bibtex writing during zettel org file creation."""
    # dummy zettel folder...
    zettel_folder = tmp_path / "lobby" / "bibtex"

    # ...created
    zettel_folder.mkdir(parents=True, exist_ok=True)

    # dummy zettel org file creation
    org_file = zettel_folder / "bibtex.org"

    # testing the utility
    add.write_org_zettel_bibliography(
        org_file_path=org_file, bibliography_file="bibtex.bib"
    )

    expexted_lines = [
        "\n",
        "* Bibliography\n",
        "\n",
        "bibliography:bibtex.bib",
    ]

    with open(org_file) as f:
        lines = f.readlines()
        assert lines == expexted_lines


@pytest.mark.dependency(name="dummy_souce_addition", depends=["addition"])
def test_dummy_source_addition(tmp_path):
    """Test sucessfull source addition using a dummy location."""
    # reassure dummy location zettel initiaion:
    initialize.structure_zettelkasten(tmp_path / "zettelkasten")

    # new zettel not present inside the dependend tmp_path loc
    add.new_zettel(
        name="woodturning/tools/skew",
        dummy_location=tmp_path / "zettelkasten",
    )

    add.new_source(
        zettel_name="woodturning/tools/skew",
        source_file="tests/bib_sources/test_video.mp4",
        uid="video2_2021_min42",
        locspec="min 42",
        dummy_location=tmp_path / "zettelkasten",
    )

    zettel_bib_location = (
        tmp_path
        / "zettelkasten"
        / "woodturning"
        / "tools"
        / "skew"
        / "skew.bib"
    )

    with open(zettel_bib_location) as f:
        assert "video2_2021_min42" in f.read()

    kasten_bib_location = (
        tmp_path / "zettelkasten" / "_sources" / "zettelkasten.bib"
    )

    with open(kasten_bib_location) as f:
        assert "video2_2021_min42" in f.read()


@pytest.mark.dependency(name="souce_addition", depends=["addition"])
def test_source_addition():
    """Test sucessfull source addition using zk's defaults."""
    import importlib

    importlib.reload(zettelkasten.defaults)

    # reassure dummy location zettel initiaion:
    location = zettelkasten.defaults.location
    initialize.structure_zettelkasten(location)

    # force addition, since the test path stays the same for each test run
    add.new_zettel(
        name="woodturning/tools/skew",
        force_overwrite=True,
    )

    add.new_source(
        zettel_name="woodturning/tools/skew",
        source_file="tests/bib_sources/test_audio.mp3",
        uid="audio2_1990_sec13",
        locspec="sec 13",
        author="Test Routine",
        title="Test Audio 2",
        date="1990-07-13",
        year="1990",
        force_overwrite=True,
    )

    zettel_bib_location = (
        Path(location) / "woodturning" / "tools" / "skew" / "skew.bib"
    )

    with open(zettel_bib_location) as fle:
        content = fle.read()
        print(content)
        print(zettel_bib_location)
        print(location)
        assert "audio2_1990_sec13" in content

    kasten_bib_location = Path(location) / "_sources" / "zettelkasten.bib"

    with open(kasten_bib_location) as f:
        content = f.read()
        assert "audio2_1990_sec13" in content
