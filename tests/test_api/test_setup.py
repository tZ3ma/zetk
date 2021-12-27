# tests/test_api/test_setup.py
"""Module for testing zettelkasten setup."""
from pathlib import Path

import pytest

import zettelkasten.defaults as defaults
import zettelkasten.setup


@pytest.mark.dependency(name="dummy_folder")
def test_dummy_config_folder_creation(tmp_path):
    """Test creating a config folder at dummy location."""
    cf_folder = tmp_path / ".zettelkasten.d"

    zettelkasten.setup.create_config_folder(dummy_location=cf_folder)

    assert cf_folder.is_dir()


@pytest.mark.dependency(name="dummy_file", depends=["dummy_folder"])
def test_dummy_config_file_creation(tmp_path):
    """Test creating a config file at dummy location."""
    cf_folder = tmp_path / ".zettelkasten.d"

    zettelkasten.setup.create_config_folder(dummy_location=cf_folder)

    cf_file = cf_folder / "zk.cfg"

    zettelkasten.setup.create_config_file(dummy_location=cf_file)

    assert cf_file.is_file()


@pytest.mark.dependency(name="dummy_styles", depends=["dummy_folder"])
def test_dummy_styles_file_creation(tmp_path):
    """Test creating a stlyes file at dummy location."""
    cf_folder = tmp_path / ".zettelkasten.d"

    zettelkasten.setup.create_config_folder(dummy_location=cf_folder)

    st_file = cf_folder / "styles.cfg"

    zettelkasten.setup.create_config_file(dummy_location=st_file)

    assert st_file.is_file()


@pytest.mark.dependency(name="home_folder", depends=["dummy_folder"])
def test_home_config_folder_creation():
    """Test creating a config folder at default location."""
    zettelkasten.setup.create_config_folder()
    assert Path(defaults.config_folder).is_dir()


@pytest.mark.dependency(name="home_file", depends=["home_folder"])
def test_home_config_file_creation():
    """Test creating a config file at default location."""
    zettelkasten.setup.create_config_file()
    assert Path(defaults.config_file).is_file()


@pytest.mark.dependency(name="home_styles", depends=["home_folder"])
def test_home_styles_file_creation():
    """Test creating a styles file at default location."""
    zettelkasten.setup.create_styles_file()
    assert Path(defaults.styles_file).is_file()


@pytest.mark.dependency(name="mpatch_folder")
def test_monkeypatched_config_folder_creation():
    """Test creating a config folder at default location."""
    original_folder = defaults.config_folder
    defaults.config_folder = Path("tests/testkasten/pytest_dir/.zettelkasten.d")

    zettelkasten.setup.create_config_folder()

    f = defaults.config_folder
    defaults.config_folder = original_folder

    assert Path(f).is_dir()


@pytest.mark.dependency(name="mpatch_file", depends=["mpatch_folder"])
def test_monkeypatched_config_file_creation():
    """Test creating a config file at default location."""
    original_file = defaults.config_file
    defaults.config_file = Path(
        "tests/testkasten/pytest_dir/.zettelkasten.d/zk.cfg"
    )

    # zettelkasten.setup.create_config_folder()
    zettelkasten.setup.create_config_file()

    f = defaults.config_file
    defaults.config_file = original_file

    assert Path(f).is_file()


@pytest.mark.dependency(name="mpatch_styles", depends=["mpatch_folder"])
def test_monkeypatched_styles_file_creation():
    """Test creating a styles file at default location."""
    original_file = defaults.styles_file
    defaults.styles_file = Path(
        "tests/testkasten/pytest_dir/.zettelkasten.d/styles.cfg"
    )

    # zettelkasten.setup.create_config_folder()
    zettelkasten.setup.create_styles_file()

    f = defaults.styles_file
    defaults.styles_file = original_file

    assert Path(f).is_file()
