from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, redirect, request, render_template, session
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from PyPDF2 import PdfReader
import os
import io
import re


app = Flask(__name__)
app.secret_key = "dev_secret_key"

# Allow HTTP for local development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

# ---------- HELPERS ----------

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9 ]", "", text)
    return text.strip()

def get_credentials():
    if "credentials" not in session:
        return None

    return Credentials(
        token=session["credentials"]["token"],
        refresh_token=session["credentials"]["refresh_token"],
        token_uri=session["credentials"]["token_uri"],
        client_id=session["credentials"]["client_id"],
        client_secret=session["credentials"]["client_secret"],
        scopes=session["credentials"]["scopes"],
    )

def extract_text_from_drive_pdf(file_id, credentials):
    drive_service = build("drive", "v3", credentials=credentials)
    request = drive_service.files().get_media(fileId=file_id)
    file_stream = io.BytesIO()

    downloader = MediaIoBaseDownload(file_stream, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    file_stream.seek(0)
    reader = PdfReader(file_stream)

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    return text.strip()

def compute_plagiarism(submissions):
    texts = [clean_text(s["full_text"]) for s in submissions]
    users = [s["userId"] for s in submissions]

    if len(texts) < 2:
        return []

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    results = []

    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            score = similarity_matrix[i][j] * 100

            if score > 15:
                results.append({
                    "student_1": users[i],
                    "student_2": users[j],
                    "similarity": round(score, 2),
                    "text_1": submissions[i]["preview"],
                    "text_2": submissions[j]["preview"]
                })

    return results


# ---------- ROUTES ----------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/logintogoogle")
def login():
    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
        redirect_uri=request.url_root + "oauth2callback"

    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent"
    )

    session["state"] = state
    return redirect(authorization_url)

@app.route("/oauth2callback")
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES,
        redirect_uri=request.url_root + "oauth2callback"

    )

    flow.fetch_token(authorization_response=request.url)

    session["credentials"] = {
        "token": flow.credentials.token,
        "refresh_token": flow.credentials.refresh_token,
        "token_uri": flow.credentials.token_uri,
        "client_id": flow.credentials.client_id,
        "client_secret": flow.credentials.client_secret,
        "scopes": flow.credentials.scopes,
    }

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    credentials = get_credentials()
    if not credentials:
        return redirect("/")

    classroom = build("classroom", "v1", credentials=credentials)
    courses_response = classroom.courses().list().execute()
    courses = courses_response.get("courses", [])

    simplified_courses = [
        {"id": c["id"], "name": c["name"]}
        for c in courses
    ]

    return render_template("dashboard.html", courses=simplified_courses)

@app.route("/course/<course_id>")
def course_assignments(course_id):
    credentials = get_credentials()
    if not credentials:
        return redirect("/")

    classroom = build("classroom", "v1", credentials=credentials)
    coursework_response = classroom.courses().courseWork().list(
        courseId=course_id
    ).execute()

    assignments = coursework_response.get("courseWork", [])

    simplified_assignments = [
        {"id": w["id"], "title": w["title"]}
        for w in assignments
    ]

    return render_template(
        "assignments.html",
        assignments=simplified_assignments,
        course_id=course_id
    )

@app.route("/submissions/<course_id>/<coursework_id>")
def submissions(course_id, coursework_id):
    credentials = get_credentials()
    if not credentials:
        return redirect("/")

    classroom = build("classroom", "v1", credentials=credentials)

    submissions_response = classroom.courses().courseWork().studentSubmissions().list(
        courseId=course_id,
        courseWorkId=coursework_id
    ).execute()

    submissions_data = submissions_response.get("studentSubmissions", [])
    extracted = []

    for s in submissions_data:
        if s.get("state") != "TURNED_IN":
            continue

        assignment = s.get("assignmentSubmission", {})
        attachments = assignment.get("attachments", [])

        for a in attachments:
            drive_file = a.get("driveFile")
            if not drive_file:
                continue

            file_id = drive_file["id"]
            file_name = drive_file["title"]

            try:
                text = extract_text_from_drive_pdf(file_id, credentials)
            except Exception:
                text = ""

            extracted.append({
                "userId": s.get("userId"),
                "fileName": file_name,
                "full_text": text,
                "preview": text[:1500]
            })

    plagiarism_results = compute_plagiarism(extracted)
    plagiarism_results.sort(key=lambda x: x["similarity"], reverse=True)

    return render_template(
        "submissions.html",
        submissions=extracted,
        plagiarism=plagiarism_results,
        course_id=course_id
    )

# ---------- RUN ----------

if __name__ == "__main__":
    app.run(debug=True)
