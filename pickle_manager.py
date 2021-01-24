import pickle

def save_pickle(results, name_results):
	name_results = './pickles/' + name_results + '.pkl'
	with open(name_results, 'wb') as f:
		pickle.dump(results, f)
		f.close()


def load_pickle(name_pickle):
	with open('./pickles/' + name_pickle + '.pkl', 'rb') as f:
		pickle_object = pickle.load(f)
		f.close()
	return pickle_object
