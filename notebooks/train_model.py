"""
AI-Based Smart Waste Segregation and Classification System
Model Training Script (MobileNetV2 Transfer Learning)

Authors: Ruthikraj Nayak, Sai Kiran, Lakshmi Narayana, Santosh Kumar
Dataset: Real-World Waste Classification Dataset - 5 Class
Source: https://www.kaggle.com/datasets/tuhanasinan/real-world-waste-classification-dataset-5-class
"""

import os
import shutil
import json
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# Set random seeds for reproducibility
SEED = 42
tf.random.set_seed(SEED)
np.random.seed(SEED)

# Hyperparameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
INITIAL_EPOCHS = 15
FINE_TUNE_EPOCHS = 10
NUM_CLASSES = 5

# Mapping from Turkish dataset folder names to English presentation labels
FOLDER_MAPPING = {
    "Cam Atik": "Glass",
    "Kagit Atik": "Paper",
    "Metal Atik": "Metal",
    "Organik Atik": "Organic Waste",
    "Plastik Atik": "Plastic"
}


def prepare_organized_dataset(raw_dataset_dir, output_dir):
    """
    Standardize dataset folders into English class names and split into
    train (70%), val (15%), and test (15%) subsets to prevent data leakage.
    """
    print("=" * 60)
    print("1. Preparing and splitting dataset...")
    print("=" * 60)

    splits = ["train", "val", "test"]
    english_classes = list(FOLDER_MAPPING.values())

    # Create directory structure
    for split in splits:
        for cls in english_classes:
            os.makedirs(os.path.join(output_dir, split, cls), exist_ok=True)

    # Process each class
    for raw_folder, eng_label in FOLDER_MAPPING.items():
        # Match folder loosely in case of unicode variations (e.g. Kağıt Atık vs Kagit Atik)
        matched_folder = None
        for item in os.listdir(raw_dataset_dir):
            if raw_folder.lower() in item.lower() or (raw_folder.split()[0].lower() in item.lower()):
                matched_folder = item
                break

        if not matched_folder:
            raise FileNotFoundError(f"Could not locate folder for {raw_folder} in {raw_dataset_dir}")

        src_class_path = os.path.join(raw_dataset_dir, matched_folder)
        all_images = [f for f in os.listdir(src_class_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        np.random.shuffle(all_images)

        total = len(all_images)
        train_end = int(total * 0.70)
        val_end = int(total * 0.85)

        train_files = all_images[:train_end]
        val_files = all_images[train_end:val_end]
        test_files = all_images[val_end:]

        print(f"Class '{eng_label}': Total {total} -> Train: {len(train_files)}, Val: {len(val_files)}, Test: {len(test_files)}")

        for f in train_files:
            shutil.copy(os.path.join(src_class_path, f), os.path.join(output_dir, "train", eng_label, f))
        for f in val_files:
            shutil.copy(os.path.join(src_class_path, f), os.path.join(output_dir, "val", eng_label, f))
        for f in test_files:
            shutil.copy(os.path.join(src_class_path, f), os.path.join(output_dir, "test", eng_label, f))

    print("\nDataset split complete with ZERO data leakage between splits!\n")


def build_data_pipelines(dataset_dir):
    """
    Create tf.data.Dataset pipelines for training, validation, and testing.
    Uses MobileNetV2 preprocessing and data augmentation.
    """
    print("=" * 60)
    print("2. Building tf.data pipelines...")
    print("=" * 60)

    train_dir = os.path.join(dataset_dir, "train")
    val_dir = os.path.join(dataset_dir, "val")
    test_dir = os.path.join(dataset_dir, "test")

    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        shuffle=True,
        seed=SEED
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        shuffle=False
    )

    test_ds = tf.keras.utils.image_dataset_from_directory(
        test_dir,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        shuffle=False
    )

    class_names = train_ds.class_names
    print(f"\nDetected Classes (Alphabetical): {class_names}")

    # Save class indices mapping
    class_indices = {str(i): name for i, name in enumerate(class_names)}
    with open("class_indices.json", "w", encoding="utf-8") as f:
        json.dump(class_indices, f, indent=2)
    print("Saved 'class_indices.json'.")

    # Data augmentation for training only
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.15),
        layers.RandomZoom(0.15),
        layers.RandomContrast(0.1),
    ], name="data_augmentation")

    # MobileNetV2 preprocessing: (x / 127.5) - 1.0
    preprocess_layer = tf.keras.layers.Lambda(preprocess_input, name="mobilenet_preprocess")

    train_ds = train_ds.map(lambda x, y: (preprocess_layer(data_augmentation(x, training=True)), y),
                            num_parallel_calls=tf.data.AUTOTUNE)
    val_ds = val_ds.map(lambda x, y: (preprocess_layer(x), y),
                        num_parallel_calls=tf.data.AUTOTUNE)
    test_ds = test_ds.map(lambda x, y: (preprocess_layer(x), y),
                          num_parallel_calls=tf.data.AUTOTUNE)

    # Performance optimization
    train_ds = train_ds.prefetch(buffer_size=tf.data.AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=tf.data.AUTOTUNE)
    test_ds = test_ds.prefetch(buffer_size=tf.data.AUTOTUNE)

    return train_ds, val_ds, test_ds, class_names


