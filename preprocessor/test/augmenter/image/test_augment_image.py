import pytest
import os
import cv2
from PIL import Image
from preprocessor.augment_image.image_augmentation import augment_image

# Fixture pour créer des fichiers temporaires
@pytest.fixture
def setup_test_files(tmp_path):
    # Créer un dossier temporaire
    test_dir = tmp_path / "test_images"
    test_dir.mkdir()
    
    # Créer une image valide (PNG)
    valid_img_path = test_dir / "valid.png"
    valid_img = Image.new("RGB", (100, 100), color="red")
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
def test_augment_valid_image(setup_test_files, capfd):
    input_path = setup_test_files["valid"]
    output_dir = setup_test_files["valid"].parent / "augmented"
    
    # Appeler la fonction
    augment_image(input_path, output_dir)
    
    # Vérifier que le dossier de sortie existe
    assert os.path.exists(output_dir)
    
    # Vérifier que le nombre de fichiers générés correspond à num_augmentations (5 par défaut)
    augmented_files = [f for f in os.listdir(output_dir) if f.startswith("valid_aug_")]
    assert len(augmented_files) == 5
    
    # Vérifier que les fichiers sont des images valides
    for file_name in augmented_files:
        file_path = os.path.join(output_dir, file_name)
        img = cv2.imread(file_path)
        assert img is not None
        assert img.shape[2] == 3  # Vérifie que c'est une image RGB
    
    # Vérifier que la sortie est imprimée
    out, err = capfd.readouterr()
    assert "Image augmentée sauvegardée" in out

# Test pour une image corrompue
def test_augment_corrupted_image(setup_test_files, capfd):
    input_path = setup_test_files["corrupted"]
    output_dir = setup_test_files["corrupted"].parent / "augmented"
    
    # Appeler la fonction
    augment_image(input_path, output_dir)
    
    # Vérifier que aucun fichier n'est créé
    assert not os.path.exists(output_dir) or len(os.listdir(output_dir)) == 0
    
    # Vérifier que l'erreur est imprimée
    out, err = capfd.readouterr()
    assert "Erreur lors de l'augmentation" in out

# Test pour un fichier non image
def test_augment_non_image(setup_test_files, capfd):
    input_path = setup_test_files["non_image"]
    output_dir = setup_test_files["non_image"].parent / "augmented"
    
    # Appeler la fonction
    augment_image(input_path, output_dir)
    
    # Vérifier que aucun fichier n'est créé
    assert not os.path.exists(output_dir) or len(os.listdir(output_dir)) == 0
    
    # Vérifier que l'erreur est imprimée
    out, err = capfd.readouterr()
    assert "Erreur lors de l'augmentation" in out

# Test pour un fichier inexistant
def test_augment_nonexistent_image(setup_test_files, capfd):
    input_path = setup_test_files["nonexistent"]
    output_dir = setup_test_files["nonexistent"].parent / "augmented"
    
    # Appeler la fonction
    augment_image(input_path, output_dir)
    
    # Vérifier que aucun fichier n'est créé
    assert not os.path.exists(output_dir) or len(os.listdir(output_dir)) == 0
    
    # Vérifier que l'erreur est imprimée
    out, err = capfd.readouterr()
    assert "Erreur lors de l'augmentation" in out