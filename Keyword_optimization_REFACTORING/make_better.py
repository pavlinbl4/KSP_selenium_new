import re


def keywords_opimization(keywords):
    step_1 = re.sub(
        r'(_РЕЛИГИЯ|_гипермаркеты|_фирмы|_ПРЕДМЕТ_|'
        r'_People|_ГОРОДА И СТРАНЫ_|'
        r'_PERSONS|_CITY|_ИМЯ СОБСТВЕННОЕ_|'
        r'COUNTRY|_РУССКИЙ_|'
        r'_ГОРОДА И СТРАНЫ|\|)',
        ' ',
        keywords).strip()
    step_2 = re.sub(r'\b([^\W\d_]+)(\s+\1)+\b', r'\1', re.sub(r'\W+', ' ', step_1).strip(), flags=re.I).strip()
    keywords = re.sub(r'\s+', ', ', step_2)
    return keywords
