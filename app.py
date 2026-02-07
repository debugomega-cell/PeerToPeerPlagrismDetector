from flask import Flask, redirect, request, render_template, session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from PyPDF2 import PdfReader

import os
import io
import re


# ---------- APP SETUP ----------

app = Flask(__name__)
app.secret_key = "dev_secret_key"

# Allow HTTP during local testing
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# ---------- GOOGLE SCOPES ----------

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]


# ---------- routes ----------

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
        redirect_uri="http://localhost:5000/oauth2callback"
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
        redirect_uri="http://localhost:5000/oauth2callback"
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
