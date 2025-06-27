#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle
import math # sqrt

###############################################################################
def cosine_similarity(t_vector, c_vector):
    # 코사인 유사도 계산
    # t_vector = 대상어 : {공기어1: value1, 공기어2: value2, ...}
    product = sum(t_vector.get(word, 0) * c_vector.get(word, 0) for word in t_vector)
    sqaure_t = math.sqrt(sum(value ** 2 for value in t_vector.values()))
    square_c = math.sqrt(sum(value ** 2 for value in c_vector.values()))
    
    if sqaure_t == 0 or square_c == 0:
        return 0.0
    
    return product / (square_c * sqaure_t)    


###############################################################################
def most_similar_words(word_vectors, target, topN=10):
    
    result = {}
    target_vector = word_vectors.get(target, None)# target 단어의 벡터를 가져옴 {대상어1: value1, 대상어2:....}
    if target_vector is None:
        return result  # 대상어x -> null
    
    for word, value in target_vector.items():
        if word in target:
            continue
        # 코사인 유사도 계산



        sim = cosine_similarity(target_vector, word_vectors.get(word, {}))
        
        if sim > 0.001:#
            result[word] = sim #유사도 전부 저장
        for word_in_word, value_in_word in word_vectors.get(word, {}).items():
            if word_in_word in target:
                continue
            sim = cosine_similarity(target_vector, word_vectors.get(word_in_word, {}))
            if sim > 0.001:  # 유사도가 0.001 이상인 경우만 저장
                result[word_in_word] = sim


    #  상위 topN개까지


    if not result:
        return result


    return sorted(result.items(), key=lambda x: x[1], reverse=True)[:topN]

###############################################################################
def print_words(words):
    for word, score in words:
        print("%s\t%.3f" %(word, score))
    
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file(pickle)", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1],"rb") as fin:
        word_vectors = pickle.load(fin)

    while True:

        print('\n검색할 단어를 입력하세요(type "^D" to exit): ', file=sys.stderr)
    
        try:
            query = input()
            
        except EOFError:
            print('프로그램을 종료합니다.', file=sys.stderr)
            break
    
        # result : list of tuples, sorted by cosine similarity
        result = most_similar_words(word_vectors, query, topN=30)
        
        if result:
            print_words(result)
        else:
            print('\n결과가 없습니다.')
