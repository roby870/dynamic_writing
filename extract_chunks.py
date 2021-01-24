from core_functions import *


nlp = spacy.load("es_core_news_lg")
nlp_gensim = spacy.load('./data/spacy.word2vec.model/')
list_adj = load_pickle("ADJ")
seq_vi_ruina_en_lugar = load_pickle("seq_vi_ruina_en_lugar")



process_files(nlp, nlp_gensim, '1', process, "nsubj", ["DET", "NOUN"])
process_files(nlp, nlp_gensim, num_docs_folder, process, "nmod", ["ADP","DET", "NOUN"])
process_files(nlp, nlp_gensim, num_docs_folder, process, "obj", ["DET", "NOUN"])
process_files(nlp, nlp_gensim, num_docs_folder, process_one_word_verbs, nlp, "3", "Sing", "Imp", "Ind")


list_nsubj = load_pickle("nsubj")
list_nmod = load_pickle("nmod")
list_obj = load_pickle("obj")
list_root_3_sing_imp_ind = load_pickle("root_3_sing_imp_ind")


#res = process_files(nlp, nlp_gensim, n_as_str, process, "obl", ["ADP","DET", "NOUN"])
#res = process_files(nlp, nlp_gensim, n_as_str, process_tokens_by_pos, "ADJ")
#res = process_files(nlp, nlp_gensim, n_as_str, get_head, "cop")
#res = process_files(nlp, nlp_gensim, n_as_str, process_token_by_dep, "amod")
#res = process_files(nlp, nlp_gensim, n_as_str, process, "nsubj", ["NOUN"])
#res = process_files(nlp, nlp_gensim, n_as_str, process_one_word_verbs, "3", "Sing", "Pas", "Ind")
#res = process_files(nlp, nlp_gensim, n_as_str, process_tokens_by_pos, 'AUX', 'Mood=Sub')


#para buscar frases comparativas que empiecen con como
#(igual despues filtre los resultados para que solo queden los chunks que empezaban con la palabra 'como'):
#res = process_files(nlp, nlp_gensim, n_as_str, process, "obl", ["SCONJ","DET", "NOUN"])
#res = process_files(nlp, nlp_gensim, n_as_str, process, "advcl", ["SCONJ","DET", "NOUN"])
#res = process_files(nlp, nlp_gensim, n_as_str, process, "advcl", ["SCONJ", "VERB", "ADP", "DET", "NOUN"])
#res = process_files(nlp, nlp_gensim, n_as_str, process, "advcl", ["SCONJ", "DET", "ADJ", "NOUN"])
#res = process_files(nlp, nlp_gensim, n_as_str, process, "acl", ["SCONJ", "VERB", "ADP", "DET", "NOUN"])

verbs = []

adj = []
for n in range(1,8):
    n_as_str = str(n)
    res = process_files(nlp, nlp_gensim, n_as_str, "obl", ["SCONJ","DET", "NOUN"])
    print(len(res))
    adj = adj + res
total = set_chunks_list(total)


save_pickle(total, "new_obj")


>>> save_pickle(sequences, "new_seq_vi_ruina_en_lugar_tagged")
>>> actuales = concat_sequences_with_most_similars_chunks(nlp_gensim, sequences, adj, 'ADJ', 5)






new_seqs = []
for seq in seq_vi_ruina_en_lugar:
    seq_text = seq.text.text
    seq_has_vector = seq.text.has_vector
    seq_vector = seq.text.vector
    seq_vector_norm = seq.text.vector_norm
    components = []
    for chunk in seq.components:
        text = chunk.text_embedding.text
        tokens = []
        for t in chunk.text:
            tokens.append(Tokens(t.text, t.pos_, t.tag_))
        source = chunk.source
        has_vector = chunk.text_embedding.has_vector
        vector = chunk.text_embedding.vector
        vector_norm = chunk.text_embedding.vector_norm
        components.append(Chunks(text, tokens, source, has_vector, vector, vector_norm))
    new_seqs.append(Sequences(seq_text, components, seq_has_vector, seq_vector, seq_vector_norm))
