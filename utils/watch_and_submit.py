import os
import time

from api.LeetCodeAPI import LeetCodeAPI

from utils.timer import start_timer
from utils.logger import log, LogLevel


def setup_file_watcher(code_path, problem_slug, language, time_limit):
    """
    Set up a file watcher to monitor changes and submit the solution.
    """
    leetcode_api = LeetCodeAPI()

    start_timer(time_limit, problem_slug)
    log(f"Watching file: {code_path}...", LogLevel.INFO)

    last_modified = os.path.getmtime(code_path)

    while True:
        current_modified = os.path.getmtime(code_path)
        if current_modified != last_modified:
            log("Detected changes. Submitting solution...", LogLevel.INFO)
            last_modified = current_modified

            with open(code_path, "r") as file:
                code = file.read()

            try:
                result = leetcode_api.submit_solution(problem_slug, code, language)
                process_submission_result(result)
                break
            except Exception as e:
                log(f"Submission failed: {e}", LogLevel.ERROR)
        time.sleep(1)


def process_submission_result(result):
    if result.get("status", {}).get("message") == "Accepted":
        log(
            f"🎉 Submission accepted! Runtime: {result['runtime']}, Memory: {result['memory']}",
            LogLevel.INFO,
        )
    else:
        log(f"Submission failed. Status: {result.get('status_msg')}", LogLevel.ERROR)
