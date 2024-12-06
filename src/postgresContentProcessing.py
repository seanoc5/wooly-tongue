# https://github.com/langchain-ai/langchain/issues/6952
import logging
import sys
from collections import defaultdict
from typing import List

import spacy
import psycopg2
from psycopg2.extras import RealDictCursor
from bs4 import BeautifulSoup
# from langchain.vectorstores import Chroma
# from langchain_community.vectorstores import Chroma
# from langchain.document_loaders import TextLoader
# from langchain_community.document_loaders import TextLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from spacy import displacy

from rich.console import Console
from rich.logging import RichHandler

from src.parse_html_readability import parse_html, extract_text, convert_html_to_markdown, split_by_md_heading

# POS: https://universaldependencies.org/u/pos/

error_console = Console(stderr=True, width=210)
width = error_console.width
# from logging.handlers import  RotatingFileHandler
# LOGFORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# LOGFORMAT = '%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
LOGFORMAT = '%(message)s'
rh = RichHandler(console=error_console)
rh.setFormatter(logging.Formatter(LOGFORMAT))

logging.basicConfig(format=LOGFORMAT, level=logging.INFO, handlers=[rh])
log = logging.getLogger(__name__)
log.info("Starting...")

# Connect to the PostgreSQL database
conn = psycopg2.connect(host="dell", dbname="cm_dev", user="sean", password="pass1234")
# Create a cursor object
cursor = conn.cursor(cursor_factory=RealDictCursor)
# Execute a query to retrieve 10 records from the database
cursor.execute("SELECT id,uri, title, structured_content FROM content where structured_size > 100 AND structured_size < 10000 LIMIT 10")

# Fetch the results of the query
records = cursor.fetchall()


spacy.require_gpu()
model_name = 'en_core_web_trf'
nlp = spacy.load(model_name)

content_map = defaultdict(lambda: [])
heading_tags = ["h1", "h2", "h3", 'h4', 'h5', 'h6']

# Process each record and extract the content_html field
rec_no:int = 0
for record in records:
    rec_no += 1
    id = record['id']
    uri = record['uri']
    title = record['title']
    log.info(f"{rec_no}) Processing title:[{title}] -- id:{id}")

    # Extract the content_html field from the record
    content_html = record['structured_content']

    soup = parse_html(content_html)
    md_text = convert_html_to_markdown(soup, heading_tags)

    sections = split_by_md_heading(md_text)
    for section_key in sections:
        section:str = sections[section_key]
        logging.debug(f"\t\tSection key({section_key}): text len:{len(section)}")

        # Parse the HTML content using SpaCy
        parsed_html = nlp(section)

        entities = parsed_html.ents
        sentences = list(parsed_html.sents)
        verbs:List[str] = []
        advs:List[str] = []
        prons:List[str] = []
        nouns:List[str] = []
        adjs:List[str] = []
        syms:List[str] = []
        # Extract all the text from the parsed HTML content
    for t in parsed_html:
        position = t.pos
        pos = t.pos_
        if(pos == 'VERB'):
            verbs.append(t.text)

        elif(pos == 'ADV'):
            advs.append(t.text)

        elif(pos == 'PRON'):
            prons.append(t.text)

        elif(pos == 'NOUN' or pos == 'PROPN'):
            nouns.append(t.text)

        elif(pos == 'ADJ'):
            adjs.append(t.text)

        elif(pos == 'SYM'):
            syms.append(t.text)

        elif(pos == 'SPACE' or pos == 'PUNCT' or pos == 'X' or pos == 'PART' or pos == 'AUX'):
            log.debug(f"\t\t\tSkip PUNCT/SPACE: pos:{pos} -- text:[{t.text.strip()}]")

        elif(pos == 'NUM'):
            log.debug(f"\t\t\tSkip NUMBER: pos:{pos} -- text:'{t.text}'")

        elif(t.is_punct):
            log.debug(f"{rec_no}:{position}) {t.text} -- POS:{pos}")

        elif(t.is_alpha):
            if(t.is_stop):
                log.debug(f"{rec_no}:{position}) {t.text} -- STOP POS:{pos}")
            else:
                log.debug(f"{rec_no}:{position}) {t.text} -- POS:{pos}")

        else:
            log.info(f"\t\t{rec_no}::{position}) '{t.text}' --> POS:{pos} :: (isAlpha: {t.is_alpha}) -- (isStop: {t.is_stop})")

    # for chunk in parsed_html.noun_chunks:
    #     log.debug(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)

    logging.debug(f"next record/content-doc...")


log.info("done?!")




# doc = nlp_trf(source_text)
# Initialize the SpaCy model
# nlp = displacy(lang="en", options={"ents": "yes"})

