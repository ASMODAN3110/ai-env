from model.log import Log
from datetime import datetime
from manager.log_manager import LogManager

def add_sample_logs(directory: str = "logs") -> None:
    """Ajoute 20 exemples de journaux au fichier logs.json.

    Args:
        directory (str): Répertoire où se trouve le fichier logs.json.
                       Par défaut, utilise le dossier 'logs'.

    Returns:
        None: Les journaux sont ajoutés au fichier logs.json.
    """
    # Initialiser le gestionnaire de journaux
    log_manager = LogManager(directory=directory)

    # Liste des exemples de journaux
    sample_logs = [
        Log(
            level="INFO",
            message="Connexion réussie",
            module="auth",
            context={"user_id": "user123", "ip": "192.168.1.10"},
            timestamp=datetime(2025, 7, 10, 8, 0, 0)
        ),
        Log(
            level="DEBUG",
            message="Requête SQL exécutée",
            module="database",
            context={"query": "SELECT * FROM users", "duration_ms": 25},
            timestamp=datetime(2025, 7, 10, 8, 5, 0)
        ),
        Log(
            level="WARNING",
            message="Tentative de connexion échouée",
            module="auth",
            context={"user_id": "user456", "attempts": 3},
            timestamp=datetime(2025, 7, 10, 8, 10, 0)
        ),
        Log(
            level="ERROR",
            message="Erreur de connexion à la base de données",
            module="database",
            context={"error_code": 1005, "db_name": "main_db"},
            timestamp=datetime(2025, 7, 10, 9, 0, 0)
        ),
        Log(
            level="CRITICAL",
            message="Serveur en panne",
            module="server",
            context={"server_id": "srv01", "downtime_s": 120},
            timestamp=datetime(2025, 7, 10, 9, 30, 0)
        ),
        Log(
            level="INFO",
            message="Mise à jour des paramètres utilisateur",
            module="profile",
            context={"user_id": "user789", "field": "email"},
            timestamp=datetime(2025, 7, 10, 10, 0, 0)
        ),
        Log(
            level="DEBUG",
            message="Cache mis à jour",
            module="cache",
            context={"cache_key": "user_data_123", "size_bytes": 2048},
            timestamp=datetime(2025, 7, 10, 10, 15, 0)
        ),
        Log(
            level="WARNING",
            message="Utilisation élevée de la mémoire",
            module="system",
            context={"memory_percent": 85.5},
            timestamp=datetime(2025, 7, 10, 11, 0, 0)
        ),
        Log(
            level="INFO",
            message="Requête API réussie",
            module="api",
            context={"endpoint": "/users", "response_time_ms": 150},
            timestamp=datetime(2025, 7, 10, 12, 0, 0)
        ),
        Log(
            level="ERROR",
            message="Échec de l'envoi d'email",
            module="mailer",
            context={"recipient": "user@example.com", "error": "SMTP timeout"},
            timestamp=datetime(2025, 7, 10, 13, 0, 0)
        ),
        Log(
            level="DEBUG",
            message="Session utilisateur créée",
            module="auth",
            context={"session_id": "sess_987", "user_id": "user123"},
            timestamp=datetime(2025, 7, 11, 8, 0, 0)
        ),
        Log(
            level="INFO",
            message="Nouveau fichier chargé",
            module="upload",
            context={"file_name": "document.pdf", "size_mb": 1.5},
            timestamp=datetime(2025, 7, 11, 9, 0, 0)
        ),
        Log(
            level="WARNING",
            message="Délai de réponse API élevé",
            module="api",
            context={"endpoint": "/reports", "response_time_ms": 2000},
            timestamp=datetime(2025, 7, 11, 10, 0, 0)
        ),
        Log(
            level="ERROR",
            message="Erreur de validation des données",
            module="form",
            context={"field": "phone", "value": "invalid"},
            timestamp=datetime(2025, 7, 11, 11, 0, 0)
        ),
        Log(
            level="CRITICAL",
            message="Fuite de mémoire détectée",
            module="system",
            context={"process_id": 1234, "memory_leak_mb": 50},
            timestamp=datetime(2025, 7, 11, 12, 0, 0)
        ),
        Log(
            level="INFO",
            message="Utilisateur déconnecté",
            module="auth",
            context={"user_id": "user456", "session_id": "sess_456"},
            timestamp=datetime(2025, 7, 11, 13, 0, 0)
        ),
        Log(
            level="DEBUG",
            message="Requête HTTP reçue",
            module="api",
            context={"method": "GET", "url": "/status"},
            timestamp=datetime(2025, 7, 12, 8, 0, 0)
        ),
        Log(
            level="WARNING",
            message="Disque presque plein",
            module="system",
            context={"disk_usage_percent": 95.0, "path": "/"},
            timestamp=datetime(2025, 7, 12, 9, 0, 0)
        ),
        Log(
            level="INFO",
            message="Tâche planifiée terminée",
            module="scheduler",
            context={"task_id": "task_001", "duration_s": 300},
            timestamp=datetime(2025, 7, 12, 10, 0, 0)
        ),
        Log(
            level="ERROR",
            message="Échec de la sauvegarde",
            module="backup",
            context={"backup_path": "/backup", "error": "Permission denied"},
            timestamp=datetime(2025, 7, 12, 11, 0, 0)
        )
    ]

    # Ajouter chaque journal au fichier logs.json
    for log in sample_logs:
        log_manager.create_log(log)

    print(f"20 journaux ajoutés à {log_manager.log_file}")

if __name__ == "__main__":
    add_sample_logs()
