# zettelkasten/compile.py
"""
Module to aggregate all of the zettelkasten meta analysis tools.
"""
import os
from collections import defaultdict

from . import defaults


def categories():
    """
    Compiles a sorted list of categories including the :ref:`lobby`

    Uses :attr:`zettelkasten.defaults.location` as top level folder for
    compiling.

    Return
    ------
    compiled_categories: list
        Alphabetically sorted list of compiled categories.

    Examples
    --------
    0. Creating the zettels of the examples below:

        >>> # creating the zettel first
        >>> from zettelkasten import add, defaults, initialize
        >>> defaults.location = "tests/doctest_dir/doctest_kasten"
        >>> initialize.structure_zettelkasten()

        >>> # creating a sorted zettel
        >>> add.new_zettel("woodturning/tools/chisel", force_overwrite=True)

        >>> # creating another sorted zettel
        >>> add.new_zettel("carpentry/tools/chisel", force_overwrite=True)

        >>> # creating an usorted zettel
        >>> add.new_zettel("my_zettel", force_overwrite=True)

    1. Compile the list of categories:

        >>> cats = categories()
        >>> print(cats)
        ['carpentry', 'lobby', 'woodturning']
    """

    path = defaults.location
    folders = [f.name for f in os.scandir(path) if f.is_dir()]
    compiled_categories = [
        f for f in folders if f not in defaults.reserved_folder_names
    ]

    return list(sorted(compiled_categories))


def all_subcategories():
    """
    Compiles a sorted list of all subcategories inside the zettelkasten.

    Uses :attr:`zettelkasten.defaults.location` as top level folder for
    compiling.

    Return
    ------
    compiled_categories: list
        Alphabetically sorted list of compiled subcategories.

    Examples
    --------
    0. Creating the zettels of the examples below:

        >>> # creating the zettel first
        >>> from zettelkasten import add, defaults, initialize
        >>> defaults.location = "tests/doctest_dir/doctest_kasten"
        >>> initialize.structure_zettelkasten()

        >>> # creating a sorted zettel
        >>> add.new_zettel("woodturning/tools/chisel", force_overwrite=True)

        >>> # creating another sorted zettel
        >>> add.new_zettel("carpentry/tools/chisel", force_overwrite=True)

        >>> # creating an usorted zettel
        >>> add.new_zettel("my_zettel", force_overwrite=True)

    1. Compile the list of categories:

        >>> all_subcategories()
        ['tools']
    """
    path = defaults.location
    all_subcats = list()
    for category in categories():
        if category != "lobby":
            subcats = [
                f.name
                for f in os.scandir(os.path.join(path, category))
                if f.is_dir()
            ]
            for subcat in subcats:
                if subcat not in all_subcats:
                    all_subcats.append(subcat)
    return list(sorted(all_subcats))


def subcategory_mapping():
    """
    Compiles a dict of sorted lists representing the subategories mapped to
    their category.

    Uses :attr:`zettelkasten.defaults.location` as top level folder for
    compiling.

    Return
    ------
    compiled_categories: dict
        Alphabetically sorted dict of compiled subcategories mapped to
        categoires.

    Examples
    --------
    0. Creating the zettels of the examples below:

        >>> # creating the zettel first
        >>> from zettelkasten import add, defaults, initialize
        >>> defaults.location = "tests/doctest_dir/doctest_kasten"
        >>> initialize.structure_zettelkasten()

        >>> # creating a sorted zettel
        >>> add.new_zettel("woodturning/tools/chisel", force_overwrite=True)

        >>> # creating another sorted zettel
        >>> add.new_zettel("carpentry/tools/chisel", force_overwrite=True)

        >>> # creating an usorted zettel
        >>> add.new_zettel("my_zettel", force_overwrite=True)

    1. Compile the mapping of subcategories:

        >>> for key, value in subcategory_mapping().items():
        ...    print(f"{key}: {value}")
        carpentry: ['tools']
        woodturning: ['tools']


    """
    path = defaults.location
    cats = dict()
    for category in categories():
        if category != "lobby":
            subcats = [
                f.name
                for f in os.scandir(os.path.join(path, category))
                if f.is_dir()
            ]
            cats[category] = list(sorted(subcats))

    sorted_cats = dict()
    for k in list(sorted(cats.keys())):
        sorted_cats[k] = cats[k]

    return sorted_cats


