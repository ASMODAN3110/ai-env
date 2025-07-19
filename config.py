from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass, field

BASE_DIR = Path(__file__).resolve().parent

@dataclass
class Paths:
    """
    Stores file path configurations for the project.

    Attributes:
        base_dir (Path): Root directory of the project.
        data_dir (Path): Directory for storing datasets.
        artifacts_dir (Path): Directory for saving model artifacts.
    """
    base_dir: Path = BASE_DIR
    data_dir: Path = BASE_DIR / "data"
    artifacts_dir: Path = BASE_DIR / "artifacts"

@dataclass
class DataConfig:
    """
    General configuration for handling datasets.

    Attributes:
        raw_path (Path): Path to the raw dataset file.
        processed_path (Path): Path to the processed dataset file.
        required_columns (List[str]): List of columns required in the dataset.
        label_columns (List[str]): List of columns to be used as labels.
        min_samples (int): Minimum number of samples required for processing.
        augment (bool): Whether to augment the dataset (e.g., data augmentation for images or text).
        balance_classes (bool): Whether to balance classes in the dataset (e.g., for imbalanced datasets).
    """
    raw_path: Path = BASE_DIR / "data/raw/data.csv"
    processed_path: Path = BASE_DIR / "data/processed/data.csv"
    required_columns: List[str] = field(default_factory=list)
    label_columns: List[str] = field(default_factory=list)
    min_samples: int = 1
    augment: bool = False
    balance_classes: bool = False

@dataclass
class ProcessingConfig:
    """
    Configuration for data preprocessing.

    Attributes:
        max_words (int): Maximum number of words to use in text processing.
        max_len (int): Maximum length of sequences (e.g., for padding/truncation).
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.
        stratify (bool): Whether to stratify the train-test split based on labels.
        validate (bool): Whether to validate the dataset after preprocessing.
        max_permutations (int): Maximum number of permutations for data augmentation.
    """
    max_words: int = 1000
    max_len: int = 20
    test_size: float = 0.2
    random_state: int = 42
    stratify: bool = True
    validate: bool = True
    max_permutations: int = 1

@dataclass
class ModelConfig:
    """
    General settings for training and model structure.

    Attributes:
        embedding_dim (int): Dimension of embedding layers.
        hidden_units (int): Number of hidden units in the model.
        activation (str): Activation function to use (e.g., "relu").
        epochs (int): Number of training epochs.
        batch_size (int): Batch size for training.
        dropout_rate (float): Dropout rate for regularization.
        output_paths (Dict[str, Path]): Dictionary of paths for saving model artifacts.
    """
    embedding_dim: int = 16
    hidden_units: int = 128
    emotion_units: any = None
    activation: str = "relu"
    epochs: int = 50
    batch_size: int = 16
    dropout_rate: float = 0.3
    output_paths: Dict[str, Path] = field(default_factory=lambda: {
        "tokenizer": BASE_DIR / "artifacts/tokenizer.pkl",
        "encoder": BASE_DIR / "artifacts/encoder.pkl",
        "model": BASE_DIR / "artifacts/model.keras",
        "tflite": BASE_DIR / "artifacts/model.tflite"
    })

@dataclass
class GeneralConfig:
    """
    The main configuration object, combining all sub-configurations.

    Attributes:
        paths (Paths): Path configurations.
        data (DataConfig): Data handling configurations.
        processing (ProcessingConfig): Data preprocessing configurations.
        model (ModelConfig): Model training configurations.
    """
    paths: Paths = field(default_factory=Paths)
    data: DataConfig = field(default_factory=DataConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    model: ModelConfig = field(default_factory=ModelConfig)

CONFIG = GeneralConfig()

# Example usage:
# print(CONFIG.data.raw_path)
# print(CONFIG.model.epochs)
