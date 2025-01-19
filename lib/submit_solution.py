import os
import requests
from typing import Dict, Any

from lib.fetch_problem import fetch_problem


def submit_solution(problem_slug: str, code: str, language: str) -> Dict[str, Any]:
    """
    Submit a solution to LeetCode.
    :param problem_slug: The slug of the problem to submit.
    :param code: The user's solution code.
    :param language: The programming language of the solution (e.g., "python3").
    """
    leetcode_session = os.getenv("LEETCODE_SESSION")
    if not leetcode_session:
        raise ValueError("❌ Missing LEETCODE_SESSION environment variable.")

    problem_details = fetch_problem(problem_slug)
    url = f"https://leetcode.com/problems/{problem_slug}/"

    headers = {
        "Content-Type": "application/json",
        "Cookie": f"LEETCODE_SESSION={leetcode_session}",
        "Referer": f"https://leetcode.com/problems/{problem_slug}/",
    }
    body = {
        "lang": language,
        "question_id": problem_details["questionId"],
        "typed_code": code,
    }

    response = requests.post(url, headers=headers, json=body)

    if not response.ok:
        raise Exception(f"❌ Failed to submit solution: {response.reason}")

    return response.json()
