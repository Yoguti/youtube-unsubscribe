# youtube.py
import os
import google_auth_httplib2
import google_auth_oauthlib
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
import google.auth.transport.requests
import pickle

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl"  # Added for playlist manipulation
    "https://www.googleapis.com/auth/youtube" # Necessary for full manipulation
]
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

def add_to_playlist(youtube, playlist_id, video_id):
    """
    Add a video to a specified playlist.
    
    Args:
        youtube: Authenticated YouTube API service
        playlist_id (str): ID of the target playlist
        video_id (str): ID of the video to add
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        request_body = {
            'snippet': {
                'playlistId': playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
        }
        
        youtube.playlistItems().insert(
            part='snippet',
            body=request_body
        ).execute()
        
        print(f"Video {video_id} added to playlist {playlist_id}")
        return True
    except Exception as e:
        print(f"Error adding video to playlist: {e}")
        return False

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

def youtube_upload_playlist(path, title, description, privacy_status, category_id, tags, playlist_id):
    """
    Upload a video to YouTube and add it to a specified playlist.
    
    Args:
        path (str): Path to the video file
        title (str): Title of the video
        description (str): Description of the video
        privacy_status (str): Privacy status ("private", "unlisted", or "public")
        category_id (str): YouTube video category ID
        tags (list): List of tags for the video
        playlist_id (str): ID of the playlist to add the video to
    
    Returns:
        tuple: (video_id, playlist_success) where video_id is the uploaded video's ID
               and playlist_success is a boolean indicating if the video was added to the playlist
    """
    youtube = authenticate_youtube()
    
    # First upload the video
    video_id = upload_video(youtube, path, {
        "categoryId": category_id,
        "title": title,
        "description": description,
        "tags": tags
    }, privacy_status)
    
    if video_id:
        # If video upload successful, add to playlist
        playlist_success = add_to_playlist(youtube, playlist_id, video_id)
        return video_id, playlist_success
    
    return None, False