import os
import random
import shutil
from pathlib import Path
import yaml

def split_data(data_dir, params):
    random.seed(params["base"]["random_seed"])
    
    # List all images
    all_files = list(Path(data_dir).glob("*.jpg"))
    
    # Calculate how many files to split off
    total_files = len(all_files)
    test_size = int(total_files * params["data_split"]["test_pct"])
    valid_size = int(total_files * params["data_split"]["valid_pct"])
    
    # Shuffle and split
    random.shuffle(all_files)
    test_files = all_files[:test_size]
    valid_files = all_files[test_size:test_size+valid_size]
    train_files = all_files[test_size+valid_size:]

    # Create directories for the splits
    for split in ["train", "val", "test"]:
        split_dir = Path(data_dir) / split
        split_dir.mkdir(parents=True, exist_ok=True)

    # Move files to corresponding directories
    for file in train_files:
        shutil.move(file, Path(data_dir) / "train" / file.name)
    for file in valid_files:
        shutil.move(file, Path(data_dir) / "val" / file.name)
    for file in test_files:
        shutil.move(file, Path(data_dir) / "test" / file.name)
    
    print("Data split completed.")

if __name__ == "__main__":
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    split_data("data/raw", params)
