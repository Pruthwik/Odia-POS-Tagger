# Odia-POS-Tagger
## This is a POS tagger using CRF, you need to install CRF++ toolkit to run this code
### The prediction consists of 2 phases
#### a. Feature Creation for CRF model
#### Run create_features_for_crf_from_conll_pos_data.py for feature creation
#### python create_features_for_crf_from_conll_pos_data.py --input input_file --output feature_file
#### input_file expects a sentence in each line
#### b. Prediction using the CRF model
#### cef_test -m model_path feature_file > features_with_prediction [crf_test is a program in the CRF++ toolkit]
