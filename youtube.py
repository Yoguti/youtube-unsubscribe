import os
import google_auth_httplib2
import google_auth_oauthlib
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
import google.auth.transport.requests
import pickle

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = 'token.json'

def authenticate_youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    credentials = None
    
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            credentials = pickle.load(token)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                "client.json",
                SCOPES,
                redirect_uri="http://localhost:8080/"
            )
            credentials = flow.run_local_server(
                port=8080,
                success_message="Authentication successful! You can close this window."
            )
        
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(credentials, token)
    
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_video(youtube, file_path, snippet_info, privacy_status):
    request_body = {
        "snippet": snippet_info,
        "status": {
            "privacyStatus": privacy_status
        }
    }
    
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=googleapiclient.http.MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    
    response = None
    print("Starting upload...")
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"Upload {int(status.progress()*100)}%")
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    
    if response:
        print(f"Video uploaded with ID: {response['id']}")
        return response['id']
    return None

def youtube_upload(path, title, description, privacy_status, category_id, tags):
    """
    Upload a video to YouTube.
    
    Args:
        path (str): Path to the video file
        title (str): Title of the video
        description (str): Description of the video
        privacy_status (str): Privacy status ("private", "unlisted", or "public")
        category_id (str): YouTube video category ID
        tags (list): List of tags for the video
    
    Returns:
        str: Video ID if upload successful, None otherwise
    """
    snippet_info = {
        "categoryId": category_id,
        "title": title,
        "description": description,
        "tags": tags
    }

    youtube = authenticate_youtube()
    return upload_video(youtube, path, snippet_info, privacy_status)