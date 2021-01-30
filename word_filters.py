class WordFilters(object):

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

	#retorna todas las sents eliminando stopwords, signos de puntuación,
	#espacios y word
	def __clean_sents(sents, word):
		new_sents = []
		for s in sents:
			new_sent = []
			for token in s:
				if not(len(token.text)==1 or token.is_stop or token.is_punct or token.is_space or token.text.lower() == word.lower()):
					new_sent.append(token) #token.lemma_lower() si quiero guardar los lemmas, es una solucion mas general y la utilizada en la documentacion de gensim
			new_sents.append(new_sent)
		return new_sents

	#busca en doc todas las oraciones que contienen la palabra word,
	#y luego las retorna "limpias"
	def contexts_words_lists(doc, word):
		list = []
		sents=sents_with_word(doc, word)
		clean_sent=self.__clean_sents(sents, word)
		for s in clean_sent:
			list.append(s)
		return list

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

	#retorna n-gramas como strings filtrando repetidos
	#n-gramas de l words a la izquierda de word y r words a la derecha de word
	def get_ngrams_from_word(doc, text, l, r):
		ngrams=[]
		for token in doc:
			if token.text == text:
				begin=token.i - l
				end=token.i + r
				span=doc[begin:end]
				ngrams.append(span)
		ngrams_set_texts = []
		ngrams_set = []
		for ngram in ngrams:
			if(ngram.text not in ngrams_set_texts):
				ngrams_set.append(ngram)
				ngrams_set_texts.append(ngram.text)
		return ngrams_set

	#recibe el string str, por ejemplo la preposicion "en", y retorna todos los chunks
	#de la lista chunks que comienzan con str, por ejemplo todos los que comienzan con "en"
	def filter_chunks_by_first_word(chunks, str): #str pasarlo en minuscula
		results = []
		for chunk in chunks:
			if(chunk.tokens[0].text == str):
				results.append(chunk)
		return results
