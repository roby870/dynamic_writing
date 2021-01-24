import spacy
from pathlib import Path
import os
import re
from spacy.tokens import DocBin
from spacy.tokens import Doc

from tokens import *
from chunks import *
from sequences import *
from basic_parser import *
from gramatical_filters import *
from similarity_filters import *
from word_filters import *
from utils import *
# from spacy import displacy
# displacy.serve(doc, style="dep")
# nlp = spacy.load("es_core_news_lg")
Doc.set_extension("source", default='')


# retorna una lista con todo lo minado (a partir de la funcion lambda) en los textos presentes en el directorio raw_texts

def process_files(model, gensim_model, num_docs_folder, process_function, *args):
    data_folder = Path("./raw_texts/" + num_docs_folder)
    data_path = data_folder / ("doc_bins" + num_docs_folder)
    with data_path.open("rb") as f:
        bytes_data = f.read()
        f.close()
    doc_bin = DocBin(store_user_data=True).from_bytes(bytes_data)
    docs = list(doc_bin.get_docs(model.vocab))
    results = []
    for doc in docs:
        result = process_function(doc, gensim_model, *args)
        results = results + result
    results = remove_last_spaces(results)
    # ejecutar esta funcion luego de obtener los resultados de todos los directorios concatenados
    results = set_chunks_list(results)
    return results


# selecciona el componente numero n (en una sequence el orden de los componentes es conocido)
# y dentro de ese chunk el token taggeado como pos, de ese saca todas las features indicadas en sequence tags
# y las establece como las de la secuencia. Pasar los sequence tags en mayusculas, por ejemplo: "Person", "Gender", "Mood"

def set_current_tags(sequence_list, n, pos, *sequence_tags):
    for sequence in sequence_list:
        for token in sequence.components[n].tokens:
            if(token.pos == pos):
                for tag in sequence_tags:
                    match = re.search(tag+'='+'\w+(\||$)', token.tag)
                    if(bool(match)):
                        match = match.group()
                        match_last_position = match[len(match) - 1]
                        if(match_last_position == '|'):
                            match = match[:len(match) - 1]
                        sequence.set_tag(match)


# se deben pasar todos los tags actuales de la secuencia y la función chequea
# que el token del chunk taggeado como pos cumpla con todos los sequence_tags indicados,
# en ese caso selecciona el chunk

def filter_chunks(chunks, pos, *sequence_tags):
    number_of_attrs = len(sequence_tags)
    results = []
    for chunk in chunks:
        for token in chunk.tokens:
            if(token.pos == pos):
                counter = 0
                for attr in sequence_tags:
                    if (attr not in token.tag):
                        break
                    else:
                        counter += 1
                        if (counter == number_of_attrs):
                            results.append(chunk)
    return results


# selecciona los n chunks mas similares a cada secuencia y los concatena
# como lo hace? utiliza el token taggeado como pos de cada chunk para chequear que su tag
# concuerde con las features de la secuencia, en ese caso lo selecciona
# para luego evaluar si esta dentro de los mas similares semanticamente

def concat_sequences_with_most_similars_chunks(model, sequences_list, chunks_list, pos, n):
    sequences = []
    for sequence in sequences_list:
        filtered_chunks = filter_chunks(
            chunks_list, pos, *sequence.get_features())
        if(len(filtered_chunks) < n):
            continue
        most_similars = most_similar_chunks_to_target(
            sequence, filtered_chunks, n)
        components = sequence.components.copy()
        for similar_chunk in most_similars:
            new_components = components
            new_components.append(similar_chunk)
            new_text = sequence.text + ' ' + similar_chunk.text
            new_doc = model(sequence.text.lower() + ' ' +
                            similar_chunk.text.lower())
            vector = new_doc.vector
            has_vector = new_doc.has_vector
            vector_norm = new_doc.vector_norm
            new_seq = Sequences(new_text, new_components,
                                has_vector, vector, vector_norm)
            new_seq.gender = sequence. gender
            new_seq.number = sequence.number
            new_seq.person = sequence.person
            new_seq.tense = sequence.tense
            new_seq.mood = sequence.mood
            sequences.append(new_seq)
    return sequences


