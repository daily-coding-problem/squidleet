from PracticeFactory import PracticeModeFactory

class PracticeModeManager:
    @staticmethod
    def handle(inputs):
        mode_handler = PracticeModeFactory.get_mode(inputs["practice_mode"])
        mode_handler.handle(inputs)
