# If data type is conll where the common format of each line is token\tpos_tag
## python create_features_for_pos_crf_training.py --input Sample-Odia-CoNLL/ --output sample_odia_pos_features.txt --type conll
# If data type is SSF for SSF annotated POS files
## python create_features_for_pos_crf_training.py --input Sample-Odia-SSF/ --output sample_odia_pos_features.txt --type ssf
# How to train a crf using CRF++ toolkit (https://taku910.github.io/crfpp/), requires a template for reading features
## crf_learn template_pos_4pre_7suff_5window feature_file_path model_pos_odia.m
