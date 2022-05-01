"""Tokenize the sentences and create features for testing with CRF."""
# this program expects each sentence in a single line.
import argparse
import codecs
import re


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
    tkns = list()
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


def read_lines_from_file(file_path):
    """
    Read lines from file.

    Args:
    file_path: Enter the file path

    Returns:
    lines: Lines from file
    """
    with open(file_path, 'r', encoding='utf-8') as file_read:
        return [line.strip() for line in file_read.readlines() if line.strip()]


def read_file_and_find_features_from_sentences(file_path):
    """
    Read lines from file and find the features.

    Args:
    file_path: Enter the file path

    Returns:
    """
    features_string = ''
    lines = read_lines_from_file(file_path)
    features_string = find_features_from_sentences(lines)
    return features_string


def find_features_from_sentences(sentences):
    """
    Find features for all the sentences.

    :param sentences: Sentences read from file
    :return features: Features of all tokens for each sentence combined for all the sentences
    """
    prefix_len = 4
    suffix_len = 7
    features = ''
    for sentence in sentences:
        sentence_features = ''
        tokens = sentence.split()
        # print(len(tokens), 'B')
        # tokens = tokenize(tokens)
        # print(len(tokens), 'A')
        for token in tokens:
            sentence_features += token + '\t'
            for i in range(1, prefix_len + 1):
                sentence_features += affix_feats(token, i, 0) + '\t'
            for i in range(1, suffix_len + 1):
                sentence_features += affix_feats(token, i, 1) + '\t'
            sentence_features = sentence_features + 'LESS\n' if len(token) <= 4 else sentence_features + 'MORE\n'
        if sentence_features.strip():
            features += sentence_features + '\n'
    return features


def affix_feats(token, length, type_aff):
    """
    Find features related to affixes.

    :param line: extract the token and its corresponding suffix list depending on its length
    :param token: the token in the line
    :param length: length of affix
    :param type: 0 for prefix and 1 for suffix
    :return suffix: returns the suffix
    """
    if len(token) < length:
        return 'NULL'
    else:
        if type_aff == 0:
            return token[:length]
        else:
            return token[len(token) - length:]


def write_file(out_path, data):
    """
    Write text to file.

    :param out_path: Enter the path of the output file
    :param data: Enter the token features of sentence separated by a blank line
    :return: None
    """
    with codecs.open(out_path, 'w+', 'utf-8') as fout:
        fout.write(data)
        fout.close()


def main():
    """
    Pass arguments and call functions here.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='inp', help="Add the input path from where tokens and its features will be extracted")
    parser.add_argument('--output', dest='out', help="Add the output file where the features will be saved")
    args = parser.parse_args()
    features_extracted = read_file_and_find_features_from_sentences(args.inp)
    write_file(args.out, features_extracted)


if __name__ == '__main__':
    main()
