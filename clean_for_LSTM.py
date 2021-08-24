import re 
from pathlib import Path	

def clean_for_lstm(file_name):
    data_folder = Path("./LSTM_corpus")
    data_path = data_folder / file_name
    with data_path.open("r") as f:
        text=f.read()
        f.close()
	#text=text.replace('\u200b', '')
    #text = text.replace("\n", " ") Asi figura en el ejemplo de la documentacion de Keras, pero considero que los punto y aparte deben ser aprendidos por el modelo
    text=re.sub(r'(?<=\s)\s+', '', text) #Eliminamos dos o mas blancos seguidos, sean dos espacios, dos /n, etc
    text=re.sub(r'\{.+\}', '', text) #texto entre llaves
    text=re.sub(r'\[.+\]', '', text) #texto entre corchetes
    text=re.sub(r'\*', '', text)     #asteriscos
    text=re.sub(r'<', '', text)
    text=re.sub(r'«', '', text)
    text=re.sub(r'»', '', text)
    #text=re.sub(r'\d+', '', text) #dígitos
    text=re.sub(r'\n\d+', '', text) #dígitos luego de un punto y aparte
	#text=re.sub(r'(?<=\w)\—', '', text) #guiones de diálogo
	#text=re.sub(r':', '.', text) #dos puntos
	#text=re.sub(r'\s\—', '. ', text) #guiones de diálogo
	#text=re.sub(r'\[\d+\]', '', text) #dígitos entre corchetes (innesesaria si no se comenta la de los corchetes)
    text=re.sub(r'\(\d+\)', '', text) #dígitos entre parentesis 
	#si se quieren eliminar los títulos de los capítulos con números romanos:
	#re.sub(r"CAPÍTULO\s[A-Z]{1,7}", '', text)
	#Lo mismo pero en minúscula e indicando el \n:
	#re.sub(r"Capítulo\s[A-Z]{1,7}\n", '', texto)
	#si se quieren eliminar líneas escritas en mayúsculas (puede servir para titulos de capítulos):
	#text=re.sub(r"(([A-Z]|[ÁÉÍÓÚÑÜ])(\W|\s)*)+\n", '', text)
	#Si se quiere agregar un punto para delimitar como oraciones todas las líneas que no tienen punto final(muy útil para epigrafes):
	#texto = re.sub(r"(?<=\w)\n", '.', texto)
    with data_path.open('w') as f:
        f.write(text)
        f.close