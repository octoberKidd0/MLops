import os
import random
import shutil
from pathlib import Path
import yaml

def split_data_with_labels(data_dir, params):
    random.seed(params["base"]["random_seed"])

    # Define image and label directories
    image_dir = Path(data_dir) / "images"
    label_dir = Path(data_dir) / "labels"

    # List all image files (assumes images have a corresponding label)
    all_images = list(image_dir.glob("*.jpg"))
    all_labels = list(label_dir.glob("*.txt"))  # Assuming labels are in .txt format

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

    # Create directories for the splits
    for split in ["train", "val", "test"]:
        (Path(data_dir) / split / "images").mkdir(parents=True, exist_ok=True)
        (Path(data_dir) / split / "labels").mkdir(parents=True, exist_ok=True)

    # Move images and labels to the respective directories
    for img, label in train_data:
        shutil.move(img, Path(data_dir) / "train" / "images" / img.name)
        shutil.move(label, Path(data_dir) / "train" / "labels" / label.name)
    for img, label in valid_data:
        shutil.move(img, Path(data_dir) / "val" / "images" / img.name)
        shutil.move(label, Path(data_dir) / "val" / "labels" / label.name)
    for img, label in test_data:
        shutil.move(img, Path(data_dir) / "test" / "images" / img.name)
        shutil.move(label, Path(data_dir) / "test" / "labels" / label.name)

    print("Data and labels split completed.")

if __name__ == "__main__":
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    split_data_with_labels("data/raw", params)
