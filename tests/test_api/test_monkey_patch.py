# zettelkasten/../tests/test_api/test_monkey_patch.py
import pytest

import zettelkasten.defaults
import zettelkasten.monkeypatch
import zettelkasten.parse as parse
import zettelkasten.setup


def test_name_sep_patching():
    """Test successfull namesep changes."""

    assert parse.zettel_name("woodturning/tools/chisel") == (
        "woodturning",
        "tools",
        "chisel",
    )

    org_sep = zettelkasten.defaults.name_sep
    zettelkasten.defaults.name_sep = "_"

    assert parse.zettel_name("woodturning/tools/chisel") == (
        None,
        None,
        "woodturning/tools/chisel",
    )

    assert parse.zettel_name("woodturning_tools_chisel") == (
        "woodturning",
        "tools",
        "chisel",
    )

    zettelkasten.defaults.name_sep = org_sep


def test_config_file_patching():
    """Test successfull monkey patching using the :ref:`config-file`."""

    import importlib

    importlib.reload(zettelkasten.defaults)

    # make sure zettelkasten.defaults is in it's hardcoded state:
    assert zettelkasten.defaults.state == "hardcoded"

    # Make sure a config folder exists:
    zettelkasten.setup.create_config_folder(
        dummy_location="tests/pytest_dir/.zettelkasten.d"
    )

    # Make sure a config file exists:
    zettelkasten.setup.create_config_file(
        dummy_location="tests/pytest_dir/.zettelkasten.d/zk.cfg"
    )

    # monkey patch
    zettelkasten.monkeypatch.patch_defaults(
        "tests/pytest_dir/.zettelkasten.d/zk.cfg"
    )

    # temp store the monkey patched title
    monkey_patched_title = zettelkasten.defaults.def_title

    # temp store the monkey patched state
    monkey_patched_state = zettelkasten.defaults.state

    none_value_example = zettelkasten.defaults.def_location_specifier
    none_dict_example = zettelkasten.defaults.zettel_meta_attribute_defaults[
        "category"
    ]

    # revert all patching before asserting to not fail any following tests

    importlib.reload(zettelkasten.defaults)

    # make sure monkey patching set it's state accordingly
    assert monkey_patched_state == "config_file_monkeypatched"

    # manually check if the desired monkey patch applies
    assert monkey_patched_title == "Config Parsed Test Title"

    # check if 'None' parsing was succesfull:
    assert none_value_example is None
    assert none_dict_example is None

    # make sure reverting was succesfull
    assert zettelkasten.defaults.def_title == "Test Title"
