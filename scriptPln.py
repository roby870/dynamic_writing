import spacy
from spacy import displacy
from spacy.tokens import DocBin
from pathlib import Path
import numpy as np

nlp = spacy.load("es_core_news_md")


# Busca en el documento str todos los tokes taggeados como dep_tag y si el subárbol de dependencias
#sintácticas que tiene a ese token como núcleo es de longitud (en tokens) mayor a 1 y menor a 7
#lo selecciona. Luego guarda todos los subárboles (como binarios) en un nuevo archivo que se va a titular
#"nombre original del archivo + _chunks_ + tipo de chunk"

def extraer_arboles_dep_tag(str, dep_tag):
	data_folder = Path("./")  #lee el archivo llamado str que se encuentra en el directorio
	data_path = data_folder / str #donde se ejecuta esta función
	with data_path.open("r") as f:
		textos=f.read()
		f.close()
	########
	chunks = []
	########
	doc = nlp(textos) #nlp.pipe con un texto solo no me funciona
	for token in doc:
		if token.dep_ == dep_tag:
			length_subtree = len(list(token.subtree))
			if (length_subtree > 1 and length_subtree < 7): #solo guarda árboles de extensión menor a 7 tokens
				begin=list(token.subtree)[0].i
				end=list(token.subtree)[-1].i
				span=doc[begin:end+1]
				chunks.append(span)
	########
	final_answer = []
	for c in chunks:
	    final_answer.append(c.as_doc()) #en lugar de guardar los chunks como spans los guarda como docs
	doc_bin = DocBin()
	for doc in final_answer:
        	doc_bin.add(doc) #uso de clase DocBin por eficiencia y luego los guarda como binarios
	bytes_data = doc_bin.to_bytes()
	########
	data_folder = Path("./")
	data_path = data_folder / (str + "_chunks_" + dep_tag) #nombre original del archivo + tipo de chunk
	with data_path.open("wb") as f:
		f.write(bytes_data)
		f.close()


#retorna los subárboles de la función extraer_arboles_dep_tag como una lista de docs
#str es el nombre del archivo donde están guardados los subárboles (los retorna como docs)

def leer_chunks(str):
	data_folder = Path("./")
	data_path = data_folder / str
	with data_path.open("rb") as f:
		leido=f.read()
		f.close()
	doc_bin = DocBin().from_bytes(leido)
	docs = list(doc_bin.get_docs(nlp.vocab))
	return docs


#hace un merge entre cada nsubj y el advcl mas similar

def merge_chunks(nsubj_chunks, advcl_chunks):
	sentences = []
	for nsubj in nsubj_chunks:
		max_score = 0
		for advcl in advcl_chunks:
		#actualizo el advcl si tiene un valor de simulitud mayor que los anteriores
			score = nsubj.similarity(advcl)
			if score > max_score:
				max_score = score
				selected_advcl = advcl
		#mergear sintagmas y guardar en sentences
		sentences.append(nsubj.text + ' ' + selected_advcl.text)
	return sentences #retorna una lista de strings


#lee el archivo llamado str en el directorio actual y retorna un doc

def tag_file(str):
	data_folder = Path("./")
	data_path = data_folder / str
	with data_path.open("r") as f:
		text=f.read()
		f.close()
	doc = nlp(text)
	return doc


#lee los archivos str_list y los retorna como docs
#con 4 novelas se rompe, problemas con la alocacion de memoria

def tag_files(str_list):
	data_folder = Path("./")
	texts = []
	for str in str_list:
		data_path = data_folder / str
		with data_path.open("r") as f:
			text=f.read()
			f.close()
			texts.append(text)
	docs = nlp.pipe(texts, batch_size=50)
	return docs


#recibe una cadena de tags(pos_tags, lista de strings),
#busca en doc un token que esté taggeado como dep_tag y
#si su subtree es una secuencia de tokens taggeada como
#pos_tags, la selecciona. Retorna todas las seleccionadas (spans)

def process(doc, dep_tag, pos_tags):
	chunks=[]
	chunk_length = len(pos_tags)
	for token in doc:
		if token.dep_ == dep_tag:
			subtree = list(token.subtree)
			chunk = []
			if (chunk_length <= len(subtree)): #este if se debe a que si no estuviera y se incluyen subtrees de menor length del
				for i in range(chunk_length): #chunk_length aca en este otro if se rompe
					if (subtree[i].pos_ != pos_tags[i]):
					 	break
					elif(i == (chunk_length - 1)): #chequea si esta en la ultima vuelta, en ese caso guarda la secuencia de tokens como span
						begin=list(token.subtree)[0].i
						end=list(token.subtree)[chunk_length - 1].i
						span=doc[begin:end+1]
						chunks.append(span)
	return chunks #retorna una lista de spans


