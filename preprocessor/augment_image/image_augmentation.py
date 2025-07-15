import os
import numpy as np
from PIL import Image, ImageEnhance
import random
from pathlib import Path

def augment_image(image_path, output_dir, num_augmentations=5):
    """Augmente une image avec diverses transformations."""
    try:
        # Charger l'image avec PIL pour supporter tous les formats
        img = Image.open(image_path).convert('RGB')
        file_name = Path(image_path).stem
        file_ext = Path(image_path).suffix.lower()

        # Créer le répertoire de sortie s'il n'existe pas
        os.makedirs(output_dir, exist_ok=True)

        for i in range(num_augmentations):
            # Appliquer des transformations
            augmented_img = img.copy()

            # Rotation aléatoire (0 à 360 degrés)
            angle = random.randint(0, 360)
            augmented_img = augmented_img.rotate(angle, expand=True)

            # Retournement horizontal ou vertical (50% de chance)
            if random.random() > 0.5:
                augmented_img = augmented_img.transpose(Image.FLIP_LEFT_RIGHT)
            if random.random() > 0.5:
                augmented_img = augmented_img.transpose(Image.FLIP_TOP_BOTTOM)

            # Ajustement de la luminosité (facteur entre 0.5 et 1.5)
            enhancer = ImageEnhance.Brightness(augmented_img)
            brightness_factor = random.uniform(0.5, 1.5)
            augmented_img = enhancer.enhance(brightness_factor)

            # Conversion en array pour OpenCV (ajout de bruit)
            img_array = np.array(augmented_img)
            noise = np.random.normal(0, 25, img_array.shape)
            augmented_img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
            augmented_img = Image.fromarray(augmented_img_array)

            # Redimensionnement aléatoire (80% à 120% de la taille originale)
            scale = random.uniform(0.8, 1.2)
            new_size = (int(img.width * scale), int(img.height * scale))
            augmented_img = augmented_img.resize(new_size, Image.Resampling.LANCZOS)

            # Sauvegarder l'image augmentée avec un suffixe
            output_path = os.path.join(output_dir, f"{file_name}_aug_{i}{file_ext}")
            augmented_img.save(output_path)
            print(f"Image augmentée sauvegardée : {output_path}")

    except Exception as e:
        print(f"Erreur lors de l'augmentation de {image_path} : {e}")


def augment_image_directory(input_dir, output_dir, num_augmentations=5):
    """Augmente toutes les images d'un répertoire."""
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif', '.webp'}

    # Créer le répertoire de sortie
    os.makedirs(output_dir, exist_ok=True)

    # Vérifier si le répertoire d'entrée existe
    if not os.path.exists(input_dir):
        print(f"Répertoire d'entrée {input_dir} inexistant. Aucune image traitée.")
        return

    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        file_ext = Path(file_name).suffix.lower()

        if os.path.isfile(file_path) and file_ext in valid_extensions:
            augment_image(file_path, output_dir, num_augmentations)
        else:
            print(f"Ignorer {file_name} : format non valide ou non un fichier")

if __name__ == "__main__":
    input_directory = r"..\test\augmenter\image"  # Remplacez par votre dossier d'images
    output_directory = "augmented_images"  # Remplacez par le dossier de sortie
    augment_image_directory(input_directory, output_directory, num_augmentations=5)