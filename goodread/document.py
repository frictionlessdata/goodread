import os
import yaml
import marko
from .renderer import GoodreadRenderer
from . import helpers


class Document:
    def __init__(self, path):
        self.__path = path

    @property
    def path(self):
        return self.__path

    def process(self, *, write=False):

        # Convert document
        with open(self.path) as file:
            markdown = marko.Markdown(renderer=GoodreadRenderer)
            text = file.read()
            to_remove = []
            if text.startswith("---"):
                frontmatter, text = text.split("---", maxsplit=2)[1:]
                metadata = yaml.safe_load(frontmatter)
                if "goodread" in metadata:
                    if "clean" in metadata["goodread"]:
                        for path in metadata["goodread"]["clean"]:
                            if os.path.exists(path):
                                raise RuntimeError(f"Clean path already exists: {path}")
                            if os.path.relpath(path, ".") != path:
                                raise RuntimeError(f"Clean path is unsafe: {path}")
                            to_remove.append(path)
            text = markdown.convert(text)
        text = frontmatter.join(["---"] * 2) + "\n" + text

        # Clean document
        for to_remove_path in to_remove:
            os.remove(to_remove_path)

        # Write document
        if write:
            helpers.write_file(self.path, text)

        return text
