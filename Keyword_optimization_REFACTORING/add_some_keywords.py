from Common.regex_tools import keywords_opimization
from Common.set_to_string import convert_set_to_string


def add_new_keywords(new_keywords: str, keywords: str) -> str:
    good_keywords = keywords_opimization(keywords)
    good_set = set(word.strip() for word in good_keywords.split(','))
    new_keywords_set = set(word.strip() for word in new_keywords.split(','))
    updated_keywords = good_set.union(new_keywords_set)
    return convert_set_to_string(updated_keywords)


if __name__ == '__main__':
    print(add_new_keywords(' new_kyeword_1   ,      new_keyword_2,   new_keyword_3', 'old1, old2'))
