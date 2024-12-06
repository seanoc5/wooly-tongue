#! /usr/bin/python
import time
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# body = ''
source_text =  open('../data/test4.html').read()

soup=BeautifulSoup(source_text, "html.parser")
# the rest is debugging/test
tag : BeautifulSoup
heading_tags = ["h1", "h2", "h3", 'h4', 'h5', 'h6']
headings = soup.find_all(heading_tags)
heading : BeautifulSoup
for heading in headings:
    tag_name = heading.name
    depth = int(tag_name[1])
    new_heading = soup.new_tag(heading.name)
    htext = f"{'#' * depth} { heading.text}"
    new_heading.string = htext
    # heading.content = new_heading
    # heading.contents = new_heading
    heading.replace_with(new_heading)
    logging.info(f'Heading: {new_heading}')

headings2 = soup.find_all(heading_tags)

body_text = soup.text

logging.info(f"Content")
