#! /usr/bin/python
import time
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

SECTION = 'section'
content_map = defaultdict(lambda: [])

def read_file_text(src, ):
    logging.info(f'using source: {src}')
    source_text = open(src).read()
    return source_text

def parse_html(source_text: str) -> BeautifulSoup:
    soup=BeautifulSoup(source_text, "html.parser")
    first_tag:BeautifulSoup = soup.currentTag
    foo_tags = first_tag.children

    # the rest is debugging/test
    tag : BeautifulSoup
    bar = first_tag.descendants
    for tag in bar:
        if(tag.name):
            if(tag.has_attr('id')):
                id = tag['id']
            else:
                logging.debug(f"no id")
            logging.info(f"tag id:{id}: {tag.name}")
        else:
            logging.debug(f"foo tag: {tag.name}")
    # children = first_tag.
    # foo_tags = soup.

    return soup


def extract_text(soup:BeautifulSoup):
    return soup.text

def split_sections(soup, content_map, section_tags = [SECTION]) -> dict:
    sections = soup.find_all(section_tags)
    if(sections):
        logging.info(f"Section count: {len(sections)}")
        content_map['sections'] = sections
    else:
        logging.info("No sections!!")
    return content_map

def split_subsections(soup, content_map, subsection_tags=["h1", "h2", "h3", 'h4', 'h5', 'h6']) -> dict:
    # logging.info(f"Section: {sect.sourceline}")
    start = 0
    content = extract_text(soup)
    tags = soup.find_all(subsection_tags)
    for tag in tags:
        logging.info(f"\t\t{tag.name}:{tag.id}) ({tag.sourceline}) : {tag.text}")


    return content_map


# def walk_nodes(soup:BeautifulSoup):


if __name__ == "__main__":
    source_text = read_file_text('../data/test3.html')
    soup = parse_html(source_text)

    heading_tags = ["h1", "h2", "h3", 'h4', 'h5', 'h6']
    headings = soup.find_all(heading_tags)
    heading : BeautifulSoup
    for heading in headings:
        htext = f'## {heading.text}'
        new_heading = soup.new_tag(heading.name)
        new_heading.string = "## mytest"
        heading.content = new_heading
        # heading.contents
        logging.debug('hacky markdown?')


    # sections = split_sections(soup, content_map)

    plain_text = extract_text(soup)

    # preformatteds = soup.find_all('pre')
    # codes = soup.find_all('code')
    # kbds = soup.find_all('kbd')
    # tables = soup.find_all('table')

    # sub_sections = split_subsections(soup, content_map, heading_tags)
    # heading_tags = soup.find_all(heading_tags)
    # for idx, heading in enumerate(heading_tags):
    #     logging.info(f"{idx} [{heading.sourceline}:{heading.sourcepos}]) {heading}")
    logging.info(f"Content")
