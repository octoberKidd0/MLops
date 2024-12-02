import os
import random
import shutil
from pathlib import Path
import yaml

def split_data_with_labels(data_dir, params):
    random.seed(params["base"]["random_seed"])

    # Define image and label directories (adjusting paths to 'data/raw/')
    image_dir = Path(data_dir) / "raw" / "images"
    label_dir = Path(data_dir) / "raw" / "labels"

    # List all image files 
    all_images = list(image_dir.glob("*.jpg"))
    all_labels = list(label_dir.glob("*.txt"))  

    # Ensure each image has a corresponding label
    all_data = []
    for img in all_images:
        label = label_dir / (img.stem + ".txt")
        if label.exists():
            all_data.append((img, label))
    
    # Calculate number of files for splits
    total_files = len(all_data)
    test_size = int(total_files * params["data_split"]["test_pct"])
    valid_size = int(total_files * params["data_split"]["valid_pct"])

    # Shuffle and split
    random.shuffle(all_data)
    test_data = all_data[:test_size]
    valid_data = all_data[test_size:test_size+valid_size]
    train_data = all_data[test_size+valid_size:]

    # Create directories for the splits under 'data/processed'
    for split in ["train", "val", "test"]:
        (Path(data_dir) / "processed" / split / "images").mkdir(parents=True, exist_ok=True)
        (Path(data_dir) / "processed" / split / "labels").mkdir(parents=True, exist_ok=True)

    # Copy images and labels to the respective directories under 'data/processed'
    for img, label in train_data:
        shutil.copy(img, Path(data_dir) / "processed" / "train" / "images" / img.name)
        shutil.copy(label, Path(data_dir) / "processed" / "train" / "labels" / label.name)
    for img, label in valid_data:
        shutil.copy(img, Path(data_dir) / "processed" / "val" / "images" / img.name)
        shutil.copy(label, Path(data_dir) / "processed" / "val" / "labels" / label.name)
    for img, label in test_data:
        shutil.copy(img, Path(data_dir) / "processed" / "test" / "images" / img.name)
        shutil.copy(label, Path(data_dir) / "processed" / "test" / "labels" / label.name)

    print("Data and labels split completed.")

if __name__ == "__main__":
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    split_data_with_labels("data", params)
