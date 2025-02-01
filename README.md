# YouTube Video Upload Script

This is a simple Python script that allows you to upload videos to YouTube using the YouTube Data API. It handles the authentication process, video upload, and allows you to set basic video details such as title, description, tags, and privacy status.

## Requirements

Before using the script, make sure you have the following:

- Python 3.x
- [Google API Python Client](https://pypi.org/project/google-api-python-client/)
- [Google Auth Library for Python](https://pypi.org/project/google-auth/)
- [OAuth 2.0 Client Secrets](https://console.developers.google.com/) to access the YouTube Data API

## Setup

1. Clone or download this repository to your local machine.
2. Install the necessary Python libraries:

   ```
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

3. Create a project in the [Google Developer Console](https://console.developers.google.com/).
4. Enable the YouTube Data API v3 for your project.
5. Download the `client.json` file containing your OAuth 2.0 client secrets.
6. Place the `client.json` file in the project directory.
7. The first time you run the script, it will prompt you to authenticate your Google account. After successful authentication, a `token.json` file will be created to store your credentials for future use.

## Usage

### Upload a Video

To upload a video to YouTube, call the `youtube_upload()` function in the script:

```python
youtube_upload(
    path="path_to_your_video.mp4",  # Path to the video file
    title="Your Video Title",       # Title of the video
    description="Your Video Description",  # Description of the video
    privacy_status="public",  # Privacy status: "public", "private", or "unlisted"
    category_id="22",         # YouTube video category ID
    tags=["tag1", "tag2"]     # Tags for the video
)
```

### Parameters

- `path`: Path to the video file you want to upload.
- `title`: The title of your video.
- `description`: A description of the video.
- `privacy_status`: Video privacy status. Can be `"private"`, `"unlisted"`, or `"public"`.
- `category_id`: The YouTube category ID for the video. You can find a list of category IDs [here](https://developers.google.com/youtube/v3/docs/videoCategories/list).
- `tags`: A list of tags for your video.

The function will return the video ID if the upload is successful.

## Notes

- The script uses OAuth 2.0 authentication to interact with your YouTube account.
- The upload process is resumable, meaning if the upload is interrupted, it will resume from where it left off.
- The `token.json` file stores your OAuth credentials, so you won't need to authenticate every time you run the script (unless the token expires).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
