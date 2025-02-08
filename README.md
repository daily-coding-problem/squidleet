# 🦑 SquidLeet [![Format Check](https://github.com/daily-coding-problem/squidleet/actions/workflows/format-check.yml/badge.svg)](https://github.com/daily-coding-problem/squidleet/actions/workflows/format-check.yml)

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?style=flat-square&logo=graphql&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/-Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![LeetCode](https://img.shields.io/badge/-LeetCode-FF4B00?style=flat-square&logo=leetcode&logoColor=white)

![squidleet](https://socialify.git.ci/daily-coding-problem/squidleet/image?language=1&forks=1&issues=1&name=1&owner=1&pattern=Circuit+Board&pulls=1&stargazers=1&theme=Dark)

Squidleet is a command-line LeetCode practice game that allows you to solve LeetCode problems in your terminal. It uses the LeetCode API to fetch problems and submit solutions. You can practice solving problems in your terminal without having to switch between the browser and the terminal.

## Features

- **Daily Challenge Integration**: Fetch and solve the LeetCode Daily Coding Challenge directly from the terminal.
- **Study Plan Mode**: Fetch random problems based on a specific study plan.
- **Random Problem Practice**: Get a randomly selected LeetCode problem to practice.
- **Company Mode**: Fetch random problems asked by a specific company over a given duration (e.g., last 30 days).
- **Specific Problem Mode**: Solve a specific problem by providing its problem slug.
- **Problem Fetching**: Added enhanced fetching capabilities, including filtering based on difficulty (e.g., `easy`, `medium`, `hard`) and more.
- **Submit Solutions**: Users can now directly submit their solutions to LeetCode from the terminal via a `submit_solution` function.
- **Custom Modes**: Support for specific practice workflows like random mode or custom problem-solving mode by providing slugs.
- **Editor Selection**: Integration with multiple editors, allowing configuration via CLI (e.g., `vim`, `nano`, and others).

## How It Works

Squidleet uses the LeetCode API to fetch problems and submit solutions. It provides a command-line interface that allows you to interact with the LeetCode platform without leaving your terminal. You can:

1. Fetch problems based on criteria like difficulty or tags.
2. Solve the **LeetCode Daily Challenge**.
3. Solve **random problems** or specific problems via their unique problem slug or study plan.
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

```text
Welcome to 🦑 SquidLeet!
🔐 Using authenticated session
Selected 📅 Daily Challenge Mode
🎯 Daily Coding Challenge:
📅 Date: 2025-01-19
🎯 Problem Selected: Trapping Rain Water II
✨ Difficulty: Hard
🔗 URL: https://leetcode.com/problems/trapping-rain-water-ii
🏷️ Tags: Array, Breadth-First Search, Heap (Priority Queue), Matrix
📈 Acceptance Rate: 55.04%
...
⏳ You have 45 min minutes to solve the problem. Good luck!
```

### Random Problem Mode

Solve a randomly selected LeetCode problem based on difficulty. Random Practice Mode allows you to solve a randomly selected LeetCode problem. Enhanced difficulty classification includes options such as `easy`, `medium`, `hard`, or a combination (e.g., `--difficulty easy,medium`).

```bash
python3 main.py --mode random --difficulty medium
```

Optional arguments:
- `--difficulty`: Choose between `easy`, `medium`, or `hard` or select multiple using comma-separated list (e.g., `easy,medium`).
- `--open-in-browser`: Opens the problem in a browser window.
- `--editor`: Specify a code editor for writing solutions. Supported editors: `default`, `vim`, `nano`, etc.

```text
Welcome to 🦑 SquidLeet!
🔐 Using authenticated session
Selected 🎲 Random Problem Mode
🎯 Problem Selected: Shortest Distance in a Plane
✨ Difficulty: Medium
🔗 URL: https://leetcode.com/problems/shortest-distance-in-a-plane
🏷️ Tags: Database
📈 Acceptance Rate: 61.29%
...
⏳ You have 45 min minutes to solve the problem. Good luck!
```

### Custom Mode

Custom Modes enable solving specific problems or sets of problems by providing one or multiple problem slugs (e.g., `--problems two-sum,three-sum`).

```bash
python3 main.py --mode custom --problems two-sum
```

Optional arguments:
- `--open-in-browser`: Opens the problem in a browser window.
- `--editor`: Specify the preferred code editor (e.g., `vim`, `nano`). Default is the system-configured default editor.

```text
Welcome to 🦑 SquidLeet!
🔐 Using authenticated session
Selected 🧩 Custom Practice Mode
🎯 Problem Selected: Two Sum
✨ Difficulty: Easy
🔗 URL: https://leetcode.com/problems/two-sum
🏷️ Tags: Array, Hash Table
📈 Acceptance Rate: 54.67%
...
⏳ You have 45 min minutes to solve the problem. Good luck!
```

### Study Plan Mode

Study Plan Mode allows you to fetch random problems based on a specific study plan. You can specify the study plan name to fetch problems from that plan.

```bash
python3 main.py --mode study-plan --plan-name top-interview-150
```

Optional arguments:
- `--open-in-browser`: Opens the problem in a browser window.
- `--editor`: Specify the preferred code editor (e.g., `vim`, `nano`). Default is the system-configured default editor.

```text
Welcome to 🦑 SquidLeet!
🔐 Using authenticated session
Selected 🎯 Study Plan Mode: top-interview-150
🎯 Problem Selected: Game of Life
✨ Difficulty: Medium
🔗 URL: https://leetcode.com/problems/game-of-life
🏷️ Tags: Array, Matrix, Simulation
📈 Acceptance Rate: 70.65%
...
⏳ You have 45 min minutes to solve the problem. Good luck!
```

### Company Mode

Company Mode allows you to fetch random problems asked by a specific company.

⚠️ **Note**: This mode requires the `--leetcode-session` argument to be set with a valid LeetCode session cookie. This is because the company-specific problem data is not available publicly and requires a valid [LeetCode Premium](https://leetcode.com/subscribe) subscription.

```bash
python3 main.py --practice-mode company --company-name microsoft --duration thirty-days
```

Optional arguments:
- `--open-in-browser`: Opens the problem in a browser window.
- `--editor`: Specify the preferred code editor (e.g., `vim`, `nano`). Default is the system-configured default editor.
- `--difficulty`: Choose between `easy`, `medium`, or `hard` or select multiple using comma-separated list (e.g., `easy,medium`).
- `--tags`: Filter problems based on tags. Example usage: `--tags Array,Hash Table`.
- `--duration`: Fetch the problems asked by the company over a given span of time. Valid values: `thirty-days`, `three-months`, `six-months`, `more-than-six-months`, or `all`. Default is `all`.

```text
Welcome to 🦑 SquidLeet!
🔐 Using authenticated session
Selected 👔 Company Mode: Top Questions asked at Microsoft in the last 30 days
🎯 Problem Selected: Maximum Length of a Concatenated String with Unique Characters
✨ Difficulty: Medium
🔗 URL: https://leetcode.com/problems/maximum-length-of-a-concatenated-string-with-unique-characters
🏷️ Tags: Array, String, Backtracking, Bit Manipulation
📈 Acceptance Rate: 54.2%
...
⏳ You have 45 min minutes to solve the problem. Good luck!
```

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

## 🐳 Docker

You can run Squidleet using Docker. Below are the steps to set up and run the application using Docker.

### Build Docker Image

Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/daily-coding-problem/squidleet.git
cd squidleet
```

Build the Docker image:
```bash
docker build -t squidleet .
```

### Run the Docker Container

Run the Docker container and mount the directory where your environment file (`.env`) is located:
```bash
docker run --rm -it --env-file .env squidleet
```

To specify additional options (e.g., modes), append them to the run command:
```bash
docker run --rm -it --env-file .env squidleet --mode daily
```

### Using Docker Compose

If you prefer using Docker Compose, you can create a `docker-compose.yml` file with the following content:

```yaml
version: "3.8"
services:
  squidleet:
    build: .
    environment:
      - LEETCODE_SESSION=<your_session_cookie>
    stdin_open: true
    tty: true
    command: ["--mode", "daily"]
```

To run the container:
```bash
docker-compose up
```

## License

Squidleet is open-sourced under the MIT License. See the `LICENSE` file for more details.
