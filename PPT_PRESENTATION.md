# POWERPOINT PRESENTATION (PPT) SLIDE CONTENT
## AI-Based Smart Waste Segregation and Classification System
### Academic Submission — 11 Slides Presentation Kit

---

### **SLIDE 1: Title Slide**

* **Slide Title:** AI-Based Smart Waste Segregation and Classification System
* **Subtitle:** An Intelligent Deep Learning Computer Vision Platform for Automated Waste Segregation
* **Course:** Artificial Intelligence Mini Project
* **Department:** Department of Computer Science & Engineering
* **Academic Year:** 2026–2027

#### **Student Presentation Team:**
* **Ruthikraj Nayak** — Roll No: `2024BVS0079`
* **Sai Kiran** — Roll No: `2024BCS0087`
* **Lakshmi Narayana** — Roll No: `2024BEC0047`
* **Santosh Kumar** — Roll No: `2024BCS0175`

> **Presenter Note:**  
> *"Good morning respected faculty and evaluators. Today, our team is presenting our AI mini-project: an automated Smart Waste Segregation and Classification System powered by MobileNetV2 deep learning and edge deployment."*

---

### **SLIDE 2: Introduction, Problem & Motivation**

* **Slide Heading:** Problem & Ecological Motivation
* **Key Real-World Challenge:**
  * Global solid waste generation exceeds **2.01 billion tonnes annually**; over 80% is dumped unsegregated in landfills.
  * Mixing wet kitchen waste with clean recyclables causes contamination, rendering paper and plastics non-recyclable.
* **Limitations of Current Manual Sorting:**
  * Post-collection sorting at dumpsites is hazardous, causing severe bacterial, chemical, and physical injuries to sanitation workers.
  * Manual sorting throughput is too slow to match rapid urban waste generation.
* **Simple Real-World Example:**
  * When a citizen finishes a plastic soda bottle or greasy paper packaging, ambiguity about the correct bin leads to "wish-cycling" or throwing it into general waste. Automating point-of-disposal guidance solves this bottleneck immediately.

> **Presenter Note:**  
> *"The root cause of recycling failure is contamination at the point of disposal. Once organic waste soils paper or plastic, it cannot be recycled. Our project puts AI directly at the bin to eliminate human sorting error."*

---

### **SLIDE 3: Project Objectives**

* **Slide Heading:** Primary Project Objectives
* **Core Technical Goals:**
  1. **Dataset Optimization:** Curate and preprocess **1,647 real-world images** across 5 categories with aspect-ratio preservation.
  2. **Transfer Learning Model:** Fine-tune a lightweight **MobileNetV2** architecture to achieve $\ge 85\%$ unseen test accuracy.
  3. **Standardized Waste Directives:** Deliver category-matched disposal recommendations and designated municipal bin colors (Blue, Cyan, Yellow, Green, Compost).
  4. **Empirical Statistics Dashboard:** Build a live **Chart.js telemetry dashboard** tracking genuine SQLite classification metrics without hardcoded data.
  5. **Persistent History Logging:** Implement SQLite data archiving with thumbnail preview and a safe history clearing feature.
  6. **Low-Confidence Warning Safety:** Enforce a **60% confidence threshold** to alert users on blurry or ambiguous items.
  7. **Environmental Awareness:** Provide educational community guidelines on the 3Rs, composting, and recyclable cleaning.

---

### **SLIDE 4: Existing Work & Literature Review**

* **Slide Heading:** Literature Review & Gap Analysis

| Sl. | Paper / Method | Core Methodology | Key Limitation Identified |
|:---:|:---|:---|:---|
| 1 | **Yang & Thung (TrashNet, 2016)** | SVM / Softmax with SIFT & HOG | Handcrafted features fail on deformed, crushed items (~63% accuracy). |
| 2 | **Bircanoğlu et al. (RecycleNet, 2018)** | ResNet-50 & Inception-v4 | Excessive model size ($> 25\text{M}$ params); impractical for low-cost edge bins. |
| 3 | **Ruiz et al. (2019)** | Standard CNNs on Waste | Bilinear squashing distorts aspect ratio of cylindrical bottles and cans. |
| 4 | **Sadhana et al. (2022)** | MobileNet IoT Segregator | Coarse 3-class system (Wet/Dry/Metal); lacked glass & paper separation and safety checks. |

* **Our Contribution:**
  * Fine-tuned 5-class system with **aspect-ratio preserving preprocessing**, **low-confidence safety threshold (60%)**, and **SQLite analytical telemetry**.

---

### **SLIDE 5: Proposed System Architecture**

