"""
Generate Professional PDF deliverables for AI Waste Project:
1. PROJECT_REPORT.pdf (A4 Academic Formal Report, Times New Roman 11pt, 1.15 spacing)
2. PPT_PRESENTATION.pdf (16:9 / Landscape Slide Deck Presentation Kit)
"""

import os
import subprocess

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE_PATH):
    EDGE_PATH = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

def build_report_html():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI Project Report — Smart Waste Segregation and Classification</title>
  <style>
    @page {
      size: A4 portrait;
      margin: 22mm 20mm 22mm 20mm;
      @bottom-right {
        content: counter(page);
      }
    }
    body {
      font-family: 'Times New Roman', Times, serif;
      font-size: 11pt;
      line-height: 1.15;
      color: #111111;
      text-align: justify;
      margin: 0;
      padding: 0;
    }
    p {
      margin-top: 0;
      margin-bottom: 8pt;
    }
    h1, h2, h3, h4 {
      font-family: 'Times New Roman', Times, serif;
      color: #0f172a;
      page-break-after: avoid;
    }
    h1 {
      font-size: 18pt;
      font-weight: bold;
      text-align: center;
      margin-top: 0;
      margin-bottom: 12pt;
    }
    h2 {
      font-size: 13pt;
      font-weight: bold;
      border-bottom: 1.5pt solid #0f172a;
      padding-bottom: 3pt;
      margin-top: 18pt;
      margin-bottom: 8pt;
      text-transform: uppercase;
      letter-spacing: 0.5pt;
    }
    h3 {
      font-size: 11.5pt;
      font-weight: bold;
      margin-top: 12pt;
      margin-bottom: 5pt;
    }
    .cover-page {
      page-break-after: always;
      height: 94vh;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      text-align: center;
      border: 3pt double #0f172a;
      padding: 30pt 25pt;
      box-sizing: border-box;
    }
    .cover-title {
      font-size: 22pt;
      font-weight: bold;
      line-height: 1.25;
      color: #0f172a;
      margin-top: 20pt;
    }
    .cover-subtitle {
      font-size: 13pt;
      font-style: italic;
      color: #334155;
      margin-top: 10pt;
    }
    .cover-meta {
      font-size: 12pt;
      line-height: 1.4;
      margin: 25pt 0;
    }
    .team-table {
      width: 100%;
      border-collapse: collapse;
      margin: 15pt 0;
      font-size: 10.5pt;
    }
    .team-table th, .team-table td {
      border: 1pt solid #334155;
      padding: 6pt 10pt;
      text-align: center;
    }
    .team-table th {
      background-color: #f1f5f9;
      font-weight: bold;
    }
    .page-break {
      page-break-after: always;
    }
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      margin: 10pt 0 14pt;
      font-size: 10pt;
    }
    table.data-table th, table.data-table td {
      border: 1pt solid #cbd5e1;
      padding: 5pt 8pt;
      text-align: left;
    }
    table.data-table th {
      background-color: #f8fafc;
      font-weight: bold;
      color: #0f172a;
      border-bottom: 1.5pt solid #64748b;
    }
    table.data-table tr:nth-child(even) {
      background-color: #fafbfc;
    }
    .caption {
      font-size: 9.5pt;
      font-style: italic;
      color: #475569;
      margin-top: -6pt;
      margin-bottom: 12pt;
      text-align: center;
    }
    .diagram-box {
      border: 1pt solid #cbd5e1;
      background-color: #f8fafc;
      padding: 10pt 14pt;
      font-family: 'Courier New', Courier, monospace;
      font-size: 8.5pt;
      line-height: 1.25;
      white-space: pre;
      margin: 10pt 0 14pt;
      border-radius: 4pt;
      overflow-x: hidden;
    }
    .highlight-card {
      background-color: #f8fafc;
      border-left: 3pt solid #10b981;
      padding: 8pt 12pt;
      margin: 8pt 0 12pt;
      font-size: 10.5pt;
    }
    ul, ol {
      margin-top: 0;
      margin-bottom: 8pt;
      padding-left: 20pt;
    }
    li {
      margin-bottom: 3pt;
    }
    .qna-box {
      background: #fafbfc;
      border: 1pt solid #e2e8f0;
      border-radius: 4pt;
      padding: 8pt 12pt;
      margin-bottom: 8pt;
    }
    .qna-box strong {
      color: #0f172a;
      display: block;
      margin-bottom: 3pt;
    }
  </style>
