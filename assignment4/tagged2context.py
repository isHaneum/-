#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import get_morphs_tags as mf

###############################################################################
# 명사, 복합명사 추출
def get_index_terms(mt_list):  # NNG, SL, SH(단일어 및 복합어), NNP(단일어), NR,NNB,SN(복합어)
    nouns = []
    kind_noun = {'NNG', 'NNP', 'NR', 'NNB', 'SL', 'SH', 'SN'} #명사 종류
    single_tags = {'NNG', 'NNP', 'SH', 'SL'} #단일어 가능능

    segments = []
    buffer = []  # 복합합

    for morph, tag in mt_list:# 일단 buffer에 저장
        if tag in kind_noun:
            buffer.append((morph, tag))
        else:
            if buffer:
                segments.append(buffer)
                buffer = []
    if buffer:
        segments.append(buffer)

    # 단일어 + 복합어어
    for seg in segments:
        # 단일어
        for morph, tag in seg:
            if tag in single_tags:
                # SL은 출력 제외
                if tag == 'SL' and len(seg) > 1: #
                    continue
                nouns.append(morph)
        # 복합어
        if len(seg) >= 2: #
            composite = ''.join(m for m, t in seg)
            nouns.append(composite)

    return nouns

###############################################################################
# Converting POS tagged corpus to a context file
def tagged2context( input_file, output_file):

    with open( input_file, "r", encoding='utf-8') as fin, open( output_file, "w", encoding='utf-8') as fout:

        for line in fin:

            # 빈 라인 (문장 경계)
            if line[0] == '\n':
                print(file=fout)
                continue

            try:
                ej, tagged = line.split(sep='\t')
            except:
                print(line, file=sys.stderr)
                continue

            # 형태소, 품사 추출
            # result : list of tuples
            result = mf.get_morphs_tags(tagged.rstrip())

            # 색인어 추출
            terms = get_index_terms(result)

            # 색인어 출력
            for term in terms:
                print(term, end=" ", file=fout)

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( f"[Usage] {sys.argv[0]} file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        output_file = input_file + ".context"
        print( f"processing {input_file} -> {output_file}", file=sys.stderr)

        # 형태소 분석 파일 -> 문맥 파일
        tagged2context( input_file, output_file)
