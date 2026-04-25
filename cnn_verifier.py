import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np

# Map our simple story labels -> lists of ImageNet class name substrings to match against
LABEL_KEYWORD_MAP = {
    # Nature / plants
    "plant":       ["plant", "flower", "tree", "shrub", "fern", "leaf", "herb", "moss", "vine", "cactus", "pot"],
    "specimen":    ["plant", "flower", "fruit", "vegetable", "leaf", "herb", "mushroom", "strawberry", "apple", "lemon", "banana"],
    "sphere":      ["ball", "orange", "apple", "sphere", "globe", "balloon"],

    # Drinks / containers
    "bottle":      ["bottle", "water_jug", "wine_bottle", "beer_bottle", "cup", "mug", "canteen"],
    "flask":       ["bottle", "cup", "mug", "jug", "pitcher", "vessel"],

    # Writing / reading
    "pen":         ["pen", "pencil", "ballpoint", "fountain_pen", "crayon", "paintbrush"],
    "scroll":      ["book", "comic_book", "binder", "envelope", "paper"],
    "wand":        ["stick", "baton", "baseball_bat", "pencil", "chopstick"],

    # Food
    "food":        ["pizza", "hamburger", "hot_dog", "sandwich", "pretzel", "bagel", "banana", "apple", "orange",
                    "broccoli", "carrot", "corn", "mushroom", "pineapple", "strawberry", "lemon", "soup", "cheeseburger",
                    "ice_cream", "chocolate", "candy", "cookie", "cake", "burrito", "sushi", "bread", "egg", "waffle"],

    # Light sources
    "light":       ["lamp", "torch", "candle", "spotlight", "lantern", "flashlight", "bulb", "street_lamp"],
    "fire":        ["candle", "torch", "bonfire", "lamp", "spotlight"],
    "star":        ["lamp", "spotlight", "bulb", "lantern", "candle", "torch"],

    # Accessories / clothing
    "watch":       ["stopwatch", "watch", "digital_watch", "analog_clock", "sundial"],
    "clothing":    ["jacket", "coat", "cloak", "sweatshirt", "jersey", "cardigan", "hat", "cap", "beret", "bonnet"],
    "disguise":    ["sunglasses", "sunglass", "hat", "cap", "beret", "wig", "mask", "scarf"],
    "gear":        ["glove", "mitten", "jacket", "coat", "goggles", "helmet", "mask"],

    # Keys / locks
    "key":         ["key", "padlock", "lock", "keychain", "safe", "combination_lock"],

    # Books / paper
    "book":        ["book", "comic_book", "binder", "notebook", "diary", "magazine", "newspaper", "envelope"],

    # Windows / doors
    "window":      ["window", "venetian_blind", "screen", "sliding_door"],
    "door":        ["door", "sliding_door", "screen", "window", "arch", "gate"],

    # Animals
    "animal":      ["cat", "dog", "bird", "fish", "hamster", "rabbit", "parrot", "snake", "turtle", "bear",
                    "elephant", "lion", "tiger", "horse", "cow", "sheep", "penguin", "duck", "chicken"],

    # Electronics / devices
    "device":      ["remote_control", "cellular_telephone", "mobile_phone", "iPod", "tape_player", "computer_keyboard",
                    "monitor", "laptop", "calculator", "joystick", "television"],
    "gadget":      ["cellular_telephone", "mobile_phone", "smartwatch", "digital_watch", "remote_control", "iPod"],
    "battery":     ["plug", "power_strip", "switch", "remote_control", "electric_fan"],
    "audio":       ["headphone", "earphone", "speaker", "microphone", "loudspeaker", "iPod"],
    "data":        ["book", "floppy_disk", "CD", "cassette", "hard_disk", "binder"],

    # Tools
    "tool":        ["screwdriver", "hammer", "wrench", "pliers", "chainsaw", "handsaw", "measuring_cup", "spatula"],

    # Espionage items
    "intel":       ["book", "notebook", "laptop", "monitor", "envelope", "newspaper", "magazine"],
    "card":        ["credit_card", "cassette", "envelope"],
    "vehicle":     ["car", "bicycle", "motorcycle", "bus", "truck", "van", "cab", "jeep", "minivan"],
    "hide":        ["safe", "locker", "mailbox", "basket", "bucket", "pot"],
    "distraction": ["coin", "padlock", "key", "puck", "frisbee"],
    "safe":        ["safe", "locker", "mailbox", "box", "chest", "cabinet"],
    "shield":      ["plate", "frisbee", "disk", "pot", "book"],
    "ring":        ["ring", "coin", "washer", "CD"],
}


class CNNVerifier:
    _model = None  # class-level cache so model loads once

    def __init__(self):
        self.target_size = (224, 224)
        self.top_k = 5

    def _get_model(self):
        if CNNVerifier._model is None:
            print("[CNNVerifier] Loading MobileNetV2 (ImageNet weights)...")
            from tensorflow.keras.applications import MobileNetV2
            CNNVerifier._model = MobileNetV2(weights="imagenet", include_top=True)
            print("[CNNVerifier] Model ready.")
        return CNNVerifier._model

    def _preprocess(self, image_path: str) -> np.ndarray:
        from tensorflow.keras.preprocessing import image as keras_image
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
        img = keras_image.load_img(image_path, target_size=self.target_size)
        arr = keras_image.img_to_array(img)
        arr = np.expand_dims(arr, axis=0)
        return preprocess_input(arr)

    def classify(self, image_path: str) -> list[tuple[str, float]]:
        """Return top-k (class_name, confidence) predictions."""
        from tensorflow.keras.applications.mobilenet_v2 import decode_predictions
        model = self._get_model()
        x = self._preprocess(image_path)
        preds = model.predict(x, verbose=0)
        decoded = decode_predictions(preds, top=self.top_k)[0]
        # decoded is list of (imagenet_id, class_name, score)
        return [(label.lower().replace("_", " "), float(score))
                for _, label, score in decoded]

    def verify(self, image_path: str, expected_label: str) -> dict:
        """
        Check if any of the top predictions match the expected label keywords.
        Returns a dict with keys: matched (bool), confidence (float), detected (str)
        """
        keywords = LABEL_KEYWORD_MAP.get(expected_label.lower(), [expected_label.lower()])
        
        try:
            predictions = self.classify(image_path)
        except Exception as e:
            print(f"[CNNVerifier] Error during classification: {e}")
            return {"matched": False, "confidence": 0.0, "detected": "unknown"}

        best_label = predictions[0][0] if predictions else "unknown"
        best_conf = predictions[0][1] if predictions else 0.0

        print(f"[CNNVerifier] Top predictions: {predictions}")
        print(f"[CNNVerifier] Checking against keywords: {keywords}")

        for pred_label, confidence in predictions:
            for kw in keywords:
                if kw in pred_label or pred_label in kw:
                    print(f"[CNNVerifier] ✅ MATCH: '{pred_label}' matched keyword '{kw}' ({confidence:.2%})")
                    return {"matched": True, "confidence": confidence, "detected": pred_label}

        print(f"[CNNVerifier] ❌ No match. Best: '{best_label}' ({best_conf:.2%})")
        return {"matched": False, "confidence": best_conf, "detected": best_label}
