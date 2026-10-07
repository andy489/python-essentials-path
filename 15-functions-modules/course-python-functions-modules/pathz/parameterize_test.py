import pytest
from reponow.parser import parse_url

HOME = "/Users/I777690"

@pytest.mark.parametrize("input_url,expected_path", [
    pytest.param("https://github.com/andy489/python-essentials-path", f"{HOME}/repos/github/andy489/python-essentials-path", id="github_https"),
    pytest.param("git@github.com:andy489/python-essentials-path", f"{HOME}/repos/github/andy489/python-essentials-path", id="github_ssh"),
    pytest.param("https://gcc.gnu.org/git/gcc.git", f"{HOME}/repos/gcc.gnu.org/git/gcc", id="gcc_https_git_proto"),
    pytest.param("https://gitlab.com/andy489/python-essentials-path.git", f"{HOME}/repos/gitlab/andy489/python-essentials-path", id="gitlab_https_git_suffix"),
    pytest.param("python-essentials-path", f"{HOME}/repos/github/andy489/python-essentials-path", id="shorthand_repo"),
    pytest.param("python/cpython", f"{HOME}/repos/github/python/cpython", id="shorthand_python_cpython"),
    pytest.param("https://github.com/jackMort/ChatGPT.nvim?tab=readme-ov-file#configuration", f"{HOME}/repos/github/jackMort/ChatGPT.nvim", id="github_extra_uri_parts"),
    pytest.param("https://huggingface.co/datasets/PleIAs/common_corpus", f"{HOME}/repos/huggingface.co/datasets/PleIAs/common_corpus", id="hf_dataset_basic"),
    pytest.param("https://huggingface.co/datasets/PleIAs/common_corpus/tree/main", f"{HOME}/repos/huggingface.co/datasets/PleIAs/common_corpus", id="hf_dataset_tree_main"),
    pytest.param("https://huggingface.co/datasets/PleIAs/common_corpus/blob/main/README.md", f"{HOME}/repos/huggingface.co/datasets/PleIAs/common_corpus", id="hf_dataset_blob_readme"),
    pytest.param("https://huggingface.co/microsoft/speecht5_tts", f"{HOME}/repos/huggingface.co/microsoft/speecht5_tts", id="hf_model_speecht5"),
])
def test_parsing_repo_dir(input_url, expected_path):
    repo_dir, _ = parse_url(input_url)
    assert repo_dir == expected_path
