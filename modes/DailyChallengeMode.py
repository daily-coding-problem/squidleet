from modes.PracticeMode import PracticeMode
from utils.constants import difficulty_map
from utils.logger import log, LogLevel
from handlers.CacheHandler import cached_api


class DailyChallengeMode(PracticeMode):
    def handle(self, args):
        log("Selected 📅 Daily Challenge Mode", LogLevel.INFO)
        try:
            daily_challenge = cached_api.fetch_daily_challenge()
            difficulty_label = difficulty_map[
                daily_challenge["question"]["difficulty"].lower()
            ]
            url = f"https://leetcode.com{daily_challenge['link'].removesuffix('/')}"
            log("🎯 Daily Coding Challenge:", LogLevel.INFO)
            log(f"📅 Date: {daily_challenge['date']}", LogLevel.INFO)
            self.log_problem_details(daily_challenge["question"], difficulty_label, url)
            self.open_in_browser(url, args["open_in_browser"])
            self.create_and_solve_handler(
                daily_challenge["question"]["titleSlug"],
                daily_challenge["codeSnippets"],
                difficulty_label,
                args,
            )
        except Exception as e:
            log(f"Failed to fetch daily challenge: {str(e)}", LogLevel.ERROR)
