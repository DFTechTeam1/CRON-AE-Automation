import os
from ftplib import FTP_TLS
from utils.logger import logging


class NasFTP:
    def __init__(self, host: str, username: str, password: str, port: int):
        self.host: str = host
        self.username: str = username
        self.password: str = password
        self.port: int = port
        self.ftp = None

    def connect(self):
        self.ftp = FTP_TLS()
        self.ftp.connect(host=self.host, port=int(self.port))
        self.ftp.auth()
        self.ftp.prot_p()
        self.ftp.login(user=self.username, passwd=self.password)
        logging.info('Login NAS via FTP.')

    def quit(self):
        if self.ftp:
            self.ftp.quit()
            logging.info('Logout NAS via FTP.')

    def upload(self, local_path: str, remote_path: str):
        self.connect()
        self.ftp.cwd(remote_path)
        filename = os.path.basename(local_path)
        with open(local_path, 'rb') as f:
            self.ftp.storbinary(f'STOR {filename}', f)
            logging.info(f'Uploaded: {local_path} to {remote_path}.')
        self.quit()

    def copy(self, remote_path: str, local_path: str, filename: str):
        self.connect()
        self.ftp.cwd(remote_path)

        local_file_path = os.path.join(local_path, filename)
        with open(local_file_path, 'wb') as f:
            self.ftp.retrbinary(f'RETR {filename}', f.write)
            logging.info(f'Copied: {filename} from {remote_path} to {local_file_path}.')

        self.quit()
