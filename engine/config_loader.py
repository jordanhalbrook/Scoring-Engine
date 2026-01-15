import yaml
from services.http import HTTPService
from services.smtp import SMTPService

SERVICE_TYPES = {
    "http": HTTPService,
    "smtp": SMTPService,
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
