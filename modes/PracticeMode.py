import html2text
import markdown

from utils.logger import log, LogLevel

from handlers.SolutionHandler import SolutionHandler


def create_and_solve_handler(problem_slug, code_snippets, difficulty_label, args):
    # Determine the starter code based on the chosen language

    code = ""
    for item in code_snippets:
        if item.get("lang").lower() == args["language"].lower():
            code = item.get("code")
            break

    if not code:
        log(
            f"Starter code not found for language: {args['language']}",
            LogLevel.ERROR,
        )
        return

    handler = SolutionHandler(
        problem=problem_slug,
        code=code,
        difficulty=difficulty_label,
        editor=args["editor"],
        language=args["language"],
        time_limit=args["time_limit"],
    )
    handler.solve()


def open_in_browser(url, open_flag):
    if open_flag:
        import webbrowser

        webbrowser.open(url)


def log_problem_details(problem, difficulty_label, url):
    log(f"🎯 Problem Selected: {problem.get('title', 'Unknown')}", LogLevel.INFO)
    log(f"✨ Difficulty: {difficulty_label}", LogLevel.INFO)
    log(f"🔗 URL: {url}", LogLevel.INFO)

    topic_tags = problem.get("topicTags", [])
    if topic_tags:
        tags = ", ".join(tag.get("name", "Unknown") for tag in topic_tags)
        log(f"🏷️ Tags: {tags}", LogLevel.INFO)

    ac_rate = problem.get("acRate")
    if ac_rate is not None:
        log(f"📈 Acceptance Rate: {ac_rate:.2f}%", LogLevel.INFO)

    # Assuming `content` is the Markdown content
    content = problem.get("content")
    if content:
        try:
            html_content = markdown.markdown(content)

            text_maker = html2text.HTML2Text()
            text_maker.ignore_links = True
            plain_text = text_maker.handle(html_content)

            log(plain_text, LogLevel.INFO)
        except Exception as e:
            log(f"Failed to convert problem content: {str(e)}", LogLevel.ERROR)


class PracticeMode:
    def __init__(self):
        pass

    def handle(self, args):
        raise NotImplementedError("This method should be implemented by subclasses.")
