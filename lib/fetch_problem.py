import os
import requests
from typing import Dict, Any


def fetch_problem(problem_slug: str) -> Dict[str, Any]:
    """
    Fetch problem details from LeetCode.
    :param problem_slug: The slug of the LeetCode problem (e.g., "two-sum").
    """
    leetcode_session = os.getenv("LEETCODE_SESSION")
    if not leetcode_session:
        raise ValueError("❌ Missing LEETCODE_SESSION environment variable.")

    url = "https://leetcode.com/graphql"
    query = """
    query getQuestionDetails($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        title
        titleSlug
        content
        acRate
        difficulty
        topicTags {
          name
          id
          slug
        }
      }
    }
    """

    headers = {
        "Content-Type": "application/json",
        "Cookie": f"LEETCODE_SESSION={leetcode_session}",
    }
    response = requests.post(
        url,
        headers=headers,
        json={
            "operationName": "getQuestionDetails",
            "variables": {"titleSlug": problem_slug},
            "query": query,
        },
    )

    if not response.ok:
        raise Exception(f"❌ Failed to fetch problem details: {response.reason}")

    data = response.json()
    question = data.get("data", {}).get("question")

    if not question:
        raise Exception(f"❌ Problem not found for slug: {problem_slug}")

    return question
