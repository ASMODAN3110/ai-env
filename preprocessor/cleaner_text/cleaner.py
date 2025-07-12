import pandas as pd
import re
import html

def clean_text_data(df: pd.DataFrame, text_columns=None, lowercase=True, remove_duplicates=True) -> pd.DataFrame:
    """
    Nettoie un DataFrame en supprimant les valeurs nulles, les caractères étranges et en normalisant le texte.

    Paramètres :
        df (pd.DataFrame) : DataFrame en entrée
        text_columns (list ou None) : Colonnes à nettoyer (toutes les colonnes de type chaîne si None)
        lowercase (bool) : Indique s'il faut convertir le texte en minuscules
        remove_duplicates (bool) : Indique s'il faut supprimer les lignes dupliquées

    Retourne :
        pd.DataFrame : DataFrame nettoyé
    """
    # Auto-detect text columns if not specified
    if text_columns is None:
        text_columns = df.select_dtypes(include='object').columns.tolist()

    # Remove rows with nulls or empty strings in text columns
    for col in text_columns:
        df = df[df[col].notnull()]  # remove NaN
        df = df[df[col].str.strip() != ""]  # remove empty/whitespace only

    def clean_string(s):
        # Decode HTML entities
        s = html.unescape(s)
        # Remove emojis and non-ASCII characters
        s = re.sub(r'[^\x00-\x7F]+', ' ', s)
        # Remove HTML tags
        s = re.sub(r'<[^>]*>', '', s)
        # Remove URLs
        s = re.sub(r'http\S+|www\S+', '', s)
        # Remove special characters (keeping alphanumerics and common punctuation)
        s = re.sub(r'[^\w\s.,!?\'\"-]', '', s)
        # Normalize whitespace
        s = re.sub(r'\s+', ' ', s).strip()
        # Lowercase
        if lowercase:
            s = s.lower()
        return s

    # Apply cleaning
    for col in text_columns:
        df[col] = df[col].astype(str).apply(clean_string)

    # Optional: remove duplicate rows
    if remove_duplicates:
        df = df.drop_duplicates()

    return df.reset_index(drop=True)
