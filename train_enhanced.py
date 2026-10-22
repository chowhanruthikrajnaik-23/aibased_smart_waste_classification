"""
Enhanced MobileNetV2 Training Script with Heavy Data Augmentation & Fine-Tuning
Maximizes real-world webcam & photo accuracy across all 5 waste categories.

Dataset: 1,647 real-world images from Kaggle
"""

import os
import sys
import json
import time
import numpy as np
from PIL import Image, ImageOps

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Seeds
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

TARGET_CLASSES = ["Glass", "Metal", "Organic Waste", "Paper", "Plastic"]


def collect_paths():
    """Collect and split all 1,647 image paths with 80/10/10 ratio."""
    print("=" * 60)
    print("Collecting images from Kaggle dataset...")
    print("=" * 60)

    train_paths, train_labels = [], []
    val_paths, val_labels = [], []
    test_paths, test_labels = [], []

    raw_items = os.listdir(RAW_DATASET_DIR)
    class_to_idx = {cls: idx for idx, cls in enumerate(TARGET_CLASSES)}
    total_imgs = 0

    for item in sorted(raw_items):
        first_char = item.strip()[0].lower()
        if first_char not in LETTER_TO_LABEL:
            continue

        eng_label = LETTER_TO_LABEL[first_char]
        class_idx = class_to_idx[eng_label]
        src_dir = os.path.join(RAW_DATASET_DIR, item)

        if not os.path.isdir(src_dir):
            continue

        images = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        rng = np.random.RandomState(SEED)
        rng.shuffle(images)

        n = len(images)
        total_imgs += n
        n_train = int(n * 0.80)
        n_val = int(n * 0.10)

        tr = images[:n_train]
        vl = images[n_train:n_train + n_val]
        ts = images[n_train + n_val:]

        train_paths.extend(tr)
        train_labels.extend([class_idx] * len(tr))

        val_paths.extend(vl)
        val_labels.extend([class_idx] * len(vl))

        test_paths.extend(ts)
        test_labels.extend([class_idx] * len(ts))

        print(f"Class '{eng_label:14s}' (idx {class_idx}): Total={n:3d} | Train={len(tr):3d} | Val={len(vl):2d} | Test={len(ts):2d}")

    print(f"\nTotal Dataset: {total_imgs} images -> Train: {len(train_paths)}, Val: {len(val_paths)}, Test: {len(test_paths)}")
    return (train_paths, train_labels), (val_paths, val_labels), (test_paths, test_labels)


