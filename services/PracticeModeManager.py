from PracticeFactory import PracticeModeFactory


def handle(inputs):
    mode_handler = PracticeModeFactory.get_mode(inputs["practice_mode"])
    mode_handler.handle(inputs)
