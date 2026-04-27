# Contributing to NBS LLM CLassifier

Thank you for your interest in contributing to the NBS LLM Classifier project! We welcome contributions from internal and NSO colleagues to help improve the codebase, documentation, and overall project quality.

## Reporting Issues
- If you find a bug, have a question, or want to suggest an improvement, **please raise an issue** in the repository.
- When raising an issue, provide as much detail as possible, including:
  - A clear description of the problem or suggestion
  - Steps to reproduce (if applicable)
  - Any relevant error messages or screenshots

## Making Code Contributions
- Please **create a new branch** from `main` for your work (no need to fork).
- You are welcome to open a branch and raise a pull request (PR) for any improvements, bug fixes, or new features.
- When opening a PR, please ensure you:
  - Clearly describe **what** you are merging and **why**
  - Reference any related issues (if applicable)
  - Provide enough context and detail for reviewers to understand your changes
  - Follow the existing code style and structure (see below)
  - Add or update tests as appropriate

## Workflow
1. **Create a new branch** from `main` (e.g., `feature/my-new-feature` or `bugfix/fix-typo`).
2. Make your changes, following the style conventions in the codebase.
3. **Install and use pre-commit hooks** (see below) to help check your code for quality and formatting before committing.
4. Ensure all tests pass locally by running `pytest`.
5. Open a pull request with a clear title and detailed description.
6. Respond to any review comments and update your PR as needed.

## Code Style, Quality & Pre-commit Hooks
- Please follow the existing code style configured in `pyproject.toml`.
- `requirements.txt` contains runtime dependencies for the pipeline.
- `requirements-dev.txt` contains additional contributor tools, including pre-commit and Ruff. It should be installed after `requirements.txt`, not instead of it.
- `pyproject.toml` stores the Ruff linting and formatting configuration.
- **Pre-commit hooks are required**! They help catch formatting, linting, and quality issues before code is committed. This keeps the codebase clean and consistent for everyone.
- To install pre-commit hooks, activate your virtual environment after installing `requirements.txt`, then run:
  ```sh
  pip install -r requirements-dev.txt
  pre-commit install
  ```
- To run the same checks locally before opening a PR:
  ```sh
  pre-commit run --all-files
  ```
- Most contributors should run Ruff through pre-commit. To run Ruff directly for a focused local check:
  ```sh
  ruff check .
  ruff check . --fix
  ruff format .
  ```
- Write clear, concise commit messages.
- Ensure your code is well-documented and tested.

## Stale Branches
- Please note: **Stale branches will be removed after 1 month** to keep the repository tidy. If you need more time, let the maintainers know!

## Questions?
If you have any questions about contributing, please raise an issue or contact the maintainers directly.

## Security
If you discover a security vulnerability, please see [SECURITY.md](SECURITY.md) for how to report it and our security policy.

## Code of Conduct
All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

Thank you for helping to make this project better!
