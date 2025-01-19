import os
import requests
from typing import Dict, Any

def fetch_daily_challenge() -> Dict[str, Any]:
    """
    Fetch details for the LeetCode Daily Coding Challenge.
    """
    leetcode_session = os.getenv("LEETCODE_SESSION")
    if not leetcode_session:
        raise ValueError("❌ Missing LEETCODE_SESSION environment variable.")

    url = "https://leetcode.com/graphql"
    query = """
    query questionOfToday {
      activeDailyCodingChallengeQuestion {
        date
        userStatus
        link
        question {
          titleSlug
          title
          translatedTitle
          acRate
          difficulty
          freqBar
          frontendQuestionId: questionFrontendId
          isFavor
          paidOnly: isPaidOnly
          status
          hasVideoSolution
          hasSolution
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
    response = requests.post(url, headers=headers, json={"operationName": "questionOfToday", "variables": {}, "query": query})

    if not response.ok:
        raise Exception(f"❌ Failed to fetch daily challenge: {response.reason}")

    data = response.json()
    daily_challenge = data.get("data", {}).get("activeDailyCodingChallengeQuestion")

    if not daily_challenge:
        raise Exception("❌ Failed to retrieve daily challenge details.")

    return daily_challenge
