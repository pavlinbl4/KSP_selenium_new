from Common.regex_tools import keywords_opimization
from Common.set_to_string import convert_set_to_string


def remove_mistake(keyword, keywords):
    good_keywords = keywords_opimization(keywords) # optimized keywords from image on site
    good_keywords_set = set(good_keywords.split(',')) # crete set from optimized keywords
    no_bad_words_set = good_keywords_set - {keyword} # remove mistake from good keywords
    return convert_set_to_string(no_bad_words_set)


if __name__ == '__main__':
    print(remove_mistake('rabbit', 'fox, box, rabbit, beer'))
