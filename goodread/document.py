import os
import yaml
import marko
from .renderer import GoodreadRenderer


class Document:
    def __init__(self, path):
        self.__path = path

    # Process

    def process(self):
        markdown = marko.Markdown(renderer=GoodreadRenderer)

        # Source document
        with open(self.__path) as file:
            source = file.read()
            target = source

        # Convert document
        to_remove = []
        if target.startswith("---"):
            frontmatter, target = target.split("---", maxsplit=2)[1:]
            metadata = yaml.safe_load(frontmatter)
            if "goodread" in metadata:
                if "clean" in metadata["goodread"]:
                    for path in metadata["goodread"]["clean"]:
                        if os.path.exists(path):
                            raise RuntimeError(f"Clean path already exists: {path}")
                        if os.path.relpath(path, ".") != path:
                            raise RuntimeError(f"Clean path is unsafe: {path}")
                        to_remove.append(path)
        target = markdown.convert(target)
        target = frontmatter.join(["---"] * 2) + "\n" + target

        # Clean document
        for to_remove_path in to_remove:
            os.remove(to_remove_path)

        return source, target
