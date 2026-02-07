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
