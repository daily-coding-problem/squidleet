import os

language_to_extension = {
    "python": "py",
    "javascript": "js",
    "java": "java",
    "c++": "cpp",
    "c": "c",
    "typescript": "ts",
    "ruby": "rb",
    "swift": "swift",
    "go": "go",
}

available_languages = list(language_to_extension.keys())


def create_solution_file(problem_slug: str, language: str) -> str:
    """
    Create a solution file for the specified problem and language.
    :param problem_slug: Slug of the problem.
    :param language: Programming language.
    :return: Path to the created file.
    """
    file_extension = language_to_extension.get(language)
    if not file_extension:
        raise ValueError(f"❌ Unsupported language: {language}")

    file_name = f"{problem_slug}.{file_extension}"
    code_path = os.path.join("./solutions", file_name)

    # Ensure the directory and file exist
    os.makedirs(os.path.dirname(code_path), exist_ok=True)
    open(code_path, "a").close()

    return code_path
