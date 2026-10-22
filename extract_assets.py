import cv2
import os
from PIL import Image

video_path = r'C:\Users\chowh\Videos\Screen Recordings\Screen Recording 2026-10-14 170959.mp4'
out_dir = r'c:\Users\chowh\OneDrive\Desktop\AI project\static\images'
os.makedirs(out_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)

def get_frame(frame_num):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    if ret:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return None

# Frame 60 (at ~2 sec): Hero section
f_hero = get_frame(60)
if f_hero is not None:
    img = Image.fromarray(f_hero)
    img.save(os.path.join(out_dir, "raw_hero_full.jpg"), quality=95)
    # The browser content is below the browser address bar
    # Browser bar is roughly top 130px.
    # The hero background image covers the whole section
    hero_bg = img.crop((0, 130, 2868, 1608))
    hero_bg.save(os.path.join(out_dir, "hero_bg.jpg"), quality=95)
    print("Saved hero_bg.jpg")

# Frame 380 (at ~12.6 sec): "Innovating Waste Management" section
f_innovate = get_frame(380)
if f_innovate is not None:
    img = Image.fromarray(f_innovate)
    img.save(os.path.join(out_dir, "raw_innovate_full.jpg"), quality=95)

# Frame 460 (at ~15.3 sec): "Innovative Waste Solutions" 3 cards
f_solutions = get_frame(460)
if f_solutions is not None:
    img = Image.fromarray(f_solutions)
    img.save(os.path.join(out_dir, "raw_solutions_full.jpg"), quality=95)

# Frame 530 (at ~17.6 sec): "How it works?" section
f_how = get_frame(530)
if f_how is not None:
    img = Image.fromarray(f_how)
    img.save(os.path.join(out_dir, "raw_how_full.jpg"), quality=95)

# Frame 580 (at ~19.3 sec): "Get in Touch" section
f_touch = get_frame(580)
if f_touch is not None:
    img = Image.fromarray(f_touch)
    img.save(os.path.join(out_dir, "raw_touch_full.jpg"), quality=95)

cap.release()
print("Base frames extracted successfully!")
