import poplib
from datetime import datetime
from .base import ServiceCheck, ServiceResult

class POP3Service(ServiceCheck):
    def __init__(self, name, server, username, password, points):

