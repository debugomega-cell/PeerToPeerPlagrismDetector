PeerToPeer Plagiarism Detector
A Python-based web application that detects similarity between student submissions using Natural Language Processing (NLP). The app integrates with Google Classroom to fetch assignments, extract PDF content, and compute plagiarism scores using TF-IDF and cosine similarity.

🚀 Features
Google Classroom login via OAuth
Fetch student submissions automatically
Extract text from PDF files
Clean and preprocess text data
TF-IDF based similarity comparison
Pairwise plagiarism scoring
Simple Flask web dashboard
🧠 How It Works
Students submit assignments in Google Classroom.
The app downloads PDF submissions using Google Drive API.
Text is extracted and cleaned.
TF-IDF vectorization converts text to numerical form.
Cosine similarity detects matching content.
Results are displayed with similarity percentages.
🛠 Tech Stack
Python 3
Flask
scikit-learn (TF-IDF + cosine similarity)
PyPDF2
Google Classroom API
Google Drive API
📦 Installation
1. Clone the repository
git clone <your-repo-url>
cd PeerToPeerPlagiarismDetector
2. Create virtual environment (recommended)
Windows (PowerShell):

python -m venv venv
.\venv\Scripts\Activate
Mac/Linux:

python -m venv venv
source venv/bin/activate
⚡ Manual Dependency Installation
If you are not using requirements.txt, install packages manually:

pip install flask
pip install scikit-learn
pip install PyPDF2
pip install google-auth
pip install google-auth-oauthlib
pip install google-api-python-client
Optional — generate requirements file later:

pip freeze > requirements.txt
🔑 Google API Setup
Create a Google Cloud project.

Enable:

Google Classroom API
Google Drive API
Create OAuth credentials.

Download client_secret.json.

Place it in the project root directory.

▶ Run the App
python app.py
Open browser:

http://localhost:5000
📁 Project Structure
project/
│
├── app.py
├── requirements.txt (optional)
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
⚠ Notes
Designed for educational and hackathon use
Only PDF submissions are processed
Similarity threshold can be customized
🎯 Future Improvements
Multi-file format support
Highlight matching text segments
Database storage
Admin analytics dashboard
👨‍💻 Author
Hackathon project built for learning NLP and API integration.

📜 License
MIT License — free to use and modify.