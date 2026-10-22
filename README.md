# AI-Based Smart Waste Segregation and Classification System

An intelligent, full-stack AI web application developed for college presentation and practical waste management demonstration. The system identifies waste items from uploaded images or live camera snapshots and accurately classifies them into five segregation categories: **Plastic, Paper, Metal, Glass, and Organic Waste**, providing actionable segregation steps, bin recommendations, and environmental conservation facts.

---

## 👥 Academic Project Team

- **Ruthikraj Nayak** (2024BVS0079)
- **Sai Kiran** (2024BCS0087)
- **Lakshmi Narayana** (2024BEC0047)
- **Santosh Kumar** (2024BCS0175)

---

## 📌 Project Overview & Key Features

1. **5-Class Waste Segregation**:
   - 🔵 **Plastic** &rarr; Blue Bin (Recyclable Dry Waste)
   - 🔷 **Paper** &rarr; Blue / Paper Bin (Dry Cellulosic Waste)
   - 🟡 **Metal** &rarr; Yellow / Red Bin (Infinitely Recyclable Metals)
   - 🟢 **Glass** &rarr; Green / Glass Bin (Container Glass Bank)
   - 🌿 **Organic Waste** &rarr; Green Compost Bin (Biodegradable Wet Waste)

2. **Deep Learning Architecture**:
   - Backbone: **MobileNetV2** with Transfer Learning (pre-trained on ImageNet).
   - Custom classification head: `GlobalAveragePooling2D` &rarr; `BatchNormalization` &rarr; `Dense(128, ReLU)` &rarr; `Dropout(0.35)` &rarr; `Dense(5, Softmax)`.
   - Data preprocessing follows MobileNetV2 specification: image resized to $224 \times 224 \times 3$ with pixel values scaled to $[-1.0, 1.0]$ via $(x / 127.5) - 1.0$.

3. **Web Application & UI**:
   - Modern, responsive **green-and-white eco-friendly design** built with HTML5, CSS3, and JavaScript.
   - **Home Page (`/`)**: Project background, 5 category cards, system architecture overview, and team credits.
   - **Classifier Page (`/classify`)**: Drag-and-drop file upload, instant image preview, live webcam capture (WebRTC), animated confidence bar, disposal instructions checklist, environmental impact facts, full 5-class probability breakdown, and local guidelines disclaimer.
   - **Quick Demo Sample Picker**: 1-click test chips for Glass, Paper, Metal, Organic, and Plastic images for live presentations.
   - **Graceful Error Handling**: Completely honest backend—if model weights are awaiting training, the UI clearly displays instructions without faking predictions or generating random numbers.

---

## 📁 Project Directory Structure

```text
AI project/
├── app.py                             # Flask web backend application
├── run.bat                            # 1-Click Windows launch script
├── requirements.txt                   # Project Python dependencies
├── test_app.py                        # Automated unit & integration test suite
├── README.md                          # Full documentation & presentation guide
├── model/
│   ├── class_indices.json             # Exact mapping of class IDs to English labels
│   ├── recommendations.json           # Bin colors, recycling guidance & eco facts
│   └── waste_mobilenetv2.keras        # Saved trained model weights (place here after Colab training)
├── notebooks/
│   ├── waste_classification_training.ipynb  # Step-by-step Google Colab training notebook
│   └── train_model.py                 # Standalone Python training script
├── sample_test_images/                # 10 Real test images extracted from dataset
│   ├── glass_sample_1.jpg, glass_sample_2.jpg
│   ├── paper_sample_1.jpg, paper_sample_2.jpg
│   ├── metal_sample_1.jpg, metal_sample_2.jpg
│   ├── organic_sample_1.jpg, organic_sample_2.jpg
│   └── plastic_sample_1.jpg, plastic_sample_2.jpg
├── static/
│   ├── css/
│   │   └── style.css                  # Custom eco-green theme styling
│   ├── js/
│   │   └── main.js                    # Client-side upload, webcam, and AJAX logic
│   └── uploads/                       # Temporary folder for classified images
└── templates/
    ├── index.html                     # Home page template
    └── classify.html                  # Waste classification & camera template
```

---

## 📊 Dataset Details

