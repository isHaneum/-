import sys
from collections import defaultdict

def word_count_by_year(filenames):
    word_freq_by_word = defaultdict(lambda: [0] * len(filenames))  #단어, [빈도 리스트]

    for year_id, filename in enumerate(filenames):
        with open(filename, "r", encoding='utf-8') as fin:
            words = fin.read().split()
            for word in words:
                word_freq_by_word[word][year_id] += 1  #해당 연도 인덱스에 count 추가

    return word_freq_by_word

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    input_files = sys.argv[1:]
    word_freq_by_word = word_count_by_year(input_files)

    with open("result.txt", "w", encoding='utf-8') as fout:

        for word in sorted(word_freq_by_word.keys()):#알파벳 순으로
            freq_list = word_freq_by_word[word]
            print(f"{word}\t{freq_list}", file=fout)