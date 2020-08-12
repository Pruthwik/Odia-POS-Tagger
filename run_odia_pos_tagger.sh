# how to run this
# sh run_odia_pos_tagger.sh input_file_path output_file_path
# for output_file_path, give just a name
input_file=$1
ouput_file=$2
python tokenizer_for_file.py --input $input_file --output input-tokenized-conll.txt
python create_features_for_crf_from_conll_pos_data.py --input input-tokenized-conll.txt --output input-features.txt
crf_test -m odia_pos_4k_model input-features.txt > input_pos_predicted.txt
cut -f1,14 input_pos_predicted.txt > $ouput_file
