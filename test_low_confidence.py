import io
import requests
from PIL import Image

# Blend two very different images (metal and paper) to create an ambiguous item with < 60% confidence
im1 = Image.open("sample_test_images/metal_sample_1.jpg").convert("RGB").resize((224, 224))
im2 = Image.open("sample_test_images/paper_sample_1.jpg").convert("RGB").resize((224, 224))
blended = Image.blend(im1, im2, alpha=0.55)

buf = io.BytesIO()
blended.save(buf, format="JPEG")
buf.seek(0)

res = requests.post("http://127.0.0.1:5000/predict", files={"image": ("ambiguous.jpg", buf.read(), "image/jpeg")})
data = res.json()
print("Category:", data.get("category"))
print("Confidence:", data.get("confidence"), "%")
print("Threshold:", data.get("confidence_threshold"), "%")
print("Is Low Confidence:", data.get("is_low_confidence"))
print("Warning Message:", data.get("warning_message"))
