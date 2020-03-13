import typing
from typing import List, Set, Dict, Tuple
from dataclasses import dataclass
from bs4 import BeautifulSoup
from math import log2
from glob import glob
from os import path

html = open("Query_1/Document/2.html").read()
soup = BeautifulSoup(html)
bs_text = soup.find_all('p')

for html_snippet in bs_text:
    print(html_snippet.text)

#input - glob path for documents, and a query document

@dataclass
class DocumentQuery:
    doc_paths: List[str]
    query: str

    doc_content: List[List[str]]   
    doc_length: Dict[int]
    term_freq_by_doc: Dict[Tuple(str, str): int]
    is_word_in_doc: Set

def prepare_bm25_stats(search_path: str, user_query: str):
    doc_paths = glob(path.join(search_path, "*.tsv"))
    

    pass

def calc_term_freq(doc: List[str], term: List[str]):
    term_freq = {w:0 for w in term}
    term_set = set(term)
    for line in doc:
        for word in line:
            if word in term_set:
                term_freq[word] += 1
    return term_freq


def bm25_score(D, Q):
    IDF = lambda qi, N, ćount_word_in_doc: log2( (N - count_word_in_doc[qi] + 0.5) / count_word_in_doc[qi] + 0.5)


#to_remove = soup.find_all("div") 