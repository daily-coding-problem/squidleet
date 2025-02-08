from modes.PracticeMode import PracticeMode, get_random_study_plan_problem
from utils.constants import difficulty_map
from utils.logger import log, LogLevel


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
            self.log_problem_details(problem, difficulty_label, url)
            self.open_in_browser(url, args["open_in_browser"])
            self.create_and_solve_handler(
                problem["titleSlug"], problem["codeSnippets"], difficulty_label, args
            )
        except Exception as e:
            log(f"Failed to fetch random problem: {str(e)}", LogLevel.ERROR)
