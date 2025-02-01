from youtube import youtube_upload

def main():
    video_path = "/path/to/your/video.mp4"
    video_title = "My Video Title"
    video_description = "Video from English Course Week 1"
    privacy = "private"
    category = "22"  # Education category
    video_tags = ["Fluency Academy", "English Course", "Education"]
    
    video_id = youtube_upload(
        video_path,
        video_title,
        video_description,
        privacy,
        category,
        video_tags
    )

if __name__ == "__main__":
    main()