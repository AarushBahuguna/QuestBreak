# ⚔️ QuestBreak AI

An AI-powered, story-based **anti-doomscrolling web application**. QuestBreak transforms passive screen time into an interactive treasure hunt where users solve riddles, upload real-world photos, and complete challenges—all verified dynamically by local Machine Learning models.

---

## 🌟 Key Features

*   **Story-Based Profiling**: Users answer an interactive questionnaire. A custom Machine Learning pipeline (SVM/K-Means) maps their responses across 5 personality traits to assign them to one of 4 unique storylines.
*   **Massive Content Pool**: 4 distinct themes (Adventure, Fantasy, Sci-Fi, Espionage) featuring **80 unique chapters/challenges** total.
*   **Endless Replayability**: Every time you start or replay a story, the backend dynamically sequences a random path of 5 chapters. No two playthroughs are exactly alike.
*   **Intelligent Answer Verification**:
    *   **Text/Riddles**: Evaluated locally using **NLP** (TF-IDF Vectorization & Cosine Similarity via `scikit-learn`) to detect semantically correct answers even with typos or phrasing variations.
    *   **Image Challenges**: Evaluated using **Deep Learning** (MobileNetV2 via `TensorFlow`). The app actually "sees" your photo to verify you've completed real-world challenges (e.g., taking a picture of a key, a plant, or a bottle).
*   **Modern UI**: Fully responsive, dark-mode glassmorphism interface with smooth JavaScript transitions.

---

## 🛠️ Tech Stack

*   **Backend framework**: Python 3, Flask
*   **Machine Learning**: `scikit-learn`, `pandas`, `numpy`, `imbalanced-learn` (SMOTE)
*   **Deep Learning / Computer Vision**: `tensorflow` (MobileNetV2)
*   **Frontend**: HTML5 (Jinja2 Templates), Vanilla CSS3, Vanilla JavaScript

---

## 🚀 How to Run Locally

### 1. Set up the Environment
It is highly recommended to use a virtual environment to manage dependencies.
```bash
# Create a virtual environment
python3 -m venv .venv

# Activate it (Linux/Mac)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate the Story Database (Optional)
The project comes with a Python script to procedurally generate the 80 chapters.
```bash
python generate_stories.py
```
*(This will overwrite `stories.json` with a fresh batch of content).*

### 4. Start the Application
```bash
python app.py
```
The server will start on `http://127.0.0.1:5000`. Open this address in your web browser.

---

## 📂 Project Structure

*   `app.py`: The Flask server and routing logic.
*   `QuestBreakApp.py`: The central orchestrator connecting the web routes to the AI models.
*   `answer_checker.py`: NLP text checking logic and routing to the image verifier.
*   `cnn_verifier.py`: Loads the TensorFlow MobileNetV2 architecture for real-world object detection.
*   `ml_classifier.py` / `data_pipeline.py`: Code for training the SVM/K-Means models on user behavior data.
*   `generate_stories.py`: A database script that populates the 80 text and image challenges into `stories.json`.
*   `templates/` & `static/`: HTML views, CSS styling, and JavaScript logic.

---

## 🧠 AI/ML Concepts Applied
This project maps to core Artificial Intelligence & Machine Learning outcomes:
*   **Supervised & Unsupervised Learning**: Logistic Regression, Random Forest, SVM, K-Means Clustering.
*   **Natural Language Processing (NLP)**: TF-IDF feature extraction.
*   **Deep Learning Neural Networks**: Convolutional Neural Networks (CNNs) & Transfer Learning (MobileNetV2).
*   **Data Processing**: Handled missing values, outliers, log normalization, and class balancing using SMOTE.
