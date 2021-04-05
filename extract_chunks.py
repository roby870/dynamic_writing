#script de ejemplo
import spacy
from chunk_extractor import *
from utils import *
from dynamic_generator import *
from pickle_manager import *

#cargamos los modelos, el de gensim es el que entrenamos y el que usaremos para
#medir la similitud semántica, de acuerdo al corpus de entrenamiento utilizado
nlp = spacy.load("es_core_news_lg")
nlp_gensim = spacy.load('./data/spacy.word2vec.model/')

#instanciamos un objeto de la clase DynamicGenerator
dynamic_generator = DynamicGenerator(nlp_gensim)
#creamos instancias de los filtros que vamos a utilizar:
gramatical_filter = GramaticalFilters(nlp_gensim)


#vemos cómo se pueden extraer chunks y posteriormente cargarlos
#cuando ya estén almacenados como pickles
#(estas sentencias deberían ejecutarse dentro de un loop para recorrer todas las carpetas
#del directorio ./raw_texts, num_docs_folder correspondería
#al número de la iteración, veremos un ejemplo de ese loop más abajo)
list_nsubj = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_pos_sequence_by_dep_tag, "nsubj", ["DET", "NOUN"])
list_nmod = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_pos_sequence_by_dep_tag, "nmod", ["ADP","DET", "NOUN"])
list_obj = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_pos_sequence_by_dep_tag, "obj", ["DET", "NOUN"])
list_root_3_sing_imp_ind = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_one_word_verbs, nlp, "3", "Sing", "Imp", "Ind")
list_nsubj = load_pickle("nsubj")
list_nmod = load_pickle("nmod")
list_obj = load_pickle("obj")
list_root_3_sing_imp_ind = load_pickle("root_3_sing_imp_ind")


#otros ejemplos de extracción de chunks:
res = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_pos_sequence_by_dep_tag, "obl", ["ADP","DET", "NOUN"])
res = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_tokens_by_pos, "ADJ")
res = dynamic_generator.process_files(num_docs_folder, gramatical_filter, get_head, "cop")
res = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_token_by_dep, "amod")
res = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_pos_sequence_by_dep_tag, "nsubj", ["NOUN"])
res = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_one_word_verbs, "3", "Sing", "Pas", "Ind")
res = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_tokens_by_pos, 'AUX', 'Mood=Sub')


#para buscar frases comparativas que empiecen con "como"
#(se deben filtrar los resultados para que solo queden los chunks que empiezan con la palabra "como"):
res = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_pos_sequence_by_dep_tag, "obl", ["SCONJ","DET", "NOUN"])
res = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_pos_sequence_by_dep_tag, "advcl", ["SCONJ","DET", "NOUN"])
res = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_pos_sequence_by_dep_tag, "advcl", ["SCONJ", "VERB", "ADP", "DET", "NOUN"])
res = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_pos_sequence_by_dep_tag, "advcl", ["SCONJ", "DET", "ADJ", "NOUN"])
res = dynamic_generator.process_files(num_docs_folder, gramatical_filter, process_pos_sequence_by_dep_tag, "acl", ["SCONJ", "VERB", "ADP", "DET", "NOUN"])


#ejemplo del loop que mencionábamos para extraer chunks de todos los doc bins
#presentes en el directorio ./raw_texts, en el caso de que hubiera siete directorios
total = []
for n in range(1,8):
    n_as_str = str(n)
    res = dynamic_generator.process_files(n_as_str, gramatical_filter, process_pos_sequence_by_dep_tag, "obl", ["SCONJ","DET", "NOUN"])
    total = total + res
    total = set_chunks_list(total)
    print(len(total)) #para controlar el crecimiento de la lista en cada iteracion
#guardamos lo extraído como pickle
save_pickle(total, "obl")
