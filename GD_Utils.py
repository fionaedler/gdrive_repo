import os
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

class GDUtils():
    def __init__(self):
        self.creds = None
        self.service = None

    def verify_creds(self):
        SCOPES = ["https://www.googleapis.com/auth/drive"]
        print("checking credentials")

        tokens_path = "C:/Users/fiona/Documents/FIONA/Coding/Rebelway_Python_for_Production/gdrive_test/tokens.json"
        creds_path = "C:/Users/fiona/Documents/FIONA/Coding/Rebelway_Python_for_Production/gdrive_test/credentials.json"

        if os.path.exists(tokens_path):
            self.creds = Credentials.from_authorized_user_file(tokens_path, SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                print("creds expired, refreshing..")
                self.creds.refresh(Request())
            else:
                print("loading creds")
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_path, SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open(tokens_path, "w") as token:
                token.write(self.creds.to_json())

    def check_dest_dir(self, gd_dest_dir):
        try:
            self.service = build("drive", "v3", credentials=self.creds)

            response = self.service.files().list(
                q=f"name='{gd_dest_dir}' and mimeType='application/vnd.google-apps.folder'", spaces='drive').execute()

            if not response["files"]:
                dir_metadata = {
                    "name": f"{gd_dest_dir}",
                    "mimeType": "application/vnd.google-apps.folder"
                }

                dir = self.service.files().create(body=dir_metadata, fields="id").execute()
                folder_id = dir.get("id")
                print(f"Folder {gd_dest_dir} created")
            else:
                folder_id = response["files"][0]["id"]
                print(f"Folder {gd_dest_dir} found")

            return folder_id

        except HttpError as e:
            print("Error: " + str(e))


    def upload_files(self, file_path, gd_dest_dir, parent_id):
        file = file_path.split("/")[-1]

        file_metadata = {"name": file, "parents": [parent_id]}
        media = MediaFileUpload(f"{file_path}")
        upload_file = self.service.files().create(body=file_metadata,
                                             media_body=media,
                                             fields="id").execute()
        print("Uploaded file: " + file)

    def upload(self, src_dir, gd_des_dir, parent_id):
        is_file = os.path.isfile(src_dir)

        if is_file:
            self.upload_files(src_dir, gd_des_dir, parent_id)
        else:
            for file in os.listdir(src_dir):
                self.upload_files(f"{src_dir}/{file}", gd_des_dir, parent_id)


def execute():
    print("----- running GD_Utils -----")

    upload_dir = "C:/Users/fiona/Desktop/GD_test"
    dest_folder = "BackupFolder2024"
    GD = GDUtils()
    GD.verify_creds()
    parent_id = GD.check_dest_dir(dest_folder)
    GD.upload_files(upload_dir, dest_folder, parent_id)

    print("----- done -----")


