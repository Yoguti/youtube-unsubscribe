import os
import subprocess
from youtube import youtube_upload_playlist
import time
from datetime import datetime

def convert_ts_to_mp4(ts_path, output_path):
    """
    Convert a .ts file to .mp4 using ffmpeg with minimal overhead
    
    Args:
        ts_path (str): Path to the .ts file
        output_path (str): Path for the output .mp4 file
    
    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        start_time = time.time()
        
        result = subprocess.run([
            'ffmpeg',
            '-progress', '-',
            '-nostats',
            '-i', ts_path,
            '-c', 'copy',
            '-bsf:a', 'aac_adtstoasc',
            '-movflags', '+faststart',
            output_path
        ], check=True, capture_output=True, text=True)
        
        elapsed_time = time.time() - start_time
        if os.path.exists(output_path):
            print(f"Conversion completed in {elapsed_time:.2f} seconds")
            return True
            
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"Conversion error: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

def get_numbered_video_path(starting_path, number):
    """
    Find a .ts video file starting with the given number in the specified directory.
    """
    files = os.listdir(starting_path)
    for file in files:
        if file.startswith(f"{number}.") and file.endswith(".ts"):
            return os.path.join(starting_path, file)
    return None

def get_file_name_without_extension(file_path):
    """
    Get the filename without extension and number prefix
    """
    base_name = os.path.basename(file_path)
    # Remove the extension
    name_without_ext = os.path.splitext(base_name)[0]
    # Remove the number prefix and dot
    parts = name_without_ext.split('.', 1)
    if len(parts) > 1:
        return parts[1].strip()
    return name_without_ext

def main():
    starting_path = "/home/ks/Downloads/Fluency Academy - Inglês 2.0 - Rhavi Carneiro/1.UNIT 01/"
    temp_folder = os.path.join(starting_path, "temp_mp4")
    
    os.makedirs(temp_folder, exist_ok=True)
    
    video_description = "Curso de inglês pirateado cracked denuvo escorrega um sobe dois da silva 2025 atualizado"
    privacy = "unlisted"
    category = "22"  # Education category
    video_tags = ["Fluency Academy", "English Course", "Education"]
    playlist_id = "PL-DjAWICHavzvGNCeLxTIcbXuTsrZolBS"
    
    i = 1
    uploaded_videos = set()
    
    for _ in range(10):
        if i in uploaded_videos:
            i += 1
            continue
            
        ts_path = get_numbered_video_path(starting_path, i)
        
        if ts_path is None:
            print(f"No video file found starting with number {i}. Stopping upload process.")
            break
        
        mp4_path = os.path.join(temp_folder, f"{i}.mp4")
        print(f"Converting {ts_path} to {mp4_path}...")
        
        if not convert_ts_to_mp4(ts_path, mp4_path):
            print(f"Conversion failed for video {i}")
            i += 1
            continue
        
        # Use the original filename for the video title
        video_title = get_file_name_without_extension(ts_path)
        
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
                uploaded_videos.add(i)
                
                if playlist_success:
                    print(f"Video {i} added to playlist successfully!")
                else:
                    print(f"Warning: Video {i} uploaded but failed to add to playlist")
                
                i += 1
            else:
                print(f"Video {i} upload failed")
                i += 1
        
        finally:
            if os.path.exists(mp4_path):
                os.remove(mp4_path)

    try:
        os.rmdir(temp_folder)
    except OSError:
        print("Note: Could not remove temp folder (it might not be empty)")

if __name__ == "__main__":
    main()