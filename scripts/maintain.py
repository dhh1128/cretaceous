#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
WIKI_PATH = os.path.join(REPO_ROOT, "wiki")
TOC_PATH = os.path.join(REPO_ROOT, "toc.md")

def check_submodule():
    # If wiki exists but is not a git repo, delete it
    if os.path.exists(WIKI_PATH):
        git_file = os.path.join(WIKI_PATH, ".git")
        if not os.path.exists(git_file):
            if os.path.isfile(WIKI_PATH):
                os.remove(WIKI_PATH)
            elif os.path.isdir(WIKI_PATH):
                shutil.rmtree(WIKI_PATH)
    # Get remote URL from git config
    git_config = os.path.join(REPO_ROOT, ".git", "config")
    remote_url = None
    with open(git_config) as f:
        for line in f:
            if line.strip().startswith("url = "):
                remote_url = line.strip().split("= ")[1]
                break
    if remote_url:
        if remote_url.endswith(".git"):
            wiki_url = remote_url[:-4] + ".wiki.git"
        else:
            wiki_url = remote_url + ".wiki.git"
        # Clone wiki repo into wiki folder
        result = subprocess.run([
            "git", "clone", wiki_url, WIKI_PATH
        ], cwd=REPO_ROOT)
        if result.returncode != 0:
            print("Warning: Could not clone wiki repo.")
    else:
        print("Could not find remote URL in git config.")

def local_path_for_rel_url(rel_url: str, base_location: str) -> str:
    if rel_url.startswith("$racdurl"):
        rel_url = rel_url[len("$racdurl"):].lstrip("/")
        base_path = REPO_ROOT
    elif rel_url.startswith("$rwdurl"):
        rel_url = rel_url[len("$rwdurl"):].lstrip("/")
        base_path = WIKI_PATH
    else:
        rel_url = rel_url.lstrip("./")
        base_path = base_location
    local_path = os.path.normpath(os.path.join(base_path, rel_url))
    return local_path

def regen_toc():
    exclude_names = {"README.md", "docs", "scripts", "prompts", "toc.md"}
    def is_hidden(name):
        return name.startswith(".") or name in exclude_names
    items = set()
    # Walk repo root
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if not is_hidden(d)]
        for file in files:
            if is_hidden(file):
                continue
            rel_path = os.path.relpath(os.path.join(root, file), REPO_ROOT)
            # If file is inside wiki, prefix with $wdurl/
            if rel_path.startswith(os.path.relpath(WIKI_PATH, REPO_ROOT) + os.sep):
                wiki_rel_path = os.path.relpath(os.path.join(root, file), WIKI_PATH)
                items.add(f"$wdurl/{wiki_rel_path}")
            else:
                items.add(rel_path)
    frontmatter = ""
    old_body = ""
    if os.path.exists(TOC_PATH):
        with open(TOC_PATH) as f:
            content = f.read()
            m = re.match(r"(---\n.*?---\n)?(.*)", content, re.DOTALL)
            if m:
                frontmatter = m.group(1) if m.group(1) else ""
                old_body = m.group(2)
    new_body = "\n".join(sorted(items))
    if new_body.strip() != old_body.strip():
        with open(TOC_PATH, "w") as f:
            if frontmatter:
                f.write(frontmatter)
            f.write(new_body)
        subprocess.run(["git", "add", TOC_PATH], cwd=REPO_ROOT, check=True)
        subprocess.run(["git", "commit", "-m", "Update toc.md"], cwd=REPO_ROOT, check=True)
        subprocess.run(["git", "push"], cwd=REPO_ROOT, check=True)
    else:
        print("toc.md is up to date; no changes made.")

def main():
    check_submodule()
    regen_toc()
    sys.exit(0)

if __name__ == "__main__":
    main()
