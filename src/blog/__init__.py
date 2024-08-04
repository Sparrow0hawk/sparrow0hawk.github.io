import sys

from blog.cli import execute


def main() -> None:
    execute(sys.argv[1:])
