#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from konlpy.tag import Komoran
import sys
# Komoran 객체 생성
komoran = Komoran()

# 입력 파일과 출력 파일 경로


# 결과 저장용 리스트
results = []

# 입력 파일 한 줄씩 읽고 처리
with open(sys.argv[1], 'r', encoding='utf-8') as infile:
    for line in infile:
        line = line.strip()

        
        # 형태소 분석
        morphs = komoran.pos(line)

        # 분석 결과 포맷팅
        formatted = "+".join([f"{word}/{tag}" for word, tag in morphs])
        
        # 전체 줄 포맷
        result_line = f"{line}\t/SS+{formatted}/SS"
        results.append(result_line)

# 출력 파일로 저장
with open(sys.argv[2], 'w', encoding='utf-8') as outfile:
    for r in results:
        outfile.write(r + "\n")