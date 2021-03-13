import yaml
import marko
import subprocess
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

        # Parse document
        prepare = []
        cleanup = []
        if target.startswith("---"):
            frontmatter, target = target.split("---", maxsplit=2)[1:]
            metadata = yaml.safe_load(frontmatter)
            if "goodread" in metadata:
                prepare.extend(metadata["goodread"].get("prepare", []))
                cleanup.extend(metadata["goodread"].get("cleanup", []))

        # Prepare document
        for code in prepare:
            subprocess.run(code, shell=True)

        # Convert document
        target = markdown.convert(target)
        target = frontmatter.join(["---"] * 2) + "\n" + target

        # Cleanup document
        for code in cleanup:
            subprocess.run(code, shell=True)

        return source, target
