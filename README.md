# Project Tree Generator

**Automated "Living Documentation" for your repository structure.**

## About
Keeping documentation synchronized with the actual file structure of a project is often a tedious manual task. **Project Tree Generator** is a Python utility designed to solve this problem. 

It automatically scans your project, filters out technical artifacts (like `.git`, `__pycache__`, or build folders), and generates a clean, visually formatted directory tree in Markdown. This ensures that your `repository_tree.md` or architectural documentation never becomes obsolete.

## Live Demo
This repository itself uses the script to generate its own structure. 

*   **[📂 View the Script Source Code](Tools/generate_tree.py)**
*   **[📄 View the Generated Output File](Docs/Project_Structure/repository_tree.md)**

## Features
- **Automatic Root Detection:** The script intelligently locates the project root, regardless of the depth from which it is executed.
- **Smart Visual Formatting:** 
  - Distinguishes directories with a trailing slash (`Docs/` vs `file.txt`).
  - Adds "smart spacing" (empty vertical lines) between folder blocks to improve readability.
- **Clean Output:** Automatically wraps the result in Markdown code blocks for immediate rendering on GitHub/GitLab.
- **Customizable:** Easily configure ignored files and output paths directly in the script.

## Getting Started

### Prerequisites
- Python 3.6 or higher.
- No external libraries required (uses standard `os` and `pathlib`).

### Installation
Simply copy the `generate_tree.py` script into your project. A common convention is to place it in a `Tools/` or `scripts/` directory.

```text
MyProject/
├── Tools/
│   └── generate_tree.py  <-- Place script here
├── src/
└── ...
```

## Usage

Run the script from your terminal. You can run it from the project root or the tools directory.

```bash
# Example: Running from the project root
python Tools/generate_tree.py
```

Upon execution, the script will:
1.  Scan the directory structure.
2.  Ignore files defined in the `IGNORE_LIST`.
3.  Generate (or overwrite) the file at `Docs/Project_Structure/repository_tree.md`.

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
**Michele Bisignano**
