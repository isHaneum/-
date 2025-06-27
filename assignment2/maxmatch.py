#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import hanja2hangeul_table
import hanja2hangeul_dic

h2h_table = hanja2hangeul_table.hanja2hangeul_table
h2h_dic = hanja2hangeul_dic.hanja2hangeul_dic

# 한자 문자열을 입력받아 한글로 변환하는 최장일치 알고리즘
# text (str): 변환할 한자 문자열
# debug (bool): 디버깅 여부. True이면 디버깅 정보 출력 ('+'로 구분된 문자열 반환)
# Return: 변환된 한글 문자열
def maxmatch(text, debug=False):
        
    if not text:
        return ""

    result = []

    n = len(text)
    pos = 0 #position

#구조를 어떻게 찾을까?
# 테이블에서 한자
    while pos < n: # 한자가 있다면 어절에서 한자 단어 시작 위치 찾기
        max_word = ''
        if text[pos] in h2h_table:#글자가 한자라면
            for i in range(1, n - pos + 1):# n+1 - pos
                word = text[pos:pos + i]
                if word in h2h_dic:#table에서 최장일치 분석
                    max_len = i
                    max_word = word


            if (max_word) :#table에 있다면
                result.append(h2h_dic[max_word])
                pos += max_len#pos+ maxlen
            else:#table에 없다면
                result.append(h2h_table[text[pos]][0])#h2h table 1번째값만 추가
                pos += 1
        else:
            result.append(text[pos])# 한자가 아니라면 그냥 result에 추가
            pos += 1
    if debug:
        return '+'.join(result)
    return ''.join(result)

###############################################################################
def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input_file>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            
            words = line.split()

            for word in words:
                word_result = maxmatch(word, debug=True)
                
                print(word, word_result, sep='\t')

###############################################################################
if __name__ == "__main__":
    main()

