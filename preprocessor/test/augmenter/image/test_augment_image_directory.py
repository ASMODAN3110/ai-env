import pytest
import os
import cv2
import numpy as np
from PIL import Image
from preprocessor.augment_image.image_augmentation import augment_image_directory

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
    valid_img = Image.new("RGB", (100, 100), color="blue")
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
def test_augment_image_directory_with_mixed_files(setup_test_directories, capfd):
    input_dir = setup_test_directories["input_dir"]
    output_dir = setup_test_directories["output_dir"]

    # Appeler la fonction
    augment_image_directory(input_dir, output_dir)

    # Vérifier que le dossier de sortie existe
    assert os.path.exists(output_dir)

    # Vérifier que seules les images valides sont augmentées (5 fichiers par défaut)
    augmented_files = [f for f in os.listdir(output_dir) if f.startswith("valid_aug_")]
    assert len(augmented_files) == 5

    # Vérifier que les fichiers augmentés sont des images valides
    for file_name in augmented_files:
        file_path = os.path.join(output_dir, file_name)
        img = cv2.imread(file_path)
        assert img is not None
        assert img.shape[2] == 3  # Vérifie que c'est une image RGB

    # Vérifier que les fichiers invalides sont gérés (erreur pour corrompu, ignoré pour non image)
    out, err = capfd.readouterr()
    assert "Erreur lors de l'augmentation" in out  # Vérifie l'erreur pour corrupted.png
    assert "Ignorer not_an_image.txt" in out  # Vérifie l'ignorance du fichier texte

# Test pour un répertoire vide
def test_augment_image_directory_empty(setup_test_directories):
    input_dir = setup_test_directories["input_dir"]
    output_dir = setup_test_directories["output_dir"]
    
    # Vider le répertoire d'entrée
    for file in os.listdir(input_dir):
        os.remove(os.path.join(input_dir, file))
    
    # Appeler la fonction
    augment_image_directory(input_dir, output_dir)
    
    # Vérifier que le dossier de sortie existe mais est vide
    assert os.path.exists(output_dir)
    assert len(os.listdir(output_dir)) == 0


# Test pour un répertoire inexistant
def test_augment_image_directory_nonexistent(setup_test_directories):
    input_dir = setup_test_directories["input_dir"] / "nonexistent_subdir"
    output_dir = setup_test_directories["output_dir"]

    # Appeler la fonction sur un répertoire inexistant
    augment_image_directory(input_dir, output_dir)

    # Vérifier que le dossier de sortie existe mais est vide
    assert os.path.exists(output_dir)
    assert len(os.listdir(output_dir)) == 0