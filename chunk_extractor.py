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
	def __init__(self, model):
		self._model = model

    @property 	
	def model(self):
		return self._model

	@model.setter
	def model(self, model):
		self._model = model

	@model.deleter
	def model(self):
		del self._model

    #lee y retorna los doc bins presentes en la carpeta num_docs_folder
    def __read_doc_bin(num_docs_folder):
        data_folder = Path("./raw_texts/" + num_docs_folder)
        data_path = data_folder / ("doc_bins" + num_docs_folder)
        with data_path.open("rb") as f:
            bytes_data = f.read()
            f.close()
        return bytes_data

    def __transform_doc_bins_to_docs(bytes_data):
        doc_bin = DocBin(store_user_data=True).from_bytes(bytes_data)
        docs = list(doc_bin.get_docs(self.model.vocab))
        return docs

    # retorna una lista con todo lo minado (a partir de la funcion lambda) en los textos presentes en el directorio raw_texts
    def process_files(num_docs_folder, filter, process_function, *args):
        bytes_data = self.__read_doc_bin(num_docs_folder)
        docs = self.__transform_doc_bins_to_docs(bytes_data)
        results = []
        for doc in docs:
            result = filter.process_function(doc, *args)
            results = results + result
        results = remove_last_spaces(results)
        results = set_chunks_list(results)
        return results
