# Project Tree Generator

**Automated "Living Documentation" for your repository structure.**

## About
Keeping documentation synchronized with the actual file structure of a project is often a tedious manual task. **Project Tree Generator** is a Python utility designed to solve this problem. 

It automatically scans your project, filters out technical artifacts (respecting your `.gitignore` rules), and generates a clean, visually formatted directory tree in Markdown. This ensures that your `repository_tree.md` or architectural documentation never becomes obsolete.

## Live Demo
This repository itself uses the script to generate its own structure. 

*   **[📂 View the Script Source Code](Tools/generate_tree.py)**
*   **[📄 View the Generated Output File](Docs/Project_Structure/repository_tree.md)**

## Features
- **Smart Root Detection:** The script automatically locates the project root (looking for `.git` or `.gitignore`), regardless of where you run it from.
- **Gitignore Integration:** Respects your project's `.gitignore` rules to exclude unwanted files (e.g., `venv`, `__pycache__`, build folders).
- **Automated Workflow:** Includes a setup script to install a Git hook, keeping documentation updated automatically on every commit.
- **Cross-Platform:** The automation works seamlessly on Windows, macOS, and Linux.
- **CLI Support:** Fully customizable via command-line arguments (set output path, max depth, etc.).
- **Clean Output:** Automatically wraps the result in Markdown code blocks for immediate rendering on GitHub/GitLab.

## Getting Started

### Prerequisites
- Python 3.6 or higher.
- No external libraries required (uses standard `os`, `argparse`, `pathlib`).

### Installation
Simply copy the `Tools/` directory into your project.

```text
MyProject/
├── Tools/
│   ├── generate_tree.py  <-- The main script
│   └── setup_hook.py     <-- The automation installer
├── src/
└── ...
```

## Automation (Set & Forget)

You can configure the repository to **automatically update the tree every time you commit**. This ensures the documentation is never out of sync with the code.

To enable this, run the setup script once:

```bash
# macOS / Linux
python3 Tools/setup_hook.py

# Windows
python Tools/setup_hook.py
```

*Note: This creates a pre-commit hook in your local `.git` configuration. From now on, whenever you run `git commit`, the tree will be regenerated and included in the commit automatically.*

## Manual Usage

You can also run the script manually from the CLI if needed.

### 1. Default Run
Generates the tree starting from the project root and saves it to the default path (`Docs/Project_Structure/repository_tree.md`).

```bash
# macOS / Linux
python3 Tools/generate_tree.py

# Windows
python Tools/generate_tree.py
```

### 2. Limit Depth (Recommended for large repos)
If you only want to see the high-level architecture (e.g., top 2 levels):

```bash
python3 Tools/generate_tree.py --depth 2
```

### 3. Custom Output File
Save the tree to a specific file (e.g., directly to a Markdown file in the root):

```bash
python3 Tools/generate_tree.py --output ARCHITECTURE.md
```

### 4. Show Help
View all available options:

```bash
python3 Tools/generate_tree.py --help
```

## Example Output

The script generates a clean, spaced-out tree like this:

```text
MyProject/
├── Docs/
│   ├── Images/
│   │   └── diagram.png
│   │
│   ├── Project_Structure/
│   │   └── repository_tree.md
│   │
│   └── Specifications/
│       └── requirements.md
│
├── Tools/
│   └── generate_tree.py
│
├── src/
│   ├── main.py
│   └── utils.py
│
└── LICENSE
```

## Authors
**Michele Bisignano & Mattia Franchini**