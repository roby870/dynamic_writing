from tensorflow import keras
from tensorflow.keras import layers

import numpy as np
import random

from pathlib import Path


def prepare_lstm(corpus):
    data_folder = Path("./LSTM_corpus")
    data_path = data_folder / corpus
    with data_path.open("r", encoding="utf-8") as f:
        text=f.read()
        f.close()
    print("Corpus length:", len(text))

    chars = sorted(list(set(text)))
    print("Total chars:", len(chars))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

    # cut the text in semi-redundant sequences of maxlen characters
    maxlen = 40
    step = 3
    sentences = []
    next_chars = []
    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i : i + maxlen])
        next_chars.append(text[i + maxlen])
    print("Number of sequences:", len(sentences))

    x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            x[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1

    model = keras.Sequential(
    [
        keras.Input(shape=(maxlen, len(chars))),
        layers.LSTM(256),
        layers.Dense(len(chars), activation="softmax"),
    ]
    )
    optimizer = keras.optimizers.RMSprop(learning_rate=0.005)
    model.compile(loss="categorical_crossentropy", optimizer=optimizer)
    
    params = {
            'x': x,
            'y': y,
            'char_indices': char_indices,
            'indices_char': indices_char,
            'maxlen': maxlen,
            'chars': chars, 
            'text': text
        }
    return model, params


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)
    


def train_lstm(model, params, epochs = 1, batch_size = 256): 
    for epoch in range(epochs):
        model.fit(params['x'], params['y'], batch_size=batch_size, epochs=1)
        print()
        print("Generating text after epoch: %d" % epoch)

        start_index = random.randint(0, len(params['text']) - params['maxlen'] - 1)
        for diversity in [0.1, 0.5, 0.7, 1.0]:
            print("...Diversity:", diversity)

            generated = ""
            sentence = params['text'][start_index : start_index + params['maxlen']]
            print('...Generating with seed: "' + sentence + '"')

            for i in range(400):
                x_pred = np.zeros((1, params['maxlen'], len(params['chars'])))
                for t, char in enumerate(sentence):
                    x_pred[0, t, params['char_indices'][char]] = 1.0
                preds = model.predict(x_pred, verbose=0)[0]
                next_index = sample(preds, diversity)
                next_char = params['indices_char'][next_index]
                sentence = sentence[1:] + next_char
                generated += next_char

            print("...Generated: ", generated)
            print()

