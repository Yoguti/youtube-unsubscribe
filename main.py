import os
import subprocess
from youtube import youtube_upload_playlist

def convert_ts_to_mp4(ts_path, output_path):
    """
    Convert a .ts file to .mp4 using ffmpeg
    
    Args:
        ts_path (str): Path to the .ts file
        output_path (str): Path for the output .mp4 file
    
    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        subprocess.run([
            'ffmpeg', '-i', ts_path,
            '-c', 'copy',  # Copy streams without re-encoding
            '-bsf:a', 'aac_adtstoasc',  # Fix audio stream
            output_path
        ], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Conversion error: {e}")
        return False

def get_numbered_video_path(starting_path, number):
    """
    Find a .ts video file starting with the given number in the specified directory.
    
    Args:
        starting_path (str): Directory path to search in
        number (int): Number to look for at the start of filename
    
    Returns:
        str: Full path to the video if found, None otherwise
    """
    files = os.listdir(starting_path)
    for file in files:
        if file.startswith(f"{number}.") and file.endswith(".ts"):
            return os.path.join(starting_path, file)
    return None

def main():
    starting_path = "your/folder/path"  # Replace with your folder path
    temp_folder = os.path.join(starting_path, "temp_mp4")
    
    # Create temp folder if it doesn't exist
    os.makedirs(temp_folder, exist_ok=True)
    
    video_description = "desired description"
    privacy = "unlisted" #You may change this to public or private
    category = "22"  # Education category
    video_tags = [" tag1", " tag2", "tag3"]
    playlist_id = "your playlist id if needed"
    
    i = 1  # Start from 1 (1-indexed)
    uploaded_videos = set()  # Keep track of uploaded video numbers
    
    for _ in range(10):  # Maximum 10 API calls
        # Skip if we've already uploaded this video number
        if i in uploaded_videos:
            i += 1
            continue
            
        # Get the path for the current numbered video
        ts_path = get_numbered_video_path(starting_path, i)
        
        # If no video found for current number, stop the loop
        if ts_path is None:
            print(f"No video file found starting with number {i}. Stopping upload process.")
            break
        
        # Convert .ts to .mp4
        mp4_path = os.path.join(temp_folder, f"{i}.mp4")
        print(f"Converting {ts_path} to {mp4_path}...")
        
        if not convert_ts_to_mp4(ts_path, mp4_path):
            print(f"Conversion failed for video {i}")
            i += 1  # Move to next video on conversion failure
            continue
            
        video_title = f"Fluency Academy {i}"     
        try:
            video_id, playlist_success = youtube_upload_playlist(
                mp4_path,
                video_title,
                video_description,
                privacy,
                category,
                video_tags,
                playlist_id
            )
        
            if video_id:
                print(f"Video {i} uploaded successfully!")
                uploaded_videos.add(i)  # Mark this video number as uploaded
                
                if playlist_success:
                    print(f"Video {i} added to playlist successfully!")
                else:
                    print(f"Warning: Video {i} uploaded but failed to add to playlist")
                
                i += 1  # Move to next video after successful upload
            else:
                print(f"Video {i} upload failed")
                i += 1  # Move to next video on upload failure
        
        finally:
            # Clean up the temporary MP4 file
            if os.path.exists(mp4_path):
                os.remove(mp4_path)

    # Clean up temp folder
    try:
        os.rmdir(temp_folder)
    except OSError:
        print("Note: Could not remove temp folder (it might not be empty)")

if __name__ == "__main__":
    main()