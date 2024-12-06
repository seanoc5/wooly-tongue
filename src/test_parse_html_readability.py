#! /usr/bin/python
import sys
import time
from typing import List
from src.parse_html_readability import read_file_text, parse_html, convert_html_to_markdown, split_by_md_heading, split_section_to_paragraphs
import logging


class TestParseHtmlReadability:
    src_file = '../data/test4.html'
    heading_tags = ["h1", "h2", "h3", 'h4', 'h5', 'h6']
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    def test_read_text(self):
        source_text = read_file_text(self.src_file)
        assert type(source_text) is str
        assert len(source_text) >= 1044


    def test_parse_html(self):
        # source_text = read_file_text(src_file)
        # soup = parse_html(source_text)
        soup = parse_html(self.src_file)
        text = soup.text
        assert type(text)==str
        assert len(text) >= 470
        lines = text.split('\n')
        assert len(lines) >= 18

    def test_convert_html_markdown(self):
        soup = parse_html(self.src_file)
        text = convert_html_to_markdown(soup, self.heading_tags)
        lines :List[str] = text.split('\n')
        headings = list(filter(lambda l : l.startswith('#') , lines))
        assert headings[0] == '# Test Span: First Heading'
        assert headings[1] == '## Second Heading'
        assert headings[2] == '### test title'


    def test_parse_heading_sections(self):
        soup = parse_html(self.src_file)
        lines = convert_html_to_markdown(soup, self.heading_tags)
        sections = split_by_md_heading(lines)
        for section in sections:
            logging.info(f"Section: {section}")
        assert len(sections) == 2

    def test_split_section_to_paragraphs(self):
        section:str = '''
    First Paragraph, first sentence.
    P1 sentence 2. P1 sentence3.
    
        Second Paragraph, second sentence. p2 - s2. 
        Third Paragraph w/spaces (more code needed to catch this one...). Second sentence
        Fourth paragraph (with tab?).
    '''
        paras = split_section_to_paragraphs(section)


    # headings = soup.find_all(heading_tags)
    # heading : BeautifulSoup
    # for heading in headings:
    #     htext = f'## {heading.text}'
    #     new_heading = soup.new_tag(heading.name)
    #     new_heading.string = "## mytest"
    #     heading.content = new_heading
    #     # heading.contents
    #     logging.debug('hacky markdown?')


