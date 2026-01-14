import requests
from datetime import datetime
from .base import ServiceCheck, ServiceResult

class HTTPService(ServiceCheck):
    def __init__(self, name, url, expected_file, points, verify_ssl=True):
        super().__init__(name, points)
        self.url = url
        self.expected_file = expected_file
        self.verify_ssl = verify_ssl

    def run_check(self):
        try:
            response = request.get(self.url, timeout=5, verify=self.verify_ssl)
            with open(self.expected_file, "r") as f:
                expected = f.read()


            if response.text.strip() == expected.strip():
                return ServiceResult(
                        self.name, True, "Content matched",
                        datetime.utcnow()
                )

            return ServiceResult(
                    self.name, False, "Content mismatch",
                    datetime.utcnow(),
                    evidence=response.text[:500]
            )

        except Exception as e:
            return ServiceResult(
                    self.name, False, str(e),
                    datetime.utcnow()
            )
