import random
from typing import Optional, List, Dict, Any

from handlers.APIHandler import api
from handlers.CacheHandler import cached_api
from modes.PracticeMode import (
    PracticeMode,
    log_problem_details,
    open_in_browser,
    create_and_solve_handler,
)
from utils.logger import log, LogLevel

company_names = api.get_company_names()


def get_company(company_name: str) -> Optional[Dict[str, Any]]:
    """
    Get company details by name.
    :param company_name: The name of the company (e.g., "facebook").
    :return: Company dictionary or None if not found.
    """
    for company in company_names:
        if company["name"].lower() == company_name.lower():
            return company
    return None


def get_random_company_problem(
    company_name: str,
    duration: Optional[str] = None,
    difficulties: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get a random problem from a specific company for a given duration.
    :param company_name: The name of the company (e.g., "facebook").
    :param duration: Duration to filter questions (e.g., "thirty-days", "three-months").
    :param difficulties: Difficulty levels of the problems (e.g., "Easy", "Medium", "Hard").
    :param tags: Tags of the problems (e.g., "Array", "String").
    :return: A random problem dictionary or None if no problems are found.
    """
    problems = cached_api.fetch_company_questions_for_duration(
        company_name=company_name,
        duration=duration,
        difficulties=difficulties,
        tags=tags,
    )

    if not problems:
        return None

    random_index = random.randint(0, len(problems) - 1)
    return problems[random_index]


class CompanyMode(PracticeMode):
    def handle(self, args):
        company = get_company(args["company_name"])

        if company is None:
            log(f"❌ Company not found: ${args['company_name']}", LogLevel.ERROR)
            raise ValueError(f"Company not found: {args['company_name']}")

        # Mapping of number words to their numeric values
        number_word_mapping = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
            "eleven": 11,
            "twelve": 12,
            "thirteen": 13,
            "fourteen": 14,
            "fifteen": 15,
            "sixteen": 16,
            "seventeen": 17,
            "eighteen": 18,
            "nineteen": 19,
            "twenty": 20,
            "thirty": 30,
        }

        log_msg = f"Selected 👔 Company Mode: Top questions asked at {company['name']}"
        if args["duration"] and args["duration"].lower() != "all":
            # Convert duration to numbers if it matches the mapping
            duration_parts = (
                args["duration"].lower().split("-")
            )  # Split on dashes if necessary
            numeric_duration = " ".join(
                str(number_word_mapping.get(word, word)) for word in duration_parts
            )
            log_msg += f" in the last {numeric_duration}"
        log(log_msg, LogLevel.INFO)

        try:
            problem = get_random_company_problem(
                company_name=company["name"],
                duration=args["duration"],
                difficulties=args["difficulties"],
                tags=args["tags"],
            )

            if not problem:
                log("No problems found for the selected criteria.", LogLevel.ERROR)
                return

            url = f"https://leetcode.com/problems/{problem['titleSlug']}"
            log_problem_details(problem, problem["difficulty"], url)
            open_in_browser(url, args.open_in_browser)
            create_and_solve_handler(
                problem["titleSlug"],
                problem["codeSnippets"],
                problem["difficulty"],
                args,
            )
        except Exception as e:
            log(f"Failed to fetch company problem: {str(e)}", LogLevel.ERROR)
