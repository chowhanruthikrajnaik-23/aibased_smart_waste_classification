/**
 * AI-Based Smart Waste Segregation and Classification System
 * Client-Side Application Script
 * 
 * Features:
 * - Drag & Drop / File Picker upload
 * - Instant image preview
 * - Webcam / Mobile camera live streaming & capture
 * - Sample image quick picker
 * - AJAX prediction handling with loading state
 * - Dynamic results rendering with confidence meter and disposal advice
 */

document.addEventListener("DOMContentLoaded", function () {
  // Elements
  const tabUpload = document.getElementById("tabUpload");
  const tabCamera = document.getElementById("tabCamera");
  const uploadArea = document.getElementById("uploadArea");
  const cameraArea = document.getElementById("cameraArea");
  const fileInput = document.getElementById("fileInput");
  const dropzone = document.getElementById("dropzone");
  const previewBox = document.getElementById("previewBox");
  const previewImage = document.getElementById("previewImage");
  const btnRemove = document.getElementById("btnRemove");
  const btnPredict = document.getElementById("btnPredict");

  // Camera Elements
  const cameraStream = document.getElementById("cameraStream");
  const btnCapture = document.getElementById("btnCapture");
  const btnRetake = document.getElementById("btnRetake");
  const captureCanvas = document.getElementById("captureCanvas");

  // Results & Feedback Elements
  const emptyState = document.getElementById("emptyState");
  const loadingBox = document.getElementById("loadingBox");
  const resultContent = document.getElementById("resultContent");
  const errorAlert = document.getElementById("errorAlert");
  const errorText = document.getElementById("errorText");

  // Result Fields
  const resCategory = document.getElementById("resCategory");
  const resConfidence = document.getElementById("resConfidence");
  const confidenceBar = document.getElementById("confidenceBar");
  const resBinColorBadge = document.getElementById("resBinColorBadge");
  const resBinName = document.getElementById("resBinName");
  const resRecyclableTag = document.getElementById("resRecyclableTag");
  const resSegregationSteps = document.getElementById("resSegregationSteps");
  const resEcoFact = document.getElementById("resEcoFact");
  const breakdownList = document.getElementById("breakdownList");
  const resDisposalInstructions = document.getElementById("resDisposalInstructions");
  const resCategoryIcon = document.getElementById("resCategoryIcon");
  const resIconBox = document.getElementById("resIconBox");
  const lowConfidenceWarning = document.getElementById("lowConfidenceWarning");
  const lowConfidenceText = document.getElementById("lowConfidenceText");
  const btnTryAnother = document.getElementById("btnTryAnother");

  // Current active file/blob to predict
  let currentImageBlob = null;
  let videoMediaStream = null;

  // ========================================================================
  // Tabs Navigation (File Upload vs Camera)
  // ========================================================================
  if (tabUpload && tabCamera) {
    tabUpload.addEventListener("click", () => {
      tabUpload.classList.add("active");
      tabCamera.classList.remove("active");
      uploadArea.style.display = "block";
      cameraArea.style.display = "none";
      stopCamera();
    });

    tabCamera.addEventListener("click", () => {
      tabCamera.classList.add("active");
      tabUpload.classList.remove("active");
      cameraArea.style.display = "flex";
      uploadArea.style.display = "none";
      startCamera();
    });
  }

  // ========================================================================
  // File Upload Handling
  // ========================================================================
  if (dropzone && fileInput) {
    dropzone.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (file) handleSelectedFile(file);
    });

    // Drag and Drop
    ["dragenter", "dragover"].forEach((eventName) => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.add("dragover");
      });
    });

    ["dragleave", "drop"].forEach((eventName) => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.remove("dragover");
      });
    });

    dropzone.addEventListener("drop", (e) => {
      const files = e.dataTransfer.files;
      if (files.length > 0) handleSelectedFile(files[0]);
    });
  }

  function handleSelectedFile(file) {
    if (!file.type.startsWith("image/")) {
      showError("Please select a valid image file (JPG, PNG, WEBP).");
      return;
    }

    currentImageBlob = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.src = e.target.result;
      previewBox.style.display = "block";
      dropzone.style.display = "none";
      btnPredict.disabled = false;
      hideError();
    };
    reader.readAsDataURL(file);
  }

  // Remove selected image
  if (btnRemove) {
    btnRemove.addEventListener("click", resetImageInput);
  }

  function resetImageInput() {
    currentImageBlob = null;
    if (fileInput) fileInput.value = "";
    previewImage.src = "";
    previewBox.style.display = "none";
    if (dropzone) dropzone.style.display = "block";
    btnPredict.disabled = true;
    hideError();
  }

  // ========================================================================
  // Camera Capture Feature (WebRTC)
  // ========================================================================
  async function startCamera() {
    hideError();
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      showError("Camera access is not supported by your browser or requires HTTPS.");
      return;
    }

    try {
      videoMediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment", width: { ideal: 640 }, height: { ideal: 480 } },
        audio: false
      });
      cameraStream.srcObject = videoMediaStream;
      btnCapture.style.display = "inline-flex";
      btnRetake.style.display = "none";
    } catch (err) {
      console.error("Camera access error:", err);
      showError("Unable to access camera. Please allow camera permissions in your browser.");
    }
  }

  function stopCamera() {
    if (videoMediaStream) {
      videoMediaStream.getTracks().forEach((track) => track.stop());
      videoMediaStream = null;
    }
  }

  if (btnCapture) {
    btnCapture.addEventListener("click", () => {
      if (!cameraStream.videoWidth) return;

      captureCanvas.width = cameraStream.videoWidth;
      captureCanvas.height = cameraStream.videoHeight;
      const ctx = captureCanvas.getContext("2d");
      ctx.drawImage(cameraStream, 0, 0, captureCanvas.width, captureCanvas.height);

      captureCanvas.toBlob((blob) => {
        currentImageBlob = blob;
        previewImage.src = captureCanvas.toDataURL("image/jpeg");
        previewBox.style.display = "block";
        btnPredict.disabled = false;
        btnCapture.style.display = "none";
        btnRetake.style.display = "inline-flex";
        stopCamera();
      }, "image/jpeg", 0.92);
    });
  }

  if (btnRetake) {
    btnRetake.addEventListener("click", () => {
      previewBox.style.display = "none";
      btnPredict.disabled = true;
      currentImageBlob = null;
      startCamera();
    });
  }

  // ========================================================================
  // Quick Sample Image Picker
  // ========================================================================
  const sampleChips = document.querySelectorAll(".chip-btn");
  sampleChips.forEach((chip) => {
    chip.addEventListener("click", async () => {
      const sampleFile = chip.dataset.sample;
      try {
        const response = await fetch(`/sample/${sampleFile}`);
        if (!response.ok) throw new Error("Could not load sample image.");
        const blob = await response.blob();
        handleSelectedFile(blob);

        // Switch to upload tab if on camera tab
        if (tabUpload && tabCamera && tabCamera.classList.contains("active")) {
          tabUpload.click();
        }
      } catch (err) {
        showError("Failed to load sample image: " + err.message);
      }
    });
  });

  // ========================================================================
  // Prediction Request
  // ========================================================================
  if (btnPredict) {
    btnPredict.addEventListener("click", async () => {
      if (!currentImageBlob) {
        showError("Please select or capture an image first.");
        return;
      }

      // Prepare UI states
      hideError();
      if (emptyState) emptyState.style.display = "none";
      if (resultContent) resultContent.style.display = "none";
      if (loadingBox) loadingBox.style.display = "block";
      btnPredict.disabled = true;

      const formData = new FormData();
      formData.append("image", currentImageBlob, "waste_image.jpg");

      try {
        const res = await fetch("/predict", {
          method: "POST",
          body: formData
        });

        const data = await res.json();
        if (loadingBox) loadingBox.style.display = "none";
        btnPredict.disabled = false;

        if (!res.ok || !data.success) {
          if (data.model_ready === false) {
            showModelAwaitingNotice(data.message);
          } else {
            showError(data.message || "An error occurred during prediction.");
          }
          return;
        }

        // Render prediction results
        renderResults(data);

      } catch (err) {
        console.error("Prediction fetch error:", err);
        if (loadingBox) loadingBox.style.display = "none";
        btnPredict.disabled = false;
        showError("Server communication error. Make sure the Flask app is running.");
      }
    });
  }

  // ========================================================================
  // Results Renderer
  // ========================================================================
  function renderResults(data) {
    const { category, confidence, breakdown, recommendation } = data;

    // Predicted Category
    if (resCategory) resCategory.textContent = category;
    if (resConfidence) resConfidence.textContent = `${confidence}% Confidence`;

    // Meter animation
    if (confidenceBar) {
      confidenceBar.style.width = "0%";
      setTimeout(() => {
        confidenceBar.style.width = `${confidence}%`;
      }, 50);
    }

    // Bin Details
    if (resBinName) resBinName.textContent = recommendation.bin_color_name || "Appropriate Bin";
    if (resBinColorBadge) {
      resBinColorBadge.style.backgroundColor = recommendation.bin_color || "#16a34a";
      resBinColorBadge.style.borderColor = recommendation.bin_color || "#16a34a";
    }

    // Recyclable Tag
    if (resRecyclableTag) {
      if (recommendation.recyclable) {
        resRecyclableTag.textContent = "Recyclable";
        resRecyclableTag.className = "recyclable-tag tag-yes";
      } else {
        resRecyclableTag.textContent = "Non-Recyclable";
        resRecyclableTag.className = "recyclable-tag tag-no";
      }
    }

    // Segregation Steps
    if (resSegregationSteps) {
      resSegregationSteps.innerHTML = "";
      if (recommendation.segregation_steps && recommendation.segregation_steps.length > 0) {
        recommendation.segregation_steps.forEach((step) => {
          const li = document.createElement("li");
          li.textContent = step;
          resSegregationSteps.appendChild(li);
        });
      }
    }

    // Environmental Fact
    if (resEcoFact) {
      resEcoFact.textContent = recommendation.environmental_fact || "";
    }

    // Probabilities Breakdown
    if (breakdownList && breakdown && breakdown.length > 0) {
      breakdownList.innerHTML = "";
      breakdown.forEach((item) => {
        const row = document.createElement("div");
        row.className = "breakdown-row";
        row.innerHTML = `
          <div class="breakdown-label">${item.class_name}</div>
          <div class="breakdown-track">
            <div class="breakdown-fill" style="width: ${item.probability}%; background-color: ${item.class_name === category ? (recommendation.bin_color || '#16a34a') : '#cbd5e1'};"></div>
          </div>
          <div class="breakdown-percentage">${item.probability}%</div>
        `;
        breakdownList.appendChild(row);
      });
    }

    // Feature 3: Standardized Disposal Instructions
    if (resDisposalInstructions) {
      resDisposalInstructions.textContent = recommendation.disposal_instructions || "";
    }

    // Category Icon
    if (resCategoryIcon && recommendation.icon) {
      resCategoryIcon.className = `fa-solid ${recommendation.icon}`;
    }
    if (resIconBox && recommendation.bin_color) {
      resIconBox.style.color = recommendation.bin_color;
      resIconBox.style.backgroundColor = `${recommendation.bin_color}18`;
    }

    // Feature 6: Low-Confidence Prediction Warning
    if (lowConfidenceWarning) {
      if (data.is_low_confidence) {
        lowConfidenceWarning.style.display = "flex";
        if (lowConfidenceText) {
          lowConfidenceText.textContent = data.warning_message || "The AI is not confident about this prediction. Please try another image with better lighting or a clearer view.";
        }
      } else {
        lowConfidenceWarning.style.display = "none";
      }
    }

    // Show Results Panel
    if (resultContent) {
      resultContent.style.display = "block";
    }
  }

  // Hook try another button
  if (btnTryAnother) {
    btnTryAnother.addEventListener("click", () => {
      resetImageInput();
      if (fileInput) fileInput.click();
    });
  }

  // ========================================================================
  // Error & Notice Helpers
  // ========================================================================
  function showError(msg) {
    if (errorAlert && errorText) {
      errorText.textContent = msg;
      errorAlert.className = "alert-box alert-danger";
      errorAlert.style.display = "flex";
    }
  }

  function showModelAwaitingNotice(msg) {
    if (errorAlert && errorText) {
      errorText.innerHTML = `<strong>AI Model Not Yet Trained:</strong><br>${msg}`;
      errorAlert.className = "alert-box alert-warning";
      errorAlert.style.display = "flex";
    }
  }

  function hideError() {
    if (errorAlert) {
      errorAlert.style.display = "none";
    }
  }
});
