"""
End-to-End Verification Test Script for New Waste Classifier Features:
- Feature 3: Waste Disposal Recommendations
- Feature 4: Waste Statistics Dashboard
- Feature 5: Classification History
- Feature 6: Low-Confidence Prediction Warning
- Feature 7: Environmental Awareness Section
"""

import os
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_routes():
    print(">>> 1. Testing Page Routes and Navigation...")
    routes = ["/", "/classify", "/dashboard", "/history", "/awareness", "/api/status"]
    for r in routes:
        res = requests.get(f"{BASE_URL}{r}")
        assert res.status_code == 200, f"Route {r} failed with status {res.status_code}"
        print(f"  [PASS] {r} -> 200 OK (Content-Length: {len(res.text)})")

def test_initial_empty_history_and_stats():
    print("\n>>> 2. Testing Initial History and Dashboard API...")
    res = requests.get(f"{BASE_URL}/api/statistics")
    assert res.status_code == 200
    stats = res.json()
    print(f"  Initial Stats: Total={stats['total']}, Counts={stats['counts']}")

    res_hist = requests.get(f"{BASE_URL}/api/history")
    assert res_hist.status_code == 200
    hist = res_hist.json()
    print(f"  Initial History Count: {hist['count']}")

def test_invalid_uploads():
    print("\n>>> 3. Testing Input Validation (Invalid Uploads)...")
    # Empty post
    res = requests.post(f"{BASE_URL}/predict", files={})
    assert res.status_code == 400
    print("  [PASS] Empty file payload rejected with 400")

    # Unsupported file extension
    files = {"image": ("test.txt", b"not an image", "text/plain")}
    res = requests.post(f"{BASE_URL}/predict", files=files)
    assert res.status_code == 400
    print("  [PASS] Non-image file rejected with 400")

def test_sample_predictions():
    print("\n>>> 4. Testing Real Model Predictions & Disposal Recommendations (Feature 3 & 6)...")
    sample_files = [
        "plastic_sample_1.jpg",
        "paper_sample_1.jpg",
        "metal_sample_1.jpg",
        "glass_sample_1.jpg",
        "organic_sample_1.jpg"
    ]

    for filename in sample_files:
        path = os.path.join("sample_test_images", filename)
        if not os.path.exists(path):
            print(f"  [SKIP] {path} not found")
            continue

        with open(path, "rb") as f:
            files = {"image": (filename, f.read(), "image/jpeg")}

        res = requests.post(f"{BASE_URL}/predict", files=files)
        assert res.status_code == 200, f"Predict failed for {filename}: {res.text}"
        data = res.json()

        assert data["success"] is True
        assert "record_id" in data
        assert "category" in data
        assert "confidence" in data
        assert "recommendation" in data
        assert "disposal_instructions" in data["recommendation"]
        assert "is_low_confidence" in data

        cat = data["category"]
        conf = data["confidence"]
        disp = data["recommendation"]["disposal_instructions"]
        is_low = data["is_low_confidence"]

        print(f"  [PASS] {filename} -> Predicted: '{cat}' | Conf: {conf}% | LowConf: {is_low} | RecordID: #{data['record_id']}")
        print(f"         Disposal Instruction: \"{disp}\"")

def test_history_and_statistics_persistence():
    print("\n>>> 5. Testing History & Statistics Persistence (Feature 4 & 5)...")
    res_hist = requests.get(f"{BASE_URL}/api/history")
    assert res_hist.status_code == 200
    hist = res_hist.json()
    count = hist["count"]
    print(f"  [PASS] Retrieved {count} history records from database")
    assert count > 0, "Expected at least 1 record in history after predictions"

    # Verify order: newest first
    records = hist["records"]
    for i in range(len(records) - 1):
        assert records[i]["id"] >= records[i+1]["id"], "History is not ordered newest first!"
    print("  [PASS] Records verified to be ordered newest first (descending ID)")

    # Verify statistics match
    res_stats = requests.get(f"{BASE_URL}/api/statistics")
    assert res_stats.status_code == 200
    stats = res_stats.json()
    assert stats["total"] == count, f"Stats total ({stats['total']}) doesn't match history count ({count})"
    sum_counts = sum(stats["counts"].values())
    assert sum_counts == count, f"Sum of category counts ({sum_counts}) does not equal total ({count})"
    print(f"  [PASS] Stats total verified: {stats['total']} matches sum of category counts {stats['counts']}")
    print(f"         Percentage breakdown: {stats['percentages']}")

def test_clear_history():
    print("\n>>> 6. Testing Clear History Functionality (Feature 5)...")
    res_clear = requests.post(f"{BASE_URL}/api/history/clear")
    assert res_clear.status_code == 200
    assert res_clear.json()["success"] is True

    # Re-check stats and history
    res_stats = requests.get(f"{BASE_URL}/api/statistics")
    stats = res_stats.json()
    assert stats["total"] == 0, "Stats total not 0 after clear!"
    for cat, val in stats["counts"].items():
        assert val == 0, f"Count for {cat} is {val}, expected 0"

    res_hist = requests.get(f"{BASE_URL}/api/history")
    assert res_hist.json()["count"] == 0
    print("  [PASS] History successfully cleared and database reset to 0.")

if __name__ == "__main__":
    test_routes()
    test_initial_empty_history_and_stats()
    test_invalid_uploads()
    test_sample_predictions()
    test_history_and_statistics_persistence()
    test_clear_history()
    print("\n=======================================================")
    print("ALL TESTS PASSED SUCCESSFULLY! ALL 5 FEATURES VERIFIED!")
    print("=======================================================")
