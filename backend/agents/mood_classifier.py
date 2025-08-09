import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import re

# Load Gemini API key from prod.env
load_dotenv("prod.env")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

VALID_EMOTIONS = [
    "happy", "sad", "angry", "excited", "depressed", "anxious",
    "lonely", "frustrated", "tired", "joyful", "scared", "worried",
    "upset", "relaxed", "stressed", "bored", "hopeful", "grateful",
    "neutral", "proud", "embarrassed", "nostalgic", "apathetic", "disappointed", "sarcastic"
]

FEW_SHOT_EXAMPLES = """
Example 1:
Text: "I scored 99/100 in my test today but somehow I feel like my life is pointless."
Output: {"emotion": ["depressed"], "confidence": 0.85, "reasoning": "Good achievement overshadowed by existential sadness."}

Example 2:
Text: "Oh sure, I love it when my computer crashes during a big project."
Output: {"emotion": ["frustrated", "sarcastic"], "confidence": 0.9, "reasoning": "Sarcasm indicating frustration with situation."}

Example 3:
Text: "I'm really excited and hopeful about the new opportunities ahead!"
Output: {"emotion": ["excited", "hopeful"], "confidence": 0.95, "reasoning": "Positive anticipation and optimism."}

Example 4:
Text: "I feel tired and bored of everything lately."
Output: {"emotion": ["tired", "bored"], "confidence": 0.9, "reasoning": "Explicit statements of tiredness and boredom."}
"""

def get_gemini_model():
    return genai.GenerativeModel("models/gemini-1.5-flash-latest")

def extract_json_from_text(text):
    """
    Attempt to extract a JSON object substring from a text block.
    Return parsed JSON dict or None if fail.
    """
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        if start == -1 or end == -1:
            return None
        json_str = text[start:end]
        return json.loads(json_str)
    except Exception:
        return None

def detect_emotion(text):
    prompt = f"""
You are a highly intelligent emotion detection AI.

Given the following journal entry, identify the emotions expressed.
- Detect multiple emotions if present.
- Handle sarcasm, contradictions, and indirect expressions.
- Respond ONLY with a JSON object with these keys:
  - "emotion": list of emotions from {VALID_EMOTIONS}
  - "confidence": a float between 0 and 1 representing confidence level
  - "reasoning": short explanation for the detected emotions

If unsure, guess the closest emotion(s).

{FEW_SHOT_EXAMPLES}

Text: "{text}"

Output (ONLY JSON):
"""
    model = get_gemini_model()
    response = model.generate_content(prompt)
    raw_text = response.text.strip()
    print("DEBUG detect_emotion raw response:", raw_text)
    return raw_text

def verify_emotion(text, detected_emotion_json):
    prompt = f"""
You are a critical reviewer AI.

Given the original text:

"{text}"

and the detected emotion JSON:

{detected_emotion_json}

Review if the emotions and confidence are appropriate.

If correct, return the exact same JSON.

If incorrect, correct the emotions, confidence, and reasoning accordingly.

Output ONLY valid JSON in the same format.
"""
    model = get_gemini_model()
    response = model.generate_content(prompt)
    raw_text = response.text.strip()
    print("DEBUG verify_emotion raw response:", raw_text)
    return raw_text

def validate_and_parse_emotion(json_str):
    data = extract_json_from_text(json_str)
    if not data:
        return None

    emotions = data.get("emotion")
    confidence = data.get("confidence")
    reasoning = data.get("reasoning", "")

    if not emotions or not isinstance(emotions, list):
        return None

    filtered = [e for e in emotions if e in VALID_EMOTIONS]
    if not filtered:
        return None

    if not isinstance(confidence, (float, int)) or not (0 <= confidence <= 1):
        confidence = 0.0

    return {
        "emotion": filtered,
        "confidence": confidence,
        "reasoning": reasoning
    }

def classify_emotion(text):
    # Quick heuristic pre-check: skip purely numeric/math texts
    if re.fullmatch(r"[0-9+\-*/=. ,]+", text.strip()):
        return {
            "emotion": "invalid",
            "message": "Please enter an emotion-related text."
        }

    try:
        detected = detect_emotion(text)
        verified = verify_emotion(text, detected)

        result = validate_and_parse_emotion(verified)
        if not result:
            result = validate_and_parse_emotion(detected)

        if not result:
            return {
                "emotion": "invalid",
                "message": "Could not determine emotion."
            }

        # Return only the first emotion string, not list
        primary_emotion = result["emotion"][0]

        return {
            "emotion": primary_emotion,
            "confidence": result["confidence"],
            "reasoning": result["reasoning"],
            "message": "Emotion detected successfully."
        }

    except Exception as e:
        return {
            "emotion": "error",
            "message": f"Error during emotion classification: {str(e)}"
        }
