import os
import json
import unittest

from model.log import Log
from manager.log_manager import LogManager


class TestLogManager(unittest.TestCase):
    """Tests pour la classe LogManager."""

    def setUp(self) -> None:
        """Prépare l'environnement avant chaque test.

        Crée un répertoire temporaire pour les tests et initialise LogManager.
        """
        self.test_dir = "test_logs"
        self.log_manager = LogManager(directory=self.test_dir)
        self.log_file = os.path.join(self.test_dir, "logs.json")

    def tearDown(self) -> None:
        """Nettoie après chaque test.

        Supprime le répertoire de test et le fichier logs.json.
        """
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_init_file(self) -> None:
        """Vérifie que le fichier logs.json est créé correctement."""
        self.assertTrue(os.path.exists(self.log_file), "Le fichier logs.json n'a pas été créé")
        with open(self.log_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, [], "Le fichier JSON initial n'est pas une liste vide")

    def test_create_log(self) -> None:
        """Vérifie l'ajout d'un journal dans le fichier JSON."""
        log = Log(level="INFO", message="Test message", module="test_module", context={"user": "alice"})
        self.log_manager.create_log(log)

        with open(self.log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)

        self.assertEqual(len(logs), 1, "Le journal n'a pas été ajouté")
        self.assertEqual(logs[0]["level"], "INFO", "Le niveau du journal est incorrect")
        self.assertEqual(logs[0]["message"], "Test message", "Le message du journal est incorrect")
        self.assertEqual(logs[0]["module"], "test_module", "Le module du journal est incorrect")
        self.assertEqual(logs[0]["context"], {"user": "alice"}, "Le contexte du journal est incorrect")
        self.assertEqual(logs[0]["id"], "1", "L'ID du journal est incorrect")

    def test_read_logs(self) -> None:
        """Vérifie la lecture de tous les journaux."""
        log1 = Log(level="INFO", message="Premier test", module="test_module")
        log2 = Log(level="ERROR", message="Deuxième test", module="test_module")
        self.log_manager.create_log(log1)
        self.log_manager.create_log(log2)

        logs = self.log_manager.read_logs()
        self.assertEqual(len(logs), 2, "Le nombre de journaux lus est incorrect")
        self.assertEqual(logs[0].message, "Deuxième test", "Les journaux ne sont pas triés par date")
        self.assertEqual(logs[1].message, "Premier test", "Les journaux ne sont pas triés par date")

    def test_read_logs_with_filter(self) -> None:
        """Vérifie la lecture des journaux filtrés par niveau."""
        log1 = Log(level="INFO", message="Test info", module="test_module")
        log2 = Log(level="ERROR", message="Test erreur", module="test_module")
        self.log_manager.create_log(log1)
        self.log_manager.create_log(log2)

        logs = self.log_manager.read_logs(filter_level="INFO")
        self.assertEqual(len(logs), 1, "Le filtrage par niveau n'a pas fonctionné")
        self.assertEqual(logs[0].level, "INFO", "Le niveau filtré est incorrect")

    def test_update_log(self) -> None:
        """Vérifie la mise à jour d'un journal."""
        log = Log(level="INFO", message="Message initial", module="test_module", context={"key": "value"})
        self.log_manager.create_log(log)

        result = self.log_manager.update_log(log_id="1", new_message="Message modifié",
                                             new_context={"new_key": "new_value"})
        self.assertTrue(result, "La mise à jour a échoué")

        logs = self.log_manager.read_logs()
        self.assertEqual(logs[0].message, "Message modifié", "Le message n'a pas été mis à jour")
        self.assertEqual(logs[0].context, {"new_key": "new_value"}, "Le contexte n'a pas été mis à jour")

    def test_update_log_non_existent(self) -> None:
        """Vérifie la mise à jour d'un journal inexistant."""
        result = self.log_manager.update_log(log_id="999", new_message="Message")
        self.assertFalse(result, "La mise à jour d'un journal inexistant devrait échouer")


    def test_delete_log(self) -> None:
        """Vérifie la suppression d'un journal."""
        log = Log(level="INFO", message="À supprimer", module="test_module")
        self.log_manager.create_log(log)

        result = self.log_manager.delete_log(log_id="1")
        self.assertTrue(result, "La suppression a échoué")

        logs = self.log_manager.read_logs()
        self.assertEqual(len(logs), 0, "Le journal n'a pas été supprimé")


    def test_delete_log_non_existent(self) -> None:
        """Vérifie la suppression d'un journal inexistant."""
        result = self.log_manager.delete_log(log_id="999")
        self.assertFalse(result, "La suppression d'un journal inexistant devrait échouer")


    def test_corrupted_json(self) -> None:
        """Vérifie la gestion d'un fichier JSON corrompu."""
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("contenu non JSON")

        logs = self.log_manager.read_logs()
        self.assertEqual(logs, [], "La lecture d'un fichier JSON corrompu devrait retourner une liste vide")


    def test_directory_creation(self) -> None:
        """Vérifie la création automatique du répertoire."""
        self.tearDown()  # Supprimer le répertoire existant
        LogManager(directory=self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir), "Le répertoire n'a pas été créé")
        self.assertTrue(os.path.exists(self.log_file), "Le fichier logs.json n'a pas été créé")


if __name__ == "__main__":
    unittest.main()