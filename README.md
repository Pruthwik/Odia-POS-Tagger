# Odia-POS-Tagger
## This is a POS tagger using CRF, you need to install CRF++ toolkit to run this code
### The prediction consists of 2 phases
#### a. Feature Creation for CRF model
#### Run create_features_for_crf_from_conll_pos_data.py for feature creation
#### python create_features_for_crf_from_conll_pos_data.py --input input_file --output feature_file
#### input_file expects a sentence in each line
#### b. Prediction using the CRF model
#### crf_test -m model_path feature_file > features_with_prediction [crf_test is a program in the CRF++ toolkit]
## If you are using this tool, please use the following citation
@misc{https://doi.org/10.48550/arxiv.2204.08960,
  doi = {10.48550/ARXIV.2204.08960},
  url = {https://arxiv.org/abs/2204.08960},
  author = {Mishra, Pruthwik and Sharma, Dipti Misra},
  keywords = {Computation and Language (cs.CL), FOS: Computer and information sciences, FOS: Computer and information sciences},
  title = {Building Odia Shallow Parser},
  publisher = {arXiv},
  year = {2022},
  copyright = {Creative Commons Attribution 4.0 International}
} 
