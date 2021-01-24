vi = nlp_gensim("vi")
# para sacar los n mas similares de la lista:
lo_que_vi = most_similar_chunks_to_target(vi, list_obj, 50)
# para sacar los n mas similares de la lista y devolverlos concatenados al tarjet:
concat_with_next_most_similars_chunks(vi, list_obj, 50)

##############################
##############################
##############################
##############################
##############################
##############################
# se elige una palabra o frase para buscar en una lista las mas similares y arrancar las
# secuencias ddesde las n seleccionadas
abro = nlp_gensim("abrir la puerta")
obj_abro = most_similar_chunks_to_target(abro, list_obj, 50)
# se crean las secuencias con los componentes seleccionados y se las concatena
# con un string hecho a mano
sequences = []
for obj in obj_abro:
    seq = Sequences(obj.text, [obj], obj.has_vector,
                    obj.vector, obj.vector_norm)
    sequences.append(seq)

    doc = nlp_gensim("Un pez dice que " + obj.text)
    seq.has_vector = doc.has_vector
    seq.vector = doc.vector
    seq.vector_norm = doc.vector_norm
    seq.text = doc.text
    sequences.append(seq)

# primer componente que se concatena a la secuencia, todavia no se considera la concordancia gramatical:
# funcion paste_sequences_with_most_similars_chunks

# seteamos los atributos gramaticales:
set_current_tags(sequences, 0, "NOUN", "Gender", "Number")

# concatenamos a mano la siguiente palabra de acuerdo a la concordancia en numero:
for seq in sequences:
    if(seq.number == 'Sing'):
        seq.text = seq.text + ' Era'
    if(seq.number == 'Plur'):
        seq.text = seq.text + ' Eran'


# cuando agregamos texto a mano podemos actualizar los puntajes de los vectores de las secuentias

for seq in selected_seqs:
    doc = nlp_gensim(seq.text)
    seq.has_vector = doc.has_vector
    seq.vector = doc.vector
    seq.vector_norm = doc.vector_norm


for chunk in nmod_ADP_DET_NOUN:
    token = chunk.tokens[2]
    chunk.tokens = [token]
    doc = nlp_gensim(token.text)
    chunk.vector = doc.vector
    chunk.vector_norm = doc.vector_norm
    chunk.has_vector = doc.has_vector
    chunk.text = doc.text


seq = Sequences(doc.text, [], doc.has_vector, doc.vector, doc.vector_norm)

>>> doc = nlp_gensim('abro la puerta')
>>> seq = Sequences(doc.text, [], doc.has_vector, doc.vector, doc.vector_norm)
