from services import CommandParser, SessionManager, InputsCollector, PracticeModeManager
from utils.logger import log, LogLevel


def main():
    try:
        # Parse CLI options
        cli_options = CommandParser.parse()

        # Validate and set the LeetCode session token
        SessionManager.initialize(cli_options)

        log("Welcome to 🦑 SquidLeet!", LogLevel.INFO)

        # Collect & validate inputs and detect practice mode
        inputs = InputsCollector.collect(cli_options)

        # Handle the selected practice mode
        PracticeModeManager.handle(inputs)
    except Exception as e:
        log(f"Error: {str(e)}", LogLevel.ERROR)
        exit(1)


if __name__ == "__main__":
    main()
