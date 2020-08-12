# how to run the code
# python3 tokenizer_for_file.py --input InputFileName --output OutputFileName --lang 0
# Author Darshan and Pruthwik
import re
import argparse


token_specification = [
    ('datemonth',
     r'^(0?[1-9]|1[012])[-\/\.](0?[1-9]|[12][0-9]|3[01])[-\/\.](1|2)\d\d\d$'),
    ('monthdate',
     r'^(0?[1-9]|[12][0-9]|3[01])[-\/\.](0?[1-9]|1[012])[-\/\.](1|2)\d\d\d$'),
    ('yearmonth',
     r'^((1|2)\d\d\d)[-\/\.](0?[1-9]|1[012])[-\/\.](0?[1-9]|[12][0-9]|3[01])'),
    ('EMAIL1', r'([\w\.])+@(\w)+\.(com|org|co\.in)$'),
    ('url1', r'(www\.)([-a-z0-9]+\.)*([-a-z0-9]+.*)(\/[-a-z0-9]+)*/i'),
    ('url', r'/((?:https?\:\/\/|www\.)(?:[-a-z0-9]+\.)*[-a-z0-9]+.*)/i'),
    ('BRACKET', r'[\(\)\[\]\{\}]'),       # Brackets
    ('NUMBER', r'^(\d+)([,\.]\d+)*(\S+)*'),  # Integer or decimal number
    # ('NUMBER', r'^(\d+)([,\.]\d+)*(\S+)*'),  # Integer or decimal number
    ('ASSIGN', r'[~:]'),          # Assignment operator
    ('END', r'[;!_]'),           # Statement terminator
    ('EQUAL', r'='),   # Equals
    ('OP', r'[+*\/\-]'),    # Arithmetic operators
    ('QUOTES', r'[\"\'‘’“”]'),          # quotes
    ('Fullstop', r'(\.+)$'),
    ('ellips', r'\.(\.)+'),
    ('HYPHEN', r'[-+\|+]'),
    ('Slashes', r'[\\\/]'),
    ('COMMA12', r'[,%]'),
    ('hin_stop', r'।'),
    ('quotes_question', r'[”\?]'),
    ('hashtag', r'#'),
    ('abbr', r'([\U00000900-\U0000097Fa-zA-Z]+\.)+')
]
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
get_token = re.compile(tok_regex)


def tokenize(list_s):
    tkns = []
    for wrds in list_s:
        wrds_len = len(wrds)
        initial_pos = 0
        end_pos = 0
        while initial_pos <= (wrds_len - 1):
            mo = get_token.match(wrds, initial_pos)
            if mo is not None and len(mo.group(0)) == wrds_len:
                tkns.append(wrds)
                initial_pos = wrds_len
            else:
                match_out = get_token.search(wrds, initial_pos)
                if match_out is not None:
                    end_pos = match_out.end()
                    if match_out.lastgroup == "NUMBER":
                        aa = wrds[initial_pos:(end_pos)]
                    elif match_out.lastgroup == "abbr":
                        if end_pos == len(wrds):
                            pass
                        else:
                            end_pos = wrds.rfind('.') + 1
                        aa = wrds[initial_pos: end_pos]
                    else:
                        aa = wrds[initial_pos:(end_pos - 1)]
                    if aa != '':
                        tkns.append(aa)
                    if match_out.lastgroup not in ["NUMBER", "abbr"]:
                        tkns.append(match_out.group(0))
                    initial_pos = end_pos
                else:
                    tkns.append(wrds[initial_pos:])
                    initial_pos = wrds_len
    return tkns


def read_file_and_tokenize(input_file, output_file):
    string_sentences = ''
    file_read = open(input_file, 'r', encoding='utf-8')
    text = file_read.read().strip()
    end_sentence_punctuations = ['?', '۔', '؟', '।', '!', '|']
    all_punctuations = '!"#$%&\'\(\)*+,\-/:;<=>?@[\\]^_`{|}~“”'
    quotes = '\'"“”`'
    sentences = re.findall(
        ".*?[" + ''.join(end_sentence_punctuations) + "]+[" + quotes + "]?|.*?\n", text + '\n')
    for index, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if sentence != '':
            if re.findall('[' + all_punctuations + ']', sentence) and len([token.strip() for token in re.findall('[' + all_punctuations + ']', sentence) if token.strip()]) == len(sentence):
                continue
            list_tokens = tokenize(sentence.split())
            string_sentences += '\n'.join(list_tokens) + \
                '\n\n'
    write_data_to_file(output_file, string_sentences)


def write_data_to_file(output_file, data):
    with open(output_file, 'w', encoding='utf-8') as file_write:
        file_write.write(data.strip() + '\n')
        file_write.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input', dest='inp', help="enter the input file path")
    parser.add_argument(
        '--output', dest='out', help="enter the output file path")
    args = parser.parse_args()
    read_file_and_tokenize(args.inp, args.out)
