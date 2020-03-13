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
    doc_word_count: Dict[str:int]
    term_freq_by_doc: Dict[Tuple(str, str): int]
    is_term_in_query: Set

    def init_doc_query(self, search_path, query):
        self.doc_paths = glob(path.join(search_path, "*.tsv"))
        self.query = query
        for term in query:
            self.is_term_in_query.add(term)

    def init_term_freq(self):
        for dp in self.doc_paths:
            html = open(dp).read()
            raw = BeautifulSoup(html)
            filtered = raw.find_all('p')
            text = [line.text for line in filtered]
            self.doc_word_count[dp] = 0
            for row in text:
                self.doc_word_count[dp] += len(row)
                self.doc_content.append([row])
                for term in row:
                    if self.is_term_in_query[term]:
                        self.term_freq_by_doc[(dp, term)] += 1

    def bm25_score(self, doc_path, query):
        N = sum(len(d) for d in self.doc_content)
        IDF = lambda qi : log2( (N - self.term_freq_by_doc[(doc_path, qi)] + 0.5) / self.term_freq_by_doc[(doc_path, qi)] + 0.5)



#to_remove = soup.find_all("div") 