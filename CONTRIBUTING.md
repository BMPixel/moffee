# Contributing to moffee

Looking to contribute to moffee? **Here's how you can help.**

**This project is currently under active development**, so we welcome all sorts of new features, improvements, and bug reports/fixes! Please take a moment to review this document to make the contribution process easy and effective for everyone involved.

Following these guidelines helps communicate that you respect the time of the developers managing and developing this open-source project. In return, they should reciprocate that respect in addressing your issue or assessing patches and features.

## Using the issue tracker

The [issue tracker](https://github.com/bmpixel/moffee/issues) is the preferred channel for [bug reports](#bug-reports), [feature requests](#feature-requests), and [submitting pull requests](#pull-requests). Please respect the opinions of others and keep the discussion on topic.

## Bug reports

A bug is a _demonstrable problem_ caused by the code in the repository. Bug reports are extremely helpful, so thank you for submitting them!

Guidelines for bug reports:

1. **Use the GitHub issue search** — check if the issue has already been reported or fixed.

2. **Isolate the problem** — ideally, create a simple test case.

3. **Provide your test environment** — Moffee version, Python version, and perhaps the document that triggers problems.

## Feature requests

Feature requests are welcome. Take a moment to consider whether your idea fits with the scope and aims of the project. Please provide as much detail and context as possible.

## Pull requests

Good pull requests—patches, improvements, new features—are a fantastic help. They should remain focused in scope and avoid containing unrelated commits.

**Please ask first** before embarking on any significant pull request (e.g., implementing features, refactoring code, porting to a different language). Otherwise, you risk spending a lot of time working on something that the project's developers might not want to merge into the project.

Adhering to the following process is the best way to get your work included in the project:

1. [Fork](https://help.github.com/fork-a-repo/) the project, clone your fork, and configure the remotes:

   ```bash
   # Clone your fork of the repo into the current directory
   git clone https://github.com/<your-username>/moffee.git
   # Navigate to the newly cloned directory
   cd moffee
   # Assign the original repo to a remote called "upstream"
   git remote add upstream https://github.com/bmpixel/moffee.git
   ```

2. Get the latest changes from upstream. Then create a new topic branch (off the main branch) to contain your feature, change, or fix (best to name it issue#xxx):

   ```bash
   git checkout main
   git pull upstream main
   git checkout -b <topic-branch-name>
   ```

3. Set up the development environment. moffee uses [uv](https://docs.astral.sh/uv/) to manage dependencies:

    ```bash
    # Install project and dependencies
    uv sync --dev
    # Use 'uv run moffee' to call the CLI tool
    uv run moffee live your_example.md
    ```

4. It's coding time! moffee uses PEP 8 compatible code. Linters and formatters are defined as [pre-commit](https://pre-commit.com/) hooks in `.pre-commit-config.yaml`. To ensure a consistent code style, you can call the pre-commit hooks manually before commits:

    ```bash
    uv run pre-commit run --all-files
    ```

5. Test your code with [pytest](https://docs.pytest.org/en/stable/):

   ```bash
   uv run pytest
   ```

6. Locally merge (or rebase) the upstream development branch into your topic branch and push your topic branch to your fork:

   ```bash
   git pull [--rebase] upstream main
   git push origin <topic-branch-name>
   ```

7. [Open a Pull Request](https://help.github.com/articles/using-pull-requests/) with a clear title and description against the `main` branch.

## Understand the project

For your reference, `moffee/README.txt` shows the structure of the project and the purpose of each file. We hope this gives you a good start! You can also check the `tests` directory to see expected inputs and outputs for core functions.
