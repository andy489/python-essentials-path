import pytest
from reponow.parser import parse_url

@pytest.mark.parametrize("input_url,expected_path", [
    pytest.param("https://github.com/torvalds/linux", "/Users/wesdemos/repos/github/torvalds/linux", id="github_https"),
    pytest.param("git@github.com:g0t4/ask-openai.nvim", "/Users/wesdemos/repos/github/g0t4/ask-openai.nvim", id="github_ssh"),
    pytest.param("https://gcc.gnu.org/git/gcc.git", "/Users/wesdemos/repos/gcc.gnu.org/git/gcc", id="gcc_https_git_proto"),
    pytest.param("https://gitlab.com/g0t4/dotfiles.git", "/Users/wesdemos/repos/gitlab/g0t4/dotfiles", id="gitlab_https_git_suffix"),
    pytest.param("SeeGit", "/Users/wesdemos/repos/github/g0t4/SeeGit", id="shorthand_SeeGit"),
    pytest.param("python/cpython", "/Users/wesdemos/repos/github/python/cpython", id="shorthand_python_cpython"),
    pytest.param("https://github.com/jackMort/ChatGPT.nvim?tab=readme-ov-file#configuration", "/Users/wesdemos/repos/github/jackMort/ChatGPT.nvim", id="github_extra_uri_parts"),
    pytest.param("https://huggingface.co/datasets/PleIAs/common_corpus", "/Users/wesdemos/repos/huggingface.co/datasets/PleIAs/common_corpus", id="hf_dataset_basic"),
    pytest.param("https://huggingface.co/datasets/PleIAs/common_corpus/tree/main", "/Users/wesdemos/repos/huggingface.co/datasets/PleIAs/common_corpus", id="hf_dataset_tree_main"),
    pytest.param("https://huggingface.co/datasets/PleIAs/common_corpus/blob/main/README.md", "/Users/wesdemos/repos/huggingface.co/datasets/PleIAs/common_corpus", id="hf_dataset_blob_readme"),
    pytest.param("https://huggingface.co/microsoft/speecht5_tts", "/Users/wesdemos/repos/huggingface.co/microsoft/speecht5_tts", id="hf_model_speecht5"),
])
def test_parsing_repo_dir(input_url, expected_path):
    repo_dir, _ = parse_url(input_url)
    assert repo_dir == expected_path
