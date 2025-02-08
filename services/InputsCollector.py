import os

from handlers.APIHandler import api
from handlers.file_handler import available_languages


def collect(cli_options):
    practice_mode = cli_options.get("practice_mode", "study-plan")
    difficulties = None
    problems = None

    if practice_mode == "random":
        difficulties = cli_options.get("difficulties")

        if difficulties:
            difficulties = difficulties.split(",")
    elif practice_mode == "custom":
        problems = cli_options.get("problems", "")

        if problems:
            problems = problems.split(",")

    company_name = cli_options.get("company_name", "")
    tags = cli_options.get("tags", "")
    duration = cli_options.get("duration", "all")
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
        "company_name": company_name,
        "tags": tags,
        "duration": duration,
        "language": language,
        "time_limit": time_limit,
        "editor": editor,
        "open_in_browser": open_in_browser,
        "log_level": log_level,
    }

    _validate(inputs)

    return inputs


def _validate(inputs):
    validate_practice_mode(inputs["practice_mode"])
    validate_company_mode(inputs)
    validate_difficulties(inputs)
    validate_problems(inputs)
    validate_study_plan(inputs)
    validate_language(inputs["language"])
    validate_time_limit(inputs["time_limit"])
    validate_editor(inputs["editor"])
    validate_log_level(inputs["log_level"])


def validate_practice_mode(practice_mode):
    if not practice_mode:
        raise ValueError("Practice mode is required.")

    valid_modes = ["company", "random", "custom", "study-plan"]
    if practice_mode not in valid_modes:
        raise ValueError(f"Invalid practice mode. Use one of: {', '.join(valid_modes)}")


def validate_company_mode(inputs):
    if inputs["practice_mode"] == "company":
        if os.environ.get("LEETCODE_SESSION") is None:
            raise ValueError("Company mode requires an authenticated session.")

        company_name = inputs.get("company_name")
        if not company_name:
            raise ValueError("Company name is required for Company mode.")

        company_names = api.get_company_names()
        valid_company_names = [company["name"].lower() for company in company_names]
        if company_name.lower() not in valid_company_names:
            raise ValueError(
                f"Invalid company name. Supported companies: {', '.join(valid_company_names)}"
            )

    if inputs["company_name"] and inputs["practice_mode"] != "company":
        raise ValueError("Company name is only allowed in Company mode.")

    if inputs["tags"] and inputs["practice_mode"] != "company":
        raise ValueError("Tags are only allowed in Company mode.")

    if inputs["duration"] and inputs["practice_mode"] != "company":
        raise ValueError("Duration is only allowed in Company mode.")

    if inputs["tags"]:
        topic_tags = api.get_topic_tags()
        valid_tags = [tag.lower() for tag in topic_tags]
        standardized_tags = [tag.lower() for tag in inputs["tags"]]
        if any(tag not in valid_tags for tag in standardized_tags):
            raise ValueError(f"Invalid tags. Supported tags: {', '.join(valid_tags)}")

    valid_durations = [
        "thirty-days",
        "three-months",
        "six-months",
        "more-than-six-months",
        "all",
    ]
    if inputs["duration"] and inputs["duration"] not in valid_durations:
        raise ValueError(
            f"Invalid duration: {inputs['duration']}. Must be one of {', '.join(valid_durations)}."
        )


def validate_difficulties(inputs):
    # Validate if difficulty levels are required for Random mode
    if inputs["practice_mode"] == "random" and not inputs.get("difficulties"):
        raise ValueError("Difficulty level is required for Random Practice mode.")

    difficulties = inputs.get("difficulties")
    if difficulties and any(
        difficulty not in ["easy", "medium", "hard"] for difficulty in difficulties
    ):
        raise ValueError("Invalid difficulty levels. Use 'easy', 'medium', or 'hard'.")


def validate_problems(inputs):
    # Validate if problems are required for Custom mode
    if inputs["practice_mode"] == "custom" and not inputs.get("problems"):
        raise ValueError("At least one problem is required for Custom Practice mode.")


def validate_study_plan(inputs):
    # Validate if study plan name is required for Study Plan mode
    if inputs["practice_mode"] == "study-plan" and not inputs.get("plan_name"):
        raise ValueError("Study plan name is required for Study Plan mode.")


def validate_language(language):
    # Validate programming language
    if language not in available_languages:
        raise ValueError(
            "Invalid language. Supported languages: " + ", ".join(available_languages)
        )


def validate_time_limit(time_limit):
    # Validate that time_limit is an integer
    if not isinstance(time_limit, int):
        raise ValueError("Time limit must be an integer.")


def validate_editor(editor):
    # Validate editor from a list of valid editors
    valid_editors = ["default", "code", "nvim", "nano", "vim"]
    if editor not in valid_editors:
        raise ValueError(f"Invalid editor. Use one of: {', '.join(valid_editors)}")


def validate_log_level(log_level):
    # Validate logging levels
    valid_log_levels = ["DEBUG", "INFO", "WARN", "ERROR"]
    if log_level not in valid_log_levels:
        raise ValueError(
            f"Invalid log level. Use one of: {', '.join(valid_log_levels)}"
        )
