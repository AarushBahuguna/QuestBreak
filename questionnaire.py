import numpy as np

QUESTIONNAIRE_INTRO = """
╔══════════════════════════════════════════════════════════════╗
║           Welcome to the QuestBreak Initiation              ║
╚══════════════════════════════════════════════════════════════╝

You wake up in a vast white room. Four doors shimmer before you,
each pulsing with a different light. A voice echoes:

"Before you choose a door, I must understand who you are.
Answer truthfully — your destiny depends on it."

"""

QUESTIONS = [
    {
        "id": "q1",
        "narrative": "The voice continues: \"You find a locked chest in front of you...\"",
        "question": "What do you do first?",
        "options": [
            {"label": "A", "text": "Smash it open immediately", "scores": {"risk": 3, "creativity": 1, "logic": 0, "social": 0, "patience": 0}},
            {"label": "B", "text": "Look for a key nearby", "scores": {"risk": 1, "creativity": 1, "logic": 2, "social": 0, "patience": 2}},
            {"label": "C", "text": "Study the lock mechanism carefully", "scores": {"risk": 0, "creativity": 2, "logic": 3, "social": 0, "patience": 3}},
            {"label": "D", "text": "Ask if anyone else is around to help", "scores": {"risk": 0, "creativity": 0, "logic": 1, "social": 3, "patience": 1}}
        ]
    },
    {
        "id": "q2",
        "narrative": "A holographic screen appears showing two paths through a dark forest...",
        "question": "Which path do you take?",
        "options": [
            {"label": "A", "text": "The short, dangerous path through the swamp", "scores": {"risk": 3, "creativity": 0, "logic": 0, "social": 0, "patience": 0}},
            {"label": "B", "text": "The long, scenic route along the river", "scores": {"risk": 0, "creativity": 2, "logic": 1, "social": 0, "patience": 3}},
            {"label": "C", "text": "Create your own path through the trees", "scores": {"risk": 2, "creativity": 3, "logic": 1, "social": 0, "patience": 1}},
            {"label": "D", "text": "Wait for a group to travel with", "scores": {"risk": 0, "creativity": 0, "logic": 1, "social": 3, "patience": 2}}
        ]
    },
    {
        "id": "q3",
        "narrative": "An AI guardian blocks your way and poses a challenge...",
        "question": "What type of challenge do you prefer?",
        "options": [
            {"label": "A", "text": "A logic puzzle or math problem", "scores": {"risk": 0, "creativity": 0, "logic": 3, "social": 0, "patience": 2}},
            {"label": "B", "text": "A creative storytelling task", "scores": {"risk": 1, "creativity": 3, "logic": 0, "social": 1, "patience": 1}},
            {"label": "C", "text": "A physical real-world challenge", "scores": {"risk": 3, "creativity": 1, "logic": 0, "social": 0, "patience": 0}},
            {"label": "D", "text": "A team-based trivia battle", "scores": {"risk": 1, "creativity": 1, "logic": 2, "social": 3, "patience": 1}}
        ]
    },
    {
        "id": "q4",
        "narrative": "You discover a time machine that can take you anywhere...",
        "question": "Where do you go?",
        "options": [
            {"label": "A", "text": "The Age of Exploration — uncharted seas and treasure", "scores": {"risk": 3, "creativity": 1, "logic": 0, "social": 0, "patience": 1}},
            {"label": "B", "text": "A magical medieval kingdom", "scores": {"risk": 1, "creativity": 3, "logic": 0, "social": 1, "patience": 1}},
            {"label": "C", "text": "A space station 200 years in the future", "scores": {"risk": 1, "creativity": 1, "logic": 3, "social": 0, "patience": 2}},
            {"label": "D", "text": "A secret spy headquarters during the Cold War", "scores": {"risk": 2, "creativity": 1, "logic": 2, "social": 2, "patience": 2}}
        ]
    },
    {
        "id": "q5",
        "narrative": "The room starts to shift and change around you...",
        "question": "How many hours do you typically spend on your phone per day?",
        "options": [
            {"label": "A", "text": "Less than 2 hours", "scores": {"risk": 0, "creativity": 0, "logic": 0, "social": 0, "patience": 3}},
            {"label": "B", "text": "2-4 hours", "scores": {"risk": 1, "creativity": 0, "logic": 0, "social": 1, "patience": 2}},
            {"label": "C", "text": "4-6 hours", "scores": {"risk": 2, "creativity": 0, "logic": 0, "social": 2, "patience": 1}},
            {"label": "D", "text": "More than 6 hours", "scores": {"risk": 3, "creativity": 0, "logic": 0, "social": 3, "patience": 0}}
        ]
    },
    {
        "id": "q6",
        "narrative": "A mirror materializes. Your reflection speaks to you...",
        "question": "When you're stressed, what do you usually do?",
        "options": [
            {"label": "A", "text": "Go for a walk or exercise", "scores": {"risk": 2, "creativity": 0, "logic": 0, "social": 0, "patience": 2}},
            {"label": "B", "text": "Listen to music or create art", "scores": {"risk": 0, "creativity": 3, "logic": 0, "social": 0, "patience": 2}},
            {"label": "C", "text": "Analyze the problem and make a plan", "scores": {"risk": 0, "creativity": 0, "logic": 3, "social": 0, "patience": 3}},
            {"label": "D", "text": "Talk to friends or scroll social media", "scores": {"risk": 1, "creativity": 0, "logic": 0, "social": 3, "patience": 0}}
        ]
    },
    {
        "id": "q7",
        "narrative": "The voice speaks one final time before the doors open...",
        "question": "What motivates you the most?",
        "options": [
            {"label": "A", "text": "Thrill and adventure", "scores": {"risk": 3, "creativity": 1, "logic": 0, "social": 0, "patience": 0}},
            {"label": "B", "text": "Imagination and self-expression", "scores": {"risk": 0, "creativity": 3, "logic": 0, "social": 1, "patience": 1}},
            {"label": "C", "text": "Knowledge and solving problems", "scores": {"risk": 0, "creativity": 0, "logic": 3, "social": 0, "patience": 2}},
            {"label": "D", "text": "Helping others and making connections", "scores": {"risk": 0, "creativity": 1, "logic": 1, "social": 3, "patience": 1}}
        ]
    }
]

