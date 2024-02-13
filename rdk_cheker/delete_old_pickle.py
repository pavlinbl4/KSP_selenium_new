import glob
import os
from datetime import date

def delete_old_pickle(today_filename):
    # today_filename = f'{date.today().strftime("%d_%m_%y")}.pickle'
    if len(glob.glob(f'*.pickle')) != 0:
        pickle_file = glob.glob(f'*.pickle')[0]
        print(pickle_file)
        if pickle_file != today_filename:
            os.remove(pickle_file)






if __name__ == '__main__':
    delete_old_pickle()