import os
import json
from datetime import datetime

def create_candidate_folder(name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_name = name.replace(" ", "_")
    folder_path = f"candidates/{safe_name}_{timestamp}"
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def save_candidate_data(data, resume_file):
    folder_path = create_candidate_folder(data["name"])
    
    # Save resume
    resume_path = os.path.join(folder_path, "resume.pdf")
    with open(resume_path, "wb") as f:
        f.write(resume_file.read())
    
    # Save metadata
    data["timestamp"] = datetime.now().isoformat()
    data_file = os.path.join(folder_path, "data.json")
    with open(data_file, "w") as f:
        json.dump(data, f, indent=4)

    return folder_path