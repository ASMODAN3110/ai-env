import json
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass, field, asdict

# ===================================================
# CONFIGURATION PRINCIPALE DU SYSTÈME D'IA
# Supporte l'ENTRAÎNEMENT de modèles TEXTE ou IMAGE.
# Tous les paramètres sont documentés et préremplis.
# ===================================================


@dataclass
class Paths:
    """
    Spécifie tous les chemins nécessaires pour organiser les données
    et les artefacts du projet.

    base_dir: Dossier racine du projet.
    data_dir: Dossier contenant les données brutes et traitées.
    artifacts_dir: Dossier où seront stockés les modèles, tokenizers, logs, etc.
    """
    base_dir: Path = Path(".").resolve()
    data_dir: Path = base_dir / "data"
    artifacts_dir: Path = base_dir / "artifacts"


@dataclass
class TextDataConfig:
    """
    Paramètres spécifiques aux données TEXTUELLES.

    raw_path: Fichier CSV contenant les données textuelles brutes.
    processed_path: Fichier CSV résultant après nettoyage et traitement.
    required_columns: Colonnes nécessaires (ex: ['text', 'label']).
    label_columns: Colonnes à utiliser comme cibles lors de l'entraînement.
    """
    raw_path: Path = Paths().data_dir / "raw/text_data.csv"
    processed_path: Path = Paths().data_dir / "processed/text_data.csv"
    required_columns: List[str] = field(default_factory=lambda: ["text"])
    label_columns: List[str] = field(default_factory=lambda: ["label"])


@dataclass
class ImageDataConfig:
    """
    Paramètres spécifiques aux données IMAGES.

    image_dir: Dossier contenant toutes les images.
    labels_file: Fichier CSV ou JSON avec les annotations/catégories des images.
    image_format: Format attendu des images ('jpg', 'png', etc.).
    resize_to: Taille standard des images après redimensionnement (largeur, hauteur).
    color_mode: Mode couleur ('rgb' pour couleur, 'grayscale' pour noir et blanc).
    """
    image_dir: Path = Paths().data_dir / "images"
    labels_file: Path = Paths().data_dir / "labels.csv"
    image_format: str = "jpg"
    resize_to: Tuple[int, int] = (224, 224)
    color_mode: str = "rgb"  # Options: 'rgb' ou 'grayscale'


@dataclass
class DataConfig:
    """
    Configuration générale pour la gestion des données.

    task_type: Type de tâche à réaliser (ex: "text_classification", "image_classification").
    text_data: Rempli uniquement pour les tâches textuelles.
    image_data: Rempli uniquement pour les tâches images.
    min_samples: Nombre minimum d'exemples nécessaires pour valider le dataset.
    augment: Appliquer des techniques d'augmentation pour enrichir les données (rotation, bruit, etc.).
    balance_classes: Rééquilibrer les classes pour traiter les datasets déséquilibrés.
    """
    task_type: str = "text_classification"  # Ou "image_classification"
    text_data: Optional[TextDataConfig] = field(default_factory=TextDataConfig)
    image_data: Optional[ImageDataConfig] = field(default_factory=ImageDataConfig)
    min_samples: int = 100
    augment: bool = False
    balance_classes: bool = False


@dataclass
class ProcessingConfig:
    """
    Paramètres de PRÉTRAITEMENT et SPLIT des données.

    test_size: Pourcentage des données réservé au TEST (0.2 = 20%).
    random_state: Graine aléatoire pour reproductibilité du split.
    stratify: Garantir une répartition équilibrée des classes dans le split.
    max_words: (TEXTE) Nombre maximal de mots autorisés dans le vocabulaire.
    max_len: (TEXTE) Longueur maximale des séquences (textes coupés au-delà).
    normalize: (IMAGE) Appliquer normalisation [0, 1] ou [-1, 1] aux images.
    """
    test_size: float = 0.2
    random_state: int = 42
    stratify: bool = True

    # Texte uniquement
    max_words: int = 5000
    max_len: int = 100

    # Image uniquement
    normalize: bool = True


@dataclass
class CNNConfig:
    """
    Configuration détaillée du modèle CNN (Convolutional Neural Network).

    filters: Nombre de filtres appliqués dans les couches convolutionnelles.
    kernel_size: Taille du noyau des filtres (ex: 3 = 3x3).
    activation: Fonction d'activation entre les couches ('relu', 'tanh', etc.).
    pooling: Appliquer un sous-échantillonnage via pooling ('max', 'average').
    """
    filters: int = 32
    kernel_size: int = 3
    activation: str = "relu"
    pooling: str = "max"


