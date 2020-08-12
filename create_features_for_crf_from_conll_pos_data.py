"""Tokenize the sentences and create features for testing with CRF."""
import argparse
import codecs

# input is the folder containing the SSF files


def read_lines_from_file(file_path):
    """
    Read lines from file.

    Args:
    file_path: Enter the file path

    Returns:
    lines: Lines from file
    """
    with open(file_path, 'r', encoding='utf-8') as file_read:
        return file_read.readlines()


def find_sentences_in_text(lines):
    """
    Find sentences from ConLL format data.

    Args:
    lines: Lines read from file

    Returns:
    sentences: Sentences formed from the lines
    """
    tempLine, sentences = list(), list()
    for line in lines:
        line = line.strip()
        if line:
            tempLine.append(line)
        else:
            if tempLine:
                sentences.append('\n'.join(tempLine))
            tempLine = list()
    if tempLine:
        sentences.append('\n'.join(tempLine))
        tempLine = list()
    print(len(sentences))
    return sentences


def read_file_and_find_features_from_sentences(file_path):
    """
    Read lines from file and find the features.

    Args:
    file_path: Enter the file path

    Returns:
    """
    features_string = ''
    lines = read_lines_from_file(file_path)
    sentences_found = find_sentences_in_text(lines)
    features_string = find_features_from_sentences(sentences_found)
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
        for line in sentence.split('\n'):
            if line.strip():
                token = line.strip()
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