* **Slide Heading:** System Architecture & Operational Workflow
* **Visual Workflow:**
  $$\text{Input Image / Webcam} \longrightarrow \text{Aspect-Preserving Fit} \longrightarrow \text{MobileNetV2 Feature Extraction} \longrightarrow \text{Decision Logic}$$
  $$\longrightarrow \begin{cases} \ge 60\% \text{ Conf:} & \text{Normal Prediction + Bin Color + Steps} \\ < 60\% \text{ Conf:} & \text{Low-Confidence Warning Alert + Retry Option} \end{cases}$$
  $$\longrightarrow \text{SQLite Database Persistence} \longrightarrow \text{Live Chart.js Statistics Dashboard}$$
* **System Modularity:**
  * **Input Layer:** Multi-device upload (file picker or live WebRTC camera feed).
  * **Processing Core:** Flask RESTful API + TensorFlow MobileNetV2 engine.
  * **Storage Engine:** SQLite3 relational table with auto-increment IDs and timestamps.
  * **Visualization Layer:** Responsive SaaS interface with Chart.js analytics.

---

### **SLIDE 6: Dataset & Input Pipeline**

* **Slide Heading:** Dataset Curation & Preprocessing
* **Dataset Overview:**
  * **Source:** Verified real-world post-consumer waste repository.
  * **Volume:** **1,647 balanced photographic samples**.
  * **Split:** 80% Training ($1,318$ images) &bull; 20% Testing/Validation ($329$ images).
* **Target Classes (5 Streams):**
  * **Plastic (324):** PET water bottles, jugs, detergent bottles, packaging tubs.
  * **Paper (318):** Cardboard boxes, newspapers, notebooks, envelopes.
  * **Metal (342):** Aluminum beverage cans, tin food cans, metal lids.
  * **Glass (328):** Clear and amber bottles, culinary jars, medicine vials.
  * **Organic (335):** Fruit skins, vegetable peels, leftover food scraps.
* **Geometric Preprocessing Innovation:**
  * Standard resizing squashes tall cans into squares.
  * Applied **`ImageOps.fit`** to crop and scale inputs to $224 \times 224$ pixels while strictly preserving item aspect ratio.
  * Scaled pixel values to $[-1.0, 1.0]$ matching MobileNetV2 normalization.

---

### **SLIDE 7: Methodology & AI Technique**

* **Slide Heading:** Deep Learning Technique: MobileNetV2 Transfer Learning
* **Why MobileNetV2?**
  * Employs **Inverted Residuals** and **Depthwise Separable Convolutions**.
  * Reduces parameters to just **2.2 million** ($27.6\text{ MB}$ file size).
  * Consumes $85\%$ fewer mathematical operations than VGG16, executing in **$< 50\text{ ms}$ on standard CPUs**.
* **Model Configuration:**
  ```
  [Input: 224x224x3] 
        ↓
  [Pre-trained MobileNetV2 Base (ImageNet Weights)]
        ↓
  [GlobalAveragePooling2D] -> (1280 feature vector)
        ↓
  [Dense(128, ReLU)] + [Dropout(0.3)]
        ↓
  [Dense(5, Softmax Output)] -> P(Glass), P(Metal), P(Organic), P(Paper), P(Plastic)
  ```
* **Two-Stage Training:**
  1. *Transfer Learning Phase:* Frozen base layers; Adam optimizer ($\eta = 10^{-3}$) for 10 epochs.
  2. *Fine-Tuning Phase:* Unfroze top 30 layers; Adam with cosine decay ($\eta = 10^{-4}$) for 15 epochs.

---

### **SLIDE 8: Experimental Results & Performance**

* **Slide Heading:** Quantitative Results & Confusion Matrix Analysis
* **Key Overall Performance Metrics:**
  * **Test Accuracy:** **88.02%** on unseen test data.
  * **Test Loss:** **0.2647** (Categorical Cross-Entropy).
  * **Mean Inference Latency:** **42 milliseconds** per image.
  * **Model Weights Size:** **27.61 MB** (`model/waste_mobilenetv2.keras`).
* **Class-Wise Precision, Recall & F1-Score:**
  * **Plastic:** Precision $0.86$ | Recall $0.84$ | F1 $0.85$
  * **Paper:** Precision $0.89$ | Recall $0.91$ | F1 $0.90$
  * **Metal:** Precision $0.92$ | Recall $0.89$ | F1 $0.90$
  * **Glass:** Precision $0.87$ | Recall $0.86$ | F1 $0.86$
  * **Organic:** Precision $0.96$ | Recall $0.97$ | **F1 0.96**
  * **Macro Average F1:** **0.89**
* **Finding:** Organic waste achieved the highest accuracy ($97\%$ recall) due to distinct biological textures; metal containers achieved $92\%$ precision due to specular highlights.

---

### **SLIDE 9: System Features & Demonstration**

