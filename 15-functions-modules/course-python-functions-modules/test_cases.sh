#!/usr/bin/env bash

# FYI this does not check for:
# - Normalized clone url for some hosts (uses_https check)

python3 wcl.py --path-only https://github.com/andy489/python-essentials-path
# /Users/I777690/repos/github/andy489/python-essentials-path

python3 wcl.py --path-only git@github.com:andy489/python-essentials-path
# /Users/I777690/repos/github/andy489/python-essentials-path

# not covered in original tests, used https instead
# python3 wcl.py --path-only git://gcc.gnu.org/git/gcc.git
python3 wcl.py --path-only https://gcc.gnu.org/git/gcc.git
# /Users/I777690/repos/gcc.gnu.org/git/gcc

# .git suffix on https
python3 wcl.py --path-only https://gitlab.com/andy489/python-essentials-path.git
# /Users/I777690/repos/gitlab/andy489/python-essentials-path

python3 wcl.py --path-only python-essentials-path
# /Users/I777690/repos/github/andy489/python-essentials-path

python3 wcl.py --path-only python/cpython
# /Users/I777690/repos/github/python/cpython

# contains other parts of URI path, strip those
python3 wcl.py --path-only "https://github.com/jackMort/ChatGPT.nvim?tab=readme-ov-file#configuration"
# /Users/I777690/repos/github/jackMort/ChatGPT.nvim

# 3 level repo_path
python3 wcl.py --path-only https://huggingface.co/datasets/PleIAs/common_corpus
# /Users/I777690/repos/huggingface.co/datasets/PleIAs/common_corpus

# ignore tree/... (don't treat as part of repo_path)
python3 wcl.py --path-only https://huggingface.co/datasets/PleIAs/common_corpus/tree/main
# /Users/I777690/repos/huggingface.co/datasets/PleIAs/common_corpus

# ignore blob/ too
python3 wcl.py --path-only https://huggingface.co/datasets/PleIAs/common_corpus/blob/main/README.md
# /Users/I777690/repos/huggingface.co/datasets/PleIAs/common_corpus

python3 wcl.py --path-only https://huggingface.co/microsoft/speecht5_tts
# /Users/I777690/repos/huggingface.co/microsoft/speecht5_tts
