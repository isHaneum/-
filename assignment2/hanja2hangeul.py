#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import maxmatch

def help(arg):
    print(f"\n{arg} Option file(s)", file=sys.stderr)
    print("\n[Option]", file=sys.stderr)
    print("\t-h1: hangeul", file=sys.stderr)
    print("\t-h2: hangeul(hanja)", file=sys.stderr)

###############################################################################
# 한자-한글 변환 (문자열 단위; 한자 외 다른 문자들이 포함될 수 있음)
# return value: 한자-한글 변환된 문자열 (형식 1)
# ex) 聖經에 -> 성경에
def hanja2hangeul_str1(str):
    return maxmatch.maxmatch(str)
    
###############################################################################
# 한자-한글 변환 (문자열 단위; 한자 외 다른 문자들이 포함될 수 있음)
# return value: 한자-한글 변환된 문자열 (형식 2)
# ex) 聖經에 -> 성경(聖經)에
def hanja2hangeul_str2(str):
    translated = maxmatch.maxmatch(str, debug=False)#한자를 한글로 변환함
    result = ''
    pos = 0
    n = len(translated)
    
    while pos < n:
        if str[pos] != translated[pos]:  # 한자였던 글자
            start = pos
            last = pos + 1
            # 계속 한자인 부분 확인 (translated와 다르면)
            while last < n and str[last] != translated[last]:#translated는 한국어임
                last += 1

            result += translated[start:last] + '(' + str[start:last] + ')'#추가
            pos = last
        else:
            result += translated[pos]#
            pos += 1

    return result 


    while pos < n:
        if str[pos] ! = translated[pos]:
            start = pos
            last = pos + 1
            while last < n and str[last] != translated[last]:#한글이 아니면 계속 +1
                last += 1
#다 체크하고  
            result += translated[start:last] + '(' + str[start:last] + ')' # 번역한거 + 원본
            pos = last#pos는 한자 마지막값
        else
            result += translated[pos]#한글이면 그냥 한글 추가하기
            pos += 1
    return result
            
###############################################################################
def main():
    
    if len(sys.argv) < 3:
        help(sys.argv[0])
        sys.exit(1)
        
    if sys.argv[1] == '-h1':
        func = hanja2hangeul_str1

    elif sys.argv[1] == '-h2':
        func = hanja2hangeul_str2

    else:
        help(sys.argv[0])
        sys.exit(1)
        
    for filename in sys.argv[2:]:

        with open(filename, "r", encoding="utf-8") as infp, open(filename+".out", "w", encoding="utf-8") as outfp:

            print("%s -> %s"%(filename, filename+".out"), file=sys.stderr)

            # 파일 읽기 (라인 단위)
            for line in infp:
                result = []
                words = line.split()

                # 각 단어에 대해 한자-한글 변환
                for word in words:
                    result.append(func(word))

                print(' '.join(result), file=outfp)

###############################################################################
if __name__ == "__main__":
    main()