def concat_sequences_with_most_similars_chunks_forbbiding_repeats(model, sequences_list, chunks_list, pos, n):
    sequences = []
    for sequence in sequences_list:
        filtered_chunks = filter_chunks(
            chunks_list, pos, *sequence.get_features())
        if(len(filtered_chunks) < n):
            continue
        most_similars = most_similar_chunks_to_target(
            sequence, filtered_chunks, n)
        components = sequence.components.copy()
        for similar_chunk in most_similars:
            new_components = components
            new_components.append(similar_chunk)
            new_text = sequence.text + ' ' + similar_chunk.text
            new_doc = model(sequence.text.lower() + ' ' +
                            similar_chunk.text.lower())
            vector = new_doc.vector
            has_vector = new_doc.has_vector
            vector_norm = new_doc.vector_norm
            new_seq = Sequences(new_text, new_components,
                                has_vector, vector, vector_norm)
            new_seq.gender = sequence. gender
            new_seq.number = sequence.number
            new_seq.person = sequence.person
            new_seq.tense = sequence.tense
            new_seq.mood = sequence.mood
            sequences.append(new_seq)
            chunks_list.remove(similar_chunk)
    return sequences

# como la anterior pero sin considerar la concordancia gramatical,
# tener en cuenta que borra los tags de la secuencia


def append_chunks_to_most_similars_sequences(nlp_gensim, sequences, chunks, n):
    new_seqs = []
    for seq in sequences:
        similars = most_similar_chunks_to_target(seq, chunks, n)
        for s in similars:
            text = seq.text + ' ' + s.text
            doc = nlp_gensim(seq.text.lower() + ' ' + s.text)
            components = seq.components.copy() + [s]
            new_seqs.append(Sequences(text, components,
                                      doc.has_vector, doc.vector, doc.vector_norm))
    return new_seqs


def append_chunks_to_most_similars_sequences_forbidding_repeats(nlp_gensim, sequences, chunks, n):
    new_seqs = []
    for seq in sequences:
        similars = most_similar_chunks_to_target(seq, chunks, n)
        for s in similars:
            text = seq.text + ' ' + s.text
            doc = nlp_gensim(seq.text.lower() + ' ' + s.text)
            components = seq.components.copy() + [s]
            new_seqs.append(Sequences(text, components,
                                      doc.has_vector, doc.vector, doc.vector_norm))
            chunks.remove(s)
    return new_seqs


def append_sequences_to_most_similars_chunks_forbidding_repeats(nlp_gensim, sequences, chunks, n):
    new_seqs = []
    for seq in sequences:
        similars = most_similar_chunks_to_target(seq, chunks, n)
        for s in similars:
            text = s.text + ' ' + seq.text
            doc = nlp_gensim(s.text + ' ' + seq.text.lower())
            components = seq.components.copy() + [s]
            new_seqs.append(Sequences(text, components,
                                      doc.has_vector, doc.vector, doc.vector_norm))
            chunks.remove(s)
    return new_seqs


# puede recibir una lista de sequences, chunks o tokens
# los imprime en un archivo, uno por linea con su numero
# de objeto en la lista

def print_on_file(verbal_list, file_name):
    data_folder = Path("./")
    data_path = data_folder / file_name
    counter = 0
    with data_path.open("w") as f:
        for verbal_object in verbal_list:
            output = f.write("%s" % verbal_object.text)
            output = f.write("  ")
            output = f.write("%s " % str(counter))
            counter += 1
            output = f.write("\n")


def concat_string(sequences, string, *sequence_tags):
    number_of_attrs = len(sequence_tags)
    for seq in sequences:
        tags = seq.get_features()
        counter = 0
        for attr in sequence_tags:
            if attr not in tags:
                break
            else:
                counter += 1
                if(counter == number_of_attrs):
                    seq.text = seq.text + ' ' + string


def paste_string(sequences, string):
    for seq in sequences:
        seq.text = seq.text + string
