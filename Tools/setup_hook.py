"""
================================================================================
SCRIPT:        Project Directory Tree Generator
AUTHOR:        Michele Bisignano & Mattia Franchini
DATE:          January 2026
LICENSE:       MIT License

USAGE:
    Run this script only the first time
    
    $ ppython setup_hook.py                       
================================================================================
"""
import os
import stat
from pathlib import Path

def install_hook():
    # 1. Locate the .git folder
    current_dir = Path(__file__).parent.resolve()
    repo_root = current_dir.parent
    hooks_dir = repo_root / ".git" / "hooks"

    if not hooks_dir.exists():
        print(f"[ERROR] Could not find .git folder in {repo_root}")
        print("Make sure you are in an initialized Git repository.")
        return

    # 2. Define the hook file path
    hook_path = hooks_dir / "pre-commit"

    # 3. Content of the bash script that will be executed by Git
    # UPDATED: Usiamo 'python3' specificamente per macOS
    hook_content = (
        "#!/bin/sh\n"
        "echo '[HOOK] Automatically updating project structure...'\n\n"
        "# 1. Generate the updated tree\n"
        "python3 Tools/generate_tree.py\n\n"
        "# 2. Add the generated file to the current commit\n"
        "git add Docs/Project_Structure/repository_tree.md\n"
    )

    # 4. Write the file
    try:
        with open(hook_path, "w", encoding="utf-8", newline='\n') as f:
            f.write(hook_content)
        
        # 5. Make the file executable
        st = os.stat(hook_path)
        os.chmod(hook_path, st.st_mode | stat.S_IEXEC)
        
        print(f"[SUCCESS] Hook installed at: {hook_path}")
        print("From now on, repository_tree.md will update on every commit!")
        
    except Exception as e:
        print(f"[ERROR] Could not write the hook: {e}")

if __name__ == "__main__":
    install_hook()