#Ejemplos de invocación de la función process
nsubj=process(doc, "nsubj", ["DET", "NOUN"])#nominal subject
nmod=process(doc, "nmod", ["ADP","DET", "NOUN"])#modificadores nominales
obj=process(doc, "obj", ["DET", "NOUN"])#objetos
pron_verb_adj=process(doc, "root", ["PRON", "VERB", "ADJ"])
lanzallamas_adj=process(lanzallamas, "amod", ["ADJ"])#modificadores adjetivos


#busca bigramas de pos AUX + tag que responda a las caracteristicas de
#genero, número y tiempo parametrizadas

def process_bigrams_verbs_with_auxiliar(doc, gender, number, tense):
	bigrams = []
	for token in doc:
		if token.pos_ == "AUX": #cuando se encuentra con un auxiliar, chequea que el verbo conjugado adyacente presente las condiciones parametrizadas
			if (("Gender=" + gender) not in token.nbor().tag_) or (("Tense=" + tense) not in token.tag_) or (("Number=" + number) not in token.nbor().tag_):
				continue
			else:
				begin=token.i
				end=token.nbor().i
				span=doc[begin:end+1]
				bigrams.append(span)
	return bigrams #retorna una lista de spans


#busca verbos con las caracteristicas indicadas
def process_one_word_verbs(doc, person, number, tense, mood):
	verbs = []
	for token in doc:
		if token.pos_ == "VERB":
			if (("Person=" + person) not in token.tag_) or (("Tense=" + tense) not in token.tag_) or (("Number=" + number) not in token.tag_) or (("Mood=" + mood) not in token.tag_):
				continue
			else:
				index=token.i
				span=doc[index]
				verbs.append(span)
	return verbs #retorna una lista de spans


#ejemplo de uso de la función process_one_word_verbs
root_3_sing_imp_ind=process_one_word_verbs(doc, "3", "Sing", "Imp", "Ind")


#generación de texto basada en una regla propia de una gramática libre de contexto
import random
print(random.choice(nsubj).text + ' ' + random.choice(nmod).text + ' ' + random.choice(root_3_sing_imp_ind).text + ' ' + random.choice(obj).text)

def generate(n):
	for i in range(n):
		print(random.choice(nsubj).text + ' ' + random.choice(nmod).text + ' ' + random.choice(root_3_sing_imp_ind).text + ' ' + random.choice(obj).text)


lines=[]
for line in open("11del02del20.txt"):
	lines.append(line)

lines_set=set(lines)

with data_path.open("w") as f:
	for item in lines_set:
		f.write("%s" % item)
		f.close()

####################################################
####################################################
####################################################


#retorna las n palabras más similares a word

def most_similar_words(doc, word, n):
	words = []
	for token in doc:
		if (token and token.has_vector and (token.text != word.text)): #ATENCION A ESTO, IGNORA LAS PALABRAS IGUALES, PERO SI SE QUIEREN ORACIONES O FRASES (NO PALABRAS SUELTAS) CON CONTEXTO SIMILAR (el token guarda información sobre su posición en el texto) LO IDEAL ES GUARDAR LAS MISMAS PALABRAS TAMBIEN
			words.append(token)
	closest = []
	for key in sorted(words, key=lambda x: word.similarity(x), reverse=True)[:n]:
		closest.append(key.text)
	return set(closest)


#igual a la anterior pero devuelve tokens en lugar de strings

def most_similar_tokens_random_set(doc, word, n):
	words = []
	for token in doc:
		if (token and token.has_vector and (token.text != word.text)):
			words.append(token)
	closest = []
	for key in sorted(words, key=lambda x: word.similarity(x), reverse=True)[:n]:
		closest.append(key)
	tokens_set_texts = []
	tokens_set = []
	for token in closest:
		if(token.text not in tokens_set_texts):
			tokens_set.append(token)
			tokens_set_texts.append(token.text)
	return tokens_set


#igual a la anterior pero devuelve tokens repetidos porque todos pertenecen a oraciones diferentes

def most_similar_tokens(doc, word, n):
	words = []
	for token in doc:
		if (token and token.has_vector and (token.text != word.text)):
			words.append(token)
	closest = []
	for key in sorted(words, key=lambda x: word.similarity(x), reverse=True)[:n]:
		closest.append(key)
	return closest


#igual a la anterior pero devuelve tokens con el mismo texto de word
def most_similar_and_equals_tokens(doc, word, n):
	words = []
	for token in doc:
		if (token and token.has_vector):
			words.append(token)
	closest = []
	for key in sorted(words, key=lambda x: word.similarity(x), reverse=True)[:n]:
		closest.append(key)
	return closest


#devuelve el primer token que encuentre cuyo texto sea igual a str

def get_token(doc, str):
	for token in doc:
		if (token.text == str):
			return token
	return None


#devuelve el primer span que encuentre cuyo texto sea igual a str_list

def get_span(doc, str_list):
	str_length = len(str_list)
	for token in doc:
		temp_token=token
		count = 0
		for str in str_list:
			if(str==temp_token.text):
				count+=1
				if(count == str_length):
					begin=temp_token.i - str_length + 1
					end=temp_token.i
					span=doc[begin:end+1]
					return span
				temp_token=doc[temp_token.i+1]
			else:
				break
	return None