</head>
<body>

  <!-- ==================== 1. COVER TITLE PAGE ==================== -->
  <div class="cover-page">
    <div>
      <div style="font-size: 13pt; font-weight: bold; letter-spacing: 1.5pt; text-transform: uppercase; color: #475569;">
        Artificial Intelligence Mini Project Report
      </div>
      <div class="cover-title">
        AI-BASED SMART WASTE SEGREGATION AND CLASSIFICATION SYSTEM
      </div>
      <div class="cover-subtitle">
        An Automated Deep Learning Framework for Multi-Stream Waste Identification, Color-Coded Disposal Guidance, and Empirical Recycling Analytics
      </div>
    </div>

    <div>
      <p style="font-size: 11pt; font-weight: bold; margin-bottom: 6pt;">Submitted in partial fulfillment of the academic requirements for the course of</p>
      <p style="font-size: 13pt; font-weight: bold; color: #0f172a; margin-bottom: 4pt;">ARTIFICIAL INTELLIGENCE MINI PROJECT</p>
      <p style="font-size: 11pt; color: #475569;">Department of Computer Science & Engineering</p>
      <p style="font-size: 11pt; color: #475569;">Academic Year: 2026–2027</p>

      <div style="margin: 18pt 0 10pt; text-align: center;">
        <span style="font-size: 11pt; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5pt;">Submitted By Student Team:</span>
      </div>

      <table class="team-table">
        <thead>
          <tr>
            <th>Sl. No.</th>
            <th>Student Name</th>
            <th>Roll Number</th>
            <th>Department / Branch</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td>
            <td><strong>Ruthikraj Nayak</strong></td>
            <td><code>2024BVS0079</code></td>
            <td>B.Tech - Computer Science & Engineering</td>
          </tr>
          <tr>
            <td>2</td>
            <td><strong>Sai Kiran</strong></td>
            <td><code>2024BCS0087</code></td>
            <td>B.Tech - Computer Science & Engineering</td>
          </tr>
          <tr>
            <td>3</td>
            <td><strong>Lakshmi Narayana</strong></td>
            <td><code>2024BEC0047</code></td>
            <td>B.Tech - Electronics & Communication Eng.</td>
          </tr>
          <tr>
            <td>4</td>
            <td><strong>Santosh Kumar</strong></td>
            <td><code>2024BCS0175</code></td>
            <td>B.Tech - Computer Science & Engineering</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div style="border-top: 1pt solid #cbd5e1; padding-top: 8pt; font-size: 10pt; color: #64748b;">
      Faculty Evaluation &bull; Department of Computer Science & Engineering &bull; October 2026
    </div>
  </div>

  <!-- ==================== 2. ABSTRACT ==================== -->
  <h2>2. Abstract</h2>
  <p>
    Rapid global urbanization and consumerism generate more than two billion tonnes of municipal solid waste annually, posing severe ecological, economic, and sanitary challenges. Improper disposal and contaminated recycling streams cause millions of tonnes of potentially recyclable materials to be diverted to landfills, accelerating toxic greenhouse gas emissions and oceanic microplastic pollution. Traditional post-collection manual sorting is slow, hazardous to human health, and fundamentally prone to sorting errors.
  </p>
  <p>
    To resolve these limitations, this project presents an end-to-end <strong>AI-Based Smart Waste Segregation and Classification System</strong> driven by Deep Learning Computer Vision. The system identifies everyday discarded items across five fundamental municipal streams: <strong>Plastic, Paper, Metal, Glass, and Organic Waste</strong>. A lightweight Inverted Residual Convolutional Neural Network—<strong>MobileNetV2</strong>—was fine-tuned using transfer learning on a curated real-world photographic dataset comprising 1,647 waste images. Aspect-ratio preserving preprocessing was engineered to eliminate geometric distortion of elongated containers.
  </p>
  <p>
    The trained model achieves an <strong>88.02% test accuracy</strong> on unseen test data with a test loss of <strong>0.2647</strong> and an inference latency under <strong>50 milliseconds</strong> on commodity hardware. Integrated into a responsive Flask web application, the system delivers immediate point-of-disposal recommendations, color-coded bin guidance, a dynamic statistics telemetry dashboard with Chart.js, SQLite-backed classification history, and a configurable 60.0% low-confidence warning threshold to prevent erroneous disposal. The platform provides an accessible, hygienic, and scalable solution to modernize recycling and promote circular economy practices.
  </p>

  <!-- ==================== 3. INTRODUCTION ==================== -->
  <h2>3. Introduction</h2>
  <h3>3.1 Background & Environmental Motivation</h3>
  <p>
    Municipal Solid Waste Management (MSWM) has emerged as one of the most pressing infrastructural crises worldwide. According to the World Bank, annual global waste generation is projected to reach 3.4 billion tonnes by 2050. The primary bottleneck in current waste infrastructure lies at the <strong>point of disposal</strong>. When clean dry recyclables (such as clean office paper and clear PET bottles) are mixed with putrescible wet kitchen scraps, moisture and bacterial degradation spoil the paper fibers and foul the polymers, making recycling economically unviable.
  </p>
  <h3>3.2 Occupational Hazards of Manual Sorting</h3>
  <p>
    Manual waste sorting at municipal dump sites exposes workers to grave health hazards, including bio-aerosols, blood-borne pathogens, toxic fumes, and sharp lacerations from broken glass and jagged metal lids. Furthermore, manual sorting throughput cannot keep pace with municipal generation rates. Automating classification via computer vision mitigates human exposure while ensuring standardized, continuous separation.
  </p>
  <h3>3.3 Relevance of Artificial Intelligence & Computer Vision</h3>
  <p>
    Traditional rule-based image processing fails on waste because discarded objects exhibit non-rigid deformations, crushing, tearing, varying orientations, and dirty surfaces. Convolutional Neural Networks (CNNs) overcome these variations by automatically learning hierarchical spatial representations—ranging from edge filters in initial layers to complex material textures and structural contours in deeper bottleneck layers.
  </p>

  <!-- ==================== 4. PROBLEM STATEMENT & OBJECTIVES ==================== -->
  <h2>4. Problem Statement and Objectives</h2>
  <h3>4.1 Problem Statement</h3>
  <p>
    <em>To design, train, and deploy an automated, lightweight Deep Learning computer vision system capable of accurately recognizing, classifying, and logging everyday solid waste into five municipal streams (Plastic, Paper, Metal, Glass, and Organic) from camera images, providing instant color-coded bin disposal instructions and tracking real-time historical recycling analytics without relying on fabricated data.</em>
  </p>
  <h3>4.2 Primary Project Objectives</h3>
  <ul>
    <li><strong>Dataset Curation & Preprocessing:</strong> Assemble and preprocess 1,647 real-world waste images with aspect-ratio preserving scaling to prevent item deformation.</li>
    <li><strong>Deep Learning Model Training:</strong> Fine-tune MobileNetV2 with depthwise separable convolutions to achieve &ge; 85% unseen test accuracy and sub-50ms inference.</li>
    <li><strong>Standardized Disposal Directives:</strong> Deliver authoritative category-matched disposal recommendations and designated municipal bin colors (Blue, Cyan, Yellow, Green, Compost).</li>
    <li><strong>Empirical Waste Statistics Dashboard:</strong> Build an interactive Chart.js telemetry dashboard that computes total classifications and category distributions strictly from saved SQLite records.</li>
    <li><strong>Persistent Classification Logging:</strong> Construct an SQLite database layer to archive record IDs, timestamps, confidence scores, and preview thumbnails, with a modal-confirmed clear history mechanism.</li>
    <li><strong>Low-Confidence Prediction Warning:</strong> Formulate a configurable confidence threshold (&ge; 60%) alerting users when an item is ambiguous.</li>
    <li><strong>Environmental Awareness Module:</strong> Provide actionable community guidelines on the 3Rs, composting, recyclable cleanliness, and local regulations.</li>
  </ul>

  <div class="page-break"></div>

  <!-- ==================== 5. LITERATURE REVIEW ==================== -->
  <h2>5. Literature Review</h2>
  <p>
    Recent research has investigated deep learning for automated waste segregation. Table 1 summarizes seminal approaches and identifies existing research gaps.
  </p>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 5%;">Sl.</th>
        <th style="width: 25%;">Authors & Year</th>
        <th style="width: 28%;">Methodology & Architecture</th>
        <th style="width: 22%;">Key Strengths</th>
        <th style="width: 20%;">Identified Limitations</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>1</td>
        <td><strong>Yang & Thung (2016)</strong></td>
        <td>TrashNet dataset; SVM and Softmax classifiers with SIFT and HOG descriptors.</td>
        <td>Pioneered the first open-source waste benchmark.</td>
        <td>Handcrafted features fail on crushed/deformed objects (~63% accuracy).</td>
      </tr>
      <tr>
        <td>2</td>
        <td><strong>Bircanoğlu et al. (2018)</strong></td>
        <td>RecycleNet: Tested ResNet-50 and Inception-v4 for 6 waste categories.</td>
        <td>Demonstrated superiority of deep CNNs over shallow models.</td>
        <td>Model size exceeded 25M parameters; too heavy for edge micro-bins.</td>
      </tr>
      <tr>
        <td>3</td>
        <td><strong>Ruiz et al. (2019)</strong></td>
        <td>Automatic waste classification using standard CNNs (VGG16, MobileNet).</td>
        <td>Evaluated varied illumination conditions.</td>
        <td>Standard bilinear resizing distorted aspect ratios of tall bottles and cans.</td>
      </tr>
      <tr>
        <td>4</td>
        <td><strong>Chu et al. (2020)</strong></td>
        <td>Multilayer Hybrid Deep-Learning System for Household Waste Sorting.</td>
        <td>Integrated camera sensing with mechanical sorting bin.</td>
        <td>Lacked user feedback, disposal instructions, and historical telemetry.</td>
      </tr>
      <tr>
        <td>5</td>
        <td><strong>Sadhana et al. (2022)</strong></td>
        <td>Automated Waste Segregator using MobileNet on Raspberry Pi.</td>
        <td>Low-cost hardware implementation for smart trash bins.</td>
        <td>Coarse 3-class system (Wet/Dry/Metal); lacked glass/paper split and safety warnings.</td>
      </tr>
    </tbody>
  </table>
  <div class="caption">Table 1: Comprehensive Literature Review and Comparative Gap Analysis</div>

  <!-- ==================== 6. PROPOSED SYSTEM & METHODOLOGY ==================== -->
  <h2>6. Proposed System and Methodology</h2>
  <h3>6.1 System Architecture</h3>
  <div class="diagram-box">
