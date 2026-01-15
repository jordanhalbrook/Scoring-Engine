"""
Configuration loader for services.

This module loads service configurations from a YAML file and creates
service check objects for the scoring engine.
"""
import yaml
from services.http import HTTPService
from services.smtp import SMTPService
from services.pop3 import POP3Service
from services.dns import DNSService
from services.ftp import FTPService

# Map of service type strings to their corresponding class
SERVICE_TYPES = {
    "http": HTTPService,
    "smtp": SMTPService,
    "pop3": POP3Service,
    "dns": DNSService,
    "ftp": FTPService,
}

def load_services(config_file):
    """
    Load services from a YAML configuration file.
    
    Args:
        config_file: Path to the YAML configuration file
        
    Returns:
        List of service check objects
        
    Raises:
        FileNotFoundError: If the config file doesn't exist
        yaml.YAMLError: If the YAML file is invalid
        KeyError: If required fields are missing
        ValueError: If service type is unknown
    """
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML in {config_file}: {e}")

    if not config or "services" not in config:
        raise ValueError(f"Config file {config_file} must contain a 'services' list")

    services = []

    for idx, svc in enumerate(config["services"]):
        if "type" not in svc:
            raise ValueError(f"Service #{idx+1} in config is missing required 'type' field")
        
        svc_type = svc.pop("type")
        
        if svc_type not in SERVICE_TYPES:
            raise ValueError(
                f"Unknown service type '{svc_type}' for service #{idx+1}. "
                f"Valid types: {list(SERVICE_TYPES.keys())}"
            )
        
        service_class = SERVICE_TYPES[svc_type]
        
        try:
            services.append(service_class(**svc))
        except TypeError as e:
            raise ValueError(
                f"Error creating {svc_type} service #{idx+1}: {e}. "
                f"Check that all required fields are present in the config."
            )

    return services
