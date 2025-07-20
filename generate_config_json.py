import json
from config import CONFIG
import os

# Fonction pour convertir Path en chaîne
def path_to_str(obj):
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError("Type non sérialisable")

# Convertir la configuration en dictionnaire
config_dict = {
    "paths": {
        "base_dir": str(CONFIG.paths.base_dir),
        "data_dir": str(CONFIG.paths.data_dir),
        "artifacts_dir": str(CONFIG.paths.artifacts_dir)
    },
    "data": {
        "raw_path": str(CONFIG.data.raw_path),
        "processed_path": str(CONFIG.data.processed_path),
        "required_columns": CONFIG.data.required_columns,
        "label_columns": CONFIG.data.label_columns,
        "min_samples": CONFIG.data.min_samples,
        "augment": CONFIG.data.augment,
        "balance_classes": CONFIG.data.balance_classes
    },
    "processing": {
        "max_words": CONFIG.processing.max_words,
        "max_len": CONFIG.processing.max_len,
        "test_size": CONFIG.processing.test_size,
        "random_state": CONFIG.processing.random_state,
        "stratify": CONFIG.processing.stratify,
        "validate": CONFIG.processing.validate,
        "max_permutations": CONFIG.processing.max_permutations
    },
    "model": {
        "embedding_dim": CONFIG.model.embedding_dim,
        "hidden_units": CONFIG.model.hidden_units,
        "emotion_units": CONFIG.model.emotion_units,
        "activation": CONFIG.model.activation,
        "epochs": CONFIG.model.epochs,
        "batch_size": CONFIG.model.batch_size,
        "dropout_rate": CONFIG.model.dropout_rate,
        "output_paths": {
            key: str(value) for key, value in CONFIG.model.output_paths.items()
        }
    }
}

# Sauvegarder dans un fichier JSON
with open("config.json", "w") as f:
    json.dump(config_dict, f, indent=4)