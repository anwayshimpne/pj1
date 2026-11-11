"""Flask web interface for the Watson NLP emotion detector."""

from flask import Flask, render_template, request
from requests.exceptions import RequestException

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """Render the text-entry page."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET", "POST"])
def detect_emotion():
    """Analyze submitted text or show a helpful message for blank input."""
    text_to_analyze = request.values.get("textToAnalyze", "").strip()
    if not text_to_analyze:
        return (
            "Please enter some text to analyze.",
            400,
            {"Content-Type": "text/plain; charset=utf-8"},
        )

    try:
        result = emotion_detector(text_to_analyze)
    except (RequestException, KeyError, IndexError, TypeError, ValueError):
        app.logger.exception("Emotion analysis request failed")
        return "Emotion analysis is temporarily unavailable.", 502

    if result["dominant_emotion"] is None:
        return "The service could not analyze that text. Please try a different input.", 400

    emotions = ("anger", "disgust", "fear", "joy", "sadness")
    scores = ", ".join(f"{emotion}: {result[emotion]:.3f}" for emotion in emotions)
    return (
        f"For the given statement, the system response is {scores}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    # Static analysis command: python3 -m pylint server.py emotion_detection.py EmotionDetection/emotion_detection.py test_emotion_detection.py
    app.run(host="0.0.0.0", port=5000, debug=False)
