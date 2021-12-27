# zettelkasten/__main__.py
"""Module providing the main entry point for the zettelkasten cli."""


def main():
    """Function providing the main entry point for the zettelkasten cli."""
    msg = "".join(
        [
            "Folder based zettelkasten with a bibtex reference system and",
            "emacs org-mode file zettels",
        ]
    )
    print(msg)


if __name__ == "__main__":
    main()
