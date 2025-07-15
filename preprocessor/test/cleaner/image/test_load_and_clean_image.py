import pytest
import cv2
import numpy as np
import os
from PIL import Image
from preprocessor.cleaner_image.clean_image_data import load_and_clean_image  # Remplacez 'your_module' par le nom de votre fichier (sans .py)

# Fixture pour créer des fichiers temporaires
@pytest.fixture
def setup_test_files(tmp_path):
    # Créer un dossier temporaire
    test_dir = tmp_path / "test_images"
    test_dir.mkdir()
    
    # Créer une image valide (PNG)
    valid_img_path = test_dir / "valid.png"
    valid_img = Image.new("RGB", (300, 200), color="blue")
    valid_img.save(valid_img_path)
    
    # Créer une image corrompue (fichier tronqué)
    corrupted_img_path = test_dir / "corrupted.png"
    with open(corrupted_img_path, "wb") as f:
        f.write(b"\xFF\xD8\xFF"[:3])  # Début d'un fichier JPG/PNG tronqué
    
    # Créer un fichier non image (texte)
    non_image_path = test_dir / "not_an_image.txt"
    non_image_path.write_text("This is not an image")
    
    # Retourner les chemins
    return {
        "valid": valid_img_path,
        "corrupted": corrupted_img_path,
        "non_image": non_image_path,
        "nonexistent": test_dir / "nonexistent.png"
    }

# Test pour une image valide
def test_valid_image(setup_test_files):
    file_path = setup_test_files["valid"]
    target_size = (224, 224)
    img = load_and_clean_image(file_path, target_size)
    assert img is not None
    assert isinstance(img, np.ndarray)
    assert img.shape == (target_size[1], target_size[0], 3)  # (hauteur, largeur, canaux)
    assert img.dtype == np.float64  # Normalisation en float
    assert img.max() <= 1.0 and img.min() >= 0.0  # Vérifie la normalisation

# Test pour une image corrompue
def test_corrupted_image(setup_test_files):
    file_path = setup_test_files["corrupted"]
    img = load_and_clean_image(file_path)
    assert img is None

# Test pour un fichier non image
def test_non_image_file(setup_test_files):
    file_path = setup_test_files["non_image"]
    img = load_and_clean_image(file_path)
    assert img is None

# Test pour un fichier inexistant
def test_nonexistent_file(setup_test_files):
    file_path = setup_test_files["nonexistent"]
    img = load_and_clean_image(file_path)
    assert img is None