#devuelve las n oraciones que tienen los n tokens más similares a target_token
#(no incluye tokens de texto igual al de target_token)

def sents_with_similar_token(doc, target_token, n):
	list=most_similar_tokens(doc, target_token, n)
	sents = []
	for token in list:
		sents.append(token.sent)
	return sents


#devuelve las n oraciones que tienen los n tokens más similares a target_token
#(incluye tokens de texto igual al de target_token)

def sents_with_token_incluiding_equals(doc, target_token, n):
	list=most_similar_and_equals_tokens(doc, target_token, n)
	sents = []
	for token in list:
		sents.append(token.sent)
	return sents



#código de ejemplo de uso de las funciones anteriores

target_token=get_token(doc, "necesidad")
target_token #para comprobar si lo encontro
sents_with_token_incluiding_equals(doc, target_token)


####################################################
####################################################
####################################################


#puede recibir un token o un span y una lista de tokens o de spans
#retorna los n strings más similares (eliminando repetidos)

def most_similar_objects_to_target(target, objects, n):
	filtered_objects = []
	for object in objects:
		if (object.has_vector):
			filtered_objects.append(object)
	closest = []
	for key in sorted(filtered_objects, key=lambda x: target.similarity(x), reverse=True)[:n]:
		closest.append(key)
	objects_set_texts = []
	objects_set = []
	for object in closest:
		if(object.text not in objects_set_texts):
			objects_set.append(object)
			objects_set_texts.append(object.text)
	return objects_set


#retorna bigramas como strings filtrando repetidos

def get_bigrams_from_first_word(doc, text):
	bigrams=[]
	for token in doc:
		if token.text == text:
			begin=token.i
			end=token.i+2
			span=doc[begin:end]
			bigrams.append(span)
	bigrams_set_texts = []
	bigrams_set = []
	for bigram in bigrams:
		if(bigram.text not in bigrams_set_texts):
			bigrams_set.append(bigram)
			bigrams_set_texts.append(bigram.text)
	return bigrams_set


#retorna bigramas como strings filtrando repetidos

def get_bigrams_from_second_word(doc, text):
	bigrams=[]
	for token in doc:
		if token.text == text:
			begin=token.i-1
			end=token.i+1
			span=doc[begin:end]
			bigrams.append(span)
	bigrams_set_texts = []
	bigrams_set = []
	for bigram in bigrams:
		if(bigram.text not in bigrams_set_texts):
			bigrams_set.append(bigram)
			bigrams_set_texts.append(bigram.text)
	return bigrams_set


#retorna triigramas como strings filtrando repetidos

def get_trigrams_from_second_word(doc, text):
	trigrams=[]
	for token in doc:
		if token.text == text:
			begin=token.i-1
			end=token.i+2
			span=doc[begin:end]
			trigrams.append(span)
	trigrams_set_texts = []
	trigrams_set = []
	for trigram in trigrams:
		if(trigram.text not in trigrams_set_texts):
			trigrams_set.append(trigram)
			trigrams_set_texts.append(trigram.text)
	return trigrams_set


#retorna todas las oraciones que contienen word, incluso las que lo contienen
#en mayúsculas

def sents_with_word(doc, word):
	selected_sents = []
	sents = list(doc.sents)
	for s in sents:
		for token in s:
			if (token.text == word or token.text == word.capitalize):
				selected_sents.append(s)
				break
	return selected_sents


#retorna todas las sents, eliminando stopwords, signos de puntuación,
#espacios y word

def clean_sents(word, sents):
	new_sents = []
	for s in sents:
		new_sent = []
		for token in s:
			if not(len(token.text)==1 or token.is_stop or token.is_punct or token.is_space or token.text.lower() == word.lower()):
				new_sent.append(token) #token.lemma_lower() si quiero guardar los lemmas, es una solucion mas general y la utilizada en la documentacion de gensim
		new_sents.append(new_sent)
	return new_sents


def concat_lists(str_list): #no logra alocar el arreglo, memory error
	list = []
	for str in str_list:
		doc=tag_file(str)
		sents=sents_with_word(doc,"calle")
		clean_sent=clean_sents("calle", sents)
		for s in clean_sent:
			list.append(s)
	return list


#taggea el archivo str, busca en el doc generado todas las oraciones
#que contienen la palabra word, y luego las retorna "limpias"

def selected_tokens_lists(str, word):
	list = []
	doc=tag_file(str)
	sents=sents_with_word(doc, word)
	clean_sent=clean_sents(word, sents)
	for s in clean_sent:
		list.append(s)
	return list

#recibe una lista de listas de tokens
#retorna todos los tokens taggeados como pos

def filter_by_pos(tokens_chains, pos):
	token_list = []
	for chain in tokens_chains:
		for token in chain:
			if(token.pos_ == pos):
				 token_list.append(token)
	return token_list
