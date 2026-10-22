"""
Fast Zero-Copy Model Training Script for MobileNetV2
Directly loads from original dataset in Downloads, caching MobileNetV2 features for ultra-fast training.

Authors: Ruthikraj Nayak, Sai Kiran, Lakshmi Narayana, Santosh Kumar
"""

import os
import sys
import json
import time
import numpy as np
from PIL import Image

# Ensure standard UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Seeds for 100% reproducible splitting & training
SEED = 42
tf.random.set_seed(SEED)
np.random.seed(SEED)

RAW_DATASET_DIR = r"C:\Users\chowh\Downloads\archive (1)\Real-World Garbage-Waste Classification (5 Classes)\Real-World Garbage-Waste Classification (5 Classes)"
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
MODEL_DIR = os.path.join(PROJECT_ROOT, "model")

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

LETTER_TO_LABEL = {
    "c": "Glass",
    "k": "Paper",
    "m": "Metal",
    "o": "Organic Waste",
    "p": "Plastic"
}

TARGET_CLASSES = ["Glass", "Paper", "Metal", "Organic Waste", "Plastic"]


def collect_and_split_paths():
    """
    Collect all image paths and split into train (70%), val (15%), test (15%) in memory.
    Avoids copying files to prevent OneDrive locking issues.
    """
    print("=" * 60)
    print("Step 1: Splitting dataset (70% Train, 15% Val, 15% Test)...")
    print("=" * 60)

    train_paths, val_paths, test_paths = [], [], []
    train_labels, val_labels, test_labels = [], [], []

    raw_items = os.listdir(RAW_DATASET_DIR)
    total_found = 0

    # Alphabetical order: Glass (0), Metal (1), Organic Waste (2), Paper (3), Plastic (4)
    ordered_classes = sorted(TARGET_CLASSES)
    class_to_idx = {cls: idx for idx, cls in enumerate(ordered_classes)}

    for item in sorted(raw_items):
        first_letter = item.strip()[0].lower()
        if first_letter not in LETTER_TO_LABEL:
            continue

        eng_label = LETTER_TO_LABEL[first_letter]
        class_idx = class_to_idx[eng_label]
        src_dir = os.path.join(RAW_DATASET_DIR, item)

        if not os.path.isdir(src_dir):
            continue

        images = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        # Shuffle deterministically
        rng = np.random.RandomState(SEED)
        rng.shuffle(images)

        total = len(images)
        n_train = int(total * 0.70)
        n_val = int(total * 0.15)

        tr_img = images[:n_train]
        vl_img = images[n_train:n_train + n_val]
        ts_img = images[n_train + n_val:]

        train_paths.extend(tr_img)
        train_labels.extend([class_idx] * len(tr_img))

        val_paths.extend(vl_img)
        val_labels.extend([class_idx] * len(vl_img))

        test_paths.extend(ts_img)
        test_labels.extend([class_idx] * len(ts_img))

        print(f"Class '{eng_label:14s}' (idx {class_idx}): Total={total:3d} | Train={len(tr_img):3d} | Val={len(vl_img):2d} | Test={len(ts_img):2d}")
        total_found += total

    print(f"\nTotal Dataset: {total_found} images | Train: {len(train_paths)} | Val: {len(val_paths)} | Test: {len(test_paths)}")
    return (train_paths, train_labels), (val_paths, val_labels), (test_paths, test_labels), ordered_classes


def load_images_to_array(paths, labels, num_classes):
    """Load image paths into preprocessed float32 NumPy arrays."""
    images = []
    one_hots = []

    for path, label_idx in zip(paths, labels):
        try:
            img = Image.open(path).convert("RGB").resize(IMG_SIZE, Image.Resampling.BILINEAR)
            arr = np.array(img, dtype=np.float32)
            # MobileNetV2 formula: (arr / 127.5) - 1.0
            arr = preprocess_input(arr)
            images.append(arr)

            oh = np.zeros(num_classes, dtype=np.float32)
            oh[label_idx] = 1.0
            one_hots.append(oh)
        except Exception as e:
            print(f"Skipping {path}: {e}")

    return np.array(images, dtype=np.float32), np.array(one_hots, dtype=np.float32)


