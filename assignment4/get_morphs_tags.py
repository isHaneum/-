#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

###############################################################################
def get_morphs_tags(tagged):#tagged는 최근/NNG 한 문장장

    result = []
    buffer = ''
    i = 0
    while i < len(tagged):
        ch = tagged[i]
        if ch == '+':
            plus_count = 1 # + 갯수
            while i + plus_count < len(tagged) and tagged[i + plus_count] == '+':# +연속 갯수
                plus_count += 1#pluscnt++

            next_slash = (i + plus_count < len(tagged) and tagged[i + plus_count] == '/')#다음이 /라면면
            if plus_count > 1 and '/' not in buffer and next_slash: # +가 2 이상이고 다음이 slash라면

                buffer += '+' * plus_count  #buffer에 +갯수 저장
                i += plus_count# 갯수만큼 넘어가기
                continue

            if buffer and '/' in buffer: # buffer에 /가 있다면
                morph, tag = buffer.rsplit('/', 1) # /1개 기준으로 왼쪽 morph, 오른쪽 tag
                result.append((morph, tag))
            buffer = '' # 버퍼 초기화

            if plus_count > 1:
                for _ in range(1, plus_count): #plus 1보다 많으면면
                    buffer += '+' #plus 갯수만큼 
                result.append((buffer, 'SW')) #sw로 추가
                i += plus_count #갯수만큼 넘어가기
                buffer = ''
                continue
            else:
                i += plus_count
        else: #다 아니면 buffer에 그냥 그 문자 저장
            buffer += ch
            i += 1

    if buffer and '/' in buffer:
        
        morph, tag = buffer.rsplit('/', 1) #split
        result.append((morph, tag))
    result = [(m, t) for m, t in result if m.strip()]

    return result



###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( f"[Usage] {sys.argv[0]} in-file", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1], encoding='utf-8') as fin:

        for line in fin:

            # 2 column format
            segments = line.split('\t')

            if len(segments) < 2:
                continue

            # result : list of tuples
            result = get_morphs_tags(segments[1].rstrip())

            for morph, tag in result:
                print(morph, tag, sep='\t')
