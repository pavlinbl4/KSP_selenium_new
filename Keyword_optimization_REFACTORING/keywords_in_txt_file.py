from datetime import datetime
from Common.set_to_string import convert_set_to_string
import logging

keyword_file = '/Users/evgeniy/Documents/keywords/keywords in work.txt'


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create formatter and file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)

# Add file handler
logger.addHandler(file_handler)


def write_keywords_in_txt_file(final: set):

    with open(keyword_file, 'a') as text_file:
        text_file.write('\n')
        text_file.write(datetime.now().strftime("%Y-%m-%d") + '\n')
        final_string = convert_set_to_string(final)
        text_file.write(final_string)

        # Log final keywords
        logger.debug(final_string)



if __name__ == '__main__':
    write_keywords_in_txt_file({'а', 'роза', 'упала', 'на', 'лапу', 'азора'})
