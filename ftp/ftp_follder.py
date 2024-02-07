import ftplib
import os
from dotenv import load_dotenv

def create_ftp_folder(shoot_id):

    load_dotenv()

    FTP_LOGIN = os.environ.get('FTP_LOGIN')
    FTP_PASS = os.environ.get('FTP_PASS')



    ftp = ftplib.FTP('ftp.kommersant.ru', FTP_LOGIN, FTP_PASS, timeout=None)
    ftp.encoding = "cp1251"
    ftp.cwd("/PHOTO/INBOX/SHOOTS/Pavlenko_Evgenij_2571")
    try:
        ftp.mkd(shoot_id)
        print("try")
    except:
        print("550 Cannot create a file when that file already exists")

    finally:
    # ftp.login() # default, i.e.: user anonymous, passwd anonymous@
        '230 Guest login ok, access restrictions apply.'
        print(ftp.retrlines('LIST'))  # list directory contents

        '226 Transfer complete.'
        ftp.quit()
        '221 Goodbye.'

if __name__ == '__main__':
    create_ftp_folder()

