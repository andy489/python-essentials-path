import argparse
import os
import subprocess
import sys
from rich import print
from reponow.parser import parse_url

# constants for subprocess.run for readability
IGNORE_FAILURE = False
STOP_ON_FAILURE = True

def main():

    parser = argparse.ArgumentParser(description="(w)es (cl)one", prog="wcl")
    parser.add_argument("url", type=str, help="repository clone url")
    parser.add_argument("--dry-run", action="store_true", help="preview changes")
    parser.add_argument("--path-only", action="store_true", help="return path (do not clone)")
    args = parser.parse_args()
    clone_repo(args.url, args.dry_run, args.path_only)


def clone_repo(url: str, dry_run: bool = False, path_only: bool = False):

    repo_dir, clone_from = parse_url(url)
    if path_only:
        print(repo_dir)
        sys.exit()

    # ensure org dir exists, including parents
    # - can also let git clone create parents
    org_dir = os.path.dirname(repo_dir)
    if dry_run:
        print("mkdir -p", org_dir, "\n")
    else:
        os.makedirs(org_dir, exist_ok=True)

    if os.name != "nt":
        which_zsh = subprocess.run("which zsh", shell=True, check=IGNORE_FAILURE, stdout=subprocess.DEVNULL)
        if which_zsh.returncode == 0:
            # - zsh's z allows dir to be added before it is created
            # - adding ahead of creating (during clone) means I can _cd_ to it while its cloning
            # - or if dir already exists, then add to the stats count for it
            Z_ADD_ZSH = f"z --add '{repo_dir}'"
            if dry_run:
                print("# zsh z add:")
                print(Z_ADD_ZSH, "\n")
            else:
                # zsh -i => interactive, otherwise z command won't be available
                subprocess.run(["zsh", "-il", "-c", Z_ADD_ZSH], check=IGNORE_FAILURE)

    if os.path.isdir(repo_dir):
        print(f"repo_dir exists {repo_dir}, attempt pull latest", "\n")
        pull = ["git", "-C", repo_dir, "pull"]
        if dry_run:
            print(pull, "\n")
        else:
            subprocess.run(pull, check=IGNORE_FAILURE)
    else:
        print(f"# cloning {clone_from}...")
        clone = ["git", "clone", "--recurse-submodules", clone_from, repo_dir]
        if dry_run:
            print(clone, "\n")
        else:
            subprocess.run(clone, check=STOP_ON_FAILURE)

    is_windows = os.name == "nt"
    if is_windows:
        # - dir must exist before calling z
        # - FYI current pwsh z caches the db, so this only works for z calls in a new pwsh instance
        Z_ADD_PWSH = f"z '{repo_dir}'"
        if dry_run:
            print("# pwsh z add:")
            print(Z_ADD_PWSH, "\n")
        else:
            subprocess.run(["pwsh", "-NoProfile", "-Command", Z_ADD_PWSH], check=IGNORE_FAILURE)

    if os.name != "nt":
        which_fish = subprocess.run("which fish", shell=True, check=IGNORE_FAILURE, stdout=subprocess.DEVNULL)
        if which_fish.returncode == 0:
            # - dir must exist before calling __z_add
            # - __z_add does not take an argument, instead it uses $PWD (hence set cwd)
            # - FYI I had issues w/ auto-venv (calling deactivate) in fish (but, not zsh)
            #   so, don't launch an interactive shell (which would then use auto-venv)
            # - fish doesn't need interactive for z to be loaded (b/c its installed in functions dir)
            z_add_fish = ["fish", "-c", "__z_add"]
            if dry_run:
                print("# fish z add:")
                print(z_add_fish, f"cwd={repo_dir}", "\n")
            else:
                subprocess.run(z_add_fish, cwd=repo_dir, check=IGNORE_FAILURE)

if __name__ == "__main__":
    main()
