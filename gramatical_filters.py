from tokens import *
from chunks import *

class Gramatical_Filter(object):
    def __init__(self, nlp_gensim):
        self._nlp_gensim = nlp_gensim

	@property
	def nlp_gensim(self):
		return self._nlp_gensim

	@text.setter
	def nlp_gensim(self, nlp_gensim):
		self._nlp_gensim = nlp_gensim

	@text.deleter
	def nlp_gensim(self):
		del self._nlp_gensim

    def __create_chunk_from_subtree(token, doc, chunk_length):
        begin = list(token.subtree)[0].i
        end = list(token.subtree)[chunk_length - 1].i
        span = doc[begin:end+1]
        tokens = []
        for t in span:
            tokens.append(
                Tokens(t.text.lower(), t.pos_, t.tag_))
        new_doc = self.nlp_gensim(span.text.lower())
        has_vector = new_doc.has_vector
        vector = new_doc.vector
        vector_norm = new_doc.vector_norm
        chunk = Chunks(span.text.lower(), tokens, doc._.source, has_vector, vector, vector_norm)
        return chunk

    # recibe una cadena de tags(pos_tags, lista de strings),
    # busca en doc un token que esté taggeado como dep_tag y
    # si su subtree es una secuencia de tokens taggeada como
    # pos_tags, la selecciona. Retorna todas las seleccionadas (chunks)
    def process(doc, dep_tag, pos_tags):
        chunks = []
        chunk_length = len(pos_tags)
        for token in doc:
            if token.dep_ == dep_tag:
                subtree = list(token.subtree)
                if (chunk_length <= len(subtree)): # este if se debe a que si no estuviera y se incluyen subtrees de menor length del
                    for i in range(chunk_length):  # chunk_length, en el siguiente if se rompe
                        if (subtree[i].pos_ != pos_tags[i]):
                            break
                        elif(i == (chunk_length - 1)): # chequea si esta en la ultima vuelta, en ese caso guarda la secuencia de tokens como chunk
                            chunk = self.__create_chunk_from_subtree(token, doc, chunk_length)
                            chunks.append(chunk)
        return chunks  # retorna una lista de spans

    def __append_token_as_chunk(token, doc, chunks):
        t = Tokens(token.text.lower(), token.pos_, token.tag_)
        new_token = self.nlp_gensim(token.text.lower())
        chunks.append(Chunks(token.text.lower(), [
                      t], doc._.source, new_token.has_vector, new_token.vector, new_token.vector_norm))

    def __get_tokens_by_pos_and_attrs(doc, gensim_model, pos_tag, attrs):
        number_of_attrs = len(attrs)
        chunks = []
        for token in doc:
            if (token.pos_ == pos_tag):
                counter = 0
                for attr in attrs:
                    if (attr not in token.tag_):
                        break
                    else:
                        counter += 1
                        if (counter == number_of_attrs):
                            self.__append_token_as_chunk(token, doc, chunks)
        return chunks

    def __get_tokens_by_pos(doc, pos_tag):
        chunks = []
        for token in doc:
            if (token.pos_ == pos_tag):
                self.__append_token_as_chunk(token, doc, chunks)
        return chunks

    # selecciona los tokens taggeados como pos_tag y que entre su tag
    # tengan todos los atributos indicados en attrs, por ejemplo "Gender=Fem", "Number=Plur".
    # Los atributos se pasan como strings. Puede no recibir ningun atributo, en ese caso
    # simplemente devuelve todos los tokens taggeados como pos_tag sin importar los atributos de su tag
    def process_tokens_by_pos(doc, pos_tag, *attrs):
        if(len(attrs) > 0):
            chunks = self.__get_tokens_by_pos_and_attrs(doc, pos_tag, attrs)
        else:
            chunks = self.__get_tokens_by_pos(doc, pos_tag)
        return chunks

    def __create_chunk_from_bigram_verbs(token, doc):
        begin = token.i
        end = token.nbor().i
        span = doc[begin:end+1]
        tokens = []
        for t in span:
            tokens.append(
                Tokens(t.text.lower(), t.pos_, t.tag_))
        new_doc = self.nlp_gensim(span.text.lower())
        has_vector = new_doc.has_vector
        vector = new_doc.vector
        vector_norm = new_doc.vector_norm
        chunk = Chunks(span.text.lower(), tokens, doc._.source, has_vector, vector, vector_norm)
        return chunk

    # busca bigramas de pos AUX + tag que respondan a las caracteristicas de
    # número y tiempo parametrizadas
    def process_bigrams_verbs_with_auxiliar(doc, number, tense):
        bigrams = []
        for token in doc:
            if token.pos_ == "AUX":  # cuando se encuentra con un auxiliar, chequea que el verbo conjugado adyacente presente las condiciones parametrizadas
                if ((("Tense=" + tense) not in token.nbor().tag_) or (("Number=" + number) not in token.nbor().tag_)):
                    continue
                else:
                    chunk = self.__create_chunk_from_bigram_verbs(token, doc)
                    bigrams.append(chunk)
        return bigrams  # retorna una lista de chunks


    # busca verbos con las caracteristicas indicadas
    def process_one_word_verbs(doc, gensim_model, person, number, tense, mood):
        verbs=[]
        for token in doc:
            if token.pos_ == "VERB":
                if (("Person=" + person) not in token.tag_) or (("Tense=" + tense) not in token.tag_) or (("Number=" + number) not in token.tag_) or (("Mood=" + mood) not in token.tag_):
                    continue
                else:
                    self._append_token_as_chunk(token, doc, verbs)
        return verbs  # retorna una lista de Chunks

    # colocar stopwords en true si se quieren incluir stopwords
    def get_head(doc, dep_tag, stopwords=False):
        chunks=[]
        if(not stopwords):
            for token in doc:
                if(not token.is_stop):
                    if token.dep_ == dep_tag:
                        self.__append_token_as_chunk(token.head, doc, chunks)
        else:
            for token in doc:
                if token.dep_ == dep_tag:
                    self.__append_token_as_chunk(token.head, doc, chunks)
        return chunks

    # selecciona los tokens taggeados como dep_tag
    def process_token_by_dep(doc, dep_tag):
        chunks=[]
        for token in doc:
            if token.dep_ == dep_tag:
                self.__append_token_as_chunk(token.head, doc, chunks)
        return chunks
