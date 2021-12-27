"""Module for testing zettel compilation."""
import os

import zettelkasten

# import pytest


def test_categories_compilation():
    """Test correct category compilation.

    Includes folders directly below the zettelkasten folder.
    """
    test_zettels = [
        "woodturning/tools/chisel",
        "my_zettel",
        "wrong_syntax/°_^%$!§",
        "too/many/seperators/zettel/test",
        "/seperators/galore/example/",
    ]

    expected_categories = [
        "lobby",
        "woodturning",
        "seperators",
    ]

    # create a mock zettelkasten
    zettelkasten.defaults.location = os.path.join(
        "tests",
        "pytest_dir",
        "pytest_kasten",
    )
    zettelkasten.initialize.structure_zettelkasten()

    for zettel in test_zettels:
        zettelkasten.add.new_zettel(zettel, force_overwrite=True)

    assert sorted(expected_categories) == zettelkasten.compile.categories()


def test_all_subcategories_compilation():
    """Test correct subcategory compilation.

    Includes folders directly below the category folders.
    """
    test_zettels = [
        "woodturning/tools/chisel",
        "my_zettel",
        "wrong_syntax/°_^%$!§",
        "too/many/seperators/zettel/test",
        "/seperators/galore/example/",
    ]

    expected_categories = [
        "galore",
        "tools",
    ]

    # create a mock zettelkasten
    zettelkasten.defaults.location = os.path.join(
        "tests",
        "pytest_dir",
        "pytest_kasten",
    )
    zettelkasten.initialize.structure_zettelkasten()

    for zettel in test_zettels:
        zettelkasten.add.new_zettel(zettel, force_overwrite=True)

    assert (
        sorted(expected_categories) == zettelkasten.compile.all_subcategories()
    )


def test_subcategory_mapping_compilation():
    """Test correct subcategory mapping compilation.

    Includes folders directly below the category folders.
    """
    test_zettels = [
        "woodturning/tools/chisel",
        "my_zettel",
        "wrong_syntax/°_^%$!§",
        "too/many/seperators/zettel/test",
        "/seperators/galore/example/",
    ]

    expected_mapping = {
        "seperators": ["galore"],
        "woodturning": ["tools"],
    }

    # create a mock zettelkasten
    zettelkasten.defaults.location = os.path.join(
        "tests",
        "pytest_dir",
        "pytest_kasten",
    )
    zettelkasten.initialize.structure_zettelkasten()

    for zettel in test_zettels:
        zettelkasten.add.new_zettel(zettel, force_overwrite=True)

    assert expected_mapping == zettelkasten.compile.subcategory_mapping()


def test_zettel_mapping_compilation():
    """Test correct zettel mapping compilation.

    Includes folders directly below the subcategory folders.
    """
    test_zettels = [
        "woodturning/tools/skew",
        "woodturning/tools/gouge",
        "woodturning/tools/chisel",
        "my_zettel",
        "wrong_syntax/°_^%$!§",
        "also_wrong_syntax/°_^%$!§",
        "too/many/seperators/zettel/test",
        "too/many/seperators/zettel/test2",
        "/seperators/galore/example/",
        "/seperators/galore/example2/",
    ]

    expected_mapping = {
        "lobby": ["my_zettel", "test", "test2", "°_^%$!§"],
        "seperators": {"galore": ["example", "example2"]},
        "woodturning": {"tools": ["chisel", "gouge", "skew"]},
    }

    # create a mock zettelkasten
    zettelkasten.defaults.location = os.path.join(
        "tests",
        "pytest_dir",
        "pytest_kasten",
    )
    zettelkasten.initialize.structure_zettelkasten()

    for zettel in test_zettels:
        zettelkasten.add.new_zettel(zettel, force_overwrite=True)

    assert expected_mapping == zettelkasten.compile.zettel_mapping()
