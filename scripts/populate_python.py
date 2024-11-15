import os
import ast
from typing import List, Tuple


def get_source_segment(source: str, node: ast.AST) -> str:
    """Extract the source code segment for a given AST node."""
    source_lines = source.splitlines()
    if isinstance(node, ast.AST):
        start_line = node.lineno - 1
        end_line = node.end_lineno if hasattr(node, "end_lineno") else start_line + 1

        # Get the full lines
        lines = source_lines[start_line:end_line]

        # For function and class definitions, we need to find the end of the signature
        # (the colon that's not inside any parentheses)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            full_text = "\n".join(lines)
            paren_count = 0
            for i, char in enumerate(full_text):
                if char == "(":
                    paren_count += 1
                elif char == ")":
                    paren_count -= 1
                elif char == ":" and paren_count == 0:
                    # Found the end of the signature
                    return full_text[: i + 1]

        return "\n".join(lines)
    return ""


def extract_signatures(source: str) -> List[Tuple[str, str, str]]:
    """
    Extract function and class signatures from Python source code.
    Returns a list of tuples (type, name, signature) where type is either 'function' or 'class'.
    """
    tree = ast.parse(source)
    signatures = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            # Get the full signature including decorators
            decorator_nodes = getattr(node, "decorator_list", [])
            signature_parts = []

            # Add decorators
            for decorator in decorator_nodes:
                decorator_text = get_source_segment(source, decorator)
                signature_parts.append(f"@{decorator_text}")

            # Add the function signature
            signature = get_source_segment(source, node)
            signature_parts.append(signature)

            full_signature = "\n".join(signature_parts)
            signatures.append(("function", name, full_signature))

        elif isinstance(node, ast.ClassDef):
            name = node.name
            # Get the full signature including decorators and base classes
            decorator_nodes = getattr(node, "decorator_list", [])
            signature_parts = []

            # Add decorators
            for decorator in decorator_nodes:
                decorator_text = get_source_segment(source, decorator)
                signature_parts.append(f"@{decorator_text}")

            # Add the class signature
            signature = get_source_segment(source, node)
            signature_parts.append(signature)

            full_signature = "\n".join(signature_parts)
            signatures.append(("class", name, full_signature))

    return signatures


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

    output = []
    signatures = extract_signatures(source)

    for _, name, signature in signatures:
        # Add the header
        output.append(f"### {name}")
        # Add the signature in a code block
        output.append("```python")
        output.append(signature)
        output.append("```")
        # Add a blank line after each item
        output.append("")

    return "\n".join(output)