def build_mobilenetv2_model(num_classes=5):
    """
    Construct transfer learning model using pre-trained MobileNetV2.
    """
    print("=" * 60)
    print("3. Building MobileNetV2 Transfer Learning Model...")
    print("=" * 60)

    base_model = MobileNetV2(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        include_top=False,
        weights="imagenet"
    )
    # Freeze base feature extractor
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(128, activation="relu", name="dense_128")(x)
    x = layers.Dropout(0.35, name="dropout")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="output_classification")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="Waste_MobileNetV2")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.summary()
    return model, base_model


def train_and_evaluate(model, base_model, train_ds, val_ds, test_ds, class_names):
    """
    Train model, fine-tune top layers, and rigorously evaluate on the unseen test set.
    """
    print("=" * 60)
    print("4. Stage 1: Training Classification Head (Feature Extraction)...")
    print("=" * 60)

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=2, min_lr=1e-6),
        tf.keras.callbacks.ModelCheckpoint("best_waste_model.keras", monitor="val_loss", save_best_only=True)
    ]

    history1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=INITIAL_EPOCHS,
        callbacks=callbacks
    )

    print("\n" + "=" * 60)
    print("5. Stage 2: Fine-Tuning Top Layers of MobileNetV2...")
    print("=" * 60)

    # Unfreeze top layers for fine-tuning
    base_model.trainable = True
    # Freeze all layers before layer 100
    for layer in base_model.layers[:100]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),  # Low LR for fine-tuning
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    history2 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=INITIAL_EPOCHS + FINE_TUNE_EPOCHS,
        initial_epoch=len(history1.epoch),
        callbacks=callbacks
    )

    # Evaluate on the unseen test set
    print("\n" + "=" * 60)
    print("6. Rigorous Evaluation on the Unseen Test Set...")
    print("=" * 60)

    test_loss, test_accuracy = model.evaluate(test_ds)
    print(f"\nFinal Test Loss:     {test_loss:.4f}")
    print(f"Final Test Accuracy: {test_accuracy * 100:.2f}%\n")

    # Generate predictions for classification report and confusion matrix
    y_true = []
    y_pred = []
    for images, labels in test_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        y_pred.extend(np.argmax(preds, axis=1))

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    print("Classification Report:")
    report = classification_report(y_true, y_pred, target_names=class_names, digits=4)
    print(report)

    # Plot Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens",
                xticklabels=class_names, yticklabels=class_names)
    plt.title("Confusion Matrix - Test Set (Waste Classification)")
    plt.xlabel("Predicted Category")
    plt.ylabel("Actual Category")
    plt.tight_layout()
    plt.savefig("confusion_matrix.png", dpi=200)
    print("Saved 'confusion_matrix.png'.")

    # Save final model in modern .keras format
    model.save("waste_mobilenetv2.keras")
    print("Saved 'waste_mobilenetv2.keras' successfully!")

    # Also export TFLite for lightweight deployment
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    with open("waste_mobilenetv2.tflite", "wb") as f:
        f.write(tflite_model)
    print("Saved 'waste_mobilenetv2.tflite' successfully!")


if __name__ == "__main__":
    # Example usage when running locally or in Colab
    DATASET_SRC = "dataset_raw"
    SPLIT_OUTPUT = "dataset_split"
    if os.path.exists(DATASET_SRC):
        prepare_organized_dataset(DATASET_SRC, SPLIT_OUTPUT)
        train_ds, val_ds, test_ds, class_names = build_data_pipelines(SPLIT_OUTPUT)
        model, base_model = build_mobilenetv2_model(len(class_names))
        train_and_evaluate(model, base_model, train_ds, val_ds, test_ds, class_names)
    else:
        print(f"Please specify the path to your dataset folder: {DATASET_SRC}")
