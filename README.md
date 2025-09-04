# Road Incident Detection �

The **Road Incident Detection** project is a computer vision application designed to detect unusual motion events (accidents, traffic jams, sudden stops) in road surveillance footage. It provides a baseline motion-based detector with extendable architecture for integrating advanced deep learning models later.

---

## ✨ Features
- Real-time motion-based detection of road incidents.
- Works with videos, webcam feeds, or live streams.
- Saves annotated videos with bounding boxes.
- Configurable detection sensitivity and frame skipping.
- Lightweight, runs on CPU (no GPU required).
- Extendable for advanced ML/DL integration.

---

## � Project Structure


Road-Incident-Detection/
│── app.py # Main script for detection
│── requirements.txt # Python dependencies
│── data/ # Sample input videos (e.g., sample.mp4)
│── outputs/ # Saved results with annotations
│── README.md # Documentation


---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Sai-vikas-Ambati/Road-Incident-Detection.git
cd Road-Incident-Detection

2. (Optional) Create virtual environment
python -m venv .venv
source .venv/Scripts/activate   # Windows PowerShell
# For Linux/Mac:
# source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

▶️ Usage
Run with sample video
python app.py --source data/sample.mp4 --save

Run with webcam
python app.py --source 0

Run with network stream
python app.py --source rtsp://username:password@ip:port/stream


--save → saves output to outputs/

--display → enables live preview (if supported)

�️ Tech Stack

Python 3.8+

OpenCV – for video processing & motion detection

NumPy – for frame manipulation

Requests / OS – for optional logging & integrations

� Contributing

Pull requests are welcome! Please follow the conventional commit style for commits (feat:, fix:, docs:, etc.) and ensure code passes linting before submitting.

� License

This project is licensed under the MIT License. See LICENSE
 for details.

