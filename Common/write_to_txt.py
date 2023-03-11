import os


def wtrite_to_txt_file(file_path, new_text):
    if os.path.exists(file_path):
        with open(file_path, 'a') as log_file:
            log_file.write(f"{new_text}\n")
    else:
        with open(file_path, 'w') as log_file:
            log_file.write(f"{new_text}\n")
