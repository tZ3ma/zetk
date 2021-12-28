# zettelkasten/parse.py
"""Module aggregating all of the user input parsing capabilities."""
import logging
import typing
from pathlib import Path

from . import defaults

logger = logging.getLogger(__name__)


class ZettelName(typing.NamedTuple):
    """Zettel name consisting of ``category``, ``subcategory``, ``uid``.

    Parameters
    ----------
    category: str
        String representing the top level folder inside the zettelkasten.
       ``None`` if Zettel is inside the :ref:`Lobby`.

    subcategory: str
        String representing the top sublevel folder inside the zettelkasten.
        ``None`` if no subcategory is given.

    uid: str
        String representing the top sublevel folder inside the zettelkasten.
        ``None`` if no subcategory is given.

    Return
    ------
    zettel_name: ~typing.NamedTuple
        Namedtuple instance object serving as zettel name.

    Examples
    --------
    >>> ZettelName('folder', 'subfolder', 'zettel')
    ZettelName(category='folder', subcategory='subfolder', uid='zettel')
    """

    category: typing.Union[None, str]
    subcategory: typing.Union[None, str]
    uid: str


def zettel_name(name):
    r"""Zettel name parsing syntax.

    Parameters
    ----------
    name : str
        Zettel name. Either a singular uid as in "my_zettel" or a
        folder/subfolder/uid syntax as in "woodturning/tools/chisel".

        Used to automatically sort new zettels either into the
        category/subcategory stated or into the :ref:`Lobby` if only an uid is
        given.

        The seperator used for uidentifying the different parts is specified
        using the :ref:`cfile`. It defaults to ``\``.

        If no complete name is given, then category and subcategory are set to
        their defaults as stated in the :ref:`cfile`.


    Examples
    --------
    1. Using a complete name to automatically sort the zettel:

        >>> zettel_name("woodturning/tools/chisel")
        ZettelName(category='woodturning', subcategory='tools', uid='chisel')

    2. Using only an uid, puts the Zettel into the :ref:`Lobby`:

        >>> zettel_name("my_zettel")
        ZettelName(category=None, subcategory=None, uid='my_zettel')

    3. Using the wrong syntax fails somewhat gracefully:

        >>> zettel_name("wrong_syntax/°_^%$!§")
        ZettelName(category=None, subcategory=None, uid='°_^%$!§')

    4. Leading and trailing seperators will be stripped before parsing:

        >>> zettel_name("/seperators/galore/example/")
        ZettelName(category='seperators', subcategory='galore', uid='example')

    5. Leading and trailing separators will be stripped before parsing but
       using more than expected (after parsing) will also result in a somewhat
       graceful failure.

        >>> zettel_name("/excessive/seperators/galore/example/")
        ZettelName(category=None, subcategory=None, uid='example')

    Returns
    -------
    zettel_name: tuple
        Tuple consisting of ('category', 'subcategory', 'uid')
    """
    logger.debug("-------------------------------")
    logger.debug("Preparing to parse Zettel name")

    # is a complete name given?
    if defaults.name_sep in name:

        # yes, so parse it
        logger.debug(f"{defaults.name_sep} found in '{name}'")
        name = name.strip("/")
        parts = name.split(defaults.name_sep)

        # syntax is only valid using 2 seperators:
        if len(parts) == 3:
            category, subcategory, uid = parts
            logger.debug(f"Succesfully dissassembled '{name}' into:")
            logger.debug(
                f"category: '{category}', subcategory: "
                + f"'{subcategory}', uid: '{uid}'"
            )

        # used wrong syntax. State a warning and fail gracefully
        else:
            uid = parts[-1]
            category = defaults.zettel_meta_attribute_defaults.get(
                "category", None
            )
            subcategory = defaults.zettel_meta_attribute_defaults.get(
                "category", None
            )

            logger.warning(f"'{name}' could not be dissassembled correctly")
            logger.warning(f"Dissassembling yielded '{parts}'. Parsing into:")
            logger.warning(
                f"category: '{category}', subcategory: "
                + f"'{subcategory}', uid: '{uid}'"
            )

    # No, only a uid was passed:
    else:
        uid = name
        category = defaults.zettel_meta_attribute_defaults.get("category", None)
        subcategory = defaults.zettel_meta_attribute_defaults.get(
            "category", None
        )

        logger.debug("Zettel name parsed.")
        logger.debug("-------------------------------\n")

    return ZettelName(category, subcategory, uid)


