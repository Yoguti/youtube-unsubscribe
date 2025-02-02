import os
from youtube import youtube_upload_playlist

def get_numbered_video_path(starting_path, number):
    """
    Find a video file starting with the given number in the specified directory.
    
    Args:
        starting_path (str): Directory path to search in
        number (int): Number to look for at the start of filename
    
    Returns:
        str: Full path to the video if found, None otherwise
    """
    # Get all files in the directory
    files = os.listdir(starting_path)
    
    # Look for files starting with the number
    for file in files:
        if file.startswith(f"{number}."):
            return os.path.join(starting_path, file)
    
    return None

def main():
    starting_path = "/path/to/your/video/folder"  # Replace with your folder path
    video_description = "Video from English Course Week 1"
    privacy = "unlisted"
    category = "22"  # Education category
    video_tags = ["Fluency Academy", "English Course", "Education"]
    playlist_id = "PL-DjAWICHavzvGNCeLxTIcbXuTsrZolBS"
    
    i = 0
    for _ in range(10):  # Maximum 10 API calls
        # Get the path for the current numbered video
        video_path = get_numbered_video_path(starting_path, i)
        
        # If no video found for current number, stop the loop
        if video_path is None:
            print(f"No video file found starting with number {i}. Stopping upload process.")
            break
            
        video_title = f"Fluency Academy {i}"
        
        video_id, playlist_success = youtube_upload_playlist(
            video_path,
            video_title,
            video_description,
            privacy,
            category,
            video_tags,
            playlist_id
        )
    
        if video_id and playlist_success:
            print(f"Video {i} uploaded and added to playlist successfully!")
            i += 1
        elif video_id:
            print(f"Video {i} uploaded but failed to add to playlist")
        else:
            print(f"Video {i} upload failed")

if __name__ == "__main__":
    main()