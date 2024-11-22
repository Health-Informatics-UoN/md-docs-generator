# md-docs-generator
 
Inspired by the autoapi plugin for Sphinx, md-docs-generator is a Python utility that builds documentation as markdown files.
It's a bit rough around the edges, and so far only renders documentation for Python scripts.

## Usage
### Prerequisites
- Python 3.12
- [Poetry](https://python-poetry.org/)

### Running md-docs-generator

md-docs-generator runs from the command line. A minimal example is:

```sh
poetry run md-docs-generator -i /path/to/source/code -o /path/to/docs -e ".py" -ox ".mdx"
```

This reads the source code directory (`-i`), walks the directory tree, looks for ".py" files (`-e`), then writes ".mdx" files matching the source code (`-ox`) to the docs directory (`-o`)

I wrote this in about a day, so expect bugs. If you use it, it breaks and you're feeling lucky, raise an issue.
An explanation of how the python documentation files are generated is in the notebook `exploring ast.ipynb`.
