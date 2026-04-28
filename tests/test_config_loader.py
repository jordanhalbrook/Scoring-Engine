import os
import tempfile
import unittest
from unittest.mock import patch

import yaml

from engine import config_loader


class FakeService:
    def __init__(self, name, points):
        self.name = name
        self.points = points


class TestLoadServices(unittest.TestCase):
    def write_config(self, data):
        fd, path = tempfile.mkstemp(suffix=".yaml")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as config_file:
            yaml.safe_dump(data, config_file)
        self.addCleanup(lambda: os.path.exists(path) and os.remove(path))
        return path

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            config_loader.load_services("/tmp/does-not-exist.yaml")

    def test_missing_services_key_raises(self):
        config_path = self.write_config({"foo": "bar"})

        with self.assertRaises(ValueError):
            config_loader.load_services(config_path)

    def test_missing_type_raises(self):
        config_path = self.write_config({"services": [{"name": "svc"}]})

        with self.assertRaises(ValueError):
            config_loader.load_services(config_path)

    def test_unknown_type_raises(self):
        config_path = self.write_config(
            {"services": [{"type": "unknown", "name": "svc"}]}
        )

        with self.assertRaises(ValueError):
            config_loader.load_services(config_path)

    def test_successfully_creates_service_instances(self):
        config_path = self.write_config(
            {"services": [{"type": "fake", "name": "my-service", "points": 50}]}
        )

        with patch.object(config_loader, "SERVICE_TYPES", {"fake": FakeService}):
            services = config_loader.load_services(config_path)

        self.assertEqual(len(services), 1)
        self.assertIsInstance(services[0], FakeService)
        self.assertEqual(services[0].name, "my-service")
        self.assertEqual(services[0].points, 50)

    def test_invalid_service_kwargs_raises_value_error(self):
        config_path = self.write_config(
            {"services": [{"type": "fake", "name": "my-service"}]}
        )

        with patch.object(config_loader, "SERVICE_TYPES", {"fake": FakeService}):
            with self.assertRaises(ValueError):
                config_loader.load_services(config_path)


if __name__ == "__main__":
    unittest.main()
