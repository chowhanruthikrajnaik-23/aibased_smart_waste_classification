import os
import requests

for f in sorted(os.listdir("sample_test_images")):
    if f.endswith(".jpg"):
        path = os.path.join("sample_test_images", f)
        with open(path, "rb") as fp:
            res = requests.post("http://127.0.0.1:5000/predict", files={"image": (f, fp.read(), "image/jpeg")})
            data = res.json()
            cat = data.get("category")
            conf = data.get("confidence")
            low = data.get("is_low_confidence")
            print(f"{f:22} -> Category: {cat:12} | Conf: {conf:6.2f}% | LowConf: {low}")
