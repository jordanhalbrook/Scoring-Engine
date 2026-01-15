from ftplib import FTP
from datetime import datetime
from .base import ServiceCheck, ServiceResult
import io

class FTPService(ServiceCheck):
    def __init__(self, name, server, username, password, points, port=21, test_file=None):
        super().__init__(name, points)
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.test_file = test_file

    def run_check(self):
        try:
            ftp = FTP()
            ftp.connect(self.server, self.port, timeout=10)
            ftp.login(self.username, self.password)

            files = ftp.nlst()

            if self.test_file:
                if self.test_file not in files:
                    return ServiceResult(
                        self.name,
                        False,
                        "Test file not found",
                        datetime.utcnow(),
                        evidence=str(files)
                    )

                buffer = io.BytesIO()
                ftp.retrbinary(f"RETR {self.test_file}", buffer.write)

            ftp.quit()

            return ServiceResult(
                self.name,
                True,
                "FTP functional",
                datetime.utcnow()
            )

        except Exception as e:
            return ServiceResult(
                self.name,
                False,
                str(e),
                datetime.utcnow()
            )
