import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--input-directory",
    "-i",
    help="provide a directory to scan for files",
)
parser.add_argument(
    "--extensions",
    "-e",
    help="provide a string listing the extensions of files you want to get, separated by a comma",
)
parser.add_argument("--output-directory", "-o", help="provide a directory for output")
parser.add_argument(
    "--output-extension", "-ox", help="provide an extension for the output files"
)
parser.add_argument("--trim-extension", "-t", action=argparse.BooleanOptionalAction)
parser.add_argument(
    "--inserted-source",
    "-is",
    help="if you want to insert a link to the source, provide the root here",
)
parser.add_argument(
    "--python",
    action=argparse.BooleanOptionalAction,
    help="if true, populate .py files with function and class signatures",
)

parser.set_defaults(trim_extension=True, python=True)
