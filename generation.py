#script de ejemplo
import spacy
from sequences import *
from similarity_filters import *
from dynamic_generator import *
#Supongamos que queremos establecer una secuencia sencilla que consista en la
#palabra "Vi" + obj (sustantivos que en el corpus cumplan la función sintáctica de objeto directo)
#Primero establecemos un doc con la palabra "vi" procesada por nuestro modelo,
#es decir por el que entrenamos utilizando gensim, y luego comenzamos la secuencia:
nlp_gensim = spacy.load('./data/spacy.word2vec.model/')
doc = nlp_gensim("vi")
seq = Sequences(doc.text, [], doc.has_vector, doc.vector, doc.vector_norm)
#instanciamos los objetos que vamos a necesitar:
similarity_filter = SimilarityFilters()
dynamic_generator = DynamicGenerator(nlp_gensim)
# para obtener los cincuenta objetos más similares de la lista list_obj
#(asumimos que previamente se almacenaron en la variable list_obj sustantivos como chunks
#que en el corpus cumplen la función de objeto directo):
objs = similarity_filter.most_similar_chunks_to_target(seq, list_obj, 50)
# para obtener los cincuenta más similares de la lista y devolverlos concatenados al target:
sequences = dynamic_generator.append_chunks_to_most_similars_sequences(similarity_filter, [seq], list_obj, 50)


#otro ejemplo: se elige una palabra o frase para buscar en una lista las más similares y
#comenzar las secuencias desde las cincuenta seleccionadas
doc = nlp_gensim("abrir la puerta")
objs = similarity_filter.most_similar_chunks_to_target(doc, list_obj, 50)
# se crean las secuencias con los componentes seleccionados y se las concatena
# con un string
sequences = []
for obj in objs:
    doc = nlp_gensim("Quería abrir " + obj.text)
    seq = Sequences(doc.text, [obj], doc.has_vector, doc.vector, doc.vector_norm)
    sequences.append(seq)
# seteamos los atributos gramaticales:
dynamic_generator.set_current_tags(sequences, 0, "NOUN", "Gender", "Number")
# concatenamos las siguientes palabras de acuerdo a la concordancia en número:
for seq in sequences:
    if(seq.number == 'Sing'):
        seq.text = seq.text + ', que era'
    if(seq.number == 'Plur'):
        seq.text = seq.text + ', que eran'
# cuando agregamos texto de esta forma podemos actualizar los puntajes de los vectores de las secuencias
for seq in sequences:
    doc = nlp_gensim(seq.text)
    seq.has_vector = doc.has_vector
    seq.vector = doc.vector
    seq.vector_norm = doc.vector_norm