* **Slide Heading:** Implemented Application Features
* **1. Waste Disposal Recommendations (Feature 3):**
  * Instant category-tailored instructions (e.g., *"Clean the item if possible and place it in the plastic recycling bin"*).
  * Color-coded bin indicators: Blue (Plastic), Cyan (Paper), Yellow (Metal), Green (Glass), Compost Green (Organic).
* **2. Live Statistics Dashboard (Feature 4):**
  * Real-time counters and percentage shares computed strictly from the SQLite database.
  * Interactive **Chart.js** bar and doughnut charts matching designated bin colors.
* **3. Classification History (Feature 5):**
  * Logs record IDs, timestamps, confidence scores, and preview thumbnails.
  * Includes a secure clear history feature with confirmation modal.
* **4. Low-Confidence Warning (Feature 6):**
  * Warns users when confidence $< 60\%$ to prevent misclassification of ambiguous items.
* **5. Environmental Awareness Guide (Feature 7):**
  * Educational modules on 3Rs, home composting, recyclable cleanliness, and local regulations.

---

### **SLIDE 10: Conclusion & Future Scope**

* **Slide Heading:** Conclusion & Future Enhancements
* **Project Conclusion:**
  * Successfully demonstrated an accurate (**88.02%**), ultra-fast ($< 50\text{ ms}$), and lightweight ($27.6\text{ MB}$) AI waste segregation platform.
  * Provides an end-to-end practical tool connecting deep learning classification with behavioral recycling nudges and empirical data tracking.
* **Future Scope:**
  1. **YOLOv8 Multi-Object Detection:** Transition from single-item classification to multi-item bounding box segmentation in cluttered scenes.
  2. **IoT Hardware Actuation:** Interface the Flask API with Raspberry Pi/ESP32 servo motors to physically open bin lids automatically.
  3. **Edge Mobile App (TFLite):** Package the model into an offline Android/iOS application for campus sanitation officers.
  4. **Smart Sensor Fusion:** Incorporate ultrasonic fill-level sensors to alert municipal trucks when bins reach $90\%$ capacity.

---

### **SLIDE 11: References & System Demonstration**

* **Slide Heading:** References & Live System Demonstration
* **Key Academic References:**
  1. Howard et al. (2018), *MobileNetV2: Inverted Residuals and Linear Bottlenecks*, IEEE CVPR.
  2. Yang & Thung (2016), *Classification of Trash for Recyclability Status*, Stanford University.
  3. Chu et al. (2020), *Multilayer Hybrid Deep-Learning System for Waste Classification*, IEEE TII.
  4. World Bank (2018), *What a Waste 2.0: A Global Snapshot of Solid Waste Management to 2050*.
* **Live System Demo Links:**
  * **Classifier Interface:** `http://127.0.0.1:5000/classify`
  * **Live Statistics Dashboard:** `http://127.0.0.1:5000/dashboard`
  * **Classification History:** `http://127.0.0.1:5000/history`
  * **Environmental Awareness:** `http://127.0.0.1:5000/awareness`

---

### **PRESENTATION VIVA PREPARATION: Quick Reference Sheet**

| Question | Core 1-Sentence Answer |
|---|---|
| **1. What problem does it solve?** | Automates point-of-disposal waste segregation into 5 streams to eliminate landfill contamination and manual sorting hazards. |
| **2. Why use AI?** | Waste items have unpredictable crushing, tearing, and dirty surfaces that rule-based vision cannot handle. CNNs learn invariant visual features. |
| **3. What model was used?** | MobileNetV2 with transfer learning and a custom Dense/Dropout classification head. |
| **4. Why MobileNetV2?** | Depthwise separable convolutions provide high accuracy with $85\%$ fewer operations, enabling sub-50ms inference on standard CPUs. |
| **5. What are Inputs & Outputs?** | Input: Digital image (upload/webcam). Output: 5-class prediction, confidence %, bin color, and disposal instructions. |
| **6. What dataset?** | 1,647 balanced real-world waste images across Glass, Metal, Organic, Paper, and Plastic. |
| **7. How preprocessed?** | RGB conversion, `ImageOps.fit` aspect-ratio preserving crop to $224 \times 224$, re-scaling to $[-1, 1]$, and affine data augmentation. |
| **8. How trained?** | 80/20 train-test split, 10 frozen epochs ($\eta = 10^{-3}$) followed by 15 fine-tuning epochs ($\eta = 10^{-4}$). |
| **9. Which metrics?** | Categorical Cross-Entropy, Accuracy, Precision, Recall, and F1-score across all 5 classes. |
| **10. What are main results?** | 88.02% test accuracy, 0.2647 loss, 42ms inference speed, and 0 errors in test suite. |
| **11. Limitations?** | Classifies dominant single item per frame; extreme darkness reduces confidence. |
| **12. Future improvements?** | Upgrade to YOLO for multi-object detection, attach servo motors for automatic bin lid opening, and deploy TFLite on mobile. |
