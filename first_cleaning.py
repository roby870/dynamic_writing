import re
from pathlib import Path

def clean_file(str):
	data_folder = Path("./prueba")
	data_path = data_folder / str
	with data_path.open("r") as f:
		text=f.read()
		f.close()
	text=re.sub(r'\{.+\}', '', text)
	text=re.sub(r'\[.+\]', '', text)
	text=re.sub(r'\*', '', text)
	return text

def clean_file(str):
	data_folder = Path("./prueba")
	data_path = data_folder / str
	with data_path.open("r") as f:
		text=f.read()
		f.close()
	text=re.sub(r'\{.+\}', '', text)
	text=re.sub(r'\[\d+\]', '', text)
	text=re.sub(r'\[', '', text)
	text=re.sub(r'\]', '', text)
	text=re.sub(r'\*', '', text)
	return text

	#caso especial de regex usado para el cuento del grial:
	#text=re.sub(r'\(VS.*\)', '', text)
	#si se quieren eliminar todos los digitos:
	#text=re.sub(r'\d+', '', text)
	#si se quieren eliminar los títulos de los capítulos con números romanos:
	#re.sub(r"CAPÍTULO\s[A-Z]{1,7}", '', text)
	#Lo mismo pero en minúscula e indicando el \n:
	#re.sub(r"Capítulo\s[A-Z]{1,7}\n", '', texto)
	#si se quieren eliminar líneas escritas en mayúsculas (puede servir para titulos de capítulos):
	#text=re.sub(r"(([A-Z]|[ÁÉÍÓÚÑÜ])(\W|\s)*)+\n", '', text)
	#Si se quieren agregar un punto para delimitar como oraciones todas las líneas que no tienen punto final(muy útil para epigrafes):
	#texto = re.sub(r"(?<=\w)\n", '.', texto)
	#caso especial usado para las fábulas de esopo:
	#text=re.sub(r'\(B\.\s*\d+\)', '', text)


def save_lines(str, text):
	data_folder = Path("./prueba")
	data_path = data_folder / str
	with data_path.open('w') as f:
		f.write(text)
		f.close()
