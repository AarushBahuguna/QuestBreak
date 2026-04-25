import json
from questionnaire import get_questions, compute_profile, assign_story_by_profile
from answer_checker import AnswerChecker

class QuestBreakApp:
    def __init__(self):
        self.answer_checker = AnswerChecker()
        self.stories = self._load_stories()
        self.user_sessions = {}

    def _load_stories(self):
        with open("stories.json", "r") as f:
            data = json.load(f)
        stories = {}
        for story in data["stories"]:
            stories[story["id"]] = story
        return stories

    def get_questionnaire(self):
        return get_questions()

    def process_questionnaire(self, answers: list) -> dict:
        profile = compute_profile(answers)
        story_id = assign_story_by_profile(profile)
        story = self.stories[story_id]
        return {
            "profile": profile,
            "story_id": story_id,
            "story_title": story["title"],
            "story_emoji": story["emoji"],
            "story_description": story["description"]
        }

    def get_story(self, story_id: str) -> dict:
        return self.stories.get(story_id)

    def get_chapter(self, story_id: str, chapter_id: str) -> dict:
        story = self.stories.get(story_id)
        if not story:
            return None
        for chapter in story["chapters"]:
            if chapter["id"] == chapter_id:
                return chapter
        return None

    def get_random_chapters(self, story_id: str, count: int = 5) -> list:
        import random
        story = self.stories.get(story_id)
        if story and story["chapters"]:
            chapters = [ch["id"] for ch in story["chapters"]]
            random.shuffle(chapters)
            return chapters[:count]
        return []

    def check_answer(self, story_id: str, chapter_id: str,
                     user_answer: str = None, image_path: str = None) -> dict:
        chapter = self.get_chapter(story_id, chapter_id)
        if not chapter:
            return {"score": 0, "status": "error", "feedback": "Chapter not found."}

        result = self.answer_checker.check_answer(
            user_answer=user_answer,
            expected_answer=chapter["expected_answer"],
            answer_type=chapter["answer_type"],
            image_path=image_path
        )

        result["points_earned"] = int(chapter.get("points", 10) * result["score"])
        result["hint"] = chapter.get("hint", "No hint available.")

        return result

    def get_story_progress(self, current_index: int, total: int = 5) -> dict:
        return {
            "current": current_index + 1,
            "total": total,
            "percent": int(((current_index + 1) / total) * 100)
        }