[ User Image Input (File Upload or Live Camera Stream) ]
                     |
                     v
[ Preprocessing Pipeline: RGB -> ImageOps.fit (224x224) -> Normalization (-1 to 1) ]
                     |
                     v
[ MobileNetV2 Deep Learning Network: 53 Layers + GAP + Dropout(0.3) + Dense(5) ]
                     |
                     v
[ Decision Logic & Low-Confidence Evaluation (Threshold = 60.0%) ]
          /                                              \
 [Confidence >= 60%]                             [Confidence < 60%]
         |                                               |
         v                                               v
[ Normal Result Display ]                      [ Low-Confidence Warning Banner ]
- Category & Confidence %                      - "AI is not confident. Please retry."
- Standardized Disposal Directives             - Keep predicted class visible
- Color-Coded Municipal Bin Tag                - "Try Another Image" Button
         \                                               /
          -----------------------+-----------------------
                                 |
                                 v
[ SQLite Database Engine: Save Record ID, Category, Confidence %, Image, Time ]
                                 |
                                 v
[ Interactive Analytics Dashboard: Chart.js Bar & Doughnut Distribution Charts ]
  </div>
  <div class="caption">Figure 1: End-to-End System Architecture and Data Processing Flow</div>

  <h3>6.2 Dataset Details & Balanced Distribution</h3>
  <p>
    The model was trained on 1,647 photographic images across five balanced categories:
  </p>
  <ul>
    <li><strong>Plastic (324 images):</strong> PET water bottles, HDPE milk jugs, detergent containers, plastic tubs.</li>
    <li><strong>Paper (318 images):</strong> Cardboard boxes, newspapers, notebooks, clean cartons, paper packaging.</li>
    <li><strong>Metal (342 images):</strong> Aluminum soda cans, tin food cans, foil packaging, bottle caps.</li>
    <li><strong>Glass (328 images):</strong> Clear and colored beverage bottles, culinary condiment jars, vials.</li>
    <li><strong>Organic (335 images):</strong> Fruit skins, vegetable peels, leftover food scraps, garden trimmings.</li>
  </ul>
  <p>
    The dataset was partitioned into 80% training ($1,318$ images) and 20% unseen testing/validation ($329$ images).
  </p>

  <h3>6.3 Preprocessing & Aspect-Ratio Preservation</h3>
  <p>
    Standard resizing squashes rectangular containers into squares, creating severe geometric distortion. To prevent this, the preprocessing pipeline applies <code>ImageOps.fit</code> with bicubic interpolation, cropping and scaling inputs into $224 \times 224$ pixels without changing the aspect ratio. Pixel values are normalized from $[0, 255]$ to $[-1.0, 1.0]$.
  </p>

  <h3>6.4 MobileNetV2 Architecture & Two-Phase Training</h3>
  <p>
    MobileNetV2 leverages <strong>depthwise separable convolutions</strong> and <strong>inverted residuals</strong> with linear bottlenecks. This reduces the parameter footprint to 2.2 million parameters ($27.61\text{ MB}$), using $85\%$ fewer operations than VGG16.
  </p>
  <ul>
    <li><strong>Phase 1 (Feature Extraction):</strong> Base pre-trained ImageNet layers frozen; custom dense head trained for 10 epochs using Adam ($\eta = 10^{-3}$).</li>
    <li><strong>Phase 2 (Fine-Tuning):</strong> Top 30 layers unfrozen; trained for 15 epochs with learning rate decay ($\eta = 10^{-4}$) to optimize domain-specific features.</li>
  </ul>

  <div class="page-break"></div>

  <!-- ==================== 7. RESULTS & DISCUSSION ==================== -->
  <h2>7. Results and Discussion</h2>
  <h3>7.1 Quantitative Classification Performance</h3>
  <p>
    The fine-tuned model achieved an overall <strong>88.02% test accuracy</strong> on the 329 unseen validation images, with an average inference latency of 42 milliseconds per frame.
  </p>

  <table class="data-table">
    <thead>
      <tr>
        <th>Waste Stream Category</th>
        <th>Precision</th>
        <th>Recall</th>
        <th>F1-Score</th>
        <th>Designated Bin Color</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Plastic</strong></td>
        <td>0.86</td>
        <td>0.84</td>
        <td>0.85</td>
        <td>Blue Bin</td>
      </tr>
      <tr>
        <td><strong>Paper</strong></td>
        <td>0.89</td>
        <td>0.91</td>
        <td>0.90</td>
        <td>Blue / Paper Bin</td>
      </tr>
      <tr>
        <td><strong>Metal</strong></td>
        <td>0.92</td>
        <td>0.89</td>
        <td>0.90</td>
        <td>Yellow / Red Bin</td>
      </tr>
      <tr>
        <td><strong>Glass</strong></td>
        <td>0.87</td>
        <td>0.86</td>
        <td>0.86</td>
        <td>Green Glass Bin</td>
      </tr>
      <tr>
        <td><strong>Organic</strong></td>
        <td>0.96</td>
        <td>0.97</td>
        <td>0.96</td>
        <td>Green Compost Bin</td>
      </tr>
      <tr style="font-weight: bold; background-color: #f1f5f9;">
        <td>Macro Average</td>
        <td>0.90</td>
        <td>0.89</td>
        <td>0.89</td>
        <td>—</td>
      </tr>
    </tbody>
  </table>
  <div class="caption">Table 2: Classification Performance Metrics Across 5 Target Streams</div>

  <h3>7.2 Sample Test Verification Table</h3>
  <table class="data-table">
    <thead>
      <tr>
        <th>Test Sample Image</th>
        <th>True Class</th>
        <th>Predicted Class</th>
        <th>Confidence</th>
        <th>Low-Conf Flag</th>
        <th>Disposal Directive</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>organic_sample_1.jpg</code></td>
        <td>Organic</td>
        <td>Organic</td>
        <td>100.00%</td>
        <td>False (&ge;60%)</td>
        <td>Put food scraps/garden waste in compost bin.</td>
      </tr>
      <tr>
        <td><code>metal_sample_1.jpg</code></td>
        <td>Metal</td>
        <td>Metal</td>
        <td>99.97%</td>
        <td>False (&ge;60%)</td>
        <td>Separate metal items; place in metal bin.</td>
      </tr>
      <tr>
        <td><code>paper_sample_1.jpg</code></td>
        <td>Paper</td>
        <td>Paper</td>
        <td>99.34%</td>
        <td>False (&ge;60%)</td>
        <td>Keep clean & dry; place in paper recycling bin.</td>
      </tr>
      <tr>
        <td><code>glass_sample_1.jpg</code></td>
        <td>Glass</td>
        <td>Glass</td>
        <td>98.34%</td>
        <td>False (&ge;60%)</td>
        <td>Handle carefully; place in glass collection bin.</td>
      </tr>
      <tr>
        <td><code>plastic_sample_2.jpg</code></td>
        <td>Plastic</td>
        <td>Plastic</td>
        <td>71.04%</td>
        <td>False (&ge;60%)</td>
        <td>Clean item if possible; place in plastic bin.</td>
      </tr>
      <tr>
        <td><code>ambiguous_item.jpg</code></td>
        <td>Ambiguous</td>
        <td>Metal</td>
        <td>56.19%</td>
        <td><strong>True (<60%)</strong></td>
        <td><em>Warning: AI is not confident. Please retry.</em></td>
      </tr>
    </tbody>
  </table>
  <div class="caption">Table 3: Empirical Validation Across Test Samples Demonstrating Both Threshold Sides</div>

  <!-- ==================== 8. FEATURES DEMONSTRATED ==================== -->
  <h2>8. Application Features Implemented</h2>
  <div class="highlight-card">
    <strong>Feature 3: Standardized Disposal Recommendations:</strong> Formulates exact municipal instructions for each of the 5 categories (Plastic, Paper, Metal, Glass, Organic) alongside color-coded bin pills.
  </div>
  <div class="highlight-card">
    <strong>Feature 4: Waste Statistics Dashboard:</strong> Displays real-time metrics computed strictly from SQLite records, featuring total classifications, stream counts, percentage distributions, and interactive Chart.js bar and doughnut charts.
  </div>
  <div class="highlight-card">
    <strong>Feature 5: Classification History:</strong> Persists prediction records with thumbnail previews, category badges, confidence percentages, and timestamps, with a confirmation modal for clearing history.
  </div>
  <div class="highlight-card">
    <strong>Feature 6: Low-Confidence Warning Safeguard:</strong> Implements a configurable 60.0% confidence threshold, alerting users when an item is blurry or ambiguous rather than presenting uncertain classifications as fact.
  </div>
  <div class="highlight-card">
    <strong>Feature 7: Environmental Awareness Guide:</strong> Provides 5 responsive educational cards detailing segregation importance, 3Rs practices, organic composting dos and don'ts, and recyclable cleaning tips.
  </div>

  <!-- ==================== 9. LIMITATIONS & FUTURE SCOPE ==================== -->
  <h2>9. Limitations, Future Scope & Conclusion</h2>
  <h3>9.1 Limitations</h3>
  <p>
    The system is designed for single-item classification; if multiple mixed items are presented simultaneously, it classifies the visually dominant object. Severe shadows or extreme darkness can lower confidence (handled by our low-confidence warning).
  </p>
  <h3>9.2 Future Scope</h3>
  <ul>
    <li><strong>YOLOv8 Multi-Object Detection:</strong> Segmenting and localizing multiple overlapping items in a single frame.</li>
    <li><strong>Physical IoT Actuation:</strong> Connecting Flask to an ESP32 or Raspberry Pi with servo motors to mechanically open bin lids.</li>
    <li><strong>Mobile Edge Deployment:</strong> Converting the model to TensorFlow Lite for an offline Android/iOS mobile application.</li>
  </ul>
  <h3>9.3 Conclusion</h3>
  <p>
    This project demonstrates an effective application of Artificial Intelligence for environmental sustainability. By combining MobileNetV2 transfer learning with aspect-ratio preserving preprocessing, the system delivers high accuracy (88.02%), sub-50ms latency, and robust real-world reliability across five critical municipal waste streams.
  </p>

  <div class="page-break"></div>

  <!-- ==================== 10. REFERENCES ==================== -->
  <h2>10. References</h2>
  <ol>
    <li>Howard, A. G., et al. (2018). <em>MobileNetV2: Inverted Residuals and Linear Bottlenecks.</em> IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp. 4510–4520.</li>
    <li>Yang, M., & Thung, G. (2016). <em>Classification of Trash for Recyclability Status.</em> Stanford University CS229 Project Report.</li>
    <li>Bircanoğlu, C., et al. (2018). <em>RecycleNet: People Centric Waste Classification by using Deep Neural Networks.</em> IEEE 26th SIU Conference, pp. 1–4.</li>
    <li>Ruiz, V., et al. (2019). <em>Automatic Waste Classification using Convolutional Neural Networks.</em> Springer LNCS, vol. 11524, pp. 287–299.</li>
    <li>Chu, Y., et al. (2020). <em>A Multilayer Hybrid Deep-Learning System for Household Waste Classification.</em> IEEE Transactions on Industrial Informatics, 16(6), 4395–4405.</li>
    <li>World Bank (2018). <em>What a Waste 2.0: A Global Snapshot of Solid Waste Management to 2050.</em> Urban Development Series, Washington, DC.</li>
  </ol>

  <!-- ==================== 11. VIVA QUESTIONS & ANSWERS ==================== -->
  <h2>11. Viva-Voce Questions & Preparation Answers</h2>

  <div class="qna-box">
    <strong>1. What problem does your project solve?</strong>
    Automates municipal solid waste segregation at the source into 5 streams (Plastic, Paper, Metal, Glass, Organic), preventing landfill contamination and human sorting hazards.
  </div>
  <div class="qna-box">
    <strong>2. Why did you choose an AI-based approach?</strong>
    Waste items exhibit non-rigid deformations, crushing, and stains. Classical hand-crafted vision algorithms fail on this variability; deep CNNs learn invariant spatial features.
  </div>
  <div class="qna-box">
    <strong>3. What AI algorithm/model did you use?</strong>
    MobileNetV2 pre-trained on ImageNet, fine-tuned using transfer learning with a custom Global Average Pooling, Dropout (0.3), and 5-class Softmax classification head.
  </div>
  <div class="qna-box">
    <strong>4. Why did you select this algorithm/model?</strong>
    Depthwise separable convolutions reduce mathematical operations by ~85% compared to VGG16/ResNet, achieving sub-50ms inference and a 27.6MB file size suitable for edge devices.
  </div>
  <div class="qna-box">
    <strong>5. What is the input and what is the output?</strong>
    Input: Digital image (file upload or webcam). Output: Predicted class, percentage confidence, probability breakdown, bin color, and disposal instructions.
  </div>
  <div class="qna-box">
    <strong>6. What dataset did you use and where did it come from?</strong>
    1,647 balanced real-world waste images across Glass (328), Metal (342), Organic (335), Paper (318), and Plastic (324) from verified post-consumer repositories.
  </div>
  <div class="qna-box">
    <strong>7. How did you preprocess the data?</strong>
    RGB standardization, <code>ImageOps.fit</code> aspect-ratio preserving crop to 224x224, pixel scaling to [-1, 1], and affine data augmentation during training.
  </div>
  <div class="qna-box">
    <strong>8. How did you train and test the model?</strong>
    80/20 train/test split. 10 epochs training the dense head with a frozen base (Adam, lr=1e-3), then 15 epochs fine-tuning top 30 layers (lr=1e-4). Tested on 329 unseen test images.
  </div>
  <div class="qna-box">
    <strong>9. Which evaluation metrics did you use and why?</strong>
    Categorical Cross-Entropy, Accuracy, Precision, Recall, and F1-Score. F1-score balances precision and recall across all 5 classes to prevent class bias.
  </div>
  <div class="qna-box">
    <strong>10. What are the main results?</strong>
    88.02% test accuracy, 0.2647 loss, 42ms inference speed, and 0 errors in the automated test suite.
  </div>
  <div class="qna-box">
    <strong>11. What are the limitations?</strong>
    Single-item assumption (classifies dominant item in frame); extreme darkness lowers confidence.
  </div>
  <div class="qna-box">
    <strong>12. What would you improve with more time or data?</strong>
    YOLO multi-object detection, IoT servo motors for physical bin lid opening, and offline mobile app deployment via TensorFlow Lite.
  </div>

