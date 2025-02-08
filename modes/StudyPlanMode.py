import random
from typing import List, Dict, Any, Optional

from handlers.CacheHandler import cached_api
from modes.PracticeMode import (
    PracticeMode,
    log_problem_details,
    create_and_solve_handler,
    open_in_browser,
)
from utils.constants import difficulty_map
from utils.logger import log, LogLevel


def get_study_plan_problems(slug: str) -> List[Dict[str, Any]]:
    """
    Fetch the list of problems for a specific study plan.
    :param slug: The slug of the study plan (e.g., "leetcode-75").
    :return: A list of dictionaries, each containing details of a problem.
    """
    study_plan = cached_api.get_study_plan(slug)

    if not study_plan:
        raise Exception(f"❌ Study plan not found for slug: {slug}")

    # Gather all questions from the study plan subgroups
    problems = []
    for subgroup in study_plan.get("planSubGroups", []):
        questions = subgroup.get("questions", [])
        problems.extend(questions)  # Add all questions to the list

    if not problems:
        raise Exception(f"❌ No problems found for study plan: {slug}")

    return problems


def get_random_study_plan_problem(slug: str) -> Optional[Dict[str, Any]]:
    """
    Get a random problem from a specific study plan.
    :param slug: The slug of the study plan (e.g., "leetcode-75").
    :return: A random problem dictionary or None if no problems are found.
    """
    problems = get_study_plan_problems(slug)

    if not problems:
        return None

    random_index = random.randint(0, len(problems) - 1)
    problem = problems[random_index]

    # Get the problem in the right format
    return cached_api.fetch_problem(problem["titleSlug"])


class StudyPlanMode(PracticeMode):
    def handle(self, args):
        try:
            log(f"Selected 🎯 Study Plan Mode: {args['plan_name']}", LogLevel.INFO)
            problem = get_random_study_plan_problem(args["plan_name"])
            if not problem:
                log("No problems found for the selected study plan.", LogLevel.ERROR)
                return
            difficulty_label = difficulty_map[problem["difficulty"].lower()]
            url = f"https://leetcode.com/problems/{problem['titleSlug']}"
            log_problem_details(problem, difficulty_label, url)
            open_in_browser(url, args["open_in_browser"])
            create_and_solve_handler(
                problem["titleSlug"], problem["codeSnippets"], difficulty_label, args
            )
        except Exception as e:
            log(f"Failed to fetch random problem: {str(e)}", LogLevel.ERROR)
