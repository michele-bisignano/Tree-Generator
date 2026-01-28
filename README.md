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
- **CLI Support:** Fully customizable via command-line arguments (set output path, max depth, etc.).
- **Performance Control:** Supports a recursion depth limit (`--depth`) to handle large repositories without clutter.
- **Clean Output:** Automatically wraps the result in Markdown code blocks for immediate rendering on GitHub/GitLab.

## Getting Started

### Prerequisites
- Python 3.6 or higher.
- No external libraries required (uses standard `os`, `argparse`, `pathlib`).

### Installation
Simply copy the `generate_tree.py` script into your project. A common convention is to place it in a `Tools/` directory.

```text
MyProject/
├── Tools/
│   └── generate_tree.py  <-- Place script here
├── src/
└── ...
```

## Usage

You can run the script from anywhere in your project.

### 1. Default Run
Generates the tree starting from the project root and saves it to the default path (`Docs/Project_Structure/repository_tree.md`).

```bash
python Tools/generate_tree.py
```

### 2. Limit Depth (Recommended for large repos)
If you only want to see the high-level architecture (e.g., top 2 levels):

```bash
python Tools/generate_tree.py --depth 2
```

### 3. Custom Output File
Save the tree to a specific file (e.g., directly to a Markdown file in the root):

```bash
python Tools/generate_tree.py --output ARCHITECTURE.md
```

### 4. Show Help
View all available options:

```bash
python Tools/generate_tree.py --help
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

## Author
**Michele Bisignano & Mattia Franchini**
