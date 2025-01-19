import os
import random

import requests
from typing import List, Dict, Any, Optional


# TODO: Need to verify how `fetchProblems` functions with multiple difficulty levels.
# TODO: Need to add tests to tests/.

def fetch_problems(limit: int = 50, skip: int = 0, difficulties: List[str] = None) -> List[Dict[str, Any]]:
    """
    Fetch a list of problems from LeetCode.
    :param limit: Number of problems to fetch.
    :param skip: Offset for pagination.
    :param difficulties: Difficulty levels of the problems (e.g., "Easy", "Medium", "Hard").
    """
    leetcode_session = os.getenv("LEETCODE_SESSION")
    if not leetcode_session:
        raise ValueError("❌ Missing LEETCODE_SESSION environment variable.")

    if limit < 1 or skip < 0:
        raise ValueError("❌ Limit must be positive and skip must be non-negative.")

    url = "https://leetcode.com/graphql"
    query = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
      problemsetQuestionList: questionList(
        categorySlug: $categorySlug,
        limit: $limit,
        skip: $skip,
        filters: $filters
      ) {
        total: totalNum
        questions: data {
          acRate
          difficulty
          content
          frontendQuestionId: questionFrontendId
          title
          titleSlug
          topicTags {
            name
            id
            slug
          }
        }
      }
    }
    """

    headers = {
        "Content-Type": "application/json",
        "Cookie": f"LEETCODE_SESSION={leetcode_session}",
    }
    variables = {
        "categorySlug": "all",
        "limit": limit,
        "skip": skip,
        "filters": {"difficulty": difficulties or []},
    }
    response = requests.post(url, headers=headers, json={"operationName": "problemsetQuestionList", "variables": variables, "query": query})

    if not response.ok:
        raise Exception(f"❌ Failed to fetch problems: {response.reason}")

    data = response.json()
    questions = data.get("data", {}).get("problemsetQuestionList", {}).get("questions")

    if not questions:
        raise Exception("❌ No problems were returned.")

    return questions

def get_random_problem(difficulties: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
    """
    Get a random problem from LeetCode.
    :param difficulties: Difficulty levels of the problems (e.g., "Easy", "Medium", "Hard").
    :return: A random problem dictionary or None if no problems are found.
    """
    problems = fetch_problems(limit=1000, difficulties=difficulties)

    if not problems:
        return None

    random_index = random.randint(0, len(problems) - 1)
    return problems[random_index]
