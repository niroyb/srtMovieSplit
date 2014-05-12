import pysrt
import re
from collections import Counter

SRT_FILE = 'Example.srt'

def fix_capital(string):
    if string.isupper():
        return string
    return string.lower()

def main():
    subs = pysrt.open(SRT_FILE)
    freq = Counter()
    for s in subs:
        words = map(fix_capital, re.findall('\w+', s.text))
        freq.update(words)
        #print words
    for word, count in freq.most_common():
        if len(word) > 2 and count > 5:
            print count, word
    pass

main()