def main():
    start_time = time.time()

    (tr_p, tr_l), (vl_p, vl_l), (ts_p, ts_l), ordered_classes = collect_and_split_paths()
    num_classes = len(ordered_classes)

    # Save class indices
    class_indices = {str(i): name for i, name in enumerate(ordered_classes)}
    with open(os.path.join(MODEL_DIR, "class_indices.json"), "w", encoding="utf-8") as f:
        json.dump(class_indices, f, indent=2)
    print(f"\nUpdated 'model/class_indices.json': {class_indices}")

    print("\n" + "=" * 60)
    print("Step 2: Loading images into preprocessed arrays...")
    print("=" * 60)

    X_train, y_train = load_images_to_array(tr_p, tr_l, num_classes)
    X_val, y_val = load_images_to_array(vl_p, vl_l, num_classes)
    X_test, y_test = load_images_to_array(ts_p, ts_l, num_classes)

    print(f"Data Loaded: Train shape={X_train.shape}, Val shape={X_val.shape}, Test shape={X_test.shape}")

    print("\n" + "=" * 60)
    print("Step 3: Extracting MobileNetV2 features (ImageNet weights)...")
    print("=" * 60)

    base_model = MobileNetV2(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False

    gap = layers.GlobalAveragePooling2D(name="gap")

    features_train = gap(base_model.predict(X_train, batch_size=32, verbose=1)).numpy()
    features_val = gap(base_model.predict(X_val, batch_size=32, verbose=1)).numpy()
    features_test = gap(base_model.predict(X_test, batch_size=32, verbose=1)).numpy()

    print(f"Features extracted: Train={features_train.shape}, Val={features_val.shape}, Test={features_test.shape}")

    print("\n" + "=" * 60)
    print("Step 4: Training Classification Head...")
    print("=" * 60)

    head = models.Sequential([
        layers.Input(shape=(1280,), name="head_input"),
        layers.BatchNormalization(name="head_bn"),
        layers.Dense(128, activation="relu", name="head_dense"),
        layers.Dropout(0.35, name="head_dropout"),
        layers.Dense(num_classes, activation="softmax", name="predictions")
    ], name="Waste_Classifier_Head")

    head.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, min_lr=1e-5)
    ]

    history = head.fit(
        features_train, y_train,
        validation_data=(features_val, y_val),
        epochs=30,
        batch_size=32,
        callbacks=callbacks,
        verbose=1
    )

    print("\n" + "=" * 60)
    print("Step 5: Assembling Full End-to-End Model & Saving...")
    print("=" * 60)

    # Recombine base feature extractor + GAP + Head into single model
    full_input = tf.keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3), name="image_input")
    x = base_model(full_input, training=False)
    x = gap(x)
    outputs = head(x)
    full_model = tf.keras.Model(inputs=full_input, outputs=outputs, name="Waste_MobileNetV2_Full")

    full_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    target_model_path = os.path.join(MODEL_DIR, "waste_mobilenetv2.keras")
    full_model.save(target_model_path)
    size_mb = round(os.path.getsize(target_model_path) / (1024 * 1024), 2)
    print(f"SUCCESS: Full trained model saved to '{target_model_path}' ({size_mb} MB)!")

    print("\n" + "=" * 60)
    print("Step 6: Evaluation on the Unseen Test Set...")
    print("=" * 60)

    test_loss, test_accuracy = full_model.evaluate(X_test, y_test, batch_size=32, verbose=1)
    print(f"\n==========================================")
    print(f"Test Accuracy: {test_accuracy * 100:.2f}%")
    print(f"Test Loss:     {test_loss:.4f}")
    print(f"==========================================\n")

    # Evaluation Metrics
    y_pred_probs = full_model.predict(X_test, batch_size=32, verbose=0)
    y_true_indices = np.argmax(y_test, axis=1)
    y_pred_indices = np.argmax(y_pred_probs, axis=1)

    try:
        from sklearn.metrics import classification_report, confusion_matrix
        import matplotlib.pyplot as plt
        import seaborn as sns

        report = classification_report(y_true_indices, y_pred_indices, target_names=ordered_classes, digits=4)
        print("Detailed Classification Report:\n")
        print(report)

        cm = confusion_matrix(y_true_indices, y_pred_indices)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Greens",
                    xticklabels=ordered_classes, yticklabels=ordered_classes)
        plt.title("Confusion Matrix — Test Set Evaluation", fontsize=14, fontweight="bold", pad=12)
        plt.xlabel("Predicted Category", fontsize=12)
        plt.ylabel("Actual True Category", fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(PROJECT_ROOT, "confusion_matrix.png"), dpi=200)
        print("Saved 'confusion_matrix.png'!")

        # Training curves
        plt.figure(figsize=(12, 4))
        plt.subplot(1, 2, 1)
        plt.plot(history.history["accuracy"], label="Train Accuracy", color="#16a34a", linewidth=2)
        plt.plot(history.history["val_accuracy"], label="Val Accuracy", color="#0284c7", linewidth=2, linestyle="--")
        plt.title("Accuracy vs Epochs", fontweight="bold")
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.legend()
        plt.grid(alpha=0.3)

        plt.subplot(1, 2, 2)
        plt.plot(history.history["loss"], label="Train Loss", color="#dc2626", linewidth=2)
        plt.plot(history.history["val_loss"], label="Val Loss", color="#ea580c", linewidth=2, linestyle="--")
        plt.title("Loss vs Epochs", fontweight="bold")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.legend()
        plt.grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig(os.path.join(PROJECT_ROOT, "training_curves.png"), dpi=200)
        print("Saved 'training_curves.png'!")

    except Exception as e:
        print(f"Visualization note: {e}")

    elapsed = time.time() - start_time
    print(f"\nTotal Pipeline Time: {elapsed:.1f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()
