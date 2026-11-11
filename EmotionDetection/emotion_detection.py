"""Call the Watson NLP emotion prediction service and normalize its response."""

import requests

WATSON_EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return the five emotion scores and dominant emotion for input text.

    If the service rejects the request with HTTP 400, return ``None`` for
    each score and dominant emotion. Other HTTP and network errors propagate
    so callers can handle service outages separately.
    """
    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    response = requests.post(
        WATSON_EMOTION_URL,
        headers=headers,
        json={"raw_document": {"text": text_to_analyze}},
        timeout=30,
    )

    if response.status_code == 400:
        return {**dict.fromkeys(EMOTIONS), "dominant_emotion": None}

    response.raise_for_status()
    payload = response.json()
    prediction = payload["emotionPredictions"][0]["emotion"]
    result = {emotion: prediction[emotion] for emotion in EMOTIONS}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
