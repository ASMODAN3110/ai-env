import os
import json

from model.log import Log
from typing import List, Optional, Dict, Any


class LogManager:
    """Gère les journaux dans un fichier JSON.

    Cette classe permet de sauvegarder, lire, modifier et supprimer des journaux
    dans un fichier JSON. Le répertoire du fichier peut être spécifié à l'initialisation.

    Attributes:
        log_file (str): Chemin complet vers le fichier JSON des journaux.
    """

    def __init__(self, directory: str = ".") -> None:
        """Initialise le gestionnaire de journaux.

        Args:
            directory (str): Répertoire où sauvegarder le fichier logs.json.
                           Par défaut, utilise le répertoire courant.

        Raises:
            OSError: Si le répertoire n'est pas accessible ou non valide.
        """
        # Vérifier si le répertoire existe, sinon le créer
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Définir le chemin du fichier logs.json
        self.log_file = os.path.join(directory, "logs.json")
        # S'assurer que le fichier JSON existe
        self._init_file()

    def _init_file(self) -> None:
        """Crée le fichier JSON s'il n'existe pas.

        Si le fichier logs.json n'existe pas, crée un fichier vide avec une liste vide.
        """
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False)

    def create_log(self, log: Log) -> None:
        """Ajoute un nouveau journal au fichier JSON.

        Args:
            log (Log): Objet Log à sauvegarder.

        Raises:
            IOError: Si l'écriture dans le fichier échoue.
        """
        # Lire les journaux existants
        with open(self.log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)

        # Générer un ID si aucun n'est fourni
        if log.id is None:
            log.id = str(len(logs) + 1)  # ID simple basé sur le nombre de journaux
        # Ajouter le nouveau journal
        logs.append(log.to_dict())

        # Sauvegarder dans le fichier
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

    def read_logs(self, filter_level: Optional[str] = None) -> List[Log]:
        """Lit les journaux depuis le fichier JSON.

        Args:
            filter_level (Optional[str]): Filtre les journaux par niveau (ex. "INFO").
                                        Si None, retourne tous les journaux.

        Returns:
            List[Log]: Liste des objets Log triés par horodatage (plus récent d'abord).

        Raises:
            IOError: Si la lecture du fichier échoue.
            json.JSONDecodeError: Si le fichier JSON est corrompu.
        """
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                logs_data = json.load(f)
        except json.JSONDecodeError:
            return []  # Retourner une liste vide si le fichier est corrompu

        # Convertir chaque dictionnaire en objet Log
        logs = [Log.from_dict(data) for data in logs_data]

        # Filtrer par niveau si spécifié
        if filter_level:
            filter_level = filter_level.upper()
            logs = [log for log in logs if log.level == filter_level]

        # Trier par horodatage (plus récent d'abord)
        return sorted(logs, key=lambda x: x.timestamp, reverse=True)

    def update_log(self, log_id: str, new_message: Optional[str] = None,
                   new_context: Optional[Dict[str, Any]] = None) -> bool:
        """Met à jour un journal existant.

        Args:
            log_id (str): ID du journal à modifier.
            new_message (Optional[str]): Nouveau message (si spécifié).
            new_context (Optional[Dict[str, Any]]): Nouveau contexte (si spécifié).

        Returns:
            bool: True si la mise à jour a réussi, False si le journal n'existe pas.

        Raises:
            IOError: Si l'écriture dans le fichier échoue.
        """
        with open(self.log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)

        # Chercher le journal avec l'ID donné
        for log_data in logs:
            if log_data["id"] == log_id:
                if new_message:
                    log_data["message"] = new_message
                if new_context:
                    log_data["context"] = new_context
                # Sauvegarder les modifications
                with open(self.log_file, "w", encoding="utf-8") as f:
                    json.dump(logs, f, ensure_ascii=False, indent=2)
                return True
        return False

    def delete_log(self, log_id: str) -> bool:
        """Supprime un journal du fichier JSON.

        Args:
            log_id (str): ID du journal à supprimer.

        Returns:
            bool: True si la suppression a réussi, False si le journal n'existe pas.

        Raises:
            IOError: Si l'écriture dans le fichier échoue.
        """
        with open(self.log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)

        # Filtrer le journal avec l'ID donné
        initial_length = len(logs)
        logs = [log for log in logs if log["id"] != log_id]

        # Si un journal a été supprimé, sauvegarder
        if len(logs) < initial_length:
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
            return True
        return False