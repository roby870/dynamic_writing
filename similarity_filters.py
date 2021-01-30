class SimilarityFilters(object):

	#devuelve n tokens con el mismo texto de word o los más similares
	def most_similar_and_equals_tokens(doc, word, n):
		words = []
		for token in doc:
			if (token and token.has_vector):
				words.append(token)
		closest = []
		for key in sorted(words, key=lambda x: word.similarity(x), reverse=True)[:n]:
			closest.append(key)
		return closest

	#devuelve las n oraciones que tienen los n tokens más similares a target_token
	#(incluye tokens de texto igual al de target_token)
	def sents_with_token_incluiding_equals(doc, target_token, n):
		list=most_similar_and_equals_tokens(doc, target_token, n)
		sents = []
		for token in list:
			sents.append(token.sent)
		return sents

	#puede recibir un token o un span y una lista de tokens o de spans
	#retorna los n objetos más similares (eliminando repetidos)
	def most_similar_objects_to_target(target, verbal_objects, n):
		filtered_objects = []
		for object in verbal_objects:
			if (object.has_vector and object.vector_norm != 0):
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

	#recibe un token o un span y una lista de chunks
	#retorna los n objetos más similares (eliminando repetidos)
	#usa el vector del chunk procesado con el modelo de gensim
	def most_similar_chunks_to_target(target, chunks, n):
		filtered_chunks = []
		for chunk in chunks:
			if (chunk.has_vector and chunk.vector_norm != 0 and target.text.lower() != chunk.text):
				filtered_chunks.append(chunk)
		closest = []
		for key in sorted(filtered_chunks, key=lambda x: target.similarity(x), reverse=True)[:n]:
			closest.append(key)
		objects_set_texts = []
		objects_set = []
		for object in closest:
			if(object.text not in objects_set_texts):
				objects_set.append(object)
				objects_set_texts.append(object.text)
		return objects_set