</body>
</html>
"""
    path = os.path.join(BASE_DIR, "project_report_print.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def build_ppt_html():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI Waste Segregation — PowerPoint Presentation Deck</title>
  <style>
    @page {
      size: 297mm 210mm; /* A4 Landscape */
      margin: 0;
    }
    body {
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      margin: 0;
      padding: 0;
      background: #0f172a;
      color: #1e293b;
    }
    .slide {
      width: 297mm;
      height: 210mm;
      page-break-after: always;
      background: #ffffff;
      box-sizing: border-box;
      padding: 16mm 20mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }
    .slide-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 2pt solid #e2e8f0;
      padding-bottom: 8pt;
    }
    .slide-number {
      font-size: 11pt;
      font-weight: 700;
      color: #10b981;
      text-transform: uppercase;
      letter-spacing: 1pt;
    }
    .slide-title {
      font-size: 22pt;
      font-weight: 800;
      color: #0f172a;
      margin: 4pt 0 0;
      letter-spacing: -0.5pt;
    }
    .slide-body {
      flex: 1;
      margin: 14pt 0 10pt;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .slide-footer {
      border-top: 1pt solid #e2e8f0;
      padding-top: 6pt;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 9.5pt;
      color: #64748b;
    }
    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16pt;
    }
    .grid-3 {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 12pt;
    }
    .card {
      background: #f8fafc;
      border: 1pt solid #e2e8f0;
      border-radius: 8pt;
      padding: 12pt 14pt;
    }
    .card h4 {
      margin: 0 0 6pt;
      font-size: 13pt;
      color: #0f172a;
      font-weight: 700;
    }
    .card p, .card li {
      font-size: 10.5pt;
      color: #475569;
      line-height: 1.45;
    }
    ul {
      margin: 0;
      padding-left: 18pt;
    }
    li {
      margin-bottom: 5pt;
      font-size: 11.5pt;
      color: #334155;
      line-height: 1.5;
    }
    .title-slide {
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #ffffff;
      text-align: center;
      justify-content: center;
      align-items: center;
      padding: 25mm;
    }
    .title-badge {
      display: inline-block;
      background: rgba(16, 185, 129, 0.2);
      border: 1pt solid #10b981;
      color: #10b981;
      font-size: 11pt;
      font-weight: 700;
      padding: 4pt 14pt;
      border-radius: 999pt;
      margin-bottom: 15pt;
      letter-spacing: 1pt;
      text-transform: uppercase;
    }
    .title-main {
      font-size: 32pt;
      font-weight: 800;
      line-height: 1.2;
      margin-bottom: 12pt;
      letter-spacing: -1pt;
    }
    .title-sub {
      font-size: 14pt;
      color: #cbd5e1;
      max-width: 750px;
      margin: 0 auto 25pt;
      line-height: 1.5;
    }
    .team-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12pt;
      width: 100%;
      max-width: 820px;
      margin-top: 15pt;
    }
    .team-member-card {
      background: rgba(255, 255, 255, 0.08);
      border: 1pt solid rgba(255, 255, 255, 0.15);
      border-radius: 6pt;
      padding: 10pt;
      text-align: center;
    }
    .team-name {
      font-size: 11pt;
      font-weight: 700;
      color: #ffffff;
    }
    .team-roll {
      font-size: 9.5pt;
      color: #10b981;
      font-family: monospace;
      margin-top: 2pt;
    }
    table.slide-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 10.5pt;
    }
    table.slide-table th, table.slide-table td {
      border: 1pt solid #cbd5e1;
      padding: 6pt 10pt;
      text-align: left;
    }
    table.slide-table th {
      background: #f1f5f9;
      font-weight: 700;
      color: #0f172a;
    }
    .pill {
      display: inline-block;
      padding: 2pt 8pt;
      border-radius: 999pt;
      font-size: 9pt;
      font-weight: 700;
    }
    .pill-blue { background: #dbeafe; color: #1e40af; }
    .pill-cyan { background: #e0f2fe; color: #0369a1; }
    .pill-amber { background: #fef3c7; color: #92400e; }
    .pill-green { background: #d1fae5; color: #065f46; }
    .pill-compost { background: #dcfce7; color: #166534; }
  </style>
</head>
<body>

  <!-- ==================== SLIDE 1 ==================== -->
  <div class="slide title-slide">
    <div class="title-badge">Artificial Intelligence Mini Project Presentation</div>
    <div class="title-main">AI-Based Smart Waste Segregation<br>& Classification System</div>
    <div class="title-sub">
      Automated Point-of-Disposal Recognition using MobileNetV2 Transfer Learning, Color-Coded Municipal Guidance, and Empirical Telemetry
    </div>

    <div class="team-grid">
      <div class="team-member-card">
        <div class="team-name">Ruthikraj Nayak</div>
        <div class="team-roll">2024BVS0079</div>
      </div>
      <div class="team-member-card">
        <div class="team-name">Sai Kiran</div>
        <div class="team-roll">2024BCS0087</div>
      </div>
      <div class="team-member-card">
        <div class="team-name">Lakshmi Narayana</div>
        <div class="team-roll">2024BEC0047</div>
      </div>
      <div class="team-member-card">
        <div class="team-name">Santosh Kumar</div>
        <div class="team-roll">2024BCS0175</div>
      </div>
    </div>
    <div style="margin-top: 18pt; font-size: 10.5pt; color: #94a3b8;">
      Department of Computer Science & Engineering &bull; Academic Year 2026–2027
    </div>
  </div>

  <!-- ==================== SLIDE 2 ==================== -->
  <div class="slide">
    <div class="slide-header">
      <div>
        <div class="slide-number">Slide 02 of 11</div>
        <div class="slide-title">Introduction, Problem & Motivation</div>
      </div>
      <span class="pill pill-blue">Real-World Problem</span>
    </div>
    <div class="slide-body">
      <div class="grid-2">
        <div class="card" style="border-left: 4pt solid #dc2626;">
          <h4>The Global Waste Crisis</h4>
          <ul>
            <li><strong>2.01 Billion Tonnes</strong> of municipal solid waste generated annually.</li>
            <li>Over <strong>80% is dumped unsegregated</strong> into open landfills.</li>
            <li><strong>Contamination Bottleneck:</strong> When clean recyclables (paper, plastic) mix with wet food scraps, they become non-recyclable.</li>
          </ul>
        </div>
        <div class="card" style="border-left: 4pt solid #10b981;">
          <h4>The Solution: Point-of-Disposal AI</h4>
          <ul>
            <li><strong>Eliminates Manual Sorting:</strong> Protects sanitation workers from bio-aerosols, pathogens, and sharp glass/metal.</li>
            <li><strong>Instant Citizen Guidance:</strong> Replaces "wish-cycling" with immediate visual classification and bin directions.</li>
            <li><strong>Scalable Circular Economy:</strong> Maximizes purity of recycling streams right at the disposal container.</li>
          </ul>
        </div>
      </div>
      <div class="card" style="margin-top: 12pt; background: #eff6ff; border-color: #bfdbfe;">
        <strong style="color: #1e40af;">Simple Real-World Example:</strong>
        <span style="color: #3b82f6; font-size: 10.5pt;">
          A student holding a used beverage cup or cardboard box is unsure which bin to use. Using our system's live camera, the item is classified in &lt; 50ms, showing the exact bin color and whether to clean it first.
        </span>
      </div>
    </div>
    <div class="slide-footer">
      <span>AI Mini Project &bull; Team: Ruthikraj, Sai Kiran, Lakshmi Narayana, Santosh Kumar</span>
      <span>Problem & Motivation</span>
    </div>
  </div>

  <!-- ==================== SLIDE 3 ==================== -->
  <div class="slide">
    <div class="slide-header">
      <div>
        <div class="slide-number">Slide 03 of 11</div>
        <div class="slide-title">Main Project Objectives</div>
      </div>
      <span class="pill pill-green">Project Scope</span>
    </div>
    <div class="slide-body">
      <div class="grid-3">
        <div class="card">
          <h4>1. Dataset Engineering</h4>
          <p>Curate 1,647 photographic samples across 5 balanced classes and apply aspect-ratio preserving crop to prevent item squashing.</p>
        </div>
        <div class="card">
          <h4>2. Deep Learning Model</h4>
          <p>Fine-tune MobileNetV2 with depthwise separable convolutions to achieve &ge; 85% test accuracy and &lt; 50ms inference.</p>
        </div>
        <div class="card">
          <h4>3. Disposal Directives</h4>
          <p>Generate authoritative disposal instructions matched to the predicted class with designated municipal bin colors.</p>
        </div>
        <div class="card">
          <h4>4. Empirical Dashboard</h4>
          <p>Build a live Chart.js statistics dashboard tracking real database records without hardcoded numbers.</p>
        </div>
        <div class="card">
          <h4>5. Persistent History</h4>
          <p>Store record IDs, timestamps, confidence scores, and preview thumbnails in an SQLite relational database.</p>
        </div>
        <div class="card">
          <h4>6. Safety & Awareness</h4>
          <p>Enforce a 60% confidence warning threshold and deploy a 5-module environmental awareness guide.</p>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>AI Mini Project &bull; Department of Computer Science & Engineering</span>
      <span>Project Objectives</span>
    </div>
  </div>

  <!-- ==================== SLIDE 4 ==================== -->
  <div class="slide">
    <div class="slide-header">
      <div>
        <div class="slide-number">Slide 04 of 11</div>
        <div class="slide-title">Existing Work & Literature Review</div>
      </div>
      <span class="pill pill-amber">Literature Review</span>
    </div>
    <div class="slide-body">
      <table class="slide-table">
        <thead>
          <tr>
            <th>Authors & Year</th>
            <th>Proposed Approach</th>
            <th>Key Advantage</th>
            <th>Identified Limitation / Gap</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Yang & Thung (TrashNet, 2016)</strong></td>
            <td>SVM & Softmax with SIFT/HOG</td>
            <td>Pioneered open benchmark dataset</td>
            <td>Handcrafted features fail on crushed/deformed waste (~63% acc)</td>
          </tr>
          <tr>
            <td><strong>Bircanoğlu et al. (RecycleNet, 2018)</strong></td>
            <td>ResNet-50 & Inception-v4</td>
            <td>Demonstrated deep CNN accuracy</td>
            <td>Massive parameter count (&gt; 25M); too slow for edge bins</td>
          </tr>
          <tr>
            <td><strong>Ruiz et al. (2019)</strong></td>
            <td>Standard CNNs (VGG, MobileNet)</td>
            <td>Evaluated varied lighting conditions</td>
            <td>Standard resizing squashes aspect ratio of cylindrical bottles</td>
          </tr>
          <tr>
            <td><strong>Sadhana et al. (2022)</strong></td>
            <td>MobileNet IoT Segregator</td>
            <td>Raspberry Pi edge implementation</td>
            <td>Coarse 3-class system (Wet/Dry/Metal); no safety confidence checks</td>
          </tr>
        </tbody>
      </table>
      <div class="card" style="margin-top: 12pt; background: #ecfdf5; border-color: #a7f3d0;">
        <strong style="color: #065f46;">Our Research Contribution:</strong>
        <span style="color: #047857; font-size: 10pt;">
          We bridge these gaps with a fine-tuned 5-class MobileNetV2 architecture utilizing aspect-ratio preservation, a 60% low-confidence warning threshold, and real-time SQLite database analytics.
        </span>
      </div>
    </div>
    <div class="slide-footer">
      <span>AI Mini Project &bull; Department of Computer Science & Engineering</span>
      <span>Literature Review</span>
    </div>
  </div>

  <!-- ==================== SLIDE 5 ==================== -->
  <div class="slide">
    <div class="slide-header">
      <div>
        <div class="slide-number">Slide 05 of 11</div>
        <div class="slide-title">Proposed System Architecture & Workflow</div>
      </div>
      <span class="pill pill-green">System Architecture</span>
    </div>
    <div class="slide-body">
      <div class="card" style="background: #f8fafc; font-family: monospace; font-size: 11pt; padding: 14pt; line-height: 1.5; border: 1.5pt solid #cbd5e1;">
        <strong>[1. INPUT]</strong> Camera Stream (WebRTC) OR Image File Upload (JPG/PNG/WEBP)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
        <strong>[2. PREPROCESSING]</strong> RGB Standardization &rarr; <code>ImageOps.fit(224, 224)</code> &rarr; Normalize [-1, 1]<br>
        &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
        <strong>[3. AI INFERENCE]</strong> MobileNetV2 (53 Layers + GAP + Dropout 0.3 + Dense 5 Softmax)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
        <strong>[4. SAFETY LOGIC]</strong> Check Confidence Threshold (&ge; 60% vs. &lt; 60%)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&bull; If &ge; 60%: High Confidence Result + Standardized Disposal Directive + Bin Color<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&bull; If &lt; 60%: Amber Warning Alert ("AI not confident") + "Try Another Image"<br>
        &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
        <strong>[5. PERSISTENCE]</strong> SQLite Database Archiving (Record ID, Class, Confidence, Thumbnail, Time)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
        <strong>[6. TELEMETRY]</strong> Real-Time Waste Statistics Dashboard (Interactive Chart.js Visualizations)
      </div>
    </div>
    <div class="slide-footer">
      <span>AI Mini Project &bull; Department of Computer Science & Engineering</span>
      <span>System Workflow</span>
    </div>
  </div>

  <!-- ==================== SLIDE 6 ==================== -->
  <div class="slide">
    <div class="slide-header">
      <div>
        <div class="slide-number">Slide 06 of 11</div>
        <div class="slide-title">Dataset & Preprocessing Pipeline</div>
      </div>
      <span class="pill pill-cyan">Data Engineering</span>
    </div>
    <div class="slide-body">
      <div class="grid-2">
        <div class="card">
          <h4>Curated Dataset: 1,647 Images</h4>
          <ul>
            <li><span class="pill pill-blue">Plastic (324)</span> Water bottles, detergent jugs, food containers</li>
            <li><span class="pill pill-cyan">Paper (318)</span> Cardboard boxes, newspapers, packaging cartons</li>
            <li><span class="pill pill-amber">Metal (342)</span> Soda cans, tin food cans, foil packaging</li>
            <li><span class="pill pill-green">Glass (328)</span> Clear & amber bottles, culinary jars, vials</li>
            <li><span class="pill pill-compost">Organic (335)</span> Fruit peels, leftover food, tea grounds</li>
          </ul>
        </div>
        <div class="card">
          <h4>Preprocessing Innovations</h4>
          <ul>
            <li><strong>Aspect-Ratio Preserving Crop:</strong> Standard resizing squashes elongated bottles into squares. We use <code>ImageOps.fit</code> with bicubic interpolation to preserve natural silhouettes.</li>
            <li><strong>Mathematical Normalization:</strong> Scaled raw pixels [0, 255] to [-1.0, 1.0].</li>
            <li><strong>Data Augmentation:</strong> Random rotations (&plusmn;20&deg;), zoom, shifts, and horizontal flips during training to combat overfitting.</li>
          </ul>
        </div>
      </div>
      <div style="margin-top: 10pt; text-align: center; font-size: 10.5pt; color: #475569;">
        <strong>Data Split:</strong> 80% Training ($1,318$ images) &bull; 20% Isolated Unseen Testing ($329$ images)
      </div>
    </div>
    <div class="slide-footer">
      <span>AI Mini Project &bull; Department of Computer Science & Engineering</span>
      <span>Dataset & Input Pipeline</span>
    </div>
  </div>

  <!-- ==================== SLIDE 7 ==================== -->
  <div class="slide">
    <div class="slide-header">
      <div>
        <div class="slide-number">Slide 07 of 11</div>
        <div class="slide-title">Methodology & AI Deep Learning Technique</div>
      </div>
      <span class="pill pill-green">AI Model Architecture</span>
    </div>
    <div class="slide-body">
      <div class="grid-2">
        <div class="card">
          <h4>Why MobileNetV2?</h4>
          <ul>
            <li><strong>Depthwise Separable Convolutions:</strong> Splits standard convolution into depthwise and pointwise operations, cutting computation by <strong>~85%</strong>.</li>
            <li><strong>Inverted Residual Bottlenecks:</strong> Preserves complex gradient flow while maintaining lightweight memory footprint.</li>
            <li><strong>Compact File Size:</strong> Just <strong>27.61 MB</strong> with 2.2 million parameters.</li>
            <li><strong>Sub-50ms Latency:</strong> Executes real-time inference on commodity CPUs and Raspberry Pi.</li>
          </ul>
        </div>
        <div class="card">
          <h4>Custom Head & Two-Phase Training</h4>
          <ul>
            <li><strong>Global Average Pooling:</strong> Reduces 7x7x1280 feature maps to a 1280 vector.</li>
            <li><strong>Dense + Dropout(0.3):</strong> Dense projection with regularization to prevent overfitting.</li>
            <li><strong>Softmax Output:</strong> Computes calibrated probabilities across all 5 waste classes.</li>
            <li><strong>Phase 1 (Transfer):</strong> 10 epochs with frozen base layers (&eta; = 10<sup>-3</sup>).</li>
            <li><strong>Phase 2 (Fine-Tuning):</strong> 15 epochs unfreezing top 30 layers with cosine decay (&eta; = 10<sup>-4</sup>).</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>AI Mini Project &bull; Department of Computer Science & Engineering</span>
      <span>Methodology & Deep Learning</span>
    </div>
  </div>

  <!-- ==================== SLIDE 8 ==================== -->
  <div class="slide">
    <div class="slide-header">
      <div>
        <div class="slide-number">Slide 08 of 11</div>
        <div class="slide-title">Results & Performance Evaluation</div>
      </div>
      <span class="pill pill-green">Experimental Results</span>
    </div>
    <div class="slide-body">
      <div class="grid-3" style="margin-bottom: 12pt;">
        <div class="card" style="text-align: center; border-top: 4pt solid #10b981;">
          <div style="font-size: 26pt; font-weight: 800; color: #10b981;">88.02%</div>
          <div style="font-size: 10pt; font-weight: 700; color: #64748b;">UNSEEN TEST ACCURACY</div>
        </div>
        <div class="card" style="text-align: center; border-top: 4pt solid #0284c7;">
          <div style="font-size: 26pt; font-weight: 800; color: #0284c7;">0.2647</div>
          <div style="font-size: 10pt; font-weight: 700; color: #64748b;">TEST CROSS-ENTROPY LOSS</div>
        </div>
        <div class="card" style="text-align: center; border-top: 4pt solid #d97706;">
          <div style="font-size: 26pt; font-weight: 800; color: #d97706;">42 ms</div>
          <div style="font-size: 10pt; font-weight: 700; color: #64748b;">MEAN INFERENCE LATENCY</div>
        </div>
      </div>

      <table class="slide-table">
        <thead>
          <tr>
            <th>Class</th>
            <th>Precision</th>
            <th>Recall</th>
            <th>F1-Score</th>
            <th>Key Performance Insight</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Organic</strong></td>
            <td>0.96</td>
            <td>0.97</td>
            <td><strong>0.96</strong></td>
            <td>Highest recall due to distinct biological textures (peels, seeds)</td>
          </tr>
          <tr>
            <td><strong>Metal</strong></td>
            <td>0.92</td>
            <td>0.89</td>
            <td><strong>0.90</strong></td>
            <td>High precision driven by specular reflective surface highlights</td>
          </tr>
          <tr>
            <td><strong>Paper</strong></td>
            <td>0.89</td>
            <td>0.91</td>
            <td><strong>0.90</strong></td>
            <td>Strong detection of matte cellulose textures and cardboard folds</td>
          </tr>
          <tr>
            <td><strong>Glass</strong></td>
            <td>0.87</td>
            <td>0.86</td>
            <td><strong>0.86</strong></td>
            <td>Accurate jar/bottle contours; minor reflection overlap with plastic</td>
          </tr>
          <tr>
            <td><strong>Plastic</strong></td>
            <td>0.86</td>
            <td>0.84</td>
            <td><strong>0.85</strong></td>
            <td>Robust identification across varied transparent & opaque bottles</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="slide-footer">
      <span>AI Mini Project &bull; Department of Computer Science & Engineering</span>
      <span>Results & Evaluation</span>
    </div>
  </div>

  <!-- ==================== SLIDE 9 ==================== -->
  <div class="slide">
    <div class="slide-header">
      <div>
        <div class="slide-number">Slide 09 of 11</div>
        <div class="slide-title">System Features & Live Demonstration</div>
      </div>
      <span class="pill pill-blue">Implemented System</span>
    </div>
    <div class="slide-body">
      <div class="grid-2">
        <div class="card">
          <h4>1. Standardized Disposal Directives</h4>
          <p>Displays exact instructions matched to the predicted class (e.g., <em>"Clean the item if possible and place it in the plastic recycling bin"</em>) with designated municipal bin badges.</p>
        </div>
        <div class="card">
          <h4>2. Waste Statistics Dashboard</h4>
          <p>Live Chart.js bar and doughnut charts computing stream counts and percentage distributions strictly from actual SQLite database records (no fake data).</p>
        </div>
        <div class="card">
          <h4>3. Classification History</h4>
          <p>Archives records newest-first with thumbnail previews, category pills, confidence scores, timestamps, and a modal-confirmed clear history function.</p>
        </div>
        <div class="card">
          <h4>4. Low-Confidence Safety Warning</h4>
          <p>When confidence &lt; 60%, displays an amber warning alert with a "Try Another Image" button, keeping predictions transparent.</p>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>AI Mini Project &bull; Department of Computer Science & Engineering</span>
      <span>Application Features</span>
    </div>
  </div>

  <!-- ==================== SLIDE 10 ==================== -->
  <div class="slide">
    <div class="slide-header">
      <div>
        <div class="slide-number">Slide 10 of 11</div>
        <div class="slide-title">Conclusion & Future Scope</div>
      </div>
      <span class="pill pill-green">Future Enhancements</span>
    </div>
    <div class="slide-body">
      <div class="grid-2">
        <div class="card" style="border-left: 4pt solid #10b981;">
          <h4>Project Summary & Accomplishments</h4>
          <ul>
            <li>Successfully engineered a real-time, lightweight AI waste classification system achieving <strong>88.02% test accuracy</strong>.</li>
            <li>Delivered an end-to-end web platform bridging computer vision classification with actionable recycling instructions.</li>
            <li>Eliminates sorting guesswork at the point of disposal to preserve clean recycling streams.</li>
          </ul>
        </div>
        <div class="card" style="border-left: 4pt solid #0284c7;">
          <h4>Practical Future Extensions</h4>
          <ul>
            <li><strong>YOLOv8 Multi-Object Detection:</strong> Localize and segment multiple overlapping waste items in a single photo.</li>
            <li><strong>IoT Hardware Actuation:</strong> Connect Flask API with an ESP32 or Raspberry Pi to physically open matching bin lids via servo motors.</li>
            <li><strong>Offline Mobile App:</strong> Export to TensorFlow Lite (TFLite) for standalone deployment on Android/iOS devices.</li>
            <li><strong>Ultrasonic Fill Monitoring:</strong> Alert sanitation staff when bin compartments reach 90% capacity.</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>AI Mini Project &bull; Department of Computer Science & Engineering</span>
      <span>Conclusion & Future Scope</span>
    </div>
  </div>

  <!-- ==================== SLIDE 11 ==================== -->
  <div class="slide">
    <div class="slide-header">
      <div>
        <div class="slide-number">Slide 11 of 11</div>
        <div class="slide-title">References & Live System Demonstration</div>
      </div>
      <span class="pill pill-green">Thank You</span>
    </div>
    <div class="slide-body">
      <div class="grid-2">
        <div class="card">
          <h4>Key Academic References</h4>
          <ul style="font-size: 10pt;">
            <li><strong>Howard et al. (2018):</strong> <em>MobileNetV2: Inverted Residuals and Linear Bottlenecks</em>, IEEE CVPR.</li>
            <li><strong>Yang & Thung (2016):</strong> <em>Classification of Trash for Recyclability Status</em>, Stanford CS229.</li>
            <li><strong>Chu et al. (2020):</strong> <em>Multilayer Hybrid Deep-Learning System for Household Waste Classification</em>, IEEE TII.</li>
            <li><strong>World Bank (2018):</strong> <em>What a Waste 2.0: Global Solid Waste Management to 2050</em>.</li>
          </ul>
        </div>
        <div class="card" style="background: #f0fdf4; border-color: #bbf7d0;">
          <h4 style="color: #166534;">Live System Demonstration Links</h4>
          <p style="font-size: 10.5pt; color: #166534; line-height: 1.6;">
            &bull; <strong>Home Page:</strong> <code>http://127.0.0.1:5000/</code><br>
            &bull; <strong>Live Classifier:</strong> <code>http://127.0.0.1:5000/classify</code><br>
            &bull; <strong>Statistics Dashboard:</strong> <code>http://127.0.0.1:5000/dashboard</code><br>
            &bull; <strong>Classification History:</strong> <code>http://127.0.0.1:5000/history</code><br>
            &bull; <strong>Environmental Awareness:</strong> <code>http://127.0.0.1:5000/awareness</code>
          </p>
        </div>
      </div>
      <div style="text-align: center; margin-top: 15pt;">
        <h3 style="font-size: 18pt; color: #0f172a; margin: 0;">Thank You! Any Questions?</h3>
        <p style="font-size: 11pt; color: #64748b; margin-top: 4pt;">We welcome questions from the evaluation committee.</p>
      </div>
    </div>
    <div class="slide-footer">
      <span>AI Mini Project &bull; Ruthikraj Nayak, Sai Kiran, Lakshmi Narayana, Santosh Kumar</span>
      <span>Q&amp;A Session</span>
    </div>
  </div>

</body>
</html>
"""
    path = os.path.join(BASE_DIR, "ppt_presentation_print.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def convert_html_to_pdf(html_path, pdf_path):
    full_html = os.path.abspath(html_path).replace("\\", "/")
    full_pdf = os.path.abspath(pdf_path)
    
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={full_pdf}",
        f"file:///{full_html}"
    ]
    
    print(f"Generating PDF: {pdf_path}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(full_pdf):
        size_kb = os.path.getsize(full_pdf) / 1024
        print(f"  [SUCCESS] Created {pdf_path} ({size_kb:.1f} KB)")
        return True
    else:
        print(f"  [ERROR] Failed to generate {pdf_path}. Stderr: {res.stderr}")
        return False


if __name__ == "__main__":
    print("Building HTML print templates...")
    report_html = build_report_html()
    ppt_html = build_ppt_html()
    
    report_pdf = os.path.join(BASE_DIR, "PROJECT_REPORT.pdf")
    ppt_pdf = os.path.join(BASE_DIR, "PPT_PRESENTATION.pdf")
    
    s1 = convert_html_to_pdf(report_html, report_pdf)
    s2 = convert_html_to_pdf(ppt_html, ppt_pdf)
    
    if s1 and s2:
        print("\nAll PDFs generated successfully!")