def load_images_with_aspect_ratio(paths, labels):
    """Load images with ImageOps.fit to preserve true aspect ratio without squashing."""
    images = []
    one_hots = []
    num_classes = len(TARGET_CLASSES)

    for path, label_idx in zip(paths, labels):
        try:
            img = Image.open(path).convert("RGB")
            # Preserve aspect ratio with center crop
            img = ImageOps.fit(img, IMG_SIZE, Image.Resampling.BICUBIC)
            arr = np.array(img, dtype=np.float32)
            # MobileNetV2 formula: [-1.0, 1.0]
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
    (tr_p, tr_l), (vl_p, vl_l), (ts_p, ts_l) = collect_paths()

    # Save class indices
    class_indices = {str(i): name for i, name in enumerate(TARGET_CLASSES)}
    with open(os.path.join(MODEL_DIR, "class_indices.json"), "w", encoding="utf-8") as f:
        json.dump(class_indices, f, indent=2)
    print("Class indices mapping:", class_indices)

    print("\nLoading and aspect-ratio preprocessing images into RAM...")
    X_train, y_train = load_images_with_aspect_ratio(tr_p, tr_l)
    X_val, y_val = load_images_with_aspect_ratio(vl_p, vl_l)
    X_test, y_test = load_images_with_aspect_ratio(ts_p, ts_l)

    print(f"Loaded: X_train={X_train.shape}, X_val={X_val.shape}, X_test={X_test.shape}")

    # Build Heavy Data Augmentation Generator for Training
    datagen = ImageDataGenerator(
        rotation_range=25,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.15,
        zoom_range=0.20,
        horizontal_flip=True,
        fill_mode="nearest"
    )

    print("\n" + "=" * 60)
    print("Constructing MobileNetV2 Model Architecture...")
    print("=" * 60)

    base_model = MobileNetV2(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D(name="gap")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(256, activation="relu", name="dense_256")(x)
    x = layers.Dropout(0.40, name="dropout_1")(x)
    x = layers.Dense(128, activation="relu", name="dense_128")(x)
    x = layers.Dropout(0.30, name="dropout_2")(x)
    outputs = layers.Dense(len(TARGET_CLASSES), activation="softmax", name="predictions")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="Waste_MobileNetV2_Enhanced")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    print("\n" + "=" * 60)
    print("Stage 1: Training Classification Head with Data Augmentation (12 Epochs)...")
    print("=" * 60)

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, min_lr=1e-6)
    ]

    history1 = model.fit(
        datagen.flow(X_train, y_train, batch_size=BATCH_SIZE, seed=SEED),
        steps_per_epoch=len(X_train) // BATCH_SIZE,
        validation_data=(X_val, y_val),
        epochs=12,
        callbacks=callbacks,
        verbose=1
    )

    print("\n" + "=" * 60)
    print("Stage 2: Fine-Tuning Top Convolutional Layers of MobileNetV2 (8 Epochs)...")
    print("=" * 60)

    # Unfreeze top layers for fine-tuning
    base_model.trainable = True
    # Freeze bottom layers, fine-tune layers 100 onwards
    for layer in base_model.layers[:100]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),  # Low LR for fine-tuning
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    history2 = model.fit(
        datagen.flow(X_train, y_train, batch_size=BATCH_SIZE, seed=SEED),
        steps_per_epoch=len(X_train) // BATCH_SIZE,
        validation_data=(X_val, y_val),
        epochs=8,
        callbacks=callbacks,
        verbose=1
    )

    print("\n" + "=" * 60)
    print("Saving Enhanced Model...")
    print("=" * 60)

    target_path = os.path.join(MODEL_DIR, "waste_mobilenetv2.keras")
    model.save(target_path)
    size_mb = round(os.path.getsize(target_path) / (1024 * 1024), 2)
    print(f"SUCCESS: Saved enhanced model to '{target_path}' ({size_mb} MB)!")

    print("\n" + "=" * 60)
    print("Evaluating on Unseen Test Set...")
    print("=" * 60)

    test_loss, test_acc = model.evaluate(X_test, y_test, batch_size=BATCH_SIZE, verbose=1)
    print(f"\n==========================================")
    print(f"Final Test Accuracy: {test_acc * 100:.2f}%")
    print(f"Final Test Loss:     {test_loss:.4f}")
    print(f"==========================================\n")

    y_pred_probs = model.predict(X_test, batch_size=BATCH_SIZE, verbose=0)
    y_true_indices = np.argmax(y_test, axis=1)
    y_pred_indices = np.argmax(y_pred_probs, axis=1)

    try:
        from sklearn.metrics import classification_report, confusion_matrix
        import matplotlib.pyplot as plt
        import seaborn as sns

        report = classification_report(y_true_indices, y_pred_indices, target_names=TARGET_CLASSES, digits=4)
        print("Classification Report:\n", report)

        cm = confusion_matrix(y_true_indices, y_pred_indices)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Greens",
                    xticklabels=TARGET_CLASSES, yticklabels=TARGET_CLASSES)
        plt.title("Confusion Matrix — Enhanced Model", fontsize=14, fontweight="bold", pad=12)
        plt.xlabel("Predicted Category", fontsize=12)
        plt.ylabel("Actual True Category", fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(PROJECT_ROOT, "confusion_matrix.png"), dpi=200)

        # Plot curves
        acc = history1.history["accuracy"] + history2.history["accuracy"]
        val_acc = history1.history["val_accuracy"] + history2.history["val_accuracy"]
        loss = history1.history["loss"] + history2.history["loss"]
        val_loss = history1.history["val_loss"] + history2.history["val_loss"]

        plt.figure(figsize=(12, 4))
        plt.subplot(1, 2, 1)
        plt.plot(acc, label="Train Accuracy", color="#16a34a", linewidth=2)
        plt.plot(val_acc, label="Val Accuracy", color="#0284c7", linewidth=2, linestyle="--")
        plt.axvline(x=len(history1.epoch)-1, color="red", linestyle=":", label="Fine-Tuning Start")
        plt.title("Accuracy vs Epochs", fontweight="bold")
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.legend()
        plt.grid(alpha=0.3)

        plt.subplot(1, 2, 2)
        plt.plot(loss, label="Train Loss", color="#dc2626", linewidth=2)
        plt.plot(val_loss, label="Val Loss", color="#ea580c", linewidth=2, linestyle="--")
        plt.axvline(x=len(history1.epoch)-1, color="red", linestyle=":", label="Fine-Tuning Start")
        plt.title("Loss vs Epochs", fontweight="bold")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.legend()
        plt.grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig(os.path.join(PROJECT_ROOT, "training_curves.png"), dpi=200)
        print("Updated 'confusion_matrix.png' and 'training_curves.png'!")

    except Exception as e:
        print("Plotting note:", e)

    print(f"\nTotal Pipeline Time: {time.time() - start_time:.1f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()
