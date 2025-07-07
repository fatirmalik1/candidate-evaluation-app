import os
import io
import json
from datetime import datetime
import streamlit as st
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import pkg_resources

# 📁 Shared Drive parent folder ID (update if needed)
PARENT_FOLDER_ID = "1PZ6fnX1on99379B9CGRuYEl6zbLqcpqV"

def create_candidate_folder(name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_name = name.replace(" ", "_")
    folder_name = f"{safe_name}_{timestamp}"
    return folder_name

def get_drive():
    gauth = GoogleAuth()

    # Use Streamlit secrets if running in cloud
    try:
        if "gdrive_service_account" in st.secrets:
            from tempfile import NamedTemporaryFile
            key_dict = st.secrets["gdrive_service_account"]

            # Save service account secret to temp file
            with NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as temp_file:
                json.dump(key_dict, temp_file)
                temp_file.flush()
                gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
                    temp_file.name,
                    scopes=["https://www.googleapis.com/auth/drive"]
                )
                return GoogleDrive(gauth)
    
    except FileNotFoundError:
        pass
    
    # Local credentials.json
    CREDENTIALS_PATH = pkg_resources.resource_filename(__name__, "credentials.json")
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_PATH,
        scopes=["https://www.googleapis.com/auth/drive"]
    )

    return GoogleDrive(gauth)

def upload_to_gdrive(folder_name, resume_file_bytes, metadata_dict):
    drive = get_drive()

    # Check if folder already exists
    folder_id = None
    folder_list = drive.ListFile({'q': f"'{PARENT_FOLDER_ID}' in parents and trashed=false"}).GetList()
    for f in folder_list:
        if f['title'] == folder_name:
            folder_id = f['id']

    # Create folder if not found
    if folder_id is None:
        folder_meta = {
            "title": folder_name,
            "parents": [{"id": PARENT_FOLDER_ID}],
            "mimeType": "application/vnd.google-apps.folder"
        }
        folder = drive.CreateFile(folder_meta)
        folder.Upload()
        folder_id = folder['id']

    # Upload resume.pdf
    resume = drive.CreateFile({'title': 'resume.pdf', 'parents': [{"id": folder_id}]})
    resume.content = io.BytesIO(resume_file_bytes)
    resume.Upload()

    # Upload data.json
    data_json = drive.CreateFile({'title': 'data.json', 'parents': [{"id": folder_id}]})
    data_json.SetContentString(json.dumps(metadata_dict, indent=4))
    data_json.Upload()

    return folder_id

def save_candidate_data(data, resume_file):
    folder_name = create_candidate_folder(data["name"])
    resume_content = resume_file.read()
    data["timestamp"] = datetime.now().isoformat()

    # Upload both resume and metadata
    folder_id = upload_to_gdrive(folder_name, resume_content, data)

    return f"https://drive.google.com/drive/folders/{folder_id}"
