import pysrt
import re
from collections import Counter

def fix_capital(string):
    if string.isupper():
        return string
    return string.lower()

def get_word_counts(srt_path):
    subs = pysrt.open(srt_path)
    freq = Counter()
    for s in subs:
        words = map(fix_capital, re.findall('\w+', s.text))
        freq.update(words)
    return freq

def print_word_counts(word_counts):
    for word, count in word_counts.most_common():
        if len(word) > 2:
            print count, word

def analyse_srt(srt_path):
    counts = get_word_counts(srt_path)
    print_word_counts(counts)

if __name__ == '__main__':
    analyse_srt('DemoData/sintel_en.srt')