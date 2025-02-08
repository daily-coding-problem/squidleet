import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional

import requests


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
              title
              titleSlug
              codeSnippets {
                lang
                code
              }
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
              content
              acRate
              difficulty
              codeSnippets {
                lang
                code
              }
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
                title
                titleSlug
                content
                acRate
                difficulty
                codeSnippets {
                    lang
                    code
                }
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
            description
            planSubGroups {
              slug
              name
              questionNum
              questions {
                title
                titleSlug
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

    def fetch_company_questions(
        self,
        favorite_slug: str,
        skip: int = 0,
        limit: int = 100,
        frequency_filter: dict = None,
        difficulty_filter: dict = None,
        topic_filter: dict = None,
        filter_combine_type: str = "ALL",
        sort_by: dict = None,
    ):
        """
        Fetch filtered and sorted questions for a specific company using the company's GraphQL slug.

        :param favorite_slug: The slug for the company (e.g., 'amazon-thirty-days').
        :param skip: Number of questions to skip in pagination (default is 0).
        :param limit: Maximum number of questions to fetch (default is 100).
        :param frequency_filter: A dictionary for frequency filters, e.g., {"rangeLeft": 90, "rangeRight": 100}.
        :param difficulty_filter: A dictionary for difficulty filters, e.g.,
                                  {"difficulties": ["MEDIUM"], "operator": "IS"}.
                                  Operators include "IS" and "IS_NOT".
        :param topic_filter: A dictionary for topic filters, e.g.,
                             {"topicSlugs": ["dynamic-programming"], "operator": "IS_NOT"}.
                             Operators include "IS" and "IS_NOT".
        :param filter_combine_type: Filter combination type, either "ALL" or "ANY" (default is "ALL").
        :param sort_by: A dictionary for sorting, e.g., {"sortField": "FREQUENCY", "sortOrder": "ASCENDING"}.
        :return: Questions and metadata as returned by the API.
        """

        # Validate filter combine type
        valid_combine_types = ["ALL", "ANY"]
        if filter_combine_type not in valid_combine_types:
            raise ValueError(
                f"Invalid filterCombineType: {filter_combine_type}. Must be one of {valid_combine_types}."
            )

        # Validate sort_by
        valid_sort_fields = ["FREQUENCY", "CUSTOM", "DIFFICULTY", "ACCEPTANCE", "TITLE"]
        if sort_by is not None:
            if sort_by.get("sortField", "") not in valid_sort_fields:
                raise ValueError(
                    f"Invalid sortField: {sort_by.get('sortField')}. Must be one of {valid_sort_fields}."
                )
            if sort_by.get("sortOrder", "") not in ["ASCENDING", "DESCENDING"]:
                raise ValueError(
                    "Invalid sortOrder: Must be 'ASCENDING' or 'DESCENDING'."
                )

        if difficulty_filter:
            # force each difficulty to uppercase
            difficulty_filter["difficulties"] = [
                diff.upper() for diff in difficulty_filter["difficulties"]
            ]

        # Default operators for filters
        default_operator = {"operator": "IS"}

        # Build the filters dynamically with proper operators
        filters_v2 = {
            "filterCombineType": filter_combine_type,
            "statusFilter": {"questionStatuses": [], **default_operator},
            "difficultyFilter": difficulty_filter
            or {"difficulties": [], **default_operator},
            "topicFilter": topic_filter or {"topicSlugs": [], **default_operator},
            "frequencyFilter": frequency_filter
            or {},  # No operator for frequencyFilter
            # There are more filters available, but we're not using them in squidleet yet
        }

        query = """
        query favoriteQuestionList(
            $favoriteSlug: String!, $filtersV2: QuestionFilterInput,
            $sortBy: QuestionSortByInput, $limit: Int, $skip: Int, $version: String = "v2"
        ) {
          favoriteQuestionList(
            favoriteSlug: $favoriteSlug
            filtersV2: $filtersV2
            sortBy: $sortBy
            limit: $limit
            skip: $skip
            version: $version
          ) {
            questions {
              difficulty
              id
              paidOnly
              questionFrontendId
              status
              title
              titleSlug
              translatedTitle
              isInMyFavorites
              frequency
              acRate
              topicTags {
                name
                nameTranslated
                slug
              }
            }
            totalLength
            hasMore
          }
        }
        """

        payload = {
            "query": query,
            "variables": {
                "skip": skip,
                "limit": limit,
                "favoriteSlug": favorite_slug,
                "filtersV2": filters_v2,
                "sortBy": sort_by
                or {"sortField": "CUSTOM", "sortOrder": "ASCENDING"},  # Default sort
            },
            "operationName": "favoriteQuestionList",
        }

        response = self.session.post(self.url, json=payload)
        if not response.ok:
            raise Exception(f"❌ Failed to fetch company questions: {response.content}")

        return response.json()

    def get_company_names(self):
        """
        Fetches the list of company names and their corresponding slugs from the LeetCode API.

        :return: A list of dictionaries containing company `name` and `slug`.
        """
        query = """
        query problemsetCompanyTags {
            problemsetCompanyTags {
                name
                slug
            }
        }
        """

        payload = {
            "query": query,
            "variables": {},
            "operationName": "problemsetCompanyTags",
        }

        response = self.session.post(self.url, json=payload)

        if not response.ok:
            raise Exception(f"❌ Failed to fetch company names: {response.content}")

        # Return company names and slugs
        data = response.json()
        return data.get("data", {}).get("problemsetCompanyTags", [])

    def get_topic_tags(self):
        """
        Fetch the set of all topic tags available in LeetCode.

        :return: set: A set of topic tag names.
        """
        query = """
        query questionTopicTags {
          questionTopicTags {
            edges {
              node {
                id
                name
                slug
                translatedName
                questionIds
              }
            }
          }
        }
        """
        payload = {
            "query": query,
            "variables": {},
            "operationName": "questionTopicTags",
        }

        response = self.session.post(self.url, json=payload)

        if not response.ok:
            raise Exception(f"❌ Failed to fetch topic tags: {response.content}")

        # Extract relevant data from response
        data = response.json()
        edges = data.get("data", {}).get("questionTopicTags", {}).get("edges", [])
        topic_tags = {edge["node"]["name"] for edge in edges if edge.get("node")}
        return topic_tags
