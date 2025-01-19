import os
import json
from utils.logger import log, LogLevel

problem_count_file_path = "/tmp/squidleet-problem-count.json"
default_problem_count = {"easy": 0, "medium": 0, "hard": 0}

score = 0
streak = 0

def load_problem_count():
    try:
        if not os.path.exists(problem_count_file_path):
            with open(problem_count_file_path, "w") as file:
                json.dump(default_problem_count, file, indent=2)
            return default_problem_count

        with open(problem_count_file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        log(f"Failed to load problem count: {str(e)}", LogLevel.ERROR)
        return default_problem_count

def update_problem_count(difficulty, count):
    try:
        problem_count = load_problem_count()

        if difficulty not in problem_count:
            log(f"Invalid difficulty: {difficulty}", LogLevel.WARN)
            return

        if count < 0:
            log(f"Problem count cannot be negative for '{difficulty}'.", LogLevel.WARN)
            return

        problem_count[difficulty] = count

        with open(problem_count_file_path, "w") as file:
            json.dump(problem_count, file, indent=2)

        log(f"Problem count updated: {difficulty} = {count}", LogLevel.INFO)
    except Exception as e:
        log(f"Failed to update problem count: {str(e)}", LogLevel.ERROR)

def update_score(difficulty, completed_in_time):
    global score, streak
    base_points = {"easy": 10, "medium": 20, "hard": 30}

    try:
        problem_count = load_problem_count()

        if difficulty not in problem_count:
            log(f"Invalid difficulty: {difficulty}", LogLevel.WARN)
            return

        current_count = problem_count[difficulty]

        if current_count <= 0:
            log(f"No more problems available for difficulty '{difficulty}'.", LogLevel.WARN)
            return

        rarity_factor = 50 / current_count if current_count else 1
        streak_multiplier = 1 + streak * 0.1
        points = round(base_points[difficulty] * rarity_factor * streak_multiplier)

        score += points
        streak = streak + 1 if completed_in_time else 0

        update_problem_count(difficulty, current_count - 1)

        log(f"🏆 Score: {score}, 🔥 Streak: {streak} (+{points} points), ✨ Difficulty: {difficulty}", LogLevel.INFO)
    except Exception as e:
        log(f"Error updating score for difficulty '{difficulty}': {str(e)}", LogLevel.ERROR)
