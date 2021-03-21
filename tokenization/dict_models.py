from base_tokenizer import BaseTokenizer
import utils
__author__ = "Ha Cao Thanh"
__copyright__ = "Copyright 2018, DeepAI-Solutions"


class LongMatchingTokenizer(BaseTokenizer):
    def __init__(self):
        """
        Initial config
        :param bi_grams_path: path to bi-grams set
        :param tri_grams_path: path to tri-grams set
        """
        self.bi_grams = utils.load_corpus('bi')
        self.tri_grams = utils.load_corpus('tri')

    def tokenize(self, text):
        """
        Tokenize text using long-matching algorithm
        :param text: input text
        :return: tokens
        """
        syllables = LongMatchingTokenizer.syllablize(text)
        syl_len = len(syllables)
        curr_id = 0
        word_list = []
        done = False
        while (curr_id < syl_len) and (not done):
            curr_word = syllables[curr_id]
            if curr_id >= (syl_len - 1):
                word_list.append(curr_word)
                done = True
            else:
                next_word = syllables[curr_id + 1]
                pair_word = ' '.join([curr_word.lower(), next_word.lower()])
                if curr_id >= (syl_len - 2):
                    if pair_word in self.bi_grams:
                        word_list.append('_'.join([curr_word, next_word]))
                        curr_id += 2
                    else:
                        word_list.append(curr_word)
                        curr_id += 1
                else:
                    next_next_word = syllables[curr_id + 2]
                    triple_word = ' '.join([pair_word, next_next_word.lower()])
                    if triple_word in self.tri_grams:
                        word_list.append('_'.join([curr_word, next_word, next_next_word]))
                        curr_id += 3
                    elif pair_word in self.bi_grams:
                        word_list.append('_'.join([curr_word, next_word]))
                        curr_id += 2
                    else:
                        word_list.append(curr_word)
                        curr_id += 1
        return word_list


"""Tests"""


def test():
    lm_tokenizer = LongMatchingTokenizer()
    tokens = lm_tokenizer.tokenize("Con Hà bị ngu vl")
    print(tokens)


if __name__ == '__main__':
    test()

