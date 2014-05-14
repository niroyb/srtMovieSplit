"""Shows the number of times each word is used in a subtitle"""
import re
from collections import Counter

import pysrt


def fix_capital(word):
    """Converts to lower case if not a fully upper cased word"""
    if word.isupper():
        return word
    return word.lower()


def get_all_subtitle_text(srt_path):
    """Returns a string of the text content of the given .srt file"""
    subs = pysrt.open(srt_path)
    texts = [s.text for s in subs]
    return '\n\n'.join(texts)


def get_words(text):
    """Returns a list of the words in the given text"""
    words = re.findall('\w+', text, re.MULTILINE)
    return words


def print_word_counts(words):
    """Prints the most common words in order with their count"""
    for word, count in Counter(words).most_common():
        print count, word


def analyse_srt(srt_path):
    text = get_all_subtitle_text(srt_path)
    words = get_words(text)
    words = map(fix_capital, words)
    print_word_counts(words)

if __name__ == '__main__':
    analyse_srt('DemoData/sintel_en.srt')