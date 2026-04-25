import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class AnswerChecker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def check_text_answer(self, user_answer: str, expected_answer: str) -> dict:
        """
        Checks a text answer using multiple strategies:
        1. Exact match (case-insensitive, stripped)
        2. Keyword containment
        3. TF-IDF cosine similarity for longer answers
        """
        user_clean = user_answer.strip().lower()
        expected_clean = expected_answer.strip().lower()

        # Strategy 1: Exact match
        if user_clean == expected_clean:
            return {"score": 1.0, "status": "correct", "feedback": "Perfect answer!"}

        # Strategy 2: Check if expected answer is contained in user answer
        if expected_clean in user_clean:
            return {"score": 0.9, "status": "correct", "feedback": "That's right!"}

        # Strategy 3: Keyword overlap for short expected answers
        expected_words = set(re.findall(r'\w+', expected_clean))
        user_words = set(re.findall(r'\w+', user_clean))

        if expected_words and expected_words.issubset(user_words):
            return {"score": 0.85, "status": "correct", "feedback": "Correct!"}

        # Strategy 4: TF-IDF cosine similarity for longer answers
        if len(expected_clean.split()) > 2:
            try:
                tfidf_matrix = self.vectorizer.fit_transform([expected_clean, user_clean])
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            except ValueError:
                similarity = 0.0

            if similarity >= 0.6:
                return {"score": similarity, "status": "correct",
                        "feedback": f"Great answer! (Confidence: {similarity:.0%})"}
            elif similarity >= 0.3:
                return {"score": similarity, "status": "partial",
                        "feedback": "You're on the right track, but not quite there."}
            else:
                return {"score": similarity, "status": "incorrect",
                        "feedback": "That's not what we're looking for."}

        # For short expected answers — check partial word overlap
        overlap = expected_words & user_words
        if overlap:
            ratio = len(overlap) / len(expected_words)
            if ratio >= 0.5:
                return {"score": ratio, "status": "partial",
                        "feedback": "Close! Try to be more specific."}

        return {"score": 0.0, "status": "incorrect",
                "feedback": "That's not the right answer. Try again!"}

    def check_image_answer(self, image_path: str, expected_label: str) -> dict:
        """
        Checks an image answer using MobileNetV2 via CNNVerifier.
        Classifies the uploaded image and checks if it matches the expected object category.
        """
        import os
        if not os.path.exists(image_path):
            return {"score": 0.0, "status": "incorrect",
                    "feedback": "No image was found. Please try uploading again."}

        valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        _, ext = os.path.splitext(image_path)
        if ext.lower() not in valid_extensions:
            return {"score": 0.0, "status": "incorrect",
                    "feedback": "Invalid image format. Please upload a JPG or PNG."}

        if os.path.getsize(image_path) < 1000:
            return {"score": 0.0, "status": "incorrect",
                    "feedback": "The image appears to be invalid or too small."}

        # Run real CNN classification
        from cnn_verifier import CNNVerifier
        verifier = CNNVerifier()
        result = verifier.verify(image_path, expected_label)

        if result["matched"]:
            conf = result["confidence"]
            return {
                "score": 1.0,
                "status": "correct",
                "feedback": f"✅ Detected '{result['detected']}' — that's exactly what we needed! ({conf:.0%} confidence)"
            }
        else:
            detected = result["detected"]
            return {
                "score": 0.0,
                "status": "incorrect",
                "feedback": f"❌ I see '{detected}' in your photo, but we need a {expected_label}. Try a different object!"
            }

    def check_answer(self, user_answer, expected_answer: str, answer_type: str,
                     image_path: str = None) -> dict:
        """Main dispatch method for checking any answer type."""
        if answer_type == "image":
            if image_path:
                return self.check_image_answer(image_path, expected_answer)
            else:
                return {"score": 0.0, "status": "incorrect",
                        "feedback": "Please upload an image for this challenge."}
        elif answer_type == "text":
            return self.check_text_answer(str(user_answer), expected_answer)
        elif answer_type == "choice":
            return self.check_text_answer(str(user_answer), expected_answer)
        else:
            return {"score": 0.0, "status": "incorrect",
                    "feedback": "Unknown answer type."}
