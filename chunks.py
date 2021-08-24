import numpy

class Chunks(object):
	def __init__(self, text, tokens, source, has_vector, vector, vector_norm):
		self._text = text
		self._tokens = tokens
		self._source = source
		self._has_vector = has_vector
		self._vector = vector
		self._vector_norm = vector_norm

	@property #almacena el texto procesado por el modelo de spacy
	def text(self):
		return self._text

	@text.setter
	def text(self, text):
		self._text = text

	@text.deleter
	def text(self):
		del self._text

	@property #almacena el texto procesado por el modelo de spacy
	def tokens(self):
		return self._tokens

	@tokens.setter
	def tokens(self, tokens):
		self._tokens = tokens

	@tokens.deleter
	def tokens(self):
		del self._tokens

	@property
	def source(self):
		return self._source

	@source.setter
	def source(self, source):
		self._source = source

	@source.deleter
	def source(self):
		del self._source

	@property
	def has_vector(self):
		return self._has_vector

	@has_vector.setter
	def has_vector(self, has_vector):
		self._has_vector = has_vector

	@has_vector.deleter
	def has_vector(self):
		del self._has_vector

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

	def similarity(self, sequence_or_chunk):
		return numpy.dot(self.vector, sequence_or_chunk.vector) / (self.vector_norm * sequence_or_chunk.vector_norm)

	def reduce(self, pos, model):
		for token in self.tokens:
			if(token.pos == pos):
				self.tokens = token
				doc = model(token.text)
				self.vector = doc.vector
				self.vector_norm = doc.vector_norm
				self.has_vector = doc.has_vector
				self.text = doc.text
				break
