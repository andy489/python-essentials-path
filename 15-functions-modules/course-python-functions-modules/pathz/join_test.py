# from os import path
import pathz as path

def test_joiner_no_tilde_expands_like_normal():
    joined = path.join("path", "to", "file.txt")
    assert "path/to/file.txt" == joined

def test_joiner_tilde_leading_expands_to_home_dir():
    joined = path.join("~/path", "to", "file.txt")
    assert "/Users/wesdemos/path/to/file.txt" == joined

def test_exists():
    assert path.exists("~/repos")

def test_abs():
    abs_path = path.abspath("~/")
    assert "/Users/wesdemos" == abs_path


