#concatena cada elemento de la esctructura sintactica con n siguientes.
#el primer parametro es un elemento que hay que elegirlo al azar de una lista de sintagmas del mismo tipo gramatical
#el segundo parametro es una lista de listas de sintagmas del mismo tipo gramatical
#first_sequence debe tener un vector diferente de 0

def generate_sequence(model, first_sequence, following_chunks_lists, n):
	sequences = []
	sequences.append(first_sequence)
	for chunk_list in following_chunks_lists:
		updated_sequences = []
		for element in sequences:
			most_similars = most_similar_text_embedding_chunks_to_target(element.text, chunk_list, n)
			for chunk in most_similars:
				concat_element_str = element.text.text + ' ' + chunk.text.text
				temporal_doc = model(concat_element_str)
				element.components.append(chunk)
				updated_sequences.append(Sequences(temporal_doc, element.components))
		sequences = updated_sequences
	return sequences


def concat_with_next_most_similars_chunks(doc, chunks, n):
	sequences = []
	most_similars = most_similar_text_embedding_chunks_to_target(doc, chunks, n)
	for chunk in most_similars:
		sequence = doc.text + ' ' + chunk.text_embedding.text
		sequences.append(sequence)
	return sequences


def concat_chunks_with_most_similars_chunks(model, first_list, n):
	sequences = []
	for chunk in first_list:
		most_similars = most_similar_text_embedding_chunks_to_target(chunk.text_embedding, second_list, n)
		for similar_chunk in most_similars:
			components = []
			components.append(chunk)
			components.append(similar_chunk)
			new_doc = model(chunk.text_embedding.text + ' ' + similar_chunk.text_embedding.text)
			sequences.append(Sequences(new_doc, components))
	return sequences


#setea el atributo text_embedding
#usar el modelo que tiene el word2vec entrenado por mi
#para que luego cuando evalúe la similitud lo haga
#con el modelo que entrené yo. Se pasa en minusculas porque el modelo esta entrenado en minusculas

def set_texts_embeddings(gensim_model, chunks_list):
	for chunk in chunks_list:
		chunk.text_embedding = gensim_model(chunk.str_text)
	return chunks_list


#recibe un token o un span y una lista de chunks
#retorna los n objetos más similares (eliminando repetidos)
#usa el doc del chunk procesado con el modelo de spacy

def most_similar_text_chunks_to_target(target, chunks, n):
	filtered_chunks = []
	for chunk in chunks:
		if (chunk.text.has_vector and chunk.text.vector_norm != 0 and target.text != chunk.text.text):
			filtered_chunks.append(chunk)
	closest = []
	for key in sorted(filtered_chunks, key=lambda x: target.similarity(x.text), reverse=True)[:n]:
		closest.append(key)
	objects_set_texts = []
	objects_set = []
	for object in closest:
		if(object.text.text not in objects_set_texts):
			objects_set.append(object)
			objects_set_texts.append(object.text.text)
	return objects_set
