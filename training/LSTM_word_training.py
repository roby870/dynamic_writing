import spacy
import tensorflow as tf 
# keras module for building LSTM 
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential

import numpy as np

from pathlib import Path

from collections import Counter

import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from preprocessing.preprocessor import tokenize_file

#solo importar en el caso de que se necesiten procesar los datos de forma más amigable para los recursos de procesamiento y memoria
#from LSTM_word_training_for_low_performance_computers import *


def get_sentences_and_tokens(doc, tokenizer):
    tokenized_sents = tokenize_file(doc, tokenizer)
    tokens = []
    for sent in tokenized_sents:
        for token in sent:
            tokens.append(token)
    sents = list(doc.sents)
    return sents, tokens


def preprocess_corpus(corpus):
    data_folder = Path("../LSTM_corpus")
    data_path = data_folder / corpus
    with data_path.open("r", encoding="utf-8") as f:
        text=f.read()
        f.close()
    nlp = spacy.load("es_core_news_md",  disable=["tagger", "parser", "ner"])
    nlp.add_pipe('sentencizer')
    doc = nlp(text)
    tokenizer = nlp.tokenizer
    sents, tokens = get_sentences_and_tokens(doc, tokenizer) 
    return sents, tokens


"""Función para analizar cuál es la lista de palabras más indicadas para pasar como 
parámetro most_common_words del método get_sentences_with_most_frequent_words.
El resultado de esta función es una instancia de la clase Counter, que debe ser analizada 
usando el método most_common(n)"""
def get_freq_dist(tokens):
    freq_dist = Counter(tokens)
    return freq_dist    


def get_sentences_with_most_frequent_words(sents, most_common_words):
    sents_as_strings = []
    for s in sents:
        for word in most_common_words:
            if word in s.text:
                sents_as_strings.append(s.text) 
                break
    return sents_as_strings


"""Esta opción es exponencialmente más costosa que la de pasarle al modelo las
oraciones, ya que convierte cada oración en múltiples n-gramas, por lo tanto retorna
una cantidad de datos exponencialmente mayor, que se deberán alojar en memoria durante
el entrenamiento del modelo. No obstante, los datos que se obtienen son de mejor calidad
para una arquitectura LSTM."""
def get_ngram_sequences_of_tokens(corpus, tokenizer):
    ## tokenization
    tokenizer.fit_on_texts(corpus)
    total_words = len(tokenizer.word_index) + 1
    ## convert data to sequence of tokens 
    input_sequences = []
    for line in corpus:
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i+1]
            input_sequences.append(n_gram_sequence)
    return input_sequences, total_words


def generate_padded_sequences(input_sequences, total_words):
    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))
    
    predictors, label = input_sequences[:,:-1],input_sequences[:,-1]
    label = tf.keras.utils.to_categorical(label, num_classes=total_words)
    return predictors, label, max_sequence_len


def create_model(max_sequence_len, total_words):
    input_len = max_sequence_len - 1
    model = Sequential()
    
    # Add Input Embedding Layer
    model.add(Embedding(total_words, 100, input_length=input_len))
    
    # Add Hidden Layer 1 - LSTM Layer
    model.add(LSTM(128))
    model.add(Dropout(0.1))
    
    # Add Output Layer
    model.add(Dense(total_words, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')
    
    return model


def load_corpus_and_train(sents):
    tokenizer = Tokenizer()
    inp_sequences, total_words = get_ngram_sequences_of_tokens(sents, tokenizer)
    print("Corpus length:", total_words)
    predictors, label, max_sequence_len = generate_padded_sequences(inp_sequences, total_words)
    print("Max sequence length:", max_sequence_len)
    model = create_model(max_sequence_len, total_words)
    model.summary()
    model.fit(predictors, label, epochs=5, verbose=2)
    return tokenizer, model, predictors, label


def generate_text(seed_text, next_words, tokenizer, model, max_sequence_len):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
        predicted = model.predict(token_list)
        predicted_word_index = np.argmax(predicted)
        output_word = ""
        for word,index in tokenizer.word_index.items():
            if index == predicted_word_index:
                output_word = word
                break
        seed_text += " "+output_word
    return seed_text


