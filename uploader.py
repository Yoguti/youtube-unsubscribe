# uploader.py

# Go to the end of file (main) or serch for "EDIT BELLOW" to change directory path and playlist id.

import os
import subprocess
from pathlib import Path
import time
from typing import Optional, Tuple
import pickle

# YouTube API imports
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http
import google.auth.transport.requests

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]

class VideoUploader:
    def __init__(self, source_dir: str, playlist_id: str):
        self.source_dir = Path(source_dir)
        self.temp_dir = self.source_dir / "temp_converted"
        self.playlist_id = playlist_id
        self.youtube = self._authenticate()
        self.temp_dir.mkdir(exist_ok=True)

    def _authenticate(self):
        """Handles YouTube API authentication with better error handling and token refresh."""
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        credentials = None
        token_path = Path("token.json")

        # Try to load existing token
        if token_path.exists():
            try:
                with open(token_path, "rb") as token_file:
                    credentials = pickle.load(token_file)
            except (EOFError, pickle.UnpicklingError, Exception) as e:
                print(f"Token file is corrupted or cannot be read: {e}")
                print("Removing corrupted token file and requesting new authentication.")
                token_path.unlink(missing_ok=True)
                credentials = None

        # Check if we need to refresh or create new credentials
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                try:
                    credentials.refresh(google.auth.transport.requests.Request())
                    # Save refreshed token
                    try:
                        with open(token_path, "wb") as token_file:
                            pickle.dump(credentials, token_file)
                    except Exception as e:
                        print(f"Failed to save refreshed token: {e}")
                except Exception as e:
                    print(f"Failed to refresh token: {e}")
                    credentials = None
            
            # If we still don't have valid credentials, run the flow
            if not credentials:
                try:
                    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                        "client.json",
                        SCOPES,
                        redirect_uri="http://localhost:8080/"
                    )
                    credentials = flow.run_local_server(
                        port=8080,
                        success_message="Authentication successful! You can close this window."
                    )
                    
                    # Save the new token with proper error handling
                    try:
                        with open(token_path, "wb") as token_file:
                            pickle.dump(credentials, token_file)
                    except Exception as e:
                        print(f"Failed to save new token: {e}")
                        raise Exception(f"Could not save authentication token: {e}")

                except Exception as e:
                    raise Exception(f"Authentication failed: {e}")

        return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)


    def convert_to_mp4(self, input_path: Path) -> Optional[Path]:
        if input_path.suffix.lower() == '.mp4':
            return input_path
            
        output_path = self.temp_dir / f"{input_path.stem}.mp4"
        try:
            subprocess.run([
                'ffmpeg',
                '-i', str(input_path),
                '-c', 'copy',
                '-movflags', '+faststart',
                '-y',
                str(output_path)
            ], check=True, capture_output=True)
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"Conversion failed for {input_path.name}: {e.stderr.decode()}")
            return None

    def upload_video(self, video_path: Path) -> Tuple[Optional[str], bool]:
        request_body = {
            "snippet": {
                "title": video_path.stem,
                "description": "Curso de inglês pirateado cracked denuvo escorrega um sobe dois da silva 2025 atualizado",
                "tags": ["Education"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "unlisted",
                "selfDeclaredMadeForKids": False
            }
        }

        media = googleapiclient.http.MediaFileUpload(
            str(video_path),
            chunksize=1024*1024,
            resumable=True
        )

        request = self.youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media
        )

        try:
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"Upload {video_path.name}: {int(status.progress() * 100)}%")
            
            video_id = response['id']
            playlist_success = self._add_to_playlist(video_id)
            return video_id, playlist_success

        except Exception as e:
            print(f"Upload failed for {video_path.name}: {str(e)}")
            return None, False

    def _add_to_playlist(self, video_id: str) -> bool:
        try:
            self.youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": self.playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            ).execute()
            return True
        except Exception as e:
            print(f"Failed to add to playlist: {str(e)}")
            return False

    def process_videos(self):
        for video_file in sorted(self.source_dir.glob("*.*")):
            if video_file.suffix.lower() not in ('.ts', '.mp4'):
                continue

            print(f"\nProcessing {video_file.name}")
            mp4_path = self.convert_to_mp4(video_file)
            if not mp4_path:
                continue

            video_id, playlist_success = self.upload_video(mp4_path)
            
            if mp4_path != video_file:  # Clean up converted file
                mp4_path.unlink(missing_ok=True)

            if video_id:
                print(f"Successfully uploaded: {video_file.name}")
                if playlist_success:
                    print("Added to playlist")
                else:
                    print("Failed to add to playlist")
            
            time.sleep(2)  # Prevent API rate limiting

        self.temp_dir.rmdir()

# EDIT BELLOW 

def main():
    source_dir = ""  # Change this, remember to the ABSOLUTE path to the directory
    playlist_id = "" # Not a full link, just the ID
    
    uploader = VideoUploader(source_dir, playlist_id)
    uploader.process_videos()

if __name__ == "__main__":
    main()