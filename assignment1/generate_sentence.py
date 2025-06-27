#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle # load
import random # choice, choices
import sys
import math # log

################################################################################
# 빈도를 가중치로 적용하여 다음 단어 선택 (random.choices 사용)
# 현재 단어가 모델에 없는 경우, 유니그램에서 랜덤하게 단어 선택
def get_next_word(model, current_word):#model은 uni와 bi의 dictionary, current_word는 입력단어
    if current_word in model['bigram_counts']:
        # bigram 모델에서 다음 단어 선택
        next_words = list(model['bigram_counts'][current_word].keys())
        next_word_values = list(model['bigram_counts'][current_word].values())        
        # 확률을 가중치로 사용하여 다음 단어 선택
        next_word = random.choices(next_words, weights=next_word_values)[0]

    else:#bigram 모델에 없으면
        # unigram 모델에서 랜덤하게 다음 단어 선택 근데 <s> 는 제외?
        model['unigram_counts'].pop('<s>', None) # <s> 제거
        next_words = list(model['unigram_counts'].keys())
        next_word_values = list(model['unigram_counts'].values())
        
        # 확률을 가중치로 사용하여 다음 단어 선택
        next_word = random.choices(next_words, weights=next_word_values)[0]
    return next_word
################################################################################
# 문장의 로그 확률 계산 (로그 취한 개별 확률들의 합)
# 모델에 없는 단어 또는 단어 바이그램이 있으면 -100을 더함
def get_probability(model, sentence):
    # 로그 확률 초기화
    log_prob = 0.0

    modelu = model['unigram_counts']  #편하게
    modelb = model['bigram_counts'] #쓰기

    tokens = ['<s>'] + sentence.split() + ['</s>'] # 문장 전처리

    for i in range(len(tokens) - 1):
        prev_word = tokens[i]
        word = tokens[i + 1]
        if prev_word not in modelb:
            # 바이그램 모델에 없는 경우
            log_prob += -100        
        elif prev_word in modelb and word in modelb[prev_word]:
         # bigram 모델에서 로그 확률 계산
            prob = modelb[prev_word][word] / sum(modelb[prev_word].values())
            log_prob += math.log(prob)
        elif word in modelu:
                # unigram 모델에서 로그 확률 계산
            prob = modelu[word] / sum(modelu.values())                    
            log_prob += math.log(prob)
        else:
                    # 모델에 없는 단어 또는 바이그램
            log_prob += -100

    
    return log_prob

################################################################################
# 랜덤 문장 생성
# start_with : 생성할 문장의 시작 단어(들). 없으면 '<s>'로 초기화
def generate_sentence(model, start_with):
    
    if not start_with:# startwith이 없을때
        start_with = '<s>'
    sentence = [start_with.strip()] # 공백 제거 sentence 시작

    while True:
        next_word = get_next_word(model, sentence[-1]) # 마지막 단어로 다음 단어 선택
        sentence.append(next_word) # 문장에 추가
        
        if next_word == '</s>': # while 종료 조건
            if sentence[0] == '<s>':#s로 시작했으면 없애주기
                sentence = sentence[1:]#
            break

    return ' '.join(sentence[:-1]) # 시작과 종료 단어 s,/s 제거

################################################################################
def load_model(model_file):
    with open(model_file, 'rb') as f:
        return pickle.load(f)

################################################################################
def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} model_file")
        sys.exit(1)
    
    model_file = sys.argv[1]
    model = load_model(model_file)
    
    print("2-gram 언어 모델 문장 생성기")
    
    while True:
        cmd = input("\n엔터 또는 문장 시작 단어(들) (q=종료): ")
        
        if cmd.lower() == 'q':
            print("프로그램을 종료합니다.")
            break
        else:
            print("\n<<<< 생성된 문장 >>>>")
            
            for i in range(10):
                sentence = generate_sentence(model, cmd)
                log_prob = get_probability(model, sentence)
                print(f"문장{i+1} : {sentence} (로그 확률: {log_prob:.4f})")

################################################################################
if __name__ == "__main__":
    main() 
