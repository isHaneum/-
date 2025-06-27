#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
from itertools import combinations 

###############################################################################
def print_word_freq(filename, word_freq):
    with open(filename, "wt", encoding='utf-8') as fout:
        print(f"#Total\t{sum(word_freq.values())}", file=fout)
        for w, freq in sorted(word_freq.items()):
            print(f"{w}\t{freq}", file=fout)



###############################################################################
def print_coword_freq(filename, coword_freq):
    with open(filename, "wt", encoding='utf-8') as fout:
        for (w1, w2), freq in sorted(coword_freq.items()):
            print(f"{w1}\t{w2}\t{freq}", file=fout)



###############################################################################
def get_coword_freq(filename):
    
    coword_freq = defaultdict(int)
    word_context_size = defaultdict(int)
    word_freq = defaultdict(int)
    total_unigram_count = 0
    
    with open(filename, "r", encoding='utf-8') as fin:
        for line in fin:
            words = sorted((line.strip().split())) #한 문장의 단어들
            for word in words:
                word_context_size[word] += len(words)
            word_context_size[word] -= 1 # 단어 context 크기 계산
            words = sorted(set(line.strip().split())) #한 문장의 단어들
            if not words:
                continue
            # 단어 빈도 계산

            for word in words:
                word_freq[word] += 1
                total_unigram_count += 1
            # 단어 context 크기 계산
            

            # co-word 빈도 계산
            for w1, w2 in (combinations(words, 2)): 
                if w1 != w2:
                    coword_freq[(w1, w2)] += 1# w2, w1은 제외

            

    return word_freq, coword_freq, word_context_size

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        
        print(f"processing {input_file}", file=sys.stderr)
        
        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos] # ex) "2017.tag.context" -> "201more 7"
        
        # 1gram, 2gram, 1gram context 빈도를 알아냄
        word_freq, coword_freq, word_context_size = get_coword_freq(input_file)

        # unigram 출력
        print_word_freq(file_stem+".1grams", word_freq)
        
        # bigram(co-word) 출력
        print_coword_freq(file_stem+".2grams", coword_freq)

        # unigram context 출력
        print_word_freq(file_stem+".1gram_contexts", word_context_size)