def zettel_mapping():
    """
    Compiles a dict of of dicts of sorted lists representing the zettels mapped
    to their subategories mapped to their category.

    Uses :attr:`zettelkasten.defaults.location` as top level folder for
    compiling.

    Return
    ------
    compiled_zettels: dict
        Alphabetically sorted dict of dict of compiled zettels mapped to
        subcategoires.

    Examples
    --------
    0. Creating the zettels of the examples below:

        >>> # creating the zettel first
        >>> from zettelkasten import add, defaults, initialize
        >>> defaults.location = "tests/doctest_dir/doctest_kasten"
        >>> initialize.structure_zettelkasten()

        >>> # creating woodturning/tools zettels
        >>> add.new_zettel("woodturning/tools/chisel", force_overwrite=True)
        >>> add.new_zettel("woodturning/tools/skew", force_overwrite=True)

        >>> # creating another sorted zettel
        >>> add.new_zettel("carpentry/tools/plane", force_overwrite=True)
        >>> add.new_zettel("carpentry/tools/chisel", force_overwrite=True)


        >>> # creating an usorted zettel
        >>> add.new_zettel("my_zettel", force_overwrite=True)

    1. Compile the zettel mapping:

        >>> import pprint
        >>> pprint.pprint(zettel_mapping())
        {'carpentry': {'tools': ['chisel', 'plane']},
         'lobby': ['my_zettel'],
         'woodturning': {'tools': ['chisel', 'skew']}}
    """
    path = defaults.location

    zettels = defaultdict(dict)  # type: ignore
    for category, subcategories in subcategory_mapping().items():
        for subcategory in subcategories:

            zettels[category][subcategory] = list(
                sorted(
                    f.name
                    for f in os.scandir(
                        os.path.join(path, category, subcategory)
                    )
                    if f.is_dir()
                )
            )

    lobby_zettels = list(
        sorted(
            f.name
            for f in os.scandir(os.path.join(path, "lobby"))
            if f.is_dir()
        )
    )

    zettels["lobby"] = lobby_zettels  # type: ignore

    return dict(zettels)


def parsed_zettels():
    """
    Compiles a dict of of dicts of sorted lists representing the zettels mapped
    to their subategories mapped to their category.

    Uses :attr:`zettelkasten.defaults.location` as top level folder for
    compiling.

    Return
    ------
    compiled_zettels: list
        Alphabetically sorted list of :attr:`parsed zettel names
        <zettelkasten.parse.zettel_name>`.


    Examples
    --------
    0. Creating the zettels of the examples below:

        >>> # creating the zettel first
        >>> from zettelkasten import add, defaults, initialize
        >>> defaults.location = "tests/doctest_dir/doctest_kasten"
        >>> initialize.structure_zettelkasten()

        >>> # creating woodturning/tools zettels
        >>> add.new_zettel("woodturning/tools/chisel", force_overwrite=True)
        >>> add.new_zettel("woodturning/tools/skew", force_overwrite=True)

        >>> # creating another sorted zettel
        >>> add.new_zettel("carpentry/tools/plane", force_overwrite=True)
        >>> add.new_zettel("carpentry/tools/chisel", force_overwrite=True)


        >>> # creating an usorted zettel
        >>> add.new_zettel("my_zettel", force_overwrite=True)

    1. Compile the parsed zettel list:

       >>> import pprint
       >>> pprint.pprint(parsed_zettels())
       ['carpentry/tools/chisel',
        'carpentry/tools/plane',
        'lobby/my_zettel',
        'woodturning/tools/chisel',
        'woodturning/tools/skew']

    """
    zettel_list = list()
    sep = defaults.name_sep
    for cat, subcats in zettel_mapping().items():
        if cat != "lobby":
            for subcat, zettels in subcats.items():
                for zettel in zettels:
                    zettel_list.append(f"{cat}{sep}{subcat}{sep}{zettel}")
        else:
            for zettel in subcats:
                zettel_list.append(f"lobby{sep}{zettel}")

    return list(sorted(zettel_list))
