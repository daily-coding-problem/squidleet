from handlers.file_handler import available_languages


def collect(cli_options):
    practice_mode = cli_options.get("practice_mode", "study-plan")
    difficulties = None
    problems = None

    if practice_mode == "random":
        difficulties = cli_options.get(
            "difficulties", ["easy", "medium", "hard"]
        ).split(",")
    elif practice_mode == "custom":
        problems = cli_options.get("problems", "").split(",")

    log_level = cli_options.get("log_level", "INFO")
    plan_name = cli_options.get("study_plan", "top-interview-150")
    language = cli_options.get("language", "python")
    time_limit = cli_options.get("time_limit", 45)
    editor = cli_options.get("editor", "default")
    open_in_browser = cli_options.get("open_in_browser", False)

    inputs = {
        "practice_mode": practice_mode,
        "difficulties": difficulties,
        "plan_name": plan_name,
        "problems": problems,
        "language": language,
        "time_limit": time_limit,
        "editor": editor,
        "open_in_browser": open_in_browser,
        "log_level": log_level,
    }

    _validate(inputs)

    return inputs


def _validate(inputs):
    if not inputs["practice_mode"]:
        raise ValueError("Practice mode is required.")

    if inputs["practice_mode"] == "random" and not inputs.get("difficulties"):
        raise ValueError("Difficulty level is required for Random Practice mode.")

    if inputs["practice_mode"] == "custom" and not inputs.get("problems"):
        raise ValueError("At least one problem is required for Custom Practice mode.")

    if inputs["practice_mode"] == "study-plan" and not inputs.get("plan_name"):
        raise ValueError("Study plan name is required for Study Plan mode.")

    if inputs["difficulties"] and any(
        difficulty not in ["easy", "medium", "hard"]
        for difficulty in inputs["difficulties"]
    ):
        raise ValueError("Invalid difficulty levels. Use 'easy', 'medium', or 'hard'.")

    if inputs["language"] not in available_languages:
        raise ValueError(
            "Invalid language. Supported languages: " + ", ".join(available_languages)
        )

    if not isinstance(inputs["time_limit"], int):
        raise ValueError("Time limit must be an integer.")

    valid_editors = ["default", "code", "nvim", "nano", "vim"]
    if inputs["editor"] not in valid_editors:
        raise ValueError(f"Invalid editor. Use one of: {', '.join(valid_editors)}")

    valid_log_levels = ["DEBUG", "INFO", "WARN", "ERROR"]
    if inputs["log_level"] not in valid_log_levels:
        raise ValueError(
            f"Invalid log level. Use one of: {', '.join(valid_log_levels)}"
        )