STORY_MAP = {
    0: "adventure",
    1: "fantasy",
    2: "scifi",
    3: "espionage"
}


def get_questions():
    return QUESTIONS


def compute_profile(answers: list) -> dict:
    """
    Takes a list of answer labels (e.g., ['A', 'B', 'C', ...])
    and computes the personality profile scores.
    """
    profile = {"risk": 0, "creativity": 0, "logic": 0, "social": 0, "patience": 0}

    for i, answer_label in enumerate(answers):
        if i >= len(QUESTIONS):
            break
        question = QUESTIONS[i]
        for option in question["options"]:
            if option["label"] == answer_label.upper():
                for trait, score in option["scores"].items():
                    profile[trait] += score
                break

    return profile


def profile_to_features(profile: dict) -> np.ndarray:
    """Convert profile dict to a numpy feature vector for ML classification."""
    return np.array([
        profile["risk"],
        profile["creativity"],
        profile["logic"],
        profile["social"],
        profile["patience"]
    ], dtype=float)


def assign_story_by_profile(profile: dict) -> str:
    """
    Rule-based story assignment as a fallback
    (or primary method if ML clusters aren't trained).
    """
    scores = {
        "adventure":  profile["risk"] * 2 + profile["patience"],
        "fantasy":    profile["creativity"] * 2 + profile["social"],
        "scifi":      profile["logic"] * 2 + profile["patience"],
        "espionage":  profile["social"] + profile["logic"] + profile["risk"]
    }
    return max(scores, key=scores.get)
