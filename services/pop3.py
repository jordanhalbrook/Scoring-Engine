import poplib
from datetime import datetime
from .base import ServiceCheck, ServiceResult

class POP3Service(ServiceCheck):
    def __init__(self, name, server, port, username, password, points):
        super().__init__(name, points)
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def run_check(self):
        try:
            pop = poplib.POP3(self.server, self.port, timeout=10)
            pop.user(self.username)
            pop.pass_(self.password)
            pop.stat()
            pop.quit()

            return ServiceResult(
                self.name, True, "POP3 functional", datetime.utcnow()
            )

        except Exception as e:
            return ServiceResult(
                self.name, False, str(e), datetime.utcnow()
            )
