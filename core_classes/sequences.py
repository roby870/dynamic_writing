import re
import numpy


class Sequences(object):
    def __init__(self, text, components, has_vector, vector, vector_norm):
        self._text = text
        self._components = components
        self._gender = None
        self._number = None
        self._person = None
        self._tense = None
        self._mood = None
        self._has_vector = has_vector
        self._vector = vector
        self._vector_norm = vector_norm

    @property  # en la variable text va el doc procesado por el modelo entrenado con gensim
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @text.deleter
    def text(self):
        del self._text

    @property
    def components(self):
        return self._components

    @components.setter
    def components(self, components):
        self._components = components

    @components.deleter
    def components(self):
        del self._components

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender

    @gender.deleter
    def gender(self):
        del self._gender

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = number

    @number.deleter
    def number(self):
        del self._number

    @property
    def person(self):
        return self._person

    @person.setter
    def person(self, person):
        self._person = person

    @person.deleter
    def person(self):
        del self._person

    @property
    def tense(self):
        return self._tense

    @tense.setter
    def tense(self, tense):
        self._tense = tense

    @tense.deleter
    def tense(self):
        del self._tense

    @property
    def mood(self):
        return self._mood

    @mood.setter
    def mood(self, mood):
        self._mood = mood

    @mood.deleter
    def mood(self):
        del self._mood

    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, vector):
        self._vector = vector

    @vector.deleter
    def vector(self):
        del self._vector

    @property
    def vector_norm(self):
        return self._vector_norm

    @vector_norm.setter
    def vector_norm(self, vector_norm):
        self._vector_norm = vector_norm

    @vector_norm.deleter
    def vector_norm(self):
        del self._vector_norm

    def set_gramatical_tags(self, gender, number, person, tense, mood):
        self.gender = gender
        self.number = number
        self.person = person
        self.tense = tense
        self.mood = mood

#puede recibir un tag con todos los atributos de un token o un recorte de ese tag
#con solo uno o algunos de sus atributos, funciona para ambos casos
    def set_tag(self, tag):
        if("Gender" in tag):
            match = re.search('(?<=Gender=)\w+', tag)
            self.gender = match.group()
        if("Number" in tag):
            match = re.search('(?<=Number=)\w+', tag)
            self.number = match.group()
        if("Person" in tag):
            match = re.search('(?<=Person=)\w+', tag)
            self.person = match.group()
        if("Tense" in tag):
            match = re.search('(?<=Tense=)\w+', tag)
            self.tense = match.group()
        if("Mood" in tag):
            match = re.search('(?<=Mood=)\w+', tag)
            self.mood = match.group()

    def unset_tag(self, tag):
        if("Gender" == tag):
            self.gender = None
        elif("Number" == tag):
            self.number = None
        elif("Person" == tag):
            self.person = None
        elif("Tense" == tag):
            self.tense = None
        elif("Mood" == tag):
            self.mood = None

    def get_features(self):
        features = []
        if(self.gender != None):
            features.append(self.gender)
        if(self.number != None):
            features.append(self.number)
        if(self.person != None):
            features.append(self.person)
        if(self.tense != None):
            features.append(self.tense)
        if(self.mood != None):
            features.append(self.mood)
        return features

    def similarity(self, sequence_or_chunk):
        return numpy.dot(self.vector, sequence_or_chunk.vector) / (self.vector_norm * sequence_or_chunk.vector_norm)

    def get_sources(self):
        sources = {}
        for component in self.components:
            sources[component.text] = component.source
        return sources
