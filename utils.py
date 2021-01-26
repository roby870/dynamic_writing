from pathlib import Path
import os

def remove_last_spaces(chunks_list):
	for chunk in chunks_list:
		str = chunk.text.lower() # .lower() para filtrar chunks iguales que solo difieren en una o más mayúsculas
		if str[len(str)-1] == ' ':
			str = str[:len(str)-1]
		chunk.text = str
	return chunks_list

    # ejecutar esta funcion luego de obtener los resultados de todos los directorios concatenados
    # para volver a eliminar elementos repetidos en el caso de que los hubiera entre los distintos
    #directorios
def set_chunks_list(chunks_list):
	str_list = []
	chunks = []
	for chunk in chunks_list:
		str = chunk.text
		if(str not in str_list):
			str_list.append(str)
			chunks.append(chunk)
	return chunks

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
