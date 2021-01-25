import spacy
from pathlib import Path
import os
import re
from spacy.tokens import DocBin
from spacy.tokens import Doc
from tokens import *
from chunks import *
from sequences import *
from basic_parser import *
from gramatical_filters import *
from similarity_filters import *
from word_filters import *
from utils import *

Doc.set_extension("source", default='')

class Chunk_Extractor(object):

    #lee y retorna los doc bins presentes en la carpeta num_docs_folder
    def read_doc_bin(num_docs_folder):
        data_folder = Path("./raw_texts/" + num_docs_folder)
        data_path = data_folder / ("doc_bins" + num_docs_folder)
        with data_path.open("rb") as f:
            bytes_data = f.read()
            f.close()
        return bytes_data

    def transform_doc_bins_to_docs(bytes_data, model):
        doc_bin = DocBin(store_user_data=True).from_bytes(bytes_data)
        docs = list(doc_bin.get_docs(model.vocab))
        return docs

    # retorna una lista con todo lo minado (a partir de la funcion lambda) en los textos presentes en el directorio raw_texts
    def process_files(model, gensim_model, num_docs_folder, process_function, *args):
        bytes_data = read_doc_bin(num_docs_folder)
        docs = transform_doc_bins_to_docs(bytes_data, model)
        results = []
        for doc in docs:
            result = process_function(doc, gensim_model, *args)
            results = results + result
        results = remove_last_spaces(results)
        results = set_chunks_list(results)
        return results
