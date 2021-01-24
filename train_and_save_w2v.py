import gensim
import gensim.models
import os

    #If we wanted to do any custom preprocessing, e.g. decode a non-standard encoding,
    #lowercase, remove numbers, extract named entities… All of this can be done inside
    #the MyCorpus iterator and word2vec doesn’t need to know.
    #All that is required is that the input yields one sentence (list of utf8 words) after another.

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):  # assume there's one document per line, tokens separated by whitespace
                yield line.split()



#en el directorio ./training_corpus ya están los textos preprocesados
sentences = MySentences('./training_corpus') # a memory-friendly iterator
model = gensim.models.Word2Vec(sentences)
#model.save('./mymodel') de esta forma se guarda en el modo binario pero lo necesitamos guardar como txt
model.wv.save_word2vec_format("./data/word2vec.txt")
#realizar los pasos necesarios para que el modelo quede legible por spacy, es decir ejecutar en el directorio data:
#gzip ./word2vec.txt
#python3 -m spacy init-model es ./spacy.word2vec.model --vectors-loc word2vec.txt.gz
#luego queda disponible para cargar asi:
#nlp_gensim = spacy.load('./data/spacy.word2vec.model/')
