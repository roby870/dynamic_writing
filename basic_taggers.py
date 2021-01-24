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


#taggea todos los textos del directorio num_docs_folder dentro del directorio raw_texts
#y guarda los docs resultantes como docbins en el archivo que llama "doc_bins" dentro
#de ese mismo directorio

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
