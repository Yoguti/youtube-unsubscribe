# YouTube Uploader

This project is a Python-based tool to automate the process of uploading videos to YouTube, converting `.ts` (MPEG-TS) files to `.mp4`, and managing playlists (If your files are already in .mp4 format, the script will skip conversion). It is designed to convert a sequence of `.ts` files into `.mp4` and upload them to a YouTube playlist, streamlining the upload process for video content.

## Features

- **Convert .ts to .mp4:** Convert `.ts` files to `.mp4` using `ffmpeg` without re-encoding the video.
- **Upload to YouTube:** Upload converted `.mp4` videos to YouTube with customizable metadata (title, description, privacy settings, etc.).
- **Playlist Management:** Optionally add uploaded videos to a predefined YouTube playlist.

# Prerequisites

Before you begin using this script, make sure you have the following:

- **Google Developer Console Project**: Create a project and enable the YouTube Data API v3.
- **OAuth 2.0 Credentials**: Obtain your OAuth 2.0 Client ID and Client Secret.
- **Python Environment**: Ensure that Python is installed on your system.

---

# Getting Started

## Step 1: Set Up Google Developer Console

1. **Navigate to the Developer Console**  
   Visit the [Google Developer Console](https://console.developers.google.com/).

2. **Create a New Project**  
   - Click on the "Select Project" dropdown at the top of the page.
   - Click "New Project", give it a name, and create the project.

3. **Enable YouTube Data API v3**  
   - Go to the "API & Services" dashboard in the sidebar.
   - Click "Enable APIs and Services".
   - In the search bar, type "YouTube Data API v3" and select it.
   - Click "Enable" to activate the API for your project.

4. **Set Up OAuth Consent Screen**  
   - In the sidebar, click "OAuth consent screen".
   - Select the "External" user type.
   - Fill in the required fields, such as your app name and support email.

5. **Create OAuth 2.0 Credentials**  
   - Go to the "Credentials" tab in the sidebar.
   - Click "Create Credentials" and choose "OAuth 2.0 Client IDs".
   - Once created, download the credentials file in JSON format and save it securely on your system.

---

Make sure you've completed these steps before moving on to the next parts of the script setup.


## Requirements

- Python 3.x
- `ffmpeg` installed and accessible via the command line
- YouTube API credentials (for uploading to YouTube)

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/youtube-uploader.git
    cd youtube-uploader
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Set up YouTube API credentials by following [Google's YouTube API guide](https://developers.google.com/youtube/registering_an_application) and store your `client_secret.json` in the project directory.

4. Replace the placeholder values in the `main()` function with your specific details:
    - `starting_path`: Path to the directory containing `.ts` files
    - `video_description`: Description to be used for the video
    - `privacy`: Set the privacy of the uploaded video (`public`, `private`, or `unlisted`)
    - `category`: YouTube category (e.g., `22` for Education)
    - `video_tags`: List of tags for the video
    - `playlist_id`: The ID of the playlist (if applicable)

## Usage

1. Place your `.ts` video files in the specified directory.
2. Run the script:
    ```
    python main.py
    ```

## Notes

- The script processes a maximum of 10 videos at a time. Adjust the loop in `main()` for different use cases.
- Temporary `.mp4` files are saved in a `temp_mp4` folder and removed after the upload.
- Failed uploads or conversions will be skipped, and the script will continue with the next video.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
