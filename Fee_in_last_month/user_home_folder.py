from pathlib import Path
import os


class HomeFolder:
    def __init__(self, subfolder_name):
        self.subfolder_name = subfolder_name
        self.user_home_directory = f'{Path.home()}/Documents/Kommersant'

    def add_subfolder(self):
        path = os.path.join(self.user_home_directory, self.subfolder_name)
        os.makedirs(path, exist_ok=True)
        return f"{self.user_home_directory}/{self.subfolder_name}"

if __name__ == '__main__':

    folder = HomeFolder('add_subfolder_to_kommersant')
    print(folder.add_subfolder())