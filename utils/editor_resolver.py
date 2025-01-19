import platform

def resolve_editor_command(editor: str, file_path: str) -> str:
    """
    Resolve the command to open a file in the specified editor.
    :param editor: Name of the editor.
    :param file_path: Path of the file to open.
    :return: Command to open the file.
    """
    editor_commands = {
        "code": f"code {file_path}",
        "vim": f"vim {file_path}",
        "nvim": f"nvim {file_path}",
        "nano": f"nano {file_path}",
    }

    if editor == "default":
        if platform.system() == "Darwin":
            return f"open {file_path}"
        elif platform.system() == "Windows":
            return f"start {file_path}"
        elif platform.system() == "Linux":
            return f"xdg-open {file_path}"

    if editor in editor_commands:
        return editor_commands[editor]

    raise ValueError(f"❌ Unsupported editor: {editor}")
