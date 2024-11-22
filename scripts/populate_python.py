import os
import ast


def render_name(name: str, entity_type: str = "") -> str:
    """
    Renders the name of an entity for markdown

    Parameters
    ----------
    name: str
        The name of the entity
    entity_type: str
        The kind of entity we're rendering. "method" and "class" have slightly different formatting.
        The default is just a def, for functions

    Returns
    -------
    str
        The name of the entity, formatted for markdown
    """
    if entity_type == "method":
        return f"#### `{name}`\n```\nmethod {name}"
    elif entity_type == "class":
        return f"### `{name}`\n```\nclass {name}"
    else:
        return f"### `{name}`\n```\ndef {name}"


def render_docstring(
    docstring: str,
    header_level: int = 4,
    parameters_string: str = "Parameters",
    returns_string: str = "Returns",
):
    """
    Renders the docstring of an entity for markdown.
    The header level of the subsections are configurable.

    Parameters
    ----------
    docstring: str
        The docstring to render
    header_level: int
        The level of header that the Parameters and Returns should be rendered at
    parameters_string: str
        The string used to delineate the parameters section
    returns_string: str
        The string used to delineate the returns section

    Returns
    -------
    str
        The markdown for the docstring
    """
    if (parameters_string in docstring) & (returns_string in docstring):
        result, func_sig_string = docstring.split(parameters_string)
        pars_string, ret_string = func_sig_string.split(returns_string)
        result += "#" * header_level + f" {parameters_string}\n"
        for line in pars_string.split("\n"):
            if any([char.isalnum() for char in line]):
                result += line.strip() + "\n\n"
        result += "#" * header_level + f" {returns_string}\n"
        for line in ret_string.split("\n"):
            if any([char.isalnum() for char in line]):
                result += line.strip() + "\n\n"
    else:
        result = docstring
    return result


def build_annotation(annotation):
    if isinstance(annotation, ast.Name):
        return annotation.id
    elif isinstance(annotation, ast.Subscript):
        try:
            return f"{annotation.slice.id}[{build_annotation(annotation.value)}]"
        except AttributeError:
            print("Couldn't parse Subscript")
            return ""
    else:
        return ""


def render_args(function_args: ast.arguments):
    result = ""
    args = [arg.arg for arg in function_args.args]
    annotations = [
        build_annotation(x) for x in [arg.annotation for arg in function_args.args]
    ]
    for arg, annotation in zip(args, annotations):
        result += f"\t{arg}: {annotation}\n\n"
    return result


def build_function_md(function_definition: ast.FunctionDef):
    result = ""
    result += render_name(function_definition.name)
    result += "(\n"
    result += render_args(function_definition.args)
    result += ")\n```"
    result += "\n\n"
    if ast.get_docstring(function_definition):
        result += render_docstring(ast.get_docstring(function_definition))

    return result


def build_class_md(class_definition: ast.ClassDef):
    methods = [x for x in class_definition.body if isinstance(x, ast.FunctionDef)]
    try:
        init_method = [x for x in methods if x.name == "__init__"][0]
    except IndexError:
        print(f"No methods in {class_definition.name}")

    result = ""
    result += render_name(class_definition.name, entity_type="class")
    result += "(\n"
    try:
        result += render_args(init_method.args)
    except UnboundLocalError:
        print(f"No init method for {class_definition.name}")
    result += ")\n```\n\n"

    if ast.get_docstring(class_definition):
        result += render_docstring(ast.get_docstring(class_definition))
    if len(methods) > 1:
        result += "\n### Methods"
        for method in methods:
            result += "\n\n"
            result += render_name(method.name, entity_type="method")
            result += "(\n"
            result += render_args(method.args)
            result += ")\n```"
            result += "\n\n"
            if ast.get_docstring(method):
                result += render_docstring(ast.get_docstring(method), header_level=5)

    return result


def populate_python(file_path: os.PathLike) -> str:
    """
    Process a Python file and generate markdown documentation with function and class signatures.

    Args:
        file_path: Path to the Python file to process

    Returns:
        A string containing markdown formatted documentation
    """
    with open(file_path, "r") as f:
        source = f.read()

    result = []

    tree = ast.parse(source)

    for entity in tree.body:
        if isinstance(entity, ast.FunctionDef):
            result.append(build_function_md(entity))
        elif isinstance(entity, ast.ClassDef):
            result.append(build_class_md(entity))

    return "\n".join(result)
