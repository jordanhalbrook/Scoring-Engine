import yaml
from services.http import HTTPService
from services.smtp import SMTPService
from services.pop3 import POP3Service
from services.dns import DNSService
from services.ftp import FTPService

SERVICE_TYPES = {
    "http": HTTPService,
    "smtp": SMTPService,
    "pop3": POP3Service,
    "dns": DNSService,
    "ftp": FTPService,
}

def load_services(config_file):
    with open(config_file) as f:
        config = yaml.safe_load(f)

    services = []

    for svc in config["services"]:
        svc_type = svc.pop("type")
        service_class = SERVICE_TYPES[svc_type]
        services.append(service_class(**svc))

    return services
