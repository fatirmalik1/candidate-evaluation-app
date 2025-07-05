import os
import json
from datetime import datetime
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# Load credentials from Streamlit secrets
key_dict = json.loads(st.secrets["gdrive_service_account"])
credentials = service_account.Credentials.from_service_account_info(
    key_dict, scopes=["https://www.googleapis.com/auth/drive"]
)
drive_service = build("drive", "v3", credentials=credentials)

# ID of your target Google Drive folder (shared with the service account)
DRIVE_FOLDER_ID = "1k39Yduk3exr3EbTJm4OBLY8fBhvZAP2H"

def upload_to_drive(filename, content, mimetype):
    file_metadata = {
        "name": filename,
        "parents": [DRIVE_FOLDER_ID]
    }
    media = MediaIoBaseUpload(io.BytesIO(content), mimetype=mimetype, resumable=True)
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return uploaded_file.get("id")

def save_candidate_data(data, resume_file):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_filename = f"{data['name'].replace(' ', '_')}_{timestamp}"

    # Save resume
    resume_content = resume_file.read()
    resume_filename = f"{base_filename}_resume.pdf"
    upload_to_drive(resume_filename, resume_content, "application/pdf")

    # Save metadata
    data["timestamp"] = datetime.now().isoformat()
    metadata_json = json.dumps(data, indent=4).encode("utf-8")
    metadata_filename = f"{base_filename}_data.json"
    upload_to_drive(metadata_filename, metadata_json, "application/json")

    return f"Uploaded to Google Drive folder with base name: {base_filename}"
