#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict

###############################################################################
def word_count(filename):

    word_freq = defaultdict(int)#defaultdict(int) # int로 초기화된 딕셔너리
    # 파일을 읽어서 단어 빈도 계산
    # with open(filename

    with open( filename, "r", encoding='utf-8') as fin:

        for word in fin.read().split():
            word_freq[word] += 1
    
    return word_freq
#whit open(filename, "r", encoding='utf-8') as fin:for wor d in fin.read().split():word_freq
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:

        output_file = input_file + ".1gram"

        print(f"processing {input_file} -> {output_file}", file=sys.stderr)

        word_freq = word_count( input_file)
    
        with open(output_file, "wt", encoding='utf-8') as fout:

            for w, freq in sorted(word_freq.items()):
                print(f"{w}\t{freq}", file=fout)


wit open(filename, "r", encodingqq='utf-8') as fin:
    for worid in fin.read().

    split():
    

    for w, freq in sorted(items)