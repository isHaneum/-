#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math # sqrt

###############################################################################
def read_frequency(filename):
    freqs = {}
    with open(filename, "r", encoding='utf-8') as fin:
        for line in fin:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                word, freq = parts
                freqs[word] = int(freq)
    if '#Total' not in freqs:
        freqs['#Total'] = sum(v for k, v in freqs.items() if k != '#Total')
    
    return freqs
###############################################################################
def calc_tscore(filename, unigrams, unigram_context, uni_N, cutoff):
    
    t_scores = {}
    with open(filename, "r", encoding='utf-8') as fin:
 #O = unigram_context[(target, coword)] # target과 coword의 공기빈도
 #E = unigrams[target] * unigrams[coword] / uni_N # 기대빈도도
 #t score = O - E / sqrt(O)
 
        for line in fin:
            w1, w2, O = line.strip().split()
            O = int(O)
            
            if O < cutoff:
                continue


            if w1 in unigram_context and w2 in unigrams:
                E1 = unigram_context[w1] * unigrams[w2] / uni_N
                if E1 > 0 and w2 not in w1:  # 공기어(w2)가 대상어(w1)에 포함되면 필터
                    t_score1 = (O - E1) / math.sqrt(O)
                    if t_score1 > 0:
                        t_scores[(w1, w2)] = t_score1

            if w2 in unigram_context and w1 in unigrams:
                E2 = unigram_context[w2] * unigrams[w1] / uni_N
                if E2 > 0 and w1 not in w2:  # 공기어(w1)가 대상어(w2)에 포함되면 필터
                    t_score2 = (O - E2) / math.sqrt(O)
                    if t_score2 > 0:
                        t_scores[(w2, w1)] = t_score2
    return t_scores
###############################################################################
def print_tscore(filename, t_scores):
    with open(filename, "wt", encoding='utf-8') as fout:
        for (target, coword), t_score in sorted((t_scores.items())):

            if t_score >= 0:  # t점수가 음수인 경우는 제외
                print(f"{target}\t{coword}\t{t_score:.3f}", file=fout)


###############################################################################
if __name__ == "__main__":

    CUTOFF = 5 # 공기빈도가 이 값 이상인 경우만 t점수를 계산
    
    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        
        print(f"processing {input_file}", file=sys.stderr)

        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos] # ex) "2017.2gram" -> "2017"
    
        print(f"\tLoading {file_stem}.1gram", file=sys.stderr)
        unigrams = read_frequency(file_stem+".1gram")
        
        print(f"\tLoading {file_stem}.1gram_context", file=sys.stderr)
        unigram_context = read_frequency(file_stem+".1gram_context")
        
        uni_N = unigrams['#Total'] # unigram 빈도 합
        
        # key : (target, coword)
        # value : t-score
        t_scores = calc_tscore(input_file, unigrams, unigram_context, uni_N, CUTOFF)
        
        print_tscore(file_stem+".tscores", t_scores)