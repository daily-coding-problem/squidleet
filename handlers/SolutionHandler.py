import subprocess

from handlers.file_handler import create_solution_file
from utils.editor_resolver import resolve_editor_command
from utils.logger import LogLevel, log
from utils.watch_and_submit import setup_file_watcher


def _open_in_editor(editor, file_path):
    open_command = resolve_editor_command(editor, file_path)
    try:
        subprocess.run(open_command, check=True, shell=True)
        log(f"📂 Opened {file_path} in the editor.", LogLevel.INFO)
    except subprocess.CalledProcessError as e:
        log(f"❌ Failed to open file in the editor: {e}", LogLevel.ERROR)


class SolutionHandler:
    def __init__(self, problem, difficulty, editor, language, time_limit):
        self.problem = problem
        self.difficulty = difficulty
        self.editor = editor
        self.language = language
        self.time_limit = time_limit

    def solve(self):
        code_path = self._create_file(self.language)
        _open_in_editor(self.editor, code_path)
        self._setup_watcher(code_path, self.language, self.time_limit)

    def _create_file(self, language):
        code_path = create_solution_file(self.problem, language)
        log(f"📂 Template created: {code_path}", LogLevel.INFO)
        return code_path

    def _setup_watcher(self, file_path, language, time_limit):
        setup_file_watcher(file_path, self.problem, language, time_limit)
        log(f"⏳ You have {time_limit} minutes to solve the problem. Good luck!", LogLevel.INFO)
        log(f"✨ Difficulty Level: {self.difficulty}", LogLevel.INFO)
