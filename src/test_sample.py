# content of test_sample.py
from src.parse_html_readability import read_file_text


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5


def test_parse():
    src_file = '../data/test4.html'
    source_text = read_file_text(src_file)
    assert type(source_text) is str
    assert len(source_text) >= 1044
