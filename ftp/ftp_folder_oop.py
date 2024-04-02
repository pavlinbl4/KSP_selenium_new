import ftplib
from get_credentials import Credentials


class FTPClient:
    HOST = 'ftp.kommersant.ru'
    FTP_DIR = "/PHOTO/INBOX/SHOOTS/Pavlenko_Evgenij_2571"

    def __init__(self, shoot_id):
        self.ftp_login = Credentials().ftp_login
        self.ftp_pass = Credentials().ftp_pass
        self.shoot_id = shoot_id

    def connect(self):
        self.ftp = ftplib.FTP(self.HOST, self.ftp_login, self.ftp_pass, timeout=1)
        self.ftp.encoding = "cp1251"
        self.ftp.cwd(self.FTP_DIR)

    def make_dir(self):
        try:
            self.connect()
            self.ftp.mkd(self.shoot_id)
            print("Directory created")
        except ftplib.error_perm:
            print("Directory already exists")
        finally:
            self.list_dir()

    def list_dir(self):
        print(self.ftp.retrlines('LIST'))
        self.ftp_close()

    def ftp_close(self):
        self.ftp.quit()

# if __name__ == '__main__':
# FTPClient('shoot_id').make_dir()
# print(FTPClient.__dict__)
# ftp1 = FTPClient('333')
# print(ftp1.__dict__)