def zettel_attributes(parsed_zettel_name, **kwargs):
    r"""Zettel attribute parsing utility.

    The attributes parsed are stated in the :ref:`cfile` along with a set
    of required attributes. These required attributes are made of the
    attributes of the :class:`ZettelName` and stem form this zettelkasten's
    dogma of having a ``zettelkasten/category/subcategory/zettel`` hierarchy.

    note
    ----
    Called by :meth:add_zettel during zettel creation.

    Parameters
    ----------
    parsed_zettel_name: ZettelName
        :class:`typing.NamedTuple` representing the zettel.

    kwargs:
        The attributes to be parsed. Attributes are/need to be stated in the
        :ref:`cfile` along with a set of required attributes.

        Attributes will be added to the Zettel-Org-File as::

            # +Attribute_Name1: Attribute_Value1
                        .
                        .
            # +Attribute_NameN: Attribute_ValueN

    Return
    ------
    parsed_attributes: dict
        Dictionairy of the parsed attributes. The attributes parsed are stated
        in the :ref:`cfile`.

    Examples
    --------
    Building on the examples stated in :meth:`parse_zettel_name`

    >>> import pprint #imported for better doctest output

        1. Using a complete name to automatically sort the zettel:

        >>> zn = zettel_name("woodturning/tools/chisel")
        >>> zattr = zettel_attributes(zn)
        >>> pprint.pprint(zattr)
        {'#+Author:': 'Mathias Ammon',
         '#+Category:': 'woodturning',
         '#+DOC:': None,
         '#+DOLE:': None,
         '#+Subcategory:': 'tools',
         '#+Tags:': [],
         '#+Title:': 'chisel',
         '#+Topics:': []}


    2. Using only a uid, but adding tags and topics:

        >>> zn = zettel_name("my_zettel")
        >>> zattr = zettel_attributes(
        ...     zn,
        ...     tags=['#Rework', '#Pressurloss', '#Solarthermal'],
        ...     topics=['#EnergyConcept', '#Thermodynamics'])
        >>> pprint.pprint(zattr)
        {'#+Author:': 'Mathias Ammon',
         '#+Category:': None,
         '#+DOC:': None,
         '#+DOLE:': None,
         '#+Subcategory:': None,
         '#+Tags:': ['#Rework', '#Pressurloss', '#Solarthermal'],
         '#+Title:': 'my_zettel',
         '#+Topics:': ['#EnergyConcept', '#Thermodynamics']}


    3. Using the wrong syntax and using non supported attributes (unsupported):

        >>> zn = zettel_name("wrong_syntax/°_^%$!§")
        >>> zattr = zettel_attributes(
        ...     zn,
        ...     unsupported='This does not show')
        >>> pprint.pprint(zattr)
        {'#+Author:': 'Mathias Ammon',
         '#+Category:': None,
         '#+DOC:': None,
         '#+DOLE:': None,
         '#+Subcategory:': None,
         '#+Tags:': [],
         '#+Title:': '°_^%$!§',
         '#+Topics:': []}

    """
    logger.debug("-------------------------------")
    logger.debug("Preparing to parse zettel attributes")

    # map zettel atrributes
    zettel_attributes = dict()

    # start with the required ones using the zettel name:
    for req_at in defaults.required_attributes:

        zettel_attributes[
            defaults.zettel_meta_attribute_labels[req_at]
        ] = getattr(parsed_zettel_name, req_at)

    # add to that the optional ones as stated in the cfile
    for attribute, label in defaults.zettel_meta_attribute_labels.items():

        if attribute not in defaults.required_attributes:
            zettel_attributes[label] = kwargs.get(
                attribute, defaults.zettel_meta_attribute_defaults[attribute]
            )

    return zettel_attributes


def zettel_path(name):
    r"""Infer the file system location of a given zettelname.

    Location is inferred relative to
    :attr:`defaults.location <zettelkasten.defaults.location>`.

    Does NOT check if location is a valid file.

    Parameters
    ----------
    name : str
        Zettel name. Either a singular uid as in "my_zettel" or a
        folder/subfolder/uid syntax as in "woodturning/tools/chisel".

        Used to automatically sort new zettels either into the
        category/subcategory stated or into the :ref:`Lobby` if only an uid is
        given.

        The seperator used for uidentifying the different parts is specified
        using the :ref:`cfile`. It defaults to ``\``.

        If no complete name is given, then category and subcategory are set to
        their defaults as stated in the :ref:`cfile`.

    Examples
    --------
    1. Getting the location of a sorted zettel:

        >>> zp = str(zettel_path("woodturning/tools/chisel"))
        >>> zp = 'woodturning' + zp.split('woodturning')[1]
        >>> print(zp)
        woodturning/tools/chisel/chisel.org

    2. Getting the location of an unsorted zettel (inside the lobby):

        >>> zp = str(zettel_path("my_zettel"))
        >>> zp = 'lobby' + zp.split('lobby')[1]
        >>> print(zp)
        lobby/my_zettel/my_zettel.org

    Raises
    ------
    TypeError:
        Raises a Type Error in case unexpected zettel parsing takes place.
        In that case :func:`zettel_name` is thr right place to start the
        investigation.

    Returns
    -------
    zettel_path: Path
        Path object representing the zettel org file location including
        the zettelkasten location.
    """
    parsed_zettel_name = zettel_name(name)

    if (
        parsed_zettel_name.category is None
        and parsed_zettel_name.subcategory is None
    ):
        zettel_path = (
            Path(defaults.location)
            / "lobby"
            / parsed_zettel_name.uid
            / f"{parsed_zettel_name.uid}.org"
        )
    elif all([part is not None for part in parsed_zettel_name]):
        zettel_path = (
            Path(defaults.location)
            / parsed_zettel_name.category
            / parsed_zettel_name.subcategory
            / parsed_zettel_name.uid
            / f"{parsed_zettel_name.uid}.org"
        )

    else:
        msg = "Something weired happend with the zettelname parsing"
        raise TypeError(msg)

    return zettel_path
