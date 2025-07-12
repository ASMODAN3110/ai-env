import pandas as pd
import re
import json
from pathlib import Path

def load_text_data(file_path):
    """Charge les données textuelles depuis différents formats."""
    try:
        file_ext = Path(file_path).suffix.lower()
        if file_ext == '.csv':
            return pd.read_csv(file_path)
        elif file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return pd.DataFrame({'text': f.readlines()})
        elif file_ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return pd.DataFrame(data)
        else:
            raise ValueError(f"Format de fichier non pris en charge : {file_ext}")
    except Exception as e:
        print(f"Erreur lors du chargement du fichier {file_path} : {e}")
        return None

def clean_text(text):
    """Nettoie une chaîne de texte."""
    if not isinstance(text, str):
        return text
    # Convertir en minuscules
    text = text.lower()
    # Supprimer les caractères spéciaux et les chiffres
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Supprimer les espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_text_data(df, text_column='text'):
    """Nettoie les données textuelles dans un DataFrame."""
    if df is None:
        return None
    # Gérer les valeurs manquantes
    df[text_column] = df[text_column].fillna('')
    # Appliquer le nettoyage
    df[text_column] = df[text_column].apply(clean_text)
    # Supprimer les lignes vides après nettoyage
    df = df[df[text_column] != '']
    return df

def save_cleaned_text_data(df, output_path):
    """Sauvegarde les données nettoyées."""
    try:
        output_ext = Path(output_path).suffix.lower()
        if output_ext == '.csv':
            df.to_csv(output_path, index=False)
        elif output_ext == '.json':
            df.to_json(output_path, orient='records', lines=True)
        else:
            raise ValueError(f"Format de sortie non pris en charge : {output_ext}")
        print(f"Données nettoyées sauvegardées dans {output_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

def main_text_cleaning(input_path, output_path, text_column='text'):
    """Pipeline principal pour le nettoyage des données textuelles."""
    df = load_text_data(input_path)
    if df is not None:
        cleaned_df = clean_text_data(df, text_column)
        if cleaned_df is not None:
            save_cleaned_text_data(cleaned_df, output_path)

if __name__ == "__main__":
    #input_file = r"..\..\test\cleaner\text\test_data.json"  # Chemin du fichier de test
    #input_file = r"..\..\test\cleaner\text\test_data.csv"  # Chemin du fichier de test
    input_file = r"..\..\test\cleaner\text\test_data.txt"  # Chemin du fichier de test
    output_file = "cleaned_test_data.csv"  # Chemin du fichier de sortie
    main_text_cleaning(input_file, output_file)