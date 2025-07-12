import json
import pandas as pd
from pathlib import Path

#TODO Inclure le log vers mon logger

def load_text_data(file_path, encoding='utf-8', txt_column_name="text"):
    """
        Charge les données textuelles dans un DataFrame pandas à partir de différents formats portables.

        Formats pris en charge : .csv, .tsv, .json, .jsonl, .txt, .parquet, .pkl

        Paramètres :
            file_path (str ou Path) : Chemin vers le fichier
            encoding (str) : Encodage du fichier, par défaut 'utf-8'
            txt_column_name (str) : Nom de la colonne à utiliser pour les fichiers .txt simples

        Retourne :
            pd.DataFrame : Données textuelles chargées
    """

    file_path = Path(file_path)
    ext = file_path.suffix.lower()

    try:
        if ext == ".csv":
            return pd.read_csv(file_path, encoding=encoding)

        elif ext == ".tsv":
            return pd.read_csv(file_path, delimiter='\t', encoding=encoding)

        elif ext == ".jsonl":
            # Line-delimited JSON (JSONL)
            with open(file_path, 'r', encoding=encoding) as f:
                lines = [json.loads(line.strip()) for line in f if line.strip()]
            return pd.DataFrame(lines)

        elif ext == ".json":
            with open(file_path, 'r', encoding=encoding) as f:
                data = json.load(f)
                if isinstance(data, list):
                    return pd.DataFrame(data)
                elif isinstance(data, dict):
                    return pd.DataFrame.from_dict(data)
                else:
                    raise ValueError("Unsupported JSON structure")

        elif ext == ".txt":
            with open(file_path, 'r', encoding=encoding) as f:
                lines = [line.strip() for line in f if line.strip()]
            return pd.DataFrame({txt_column_name: lines})

        elif ext == ".parquet":
            return pd.read_parquet(file_path)

        elif ext == ".pkl":
            return pd.read_pickle(file_path)

        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    except Exception as e:
        raise RuntimeError(f"Failed to load file {file_path}: {e}")
