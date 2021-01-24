def remove_last_spaces(chunks_list):
	for chunk in chunks_list:
		str = chunk.text.lower() # .lower() para filtrar chunks iguales que solo difieren en una o mas mayusculas
		if str[len(str)-1] == ' ':
			str = str[:len(str)-1]
		chunk.text = str
	return chunks_list


def set_chunks_list(chunks_list):
	str_list = []
	chunks = []
	for chunk in chunks_list:
		str = chunk.text
		if(str not in str_list):
			str_list.append(str)
			chunks.append(chunk)
	return chunks
