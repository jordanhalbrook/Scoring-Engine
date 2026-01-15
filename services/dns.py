import dns.resolver
from datetime import datetime
from .base import ServiceCheck, ServiceResult

class DNSService(ServiceCheck):
    def __init__(self, name, server, records, points):
        super().__init__(name, points)
        self.server = server
        self.records = records

    def run_check(self):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [self.server]

        try:
            for record in self.records:
                if "expected" not in record:
                    return ServiceResult(
                        self.name,
                        False,
                        f"Missing 'expected' field in DNS record for {record.get('name', 'unknown')}",
                        datetime.utcnow()
                    )
                
                answers = resolver.resolve(
                    record["name"],
                    record["type"]
                )

                values = [rdata.to_text() for rdata in answers]

                if record["expected"] not in values:
                    return ServiceResult(
                        self.name,
                        False,
                        f"DNS mismatch for {record['name']}",
                        datetime.utcnow(),
                        evidence=str(values)
                    )
            return ServiceResult(
                self.name,
                True,
                "All DNS records resolved correctly",
                datetime.utcnow()
            )

        except Exception as e:
            return ServiceResult(
                self.name,
                False,
                str(e),
                datetime.utcnow()
            )
