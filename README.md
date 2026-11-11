# Final Project: Emotion Detector

A Flask web application that analyzes English text with the Watson NLP emotion prediction service and displays scores for anger, disgust, fear, joy, and sadness, plus the dominant emotion.

## Project contents

- `emotion_detection.py` — top-level import-compatible module for the emotion detector.
- `EmotionDetection/emotion_detection.py` — Watson NLP request, response formatting, and HTTP 400 handling.
- `EmotionDetection/__init__.py` — exports the application function as a package.
- `server.py` — Flask web interface and blank-input handling.
- `test_emotion_detection.py` — isolated unit tests (network requests are mocked).
- `templates/index.html` — browser interface.

## Setup and run

Python 3.9 or later is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python3 -m pip install -r requirements.txt
python3 server.py
```

Open <http://127.0.0.1:5000> and enter text. The application uses the public Skills Network Watson NLP endpoint; internet access is required for live predictions.

## Tests and static analysis

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
python3 -m pylint server.py emotion_detection.py EmotionDetection/emotion_detection.py test_emotion_detection.py
```

The tests mock the remote service and verify formatted predictions and the HTTP 400 fallback. Run the commands in your own environment to capture genuine terminal output for submission. Run the app locally to capture screenshots of a successful prediction (`6b_deployment_test.png`) and blank-input validation (`7c_error_handling_interface.png`).