@dataclass
class LSTMConfig:
    """
    Paramètres spécifiques aux modèles LSTM (Long Short-Term Memory).

    embedding_dim: Dimension des vecteurs d'embedding du texte.
    hidden_units: Nombre d'unités cachées dans la couche LSTM.
    activation: Fonction d'activation de sortie.
    bidirectional: Ajouter un flux inversé (utile en NLP).
    """
    embedding_dim: int = 64
    hidden_units: int = 128
    activation: str = "tanh"
    bidirectional: bool = False


@dataclass
class ModelConfig:
    """
    Paramètres globaux pour l'architecture et l'entraînement du modèle.

    architecture: Nom du modèle utilisé ('cnn', 'lstm', 'transformer', etc.).
    cnn: Paramètres spécifiques au CNN (si utilisé).
    lstm: Paramètres spécifiques au LSTM (si utilisé).
    epochs: Nombre total de passages sur le dataset complet.
    batch_size: Nombre d'échantillons utilisés par étape d'entraînement.
    dropout_rate: Proportion d'unités désactivées pour réduire l'overfitting.
    model_path: Chemin de sauvegarde du modèle entraîné.
    tokenizer_path: Chemin de sauvegarde du tokenizer (TEXTE uniquement).
    encoder_path: Chemin de sauvegarde de l'encodeur (optionnel).
    tflite_path: Chemin optionnel pour exporter le modèle en format TFLite.
    """
    architecture: str = "lstm"  # Valeurs possibles: 'cnn', 'lstm', 'transformer'

    # Sub-configs (Must use default_factory)
    cnn: CNNConfig = field(default_factory=CNNConfig)
    lstm: LSTMConfig = field(default_factory=LSTMConfig)

    epochs: int = 10
    batch_size: int = 32
    dropout_rate: float = 0.3

    model_path: Path = Paths().artifacts_dir / "model.pth"
    tokenizer_path: Path = Paths().artifacts_dir / "tokenizer.pkl"
    encoder_path: Path = Paths().artifacts_dir / "encoder.pkl"
    tflite_path: Path = Paths().artifacts_dir / "model.tflite"


@dataclass
class AIProjectConfig:
    """
    Configuration MAÎTRE pour l'ensemble du projet IA.
    """

    paths: Paths = field(default_factory=Paths)
    data: DataConfig = field(default_factory=DataConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    model: ModelConfig = field(default_factory=ModelConfig)

    @staticmethod
    def from_json(json_path: Path) -> 'AIProjectConfig':
        """
        Charger toute la configuration depuis un fichier JSON.
        Chaque sous-classe est reconstruite proprement.
        """
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return AIProjectConfig(
            paths=Paths(**data['paths']),
            data=DataConfig(
                task_type=data['data']['task_type'],
                text_data=TextDataConfig(**data['data']['text_data'])
                if data['data'].get('text_data') else None,
                image_data=ImageDataConfig(**data['data']['image_data'])
                if data['data'].get('image_data') else None,
                min_samples=data['data'].get('min_samples', 1),
                augment=data['data'].get('augment', False),
                balance_classes=data['data'].get('balance_classes', False)
            ),
            processing=ProcessingConfig(**data['processing']),
            model=ModelConfig(
                architecture=data['model']['architecture'],
                cnn=CNNConfig(**data['model']['cnn']) if data['model'].get('cnn') else CNNConfig(),
                lstm=LSTMConfig(**data['model']['lstm']) if data['model'].get('lstm') else LSTMConfig(),
                epochs=data['model'].get('epochs', 10),
                batch_size=data['model'].get('batch_size', 32),
                dropout_rate=data['model'].get('dropout_rate', 0.3),
                model_path=Path(data['model']['model_path']),
                tokenizer_path=Path(data['model']['tokenizer_path']),
                encoder_path=Path(data['model']['encoder_path']),
                tflite_path=Path(data['model']['tflite_path'])
            )
        )

    def to_json(self, json_path: Path):
        """
        Sauvegarder la configuration dans un fichier JSON.
        Les objets Path sont convertis en chaînes.
        """
        with open(json_path, 'w', encoding='utf-8') as file:
            data_dict = convert_paths(asdict(self))
            json.dump(data_dict, file, indent=4, ensure_ascii=False)



def convert_paths(obj):
    """
    Recursively convert Path objects to strings inside dictionaries/lists.
    """
    if isinstance(obj, Path):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: convert_paths(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_paths(i) for i in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_paths(i) for i in obj)
    else:
        return obj

