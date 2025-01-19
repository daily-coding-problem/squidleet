from handlers.PracticeHandler import PracticeModeHandler


def handle(inputs):
    mode_handler = PracticeModeHandler.get_mode(inputs["practice_mode"])
    mode_handler.handle(inputs)
