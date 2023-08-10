import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def create_file_if_not_exists(folder_path, file_name):
    # Validate inputs
    if not os.path.isdir(folder_path):
        raise ValueError(f"{folder_path} is not a valid folder")

    file_path = os.path.join(folder_path, file_name)

    # Create file if doesn't exist
    if not os.path.exists(file_path):
        logger.info("Creating file %s", file_path)
        with open(file_path, 'w') as f:
            pass

    return file_path


if __name__ == '__main__':
    folder_path = Path.home() / 'Documents' / 'keywords'
    file_name = 'bad_words.txt'

    created_file = create_file_if_not_exists(folder_path, file_name)
    print(created_file)
