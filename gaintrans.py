from model.inf import Inference

if __name__ == '__main__':
	test_path = "testlist/test3.lst"
	query_path = "testlist/test3.lst"
	model_path = "G:/align/modelparam/params_epoch-189.pkl"
	output_dir = "output/"

	inference = Inference(test_path, query_path, model_path, output_dir)
	preds = inference.inference()

