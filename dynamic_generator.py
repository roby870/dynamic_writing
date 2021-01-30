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

Doc.set_extension("source", default='')


class DynamicGenerator(object):

    # selecciona el componente numero n (en una sequence el orden de los componentes es conocido)
    # y dentro de ese chunk el token taggeado como pos, de ese saca todas las features indicadas en sequence tags
    # y las establece como las de la secuencia. Pasar los sequence tags en
    # mayusculas, por ejemplo: "Person", "Gender", "Mood"
    def set_current_tags(sequence_list, n, pos, *sequence_tags):
        for sequence in sequence_list:
            for token in sequence.components[n].tokens:
                if(token.pos == pos):
                    for tag in sequence_tags:
                        match = re.search(tag + '=' + r'\w+(\||$)', token.tag)
                        if(bool(match)):
                            match = match.group()
                            match_last_position = match[len(match) - 1]
                            if(match_last_position == '|'):
                                match = match[:len(match) - 1]
                            sequence.set_tag(match)

    # se deben pasar todos los tags actuales de la secuencia y la función chequea
    # que el token del chunk taggeado como pos cumpla con todos los sequence_tags indicados,
    # en ese caso selecciona el chunk
    def __filter_chunks(chunks, pos, *sequence_tags):
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

    def __extend_sequence(model, sequence, components, similar_chunk, reverse=False):
        new_components = components
        new_components.append(similar_chunk)
        if (reverse):
            new_text = similar_chunk.text + ' ' + sequence.text
            new_doc = model(similar_chunk.text.lower() + ' ' +
                            sequence.text.lower())
        else:
            new_text = sequence.text + ' ' + similar_chunk.text
            new_doc = model(sequence.text.lower() + ' ' +
                            similar_chunk.text.lower())
        vector = new_doc.vector
        has_vector = new_doc.has_vector
        vector_norm = new_doc.vector_norm
        new_seq = Sequences(new_text, new_components,
                            has_vector, vector, vector_norm)
        return new_seq

    # selecciona los n chunks mas similares a cada secuencia y los concatena
    # como lo hace? utiliza el token taggeado como pos de cada chunk para chequear que su tag
    # concuerde con las features de la secuencia, en ese caso lo selecciona
    # para luego evaluar si esta dentro de los mas similares semanticamente.
    # El parámetro n es para indicar con cuántos chunks se quiere concatenar cada secuencia
    # (un n grande dará como resultado un crecimiento exponencial en la cantidad de secuencias)
    def concat_sequences_with_most_similars_chunks(
            model, sequences_list, chunks_list, pos, n, reverse=false):
        sequences = []
        for sequence in sequences_list:
            filtered_chunks = self.__filter_chunks(
                chunks_list, pos, *sequence.get_features())
            if(len(filtered_chunks) < n):
                continue
            most_similars = most_similar_chunks_to_target(
                sequence, filtered_chunks, n)
            components = sequence.components.copy()
            for similar_chunk in most_similars:
                new_seq = self.__extend_sequence(model, sequence, components, similar_chunk, reverse)
                new_seq.set_gramatical_tags(sequence.gender, sequence.number, sequence.person, sequence.tense, sequence.mood)
                sequences.append(new_seq)
        return sequences

    # pasar una copia de chunks_list si no se quiere modificarla, ya que este método elimina
    # de la lista los chunks que concatena en cada iteración
    def concat_sequences_with_most_similars_chunks_forbbiding_repeats(
            model, sequences_list, chunks_list, pos, n, reverse=false):
        sequences = []
        for sequence in sequences_list:
            filtered_chunks = self.__filter_chunks(
                chunks_list, pos, *sequence.get_features())
            if(len(filtered_chunks) < n):
                continue
            most_similars = most_similar_chunks_to_target(
                sequence, filtered_chunks, n)
            components = sequence.components.copy()
            for similar_chunk in most_similars:
                new_seq = self.__extend_sequence(
                    model, sequence, components, similar_chunk, reverse)
                new_seq.set_gramatical_tags(sequence.gender, sequence.number, sequence.person, sequence.tense, sequence.mood)
                sequences.append(new_seq)
                chunks_list.remove(similar_chunk)
        return sequences

    # como el anterior método pero sin considerar la concordancia gramatical,
    # tener en cuenta que borra los tags de la secuencia
    def append_chunks_to_most_similars_sequences(
            model, sequences, chunks, n, reverse=false):
        new_seqs = []
        for seq in sequences:
            similars = most_similar_chunks_to_target(seq, chunks, n)
            for s in similars:
                components = seq.components.copy() + [s]
                new_seq = self.__extend_sequence(
                    model, seq, components, s, reverse)
                new_seqs.append(new_seq)
        return new_seqs

    def append_chunks_to_most_similars_sequences_forbidding_repeats(
            model, sequences, chunks, n, reverse=false):
        new_seqs = []
        for seq in sequences:
            similars = most_similar_chunks_to_target(seq, chunks, n)
            for s in similars:
                components = seq.components.copy() + [s]
                new_seq = self.__extend_sequence(
                    model, seq, components, s, reverse)
                new_seqs.append(new_seq)
                chunks.remove(s)
        return new_seqs

    # concatena un string en el caso de que la secuencia esté taggeada
    # con todos los atributos indicados en sequence_tags
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
