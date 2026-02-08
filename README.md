# PeerToPeer Plagiarism Detector

A Python-based web application that detects similarity between student submissions using Natural Language Processing (NLP). The app integrates with Google Classroom to fetch assignments, extract PDF content, and compute plagiarism scores using TF-IDF and cosine similarity.

---

## 🚀 Features

* Google Classroom login via OAuth
* Fetch student submissions automatically
* Extract text from PDF files
* Clean and preprocess text data
* TF-IDF based similarity comparison
* Pairwise plagiarism scoring
* Simple Flask web dashboard

---

## 🧠 How It Works

1. Students submit assignments in Google Classroom.
2. The app downloads PDF submissions using Google Drive API.
3. Text is extracted and cleaned.
4. TF-IDF vectorization converts text to numerical form.
5. Cosine similarity detects matching content.
6. Results are displayed with similarity percentages.

---

## 🛠 Tech Stack

* Python 3
* Flask
* scikit-learn (TF-IDF + cosine similarity)
* PyPDF2
* Google Classroom API
* Google Drive API

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd PeerToPeerPlagiarismDetector
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Google API Setup

1. Create a Google Cloud project.
2. Enable:

   * Google Classroom API
   * Google Drive API
3. Create OAuth credentials.
4. Download `client_secret.json`.
5. Place it in the project root directory.

---

## ▶ Run the App

```bash
python app.py
```

Open browser:

```
http://localhost:5000
```

---

## 📁 Project Structure

```
project/
│
├── app.py
├── requirements.txt
├── client_secret.json
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── assignments.html
│   └── submissions.html
│
└── static/
```

---

## ⚠ Notes

* Designed for educational and hackathon use.
* Only PDF submissions are processed.
* Similarity threshold can be customized in the code.

---

## 🎯 Future Improvements

* Multi-file format support
* Highlight matching text segments
* Database storage
* Admin analytics dashboard

---

## 👨‍💻 Author

Hackathon project built for learning NLP + API integration.

---

## 📜 License

MIT License — free to use and modify.