The system is trained on the Kaggle public dataset:
**[Real-World Waste Classification Dataset – 5 Class](https://www.kaggle.com/datasets/tuhanasinan/real-world-waste-classification-dataset-5-class)**

The dataset was already downloaded and verified in your Downloads folder:
`C:\Users\chowh\Downloads\archive (1)\Real-World Garbage-Waste Classification (5 Classes)\Real-World Garbage-Waste Classification (5 Classes)`

### Class Distribution & Test Evaluation (1,647 Total Images):
| Dataset Folder | Category Name | Total | Train (70%) | Val (15%) | Test (15%) | Test Precision | Test Recall | Test F1-Score |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Cam Atik` | **Glass** | 314 | 219 | 47 | 48 | **93.48%** | 89.58% | **91.49%** |
| `Metal Atik` | **Metal** | 375 | 262 | 56 | 57 | **82.26%** | 89.47% | **85.71%** |
| `Organik Atik` | **Organic Waste** | 300 | 210 | 45 | 45 | **97.56%** | 88.89% | **93.02%** |
| `Kagit Atik` | **Paper** | 323 | 226 | 48 | 49 | **86.96%** | 81.63% | **84.21%** |
| `Plastik Atik` | **Plastic** | 335 | 234 | 50 | 51 | **78.18%** | 84.31% | **81.13%** |
| **Overall** | **5 Classes** | **1,647** | **1,151** | **246** | **250** | **87.26%** (Avg) | **86.80%** | **86.91%** (Avg) |

- **Overall Test Accuracy**: **86.80%** (Evaluated on 250 completely unseen test images)
- **Overall Test Loss**: **0.3646**
- **Evaluation Visualizations**:
  - `confusion_matrix.png`: Heatmap showing true vs. predicted counts across all 5 classes.
  - `training_curves.png`: Training vs. Validation Accuracy and Loss progression over epochs.

---

## 🚀 Quick Start (Local Web Server)

### Step 1: Install Python Dependencies
Open PowerShell or Command Prompt in the project folder:
```powershell
cd "c:\Users\chowh\OneDrive\Desktop\AI project"
python -m pip install -r requirements.txt
```

### Step 2: Run the Web Server
You can simply double-click **`run.bat`**, or execute:
```powershell
python app.py
```

### Step 3: Open in Browser
Open your web browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🧠 Model Training in Google Colab (Step-by-Step)

Google Colab provides free GPU acceleration (NVIDIA T4), which trains the deep learning model in approximately 5 to 8 minutes.

### Steps to Train:
1. Open [Google Colab](https://colab.research.google.com).
2. Click **Upload** and select `notebooks/waste_classification_training.ipynb` from this project.
3. Enable GPU:
   - Go to top menu: **Runtime** &rarr; **Change runtime type**.
   - Select **T4 GPU** under Hardware accelerator &rarr; Click **Save**.
4. Upload your dataset zip file:
   - In Colab's left sidebar, click the 📁 **Files** icon.
   - Click the **Upload** icon and upload your `archive (1).zip` (or download it via Kaggle API in Cell 3).
5. Click **Runtime** &rarr; **Run all** (or execute cells sequentially).
6. The notebook will automatically:
   - Unpack and reorganize images into `train` (70%), `val` (15%), and `test` (15%) subsets.
   - Apply data augmentation (horizontal flip, random rotation, random zoom, contrast).
   - Build the MobileNetV2 transfer learning network.
   - Train the classification head (Stage 1) and fine-tune top layers (Stage 2).
   - Evaluate on the unseen test set, printing the **Classification Report** (Precision, Recall, F1) and plotting the **Confusion Matrix** (`confusion_matrix.png`) and **Accuracy/Loss Curves** (`training_curves.png`).
   - Automatically trigger download of `waste_mobilenetv2.keras` and `class_indices.json`.
7. **Deploying the Trained Model**:
   - Move the downloaded `waste_mobilenetv2.keras` into your local `model/` folder:
     `c:\Users\chowh\OneDrive\Desktop\AI project\model\waste_mobilenetv2.keras`
   - Refresh your Flask application (`http://127.0.0.1:5000/classify`). The status banner will turn green: **AI Model Active: waste_mobilenetv2.keras**!

---

## 🧪 Automated Testing

An automated test suite (`test_app.py`) is included to verify all components without needing external testing frameworks:

```powershell
python test_app.py
```

### Test Suite Covers:
- ✅ **Route Integrity**: Verifies `/` and `/classify` return HTTP 200 with proper template rendering.
- ✅ **Status API**: Verifies `/api/status` returns valid JSON with all 5 classes.
- ✅ **Preprocessing Integrity**: Ensures images are resized to $(224, 224, 3)$, float32, and scaled strictly within $[-1.0, 1.0]$.
- ✅ **Error Handling**: Verifies missing files and invalid extensions (e.g. `.txt`) are rejected with HTTP 400.
- ✅ **Honest Missing Model Refusal**: Ensures the application displays an informative message rather than inventing fake predictions or random numbers.
- ✅ **Class-to-Recommendation Mapping**: Validates all 5 classes have designated bin colors, segregation steps, and eco facts.
- ✅ **Sample Test Images**: Preprocesses real dataset samples across all 5 categories.

---

## 🎓 College Presentation & Viva Guide

Use these structured explanations and answers during your project review or viva voce:

### 1. High-Level System Workflow
1. **Input Phase**: The user uploads an image or captures a live frame using the device webcam via WebRTC.
2. **Preprocessing**: The image is decoded using Pillow, converted to RGB, rescaled to $224 \times 224$ pixels, and normalized to $[-1.0, 1.0]$ using MobileNetV2's formula: $\text{Normalized} = \frac{\text{Pixel}}{127.5} - 1.0$.
3. **Inference**: The preprocessed tensor is passed through the MobileNetV2 transfer learning model. Softmax outputs a probability distribution across the 5 classes.
4. **Segregation Guidance**: The system identifies the class with the highest confidence ($\text{argmax}$), maps it to human-readable labels, and retrieves disposal guidelines, bin color codes, and environmental facts from `recommendations.json`.

---

### 2. Common Viva Questions & Model Answers

#### Q1: Why did you choose MobileNetV2 instead of heavier models like VGG16 or ResNet50?
> **Answer**:  
> VGG16 has approximately 138 million parameters and ResNet50 has 25 million, which requires heavy computation and slow inference times. MobileNetV2 has only ~3.4 million parameters because it utilizes **Depthwise Separable Convolutions** and **Inverted Residual Blocks** with linear bottlenecks. This makes MobileNetV2 over 40 times smaller, extremely fast for web and mobile deployment, and energy-efficient while maintaining high classification accuracy.

#### Q2: What is Transfer Learning and why did you use it here?
> **Answer**:  
> Training a deep Convolutional Neural Network from scratch requires hundreds of thousands of labeled images and days of compute. Transfer Learning allows us to reuse the visual features (such as edges, textures, shapes, and material reflections) learned by MobileNetV2 on the large **ImageNet** dataset (1.4 million images). We kept the pre-trained feature extractor frozen, trained a custom dense classification head on our 1,647 waste images, and then fine-tuned the top layers with a small learning rate ($1 \times 10^{-5}$) to specialize in waste textures.

#### Q3: How did you ensure there was no Data Leakage?
> **Answer**:  
> We divided the dataset physically into three distinct splits before any model training: 70% Training, 15% Validation, and 15% Testing. Data augmentation (random rotation, zoom, flips) was applied **only** to the training split. The test split was kept completely untouched and was only evaluated once at the very end to measure true real-world generalization performance.

#### Q4: How does the live camera capture work in the browser?
> **Answer**:  
> We used HTML5 and the browser's native **WebRTC MediaDevices API** (`navigator.mediaDevices.getUserMedia`). When the user clicks 'Capture', a snapshot of the live `<video>` feed is drawn onto an HTML5 `<canvas>`, converted into a compressed JPEG Blob via `canvas.toBlob()`, wrapped in a standard `FormData` object, and transmitted asynchronously via AJAX `fetch()` to Flask's `/predict` route.

#### Q5: What happens if an image is submitted before the model is trained?
> **Answer**:  
> The backend follows strict academic integrity: it checks if the model file exists on disk. If not, it returns HTTP 400 with `model_ready: False` and a transparent message instructing the user to complete the Google Colab training. It strictly refuses to display random guesses or fake confidence numbers.

---

## 💡 Troubleshooting & FAQs

- **Port 5000 already in use**:
  Change `port=5000` to `port=5050` at the bottom of `app.py`, then open `http://127.0.0.1:5050`.
- **Camera not opening**:
  Ensure camera permissions are allowed in your browser settings. In modern browsers, camera access is permitted on `localhost` / `127.0.0.1`.
- **Model not recognized after Colab download**:
  Ensure the downloaded file is named `waste_mobilenetv2.keras` and placed directly inside the `model/` folder (`AI project/model/waste_mobilenetv2.keras`).

---

## 📜 License & Disclaimers

Waste segregation suggestions provided by this application are intended for general educational and civic awareness. Please check with your local municipality or regional waste authority for specific sorting guidelines.
