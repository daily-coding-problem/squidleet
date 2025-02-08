import random
from typing import Optional, List, Dict, Any

from handlers.CacheHandler import cached_api
from modes.PracticeMode import (
    PracticeMode,
    log_problem_details,
    open_in_browser,
    create_and_solve_handler,
)
from utils.constants import difficulty_map
from utils.logger import log, LogLevel


def get_random_problem(
    difficulties: Optional[List[str]] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get a random problem from LeetCode.
    :param difficulties: Difficulty levels of the problems (e.g., "Easy", "Medium", "Hard").
    :return: A random problem dictionary or None if no problems are found.
    """
    problems = cached_api.fetch_problems(limit=1000, difficulties=difficulties)

    if not problems:
        return None

    random_index = random.randint(0, len(problems) - 1)
    return problems[random_index]


class RandomProblemMode(PracticeMode):
    def handle(self, args):
        log("Selected 🎲 Random Problem Mode", LogLevel.INFO)
        try:
            problem = get_random_problem(difficulties=args["difficulties"])
            if not problem:
                log("No problems found for the selected difficulties.", LogLevel.ERROR)
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
