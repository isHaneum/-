#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle

###############################################################################
def vector_indexing(filename):
    with open(filename, "r", encoding='utf-8') as fin:
        word_vectors = {}  # 각 단어 벡터 저장할 dic
#file 예시 
#%포인트 금리    73.371
#%포인트 1%포인트        62.996
#%포인트 2%포인트        62.758
        for line in fin:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            word = parts[0]
            #dictionary 형태로 저장 part0 : {part1: value, part2: value ...}
            if word not in word_vectors:
                word_vectors[word] = {}
            word_vectors[word][parts[1]] = float(parts[2]) # 각 단어에 대한 벡터를 저장

    return word_vectors
    
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(f"[Usage] {sys.argv[0]} in-file out-file(pickle)", file=sys.stderr)
        sys.exit()

    filename = sys.argv[1]
    print(f"processing {filename} ...", file=sys.stderr)
    
    # 공기어 벡터 저장 (dictionary of dictionary)
    word_vectors = vector_indexing(filename)

    print(f"# of entries = {len(word_vectors)}", file=sys.stderr)

    with open(sys.argv[2],"wb") as fout:
        print(f"saving {sys.argv[2]}", file=sys.stderr)
        pickle.dump(word_vectors, fout)
