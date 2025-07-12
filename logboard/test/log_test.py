import json
import unittest

from datetime import datetime
from model.log import Log, LogLevel

class TestLog(unittest.TestCase):
    """Tests pour la classe Log."""

    def test_create_log(self):
        """Vérifie qu'un journal est créé correctement."""
        log = Log(level="INFO", message="Tout va bien", module="test_module", context={"user": "alice"})
        self.assertEqual(log.level, "INFO")
        self.assertEqual(log.message, "Tout va bien")
        self.assertEqual(log.module, "test_module")
        self.assertEqual(log.context, {"user": "alice"})
        self.assertIsNotNone(log.timestamp)

    def test_invalid_level(self):
        """Vérifie qu'un niveau invalide lève une erreur."""
        with self.assertRaises(ValueError):
            Log(level="BLAH", message="Erreur", module="test_module")

    def test_valid_level(self):
        """Vérifie que tous les niveaux valides sont acceptés."""
        for level in LogLevel:
            log = Log(level=level.value, message="Test", module="test_module")
            self.assertEqual(log.level, level.value)

    def test_to_dict(self):
        """Vérifie la conversion en dictionnaire."""
        log = Log(level="INFO", message="Test", module="test_module", context={"key": "value"})
        result = log.to_dict()
        expected = {
            "id": None,
            "timestamp": log.timestamp.isoformat(),
            "level": "INFO",
            "message": "Test",
            "module": "test_module",
            "context": {"key": "value"}
        }
        self.assertEqual(result, expected)

    def test_to_json(self):
        """Vérifie la conversion en JSON."""
        log = Log(level="INFO", message="Test", module="test_module", context={"key": "value"})
        json_str = log.to_json()
        self.assertTrue(isinstance(json_str, str))
        import json
        parsed = json.loads(json_str)
        self.assertEqual(parsed["level"], "INFO")
        self.assertEqual(parsed["message"], "Test")

    def test_to_json_with_unserializable_context(self):
        """Vérifie la gestion d'un contexte non sérialisable."""
        class NonSerializable:
            pass
        log = Log(level="INFO", message="Test", module="test_module", context={"obj": NonSerializable()})
        json_str = log.to_json()
        parsed = json.loads(json_str)
        self.assertIn("error", parsed["context"])
        self.assertTrue("Erreur de sérialisation JSON" in parsed["context"]["error"])

    def test_str_representation(self):
        """Vérifie la représentation en texte."""
        log = Log(level="INFO", message="Test", module="test_module", context={"key": "value"})
        str_rep = str(log)
        self.assertIn("INFO", str_rep)
        self.assertIn("Test", str_rep)
        self.assertIn("test_module", str_rep)
        self.assertIn("'key': 'value'", str_rep)

    def test_from_dict(self):
        """Vérifie la création d'un journal à partir d'un dictionnaire."""
        data = {
            "id": "123",
            "timestamp": "2025-07-12T16:24:00",
            "level": "WARNING",
            "message": "Attention",
            "module": "test_module",
            "context": {"error_code": 42}
        }
        log = Log.from_dict(data)
        self.assertEqual(log.id, "123")
        self.assertEqual(log.level, "WARNING")
        self.assertEqual(log.message, "Attention")
        self.assertEqual(log.module, "test_module")
        self.assertEqual(log.context, {"error_code": 42})
        self.assertEqual(log.timestamp.isoformat(), "2025-07-12T16:24:00")

if __name__ == "__main__":
    unittest.main()