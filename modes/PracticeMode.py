import random
import html2text
import markdown

from typing import List, Dict, Any, Optional

from utils.logger import log, LogLevel

from handlers.SolutionHandler import SolutionHandler
from handlers.CacheHandler import cached_api


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


def create_and_solve_handler(problem_slug, code_snippets, difficulty_label, args):
    # Determine the starter code based on the chosen language

    code = ""
    for item in code_snippets:
        if item.get("lang").lower() == args["language"].lower():
            code = item.get("code")
            break

    if not code:
        log(
            f"Starter code not found for language: {args['language']}",
            LogLevel.ERROR,
        )
        return

    handler = SolutionHandler(
        problem=problem_slug,
        code=code,
        difficulty=difficulty_label,
        editor=args["editor"],
        language=args["language"],
        time_limit=args["time_limit"],
    )
    handler.solve()


def open_in_browser(url, open_flag):
    if open_flag:
        import webbrowser

        webbrowser.open(url)


def log_problem_details(problem, difficulty_label, url):
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

    # Assuming `content` is the Markdown content
    content = problem.get("content")
    if content:
        try:
            html_content = markdown.markdown(content)

            text_maker = html2text.HTML2Text()
            text_maker.ignore_links = True
            plain_text = text_maker.handle(html_content)

            log(plain_text, LogLevel.INFO)
        except Exception as e:
            log(f"Failed to convert problem content: {str(e)}", LogLevel.ERROR)


class PracticeMode:
    def __init__(self):
        pass

    def handle(self, args):
        raise NotImplementedError("This method should be implemented by subclasses.")
