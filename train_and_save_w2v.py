import gensim
import gensim.models
import os

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):  #debe haber un "documento" por línea, con los tokens separados por espacios en blanco
                yield line.split()

#en el directorio ./training_corpus ya están los textos preprocesados
sentences = MySentences('./training_corpus') # a memory-friendly iterator
model = gensim.models.Word2Vec(sentences)
#ejecutando model.save('./mymodel') se guarda en el modo binario pero lo necesitamos guardar como txt
model.wv.save_word2vec_format("./data/word2vec.txt")
#realizar los pasos necesarios para que el modelo quede legible por spacy, es decir ejecutar en el directorio data:
#gzip ./word2vec.txt
#python3 -m spacy init vectors es word2vec.txt.gz ./spacy.word2vec.model
#luego queda disponible para cargar de esta manera:
#nlp_gensim = spacy.load('./data/spacy.word2vec.model/')
