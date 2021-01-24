#################################
#para cargar nlp con tokenizer y sentencizer
#NO FUNCIONA, CUANDO VA A PROCESAR EL TEXTO TIRA EROR, DICE COMO QUE
#LE ESTOY PASANDO UN DOC PORQUE SEA QUE PRIMERO SE EJECUTE EL sentencizer
#O EL TOKENIZER, EL SEGUNDO ESPERA UN STRING PERO RECIBE UN DOC
#SON COMPONENTES PARA USAR SOLOS, NO DENTRO DE UN PIPELINE
#POR ESO CARGO DOS VECES EL MODELO, UNA CON CADA COMPONENTE
import spacy
import re
from pathlib import Path
import os

nlp = spacy.load("es_core_news_md",  disable=["tagger", "parser", "ner"])

#procesa con la funcion preprocess_files() los archivos que están en ./raw_texts
#y los almacena en ./training_corpus
class Preprocessor(object):

	def sentencize_file(self, str):
		data_folder = Path("./raw_texts")
		data_path = data_folder / str
		with data_path.open("r") as f:
			text=f.read()
			f.close()
		text=text.replace('\u200b', '')
		text=re.sub(r'\.\d+', '.', text)
		text=re.sub(r'(?<=\w)\—', '', text)
		text=re.sub(r':', '.', text)
		text=re.sub(r'\s\—', '. ', text)
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

	def preprocess_files(self):
		sentencizer = nlp.create_pipe("sentencizer")
		nlp.add_pipe(sentencizer)
		tokenizer = nlp.Defaults.create_tokenizer(nlp)
		for fname in os.listdir("./raw_texts"):
			doc = self.sentencize_file(fname)
			final_sents = self.tokenize_file(doc, tokenizer)
			self.save_lines(fname, final_sents)


preprocessor = Preprocessor()
preprocessor.preprocess_files()
