<h1>Dynamic Writing</h1>

<h4>Preprocesamiento del corpus y entrenamiento del modelo de similitud mediante el algoritmo word2vec</h4>

En primer lugar, ejecutar el script preprocessor.py para realizar data cleaning sobre los textos originales (se espera formato txt)
presentes en el directorio raw_texts y almacenarlos en el directorio training_corpus. Los almacena de la forma esperada
por los algoritmos de entrenamiento de Gensim. Optativamente, se pueden utilizar los scripts trim_head y trim_tail para eliminar las n primeras líneas de un archivo txt ó para quedarse con las n primeras líneas de un archivo txt. En el archivo instructivo_trim_archivos se indica cómo invocar a los scripts con los parámetros pertinentes.
Para crear el modelo que servirá para establecer niveles de similitud entre distintos chunks se debe ejecutar el script train_and_save_w2v.py. En ese archivo también se indican los pasos a seguir para que el modelo (entrenado con la librería Gensim) quede interpretable por SpaCy.

<h4>Taggeo del corpus</h4>

Luego ejecutar el script split_files.sh para fragmentar los textos crudos de modo que en los posteriores procesamientos no se generen documentos tan extensos y así evitar problemas de alocación de memoria (los taggeos de SpaCy generan estructuras de datos muy pesadas). 
Los textos, una vez fragmentados, deben estar ubicados en diferentes subdirectorios dentro del directorio raw_texts. Cuanto más divididos estén los textos originales en diferentes subdirectorios, más eficiente será el procesamiento. 20 fragmentos por subdirectorio es el número recomendado. Esto es así porque cuando se ejecute posteriormente el método tag_files de la clase BasicTagger, mantendrá en memoria todos los documentos de cada subdirectorio y solo al finalizar el procesamiento de los textos de un subdirectorio los guardará dentro de él en un archivo binario que contendrá un objeto de tipo DocBin. 

<h4>Extracción y almacenamiento de chunks</h4>

Los objetos de la clase Chunk_Extractor, mediante el método process_files, serán los encargados de llevar a memoria todos los DocBins de 
un directorio determinado (se indica por parámetro) y, una vez transformados en los docs originales, realizar el procesamiento indicado. Utilizará objetos de las distintas clases de Filters para realizar los diversos procesamientos. Los resultados serán estructuras de datos que pueden almacenarse como pickles ó en una base de datos, para que después se utilicen como sugerencias dentro del proceso generativo. 

<h4>Proceso de escritura </h4>

Los objetos de la clase Dynamic_Generator tienen la responsabilidad de extender una secuencia determinada. Es la clase core del sistema. La API debería hacer peticiones que el sistema delegue en objetos de esta clase, salvo que se dé al usuario la posibilidad de elaborar su propio conjunto de datos a partir de los documentos almacenados como DocBins, en ese caso también se realizarían peticiones que se deleguen a objetos de la clase Chunk_Extractor.
El sistema cuenta con mecanismos morfosintácticos como semánticos (gracias al modelo de word embeddings entrenado) para asistir al usuario en su proceso de escritura.

<h4>Casos de uso</h4>

El uso esperado es el de un asistente para la escritura, en el que se le pidan fragmentos del texto en construcción al sistema pero se espera que el usuario también contribuya en la elaboración del texto mediante su propia redacción. Este asistente debería poder adaptarse a múltiples usos, sea con fines recreativos para facilitar escritura creativa, explorar la construcción de textos híbridos (elaborados por humanos y máquinas), asistir en la resolución de consignas de escritura con fines educativos, etc. La versión principal del sistema está pensada para ser lo más genérica y abstracta posible, siendo extensible y adaptable a cada caso de uso. 

<h4>Proyecto final</h4>

El proyecto final comprende el desarrollo de una interfaz, desde la que el usuario pueda escribir el texto con la asistencia de este sistema. Eventualmente también podría desarrollarse la funcionalidad para que el usuario establezca desde la interfaz su propio corpus, adjuntando archivos de extensión txt al sistema para que se realice el preprocesamiento y procesamiento de ese corpus, estableciendo tanto los DocBins del sistema como el modelo de Gensim a partir de esos archivos txt enviados por el usuario.  

<h4>Scripts de ejemplo</h4>

Se agregan scrips de ejemplos de uso, tanto de cómo extraer chunks del corpus (archivo extract_chunks.py) como del proceso de generación de una secuencia textual (generation.py)  
