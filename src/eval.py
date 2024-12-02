from ultralytics import YOLO
import yaml

def evaluate_model(params):
    n_samples = params["evaluate"]["n_samples_to_save"]
    model = YOLO("runs/train/weights/best.pt")
    metrics = model.val()
    print(f"Evaluation metrics: {metrics}")
    model.predict("data/val", save=True, imgsz=params["train"]["img_size"], max_det=n_samples)

if __name__ == "__main__":
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    evaluate_model(params)
