import os
from typing import List
from pathlib import Path


def list_files(directory: os.PathLike, extensions: List[str]) -> List[str]:
    """
    Gets a list of files in a directory (and subdirectories) with specified extensions,
    returning paths relative to the input directory.

    Parameters
    ----------
    directory : os.PathLike
        The directory path to scan for files
    extensions : List[str]
        List of file extensions to search for (without the dot)
        e.g. ['txt', 'pdf', 'doc']

    Returns
    -------
    List[str]
        A list of relative file paths matching the specified extensions

    Examples
    --------
    >>> list_files('/path/to/dir', ['txt', 'pdf'])
    ['file1.txt', 'subdirectory/file2.pdf']
    """
    # Convert directory to Path object for better path handling
    path = Path(directory).resolve()

    # Ensure extensions don't have leading dots and are lowercase
    clean_extensions = [ext.lower().lstrip(".") for ext in extensions]

    # List to store matching files
    matching_files = []

    # Walk through directory and subdirectories
    for root, _, files in os.walk(path):
        for file in files:
            # Check if file extension matches any in the list
            if any(file.lower().endswith(f".{ext}") for ext in clean_extensions):
                # Get full path and convert to relative path
                full_path = Path(root) / file
                relative_path = full_path.relative_to(path)
                matching_files.append(str(relative_path))

    return matching_files
