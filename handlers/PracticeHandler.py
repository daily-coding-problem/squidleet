import random
import html2text

from typing import List, Dict, Any, Optional

from utils.logger import log, LogLevel
from handlers.SolutionHandler import SolutionHandler
from api.LeetCodeAPI import LeetCodeAPI

difficulty_map = {
    "easy": "Easy",
    "medium": "Medium",
    "hard": "Hard",
}


class PracticeMode:
    def __init__(self):
        self.leetcode_api = LeetCodeAPI()

    def handle(self, args):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def log_problem_details(self, problem, difficulty_label, url):
        log(f"🎯 Problem Selected: {problem.get('title', 'Unknown')}", LogLevel.INFO)
        log(f"✨ Difficulty: {difficulty_label}", LogLevel.INFO)
        log(f"🔗 URL: {url}", LogLevel.INFO)

        topic_tags = problem.get("topicTags", [])
        if topic_tags:
            tags = ", ".join(tag.get("name", "Unknown") for tag in topic_tags)
            log(f"🏷️ Tags: {tags}", LogLevel.INFO)

        ac_rate = problem.get("acRate")
        if ac_rate is not None:
            log(f"📈 Acceptance Rate: {ac_rate:.2f}%", LogLevel.INFO)

        content = problem.get("content")
        if content:
            try:
                text_maker = html2text.HTML2Text()
                text_maker.ignore_links = True
                plain_text = text_maker.handle(content)
                log(f"📝 Problem Description:", LogLevel.INFO)
                log(f"{plain_text}", LogLevel.INFO)
            except Exception as e:
                log(f"⚠️ Failed to process problem description: {e}", LogLevel.WARN)

    def open_in_browser(self, url, open_flag):
        if open_flag:
            import webbrowser

            webbrowser.open(url)

    def create_and_solve_handler(self, problem_slug, difficulty_label, args):
        handler = SolutionHandler(
            problem=problem_slug,
            difficulty=difficulty_label,
            editor=args["editor"],
            language=args["language"],
            time_limit=args["time_limit"],
        )
        handler.solve()

    def get_random_problem(
        self,
        difficulties: Optional[List[str]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get a random problem from LeetCode.
        :param difficulties: Difficulty levels of the problems (e.g., "Easy", "Medium", "Hard").
        :return: A random problem dictionary or None if no problems are found.
        """
        problems = self.leetcode_api.fetch_problems(
            limit=1000, difficulties=difficulties
        )

        if not problems:
            return None

        random_index = random.randint(0, len(problems) - 1)
        return problems[random_index]

    def get_study_plan_problems(self, slug: str) -> List[Dict[str, Any]]:
        """
        Fetch the list of problems for a specific study plan.
        :param slug: The slug of the study plan (e.g., "leetcode-75").
        :return: A list of dictionaries, each containing details of a problem.
        """
        study_plan = self.leetcode_api.get_study_plan(slug)

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

    def get_random_study_plan_problem(self, slug: str) -> Optional[Dict[str, Any]]:
        """
        Get a random problem from a specific study plan.
        :param slug: The slug of the study plan (e.g., "leetcode-75").
        :return: A random problem dictionary or None if no problems are found.
        """
        problems = self.get_study_plan_problems(slug)

        if not problems:
            return None

        random_index = random.randint(0, len(problems) - 1)
        return problems[random_index]


class RandomProblemMode(PracticeMode):
    def handle(self, args):
        log("Selected 🎲 Random Problem Mode", LogLevel.INFO)

        try:
            # Use the LeetCodeAPI's fetch_problems method
            problem = self.get_random_problem(difficulties=args["difficulties"])

            if not problem:
                log("No problems found for the selected difficulties.", LogLevel.ERROR)
                return

            difficulty_label = difficulty_map[problem["difficulty"].lower()]
            url = f"https://leetcode.com/problems/{problem['titleSlug']}"

            self.log_problem_details(problem, difficulty_label, url)
            self.open_in_browser(url, args["open_in_browser"])
            self.create_and_solve_handler(problem["titleSlug"], difficulty_label, args)
        except Exception as e:
            log(f"Failed to fetch random problem: {str(e)}", LogLevel.ERROR)


class DailyChallengeMode(PracticeMode):
    def handle(self, args):
        log("Selected 📅 Daily Challenge Mode", LogLevel.INFO)

        try:
            # Use the LeetCodeAPI's fetch_daily_challenge method
            daily_challenge = self.leetcode_api.fetch_daily_challenge()
            difficulty_label = difficulty_map[
                daily_challenge["question"]["difficulty"].lower()
            ]
            url = f"https://leetcode.com{daily_challenge['link'].removesuffix('/')}"

            log("🎯 Daily Coding Challenge:", LogLevel.INFO)
            log(f"📅 Date: {daily_challenge['date']}", LogLevel.INFO)
            self.log_problem_details(daily_challenge["question"], difficulty_label, url)
            self.open_in_browser(url, args["open_in_browser"])
            self.create_and_solve_handler(
                daily_challenge["question"]["titleSlug"], difficulty_label, args
            )
        except Exception as e:
            log(f"Failed to fetch daily challenge: {str(e)}", LogLevel.ERROR)


class CustomPracticeMode(PracticeMode):
    def handle(self, args):
        log("Selected 🧩 Custom Practice Mode", LogLevel.INFO)

        for slug in args["problems"]:
            try:
                problem = self.leetcode_api.fetch_problem(slug.strip())

                if not problem:
                    log(f"Problem with slug '{slug}' not found.", LogLevel.ERROR)
                    continue

                difficulty_label = difficulty_map[problem["difficulty"].lower()]
                url = f"https://leetcode.com/problems/{problem['titleSlug']}"

                self.log_problem_details(problem, difficulty_label, url)
                self.open_in_browser(url, args["open_in_browser"])
                self.create_and_solve_handler(slug, difficulty_label, args)
            except Exception as e:
                log(f"Failed to process problem '{slug}': {str(e)}", LogLevel.ERROR)


class StudyPlanMode(PracticeMode):
    def handle(self, args):
        try:
            log(f"Selected 🎯 Study Plan Mode: {args['plan_name']}", LogLevel.INFO)

            problem = self.get_random_study_plan_problem(args["plan_name"])

            if not problem:
                log("No problems found for the selected study plan.", LogLevel.ERROR)
                return

            # Get the problem in the right format
            problem = self.leetcode_api.fetch_problem(problem["titleSlug"])

            difficulty_label = difficulty_map[problem["difficulty"].lower()]
            url = f"https://leetcode.com/problems/{problem['titleSlug']}"

            self.log_problem_details(problem, difficulty_label, url)
            self.open_in_browser(url, args["open_in_browser"])
            self.create_and_solve_handler(problem["titleSlug"], difficulty_label, args)
        except Exception as e:
            log(f"Failed to fetch random problem: {str(e)}", LogLevel.ERROR)


class PracticeModeHandler:
    @staticmethod
    def get_mode(selection_mode: str) -> PracticeMode:
        if selection_mode == "random":
            return RandomProblemMode()
        elif selection_mode == "daily":
            return DailyChallengeMode()
        elif selection_mode == "custom":
            return CustomPracticeMode()
        elif selection_mode == "study-plan":
            return StudyPlanMode()
        else:
            raise ValueError(f"Unsupported mode: {selection_mode}")
