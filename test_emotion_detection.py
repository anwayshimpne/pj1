"""Unit tests for EmotionDetection.emotion_detection."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import (
    MODEL_ID,
    WATSON_EMOTION_URL,
    emotion_detector,
)


class EmotionDetectorTests(unittest.TestCase):
    """Verify response formatting and service error handling."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_formats_scores_and_dominant_emotion(self, post):
        post.return_value = Mock(
            status_code=200,
            json=lambda: {
                "emotionPredictions": [
                    {
                        "emotion": {
                            "anger": 0.1,
                            "disgust": 0.05,
                            "fear": 0.15,
                            "joy": 0.6,
                            "sadness": 0.1,
                        }
                    }
                ]
            },
        )
        result = emotion_detector("I am happy")
        self.assertEqual(
            result,
            {
                "anger": 0.1,
                "disgust": 0.05,
                "fear": 0.15,
                "joy": 0.6,
                "sadness": 0.1,
                "dominant_emotion": "joy",
            },
        )
        post.assert_called_once_with(
            WATSON_EMOTION_URL,
            headers={"grpc-metadata-mm-model-id": MODEL_ID},
            json={"raw_document": {"text": "I am happy"}},
            timeout=30,
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_returns_empty_result(self, post):
        post.return_value = Mock(status_code=400)
        self.assertEqual(
            emotion_detector("invalid input"),
            {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None,
            },
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_other_http_errors_are_raised(self, post):
        response = Mock(status_code=503)
        response.raise_for_status.side_effect = RuntimeError("service unavailable")
        post.return_value = response
        with self.assertRaisesRegex(RuntimeError, "service unavailable"):
            emotion_detector("some text")


if __name__ == "__main__":
    unittest.main()
