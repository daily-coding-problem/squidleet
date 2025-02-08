from modes.PracticeMode import PracticeMode, log_problem_details, open_in_browser, create_and_solve_handler
from utils.constants import difficulty_map
from utils.logger import log, LogLevel
from handlers.CacheHandler import cached_api


class CustomPracticeMode(PracticeMode):
    def handle(self, args):
        log("Selected 🧩 Custom Practice Mode", LogLevel.INFO)
        for slug in args["problems"]:
            try:
                problem = cached_api.fetch_problem(slug.strip())
                if not problem:
                    log(f"Problem with slug '{slug}' not found.", LogLevel.ERROR)
                    continue
                difficulty_label = difficulty_map[problem["difficulty"].lower()]
                url = f"https://leetcode.com/problems/{problem['titleSlug']}"
                log_problem_details(problem, difficulty_label, url)
                open_in_browser(url, args["open_in_browser"])
                create_and_solve_handler(
                    slug, problem["codeSnippets"], difficulty_label, args
                )
            except Exception as e:
                log(f"Failed to process problem '{slug}': {str(e)}", LogLevel.ERROR)
