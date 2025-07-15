import shutil
import pytest
import os
import cv2
import numpy as np
from PIL import Image
from preprocessor.cleaner_image.clean_image_data import clean_image_directory, is_valid_image, load_and_clean_image  # Remplacez 'your_module' par le nom de votre fichier (sans .py)

# Fixture pour créer un répertoire d'entrée avec des fichiers de test
@pytest.fixture
def setup_test_directories(tmp_path):
    # Créer un dossier d'entrée
    input_dir = tmp_path / "input_images"
    input_dir.mkdir()
    
    # Créer un dossier de sortie
    output_dir = tmp_path / "output_images"
    
    # Créer une image valide (PNG)
    valid_img_path = input_dir / "valid.png"
    valid_img = Image.new("RGB", (300, 200), color="green")
    valid_img.save(valid_img_path)
    
    # Créer une image corrompue (fichier tronqué)
    corrupted_img_path = input_dir / "corrupted.png"
    with open(corrupted_img_path, "wb") as f:
        f.write(b"\xFF\xD8\xFF"[:3])  # Début d'un fichier JPG/PNG tronqué
    
    # Créer un fichier non image (texte)
    non_image_path = input_dir / "not_an_image.txt"
    non_image_path.write_text("This is not an image")
    
    # Retourner les chemins
    return {
        "input_dir": input_dir,
        "output_dir": output_dir,
        "valid": valid_img_path,
        "corrupted": corrupted_img_path,
        "non_image": non_image_path
    }

# Test pour un répertoire avec des images valides et invalides
def test_clean_image_directory(setup_test_directories, capfd):
    input_dir = setup_test_directories["input_dir"]
    output_dir = setup_test_directories["output_dir"]
    
    # Appeler la fonction
    processed_images = clean_image_directory(input_dir, output_dir)
    
    # Vérifier que le dossier de sortie existe
    assert os.path.exists(output_dir)
    
    # Vérifier que seule l'image valide est traitée
    assert len(processed_images) == 1
    assert processed_images[0] == "valid.png"
    
    # Vérifier que l'image nettoyée est présente et a la bonne taille
    output_img_path = os.path.join(output_dir, "valid.png")
    assert os.path.exists(output_img_path)
    cleaned_img = cv2.imread(output_img_path)
    assert cleaned_img.shape == (224, 224, 3)
    
    # Vérifier que les fichiers invalides sont ignorés (capturer la sortie)
    out, err = capfd.readouterr()
    assert "Ignorer corrupted.png" in out
    assert "Ignorer not_an_image.txt" in out

# Test pour un répertoire vide
def test_empty_directory(setup_test_directories):
    input_dir = setup_test_directories["input_dir"]
    output_dir = setup_test_directories["output_dir"]
    
    # Vider le répertoire d'entrée
    for file in os.listdir(input_dir):
        os.remove(os.path.join(input_dir, file))
    
    # Appeler la fonction
    processed_images = clean_image_directory(input_dir, output_dir)
    
    # Vérifier que aucune image n'est traitée
    assert len(processed_images) == 0
    assert os.path.exists(output_dir)  # Le dossier est créé même s'il est vide
