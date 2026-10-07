import os
import re
import sys
from rich import print
from urllib.parse import urlparse

_SSH_PATTERN = re.compile(r"git@([^:]+):(.+)")
_BLOB_TREE_PATTERN = re.compile(r"[^/]+/[^/]+/(blob|tree)/")
_HOST_ALIASES = {
    "github.com": "github",
    "gitlab.com": "gitlab",
    "bitbucket.org": "bitbucket",
}
_HTTPS_ONLY_HOSTS = {"gitlab.gnome.org", "sourceware.org", "git.kernel.org", "huggingface.co", "git.sr.ht"}

def parse_url(url: str) -> tuple[str, str]:

    url = url.strip().removesuffix(".git")

    parsed: dict | None = None

    if url.startswith("git@"):  # SSH: git@host:path/to/repo
        match = _SSH_PATTERN.match(url)
        if match:
            host, path = match.groups()
            parsed = {"domain": host, "repo_path": path}
    elif url.startswith("https://"):  # HTTPS
        url_parsed = urlparse(url)
        path = url_parsed.path.strip("/")
        # strip /blob/ and /tree/ sub-paths (e.g. github file browser URLs)
        if _BLOB_TREE_PATTERN.search(path):
            path = re.sub(r"/(blob|tree).*", "", path)
        parsed = {"domain": url_parsed.netloc, "repo_path": path}
    elif "/" not in url:  # shorthand: repo  =>  github.com/g0t4/{url}
        parsed = {"domain": "github.com", "repo_path": "g0t4/" + url}
    else:  # shorthand: org/repo  =>  github.com/{url}
        parsed = {"domain": "github.com", "repo_path": url}

    if not parsed:
        print("unable to parse repository url", url, "\n")
        sys.exit(1)

    domain = parsed["domain"]
    host_name = _HOST_ALIASES.get(domain, domain)
    repo_dir = os.path.expanduser(os.path.join("~/repos", host_name, parsed["repo_path"]))

    if domain in _HTTPS_ONLY_HOSTS:
        clone_from = f"https://{domain}/{parsed['repo_path']}"
    else:
        clone_from = f"git@{domain}:{parsed['repo_path']}"

    return repo_dir, clone_from

if __name__ == "__main__":
    HOME = os.path.expanduser("~")

    cases = [
        ("https://gitlab.com/g0t4/dotfiles.git",                                    f"{HOME}/repos/gitlab/g0t4/dotfiles"),
        ("https://huggingface.co/datasets/PleIAs/common_corpus/tree/main",           f"{HOME}/repos/huggingface.co/datasets/PleIAs/common_corpus"),
        ("https://github.com/torvalds/linux",                                        f"{HOME}/repos/github/torvalds/linux"),
        ("git@github.com:g0t4/ask-openai.nvim",                                     f"{HOME}/repos/github/g0t4/ask-openai.nvim"),
    ]
    for url, expected in cases:
        result, _ = parse_url(url)
        assert result == expected, f"FAIL: {url!r}\n  got:      {result}\n  expected: {expected}"
    print("all tests passed")

