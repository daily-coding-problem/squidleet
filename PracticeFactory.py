from lib.fetch_problems import get_random_problem
from lib.fetch_daily_challenge import fetch_daily_challenge
from lib.fetch_problem import fetch_problem
from utils.logger import log, LogLevel
from handlers.SolutionHandler import SolutionHandler

difficulty_map = {
    "easy": "Easy",
    "medium": "Medium",
    "hard": "Hard",
}

class PracticeMode:
    def handle(self, args):
        raise NotImplementedError("This method should be implemented by subclasses.")

class RandomProblemMode(PracticeMode):
    def handle(self, args):
        problem = get_random_problem(args["difficulties"])

        # Log problem details
        log(f"🎯 Problem Selected: {problem['title']}", LogLevel.INFO)
        log(f"✨ Difficulty: {difficulty_map[problem['difficulty']]}", LogLevel.INFO)
        log(f"🔗 URL: https://leetcode.com/problems/{problem['slug']}", LogLevel.INFO)

        # Open in browser if flag is set
        if args["open_in_browser"]:
            import webbrowser
            webbrowser.open(f"https://leetcode.com/problems/{problem['slug']}")

        handler = SolutionHandler(
            problem=problem["slug"],
            difficulty=difficulty_map[problem["difficulty"]],
            editor=args["editor"],
            language=args["language"],
            time_limit=args["time_limit"],
        )
        handler.solve()

class DailyChallengeMode(PracticeMode):
    def handle(self, args):
        try:
            daily_challenge = fetch_daily_challenge()

            difficulty_label = difficulty_map[daily_challenge["question"]["difficulty"].lower()]

            # Log daily challenge details
            log("🎯 Daily Coding Challenge:", LogLevel.INFO)
            log(f"📅 Date: {daily_challenge['date']}", LogLevel.INFO)
            log(f"📖 Title: {daily_challenge['question']['title']}", LogLevel.INFO)
            log(f"✨ Difficulty: {difficulty_label}", LogLevel.INFO)
            log(f"🔗 Link: https://leetcode.com{daily_challenge['link']}", LogLevel.INFO)

            if args["open_in_browser"]:
                import webbrowser
                webbrowser.open(f"https://leetcode.com{daily_challenge['link']}")

            handler = SolutionHandler(
                problem=daily_challenge["question"]["titleSlug"],
                difficulty=difficulty_label,
                editor=args["editor"],
                language=args["language"],
                time_limit=args["time_limit"],
            )
            handler.solve()
        except Exception as e:
            log(f"Failed to fetch daily challenge: {str(e)}", LogLevel.ERROR)

class CustomPracticeMode(PracticeMode):
    def handle(self, args):
        problems = args["problems"]

        for slug in problems:
            log(f"🔍 Fetching details for problem: {slug}", LogLevel.INFO)
            try:
                problem = fetch_problem(slug.strip())

                if not problem:
                    log(f"Problem with slug '{slug}' not found.", LogLevel.ERROR)
                    continue

                log(f"🎯 Problem Selected: {problem['title']}", LogLevel.INFO)
                log(f"✨ Difficulty: {problem['difficulty']}", LogLevel.INFO)
                log(f"🔗 URL: https://leetcode.com/problems/{slug}", LogLevel.INFO)

                if args["open_in_browser"]:
                    import webbrowser
                    webbrowser.open(f"https://leetcode.com/problems/{problem['slug']}")

                handler = SolutionHandler(
                    problem=slug,
                    difficulty=problem["difficulty"],
                    editor=args["editor"],
                    language=args["language"],
                    time_limit=args["time_limit"],
                )
                handler.solve()
            except Exception as e:
                log(f"Failed to process problem '{slug}': {str(e)}", LogLevel.ERROR)

class PracticeModeFactory:
    @staticmethod
    def get_mode(selection_mode: str) -> PracticeMode:
        if selection_mode == "random":
            return RandomProblemMode()
        elif selection_mode == "daily":
            return DailyChallengeMode()
        elif selection_mode == "custom":
            return CustomPracticeMode()
        elif selection_mode == "study-plan":
            raise ValueError("Study Plan mode is not yet supported.")
        else:
            raise ValueError(f"Unsupported mode: {selection_mode}")
