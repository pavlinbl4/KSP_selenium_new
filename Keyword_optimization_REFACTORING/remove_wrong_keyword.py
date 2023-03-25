from Common.set_to_string import convert_set_to_string
from Keyword_optimization_REFACTORING.make_better import keywords_opimization


def remove_mistake(keyword, keywords):
    good_keywords = keywords_opimization(keywords)
    good_set = set(good_keywords.split(','))
    no_bad_word_set = good_set.difference(set([keyword]))
    return convert_set_to_string(no_bad_word_set)




if __name__ == '__main__':
    print(remove_mistake('rabbit', 'fox, box, rabbit, beer'))