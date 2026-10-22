"""
AI-Based Smart Waste Segregation and Classification System
Flask Backend Application

Authors: Ruthikraj Nayak, Sai Kiran, Lakshmi Narayana, Santosh Kumar
Model: MobileNetV2 Transfer Learning
Target Classes: Glass, Paper, Metal, Organic Waste, Plastic

Features:
- Live MobileNetV2 Image Classification (File Upload & Webcam)
- Standardized Waste Disposal Recommendations (Feature 3)
- SQLite Database-Driven Waste Statistics Dashboard (Feature 4)
- Classification History with Safe Storage and Clear Action (Feature 5)
- Configurable Low-Confidence Prediction Warning (Feature 6)
- Comprehensive Environmental Awareness Section (Feature 7)
"""

import os
import io
import json
import uuid
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps
import numpy as np

# Import database layer for history and statistics
import database

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Base configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
SAMPLE_FOLDER = os.path.join(BASE_DIR, "sample_test_images")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# Feature 6: Configurable confidence threshold (start at 60.0%)
# If model confidence is below this percentage, a low-confidence warning is shown.
CONFIDENCE_THRESHOLD = 60.0

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database schema
database.init_db()

# Global model state
AI_MODEL = None
AI_MODEL_TYPE = None  # 'keras' or 'tflite'
AI_MODEL_NAME = None
CLASS_INDICES = {}
RECOMMENDATIONS = {}

# Load class indices
CLASS_INDICES_FILE = os.path.join(MODEL_DIR, "class_indices.json")
if os.path.exists(CLASS_INDICES_FILE):
    try:
        with open(CLASS_INDICES_FILE, "r", encoding="utf-8") as f:
            CLASS_INDICES = json.load(f)
        logger.info(f"Loaded class indices: {CLASS_INDICES}")
    except Exception as e:
        logger.error(f"Failed to load class_indices.json: {e}")
else:
    # Default fallback mapping
    CLASS_INDICES = {
        "0": "Glass",
        "1": "Metal",
        "2": "Organic Waste",
        "3": "Paper",
        "4": "Plastic"
    }

# Load recommendations
RECOMMENDATIONS_FILE = os.path.join(MODEL_DIR, "recommendations.json")
if os.path.exists(RECOMMENDATIONS_FILE):
    try:
        with open(RECOMMENDATIONS_FILE, "r", encoding="utf-8") as f:
            RECOMMENDATIONS = json.load(f)
        logger.info(f"Loaded recommendations for: {list(RECOMMENDATIONS.keys())}")
    except Exception as e:
        logger.error(f"Failed to load recommendations.json: {e}")


def load_ai_model():
    """
    Attempt to load a trained model file from the model directory.
    Checks for .keras, .h5, or .tflite formats.
    Returns True if successfully loaded, False otherwise.
    """
    global AI_MODEL, AI_MODEL_TYPE, AI_MODEL_NAME

    candidate_files = [
        ("waste_mobilenetv2.keras", "keras"),
        ("waste_mobilenetv2.h5", "keras"),
        ("model.keras", "keras"),
        ("waste_mobilenetv2.tflite", "tflite"),
    ]

    for filename, m_type in candidate_files:
        model_path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(model_path):
            try:
                if m_type == "keras":
                    import tensorflow as tf
                    logger.info(f"Loading Keras model from: {model_path}")
                    AI_MODEL = tf.keras.models.load_model(model_path)
                    AI_MODEL_TYPE = "keras"
                    AI_MODEL_NAME = filename
                    logger.info("Successfully loaded Keras MobileNetV2 model!")
                    return True
                elif m_type == "tflite":
                    try:
                        import tflite_runtime.interpreter as tflite
                    except ImportError:
                        import tensorflow.lite as tflite
                    logger.info(f"Loading TFLite model from: {model_path}")
                    interpreter = tflite.Interpreter(model_path=model_path)
                    interpreter.allocate_tensors()
                    AI_MODEL = interpreter
                    AI_MODEL_TYPE = "tflite"
                    AI_MODEL_NAME = filename
                    logger.info("Successfully loaded TFLite model!")
                    return True
            except Exception as e:
                logger.error(f"Error loading model from {model_path}: {e}")

    logger.warning("No trained model weights found in 'model/' directory. Running in 'Awaiting Model' mode.")
    AI_MODEL = None
    AI_MODEL_TYPE = None
    AI_MODEL_NAME = None
    return False


# Attempt model load at startup
load_ai_model()


