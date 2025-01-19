from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor

import requests
import os


class LeetCodeAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
            }
        )

        leetcode_session = os.getenv("LEETCODE_SESSION")
        if not leetcode_session:
            raise ValueError("❌ Missing LEETCODE_SESSION environment variable.")

        self.session.cookies.set("LEETCODE_SESSION", leetcode_session)
        self.url = "https://leetcode.com/graphql"

    def fetch_problems(
        self,
        limit: int = 50,
        skip: int = 0,
        difficulties: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch a list of problems from LeetCode.
        :param limit: Number of problems to fetch.
        :param skip: Offset for pagination.
        :param difficulties: List of difficulty levels (e.g., ["Easy", "Medium", "Hard"]).
        :return: A list of problem dictionaries.
        """
        if limit < 1 or skip < 0:
            raise ValueError("❌ Limit must be positive and skip must be non-negative.")

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

        # Helper function for fetching problems for a single difficulty
        def fetch_for_difficulty(difficulty: str) -> List[Dict[str, Any]]:
            difficulty_enum = {"easy": "EASY", "medium": "MEDIUM", "hard": "HARD"}

            if difficulty.lower() not in difficulty_enum:
                return []

            filters = {"difficulty": difficulty_enum.get(difficulty.lower())}
            variables = {
                "categorySlug": "all-code-essentials",
                "limit": limit,
                "skip": skip,
                "filters": filters,
            }

            response = self.session.post(
                self.url,
                json={
                    "operationName": "problemsetQuestionList",
                    "variables": variables,
                    "query": query,
                },
            )

            if not response.ok:
                raise Exception(f"❌ Failed to fetch problems: {response.content}")

            data = response.json()
            return (
                data.get("data", {})
                .get("problemsetQuestionList", {})
                .get("questions", [])
            )

        # Execute the fetches in parallel if multiple difficulties are provided
        if difficulties:
            with ThreadPoolExecutor() as executor:
                # Create tasks for all difficulties
                results = list(executor.map(fetch_for_difficulty, difficulties))

            # Flatten the results
            return [problem for result in results for problem in result]

        # If no difficulties are provided, fetch without any difficulty filtering
        return fetch_for_difficulty("easy")  # Default difficulty or unfiltered

    def fetch_daily_challenge(self) -> Dict[str, Any]:
        """
        Fetch details for the LeetCode Daily Coding Challenge.
        :return: A dictionary containing the daily challenge details.
        """
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
              content
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

        response = self.session.post(
            self.url,
            json={"operationName": "questionOfToday", "variables": {}, "query": query},
        )

        if not response.ok:
            raise Exception(f"❌ Failed to fetch daily challenge: {response.content}")

        data = response.json()
        daily_challenge = data.get("data", {}).get("activeDailyCodingChallengeQuestion")

        if not daily_challenge:
            raise Exception("❌ Failed to retrieve daily challenge details.")

        return daily_challenge

    def fetch_problem(self, problem_slug: str) -> Dict[str, Any]:
        """
        Fetch problem details from LeetCode.
        :param problem_slug: The slug of the LeetCode problem (e.g., "two-sum").
        :return: A dictionary containing the problem details.
        """
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

        response = self.session.post(
            self.url,
            json={
                "operationName": "getQuestionDetails",
                "variables": {"titleSlug": problem_slug},
                "query": query,
            },
        )

        if not response.ok:
            raise Exception(f"❌ Failed to fetch problem details: {response.content}")

        data = response.json()
        question = data.get("data", {}).get("question")

        if not question:
            raise Exception(f"❌ Problem not found for slug: {problem_slug}")

        return question

    def get_study_plan(self, slug: str) -> Dict[str, Any]:
        """
        Fetch study plan details from LeetCode.
        :param slug: The slug of the study plan (e.g., "leetcode-75").
        :return: A dictionary containing the study plan details.
        """
        query = """
        query studyPlanDetail($slug: String!) {
          studyPlanV2Detail(planSlug: $slug) {
            slug
            name
            highlight
            staticCoverPicture
            colorPalette
            threeDimensionUrl
            description
            premiumOnly
            needShowTags
            awardDescription
            defaultLanguage
            award {
              name
              config {
                icon
                iconGif
                iconGifBackground
              }
            }
            relatedStudyPlans {
              cover
              highlight
              name
              slug
              premiumOnly
            }
            planSubGroups {
              slug
              name
              premiumOnly
              questionNum
              questions {
                translatedTitle
                titleSlug
                title
                questionFrontendId
                paidOnly
                id
                difficulty
                hasOfficialSolution
                topicTags {
                  slug
                  name
                }
                solutionInfo {
                  solutionSlug
                  solutionTopicId
                }
              }
            }
          }
        }
        """

        variables = {"slug": slug}

        response = self.session.post(
            self.url,
            json={
                "operationName": "studyPlanDetail",
                "variables": variables,
                "query": query,
            },
        )

        if not response.ok:
            raise Exception(f"❌ Failed to fetch study plan: {response.content}")

        data = response.json()
        study_plan = data.get("data", {}).get("studyPlanV2Detail")

        if not study_plan:
            raise Exception(f"❌ Study plan not found for slug: {slug}")

        return study_plan

    def submit_solution(
        self, problem_slug: str, code: str, language: str
    ) -> Dict[str, Any]:
        """
        Submit a solution to LeetCode.
        :param problem_slug: The slug of the problem to submit.
        :param code: The user's solution code.
        :param language: The programming language of the solution (e.g., "python3").
        :return: A dictionary containing the submission result.
        """
        problem_details = self.fetch_problem(problem_slug)
        url = f"https://leetcode.com/problems/{problem_slug}/"

        headers = {
            "Referer": f"https://leetcode.com/problems/{problem_slug}/",
        }
        body = {
            "lang": language,
            "question_id": problem_details["questionId"],
            "typed_code": code,
        }

        response = self.session.post(url, headers=headers, json=body)

        if not response.ok:
            raise Exception(f"❌ Failed to submit solution: {response.content}")

        return response.json()
