# Emotion Detector

A Flask web application that analyzes English text with the Watson NLP emotion prediction service and displays anger, disgust, fear, joy, sadness, and the dominant emotion.

## Project contents

- `EmotionDetection/emotion_detection.py` — Watson NLP request, response formatting, and HTTP 400 handling.
- `EmotionDetection/__init__.py` — exports the application function as a package.
- `server.py` — Flask web interface and blank-input handling.
- `test_emotion_detection.py` — isolated unit tests (network requests are mocked).
- `templates/index.html` — simple browser interface.

## Setup and run

Python 3.9 or later is recommended.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python server.py
```

Open <http://127.0.0.1:5000> and enter text. The application uses the public Skills Network Watson NLP endpoint; internet access is required for live predictions.

## Tests and static analysis

```bash
python -m unittest discover -s . -p 'test_*.py' -v
python -m pylint server.py EmotionDetection/emotion_detection.py test_emotion_detection.py
```

The tests mock the remote service and verify formatted predictions and the HTTP 400 fallback. Run the commands in your own environment to capture genuine terminal output for submission; no terminal run or browser screenshot is represented as having been performed here.

For the assignment screenshots, run the app locally and save a screenshot of a successful prediction as `6b_deployment_test.png`, then a blank-input validation as `7c_error_handling_interface.png`.
