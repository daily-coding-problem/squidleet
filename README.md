# 🦑 SquidLeet [![Format Check](https://github.com/daily-coding-problem/squidleet/actions/workflows/format-check.yml/badge.svg)](https://github.com/daily-coding-problem/squidleet/actions/workflows/format-check.yml)

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/-Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?style=flat-square&logo=graphql&logoColor=white)
![LeetCode](https://img.shields.io/badge/-LeetCode-FF4B00?style=flat-square&logo=leetcode&logoColor=white)

![squidleet](https://socialify.git.ci/daily-coding-problem/squidleet/image?description=1&forks=1&issues=1&name=1&owner=1&pattern=Circuit+Board&pulls=1&stargazers=1&theme=Dark)

Squidleet is a command-line LeetCode practice game that allows you to solve LeetCode problems in your terminal. It uses the LeetCode API to fetch problems and submit solutions. You can practice solving problems in your terminal without having to switch between the browser and the terminal.

## Features

- **Daily Challenge Integration**: Fetch and solve the LeetCode Daily Coding Challenge directly from the terminal.
- **Random Problem Practice**: Get a randomly selected LeetCode problem to practice.
- **Specific Problem Mode**: Solve a specific problem by providing its problem slug.
- **Problem Fetching**: Added enhanced fetching capabilities, including filtering based on difficulty (e.g., `easy`, `medium`, `hard`) and more.
- **Submit Solutions**: Users can now directly submit their solutions to LeetCode from the terminal via a `submit_solution` function.
- **Custom Modes**: Support for specific practice workflows like random mode or custom problem-solving mode by providing slugs.
- **Editor Selection**: Integration with multiple editors, allowing configuration via CLI (e.g., `vim`, `nano`, and others).

## How It Works

Squidleet uses the LeetCode API to fetch problems and submit solutions. It provides a command-line interface that allows you to interact with the LeetCode platform without leaving your terminal. You can:

1. Fetch problems based on criteria like difficulty or tags.
2. Solve the **LeetCode Daily Challenge**.
3. Solve **random problems** or specific problems via their unique problem slug.
4. Write solutions with your preferred code editor and submit them directly from the terminal.
5. Open problem links in your browser if preferred.

Additionally, Squidleet provides an interactive CLI experience with options for configuring your practice workflow.

## Installation and Configuration

You can install `squidleet` using `pip`:

```bash
git clone https://github.com/daily-coding-problem/squidleet.git
cd squidleet
python3 -m venv .venv
pip install -r requirements.txt
```

## Usage

Squidleet offers multiple modes and configuration options for practicing LeetCode problems effectively, catering to various workflows. Below are commands to get started:

### Daily Challenge Mode

Daily Challenge Mode allows you to fetch and solve the LeetCode Daily Challenge directly from the terminal.

```bash
python3 main.py --mode daily
```

Optional arguments:
- `--open-in-browser`: Opens the challenge in a browser window.
- `--editor`: Open the code editor to write solutions. Supported editors include `default`, `vim`, `nano`, and others. Example usage: `--editor vim`

### Random Problem Mode

Solve a randomly selected LeetCode problem based on difficulty.
Random Practice Mode allows you to solve a randomly selected LeetCode problem. Enhanced difficulty classification includes options such as `easy`, `medium`, `hard`, or a combination (e.g., `--difficulty easy,medium`).
```bash
python3 main.py --mode random --difficulty medium
```

Optional arguments:
- `--difficulty`: Choose between `easy`, `medium`, or `hard` or select multiple using comma-separated list (e.g., `easy,medium`).
- `--open-in-browser`: Opens the problem in a browser window.
- `--editor`: Specify a code editor for writing solutions. Supported editors: `default`, `vim`, `nano`, etc.
- `--editor`: Open the code editor to write solutions. (e.g., `--editor code` or `--editor vim`)

### Custom Mode

Custom Modes enable solving specific problems or sets of problems by providing one or multiple problem slugs (e.g., `--problems two-sum,three-sum`).

```bash
python3 main.py --mode custom --problems two-sum
```

- `--open-in-browser`: Opens the problem in a browser window.
- `--editor`: Specify the preferred code editor (e.g., `vim`, `nano`). Default is the system-configured default editor.
- `--open-in-browser`: Opens the problem in a browser window.
- `--editor`: Open the code editor to write solutions. (e.g., `--editor code` or `--editor vim`)

## Configurations
Squidleet uses a `LEETCODE_SESSION` cookie for authentication. Setting the `LEETCODE_SESSION` environment variable is necessary for all operations, including fetching and submitting problems.

### `LEETCODE_SESSION` Cookie

#### Extracting `LEETCODE_SESSION`  🍪 Cookie

To obtain the `LEETCODE_SESSION` cookie, follow these steps:

1. **Login to LeetCode**: Open the LeetCode website and log in to your account.
2. **Open Developer Tools**: Press `F12` or right-click and select `Inspect` to bring up the browser's Developer Tools.
3. **Locate Cookies**: In the `Application` tab, expand the `Cookies` section and click on `https://leetcode.com`.
4. **Copy `LEETCODE_SESSION`**: Locate the `LEETCODE_SESSION` cookie in the table and copy its value.

Set the cookie value as an environment variable `.env`:

```bash
LEETCODE_SESSION=<your_session_cookie>
```

### Logs

Squidleet exposes two environment variables for logging:

- `LOG_LEVEL`: Set the log level for the application. Default is `INFO`.
- `SHOW_DETAILED_LOGS`: Enable detailed logs for debugging purposes. Default is `False`.

These can also be set via arguments in the CLI:

```bash
python3 main.py --mode daily --log-level INFO --show-detailed-logs
```

## License

Squidleet is open-sourced under the MIT License. See the `LICENSE` file for more details.
