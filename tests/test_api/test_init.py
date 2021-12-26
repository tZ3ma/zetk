# zettelkasten/../tests/test_api/test_monkey_patch.py
import pytest
from zettelkasten import add, defaults, initialize


@pytest.mark.dependency(name="zk_dir")
def test_zettelkasten_creation(tmp_path):
    """Test succesfull zettelkasten creation."""

    # create dummy zettelkasten location
    dummy_location = tmp_path / "zettelkasten"

    # assert that the directory is not already existing
    assert not (tmp_path / "zettelkasten").is_dir()

    # create the zettelkasten
    initialize.structure_zettelkasten(dummy_location=dummy_location)

    # assert that the main directory is now present
    assert (tmp_path / "zettelkasten").is_dir()


def test_zettelkasten_subdir_creation(tmp_path):
    """Test succesfull zettelkasten subdir creation."""

    # create dummy zettelkasten location
    dummy_location = tmp_path / "zettelkasten"

    # assert that none of the subdirs exist
    for directory in defaults.initial_folder_structure:
        assert not (dummy_location / directory).is_dir()

    # create the zettelkasten
    initialize.structure_zettelkasten(dummy_location=dummy_location)

    # assert that the subdirs are now present
    for directory in defaults.initial_folder_structure:
        assert (dummy_location / directory).is_dir()


def test_non_overwrite_creation(tmp_path):
    """Test reinitiating a zettelkasten not overwriting any existing stuff."""

    # create dummy zettelkasten location
    dummy_location = tmp_path / "zettelkasten"

    # create the zettelkasten
    initialize.structure_zettelkasten(dummy_location=dummy_location)

    # add a new zettel
    add.new_zettel(
        name="woodturning/tools/chisel",
        dummy_location=dummy_location,
    )

    # assert that the zettel exists:
    assert (
        dummy_location / "woodturning" / "tools" / "chisel" / "chisel.org"
    ).is_file()

    # recreate the zettelkasten
    initialize.structure_zettelkasten(dummy_location=dummy_location)

    # assert that the original zettel still exists
    assert (
        dummy_location / "woodturning" / "tools" / "chisel" / "chisel.org"
    ).is_file()


def test_rebuilding_initial_structure(tmp_path):
    """Test rebuilding the initial folder structure on reinitializing the
    zettelkasten."""

    # create dummy zettelkasten location
    dummy_location = tmp_path / "zettelkasten"

    # create the zettelkasten
    initialize.structure_zettelkasten(dummy_location=dummy_location)

    # remove the lobby folder
    (dummy_location / "lobby").rmdir()

    # assert that its gone
    assert not (dummy_location / "lobby").is_dir()

    # remove the _sources/audios folder
    (dummy_location / "_sources" / "audios").rmdir()

    # assert that its gone
    assert not (dummy_location / "_sources" / "audios").is_dir()

    # reinitiate the zettelkasten
    initialize.structure_zettelkasten(dummy_location=dummy_location)

    # asssert that the missing directories are back
    assert (dummy_location / "lobby").is_dir()
    assert (dummy_location / "_sources" / "audios").is_dir()
