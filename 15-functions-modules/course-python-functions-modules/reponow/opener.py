import argparse
import subprocess
from rich import print
from reponow.parser import parse_url
from reponow.wcl import clone_repo, IGNORE_FAILURE


def main():
    parser = argparse.ArgumentParser(description="clone and open a repo in VS Code", prog="open_repo")
    parser.add_argument("url", type=str, help="repository clone url")
    args = parser.parse_args()

    clone_repo(args.url)

    repo_dir, _ = parse_url(args.url)
    subprocess.run(f"code '{repo_dir}'", shell=True, check=IGNORE_FAILURE, stdout=subprocess.DEVNULL)


if __name__ == "__main__":
    main()
