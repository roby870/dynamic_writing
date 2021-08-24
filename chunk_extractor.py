import spacy
from pathlib import Path
from spacy.tokens import DocBin
from spacy.tokens import Doc
from core_classes.tokens import *
from core_classes.chunks import *
from core_classes.sequences import *
from filters.gramatical_filters import *
from filters.similarity_filters import *
from filters.word_filters import *
from utils.utils import *

"""no existe la extensión source en la clase Doc
tal como está implementada en SpaCy, pero lo forzamos
para que no levante un error en las sucesivas cargas de este script
en la fase de desarrollo del proyecto"""

Doc.set_extension("source", default='', force=True) 
													
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
	def __read_doc_bin(self, num_docs_folder):
		data_folder = Path("./raw_texts/" + num_docs_folder)
		data_path = data_folder / ("doc_bins" + num_docs_folder)
		with data_path.open("rb") as f:
		    bytes_data = f.read()
		    f.close()
		return bytes_data

	def __transform_doc_bins_to_docs(self, bytes_data):
		doc_bin = DocBin(store_user_data=True).from_bytes(bytes_data)
		docs = list(doc_bin.get_docs(self.model.vocab))
		return docs

    # retorna una lista con todo lo minado (a partir de la funcion lambda) en los textos presentes en el directorio raw_texts
	def process_files(self, num_docs_folder, process_function, *args):
		bytes_data = self.__read_doc_bin(num_docs_folder)
		docs = self.__transform_doc_bins_to_docs(bytes_data)
		results = []
		for doc in docs:
		    result = process_function(doc, *args)
		    results = results + result
		results = remove_last_spaces(results)
		results = set_chunks_list(results)
		return results
