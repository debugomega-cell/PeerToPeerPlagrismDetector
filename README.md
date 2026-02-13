# Peer-to-Peer Plagiarism Detector

A Python-based web application that detects similarity between student submissions using Natural Language Processing (NLP). The system compares uploaded documents and calculates plagiarism scores using TF-IDF vectorization and cosine similarity.

The app is designed for academic use and can integrate with Google Classroom to fetch submissions automatically.

---

## 🚀 Features

* Upload and compare multiple documents
* Automatic text cleaning & preprocessing
* TF-IDF similarity scoring
* Cosine similarity plagiarism detection
* PDF text extraction
* Optional Google Classroom integration
* Clean web dashboard interface

---

## 🛠 Tech Stack

Frontend:

* HTML / CSS / JavaScript

Backend:

* Python
* Flask

Libraries:

* Scikit-learn
* NumPy
* PDF processing tools

Deployment:

* Render

---

## 📂 Project Structure

peer-plagiarism/
│
├── app.py
├── requirements.txt
├── Procfile
├── templates/
├── static/
└── README.md

---

## ⚙ Installation (Local Setup)

### 1. Clone the repository

git clone https://github.com/your-username/peer-plagiarism.git
cd peer-plagiarism

### 2. Create virtual environment

python -m venv venv

Activate environment:

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the app

python app.py

Open browser:

http://127.0.0.1:5000

---

## 🌐 Deployment (Render)

### Step 1 — Prepare files

Create requirements.txt:

pip freeze > requirements.txt

Create Procfile:

web: gunicorn app:app

---

### Step 2 — Push to GitHub

git init
git add .
git commit -m "deploy app"
git push

---

### Step 3 — Deploy on Render

1. Go to https://render.com
2. Login with GitHub
3. New → Web Service
4. Select repository

Settings:

Build command:
pip install -r requirements.txt

Start command:
gunicorn app:app

Click **Deploy**.

Render will generate a public URL:

https://your-app-name.onrender.com

---

## 🔐 Google Classroom Integration (Optional)

If using OAuth:

Update redirect URI in Google Cloud Console:

https://your-app-name.onrender.com/callback

---

## 📊 How Plagiarism Detection Works

1. Extract text from documents
2. Clean and normalize text
3. Convert to TF-IDF vectors
4. Compute cosine similarity
5. Display plagiarism percentage

---

## 🧠 Future Improvements

* Real-time classroom sync
* AI-based semantic comparison
* Report export system
* Teacher dashboard analytics

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you’d like to improve.

---

## 📜 License

This project is for educational purposes. Modify and use freely.

---

## ✨ Author

Developed as a peer-to-peer plagiarism detection tool to support academic integrity.
