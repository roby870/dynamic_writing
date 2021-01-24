import pickle
import os
from spacy.tokens import DocBin
from pathlib import Path


#lee el archivo llamado str en el directorio raw_texts y retorna un doc

def tag_file(str, model):
	data_folder = Path("./raw_texts")
	data_path = data_folder / str
	with data_path.open("r") as f:
		text=f.read()
		f.close()
	doc = model(text)
	return doc


#taggea todos los textos del directorio raw_texts y guarda los docs resultantes
#como docbins en el archivo que llama "doc_bins"

def tag_files(model, num_docs_folder):
	doc_bin = DocBin(attrs=["LEMMA", "POS", "TAG", "DEP", "HEAD"], store_user_data=True)
	data_folder = Path("./raw_texts/" + num_docs_folder)
	texts = []
	for fname in os.listdir("./raw_texts/" + num_docs_folder):
		data_path = data_folder / fname
		with data_path.open("r") as f:
			text=f.read()
			f.close()
		doc = model(text)
		doc._.source = fname
		doc_bin.add(doc)
	bytes_data = doc_bin.to_bytes()
	data_path = data_folder / ("doc_bins" + num_docs_folder)
	with data_path.open("wb") as f:
		f.write(bytes_data)
		f.close()


def save_pickle(results, name_results):
	name_results = './pickles/' + name_results + '.pkl'
	with open(name_results, 'wb') as f:
		pickle.dump(results, f)
		f.close()


def load_pickle(name_pickle):
	with open('./pickles/' + name_pickle + '.pkl', 'rb') as f:
		pickle_object = pickle.load(f)
		f.close()
	return pickle_object
