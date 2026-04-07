"""
================================================================================
Project:       Project Tree Generator
File:          setup_hook.py (o generate_tree.py)
Authors:       Michele Bisignano & Mattia Franchini
Date:          January 2026
License:       Apache License 2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
================================================================================
"""

import os
import stat
import sys
from pathlib import Path

def install_hook():
    # 1. Locate the .git folder
    try:
        current_dir = Path(__file__).resolve()
        def find_git_root(start_path: Path) -> Path:
            for parent in [start_path] + list(start_path.parents):
                if (parent / ".git").exists():
                    return parent
            raise RuntimeError(".git folder not found")
        
        repo_root = find_git_root(current_dir)
        hooks_dir = repo_root / ".git" / "hooks"
    except Exception as e:
        print(f"[ERROR] {e}. Make sure you are in a Git repository.")
        return

    # 2. Define the hook file path
    hook_path = hooks_dir / "pre-commit"

    # 3. Content of the bash script
    # We use a more robust detection: check if the command actually works, not just if it exists.
    hook_content = (
        "#!/bin/sh\n"
        "echo '[HOOK] Checking Python environment...'\n\n"
        
        "# Detection logic: try py (Windows), then python3 (Mac/Linux), then python\n"
        "if py -c 'import sys' >/dev/null 2>&1; then\n"
        "    PY_CMD=py\n"
        "elif python3 -c 'import sys' >/dev/null 2>&1; then\n"
        "    PY_CMD=python3\n"
        "elif python -c 'import sys' >/dev/null 2>&1; then\n"
        "    PY_CMD=python\n"
        "else\n"
        "    echo '[ERROR] Python not found! Please install Python or add it to PATH.'\n"
        "    exit 1\n"
        "fi\n\n"
        
        "echo \"[HOOK] Using: $PY_CMD\"\n"
        "echo \"[HOOK] Regenerating project tree...\"\n\n"
        
        "# 1. Run the generator\n"
        "$PY_CMD Tools/project_tree/generate_tree.py\n\n"
        
        "# 2. Add the generated file to the commit\n"
        "git add Docs/Project_Structure/repository_tree.md\n"
    )

    # 4. Write the file
    try:
        # We use binary write or explicit newline to avoid CRLF issues on some git-bash setups
        with open(hook_path, "w", encoding="utf-8", newline='\n') as f:
            f.write(hook_content)
        
        # 5. Make the file executable
        st = os.stat(hook_path)
        os.chmod(hook_path, st.st_mode | stat.S_IEXEC)
        
        print(f"[SUCCESS] Hook installed at: {hook_path}")
        print("The tree will now update automatically on every commit.")
        
    except Exception as e:
        print(f"[ERROR] Could not write the hook: {e}")

if __name__ == "__main__":
    install_hook()