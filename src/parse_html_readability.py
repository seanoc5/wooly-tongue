#! /usr/bin/python
import os
import re
import time
import requests
from typing import List
from bs4 import BeautifulSoup
from collections import defaultdict
import sys
import logging

SECTION = 'section'
content_map = defaultdict(lambda: [])
heading_tags = ["h1", "h2", "h3", 'h4', 'h5', 'h6']

def read_file_text(src: str) -> str:
    """ wrapper to get text from file"""
    logging.info(f'using source: {src}')
    source_text = open(src).read()
    return source_text


def parse_html(src: str) -> BeautifulSoup:
    """wrapper to accept either html text, or a path string to an html file, load it in soup and return soup"""
    body_text:str

    if os.path.exists(src):
        body_text = read_file_text(src)
        logging.debug(f"Read content from file: {src} -> size: {len(body_text)}")
    else:
        logging.debug(f"text content (not file pointer) given in src param: {len(src)}")
        body_text = src

    soup=BeautifulSoup(body_text, "html.parser")
    return soup


def extract_text(soup:BeautifulSoup):
    """simple wrapper method to get text from soup (may be useful to extend later)"""
    return soup.text


def convert_html_to_markdown(soup:BeautifulSoup, subsection_tags: List[str]) -> str:
    """simplified and custom code to convert a subset of html to markdown"""
    start = 0
    tags = soup.find_all(subsection_tags)
    tag_count = len(tags)
    logging.info(f"\t\tsubsection tags: {len(tags)}")

    tag:BeautifulSoup
    for tag in tags:
        tag_name = tag.name
        depth = tag_name[1]
        new_heading = soup.new_tag(tag.name)
        new_heading.string = f"{'#' * int(depth)} {tag.text}"
        tag.replace_with(new_heading)
        logging.debug(f"\t\ttag:{tag.name} id:{tag.id}) (src line:{tag.sourceline}) : {tag.text}")
    txt = soup.text
    return txt


heading_regex = re.compile("^#+ (.*)")  # type: Pattern[str]
def split_by_md_heading(body_text:str, heading_regex: re.Pattern[str] = heading_regex) -> List[str]:
    sections_map = {}
    lines = body_text.split("\n")
    logging.info(f"\t\tline count: {len(lines)}")

    current_section_lines:List[str] = []
    line:str
    l_no = 0
    for line in lines:
        l_no += 1
        if(heading_regex.match(line)):
            if(current_section_lines):
                chunk:str = '\n'.join(current_section_lines)
                if(chunk.strip()):
                    sections_map[l_no] = chunk
                else:
                    logging.debug(f"{l_no}: empty chunk, no need to add? '{chunk.strip()}' (stripped())")
                current_section_lines = [line]
                logging.debug(f"\t\t{l_no}: Created section starting at {l_no}")
            else:
                logging.warning(f"\t\t{l_no}: No section lines??  {l_no}")
        else:
            current_section_lines.append(line)

    if(current_section_lines):
        chunk:str = '\n'.join(current_section_lines)
        sections_map[l_no] = chunk
        logging.debug(f"\t\tAdded last section starting at {l_no}: text len:{len(chunk)}")

    logging.debug(f"\t\tFound: {len(sections_map)}")
    return sections_map


pr = re.compile("^(.+) (.*)")
def split_section_to_paragraphs(section:str, para_regex= pr) -> List[str]:
    paras:List[str] = section.split("\n\s*\n\s*")
    return paras


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    source_text = read_file_text('../data/test4.html')
    soup = parse_html(source_text)

    headings = soup.find_all(heading_tags)
    heading : BeautifulSoup
    for heading in headings:
        htext = f'## {heading.text}'
        new_heading = soup.new_tag(heading.name)
        new_heading.string = "## mytest"
        heading.content = new_heading
        # heading.contents
        logging.debug('hacky markdown?')


    plain_text = extract_text(soup)
    logging.info(f"Content")
    print("More code here (add some default testing when running this library as a script)...")




# preformatteds = soup.find_all('pre')
# codes = soup.find_all('code')
# kbds = soup.find_all('kbd')
# tables = soup.find_all('table')

# sub_sections = split_subsections(soup, content_map, heading_tags)
# heading_tags = soup.find_all(heading_tags)
# for idx, heading in enumerate(heading_tags):
#     logging.info(f"{idx} [{heading.sourceline}:{heading.sourcepos}]) {heading}")
