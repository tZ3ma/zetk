.. _zettelkasten:

Zettelkasten
============

All of the default zettelkasten structure can be tweaked changing
:ref:`defaults_structure` using the :ref:`cfile`.

The realized structure of :mod:`zettelkasten's <zettelkasten>` zettelkasten is
as follows:


.. contents::
   :local:
   :backlinks: top

.. _lobby:

lobby
-----
The lobby serves as main folder for all zettels that are ``uncategorized``.
Meaning a :ref:`zettel <zettels_design>` was added without specifying a
category or subcategory as in:


   .. code:: shell

      zk add zettelname

This allows for rapid and convenient note taking in zettelkasten style as a
quick:

   .. code:: shell

      zk open zettelname

opens the newly generated zettel as :ref:`org-file <zettels_design_org>`.

After adding a few zettels you usually realize that a lot of zettels are about
the same topic and or group of topics. This where
:mod:`zettelkasten's <zettelkasten>` structure of using a category and
subcategory enable you to conveniently sorting and organizing your zettels
by changing the :ref:`Zettel Attributes <zettel_attributes>` at the top of the
respective :ref:`org-file <zettels_design_org>`, or by adding an already sorted
zettel as in:

   .. code:: shell

      zk add category/subcategory/zettelname


.. _sources:

_sources
--------
The ``_sources`` folder is created during :ref:`installation_setup`. Whether it
is created and what it is called can be tweaked changing the
:ref:`defaults_structure` using the :ref:`cfile`.

It serves as top level folder for all reference files as well as the zettelkasten's
global bibliography file.

audios
^^^^^^
The ``audios`` folder is created during :ref:`installation_setup`. Whether it
is created and what it is called can be tweaked changing the
:ref:`defaults_structure` using the :ref:`cfile`.

It serves as top level folder for all reference files
:attr:`recognized <zettelkasten.defaults.infer_file_type>` as audios.

images
^^^^^^
The ``images`` folder is created during :ref:`installation_setup`. Whether it
is created and what it is called can be tweaked changing the
:ref:`defaults_structure` using the :ref:`cfile`.

It serves as top level folder for all reference files
:attr:`recognized <zettelkasten.defaults.infer_file_type>` as images.

pdfs
^^^^
The ``pdfs`` folder is created during :ref:`installation_setup`. Whether it
is created and what it is called can be tweaked changing the
:ref:`defaults_structure` using the :ref:`cfile`.

It serves as top level folder for all reference files
:attr:`recognized <zettelkasten.defaults.infer_file_type>` as PDF.

videos
^^^^^^

The ``videos`` folder is created during :ref:`installation_setup`. Whether it
is created and what it is called can be tweaked changing the
:ref:`defaults_structure` using the :ref:`cfile`.

It serves as top level folder for all reference files
:attr:`recognized <zettelkasten.defaults.infer_file_type>` as videos.

zettelkasten.bib
^^^^^^^^^^^^^^^^
The ``zettelkasten.bib`` file is created during :ref:`installation_setup`.
Its name can be tweaked changing the
:ref:`defaults_structure` using the :ref:`cfile`.
