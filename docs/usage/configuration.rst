.. _configuration:

Configuration
=============

Following sections provide details on how to configure zettelkasten behavour to
your needs.


.. contents::
   :local:
   :backlinks: top

.. _cfile:

Configuration File
------------------

During :ref:`installation_setup` a default `configuration file
<https://docs.python.org/3/library/configparser.html>`_ is placed inside

   .. code:: shell

      ~/.zettelkasten.d/test_config.cfg

Each of the keys has a hardcoded counterpart inside
:mod:`zettelkasten.defaults`. For each command that is executed (excl.
:ref:`setup <installation_setup>`) all of the attributes present in
:attr:`zettelkasten.defaults`.

Among the :ref:`most tweaked <most_tweaked>` attributes are the:

    - :attr:`Zettel name seperator <zettelkasten.defaults.name_sep>`
    - :attr:`Zettelkasten location <zettelkasten.defaults.location>`

This default config file can be seen below:

    .. literalinclude:: ../../tests/testkasten/pytest_dir/.zettelkasten.d/zk.cfg
       :language: cfg
