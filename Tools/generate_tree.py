"""
================================================================================
SCRIPT:        Project Directory Tree Generator
AUTHOR:        Michele Bisignano
DATE:          January 2026
LICENSE:       MIT License

DESCRIPTION:
    This script automatically generates a visual representation of the project's 
    file structure (a directory tree). 
    
    It respects the project's '.gitignore' file to determine which files should 
    be excluded. If no '.gitignore' is found, it lists all files.
    
    The output is saved as a Markdown file wrapped in code blocks.

USAGE:
    Run this script from the 'Tools/' directory (or anywhere within the project).
    It will automatically detect the project root and update the documentation.
================================================================================
"""

import os
import fnmatch
from pathlib import Path
from typing import List, Set

# ==========================================
# CONFIGURATION
# ==========================================

# The target output path relative to the project root.
OUTPUT_REL_PATH = Path("Docs/Project_Structure/repository_tree.md")

# ==========================================
# LOGIC
# ==========================================

def load_gitignore_patterns(root_path: Path) -> List[str]:
    """
    Reads the .gitignore file from the project root and returns a list of patterns.
    
    It handles comments (lines starting with #) and empty lines.
    It automatically adds '.git' to the patterns to prevent internal git 
    metadata from cluttering the documentation.

    Args:
        root_path (Path): The absolute path to the project root.

    Returns:
        List[str]: A list of glob patterns to ignore.
    """
    gitignore_path = root_path / ".gitignore"
    patterns = ['.git'] # Always ignore the .git metadata folder

    if gitignore_path.exists():
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if line and not line.startswith("#"):
                        patterns.append(line)
        except Exception as e:
            print(f"[WARN] Could not read .gitignore: {e}")
    
    return patterns

def is_ignored(name: str, patterns: List[str]) -> bool:
    """
    Checks if a file or directory name matches any of the gitignore patterns.
    
    Args:
        name (str): The file or directory name.
        patterns (List[str]): List of patterns to check against.

    Returns:
        bool: True if the item should be ignored, False otherwise.
    """
    for pattern in patterns:
        # Normalize pattern: remove leading/trailing slashes for simple matching
        clean_pattern = pattern.rstrip('/')
        
        # Check if name matches the pattern (using unix filename matching)
        if fnmatch.fnmatch(name, clean_pattern):
            return True
            
    return False

def generate_tree_structure(current_path: Path, patterns: List[str], prefix: str = "") -> str:
    """
    Recursively iterates through directories to build a visual tree structure string.
    
    It filters items based on the provided ignore patterns (from .gitignore).
    It adds 'smart spacing' (empty vertical lines) between folder blocks.

    Args:
        current_path (Path): The Path object of the directory currently being scanned.
        patterns (List[str]): List of ignore patterns.
        prefix (str): The string prefix used for indentation and visual tree connectors.

    Returns:
        str: A multi-line string representing the formatted directory tree.
    """
    output_string = ""
    
    try:
        # Sort items: Case-insensitive alphabetical order
        items = sorted(os.listdir(current_path), key=lambda s: s.lower())
    except PermissionError:
        return ""

    # Filter out items based on .gitignore patterns
    filtered_items = [item for item in items if not is_ignored(item, patterns)]
    
    count = len(filtered_items)
    for i, item in enumerate(filtered_items):
        is_last = (i == count - 1)
        path = current_path / item
        is_dir = path.is_dir()
        
        # Format the display name: append '/' if it is a directory
        display_name = f"{item}/" if is_dir else item

        # Determine the connector symbol based on list position
        connector = "└── " if is_last else "├── "
        
        # Append the current item to the output string
        output_string += f"{prefix}{connector}{display_name}\n"
        
        if is_dir:
            # Determine the extension prefix for the next recursive level
            extension = "    " if is_last else "│   "
            
            # Recursive call to process the subdirectory
            output_string += generate_tree_structure(path, patterns, prefix + extension)
            
            # Add a vertical spacer line to visually separate folder blocks,
            # but only if there are subsequent items in the current directory.
            if not is_last:
                output_string += f"{prefix}│\n"

    return output_string

def main():
    """
    Main entry point of the script.

    1. Detects the project root.
    2. Loads .gitignore patterns.
    3. Generates the tree string.
    4. Writes the final content to the specified Markdown file.
    """
    # 1. Determine Project Root automatically
    script_location = Path(__file__).resolve()
    project_root = script_location.parent.parent
    
    print(f"[INFO] Project Root detected at: {project_root}")

    # 2. Load Ignore Patterns
    patterns = load_gitignore_patterns(project_root)
    print(f"[INFO] Loaded {len(patterns)} ignore patterns from .gitignore (including defaults).")

    # 3. Generate the Tree String
    tree_body = generate_tree_structure(project_root, patterns)
    
    # 4. Construct the Final Markdown Content
    final_content = (
        "```\n"
        f"{project_root.name}/\n"
        f"{tree_body}"
        "```\n"
    )

    # 5. Define Output Path and Create Directory if needed
    output_file = project_root / OUTPUT_REL_PATH
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 6. Write File
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"[SUCCESS] Tree generated successfully at: {output_file}")
    except Exception as e:
        print(f"[ERROR] Failed to write file: {e}")

if __name__ == "__main__":
    main()