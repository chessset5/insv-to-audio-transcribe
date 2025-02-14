import os


def get_path_components(file_path: str) -> dict[str, str]:
    '''
    get_path_components returns the string components of a dir<br>
    

    Args:
        file_path (str): file path to be processed

    Returns:
        dict\[str,str\]:
            `"dir"`: directory<br>
            `"filename"`: name of the file, no extension<br>
            `"ext"`: the extension of the file<br>
    '''
    # Split the file path into directory, base name, and extension
    directory, base_name = os.path.split(file_path)
    name, ext = os.path.splitext(base_name)

    return {"dir": directory, "filename": name, "ext": ext}


def get_base_file_name(file_path: str) -> str:
    """
    getBaseName returns the file name of a path, no ext

    Args:
        file (str): file path

    Returns:
        str: file name
    """
    return get_path_components(file_path=file_path)["filename"]


def increment_filename(file_path: str, template: str = " ({counter})") -> str:
    """
    increment_filename increments given file

    Args:
        file_path (str): path to file. will increment if exists
        template (str): python template. Please use `counter` for the increment argument<br>
            Defaults to " ({counter})".<br>
            ex: `' ({counter:03})'` to pad left with zeros.

    Returns:
        str: new file path
    """
    # Split the file path into directory, base name, and extension
    directory, base_name = os.path.split(file_path)
    name, ext = os.path.splitext(base_name)

    # Initialize the counter
    counter: int = 1

    # Generate new file name with increment
    while os.path.exists(file_path):
        increment: str = template.replace("{counter}", str(counter))
        new_name: str = f"{name}{increment}{ext}"
        file_path = os.path.normpath(os.path.join(directory, new_name))
        counter += 1
    return file_path
