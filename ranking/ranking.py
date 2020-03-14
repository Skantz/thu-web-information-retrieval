import csv
import argparse
import typing
import sys
import locale
import numpy as np
from typing import List, Set, Dict, Tuple
from dataclasses import dataclass

from bs4 import BeautifulSoup
from math import log2
from glob import glob
from os import path

from VSM import vsm

locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

#html = open("Query_1/Document/2.html").read()
#soup = BeautifulSoup(html)
#bs_text = soup.find_all('p')
#
#for html_snippet in bs_text:
#    print(html_snippet.text)

#input - glob path for documents, and a query document

@dataclass
class DocumentQuery:
    doc_paths: List[str]
    query: str
    doc_content: List[List[str]]
    doc_word_count: Dict[str, int]
    term_freq_by_doc: Dict[Tuple[str, str], int]
    is_term_in_query: Set
    term_freq_corpus: Dict[str, int]

    def init_doc_query(self, query, doc_paths):
        #self.doc_paths = glob(path.join(search_path, "*.tsv"))
        self.doc_paths = doc_paths
        for term in query:
            self.is_term_in_query.add(term)
        for doc in doc_paths:
            for term in self.query:
                self.term_freq_by_doc[(doc, term)] = 0

    def init_term_freq(self):
        for dp in self.doc_paths:
            html = open(dp).read()
            raw = BeautifulSoup(html)
            filtered = raw.find_all('p')
            text = [line.text for line in filtered]
            self.doc_word_count[dp] = 0
            for idx, row in enumerate(text):
                if idx == 0:
                    print("Sample row from", dp, ":", row)
                row = row.lower()
                row = row.split(" ")
                self.doc_word_count[dp] += len(row)
                self.doc_content.append([row])
                for term in row:
                    if term in self.is_term_in_query:
                        self.term_freq_by_doc[(dp, term)] += 1

    def bm25_score(self, query, doc_path):
        k1, b = 1.60, 0.75
        N = 10**9
        avdl = 500
        D_size = sum([len(d) for d in self.doc_content])
        IDF = lambda qi, doc_path: log2(max(1, (N - self.term_freq_corpus[qi] + 0.5)
                                          / (self.term_freq_corpus[qi] + 0.5)))
        IDF_no_log = lambda qi, doc_path: (N - self.term_freq_corpus[qi] + 0.5) \
                                          / (self.term_freq_corpus[qi] + 0.5)

        numer = lambda qi, doc_path: self.term_freq_by_doc[(doc_path, qi)] * (k1 + 1)
        denom = lambda qi, doc_path: self.term_freq_by_doc[(doc_path, qi)] + k1 * (1 - b + b * D_size / avdl) 

        return sum([IDF(qi, doc_path) * numer(qi, doc_path) / denom(qi, doc_path) for qi in query])

def io():

    parser = argparse.ArgumentParser(description='Compute BM25 and VSM on documents')
    parser.add_argument('-q', type=str, required=False, #nargs=1,
                        help='search string')
    parser.add_argument('-qf', required=False, nargs='*',
                        help='Read queries from file instead of stdio')
    parser.add_argument('-d', dest='docs', required=True, nargs="+", help='Path to html documents')
    parser.add_argument('-r', required=False, nargs='?', help='Path to pre-computed frequency list. Format is word - frequency')
    args = parser.parse_args()

    queries = []
    if args.q is None and args.qf is None:
        parser.error("at least one of -q and -f is required")

    if args.qf is not None:
        for qf in args.qf:
            with open(qf, "r") as f:
                queries += [line.split("\t")[0].lower() for i, line in enumerate(f) if i != 0]
        print(args.qf)
        print(queries)
    else:
        queries = [args.q]

    term_freq_corpus = {}
    if args.r != None:
        with open(args.r, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue
                split = line.split(maxsplit=2)
                try:
                    term_freq_corpus[split[0].lower()] = locale.atoi(split[1].lower())
                except ValueError:
                    pass
                try:
                    term_freq_corpus[split[0].lower()] = locale.atoi(split[1].strip('\"').lower())
                except ValueError:
                    print("Can't parse frequency value. Ignoring")
                    continue
            print(term_freq_corpus)

    return queries, args.docs, term_freq_corpus

def main():
    """Provide a search query and a document folder path on standard input"""
    """Calculates BM25 and VSM score"""

    queries, docs, term_freq_corpus = io() 
    DocQ = DocumentQuery(docs, queries[0].split(" "), [], {}, {}, set(), term_freq_corpus)
    #print(queries[0].split(" "))
    DocQ.init_doc_query(queries[0].split(" "), docs)
    DocQ.init_term_freq()
    for i, d in enumerate(docs):
        bm25 = DocQ.bm25_score(queries[0].split(" "), d)
        print(docs[i], bm25)

    vsm.document_filenames = {i:d for i, d in enumerate(docs)}
    vsm.N = len(docs)
    vsm.query = queries[0]
    vsm.initialize_terms_and_postings()
    vsm.initialize_document_frequencies()
    vsm.initialize_lengths()
    vsm.do_search()

if __name__ == "__main__":
    #html = open("Query_1/Document/2.html").read()
    #soup = BeautifulSoup(html)
    #bs_text = soup.find_all('p')
    #for html_snippet in bs_text:
    #    print(html_snippet.text)

    #input - glob path for documents, and a query document
    main()


#to_remove = soup.find_all("div") 