import spacy
import re
from pathlib import Path
import os

nlp = spacy.load("es_core_news_md",  disable=["tagger", "parser", "ner"])

"""procesa con la funcion preprocess_files() los archivos que están en ./raw_texts
y los almacena en ./training_corpus. La limpieza que hace está pensada en función
tanto de la forma en la que Gensim espera los textos para alimentar a sus algoritmos como
de las características de los textos del proyecto Scriptorium, comentar cualquier regex
que se quiera suprimir para un prcesamiento determinado o descomentar la que se necesite
de las comentadas"""

class Preprocessor(object):

	def sentencize_file(self, str):
		data_folder = Path("./raw_texts")
		data_path = data_folder / str
		with data_path.open("r") as f:
			text=f.read()
			f.close()
		text=text.replace('\u200b', '')
		text=re.sub(r'\{.+\}', '', text) #texto entre llaves
		text=re.sub(r'\[.+\]', '', text) #texto entre corchetes
		text=re.sub(r'\*', '', text)     #asteriscos
		text=re.sub(r'\.\d+', '.', text) #dígitos
		text=re.sub(r'(?<=\w)\—', '', text) #guiones de diálogo
		text=re.sub(r':', '.', text) #dos puntos
		text=re.sub(r'\s\—', '. ', text) #guiones de diálogo
		text=re.sub(r'\[\d+\]', '', text) #dígitos entre corchetes (innesesaria si no se comenta la de los dígitos)
		#si se quieren eliminar los títulos de los capítulos con números romanos:
		#re.sub(r"CAPÍTULO\s[A-Z]{1,7}", '', text)
		#Lo mismo pero en minúscula e indicando el \n:
		#re.sub(r"Capítulo\s[A-Z]{1,7}\n", '', texto)
		#si se quieren eliminar líneas escritas en mayúsculas (puede servir para titulos de capítulos):
		#text=re.sub(r"(([A-Z]|[ÁÉÍÓÚÑÜ])(\W|\s)*)+\n", '', text)
		#Si se quiere agregar un punto para delimitar como oraciones todas las líneas que no tienen punto final(muy útil para epigrafes):
		#texto = re.sub(r"(?<=\w)\n", '.', texto)
		doc = nlp(text)
		return doc

	def tokenize_file(self, doc, tokenizer):
		final_sents = []
		for s in doc.sents:
			doc_t=tokenizer(s.text)
			final_sent = []
			for token in doc_t:
				if (token.is_alpha):
					final_sent.append(token.text.lower())
			if len(final_sent) > 1:  #filtra las listas vacias o las de una sola palabra
				final_sents.append(final_sent)
		return final_sents

	def save_lines(self, str, final_sents):
		data_folder = Path("./training_corpus")
		data_path = data_folder / str
		with data_path.open('w') as f:
			for list in final_sents:
				for item in list:
					f.write("%s " % item)
				f.write("\n")
			f.close()

"""para cargar nlp con tokenizer y sentencizer
no funciona, cuando va a procesar el texto levanta un eror,
señala el tipo de dato doc como erróneo porque sea que primero se ejecute el sentencizer
o el tokenizer, el segundo componente espera un string pero recibe un doc.
son componentes pensados para usar por separado, no dentro de un pipeline.
por eso cargo dos veces el modelo, una con cada componente"""

	def preprocess_files(self):
		nlp.add_pipe('sentencizer')
		tokenizer = nlp.tokenizer
		for fname in os.listdir("./raw_texts"):
			doc = self.sentencize_file(fname)
			final_sents = self.tokenize_file(doc, tokenizer)
			self.save_lines(fname, final_sents)


preprocessor = Preprocessor()
preprocessor.preprocess_files()
