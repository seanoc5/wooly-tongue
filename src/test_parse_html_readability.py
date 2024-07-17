#! /usr/bin/python
import time
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import sys
import logging
from parse_html_readability import *

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
src_file = '../data/test4.html'

def test_read_text():
    source_text = read_file_text(src_file)
    soup = parse_html(source_text)
    text = soup.text
    assert type(text) is str
    assert len(text) >= 470


def test_parse_html():
    # source_text = read_file_text(src_file)
    # soup = parse_html(source_text)
    soup = parse_html(src_file)
    text = soup.text
    assert type(text)==str
    assert len(text) >= 470

def test_split_html():
    soup = parse_html(src_file)
    text = soup.text
    assert type(text)==str
    assert len(text) >= 470



# heading_tags = ["h1", "h2", "h3", 'h4', 'h5', 'h6']
# headings = soup.find_all(heading_tags)
# heading : BeautifulSoup
# for heading in headings:
#     htext = f'## {heading.text}'
#     new_heading = soup.new_tag(heading.name)
#     new_heading.string = "## mytest"
#     heading.content = new_heading
#     # heading.contents
#     logging.debug('hacky markdown?')


