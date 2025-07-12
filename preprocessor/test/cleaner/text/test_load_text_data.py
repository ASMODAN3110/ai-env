import pytest
import pandas as pd

from preprocessor.cleaner_text.clean_text_data import load_text_data

# Fixture pour créer des fichiers temporaires
@pytest.fixture
def setup_test_files(tmp_path):
    # Créer un dossier temporaire
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()
    
    # Créer un fichier CSV
    csv_path = test_dir / "test.csv"
    csv_content = "text\nHello, World!\nTest Line"
    csv_path.write_text(csv_content)
    
    # Créer un fichier TXT
    txt_path = test_dir / "test.txt"
    txt_content = "Line 1\nLine 2\nLine 3"
    txt_path.write_text(txt_content)
    
    # Créer un fichier JSON
    json_path = test_dir / "test.json"
    json_content = '[{"text": "JSON Line 1"}, {"text": "JSON Line 2"}]'
    json_path.write_text(json_content)
    
    # Retourner les chemins
    return {
        "csv": csv_path,
        "txt": txt_path,
        "json": json_path,
        "invalid": test_dir / "test.invalid",
        "nonexistent": test_dir / "nonexistent.txt"
    }

# Test pour le chargement d'un fichier CSV
def test_load_csv(setup_test_files):
    file_path = setup_test_files["csv"]
    df = load_text_data(file_path)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2  # Deux lignes de données + en-tête
    assert df.iloc[0]["text"] == "Hello, World!"

# Test pour le chargement d'un fichier TXT
def test_load_txt(setup_test_files):
    file_path = setup_test_files["txt"]
    df = load_text_data(file_path)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3  # Trois lignes
    assert df.iloc[0]["text"] == "Line 1"

# Test pour le chargement d'un fichier JSON
def test_load_json(setup_test_files):
    file_path = setup_test_files["json"]
    df = load_text_data(file_path)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2  # Deux objets JSON
    assert df.iloc[0]["text"] == "JSON Line 1"

# Test pour un format de fichier non supporté
def test_load_invalid_format(setup_test_files):
    file_path = setup_test_files["invalid"]
    file_path.touch()  # Créer un fichier vide avec extension non supportée
    df = load_text_data(file_path)
    assert df is None  # Devrait retourner None en cas d'erreur

# Test pour un fichier inexistant
def test_load_nonexistent_file(setup_test_files):
    file_path = setup_test_files["nonexistent"]
    df = load_text_data(file_path)
    assert df is None  # Devrait retourner None en cas d'erreur

# Test pour un fichier corrompu (JSON mal formé)
def test_load_corrupted_json(setup_test_files):
    file_path = setup_test_files["json"]
    file_path.write_text("{invalid json")  # JSON mal formé
    df = load_text_data(file_path)
    assert df is None  # Devrait retourner None en cas d'erreur