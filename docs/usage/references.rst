.. _references:

References
==========
:mod:`zettelkasten's <zettelkasten>` uses
`org-ref <https://github.com/jkitchin/org-ref>`_ as a system for references,
because it is simple, packaged inside `MELPA <https://melpa.org/#/>`_ and
has some very nice features like drag and drop PDF source adding and opening
the respective source files via clicking (or C+c C+o) on the reference link
and using option 4 in the respective context menu.

During :ref:`zettelkasten setup <installation_setup>` a global bibliography file
is created (by default inside ``_sources/zettelkasten.bib``) holding all
references ever added to any zettel inside the zettelkasten given, it was added
using the respective command (opposed to being added manually be creating
a bibtex entry by hand).

During :ref:`zettel creation <zettels_adding>`
(``zk add category/subcategory/zettelname``) a zettel specific bibliography
file is created holding all future references as well as a bunch of
test entries serving as templates.
