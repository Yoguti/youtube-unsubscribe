from youtube import youtube_upload_playlist

def main():

    video_path = "/home/ks/Documents/code/youtube-video-uploader/rapidsave.com_pvp-dd2g3ww8ycfe1.mp4"
    video_title = "Fluency Academy "
    video_description = "Video from English Course Week 1"
    privacy = "unlisted"
    category = "22"  # Education category
    video_tags = ["Fluency Academy", "English Course", "Education"]
    playlist_id = "PL-DjAWICHavzvGNCeLxTIcbXuTsrZolBS"
    
    i = 0
    for _ in range(10):
        video_title = "Fluency Academy {}".format(i)

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
            print("Video uploaded and added to playlist successfully!")
            i += 1

        elif video_id:
            print("Video uploaded but failed to add to playlist")
        else:
            print("Video upload failed")

if __name__ == "__main__":
    main()