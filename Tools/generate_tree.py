"""
================================================================================
SCRIPT:        Project Directory Tree Generator
AUTHOR:        Michele Bisignano & Mattia Franchini
DATE:          January 2026
LICENSE:       MIT License

DESCRIPTION:
    This script automatically generates a visual representation of the project's 
    file structure (a directory tree) and saves it as a Markdown file.

    FEATURES:
    - Smart Root Detection: Automatically finds the project root (looking for .git).
    - Gitignore Support: Respects .gitignore rules to exclude unwanted files.
    - CLI Support: Customizable output path and recursion depth via arguments.
    - Performance: Supports a --depth limit for large repositories.

USAGE:
    Run this script from anywhere within the project using Python:
    
    $ python tree_gen.py                        # Default usage
    $ python tree_gen.py --depth 2              # Limit recursion depth
    $ python tree_gen.py --output docs/tree.md  # Custom output file
    $ python tree_gen.py --help                 # Show all options
================================================================================
"""

import os
import fnmatch
from pathlib import Path
from typing import List, Set
import argparse

# ==========================================
# CONFIGURATION
# ==========================================

# The target output path relative to the project root.
OUTPUT_REL_PATH = Path("Docs/Project_Structure/repository_tree.md")

def find_project_root(start_path: Path) -> Path:
    """
    Recursively looks up parent directories until .git or .gitignore is found.
    Fallback to the current path if not found.
    """
    current = start_path.resolve()
    for path in [current] + list(current.parents):
        if (path / ".git").exists() or (path / ".gitignore").exists():
            return path
    return current

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

def is_ignored(path: Path, patterns: List[str], root_path: Path) -> bool:
    """
    Checks if a file or directory should be ignored, handling relative paths
    and folder-specific patterns.
    """
    name = path.name
    
    # Calculate path relative to root for precise matching (e.g., src/temp/*)
    try:
        rel_path = path.relative_to(root_path).as_posix()
    except ValueError:
        rel_path = name

    for pattern in patterns:
        clean_pattern = pattern.rstrip('/')
        
        # If pattern ends with '/', it should only match directories
        if pattern.endswith('/') and not path.is_dir():
            continue
            
        # Match against filename (e.g., *.log) OR relative path (e.g., logs/*.txt)
        if fnmatch.fnmatch(name, clean_pattern) or fnmatch.fnmatch(rel_path, clean_pattern):
            return True
    return False
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

def generate_tree_structure(current_path: Path, patterns: List[str], root_path: Path, 
                            prefix: str = "", current_depth: int = 0, max_depth: int = -1) -> str:
    # 1. STOP if max depth is reached
    if max_depth != -1 and current_depth > max_depth:
        return ""

    output_string = ""
    try:
        items = sorted(os.listdir(current_path), key=lambda s: s.lower())
    except PermissionError:
        return ""

    # 2. FILTER items using the new is_ignored logic (passing the full path)
    filtered_items = []
    for item in items:
        full_path = current_path / item
        if not is_ignored(full_path, patterns, root_path):
            filtered_items.append(item)
    
    count = len(filtered_items)
    for i, item in enumerate(filtered_items):
        is_last = (i == count - 1)
        path = current_path / item
        is_dir = path.is_dir()
        
        display_name = f"{item}/" if is_dir else item
        connector = "└── " if is_last else "├── "
        output_string += f"{prefix}{connector}{display_name}\n"
        
        if is_dir:
            extension = "    " if is_last else "│   "
            # 3. RECURSIVE CALL with new parameters
            output_string += generate_tree_structure(
                path, patterns, root_path, prefix + extension, 
                current_depth + 1, max_depth
            )

    return output_string


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

def main():
    parser = argparse.ArgumentParser(description="Generate Project Directory Tree")
    parser.add_argument("--root", type=str, default=None, help="Root path (default: auto-detect)")
    parser.add_argument("--output", type=str, default=str(OUTPUT_REL_PATH), help="Output file path")
    parser.add_argument("--depth", type=int, default=-1, help="Max recursion depth (-1 for infinite)")
    
    args = parser.parse_args()

    # 1. Determine Project Root
    if args.root:
        project_root = Path(args.root).resolve()
    else:
        # Use the new auto-detection function
        project_root = find_project_root(Path(__file__))
    
    print(f"[INFO] Project Root detected at: {project_root}")

    # 2. Load Ignore Patterns
    patterns = load_gitignore_patterns(project_root)

    # 3. Generate the Tree String (passing new arguments)
    tree_body = generate_tree_structure(
        project_root, patterns, project_root, max_depth=args.depth
    )
    
    final_content = (
        "```text\n"
        f"{project_root.name}/\n"
        f"{tree_body}"
        "```\n"
    )

    # 4. Define Output Path (handles absolute or relative paths)
    out_path = Path(args.output)
    output_file = out_path if out_path.is_absolute() else project_root / out_path
    
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 5. Write File
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"[SUCCESS] Tree generated successfully at: {output_file}")
    except Exception as e:
        print(f"[ERROR] Failed to write file: {e}")

if __name__ == "__main__":
    main()