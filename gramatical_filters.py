# recibe una cadena de tags(pos_tags, lista de strings),
# busca en doc un token que esté taggeado como dep_tag y
# si su subtree es una secuencia de tokens taggeada como
# pos_tags, la selecciona. Retorna todas las seleccionadas (chunks)
from tokens import *
from chunks import *


def process(doc, nlp_gensim, dep_tag, pos_tags):
    chunks = []
    chunk_length = len(pos_tags)
    for token in doc:
        if token.dep_ == dep_tag:
            subtree = list(token.subtree)
            # este if se debe a que si no estuviera y se incluyen subtrees de menor length del
            if (chunk_length <= len(subtree)):
                for i in range(chunk_length):  # chunk_length aca en este otro if se rompe
                    if (subtree[i].pos_ != pos_tags[i]):
                        break
                    # chequea si esta en la ultima vuelta, en ese caso guarda la secuencia de tokens como span
                    elif(i == (chunk_length - 1)):
                        begin = list(token.subtree)[0].i
                        end = list(token.subtree)[chunk_length - 1].i
                        span = doc[begin:end+1]
                        tokens = []
                        for t in span:
                            tokens.append(
                                Tokens(t.text.lower(), t.pos_, t.tag_))
                        new_doc = nlp_gensim(span.text.lower())
                        has_vector = new_doc.has_vector
                        vector = new_doc.vector
                        vector_norm = new_doc.vector_norm
                        chunks.append(
                            Chunks(span.text.lower(), tokens, doc._.source, has_vector, vector, vector_norm))
    return chunks  # retorna una lista de spans


# selecciona los tokens taggeados como pos_tag y que entre su tag
# tengan todos los atributos indicados en attrs, por ejemplo "Gender=Fem", "Number=Plur"
# los atributos se pasan de esa forma, como strings. Puede no recibir ningun atributo, en ese caso
# simplemente devuelve todos los tokens taggeados como pos_tag sin importar los atributos de su tag

def process_tokens_by_pos(doc, gensim_model, pos_tag, *attrs):
    number_of_attrs = len(attrs)
    chunks = []
    if(number_of_attrs > 0):
        for token in doc:
            if (token.pos_ == pos_tag):
                counter = 0
                for attr in attrs:
                    if (attr not in token.tag_):
                        break
                    else:
                        counter += 1
                        if (counter == number_of_attrs):
                            t = Tokens(token.text.lower(),
                                       token.pos_, token.tag_)
                            new_token = gensim_model(token.text.lower())
                            chunks.append(Chunks(token.text.lower(), [
                                          t], doc._.source, new_token.has_vector, new_token.vector, new_token.vector_norm))
    else:
        for token in doc:
            if (token.pos_ == pos_tag):
                t = Tokens(token.text.lower(), token.pos_, token.tag_)
                new_token = gensim_model(token.text.lower())
                chunks.append(Chunks(token.text.lower(), [
                              t], doc._.source, new_token.has_vector, new_token.vector, new_token.vector_norm))
    return chunks


# busca bigramas de pos AUX + tag que responda a las caracteristicas de
# genero, número y tiempo parametrizadas

def process_bigrams_verbs_with_auxiliar(doc, nlp_gensim, number, tense):
    bigrams = []
    for token in doc:
        if token.pos_ == "AUX":  # cuando se encuentra con un auxiliar, chequea que el verbo conjugado adyacente presente las condiciones parametrizadas
            if ((("Tense=" + tense) not in token.nbor().tag_) or (("Number=" + number) not in token.nbor().tag_)):
                continue
            else:
                begin=token.i
                end=token.nbor().i
                span=doc[begin:end+1]
                tokens=[]
                for t in span:
                    tokens.append(
                        Tokens(t.text.lower(), t.pos_, t.tag_))
                new_doc=nlp_gensim(span.text.lower())
                has_vector=new_doc.has_vector
                vector=new_doc.vector
                vector_norm=new_doc.vector_norm
                bigrams.append(
                    Chunks(span.text.lower(), tokens, doc._.source, has_vector, vector, vector_norm))
    return bigrams  # retorna una lista de chunks


# busca verbos con las caracteristicas indicadas

def process_one_word_verbs(doc, gensim_model, person, number, tense, mood):
    verbs=[]
    for token in doc:
        if token.pos_ == "VERB":
            if (("Person=" + person) not in token.tag_) or (("Tense=" + tense) not in token.tag_) or (("Number=" + number) not in token.tag_) or (("Mood=" + mood) not in token.tag_):
                continue
            else:
                t=Tokens(token.text, token.pos_, token.tag_)
                new_token=gensim_model(token.text.lower())
                verbs.append(Chunks(token.text.lower(), [
                             t], doc._.source, new_token.has_vector, new_token.vector, new_token.vector_norm))
    return verbs  # retorna una lista de Chunks


# colocar stopwords en true si se quieren incluir stopwords
def get_head(doc, nlp_gensim, dep_tag, stopwords=False):
    chunks=[]
    if(not stopwords):
        for token in doc:
            if(not token.is_stop):
                if token.dep_ == dep_tag:
                    tokens=[]
                    tokens.append(
                        Tokens(token.head.text, token.head.pos_, token.head.tag_))
                    new_doc=nlp_gensim(token.head.text.lower())
                    has_vector=new_doc.has_vector
                    vector=new_doc.vector
                    vector_norm=new_doc.vector_norm
                    chunks.append(Chunks(token.head.text.lower(), tokens,
                                         doc._.source, has_vector, vector, vector_norm))
    else:
        for token in doc:
            if token.dep_ == dep_tag:
                tokens=[]
                tokens.append(
                    Tokens(token.head.text.lower(), token.head.pos_, token.head.tag_))
                new_doc=nlp_gensim(token.head.text.lower())
                has_vector=new_doc.has_vector
                vector=new_doc.vector
                vector_norm=new_doc.vector_norm
                chunks.append(Chunks(token.head.text.lower(), tokens,
                                     doc._.source, has_vector, vector, vector_norm))
    return chunks


# selecciona los tokens taggeados como dep_tag

def process_token_by_dep(doc, nlp_gensim, dep_tag):
    chunks=[]
    for token in doc:
        if token.dep_ == dep_tag:
            tokens=[]
            tokens.append(Tokens(token.text.lower(), token.pos_, token.tag_))
            new_doc=nlp_gensim(token.text.lower())
            has_vector=new_doc.has_vector
            vector=new_doc.vector
            vector_norm=new_doc.vector_norm
            chunks.append(Chunks(token.text.lower(), tokens,
                                 doc._.source, has_vector, vector, vector_norm))
    return chunks  # retorna una lista de spans
