import tensorflow as tf 
# keras module for building LSTM 
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

import numpy as np

import pickle

import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)


"""Esta función pasa al modelo oraciones completas, no n-gramas"""
def get_sents_sequences_of_tokens(corpus, tokenizer):
    ## tokenization
    tokenizer.fit_on_texts(corpus)
    total_words = len(tokenizer.word_index) + 1
    ## convert data to sequence of tokens 
    input_sequences = []
    for line in corpus:
        token_list = tokenizer.texts_to_sequences([line])[0]
        input_sequences.append(token_list)
    return input_sequences, total_words


"""divide los datos en n splits, algo útil en el caso de que 
se disponga de un equipo sin GPU y/o con poca memoria"""
def split_sequences(n, sents, corpus_name):
    tokenizer = Tokenizer()  
    tokenizer.fit_on_texts(sents)
    total_words = len(tokenizer.word_index) + 1 
    print("Total words:", total_words) 
    input_sequences = []
    splits = np.array_split(sents, n)
    max_sequence_len = 0
    for index, split in enumerate(splits):
        split = list(split)
        for line in split:
            token_list = tokenizer.texts_to_sequences([line])[0]
            for i in range(1, len(token_list)):
                n_gram_sequence = token_list[:i+1]
                input_sequences.append(n_gram_sequence)
        name_results = './pickles/' + corpus_name + "_ngrams_" + str(index) + '.pkl'
        split_max_sequence_len = max([len(x) for x in input_sequences])
        if (split_max_sequence_len > max_sequence_len):
            max_sequence_len = split_max_sequence_len
        with open(name_results, 'wb') as f:
            pickle.dump(input_sequences, f)
            f.close()
        print(name_results, "saved")
        input_sequences = []
    print("Max sequence length: ", max_sequence_len)
    model_dict = {'tokenizer': tokenizer, 'total_words': total_words, 'max_sequence_len': max_sequence_len}
    with open('./pickles/' + corpus_name + "_dict" + '.pkl', 'wb') as f:
        pickle.dump(model_dict, f)
        f.close()


"""para utilizar si se generaron los datos mediante la función split_sequences"""
def generate_split_padded_sequences(n, corpus_name, total_words, max_sequence_len):    
    for index in range(n):
        name_pickle = corpus_name + "_ngrams_" + str(index) 
        with open('./pickles/' + name_pickle + '.pkl', 'rb') as f:
            pickle_object = pickle.load(f)
            f.close()
        input_sequences = np.array(pad_sequences(pickle_object, maxlen=max_sequence_len, padding='pre'))
        predictors, label = input_sequences[:,:-1],input_sequences[:,-1]
        label = tf.keras.utils.to_categorical(label, num_classes=total_words)
        train_data = predictors, label
        name_results = './pickles/' + corpus_name + "_train_data_" + str(index) + '.pkl'
        with open(name_results, 'wb') as f:
            pickle.dump(train_data, f)
            f.close()
        print(name_results, "saved")


"""si se dividieron los datos de entrenamiento en splits, entrenar con esta función"""
def train_split_data(model, splits, corpus_name, epochs):
    for n in range(epochs):
        for index in range(splits):
            name_pickle = corpus_name + "_train_data_" + str(index) 
            with open('./pickles/' + name_pickle + '.pkl', 'rb') as f:
                predictors, label = pickle.load(f)
                f.close()
            model.fit(predictors, label, verbose=2)
            predictors = []
            label = []