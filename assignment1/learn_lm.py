#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle # dump
from collections import defaultdict

# 2gram 언어 모델 학습
# unigram 빈도와 bigram 빈도를 리턴
# 문장의 앞뒤에 시작(<s>)과 끝(</s>)을 나타내는 가상의 단어를 포함해야 함
# 단어 토큰은 공백을 기준으로 분리
def learn_bigram_language_model(input_file):
    # 단어 빈도를 저장할 dictionary
    unigram_counts = defaultdict(int) 
    bigram_counts = {} # dictionary of dictionary
    with open(input_file, 'r', encoding='utf-8') as f:#file
        for line in f:            # 문장 전처리
            line = line.strip() #필요없는 공백 제거
            if not line: #라인 끝나면 for문 종료
                continue

            tokens = ['<s>'] + line.split() + ['</s>']#tokens에 line '<s>'와 '</s>' 추가해서 저장
            
            for token in tokens: #tokens에 있는 token 하나씩 세기
                unigram_counts[token] += 1 #unigram

            for i in range(len(tokens) - 1):#tokens의 길이 - 1 만큼
                token1 = tokens[i]#bigram의 첫번째
                token2 = tokens[i + 1]#두번째
                if token1 not in bigram_counts:#token1이 없으면 새로 저장
                    bigram_counts[token1] = defaultdict(int)#key는 token1, value는 dictionary
                bigram_counts[token1][token2] += 1#dictionary의 dictionary에 token2 개수 추가


    return unigram_counts, bigram_counts

################################################################################
def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input_file output_file(pickle)")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # 모델 학습
    unigram_counts, bigram_counts = learn_bigram_language_model(input_file)
    
    # 모델 저장
    model = {
        'unigram_counts': unigram_counts,
        'bigram_counts': bigram_counts
    }
    
    with open(output_file, 'wb') as f:
        pickle.dump(model, f)

################################################################################
if __name__ == "__main__":
    main() 