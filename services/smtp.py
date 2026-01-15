import smtplib
from datetime import datetime
from .base import ServiceCheck, ServiceResult

class SMTPService(ServiceCheck):
    def __init__(self, name, server, port, username, password, points):
        super().__init__(name, points)
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def run_check(self):
        try:
            with smtplib.SMTP(self.server, self.port, timeout=10) as smtp:
                smtp.starttls()
                smtp.login(self.username, self.password)
                smtp.noop()

            return ServiceResult(
                    self.name, True, "SMTP functional",
                    datetime.utcnow()
            )

        except Exception as e:
            return ServiceResult(
                    self.name, False, str(e),
                    datetime.utcnow()
            )