def allowed_file(filename):
    """Validate file extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(image_bytes, target_size=(224, 224)):
    """
    Preprocess image bytes exactly as required by MobileNetV2:
    1. Open with Pillow and convert to RGB (removes alpha/grayscale issues)
    2. Aspect-ratio preserving crop to 224x224 (prevents geometric distortion)
    3. Convert to float32 NumPy array
    4. MobileNetV2 normalization: scale pixel values to [-1.0, 1.0] via (x / 127.5) - 1.0
    5. Expand dimensions to (1, 224, 224, 3) batch format
    """
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Aspect-ratio preserving high-quality crop
    img = ImageOps.fit(img, target_size, Image.Resampling.BICUBIC)

    # Convert to array and normalize
    arr = np.array(img, dtype=np.float32)
    arr = (arr / 127.5) - 1.0
    batch = np.expand_dims(arr, axis=0)
    return batch


def predict_waste_category(img_batch):
    """
    Run inference on the preprocessed image batch using the loaded model.
    Returns the softmax probability array.
    """
    global AI_MODEL, AI_MODEL_TYPE

    if AI_MODEL is None:
        return None

    if AI_MODEL_TYPE == "keras":
        preds = AI_MODEL.predict(img_batch, verbose=0)[0]
    elif AI_MODEL_TYPE == "tflite":
        input_details = AI_MODEL.get_input_details()
        output_details = AI_MODEL.get_output_details()
        AI_MODEL.set_tensor(input_details[0]["index"], img_batch)
        AI_MODEL.invoke()
        preds = AI_MODEL.get_tensor(output_details[0]["index"])[0]
    else:
        return None

    # Ensure softmax probabilities
    preds = np.array(preds, dtype=np.float32)
    if preds.sum() > 0 and not np.isclose(preds.sum(), 1.0, atol=1e-2):
        exp_preds = np.exp(preds - np.max(preds))
        preds = exp_preds / exp_preds.sum()

    return preds


def get_recommendation_for_category(category_name):
    """
    Retrieve standardized disposal recommendation matching Feature 3 specifications.
    Always returns valid instructions, icons, and bin colors without fabricated data.
    """
    norm_cat = database.normalize_category_name(category_name)

    # Standard recommendations mandated by specifications
    canonical_instructions = {
        "Plastic": "Clean the item if possible and place it in the appropriate plastic recycling bin. Follow local recycling rules.",
        "Paper": "Keep it clean and dry, then place it in the paper recycling bin. Avoid recycling heavily contaminated paper.",
        "Metal": "Separate metal items and place recyclable metal in the appropriate recycling bin.",
        "Glass": "Handle carefully and place recyclable glass in the designated glass collection bin. Do not put broken glass into a normal recycling bin unless local rules allow it.",
        "Organic": "Put suitable food scraps and garden waste in a compost bin or an approved organic-waste collection bin."
    }

    base_rec = RECOMMENDATIONS.get(norm_cat) or RECOMMENDATIONS.get(category_name) or {}

    # Build finalized recommendation dict
    rec = {
        "category": norm_cat,
        "disposal_instructions": canonical_instructions.get(norm_cat, base_rec.get("disposal_instructions", "Follow local sanitation rules.")),
        "bin_color": base_rec.get("bin_color", "#10b981"),
        "bin_color_name": base_rec.get("bin_color_name", "Appropriate Bin"),
        "bin_type": base_rec.get("bin_type", "Standard Collection"),
        "recyclable": base_rec.get("recyclable", True),
        "badge_class": base_rec.get("badge_class", f"badge-{norm_cat.lower()}"),
        "icon": base_rec.get("icon", "fa-recycle"),
        "segregation_steps": base_rec.get("segregation_steps", [canonical_instructions.get(norm_cat)]),
        "examples": base_rec.get("examples", ""),
        "environmental_fact": base_rec.get("environmental_fact", "Proper segregation helps preserve environmental quality.")
    }
    return rec


# ============================================================================
# Routes
# ============================================================================

@app.route("/")
def index():
    """Render the homepage introducing the project, categories, and team."""
    model_ready = AI_MODEL is not None
    return render_template("index.html", model_ready=model_ready, model_name=AI_MODEL_NAME)


@app.route("/classify")
def classify_page():
    """Render the classification page with file upload, camera, and sample picker."""
    model_ready = AI_MODEL is not None
    return render_template(
        "classify.html",
        model_ready=model_ready,
        model_name=AI_MODEL_NAME,
        confidence_threshold=CONFIDENCE_THRESHOLD
    )


@app.route("/dashboard")
def dashboard_page():
    """Render the Waste Statistics Dashboard (Feature 4)."""
    stats = database.get_classification_stats()
    return render_template("dashboard.html", stats=stats)


@app.route("/history")
def history_page():
    """Render the Classification History page (Feature 5)."""
    records = database.get_all_classifications(limit=100)
    return render_template("history.html", records=records, count=len(records))


@app.route("/awareness")
def awareness_page():
    """Render the Environmental Awareness section (Feature 7)."""
    return render_template("awareness.html")


@app.route("/api/status")
def api_status():
    """Check current model and system status."""
    if AI_MODEL is None:
        load_ai_model()

    return jsonify({
        "model_ready": AI_MODEL is not None,
        "model_type": AI_MODEL_TYPE,
        "model_name": AI_MODEL_NAME,
        "classes_count": len(CLASS_INDICES),
        "classes": CLASS_INDICES,
        "confidence_threshold": CONFIDENCE_THRESHOLD
    })


@app.route("/api/statistics")
def api_statistics():
    """API endpoint providing real-time statistics computed from SQLite."""
    stats = database.get_classification_stats()
    return jsonify(stats)


@app.route("/api/history")
def api_history():
    """API endpoint returning saved classification history records."""
    records = database.get_all_classifications(limit=200)
    return jsonify({
        "count": len(records),
        "records": records
    })


@app.route("/api/history/clear", methods=["POST"])
def api_history_clear():
    """API endpoint to clear all classification history records with safety."""
    try:
        database.clear_all_classifications()
        return jsonify({
            "success": True,
            "message": "Classification history cleared successfully."
        })
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        return jsonify({
            "success": False,
            "error": "Database error",
            "message": f"Failed to clear history: {str(e)}"
        }), 500


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handle waste image prediction:
    1. Validate input file
    2. Check real AI model availability
    3. Preprocess image
    4. Predict category and confidence
    5. Evaluate low-confidence threshold (Feature 6)
    6. Attach standardized disposal recommendation (Feature 3)
    7. Save successful prediction to SQLite database (Feature 5)
    8. Return complete response
    """
    global AI_MODEL

    if AI_MODEL is None:
        load_ai_model()

    if AI_MODEL is None:
        return jsonify({
            "success": False,
            "model_ready": False,
            "error": "Trained Model Not Found",
            "message": (
                "The AI model file ('waste_mobilenetv2.keras') is not loaded. "
                "No fake or random predictions are shown."
            )
        }), 400

    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "No image uploaded",
            "message": "Please choose an image file to classify."
        }), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "error": "No file selected",
            "message": "Please select an image file."
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "error": "Unsupported file format",
            "message": "Please upload a valid image file (.jpg, .jpeg, .png, or .webp)."
        }), 400

    try:
        image_bytes = file.read()
        preprocessed_batch = preprocess_image(image_bytes)

        probabilities = predict_waste_category(preprocessed_batch)
        if probabilities is None:
            raise ValueError("Inference returned empty result.")

        predicted_idx = int(np.argmax(probabilities))
        confidence_val = float(probabilities[predicted_idx])
        confidence_pct = round(confidence_val * 100, 2)

        predicted_raw = CLASS_INDICES.get(str(predicted_idx), f"Class {predicted_idx}")
        canonical_category = database.normalize_category_name(predicted_raw)

        # Build full probability breakdown
        breakdown = []
        for idx_str, class_name in sorted(CLASS_INDICES.items(), key=lambda x: int(x[0])):
            idx = int(idx_str)
            prob = float(probabilities[idx]) if idx < len(probabilities) else 0.0
            norm_name = database.normalize_category_name(class_name)
            breakdown.append({
                "class_name": norm_name,
                "probability": round(prob * 100, 2)
            })

        breakdown.sort(key=lambda x: x["probability"], reverse=True)

        # Standardized disposal recommendation (Feature 3)
        recommendation = get_recommendation_for_category(canonical_category)

        # Low-confidence evaluation (Feature 6)
        is_low_confidence = confidence_pct < CONFIDENCE_THRESHOLD
        low_confidence_warning = None
        if is_low_confidence:
            low_confidence_warning = (
                "The AI is not confident about this prediction. "
                "Please try another image with better lighting or a clearer view."
            )

        # Save safe unique image file to uploads folder
        ext = file.filename.rsplit(".", 1)[1].lower() if "." in file.filename else "jpg"
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
        saved_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
        with open(saved_path, "wb") as f_out:
            f_out.write(image_bytes)

        # Save record to SQLite database only on genuine success (Feature 5)
        record_id = database.insert_classification(
            category=canonical_category,
            confidence=confidence_pct,
            image_filename=unique_filename
        )

        return jsonify({
            "success": True,
            "model_ready": True,
            "record_id": record_id,
            "category": canonical_category,
            "confidence": confidence_pct,
            "confidence_threshold": CONFIDENCE_THRESHOLD,
            "is_low_confidence": is_low_confidence,
            "warning_message": low_confidence_warning,
            "confidence_disclaimer": (
                "Confidence is the model's score and does not guarantee that the classification is correct."
            ),
            "breakdown": breakdown,
            "recommendation": recommendation,
            "image_url": f"/static/uploads/{unique_filename}"
        })

    except Exception as e:
        logger.exception("Prediction failed with error:")
        return jsonify({
            "success": False,
            "error": "Image processing error",
            "message": f"Could not process the uploaded image: {str(e)}"
        }), 500


@app.route("/sample/<filename>")
def get_sample_image(filename):
    """Serve sample test images for easy demonstration."""
    return send_from_directory(SAMPLE_FOLDER, filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    logger.info("=" * 60)
    logger.info("AI Smart Waste Segregation & Classification Web Server")
    logger.info("Project by: Ruthikraj, Sai Kiran, Lakshmi Narayana, Santosh Kumar")
    logger.info(f"Model status: {'READY (' + str(AI_MODEL_NAME) + ')' if AI_MODEL else 'AWAITING TRAINED MODEL'}")
    logger.info(f"Access locally at: http://127.0.0.1:{port}")
    logger.info("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=debug)
