import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from QuestBreakApp import QuestBreakApp

app = Flask(__name__)
app.secret_key = "questbreak-secret-key-2024"
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

quest_app = QuestBreakApp()


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/questionnaire")
def questionnaire():
    questions = quest_app.get_questionnaire()
    return render_template("questionnaire.html", questions=questions)


@app.route("/submit_questionnaire", methods=["POST"])
def submit_questionnaire():
    data = request.get_json()
    answers = data.get("answers", [])

    result = quest_app.process_questionnaire(answers)

    session["story_id"] = result["story_id"]
    session["total_points"] = 0
    session["chapters_completed"] = 0

    return jsonify(result)


@app.route("/story/<story_id>")
def story_start(story_id):
    story = quest_app.get_story(story_id)
    if not story:
        return redirect(url_for("landing"))

    chapters = quest_app.get_random_chapters(story_id, 5)
    if not chapters:
        return redirect(url_for("landing"))

    session["chapter_sequence"] = chapters
    session["current_chapter_idx"] = 0
    session["story_id"] = story_id
    session.setdefault("total_points", 0)
    session.setdefault("chapters_completed", 0)

    first_chapter_id = chapters[0]
    return redirect(url_for("play_chapter", story_id=story_id, chapter_id=first_chapter_id))


@app.route("/story/<story_id>/chapter/<chapter_id>")
def play_chapter(story_id, chapter_id):
    story = quest_app.get_story(story_id)
    chapter = quest_app.get_chapter(story_id, chapter_id)

    if not story or not chapter:
        return redirect(url_for("landing"))

    current_idx = session.get("current_chapter_idx", 0)
    total_chapters = len(session.get("chapter_sequence", [])) or 5
    progress = quest_app.get_story_progress(current_idx, total_chapters)

    return render_template("story.html",
                           story=story,
                           chapter=chapter,
                           progress=progress,
                           total_points=session.get("total_points", 0))


@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    story_id = request.form.get("story_id")
    chapter_id = request.form.get("chapter_id")
    answer_type = request.form.get("answer_type")

    user_answer = None
    image_path = None

    if answer_type == "image":
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename:
                filename = secure_filename(file.filename)
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(image_path)
                print(f"[Upload] Image saved to: {image_path} ({os.path.getsize(image_path)} bytes)")
            else:
                return jsonify({"score": 0.0, "status": "incorrect",
                                "feedback": "No image file was selected. Please upload a photo.",
                                "points_earned": 0, "hint": "", "next_chapter": chapter_id,
                                "total_points": session.get("total_points", 0),
                                "chapters_completed": session.get("chapters_completed", 0)})
        else:
            return jsonify({"score": 0.0, "status": "incorrect",
                            "feedback": "No image was received. Please try uploading again.",
                            "points_earned": 0, "hint": "", "next_chapter": chapter_id,
                            "total_points": session.get("total_points", 0),
                            "chapters_completed": session.get("chapters_completed", 0)})
    else:
        user_answer = request.form.get("answer", "")

    result = quest_app.check_answer(story_id, chapter_id,
                                     user_answer=user_answer,
                                     image_path=image_path)

    if result["status"] == "correct":
        session["total_points"] = session.get("total_points", 0) + result["points_earned"]
        session["chapters_completed"] = session.get("chapters_completed", 0) + 1
        
        current_idx = session.get("current_chapter_idx", 0) + 1
        session["current_chapter_idx"] = current_idx
        seq = session.get("chapter_sequence", [])
        
        if current_idx < len(seq):
            result["next_chapter"] = seq[current_idx]
        else:
            result["next_chapter"] = None
    else:
        result["next_chapter"] = chapter_id

    result["total_points"] = session.get("total_points", 0)
    result["chapters_completed"] = session.get("chapters_completed", 0)

    return jsonify(result)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",
                           total_points=session.get("total_points", 0),
                           chapters_completed=session.get("chapters_completed", 0),
                           story_id=session.get("story_id"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
