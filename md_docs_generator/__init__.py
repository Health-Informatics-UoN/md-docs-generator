from pathlib import Path
from scripts.list_files import list_files
from scripts.parser import parser
from scripts.populate_python import populate_python


def main():
    args = parser.parse_args()
    file_list = list_files(
        directory=args.input_directory, extensions=args.extensions.split(",")
    )

    for in_file in file_list:
        if args.trim_extension:
            if "." in in_file:
                filename = in_file[: in_file.rindex(".")]
        else:
            filename = in_file

        header = filename.replace("/", ".")
        file_contents = f"## {header}"

        if args.inserted_source:
            file_contents += f"\n[source]({args.inserted_source}/{in_file})"

        if args.python:
            if in_file[-3:] == ".py":
                file_contents += "\n"
                file_contents += populate_python(Path(args.input_directory, in_file))
        out_filename = Path(args.output_directory, filename + args.output_extension)
        out_filename.parent.mkdir(exist_ok=True, parents=True)
        with open(out_filename, "w") as f:
            f.write(file_contents)

    print(file_list)
