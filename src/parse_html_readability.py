#! /usr/bin/python
import os
import time
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import sys
import logging


SECTION = 'section'
content_map = defaultdict(lambda: [])
heading_tags = ["h1", "h2", "h3", 'h4', 'h5', 'h6']

def read_file_text(src, ):
    logging.info(f'using source: {src}')
    source_text = open(src).read()
    return source_text

def parse_html(src: str) -> BeautifulSoup:
    body_text:str

    if os.path.exists(src):
        body_text = read_file_text(src)
        logging.info(f"Read content from file: {src} -> size: {len(body_text)}")
    else:
        logging.info(f"content given in src param: {len(src)}")
        body_text = src

    soup=BeautifulSoup(body_text, "html.parser")

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

    return soup


def extract_text(soup:BeautifulSoup):
    return soup.text

# def split_sections(soup, content_map, section_tags = [SECTION]) -> dict:
#     sections = soup.find_all(section_tags)
#     if(sections):
#         logging.info(f"Section count: {len(sections)}")
#         content_map['sections'] = sections
#     else:
#         logging.info("No sections!!")
#     return content_map


def split_sections_by_tags(soup, content_map, subsection_tags) -> dict:
    start = 0
    content = extract_text(soup)
    tags = soup.find_all(subsection_tags)
    tag:BeautifulSoup
    for tag in tags:
        tag_name = tag.name
        depth = tag_name[1]
        # if(
        new_heading = soup.new_tag(heading.name)
        htext = f"{'#' * depth} { heading.text}"

        logging.info(f"\t\t{tag.name}:{tag.id}) ({tag.sourceline}) : {tag.text}")

        htext = f'## {heading.text}'
        new_heading = soup.new_tag(heading.name)
        new_heading.string = "## mytest"
        heading.content = new_heading
        # heading.contents
        logging.debug('hacky markdown?')



    return content_map



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

    # preformatteds = soup.find_all('pre')
    # codes = soup.find_all('code')
    # kbds = soup.find_all('kbd')
    # tables = soup.find_all('table')

    # sub_sections = split_subsections(soup, content_map, heading_tags)
    # heading_tags = soup.find_all(heading_tags)
    # for idx, heading in enumerate(heading_tags):
    #     logging.info(f"{idx} [{heading.sourceline}:{heading.sourcepos}]) {heading}")
    logging.info(f"Content")
