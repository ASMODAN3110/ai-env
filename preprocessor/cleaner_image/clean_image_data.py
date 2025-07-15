import cv2
import os
from pathlib import Path
from PIL import Image
import numpy as np

def is_valid_image(file_path):
    """Vérifie si une image est valide."""
    try:
        img = Image.open(file_path)
        img.verify()
        return True
    except:
        return False

def load_and_clean_image(file_path, target_size=(224, 224)):
    """Charge et nettoie une image."""
    try:
        # Charger l'image avec OpenCV
        img = cv2.imread(file_path)
        if img is None:
            return None
        # Redimensionner l'image
        img = cv2.resize(img, target_size)
        # Normaliser les couleurs (convertir en RGB et normaliser les valeurs)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0  # Normalisation entre 0 et 1
        return img
    except Exception as e:
        print(f"Erreur lors du traitement de l'image {file_path} : {e}")
        return None

def clean_image_directory(input_dir, output_dir, target_size=(224, 224)):
    """Nettoie toutes les images d'un répertoire."""
    os.makedirs(output_dir, exist_ok=True)
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif', '.webp'}
    processed_images = []
    
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        file_ext = Path(file_name).suffix.lower()
        
        if file_ext in valid_extensions and is_valid_image(file_path):
            cleaned_img = load_and_clean_image(file_path, target_size)
            if cleaned_img is not None:
                output_path = os.path.join(output_dir, file_name)
                # Sauvegarder l'image nettoyée
                cv2.imwrite(output_path, (cleaned_img * 255).astype(np.uint8))
                processed_images.append(file_name)
        else:
            print(f"Ignorer {file_name} : format non valide ou image corrompue")
    
    print(f"Images nettoyées sauvegardées dans {output_dir}")
    return processed_images

if __name__ == "__main__":
    input_directory = r"..\test\cleaner\image"  # Remplacer par votre dossier d'images
    output_directory = "cleaned_test_images"  # Remplacer par le dossier de sortie
    clean_image_directory(input_directory, output_directory)