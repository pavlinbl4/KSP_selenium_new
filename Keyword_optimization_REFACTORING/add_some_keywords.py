from Common.set_to_string import convert_set_to_string
from Keyword_optimization_REFACTORING.make_better import keywords_opimization


def add_new_keywords(new_keywords, keywords):
    good_keywords = keywords_opimization(keywords)
    good_set = set(good_keywords.split(','))
    new_keywords_set = set(new_keywords.split(','))
    apdated_keywords = good_set.union(new_keywords_set)
    return convert_set_to_string(apdated_keywords)


if __name__ == '__main__':
    print(add_new_keywords(' water   ,      beer,   bread', 'cheese, bread'))