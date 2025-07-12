import json


from enum import Enum
from datetime import datetime
from typing import Dict, Optional, Any


class LogLevel(Enum):
    """Enumération des niveaux de journalisation possibles."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Log:
    """Une classe pour créer et gérer des entrées de journalisation.

    Cette classe permet de créer des journaux avec un niveau de gravité,
    un message, un module source et un contexte optionnel. Les journaux
    incluent automatiquement un horodatage et peuvent être convertis
    en dictionnaire ou en chaîne de caractères.

    Attributes:
        id (Optional[str]): Identifiant unique du journal (optionnel).
        timestamp (str): Horodatage au format ISO 8601.
        level (str): Niveau de gravité du journal (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        message (str): Message descriptif du journal.
        module (str): Nom du module ou composant qui a généré le journal.
        context (Dict[str, Any]): Informations supplémentaires au format dictionnaire.
    """

    def __init__(
        self,
        level: str,
        message: str,
        module: str,
        context: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        id: Optional[str] = None
    ) -> None:
        """Initialise une nouvelle entrée de journal.

        Args:
            level (str): Niveau de journalisation (ex. "INFO", "ERROR").
            message (str): Message descriptif de l'événement.
            module (str): Nom du module source.
            context (Optional[Dict[str, Any]]): Données supplémentaires (par défaut {}).
            timestamp (Optional[datetime]): Horodatage (par défaut maintenant en UTC).
            id (Optional[str]): Identifiant unique (par défaut None).

        Raises:
            ValueError: Si le niveau de journalisation n'est pas valide.
        """
        self.id = id
        self.timestamp = timestamp or datetime.now()
        self.level = self._validate_level(level)
        self.message = message
        self.module = module
        self.context = context or {}

    @staticmethod
    def _validate_level(level: str) -> str:
        """Valide et normalise le niveau de journalisation.

        Args:
            level (str): Niveau de journalisation à valider.

        Returns:
            str: Niveau validé en majuscules.

        Raises:
            ValueError: Si le niveau n'est pas dans LogLevel.
        """
        level = level.upper()
        if level not in LogLevel.__members__:
            raise ValueError(
                f"Niveau de journalisation invalide : {level}. "
                f"Doit être l'un de {', '.join(LogLevel.__members__)}"
            )
        return level

    def to_dict(self) -> Dict[str, Any]:
        """Convertit le journal en dictionnaire.

        Returns:
            Dict[str, Any]: Représentation du journal sous forme de dictionnaire.
        """
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "message": self.message,
            "module": self.module,
            "context": self.context
        }

    def to_json(self) -> str:
        """Convertit le journal en chaîne JSON.

        Returns:
            str: Représentation JSON du journal.
        """
        try:
            return json.dumps(self.to_dict(), ensure_ascii=False)
        except (TypeError, ValueError) as e:
            return json.dumps({
                **self.to_dict(),
                "context": {"error": f"Erreur de sérialisation JSON: {str(e)}"}
            })

    def __str__(self) -> str:
        """Représentation sous forme de chaîne lisible du journal.

        Returns:
            str: Chaîne formatée avec les informations du journal.
        """
        return (
            f"[{self.timestamp.isoformat()}] {self.level} | "
            f"{self.module} | {self.message} | contexte: {self.context}"
        )

    def __repr__(self) -> str:
        """Représentation détaillée du journal pour le débogage.

        Returns:
            str: Chaîne détaillée avec toutes les informations du journal.
        """
        return (
            f"Log(id={self.id}, timestamp={self.timestamp.isoformat()}, "
            f"level={self.level}, message={self.message}, "
            f"module={self.module}, context={self.context})"
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Log':
        """Crée un journal à partir d'un dictionnaire.

        Args:
            data (Dict[str, Any]): Dictionnaire contenant les données du journal.

        Returns:
            Log: Nouvelle instance de Log.
        """
        timestamp = datetime.fromisoformat(data.get("timestamp")) if data.get("timestamp") else None
        return cls(
            level=data.get("level", "INFO"),
            message=data.get("message", ""),
            module=data.get("module", "unknown"),
            context=data.get("context", {}),
            timestamp=timestamp,
            id=data.get("id")
        )
