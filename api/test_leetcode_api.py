import os
import unittest
import requests

from api.LeetCodeAPI import LeetCodeAPI

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class TestLeetCodeAPI(unittest.TestCase):

    def setUp(self):
        """
        Initializes the LeetCodeAPI instance with a real session and token.
        """
        # Initialize LeetCodeAPI with the live session
        self.leetcode_api = LeetCodeAPI()

        self.leetcode_api.session = requests.Session()
        self.leetcode_api.session.headers.update(
            {
                "Content-Type": "application/json",
            }
        )

        leetcode_session = os.getenv("LEETCODE_SESSION")
        if not leetcode_session:
            raise ValueError("❌ Missing LEETCODE_SESSION environment variable.")

        self.leetcode_api.session.cookies.set("LEETCODE_SESSION", leetcode_session)

    def test_fetch_company_questions(self):
        """
        Test the fetch_company_questions method for a real company.
        """
        company_slug = "amazon-thirty-days"  # Example slug for Amazon
        results = self.leetcode_api.fetch_company_questions(favorite_slug=company_slug)

        # Navigate to the questions in the actual response structure
        favorite_question_list = results.get("data", {}).get("favoriteQuestionList", {})
        self.assertIn("questions", favorite_question_list)
        questions = favorite_question_list.get("questions", [])

        # Ensure the results have questions
        self.assertGreater(len(questions), 0, "No questions returned for the company.")

    def test_fetch_company_questions_no_questions(self):
        """
        Test fetch_company_questions for a company that might have no questions.
        """
        company_slug = "nonexistent-company"  # Use a slug that doesn't exist
        results = self.leetcode_api.fetch_company_questions(favorite_slug=company_slug)

        # Navigate to the questions in the actual response structure
        favorite_question_list = results.get("data", {}).get("favoriteQuestionList", {})
        self.assertIn("questions", favorite_question_list)
        questions = favorite_question_list.get("questions", [])

        # Confirm no questions are returned
        self.assertEqual(
            len(questions), 0, "Questions were returned for a non-existent company."
        )

    def test_fetch_real_company_questions(self):
        """
        A more exploratory test to fetch all questions for a company.
        """
        company_slug = "microsoft-thirty-days"  # Example slug for Microsoft
        results = self.leetcode_api.fetch_company_questions(favorite_slug=company_slug)

        # Navigate to the questions in the actual response structure
        favorite_question_list = results.get("data", {}).get("favoriteQuestionList", {})
        self.assertIn("questions", favorite_question_list)
        questions = favorite_question_list.get("questions", [])

        # Ensure results have questions
        self.assertGreater(len(questions), 0)

    def test_fetch_company_names(self):
        """
        Test the fetch_company_names method.
        """
        company_names = self.leetcode_api.get_company_names()
        self.assertGreater(len(company_names), 0, "No company names returned.")

    def test_get_topic_tags(self):
        """
        Test the get_topic_tags method.
        """
        topic_tags = self.leetcode_api.get_topic_tags()
        self.assertGreater(len(topic_tags), 0, "No topic tags returned.")


if __name__ == "__main__":
    unittest.main()
