from pymystem3 import Mystem
from Common.regex_tools import extract_only_words


def lema(any_text:str)->list:
    lemmatized_words = extract_only_words(Mystem().lemmatize(any_text))
    return [word for word in lemmatized_words if len(word) > 2]


if __name__ == '__main__':
    print(lema(
        'XXVI Петербургский международный экономический форум (ПМЭФ) 2023 в конгрессно-выставочном центре (КВЦ) "Экспофорум". Генеральный директор компании «Метеор Лифт» (Meteor lift) Игорь Майоров.'))
