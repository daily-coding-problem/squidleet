from modes.RandomProblemMode import RandomProblemMode
from modes.DailyChallengeMode import DailyChallengeMode
from modes.CustomPracticeMode import CustomPracticeMode
from modes.StudyPlanMode import StudyPlanMode


class PracticeModeHandler:
    @staticmethod
    def get_mode(selection_mode: str):
        if selection_mode == "random":
            return RandomProblemMode()
        elif selection_mode == "daily":
            return DailyChallengeMode()
        elif selection_mode == "custom":
            return CustomPracticeMode()
        elif selection_mode == "study-plan":
            return StudyPlanMode()
        else:
            raise ValueError(f"Unsupported mode: {selection_mode}")
